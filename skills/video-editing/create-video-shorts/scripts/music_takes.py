"""Music for each short, generated locally with ACE-Step 1.5 XL (music_gen.py; MIT licence, outputs may be used
commercially). All takes of all shorts come from ONE model load; each take is cut so its lift (drums and bass coming in)
lands exactly on the hook join, then the best take is picked automatically: instrumental, a clear lift on the join, no
gaps or dips. The other takes stay next to it, and finish.sh delivers them as MP3s, so the user can swap by ear.
usage: python scripts/music_takes.py s1 [s2 ...] [--takes 3] [--force]   generate (or reuse) the takes and pick one
       python scripts/music_takes.py s1 --ensure                         finish.sh: wait for a running job, else generate
       python scripts/music_takes.py s1 --pick 2                         use take 2 instead (then finish.sh: audio only)
Reads cut.json (END, and the hook join = end of run 0) and shorts.json <sk>.music:
  {"style": "cinematic" (default) | "indie" | "piano_pop" | "electro_pop" | "lofi" | "chillhop" | "ambient" |
   "synthwave" | "upbeat", "prompt": "<your own caption>", "structure": "...", "bpm": 105, "takes": 3, "seed": N,
   "file": "<a wav to use instead: no generation>", "generate": false (synthesized bed instead)}
Writes <sk>/music/take_<k>.wav (+ .json sidecars with the analysis), <sk>/music/pick.json and <sk>/music/status.
audio.py uses pick.json; without it (no GPU / no music env / generate: false) it falls back to music.py's synthesized bed."""
import json, os, subprocess, sys, time, zlib

# Prompt presets. "cinematic" is Leon's pick (2026-10-14, chosen by ear over the other three for the Harness Engineering
# hook: "That's the one!"); the next three are the takes it beat; the last five follow music.py's synthesized styles.
STYLES = {
    'cinematic': dict(bpm=105, prompt='uplifting cinematic instrumental, opens with a solo emotional piano ostinato and soft pads with no drums, then pulsing staccato strings, warm bass and a steady driving modern drum groove enter, hopeful and inspiring, warm, documentary style, not an epic trailer',
                      structure='[Intro - solo piano ostinato, quiet, no drums, no bass]\n\n[Build - strings, bass and drums enter]\n\n[Main Theme - full drums, driving, inspiring]\n\n[Main Theme - variation, sustained energy]\n\n[Bridge - rising]\n\n[Final Theme - biggest]\n\n[Outro]'),
    'indie': dict(bpm=112, prompt='positive inspiring indie electronic instrumental, opens with a plucked guitar and marimba-like synth arpeggio over warm pads with no drums, then upbeat drums with claps and shaker and a round bass enter, warm Rhodes, sunny, optimistic, modern tech vlog background music',
                  structure='[Intro - soft arpeggio and pads, quiet, no drums, no bass]\n\n[Build - drums and bass enter, energy lifts]\n\n[Main Theme - full, upbeat, driving]\n\n[Main Theme - variation, sustained energy]\n\n[Bridge]\n\n[Final Theme - biggest]\n\n[Outro]'),
    'piano_pop': dict(bpm=110, prompt='inspirational modern tech background music, instrumental, opens with warm felt piano chords and airy pads alone with no drums, then punchy modern drums, deep warm bass, claps and bright synth plucks lift the energy, optimistic, hopeful, forward-moving, cinematic but light, polished clean production',
                      structure='[Intro - solo piano and pads, quiet, no drums, no bass]\n\n[Build - drums and bass enter, energy lifts]\n\n[Main Theme - full arrangement, uplifting, driving]\n\n[Main Theme - variation, bright, sustained energy]\n\n[Bridge - layered, rising]\n\n[Final Theme - biggest, euphoric]\n\n[Outro]'),
    'electro_pop': dict(bpm=118, prompt='uplifting electronic pop instrumental for a tech product launch, opens with soft filtered synth plucks and warm pads alone with no drums, then a steady four-on-the-floor kick, crisp claps and rolling bass drive it forward, shimmering arpeggios, gentle piano motif, bright, optimistic, motivational, sleek modern production',
                        structure='[Intro - soft filtered plucks and pads, quiet, no drums, no bass]\n\n[Build - kick and bass enter]\n\n[Main Theme - full, uplifting, driving]\n\n[Main Theme - variation, sustained energy]\n\n[Breakdown - short]\n\n[Final Theme - biggest]\n\n[Outro]'),
    'lofi': dict(bpm=84, prompt='warm lofi hip-hop instrumental, opens with soft Rhodes seventh chords and gentle vinyl crackle alone with no drums, then dusty swung drums and a warm round bass enter, mellow, focused, modern study beat, clean mix',
                 structure='[Intro - Rhodes chords, quiet, no drums, no bass]\n\n[Build - drums and bass enter]\n\n[Main Theme - laid-back groove]\n\n[Main Theme - variation]\n\n[Outro]'),
    'chillhop': dict(bpm=92, prompt='relaxed chillhop instrumental, opens with a clean jazzy guitar and soft keys alone with no drums, then a crisp head-nodding beat, warm bass and light percussion enter, easy-going, friendly, modern how-to background music',
                     structure='[Intro - guitar and keys, quiet, no drums, no bass]\n\n[Build - beat and bass enter]\n\n[Main Theme - relaxed groove]\n\n[Main Theme - variation]\n\n[Outro]'),
    'ambient': dict(bpm=80, prompt='calm reflective ambient electronic instrumental, opens with soft evolving pads and a gentle piano motif alone, then a soft pulse, subtle sub bass and light textured percussion enter, serious, thoughtful, spacious, modern documentary underscore',
                    structure='[Intro - pads and piano, quiet, no drums]\n\n[Build - soft pulse and bass enter]\n\n[Main Theme - steady, spacious]\n\n[Outro]'),
    'synthwave': dict(bpm=100, prompt='modern synthwave instrumental, opens with shimmering arpeggiated analog synths and warm pads alone with no drums, then punchy retro drums, a driving pulsing bass and bright lead synth chords enter, futuristic, confident, the future is here',
                      structure='[Intro - arpeggios and pads, quiet, no drums, no bass]\n\n[Build - drums and bass enter]\n\n[Main Theme - driving, bright]\n\n[Main Theme - variation]\n\n[Outro]'),
    'upbeat': dict(bpm=120, prompt='upbeat modern house instrumental for a launch, opens with filtered piano chords and pads alone with no drums, then a four-on-the-floor kick, claps, an energetic bassline and bright stabs enter, celebratory, confident, polished production',
                   structure='[Intro - filtered piano and pads, quiet, no drums, no bass]\n\n[Build - kick and bass enter]\n\n[Main Theme - full, energetic]\n\n[Main Theme - variation]\n\n[Outro]'),
}
DEFAULT_STYLE = 'cinematic'
SK = [a for a in sys.argv[1:] if not a.startswith('--') and not a.isdigit()]
ARGS = sys.argv[1:]
PY = sys.executable


def opt(name, default=None, cast=str):
    return cast(ARGS[ARGS.index(name) + 1]) if name in ARGS else default


def status(sk, s):
    os.makedirs(f'{sk}/music', exist_ok=True)
    open(f'{sk}/music/status', 'w').write(f'{s} {os.getpid()} {int(time.time())}')


def read_status(sk):
    try:
        st, pid, t = open(f'{sk}/music/status').read().split()
        return st, int(pid), int(t)
    except (OSError, ValueError):
        return None, None, None


def alive(pid):
    if not pid: return False
    if os.name == 'nt':
        o = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/NH'], capture_output=True, text=True).stdout
        return str(pid) in o
    try:
        os.kill(pid, 0); return True
    except OSError:
        return False


def score(side, drop):
    """higher is better; None = unusable (a voice, or no lift at all)"""
    a = side.get('analysis') or {}
    if a.get('vocal_seconds_over_m15db', 0) > 2 or a.get('vocal_stem_db_p95', -99) > -12: return None, 'vocals'
    if side.get('lift_in_generation_s') is None: return None, 'no lift'
    lift = a.get('lift_s')
    aligned = lift is not None and abs(lift - drop) < 0.6
    s = 0.5 * min(a.get('lift_db', 0), 12) + 0.2 * min(a.get('percussive_lift_db', 0), 20)
    s -= max(0, a.get('worst_dip_db', 0) - 6) + 2 * a.get('silent_100ms_windows', 0) + a.get('dips_over_6db_s', 0)
    if not aligned: s -= 8
    return round(s, 2), ('lift on the join' if aligned else f'lift at {lift} s, join at {drop:.2f} s')


def pick(sk, force_take=None):
    C = json.load(open('cut.json', encoding='utf-8'))[sk]; drop = C['runs'][0]['T1']
    takes = sorted(f for f in os.listdir(f'{sk}/music') if f.startswith('take_') and f.endswith('.wav'))
    rows = []
    for f in takes:
        p = f'{sk}/music/{f}'
        if not os.path.exists(p + '.json'): continue
        side = json.load(open(p + '.json', encoding='utf-8'))
        sc, why = score(side, drop)
        rows.append(dict(take=int(f[5:-4]), file=os.path.abspath(p).replace('\\', '/'), score=sc, why=why, seed=side.get('seed'),
                         lift_s=(side.get('analysis') or {}).get('lift_s'), style=side.get('style'), prompt=side.get('prompt'),
                         model=side.get('model'), bpm=side.get('bpm_requested'), licence=side.get('licence')))
    ok = [r for r in rows if r['score'] is not None]
    if force_take is not None:
        best = next(r for r in rows if r['take'] == force_take)
    elif ok:
        best = max(ok, key=lambda r: (r['score'], -r['take']))
    else:
        print(f'{sk}: no usable take ({[(r["take"], r["why"]) for r in rows]}); audio.py will use the synthesized bed')
        if os.path.exists(f'{sk}/music/pick.json'): os.remove(f'{sk}/music/pick.json')
        return None
    out = dict(best, alternatives=[dict(take=r['take'], file=r['file'], score=r['score'], why=r['why']) for r in rows if r is not best],
               drop=round(drop, 3), picked='by hand' if force_take is not None else 'automatically')
    json.dump(out, open(f'{sk}/music/pick.json', 'w'), indent=1)
    print(f"{sk}: music take {best['take']} ({best['style']}, seed {best['seed']}, score {best['score']}, {best['why']}) -> {sk}/music/pick.json; "
          f"others: {[(r['take'], r['score'], r['why']) for r in rows if r is not best]}")
    return out


def generate(sks, force=False):
    jobs, todo = [], []
    for sk in sks:
        S = json.load(open('shorts.json', encoding='utf-8'))[sk]; mp = S.get('music', {})
        if mp.get('file') or mp.get('generate') is False:
            print(f'{sk}: music.{"file" if mp.get("file") else "generate=false"} - nothing to generate'); continue
        C = json.load(open('cut.json', encoding='utf-8'))[sk]
        style = mp.get('style') if mp.get('style') in STYLES else DEFAULT_STYLE
        pr = STYLES[style]
        n = int(mp.get('takes', opt('--takes', 3, int)))
        base = int(mp.get('seed', zlib.crc32((S.get('title', '') + '|' + sk).encode()) % 2 ** 31))
        os.makedirs(f'{sk}/music', exist_ok=True)
        mine = []
        for k in range(1, n + 1):
            out = f'{sk}/music/take_{k}.wav'
            if os.path.exists(out + '.json') and not force: continue
            mine.append(dict(prompt=mp.get('prompt', pr['prompt']), structure=mp.get('structure', pr['structure']),
                             bpm=mp.get('bpm', pr['bpm']), seconds=round(C['END'] + 0.5, 2), seed=(base + 7919 * (k - 1)) % 2 ** 31,
                             out=out, drop=round(C['runs'][0]['T1'], 3), align=True, style=style))
        if mine: jobs += mine; todo.append(sk); status(sk, 'running')
    if jobs:
        json.dump(jobs, open('music_jobs.json', 'w'), indent=1)
        print(f'generating {len(jobs)} take(s) for {todo} in one model load (~1-3 min load, ~15 s a take on an RTX 5090)', flush=True)
        rc = subprocess.run([PY, 'scripts/music_gen.py', '--jobs', 'music_jobs.json']).returncode
        for j in jobs:                                    # carry the preset name into each sidecar (the report names the style)
            p = j['out'] + '.json'
            if os.path.exists(p):
                d = json.load(open(p, encoding='utf-8')); d['style'] = j['style']; json.dump(d, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        if rc != 0: print(f'music_gen exited {rc} (some takes may be missing)')
    for sk in sks:
        if os.path.isdir(f'{sk}/music'):
            r = pick(sk)
            status(sk, 'done' if r else 'failed')


if __name__ == '__main__':
    if not SK: sys.exit(__doc__)
    if '--pick' in ARGS:
        pick(SK[0], int(ARGS[ARGS.index('--pick') + 1])); sys.exit(0)
    if '--ensure' in ARGS:
        for sk in SK:
            st, pid, t = read_status(sk)
            while st == 'running' and alive(pid):
                print(f'{sk}: music takes still generating (pid {pid}) - waiting', flush=True); time.sleep(10)
                st, pid, t = read_status(sk)
            mp = json.load(open('shorts.json', encoding='utf-8'))[sk].get('music', {})
            if os.path.exists(f'{sk}/music/pick.json') or mp.get('file') or mp.get('generate') is False: continue
            generate([sk])
        sys.exit(0)
    generate(SK, '--force' in ARGS)
