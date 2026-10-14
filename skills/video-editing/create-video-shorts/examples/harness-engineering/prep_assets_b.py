# Graphics agent B (s2 "30,000 tokens before you type", s3 "What an AI agent actually is"): cuts its stills/clips into
# gfx/assets/b_*, copies the captures/logos it uses (long-form b_* files are copied under NEW names b_lf_*), and writes
# gfx/asset_dims_b.json. Run from anywhere: python scripts/prep_assets_b.py
# Raw screen recordings are 3840x2160 with Leon's webcam picture-in-picture at x 3110, y 18, 698x944: every crop here
# stays left of x 2600 (or 1560), so the webcam never shows.
import json, os, subprocess, shutil, io, sys
from PIL import Image, ImageDraw
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
A = 'gfx/assets'; os.makedirs(A, exist_ok=True)
RAW = 'C:/Users/leon/Videos/Skool/YouTube/Media/Harness Engineering'
SRC6 = f'{RAW}/6.mkv'
dims = {}


def grab(src, t):
    """exact still by output seeking (lessons: input-only seeking can land a frame early)"""
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t - 1:.3f}', '-i', src, '-ss', '1', '-frames:v', '1',
                        '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True)
    return Image.open(io.BytesIO(r.stdout)).convert('RGB')


def save(im, name, **kw):
    im.save(f'{A}/{name}', **kw); dims[name] = list(im.size)


def copy(src, name):
    shutil.copyfile(src, f'{A}/{name}'); dims[name] = list(Image.open(f'{A}/{name}').size)


# ------------------------------------------------------------------------------------------------ s2_r0: Claude Code /context
# Long-form 12:02-12:19 = 6.mkv items 100-102. The terminal scrolls between the states, so every still is re-cropped so that
# the Claude Code banner (the orange Clawd mascot) sits at the same place: F coordinates, 2600 x 1640, mascot top at F y 160.
FW, FH, MASCOT_Y = 2600, 1640, 160
BG = (11, 11, 11)                                   # Windows Terminal background, measured


def mascot_top(im):
    a = np.asarray(im.crop((0, 0, 400, 2160))).astype(int)
    m = (a[..., 0] > 180) & (a[..., 1] > 80) & (a[..., 1] < 160) & (a[..., 2] < 120)
    rows = np.where(m.sum(1) > 40)[0]               # the mascot is a solid block; text glyphs are thin
    return int(rows.min())


def fcrop(im, cursor=None):
    if cursor:                                      # paint out the mouse pointer (a white arrow on the plain background)
        ImageDraw.Draw(im).rectangle(cursor, fill=BG)
    off = mascot_top(im) - MASCOT_Y
    out = Image.new('RGB', (FW, FH), BG)
    src = im.crop((0, max(0, off), FW, min(2160, off + FH)))
    out.paste(src, (0, max(0, -off)))
    return out, off


CTX = [('b_ctx_a.png', 605.5, (1488, 1360, 1548, 1418)),       # banner + empty prompt ("Try refactor <filepath>")
       ('b_ctx_t1.png', 607.05, None), ('b_ctx_t2.png', 607.5, None), ('b_ctx_t3.png', 607.6, None),
       ('b_ctx_t4.png', 607.75, None), ('b_ctx_t5.png', 607.95, None), ('b_ctx_t6.png', 608.2, None),
       ('b_ctx_sp.png', 608.55, None),                             # /context sent, "Spinning..."
       ('b_ctx_c.png', 630.0, (2092, 1006, 2150, 1072))]          # the /context result (36.2k/1m tokens)
offs = {}
for name, t, cur in CTX:
    im, off = fcrop(grab(SRC6, t), cur)
    offs[name] = off
    save(im, name, optimize=True)
print('ctx offsets', offs)

# ------------------------------------------------------------------------------------------------ s2_r1: Ollama context-length doc
im = Image.open('captures/ollama_ctx/screenshots/full-page.png').convert('RGB').crop((0, 0, 2880, 1800))
save(im, 'b_ollama_ctx.png', optimize=True)

# ------------------------------------------------------------------------------------------------ s2_r5: the real SMOL Coder CLI
# Long-form 11:21 (6.mkv item 94, src 550.5-555.1 s): "smol" just started, SMOL coder v0.7.0, the status line with 1.4k (1%).
x, y, w, h = 0, 0, 1560, 1580
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '550.0', '-i', SRC6, '-ss', '1.0', '-t', '3.8',
                '-vf', f'crop={w}:{h}:{x}:{y},fps=60', '-an', '-c:v', 'libx264', '-crf', '12', '-g', '12', '-pix_fmt', 'yuv420p',
                f'{A}/b_smol_cli.mp4'], check=True)
dims['b_smol_cli.mp4'] = [w, h]

# ------------------------------------------------------------------------------------------------ s3_r3: the real model pages
o = Image.open('captures/opus55/screenshots/full-page.png').convert('RGB').crop((490, 600, 2390, 1170))
save(o, 'b_hero_opus.jpg', quality=93)
f = Image.open('captures/fable51/screenshots/full-page.png').convert('RGB').crop((490, 520, 2390, 1090))
save(f, 'b_hero_fable.jpg', quality=93)
g = Image.open('captures/gpt6_api/screenshots/full-page.png').convert('RGB').crop((500, 330, 1540, 535))
save(g, 'b_hero_gpt6.png', optimize=True)

# ------------------------------------------------------------------------------------------------ logos (official marks)
for src, name in [('longform_assets/claude_symbol.png', 'b_lf_claude_symbol.png'),
                  ('longform_assets/openai_symbol.png', 'b_lf_openai_symbol.png'),
                  ('longform_assets/b_openai_white.png', 'b_lf_openai_white.png'),
                  ('longform_assets/b_cc_wordmark_dark.png', 'b_lf_cc_wordmark_ondark.png'),   # light artwork for the stage
                  ('longform_assets/b_smol_logo_alpha.png', 'b_lf_smol_logo_alpha.png'),
                  ('longform_assets/b_ollama_white.png', 'b_lf_ollama_white.png')]:
    copy(src, name)

json.dump(dims, open('gfx/asset_dims_b.json', 'w'), indent=1)
print(json.dumps(dims))
