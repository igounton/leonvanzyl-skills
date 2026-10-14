# Graphics agent A (shorts s1 + s5): cuts stills / clips from the RAW recordings (via longform_program.json), copies the
# research captures and official logos it uses into gfx/assets/ (all prefixed a_) and writes gfx/asset_dims_a.json.
# Run from the work folder:  ../.venv/Scripts/python.exe scripts/prep_assets_a.py
# Raw recordings are 3840x2160 60 fps with Leon's webcam PiP top-right at x 3110, y 18, 698x944: every crop below stays
# at x <= 3104 (left of it) or under y 962, so the webcam never shows.
import json, os, subprocess, shutil, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
A = 'gfx/assets'
os.makedirs(A, exist_ok=True)
RAW = 'C:/Users/leon/Videos/Skool/YouTube/Media/Harness Engineering'
P = json.load(open('longform_program.json', encoding='utf-8'))
dims = {}
PIP = (3110, 18, 698, 944)


def raw_of(t):
    """final-video time -> (raw file, source seconds)"""
    for it in P['items']:
        if it['t0'] <= t < it['t1']:
            return it['file'], (it['src0'] + (t - it['t0']) * 60) / 60
    raise ValueError(t)


def safe(crop):
    x, y, w, h = crop
    px, py, pw, ph = PIP
    assert x + w <= px or y >= py + ph, f'crop {crop} would show the webcam'
    assert w % 2 == 0 and h % 2 == 0, f'odd crop {crop}'


def still(name, f, s, crop, scale=1.0):
    safe(crop)
    x, y, w, h = crop
    vf = f'crop={w}:{h}:{x}:{y}' + (f',scale={round(w * scale / 2) * 2}:{round(h * scale / 2) * 2}:flags=lanczos' if scale != 1 else '')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s - 1:.3f}', '-i', f'{RAW}/{f}', '-ss', '1', '-frames:v', '1', '-vf', vf, f'{A}/{name}'], check=True)
    dims[name] = list(Image.open(f'{A}/{name}').size)


def clip(name, f, s0, dur, crop, scale, hold=0.0):
    """a frame-exact clip (crop + scale, 60 fps, dense keyframes for HyperFrames); hold = freeze the last frame for N s"""
    safe(crop)
    x, y, w, h = crop
    ow, oh = round(w * scale / 2) * 2, round(h * scale / 2) * 2
    pre = min(2, s0)
    # input seek 2 s early (decoded frames from there are 0-based), then a frame-exact trim; tpad freezes the last frame
    vf = (f'trim=start={pre:.4f}:duration={dur:.4f},setpts=PTS-STARTPTS,crop={w}:{h}:{x}:{y},scale={ow}:{oh}:flags=lanczos,fps=60'
          + (f',tpad=stop_mode=clone:stop_duration={hold:.3f}' if hold > 0 else ''))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s0 - pre:.4f}', '-i', f'{RAW}/{f}',
                    '-vf', vf, '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-g', '12', '-keyint_min', '12', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart', f'{A}/{name}'], check=True)
    dims[name] = [ow, oh]


def copy(name, src, max_side=None):
    im = Image.open(src)
    if max_side and max(im.size) > max_side:
        im.thumbnail((max_side, max_side), Image.LANCZOS)
    im.save(f'{A}/{name}')
    dims[name] = list(im.size)


def crop_png(name, src, box, scale=1.0):
    im = Image.open(src).crop(box)
    if scale != 1: im = im.resize((round(im.size[0] * scale), round(im.size[1] * scale)), Image.LANCZOS)
    im.save(f'{A}/{name}')
    dims[name] = list(im.size)


L = 'captures/logos'
jobs = []
# ---------------------------------------------------------------- official logos (captures/logos, longform_assets)
copy('a_grok.png', f'{L}/grok_logomark_on-dark.png', 512)
copy('a_langchain_wm.png', f'{L}/langchain_logo_on-dark.png', 1400)          # white wordmark for the stage
copy('a_openai_ink.png', f'{L}/openai_symbol.png', 384)                         # dark mark for paper chips
copy('a_openai_white.png', f'{L}/openai_symbol_on-dark.png', 384)
copy('a_claude.png', f'{L}/claude_symbol.png', 384)
copy('a_codex.png', 'longform_assets/codex_app_icon.png')
copy('a_opencode.png', f'{L}/opencode-logo-dark.png', 384)                      # light artwork for the glass
copy('a_github_white.png', f'{L}/github_invertocat_on-dark.png', 384)
copy('a_x_white.png', f'{L}/x_logo_on-dark.png', 256)

# ---------------------------------------------------------------- research captures (2x PNGs)
LC = 'captures/langchain_harness/screenshots/full-page.png'
crop_png('a_lc_head.png', LC, (440, 380, 2440, 830))                              # tags + title + author/date
crop_png('a_lc_page.png', LC, (0, 0, 2880, 3300))                                 # title -> TLDR -> 52.8/66.5 line -> leaderboard

# ---------------------------------------------------------------- raw screen recordings
# s1_r8: Can Boluk's X article as Leon had it open (6.mkv 266.0 s = final 9:19.2): article column x 896-2600, left of the PiP
jobs.append(lambda: still('a_x_post.png', '6.mkv', 266.0, (896, 200, 1712, 1960)))
# s5 (cubefarm, 8.mkv). Full height, x 0-3104 (the PiP starts at x 3110).
CF = (0, 0, 3104, 2160)
f8, s = raw_of(890.18)
assert f8.endswith('8.mkv')
# r0 (hook): the walk into the office, 8.mkv 41.33-44.01, ends where r1's synced footage starts (continuous across the cut)
jobs.append(lambda: clip('a_s5_r0.mp4', '8.mkv', 41.333, 2.80, CF, 0.5))
# r1 synced: final 893.09-901.24 -> 8.mkv 44.01-52.16 (dur 7.583 + margin)
jobs.append(lambda: clip('a_s5_r1.mp4', '8.mkv', raw_of(893.09)[1], 7.70, CF, 0.6))
# r2 synced: final 901.64 -> 8.mkv 60.79 (Margaret at her desk, monitor streaming code)
jobs.append(lambda: clip('a_s5_r2.mp4', '8.mkv', raw_of(901.64)[1], 3.25, CF, 0.5))
# r3 synced: final 905.03 -> 8.mkv 64.33: walk up to Margaret, her terminal opens at 68.1 (claude-opus-5-5 in its header)
jobs.append(lambda: clip('a_s5_r3.mp4', '8.mkv', raw_of(905.03)[1], 8.35, CF, 0.75))
# r5 synced: final 922.51 -> 8.mkv 81.93: the 3D whiteboard, then the full-screen Kanban board at 84.45
jobs.append(lambda: clip('a_s5_r5.mp4', '8.mkv', raw_of(922.51)[1], 6.30, CF, 0.7))
# r6: the board with Leon's real cursor moving onto "PR #300" (click at 90.82), last frame held; then the PR page still
BOARD = (1150, 370, 1100, 900)
jobs.append(lambda: clip('a_s5_r6_board.mp4', '8.mkv', 89.82, 0.98, BOARD, 1.0, hold=5.4))
jobs.append(lambda: still('a_s5_pr.png', '8.mkv', 94.30, (0, 0, 2900, 2000), 0.5))

with ThreadPoolExecutor(6) as ex:
    for f in [ex.submit(j) for j in jobs]: f.result()


def backdrop_clip(name):
    """a 640 px copy of a footage clip for the capture frame's washed, 40 px-blurred backdrop (HyperFrames holds every
    extracted video frame in memory: two full-size copies of an 8 s clip ran the renderer out of heap)"""
    out = name.replace('.mp4', '_bd.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{A}/{name}', '-vf', 'scale=640:-2:flags=bicubic', '-an', '-c:v', 'libx264', '-crf', '20',
                    '-g', '12', '-keyint_min', '12', '-pix_fmt', 'yuv420p', f'{A}/{out}'], check=True)


with ThreadPoolExecutor(3) as ex:
    list(ex.map(backdrop_clip, ['a_s5_r1.mp4', 'a_s5_r3.mp4', 'a_s5_r5.mp4']))

json.dump(dict(sorted(dims.items())), open('gfx/asset_dims_a.json', 'w'), indent=1)
print(json.dumps(dims))
