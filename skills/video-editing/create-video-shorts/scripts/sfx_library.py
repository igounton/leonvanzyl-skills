"""Curated, licence-clean sound-effects library (real recordings and designed SFX, not synthesized), built once into
the skill's own folder and shared by every edit.

  Library   <skill>/assets/sfx/<category>/<name>.wav      48 kHz, stereo, 24-bit PCM
            <skill>/assets/sfx/manifest.json              per file: duration, peak_time, LUFS, source, licence
            <skill>/assets/sfx/_originals/                 the untouched downloads (data only)
            PRO_EDIT_SFX_DIR moves it. Git holds the CC0 sounds; the .gitignore there keeps the Mixkit ones out
            (their licence forbids redistributing the files), so on a fresh clone `--check` lists them as missing
            and `build` downloads them from Mixkit.
  Sources   Mixkit (Mixkit Sound Effects Free License) and Freesound sounds licensed CC0 (HQ previews, no login).
            Every entry below names its page, direct download URL, author and licence; nothing else is fetched.

  python scripts/sfx_library.py build            download what is missing, (re)process everything, write manifest.json
  python scripts/sfx_library.py build --force    re-download the originals too
  python scripts/sfx_library.py --check          verify the library is complete and well-formed (exit 1 if not)
  python scripts/sfx_library.py list [category]  what is in it (name, duration, peak time, LUFS, picks marked *)
  python scripts/sfx_library.py build --from-manifest other/manifest.json   rebuild from another manifest's URLs

Processing (deterministic): decode (ffmpeg, float), cut the listed segment, resample to 48 kHz (polyphase), mono ->
stereo, trim so the onset (first sample above -50 dB re peak) sits at 5 ms and the file ends where the level stays
below -60 dB, 5 ms fade-in, 20-50 ms fade-out, sample-peak normalise to -1 dBFS (levels are set later by the pipeline).
peak_time = centre of the loudest 10 ms (put it on the cut for whooshes). `align` says which point to sync:
onset (hits, clicks, pops: t=0.005 on the event) or peak (whooshes, swoosh-ins, risers: peak_time on the cut/join;
for builds that stop dead the peak is the stop).

In code:  import sfx_library as SFX;  SFX.entries('whoosh');  SFX.path('ding', 'bell_attention');  SFX.picks('pop')
Needs: ffmpeg on PATH, numpy, scipy, soundfile, pyloudnorm (the pro-edit render env)."""
import hashlib, json, os, subprocess, sys, time, urllib.request
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import root as _root
LIB = _root()                  # $PRO_EDIT_SFX_DIR or <skill>/assets/sfx (sfxlib.root)
ORIG = os.path.join(LIB, '_originals')
MANIFEST = os.path.join(LIB, 'manifest.json')
SR = 48000
PEAK_DBFS = -1.0
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'

LICENSES = {
    'CC0-1.0': dict(name='Creative Commons 0 (CC0 1.0 Universal, public domain dedication)',
                    url='http://creativecommons.org/publicdomain/zero/1.0/',
                    terms='Copy, modify, distribute and perform, even commercially, without asking permission; no attribution required.'),
    'Mixkit-SFX-Free': dict(name='Mixkit Sound Effects Free License', url='https://mixkit.co/license/#sfxFree',
                            terms='Free for commercial and non-commercial projects incl. YouTube videos; no attribution required. '
                                  'Do not redistribute the item on its own (as stock, in a tool or template), claim it as your own '
                                  'or register it with a rights-management / Content ID service.'),
}


def mixkit(id_, page_slug, title):
    return dict(site='Mixkit', id=id_, title=title, author='Mixkit (Envato)', license='Mixkit-SFX-Free',
                page_url=f'https://mixkit.co/free-sound-effects/{page_slug}/',
                download_url=f'https://assets.mixkit.co/active_storage/sfx/{id_}/{id_}.wav', original=f'mixkit_{id_}.wav',
                original_format='WAV (Mixkit download)')


def freesound(id_, user, user_id, title, orig_fmt):
    return dict(site='Freesound', id=id_, title=title, author=user, license='CC0-1.0',
                page_url=f'https://freesound.org/people/{user}/sounds/{id_}/',
                download_url=f'https://cdn.freesound.org/previews/{id_ // 1000}/{id_}_{user_id}-hq.ogg',
                original=f'freesound_{id_}-hq.ogg',
                original_format=f'HQ preview, Ogg Vorbis ~192 kbps (uploaded original: {orig_fmt}; downloading it needs a login)')


# (category, name, source, segment [s, s] of the original or None, align, pick, description)
SOURCES = [
    # --- highlight: marker strokes for a highlight band sweeping across text, plus a soft swish and a shimmer
    ('highlight', 'marker_stroke_a', freesound(371330, 'TubbsMedia', 6912397, 'Marker Circle.WAV', 'WAV 48 kHz 24-bit'), [0.45, 1.35], 'onset', True,
     'Permanent-marker stroke on paper (~0.85 s incl. tail), dry felt-tip texture: the natural highlighter swipe.'),
    ('highlight', 'marker_stroke_b', freesound(371330, 'TubbsMedia', 6912397, 'Marker Circle.WAV', 'WAV 48 kHz 24-bit'), [3.10, 4.10], 'onset', False,
     'Second stroke from the same marker take (~0.95 s), for back-to-back highlights without repeats.'),
    ('highlight', 'marker_underline', freesound(428338, 'zembacraftworks', 8617763, 'Underlining Stroke on Paper', 'WAV 44.1 kHz 16-bit'), [0.15, 0.85], 'onset', True,
     'Quick underline stroke with a pen on paper (~0.65 s, the stroke itself ~0.45 s): short highlights and underlines.'),
    ('highlight', 'paper_swish', mixkit(1530, 'slide', 'Paper slide'), None, 'peak', False,
     'Soft paper slide (~0.45 s): a gentle, airy swish for a band wiping across text.'),
    ('highlight', 'shimmer_sweep', mixkit(3060, 'ding', 'Sparkle hybrid transition'), None, 'onset', False,
     'Sparkle/air hybrid sweep (~1.2 s): a highlight with a touch of shimmer, for the hook.'),
    # --- ding: a box/outline landing on a UI element
    ('ding', 'bell_attention', mixkit(586, 'bell', 'Attention bell ding'), None, 'onset', True,
     'Clean single bell strike (~1 s decay), bright but not harsh.'),
    ('ding', 'bell_glassy', freesound(127149, 'Daphne_in_Wonderland', 667113, 'ding.wav', 'WAV 44.1 kHz 32-bit'), None, 'onset', True,
     'Glassy metal ding (struck fireplace tool), pure partials, natural ~1.3 s decay.'),
    ('ding', 'bell_relaxing', mixkit(3109, 'bell', 'Relaxing bell chime'), None, 'onset', False,
     'Soft, warm bell with a gentle sustain (~1.6 s).'),
    ('ding', 'bell_small', freesound(611113, '5ro4', 1629501, 'bell ding 1.wav', 'WAV 44.1 kHz 16-bit'), None, 'onset', False,
     'Small training-bell ding, bright and short (~1.5 s).'),
    ('ding', 'tone_correct', mixkit(2870, 'notification', 'Correct answer tone'), None, 'onset', False,
     'Single clean tonal strike with a long sustain (~2 s): a calmer, more synthetic ding.'),
    # --- chime: success / confirm (a check mark, tests pass)
    ('chime', 'success_two_note', mixkit(2869, 'notification', 'Access allowed tone'), None, 'onset', True,
     'Clean two-note rising sine chime (~1.9 s): the classic modern "confirmed" tone.'),
    ('chime', 'success_soft', mixkit(2865, 'notification', 'Success software tone'), None, 'onset', False,
     'Soft two-note software success tone, rounder and lower than success_two_note.'),
    ('chime', 'success_arpeggio', freesound(541985, 'Rob_Marion', 6856600, 'GASP_Chimes_Success_4.wav', 'WAV 48 kHz 24-bit'), None, 'onset', True,
     'Quick rising chime arpeggio (~1.3 s), polished UI-success sound (GASP series).'),
    ('chime', 'achievement_bell', mixkit(600, 'bell', 'Achievement bell'), None, 'onset', False,
     'Two quick bell strikes ringing out (~1.5 s): a warmer, acoustic success.'),
    # --- pop: soft modern UI pops for a card landing
    ('pop', 'pop_light', mixkit(3005, 'whoosh', 'Explainer video pops whoosh light pop'), None, 'onset', True,
     'Light explainer-video pop (~0.17 s) with a tiny air tail: cards and badges landing.'),
    ('pop', 'ui_pop', freesound(541993, 'Rob_Marion', 6856600, 'GASP_UI_Pop_1.wav', 'WAV 48 kHz 24-bit'), None, 'onset', True,
     'Soft tonal UI pop with a slight upward glide (~0.1 s audible), clean 48 kHz design.'),
    ('pop', 'bubble_pop', freesound(669918, 'el_boss', 9129912, 'The Best Bubble Pop Sound For Game and UI', 'WAV 44.1 kHz 16-bit'), None, 'onset', False,
     'Recorded bubble pop, crisp and short (~0.25 s).'),
    ('pop', 'plop', freesound(447910, 'Breviceps', 9159316, 'Plop!', 'WAV 44.1 kHz 16-bit'), None, 'onset', False,
     'Round, soft plop (~0.24 s), slightly lower and fuller than ui_pop.'),
    # --- click: a button press
    ('click', 'mouse_click', mixkit(1113, 'click', 'Mouse click close'), None, 'onset', True,
     'Real mouse click, press + release (~0.2 s), close-miked.'),
    ('click', 'mouse_click_mx', freesound(256455, 'HunteR4708', 4772965, 'Mouse Click', 'WAV 96 kHz 16-bit'), None, 'onset', True,
     'Logitech mouse click recorded at 96 kHz, press + release (~0.3 s).'),
    ('click', 'switch_click', mixkit(2582, 'click', 'Quick switch click'), None, 'onset', False,
     'Quick, crisp switch click (~0.17 s): toggles and buttons.'),
    ('click', 'ui_check', mixkit(1120, 'click', 'Modern click box check'), None, 'onset', False,
     'Compact modern UI click for a checkbox / tick (~0.1 s).'),
    ('click', 'ui_tone_click', mixkit(2568, 'click', 'Cool interface click tone'), None, 'onset', False,
     'Very short tonal interface click (~0.07 s), the most "digital" of the set.'),
    # --- typing: single key ticks and short runs (1-3 s)
    ('typing', 'key_laptop', mixkit(2541, 'keyboard', 'Single key press in a laptop'), None, 'onset', True,
     'Single laptop (scissor-switch) key press, crisp and light (~0.1 s).'),
    ('typing', 'key_mech_a', freesound(348239, 'newagesoup', 4067257, 'MECH-KEYBOARD-01.wav', 'WAV 48 kHz 24-bit'), None, 'onset', False,
     'Mechanical keyboard keystroke (Razer BlackWidow), clicky (~0.2 s).'),
    ('typing', 'key_mech_b', freesound(348238, 'newagesoup', 4067257, 'MECH-KEYBOARD-02.wav', 'WAV 48 kHz 24-bit'), None, 'onset', False,
     'Mechanical keystroke variant, slightly darker (~0.2 s); alternate with key_mech_a.'),
    ('typing', 'run_pc_2s', freesound(539146, 'ristooooo1', 6205597, 'Keyboard Typing 001.wav', 'WAV 44.1 kHz 32-bit'), [0.08, 1.95], 'onset', True,
     'PC keyboard typing run (~1.7 s): two bursts with a natural pause, silent gaps (no room noise).'),
    ('typing', 'run_slow_2s', mixkit(2532, 'keyboard', 'Slow typing on a keyboard'), [2.98, 4.72], 'onset', False,
     'Unhurried typing of a couple of words (~1.6 s), clean gaps.'),
    ('typing', 'run_fast_laptop_2s', mixkit(1392, 'laptop', 'Fast laptop keyboard typing'), [0.36, 2.33], 'onset', False,
     'Fast continuous laptop typing (~2 s), for a command being typed quickly.'),
    # --- whoosh: transitions, peak on the cut, light -> heavy
    ('whoosh', 'air_short', freesound(60013, 'qubodup', 71257, 'Whoosh', 'FLAC 44.1 kHz 24-bit'), None, 'peak', False,
     'Short, light swish (~0.4 s, bamboo stick through air): quick zoom-ins and small moves.'),
    ('whoosh', 'air_fast', mixkit(2637, 'woosh', 'Fast air transition sweep'), None, 'peak', False,
     'Fast airy sweep (~0.7 s), symmetric rise/fall, on the bright side.'),
    ('whoosh', 'wind_sweep', mixkit(2632, 'woosh', 'Whoosh wind sweep'), None, 'peak', True,
     'Smooth mid-range whoosh (~1 s), soft attack and tail: the default transition.'),
    ('whoosh', 'pass_by', freesound(332003, 'LloydEvans09', 2567799, 'whoosh.wav', 'WAV 44.1 kHz 16-bit'), None, 'peak', True,
     'Punchy processed pass-by whoosh (~0.7 s), clear centre peak: camera whips.'),
    ('whoosh', 'air_full', mixkit(2607, 'woosh', 'Fast air woosh'), None, 'peak', False,
     'Fuller air woosh (~1.3 s), more body for bigger moves.'),
    ('whoosh', 'deep_low', freesound(648729, 'AudioPapkin', 8698658, 'Cinematic Woosh SFX-010.wav', 'WAV 96 kHz 24-bit'), None, 'peak', False,
     'Deep, low cinematic woosh (~1.1 s), mostly sub/low-mid: heavy scene changes, use sparingly.'),
    # --- swoosh_in / swoosh_out: shape-matched (not same-session pairs)
    ('swoosh_in', 'build_fast', mixkit(1490, 'whoosh', 'Fast whoosh transition'), None, 'peak', True,
     'Fast reverse-style whoosh that builds and stops dead (~0.75 s): the stop is peak_time, put it on the cut.'),
    ('swoosh_in', 'vacuum_in', mixkit(2608, 'woosh', 'Air zoom vacuum'), None, 'peak', False,
     'Air "suck-in" build peaking at ~0.35 s then cutting off quickly: put the peak on the cut.'),
    ('swoosh_out', 'release_fast', freesound(812678, 'AudioPapkin', 8698658, 'Sound Design Elements Whoosh SFX 041', 'WAV 96 kHz 32-bit'), None, 'onset', True,
     'Air burst that starts hard and decays (~0.7 s): put the START on the cut.'),
    ('swoosh_out', 'quick_out', mixkit(1462, 'swoosh', 'Quick swoosh'), None, 'onset', False,
     'Quick swoosh with a sharp attack and fast decay (~0.55 s).'),
    # --- sting: punchline / end-of-hook hits, plus soft reveal shimmers
    ('sting', 'hit_minimal', freesound(736850, 'xkeril', 13504080, 'Stab reverb hit (minimal)', 'WAV 48 kHz 24-bit'), None, 'onset', True,
     'Minimal stab hit with a long reverb tail (~2.3 s), processed metal jar: tasteful brand hit.'),
    ('sting', 'hit_sonar', freesound(736851, 'xkeril', 13504080, 'One hit (sonar inspired)', 'WAV 48 kHz 24-bit'), None, 'onset', False,
     'Brighter, sonar-like tonal hit with reverb tail (~2.9 s): a "ping" for a reveal or punchline.'),
    ('sting', 'luxury_shimmer', freesound(714565, 'LilMati', 6142149, 'Fashion Shimmer - Luxury Runway Percussion Stinger', 'WAV 48 kHz 16-bit'), None, 'onset', False,
     'Short luxury percussion stinger with shimmer (~2.2 s): polished, product-shot energy.'),
    ('sting', 'sub_hit', mixkit(2299, 'hit', 'Short bass hit'), None, 'onset', False,
     'Short, subtle bass hit (~0.9 s with its tail): felt more than heard, under a punchline.'),
    ('sting', 'reveal_sparkle_sweep', mixkit(2633, 'sweep', 'Sweeping sparkle presentation intro'), None, 'peak', True,
     'Soft reveal shimmer sweeping up to a peak at ~0.9 s, then a sparkle tail (~2.6 s).'),
    ('sting', 'reveal_wand', mixkit(3062, 'sparkle', 'Magic wand sparkle'), None, 'onset', False,
     'Light, high sparkle shimmer (~1.5 s): a delicate reveal.'),
    # --- riser: hook -> content join (peak/end on the join)
    ('riser', 'cinematic_build', mixkit(790, 'cinematic', 'Cinematic trailer riser'), None, 'peak', True,
     'Cinematic riser (~2.3 s) building to its peak right at the end: put peak_time on the join.'),
    ('riser', 'riser_hit_resolve', freesound(511872, 'AudioPapkin', 8698658, 'Riser Hit sfx 025.wav', 'WAV 44.1 kHz 16-bit'), None, 'peak', True,
     'Riser into a soft hit that resolves (peak ~1.7 s, ~2.5 s total): put the peak on the join.'),
    ('riser', 'synth_resolve', freesound(840719, 'SoundEffectsForAll', 17848526, 'Simple Riser', 'WAV 48 kHz 16-bit'), None, 'peak', False,
     'Suspenseful tonal riser peaking at ~2.6 s, then a short smooth resolve (~2.8 s total).'),
    ('riser', 'noise_riser', freesound(685256, 'syntheffects', 12265588, 'Riser sound effect short.wav', 'WAV 44.1 kHz 16-bit'), None, 'peak', False,
     'Organic noise riser (~2.7 s) that drops at its peak: classic build.'),
    ('riser', 'grain_riser', freesound(561207, 'Rizzard', 10825267, 'Riser', 'WAV 44.1 kHz 24-bit'), None, 'peak', False,
     'Short granular riser (~1.9 s) building to its peak at the end; darker (rolled off above ~10 kHz).'),
    # --- glitch / notification (optional extras)
    ('glitch', 'glitch_short', mixkit(1031, 'glitch', 'Glitch short'), None, 'onset', True,
     'Short digital glitch burst (~0.7 s).'),
    ('glitch', 'digital_glitch', freesound(458065, 'tadaizm', 1316332, 'Digital Glitch_v1.wav', 'WAV 48 kHz 32-bit'), None, 'onset', False,
     'Digital glitch for glitch transitions (~0.5 s).'),
    ('notification', 'chat_ping', freesound(235911, 'yfjesse', 2391840, 'Notification Sound', 'WAV 44.1 kHz 24-bit'), None, 'onset', True,
     'Chat-message style notification (layered synth), short and friendly (~0.5 s).'),
    ('notification', 'triple_ping', freesound(842513, 'PiesHelpfulOven', 14031674, 'Triple_Ping_Notification_Sound_Mobile_Optimized', 'WAV 48 kHz 24-bit'), None, 'onset', False,
     'Three-note rising notification chime (E6-G6-C7), very clear (~0.6 s).'),
]


# ------------------------------------------------------------------------------------------------ download
def _sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def download(url, dst, tries=3):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if len(data) < 1000: raise IOError(f'only {len(data)} bytes')
            tmp = dst + '.part'
            with open(tmp, 'wb') as f: f.write(data)
            os.replace(tmp, dst); return
        except Exception as e:
            last = e; time.sleep(1.5 * (k + 1))
    raise IOError(f'download failed: {url}: {last}')


# ------------------------------------------------------------------------------------------------ processing
def decode(path):
    """-> (float64 [n, ch], sr) at the file's native rate; float decode keeps lossy overshoot above 1.0 (no clipping)."""
    import numpy as np
    pr = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=sample_rate,channels', '-of', 'json', path],
                        capture_output=True, text=True, check=True)
    s = json.loads(pr.stdout)['streams'][0]; sr, ch = int(s['sample_rate']), int(s['channels'])
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-acodec', 'pcm_f32le', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, ch).astype(np.float64), sr


def process(src_path, segment=None):
    """Returns (stereo float32 @48k, info) per the rules in the module docstring."""
    import numpy as np
    from math import gcd
    from scipy.signal import resample_poly
    x, sr = decode(src_path)
    if segment:
        x = x[int(round(segment[0] * sr)):int(round(segment[1] * sr))]
    if x.shape[1] == 1: x = np.repeat(x, 2, axis=1)
    elif x.shape[1] > 2: x = x[:, :2]
    if sr != SR:
        g = gcd(SR, sr); x = resample_poly(x, SR // g, sr // g, axis=0)
    a = np.abs(x).max(1); pk = a.max()
    if pk <= 0: raise ValueError('silent')
    # envelope on 2 ms blocks, so a single stray sample does not decide where the sound starts / ends
    blk = int(0.002 * SR); nb = int(np.ceil(len(a) / blk)); env = np.zeros(nb)
    for i in range(nb): env[i] = a[i * blk:(i + 1) * blk].max()
    on_blk = int(np.flatnonzero(env > pk * 10 ** (-50 / 20))[0])
    onset = on_blk * blk + int(np.flatnonzero(a[on_blk * blk:(on_blk + 1) * blk] > pk * 10 ** (-50 / 20))[0])
    end_blk = int(np.flatnonzero(env > pk * 10 ** (-60 / 20))[-1])
    end = min(len(a), (end_blk + 1) * blk + int(0.005 * SR))
    pre = int(0.005 * SR)
    start = onset - pre
    y = x[max(0, start):end]
    if start < 0: y = np.vstack([np.zeros((-start, 2)), y])
    truncated_db = float(20 * np.log10(np.sqrt((x[max(0, len(x) - int(0.02 * SR)):] ** 2).mean()) / pk + 1e-12))
    n = len(y)
    fi = int(0.005 * SR); fo = int(min(0.05, max(0.02, 0.1 * n / SR)) * SR)
    y[:fi] *= (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, fi)))[:, None]
    y[-fo:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, fo)))[:, None]
    y *= 10 ** (PEAK_DBFS / 20) / np.abs(y).max()
    return y.astype(np.float32), dict(src_sr=sr, src_end_level_db=round(truncated_db, 1))


def measure(y):
    import numpy as np, pyloudnorm as pyln
    n = len(y); mono = y.astype(np.float64).mean(1)
    w = int(0.010 * SR)
    e = np.convolve(mono ** 2, np.ones(w) / w, 'valid') if n > w else np.array([np.mean(mono ** 2)])
    peak_time = (int(np.argmax(e)) + w / 2) / SR if n > w else n / 2 / SR
    yy = y.astype(np.float64)
    if n < int(0.4 * SR): yy = np.vstack([yy, np.zeros((int(0.4 * SR) - n, 2))])
    lufs = pyln.Meter(SR).integrated_loudness(yy)
    return dict(duration=round(n / SR, 4), peak_time=round(peak_time, 4), lufs=round(float(lufs), 1),
                peak_dbfs=round(float(20 * np.log10(np.abs(y).max())), 2), onset=0.005)


# ------------------------------------------------------------------------------------------------ build / check
def _entries_from_sources():
    out = []
    for cat, name, src, seg, align, pick, desc in SOURCES:
        lic = LICENSES[src['license']]
        out.append(dict(category=cat, name=name, file=f'{cat}/{name}.wav', description=desc, align=align, pick=pick, segment=seg,
                        source=dict(src, license_name=lic['name'], license_url=lic['url'])))
    return out


def build(force=False, from_manifest=None, only=None):
    import soundfile as sf
    if from_manifest:
        entries = json.load(open(from_manifest, encoding='utf-8'))['files']
    else:
        entries = _entries_from_sources()
    old = {}
    if os.path.exists(MANIFEST):
        try: old = {e['file']: e for e in json.load(open(MANIFEST, encoding='utf-8'))['files']}
        except Exception: old = {}
    os.makedirs(ORIG, exist_ok=True)
    fetched, failed, out = set(), [], []
    for e in entries:
        if only and not (e['file'].startswith(only) or e['category'] == only):
            if e['file'] in old: out.append(old[e['file']])
            continue
        src = e['source']; op = os.path.join(ORIG, src['original'])
        try:
            if (force and op not in fetched) or not os.path.exists(op):
                download(src['download_url'], op); fetched.add(op); time.sleep(0.3)
            sha = _sha256(op)
            rec = src.get('original_sha256') or old.get(e['file'], {}).get('source', {}).get('original_sha256')
            if rec and rec != sha:
                print(f"  note: {src['original']} differs from the recorded download (upstream re-encode?) - listen-check it")
            src['original_sha256'] = sha
            y, info = process(op, e.get('segment'))
            dst = os.path.join(LIB, e['file']); os.makedirs(os.path.dirname(dst), exist_ok=True)
            sf.write(dst, y, SR, subtype='PCM_24')
            m = measure(y)
            e.update(m); e['source']['original_sample_rate'] = info['src_sr']
            e['bytes'] = os.path.getsize(dst)
            out.append(e)
            print(f"  {e['file']:40s} {m['duration']:6.3f}s  peak@{m['peak_time']:6.3f}  {m['lufs']:6.1f} LUFS")
        except Exception as ex:
            failed.append((e['file'], str(ex))); print(f"  FAILED {e['file']}: {ex}")
    man = dict(version=1, generated=str(date.today()),
               library=LIB.replace('\\', '/') if os.environ.get('PRO_EDIT_SFX_DIR') else '<skill>/assets/sfx',
               format=dict(sample_rate=SR, channels=2, subtype='PCM_24', peak_dbfs=PEAK_DBFS),
               processing='decode (float) -> segment -> resample to 48 kHz (polyphase) -> stereo -> onset (-50 dB re peak) at 5 ms, '
                          'cut where the level stays below -60 dB -> 5 ms fade-in, 20-50 ms fade-out -> sample peak -1 dBFS. '
                          'peak_time = centre of the loudest 10 ms. lufs = integrated (BS.1770), files < 0.4 s zero-padded to 0.4 s.',
               align_help=dict(onset='sync the start (t=0.005) to the event', peak='put peak_time on the cut / landing / join'),
               licenses=LICENSES, files=out)
    with open(MANIFEST, 'w', encoding='utf-8') as f: json.dump(man, f, indent=1, ensure_ascii=False)
    if not only and not failed:   # drop processed files a previous build made that are no longer listed (originals are kept)
        keep = {os.path.normcase(os.path.join(LIB, e['file'])) for e in out}
        for d in os.listdir(LIB):
            dp = os.path.join(LIB, d)
            if d.startswith('_') or not os.path.isdir(dp): continue
            for fn in os.listdir(dp):
                fp = os.path.join(dp, fn)
                if fn.endswith('.wav') and os.path.normcase(fp) not in keep:
                    os.remove(fp); print(f'  removed stale {d}/{fn}')
            if not os.listdir(dp): os.rmdir(dp)
    print(f"{len(out)} files -> {LIB}  ({sum(e.get('bytes', 0) for e in out) / 1e6:.1f} MB)")
    if failed:
        print('FAILED:', *[f'{a}: {b}' for a, b in failed], sep='\n  '); return 1
    return 0


def check(verbose=True):
    import soundfile as sf
    problems = []
    if not os.path.exists(MANIFEST):
        print(f'no manifest at {MANIFEST} - run: python scripts/sfx_library.py build'); return 1
    man = json.load(open(MANIFEST, encoding='utf-8'))
    have = {e['file'] for e in man['files']}
    for e in _entries_from_sources():
        if e['file'] not in have: problems.append(f"{e['file']}: listed in SOURCES but missing from the manifest")
    for e in man['files']:
        p = os.path.join(LIB, e['file'])
        if not os.path.exists(p): problems.append(f"{e['file']}: missing"); continue
        try:
            i = sf.info(p)
        except Exception as ex:
            problems.append(f"{e['file']}: unreadable ({ex})"); continue
        if i.samplerate != SR or i.channels != 2 or i.subtype != 'PCM_24':
            problems.append(f"{e['file']}: {i.samplerate} Hz / {i.channels} ch / {i.subtype}")
        if abs(i.frames / SR - e['duration']) > 0.002: problems.append(f"{e['file']}: duration {i.frames / SR:.3f} != {e['duration']}")
        for k in ('peak_time', 'lufs', 'description'):
            if e.get(k) in (None, ''): problems.append(f"{e['file']}: no {k}")
        s = e.get('source', {})
        for k in ('page_url', 'download_url', 'author', 'license_name', 'license_url'):
            if not s.get(k): problems.append(f"{e['file']}: source.{k} missing")
        if not os.path.exists(os.path.join(ORIG, s.get('original', '?'))): problems.append(f"{e['file']}: original {s.get('original')} missing")
    cats = {}
    for e in man['files']: cats[e['category']] = cats.get(e['category'], 0) + 1
    if verbose:
        print(f"{LIB}: {len(man['files'])} files  " + '  '.join(f'{c}={n}' for c, n in sorted(cats.items())))
        print('OK' if not problems else 'PROBLEMS:\n  ' + '\n  '.join(problems))
    return 1 if problems else 0


# ------------------------------------------------------------------------------------------------ lookup API
def _man():
    return json.load(open(MANIFEST, encoding='utf-8'))


def entries(category=None):
    """Manifest entries (dicts) with an absolute 'path' added; category=None for all."""
    out = []
    for e in _man()['files']:
        if category is None or e['category'] == category:
            out.append(dict(e, path=os.path.join(LIB, e['file'])))
    return out


def picks(category):
    """The recommended files of a category (best first), falling back to all of them."""
    es = entries(category); p = [e for e in es if e.get('pick')]
    return p or es


def path(category, name):
    return os.path.join(LIB, category, f'{name}.wav')


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] in ('-h', '--help', 'help'):
        print(__doc__); sys.exit(0)
    if a[0] in ('--check', 'check'):
        sys.exit(check())
    if a[0] == 'list':
        for e in entries(a[1] if len(a) > 1 else None):
            print(f"{'*' if e.get('pick') else ' '} {e['file']:40s} {e['duration']:6.3f}s peak@{e['peak_time']:6.3f} {e['lufs']:6.1f} LUFS  "
                  f"align={e['align']:5s} {e['source']['site']}:{e['source']['id']}  {e['description'][:70]}")
        sys.exit(0)
    if a[0] == 'build':
        fm = a[a.index('--from-manifest') + 1] if '--from-manifest' in a else None
        only = a[a.index('--only') + 1] if '--only' in a else None
        rc = build(force='--force' in a, from_manifest=fm, only=only)
        sys.exit(rc or check(verbose=True))
    print(__doc__); sys.exit(2)
