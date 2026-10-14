"""Per-item webcam PiP windows, for recordings whose OBS scenes put the webcam in different corners inside ONE file
(harness-engineering 5.mkv: top-right on the slides, bottom-left in the VS Code scene). scenes.py keeps one window per
source file; this finds, for every 'screen' V1 item, which corner the webcam is in (YuNet faces in the four corner
windows of the file's PiP size, on 4 samples per item) and writes scenes.json -> items.<v1>.pip. zoom.py, compose.py,
look.py and patch_flash.py prefer the item's window over the file's.
Run it after scenes.py and look at the summary: items whose samples disagree are listed (the scene changes inside the
item - keep beats off them or split the beat at the change).
usage: python scripts/pip_items.py [--dry]"""
import sys, json, subprocess, threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np, cv2
sys.path.insert(0, 'scripts'); import media as M, faces

S = json.load(open('scenes.json')); P = M.program()
LOCK = threading.Lock()                                       # one YuNet net per size, not thread-safe


def corners(win, W, H):
    """the four corner windows of the file's PiP size; the file's own corner keeps its measured window exactly"""
    x, y, w, h = win
    own = ('T' if y + h / 2 < H / 2 else 'B') + ('L' if x + w / 2 < W / 2 else 'R')
    mx = min(x, W - x - w); my = min(y, H - y - h)               # the measured margins, mirrored to the other corners
    cs = {'TR': [W - w - mx, my, w, h], 'TL': [mx, my, w, h], 'BR': [W - w - mx, H - h - my, w, h], 'BL': [mx, H - h - my, w, h]}
    cs[own] = list(win)
    return cs, own


def edge_fit(frames, guess, W, H, reach=24):
    """snap a mirrored window to the PiP's real border: the window size is known, so only its position is searched,
    scoring each candidate by BOTH of its edges (a status bar or a panel edge next to one side can't win alone)"""
    x, y, w, h = guess
    g = np.median(np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]), 0).astype(np.float32)
    gx = np.abs(np.diff(g, axis=1)); gy = np.abs(np.diff(g, axis=0))
    colp = gx[y + h // 5:y + 4 * h // 5].mean(0); rowp = gy[:, x + w // 5:x + 4 * w // 5].mean(1)
    def best(prof, c, size, n):
        cands = [k for k in range(c - reach, c + reach + 1) if 1 <= k and k + size < n]
        return max(cands, key=lambda k: prof[k - 1] + prof[k + size - 1]) if cands else c
    return [best(colp, x, w, W - 1), best(rowp, y, h, H - 1), w, h]


def grab(f, t, W, H):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', f, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H, W, 3) if len(raw) == W * H * 3 else None


def which(it):
    sc = S['items'].get(str(it['v1']), {})
    win = (S['files'].get(it['file']) or {}).get('pip')
    if sc.get('scene') != 'screen' or not win or win[2] * 2 > 3840: return it['v1'], None, []
    p = M.probe(it['file']); W, H = p['width'], p['height']
    cs, own = corners(win, W, H); votes = []; frs = []
    for q in (0.15, 0.4, 0.65, 0.9):
        fr = grab(it['file'], (it['src0'] + q * (it['src1'] - it['src0'])) / 60, W, H)
        if fr is None: continue
        frs.append(fr)
        best, area = None, 0
        for name, (x, y, w, h) in cs.items():
            with LOCK: fs = faces.detect(cv2.resize(fr[y:y + h, x:x + w], (w // 2, h // 2)), 0.75)
            if fs and fs[0][2] * fs[0][3] > area: best, area = name, fs[0][2] * fs[0][3]
        votes.append(best)
    known = [v for v in votes if v]
    if not known: return it['v1'], None, votes
    top = max(set(known), key=known.count)
    return it['v1'], (cs[top] if top == own else edge_fit(frs, cs[top], W, H)), votes


with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(which, P['items']))
changed, mixed = [], []
for v1, win, votes in res:
    if win is None: continue
    if len(set(v for v in votes if v)) > 1: mixed.append((v1, votes))
    if S['items'][str(v1)].get('pip') != win: changed.append(v1)
    S['items'][str(v1)]['pip'] = win
    S['items'][str(v1)]['pip_corner'] = max(set(v for v in votes if v), key=[v for v in votes if v].count)
from collections import Counter
print('corners:', dict(Counter(S['items'][str(v)]['pip_corner'] for v, w, _ in res if w)))
print('items whose window changed:', changed or 'none')
if mixed: print('items whose samples disagree (scene change inside the item):', mixed)
if '--dry' not in sys.argv:
    json.dump(S, open('scenes.json', 'w'), indent=1); print('scenes.json updated')
