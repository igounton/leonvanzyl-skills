"""The royalty-free SFX library built by sfx_library.py (the skill's own assets/sfx, or $PRO_EDIT_SFX_DIR):
samples by category, rotated so the same sound never plays twice in a row, as 48 kHz stereo float arrays peak-normalised
to 1, with the sample index of each one's loudest moment (whooshes land that peak exactly on the cut).
audio.py uses it when it exists and falls back to its synthesized sounds otherwise."""
import os, json
import numpy as np, soundfile as sf
from scipy.signal import resample_poly

SR = 48000


def root():
    """$PRO_EDIT_SFX_DIR, else the skill's assets/sfx: found from project.json's skill_dir (a work dir, setup.sh writes
    it), from this script's own folder (run inside the skill), or the usual install paths. The first one with a
    manifest wins; with none built yet, the first skill folder found (where `sfx_library.py build` puts it)."""
    env = os.environ.get('PRO_EDIT_SFX_DIR') or os.environ.get('PRO_EDIT_SFX')
    if env: return env
    skills = []
    try: skills.append(json.load(open('project.json', encoding='utf-8'))['skill_dir'])
    except Exception: pass
    skills.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    skills += [os.path.join(os.path.expanduser('~'), d, 'skills', n) for n in ('davinci-resolve-pro-edit', 'create-video-shorts')
               for d in ('.claude', '.agents')]                 # both video skills ship the same library
    skills = [os.path.normpath(d) for d in skills if os.path.exists(os.path.join(d, 'SKILL.md'))]
    for d in skills:
        if os.path.exists(os.path.join(d, 'assets', 'sfx', 'manifest.json')): return os.path.join(d, 'assets', 'sfx')
    return os.path.join(skills[0], 'assets', 'sfx') if skills else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'sfx')


def _entries(man):
    """accepts {'files': [...]}, a plain list, or {category: [...]}"""
    if isinstance(man, dict) and isinstance(man.get('files'), list): return man['files']
    if isinstance(man, list): return man
    if isinstance(man, dict):
        out = []
        for cat, v in man.items():
            if isinstance(v, list): out += [dict(e, category=e.get('category', cat)) for e in v if isinstance(e, dict)]
        return out
    return []


class Library:
    def __init__(self, path=None, prefer=None):
        self.dir = path or root(); self.cats = {}; self.count = {}; self.cache = {}; self.last = {}
        self.prefer = prefer or {}                     # {category: [file stems in order of preference]} from the plan
        mf = os.path.join(self.dir, 'manifest.json')
        if not os.path.exists(mf): return
        for e in _entries(json.load(open(mf, encoding='utf-8'))):
            f = e.get('file') or e.get('path')
            if not f: continue
            p = f if os.path.isabs(f) else os.path.join(self.dir, f)
            if not os.path.exists(p): continue
            self.cats.setdefault(e.get('category', os.path.basename(os.path.dirname(p))), []).append(
                dict(path=p, peak=float(e.get('peak_time', 0.0) or 0.0), dur=float(e.get('duration', 0.0) or 0.0),
                     pick=bool(e.get('pick')), align=e.get('align', 'onset')))
        for c, lst in self.cats.items():
            pref = self.prefer.get(c)
            if pref:                                    # preferred files first, the rest after
                stem = lambda d: os.path.splitext(os.path.basename(d['path']))[0]
                lst.sort(key=lambda d: pref.index(stem(d)) if stem(d) in pref else len(pref))

    def has(self, cat, short=None):
        return bool(self.pick_list(cat, short))

    def pick_list(self, cat, short=None):
        lst = self.cats.get(cat, [])
        if short is not None: return [d for d in lst if d['dur'] and d['dur'] <= short]   # e.g. all single key ticks
        if cat in self.prefer: return lst                                                # the plan's order, all files
        picks = [d for d in lst if d['pick']]
        return picks or lst                                                              # the library's recommended picks

    def load(self, p):
        if p not in self.cache:
            x, sr = sf.read(p, dtype='float32', always_2d=True)
            if sr != SR: x = resample_poly(x, SR, sr, axis=0).astype(np.float32)
            if x.shape[1] == 1: x = np.repeat(x, 2, 1)
            x = x[:, :2]; m = np.abs(x).max()
            self.cache[p] = x / m if m > 0 else x
        return self.cache[p]

    def get(self, cat, short=None, top=None):
        """(stereo samples, index of the loudest moment, name) - rotates over the category's first `top` files"""
        lst = self.pick_list(cat, short)
        if not lst: return None
        if top: lst = lst[:top]
        k = self.count.get(cat, 0); self.count[cat] = k + 1
        d = lst[k % len(lst)]
        if len(lst) > 1 and self.last.get(cat) == d['path']: d = lst[(k + 1) % len(lst)]
        self.last[cat] = d['path']
        x = self.load(d['path'])
        pk = int(d['peak'] * SR) if d['peak'] else int(np.argmax(np.abs(x).mean(1)))
        # the sample index to land on the event: the onset, or the loudest moment when the manifest says align=peak
        return x, (pk if d['align'] == 'peak' else 0), os.path.splitext(os.path.basename(d['path']))[0]
