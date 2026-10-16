"""Every sound of a short, and the stems + mix.
usage: python audio.py s1  -> reads cut.json, gfx/sfx_events.json (+ the gfx pages' reveals), <sk>/events_extra.json,
                              <sk>/music/pick.json ; writes <sk>/stems/*.wav, <sk>/mix.wav, <sk>/music.json, <sk>/sfx_log.json
SFX: real recordings from the skill's royalty-free library (assets/sfx, sfxlib.py: rotated, whooshes and risers land
their loudest moment on the cut). Without the library, the synthesized sounds below stand in.
Music: the generated take music_takes.py picked (or shorts.json music.file); without one, the synthesized bed (music.py)."""
import json, sys, os, re, glob, zlib, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal
sys.path.insert(0, 'scripts'); import sfxlib
SR = 48000
sk = sys.argv[1]
C = json.load(open('cut.json', encoding='utf-8'))[sk]
SH = json.load(open('shorts.json', encoding='utf-8'))[sk]
END = C['END']; N = int(round(END * SR))
JOIN = C['runs'][0]['T1']                       # the hook -> first point join: riser, sting and music lift land here
rng = np.random.default_rng(7)
voice, _ = sf.read(f'{sk}/voice.wav'); voice = voice.astype(np.float32)
if voice.ndim == 1: voice = np.stack([voice, voice], 1)
if len(voice) < N: voice = np.pad(voice, ((0, N - len(voice)), (0, 0)))
voice = voice[:N]
vpeak = np.abs(voice).max()
meter = pyln.Meter(SR)

def env_exp(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))

def norm(x):
    m = np.abs(x).max(); return x / m if m > 0 else x

def lp(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), 'low'); return signal.lfilter(b, a, x)

def hp(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), 'high'); return signal.lfilter(b, a, x)

def bp(x, f0, f1, order=2):
    b, a = signal.butter(order, [f0 / (SR / 2), f1 / (SR / 2)], 'band'); return signal.lfilter(b, a, x)

# ---------------- synthesized stand-ins (mono, peak-normalised): used only when the library is missing ----------------
def click():
    n = int(0.09 * SR); t = np.arange(n) / SR
    f = 1250 * np.exp(-t / 0.018) + 620          # bubbly downward chirp
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env_exp(n, 0.016)
    s += 0.35 * np.sin(2 * np.pi * np.cumsum(1.5 * f) / SR) * env_exp(n, 0.008)
    s[:24] *= np.linspace(0, 1, 24)
    return norm(lp(s, 5000))

def key(i):
    n = int(0.05 * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    s = bp(nz, 1800 + 300 * (i % 3), 5200) * env_exp(n, 0.004)
    s += 0.6 * np.sin(2 * np.pi * (170 + 15 * (i % 4)) * t) * env_exp(n, 0.010)
    s[:8] *= np.linspace(0, 1, 8)
    return norm(s)

def pop():
    n = int(0.22 * SR); t = np.arange(n) / SR
    f = 150 * np.exp(-t / 0.04) + 62
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.055)
    s += 0.25 * lp(rng.standard_normal(n), 900) * env_exp(n, 0.012)
    s[:48] *= np.linspace(0, 1, 48)
    return norm(lp(s, 1800))

def chime():
    n = int(1.1 * SR); out = np.zeros(n)
    for k, (f, t0) in enumerate([(1318.5, 0.0), (1760.0, 0.13)]):
        i0 = int(t0 * SR); m = n - i0; t = np.arange(m) / SR
        tone = np.sin(2 * np.pi * f * t) + 0.28 * np.sin(2 * np.pi * 2.01 * f * t) * env_exp(m, 0.12) + 0.12 * np.sin(2 * np.pi * 3.02 * f * t) * env_exp(m, 0.06)
        e = env_exp(m, 0.35); e[:96] *= np.linspace(0, 1, 96)
        out[i0:] += tone * e * (0.85 if k == 0 else 1.0)
    return norm(out)

def whoosh(variant, dur_out=0.45, dur_in=0.6):
    """low airy whoosh whose loudest moment is exactly at dur_out (the whip midpoint)"""
    pre, post = dur_out + 0.12, dur_in + 0.25
    n = int((pre + post) * SR); t = np.arange(n) / SR; tm = pre
    nz = rng.standard_normal(n)
    lo, hi, q = [(180, 700, 1.2), (140, 560, 1.4), (220, 820, 1.1), (160, 640, 1.3)][variant % 4]
    x = np.clip((t - (tm - dur_out)) / dur_out, 0, 1); y = np.clip((t - tm) / dur_in, 0, 1)
    fc = np.where(t < tm, lo + (hi - lo) * x ** 1.6, hi - (hi - lo) * y ** 0.8)
    w = np.clip((fc - lo) / (hi - lo), 0, 1)
    s = (1 - w) * bp(nz, lo * 0.55, lo * 1.7) + w * bp(nz, hi * 0.55, hi * 1.5) * 0.8
    e = np.where(t < tm, (np.clip((t - (tm - pre)) / pre, 0, 1)) ** 2.2, np.exp(-(t - tm) / (0.22 + 0.05 * variant)))
    s = lp(s * e, 1400)
    s = s / np.abs(s[int((tm - 0.03) * SR):int((tm + 0.03) * SR)]).max()
    return np.clip(s, -1.2, 1.2) / 1.2, int(tm * SR)

def riser(dur=2.6):
    n = int(dur * SR); t = np.arange(n) / SR; p = t / dur
    f = 48 * 2 ** (1.1 * p ** 1.3)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(2 * f) / SR + 0.3)
    nz = rng.standard_normal(n)
    w = p ** 2
    air = (1 - w) * bp(nz, 180, 500) + w * bp(nz, 900, 2600) * 0.7
    s = 0.8 * lp(tone, 400) + 0.45 * air
    e = p ** 2.4
    s *= e
    s[-int(0.012 * SR):] *= np.linspace(1, 0, int(0.012 * SR))   # audible end exactly on the join
    return norm(s)

# ---------------- levels: by LOUDNESS against the voice's speaking loudness (sfxlib; Leon's A/B/C test, 2026-10-16) ----
# Peak-based levels made chimes the loudest sound (8 LU under the voice) while clicks sat 22 LU under. The shorts keep
# their own levels (sfxlib.SHORTS_TARGET: pop and scribble -14, whoosh / chime -12, the hit -16, click -21, keys -27 LU),
# chimes evened out and the scribble's hiss tamed; shorts.json "sfx_levels" overrides per type.
RISER_DB = -12                                  # the riser's peak against the voice's peak
TARGET = dict(sfxlib.SHORTS_TARGET, **SH.get('sfx_levels', {}))
RULES = dict(sfxlib.SHORTS_RULES, **SH.get('sfx_rules', {}))
VSPEECH = sfxlib.speech_loudness(voice)
LIB_CAT = {'click': 'click', 'pop': 'pop', 'chime': 'chime', 'whoosh': 'whoosh', 'highlight': 'highlight', 'ding': 'ding',
           'sting': 'sting', 'key': 'typing', 'tick': 'typing', 'riser': 'riser'}
# Leon's picks from the long-form edits: the minimal hit on the hook end, the cinematic build as the riser
LIB = sfxlib.Library(prefer=SH.get('sfx_prefer') or {'sting': ['hit_minimal'], 'riser': ['cinematic_build']})
USE_LIB = bool(LIB.cats) and SH.get('sfx_library', True)

# ---------------- events ----------------
def gfx_cfg(rid):
    try:
        m = re.search(r'window\.CFG=(\{.*?\});</script>', open(f'gfx/{rid}.html', encoding='utf-8').read(), re.S)
        return json.loads(m.group(1)) if m else {}
    except (OSError, ValueError):
        return {}

ev = []
gfx_ev = json.load(open('gfx/sfx_events.json', encoding='utf-8')) if os.path.exists('gfx/sfx_events.json') else {}
for r in C['runs']:
    rid = f"{sk}_r{r['i']}"
    for e in gfx_ev.get(rid, []): ev.append(dict(t=r['T0'] + e['t'], type=e['type'], src=rid))
    # a highlight swish on every highlight band drawn in (a scaleX reveal), the marker-pen sound the eye expects
    if SH.get('auto_sfx', True):
        for rv in gfx_cfg(rid).get('reveals', []):
            if rv.get('type') == 'scaleX' and 0 <= rv['t'] < r['dur']: ev.append(dict(t=r['T0'] + rv['t'], type='highlight', src=rid))
if os.path.exists(f'{sk}/events_extra.json'):
    ev += [dict(e, src='cta') for e in json.load(open(f'{sk}/events_extra.json', encoding='utf-8'))]
if SH.get('auto_sfx', True) and SH.get('sting', True):
    ev.append(dict(t=JOIN, type='sting', src='hook'))         # a minimal hit where the hook lands on the first point
ev.sort(key=lambda e: e['t'])
main_t = [e['t'] for e in ev if e['type'] not in ('highlight', 'key', 'tick')]
ev = [e for e in ev if not (e['type'] == 'highlight' and any(abs(e['t'] - t) < 0.15 for t in main_t))]   # never stacked on another sound
for e in ev:
    if e.get('src') in ('cta', 'hook'): e['keep'] = True      # the CTA card and the hook hit always play
ev, dropped = sfxlib.select(ev, RULES)                         # a light safety net: no pile-ups, accents 8 s apart

sfx = np.zeros((N, 2)); log = []; wv = 0; k = 0
def add(s, i0, typ, name, e, vary=1.0):
    s = np.asarray(s, np.float64)
    if s.ndim == 1: s = np.stack([s, s], 1)
    if typ == 'highlight': s = sfxlib.tame(s)                  # the marker scribble's hiss off
    tgt = TARGET.get(typ, -14); g = sfxlib.gain_for(s, tgt, VSPEECH) * vary
    c0 = max(0, -i0); i0 = max(0, i0); m = min(len(s) - c0, N - i0)
    if m > 0: sfx[i0:i0 + m] += g * s[c0:c0 + m]
    log.append(dict(t=round(float(e['t']), 3), type=e['type'], sound=name, lu=tgt,
                    level_db=round(float(20 * np.log10(g * np.abs(s).max() / vpeak + 1e-12)), 1), src=e.get('src')))
while k < len(ev):
    e = ev[k]; typ = e['type']
    lib_ok = USE_LIB and LIB.has(LIB_CAT.get(typ, typ), short=0.35 if typ in ('key', 'tick') else None)
    if typ in ('key', 'tick'):                       # a typing run -> real single key strokes, slightly varied in level
        run = [e]
        while k + 1 < len(ev) and ev[k + 1]['type'] in ('key', 'tick') and ev[k + 1]['t'] - run[-1]['t'] < 0.35:
            k += 1; run.append(ev[k])
        for j, r in enumerate(run):
            kk, _, stem = LIB.get('typing', short=0.35) if lib_ok else (key(j), 0, 'synth_key')
            add(kk, int(round(r['t'] * SR)), typ, stem, r, vary=0.8 + 0.2 * ((j * 7) % 3) / 2)
    elif lib_ok:                                     # a recorded sample; whooshes land their loudest moment on the whip midpoint
        x, pk, stem = LIB.get(LIB_CAT.get(typ, typ))
        add(x, int(round(e['t'] * SR)) - pk, typ, stem, e)
    elif typ == 'whoosh':
        s, mid = whoosh(wv); wv += 1
        add(s, int(round(e['t'] * SR)) - mid, typ, f'synth_whoosh_{wv % 4}', e)
    elif typ in ('highlight', 'ding', 'sting'):      # no library: soft synthesized stand-ins
        s, mid = (whoosh(wv) if typ == 'highlight' else (chime(), 0)); wv += 1
        add(s, int(round(e['t'] * SR)) - mid, typ, f'synth_{typ}', e)
    else:
        s = {'click': click, 'pop': pop, 'chime': chime}.get(typ, pop)()
        add(s, int(round(e['t'] * SR)), typ, f'synth_{typ}', e)
    k += 1
json.dump(log, open(f'{sk}/sfx_log.json', 'w'), indent=1)
AUD = sfxlib.audit(ev, END)
print(f"{sk}: sfx {AUD['sounds']} sounds ({AUD['per_min']}/min) {AUD['by_type']}, accents {AUD['accents']}, "
      f"busiest 15 s {AUD['busiest_15s']}; {len(dropped)} not played" + (f" ({sorted({d['why'] for d in dropped})})" if dropped else ''))

# ---------------- riser: its loudest moment exactly on the hook join ----------------
ris = np.zeros((N, 2))
if USE_LIB and LIB.has('riser') and SH.get('riser_from_library', True):
    x, pk, rstem = LIB.get('riser'); pk = pk or int(np.argmax(np.abs(x).mean(1)))
    rs = x[:pk + int(0.012 * SR)].astype(np.float64)                     # cut right after its peak
    rs[-int(0.012 * SR):] *= np.linspace(1, 0, int(0.012 * SR))[:, None]
    rs *= vpeak * 10 ** (RISER_DB / 20)
else:
    rstem = 'synth_riser'; rs = np.repeat(riser(2.6)[:, None], 2, 1) * vpeak * 10 ** (-12 / 20)
i1 = int(round(JOIN * SR)); i0 = i1 - len(rs); a = max(0, i0)
ris[a:i1] = rs[a - i0:]

# ---------------- music: the generated take (or a given file), else the synthesized bed ----------------
mp = SH.get('music', {})
pick = json.load(open(f'{sk}/music/pick.json', encoding='utf-8')) if os.path.exists(f'{sk}/music/pick.json') else None
src = mp.get('file') or (pick['file'] if pick and os.path.exists(pick.get('file', '')) else None)
if src:
    x, sr = sf.read(src, dtype='float32', always_2d=True)
    if sr != SR: x = signal.resample_poly(x, SR, sr, axis=0).astype(np.float32)
    if x.shape[1] == 1: x = np.repeat(x, 2, 1)
    off = int(float(mp.get('file_offset', 0.0)) * SR)             # a take from music_takes.py is already cut: its lift is on JOIN
    mus = x[off:off + N, :2].astype(np.float64)
    if len(mus) < N: mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
    side = pick if (pick and src == pick.get('file')) else {}
    mparams = dict(source='generated' if side else 'file', file=src, file_offset=float(mp.get('file_offset', 0.0)),
                   style=side.get('style', mp.get('style', '-')), take=side.get('take'), seed=side.get('seed'),
                   model=side.get('model'), prompt=side.get('prompt'), bpm=side.get('bpm'), licence=side.get('licence'),
                   alternatives=side.get('alternatives'))
    under = float(mp.get('under_voice_lu', 15))     # Leon's hook-music lesson: 18 LU under was barely there, 15 reads
else:
    sys.path.insert(0, 'scripts'); import music as MUS
    KEYS = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    key_ = mp.get('key'); key_ = KEYS.index(key_) if isinstance(key_, str) and key_ in KEYS else key_
    seed = int(mp.get('seed', zlib.crc32((SH.get('title', '') + '|' + sk).encode()) % 1000003))
    syn_style = mp.get('style') if mp.get('style') in MUS.STYLES else 'lofi'
    mus, mparams = MUS.render(syn_style, seed, END, drop=JOIN, bpm=mp.get('bpm'), key=key_, mood=mp.get('mood'))
    mus = mus.astype(np.float64)[:N]
    if len(mus) < N: mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
    mparams = dict(source='synthesized', **mparams)
    under = float(mp.get('under_voice_lu', 17))     # the synthesized beds sat at -31 LUFS under a -14 LUFS voice
fi = int(0.8 * SR); mus[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(1.2 * SR); mus[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
v_lufs = meter.integrated_loudness(voice)
target = v_lufs - under
mus *= 10 ** ((target - meter.integrated_loudness(mus)) / 20)
venv = np.abs(voice.mean(1)); venv = signal.filtfilt(*signal.butter(1, 6 / (SR / 2)), venv)
duck = 1 - 0.45 * np.clip(venv / (np.percentile(venv, 90) + 1e-9), 0, 1)
mus *= duck[:, None]
mparams.update(level_lufs=round(float(target), 1), under_voice_lu=under, riser=rstem, sfx_library=LIB.dir if USE_LIB else None)
json.dump(mparams, open(f'{sk}/music.json', 'w'), indent=1)
print('music:', {k: v for k, v in mparams.items() if k not in ('prompt', 'alternatives')})

os.makedirs(f'{sk}/stems', exist_ok=True)
for nm, x in [('voice', voice), ('sfx', sfx), ('riser', ris), ('music', mus)]:
    sf.write(f'{sk}/stems/{nm}.wav', x[:N].astype(np.float32), SR, subtype='PCM_24')
mix = voice + sfx + ris + mus
# true-peak limiter (spec: final mix <= -1 dBFS true peak). 4x oversampled peak detection, 1.5 ms look-ahead (minimum
# filter), smoothed gain; touches only the few hot transients, so the integrated loudness stays ~-14 LUFS. (A plain
# sample-peak rescale to 0.95 let a less-compressed voice through at -0.4 dBTP.)
from scipy.ndimage import minimum_filter1d, uniform_filter1d
TP_THR = 10 ** (-1.3 / 20)
for _ in range(3):
    os_pk = np.max(np.abs(np.stack([signal.resample_poly(mix[:, c], 4, 1) for c in range(mix.shape[1])], 1)), 1)
    n4 = len(os_pk) // 4 * 4
    pk_n = os_pk[:n4].reshape(-1, 4).max(1)
    pk_n = np.pad(pk_n, (0, max(0, len(mix) - len(pk_n))), mode='edge')[:len(mix)]
    g = np.minimum(1.0, TP_THR / np.maximum(pk_n, 1e-9))
    if g.min() >= 0.9999: break
    la = int(0.0015 * SR)
    g = minimum_filter1d(g, size=4 * la + 1)
    g = uniform_filter1d(g, size=2 * la + 1)
    mix = mix * g[:, None]
tp = np.max(np.abs(np.stack([signal.resample_poly(mix[:, c], 4, 1) for c in range(mix.shape[1])], 1)))
print(f'{sk}: true peak after limiter {20 * np.log10(tp):.2f} dBTP')
sf.write(f'{sk}/mix.wav', mix.astype(np.float32), SR, subtype='PCM_24')
print(f"{sk}: END={END:.3f}s N={N} events={len(ev)} sounds={len(log)} ({'library ' + LIB.dir if USE_LIB else 'synthesized'}) "
      f"voice_peak={20*np.log10(vpeak):.1f}dBFS mix_peak={20*np.log10(np.abs(mix).max()):.1f} mix_lufs={meter.integrated_loudness(mix):.1f} "
      f"music_lufs={meter.integrated_loudness(mus+1e-9):.1f}")
