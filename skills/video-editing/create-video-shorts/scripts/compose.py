"""Final compositor for one short: layouts (full cam / split / full visual), camera card + matted head,
captions, CTA comment box, cover (frame 0). Writes <sk>/final_video.mp4 (video+mix) and caption/CTA metadata.
usage: python compose.py s1 --events-only            captions.json + events_extra.json only (audio.py can start)
       python compose.py s1 --preview t1,t2,...      full-resolution frames -> <sk>/preview/ (add --runs i,j to decode only those)
       python compose.py s1 --preview t1,... --clean the same frames without captions, CTA or cover -> <sk>/thumb/ (thumbnail.py)
       python compose.py s1 --runs i --seg-out f.mp4 one run as a video segment (one process per run)
       python compose.py s1 --segments [--jobs N] [--no-concat] [--force]
                                                    every run as its own process in parallel, cached by its inputs (a run whose
                                                    graphic, camera clip, matte, captions and code are unchanged is skipped),
                                                    frame counts verified, then --concat
       python compose.py s1 --concat                stream-copy the segments + the mix -> <sk>/final_video.mp4"""
import json, sys, os, subprocess, re, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sk = sys.argv[1]
PREVIEW = None
ONLY = None; SEG_OUT = None; CONCAT = '--concat' in sys.argv; SEGMENTS = '--segments' in sys.argv
if '--runs' in sys.argv: ONLY = [int(x) for x in sys.argv[sys.argv.index('--runs') + 1].split(',')]
if '--seg-out' in sys.argv: SEG_OUT = sys.argv[sys.argv.index('--seg-out') + 1]
if CONCAT: ONLY = []
if '--preview' in sys.argv: PREVIEW = [float(x) for x in sys.argv[sys.argv.index('--preview') + 1].split(',')]
CLEAN = PREVIEW is not None and '--clean' in sys.argv   # thumbnail candidates: the picture alone
FPS = 60; Wc, Hc = 1080, 1920
C = json.load(open('cut.json', encoding='utf-8'))[sk]; S = json.load(open('shorts.json', encoding='utf-8'))[sk]
CAM = json.load(open(f'{sk}/cam/plan.json', encoding='utf-8'))
END = C['END']; NF = int(round(END * FPS))
RUNS = C['runs']
F = 'fonts/'
# The channel's design system ("Leon YouTube": graphite stage, glass, Figtree / Geist Mono, azure accent) - the same
# look as the long-form edits' keyword pops and CTA cards, which Leon approved ("Now that looks cool. Lock it in").
def vfont(name, size, weight):
    f = ImageFont.truetype(F + name, int(round(size)))
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f
CAP = vfont('Figtree-VF.ttf', 74, 700)        # captions: Figtree bold, white with a graphite stroke
INK = (17, 18, 20); STAGE950 = (11, 12, 14); STAGE800 = (24, 25, 28); STAGE700 = (33, 34, 38)
TEXT_MUTED = (126, 129, 138); AZURE = (47, 149, 255); AZURE_INK = (21, 96, 208)
ACCENTS = {'azure': (47, 149, 255), 'ember': (255, 138, 91), 'iris': (156, 124, 255), 'mint': (79, 214, 160)}
GLASS = (24, 25, 28, 224)                     # stage-800, more opaque than the slides' 62% (no backdrop blur here)

def run_at(t):
    for r in RUNS:
        if r['T0'] - 1e-6 <= t < r['T1'] - 1e-6: return r
    return RUNS[-1]

# ---------------------------------------------------------------- captions
def disp_tokens():
    toks = []
    for w in C['words']:
        s = w['w']
        if re.match(r'^\.\d', s) and toks:
            toks[-1]['w'] += s.rstrip('.,'); toks[-1]['e'] = w['e']; toks[-1]['p'] = s[-1] in '.,?' ; continue
        toks.append(dict(w=s, s=w['s'], e=w['e'], p=s[-1] in '.,?'))
    for t in toks:
        t['d'] = t['w'].rstrip('.,')
        if t['d'].lower() == 'sonic': t['d'] = 'Sonnet'
    return toks

FUNC = set('a an the to of and or but if in on at for with from by is it its it\'s this that as be are was were you your i i\'m we we\'ll so then than up out like'.split())
HL = [h.lower().split() for h in S.get('highlights', [])]

J_LEAD = 0.06

def build_chunks():
    toks = disp_tokens(); chunks = []; i = 0; since = 3
    while i < len(toks):
        # J_LEAD: a line's audio (and its first word) starts 50 ms before its picture cut, so a word belongs to the run it
        # is heard in 60 ms later; otherwise each line's first word flashes alone as a caption at the end of the run before
        r = run_at(toks[i]['s'] + J_LEAD)
        # highlight candidate?
        hit = None
        for h in HL:
            seg = [t['d'].lower() for t in toks[i:i + len(h)]]
            if seg == h: hit = h; break
        if hit and since >= 2 and (not chunks or not chunks[-1]['hl']):
            chunks.append(dict(toks=toks[i:i + len(hit)], hl=True)); i += len(hit); since = 0; continue
        cur = [toks[i]]; i += 1
        while i < len(toks) and len(cur) < 3:
            nt = toks[i]
            if cur[-1]['p']: break
            if run_at(nt['s'] + J_LEAD) is not r: break
            if nt['s'] - cur[-1]['e'] > 0.32: break
            if len(' '.join(t['d'] for t in cur + [nt])) > 20: break
            if any([t['d'].lower() for t in toks[i:i + len(h)]] == h for h in HL) and since + 1 >= 2: break
            cur.append(nt); i += 1
        chunks.append(dict(toks=cur, hl=False)); since += 1
    for k, c in enumerate(chunks):
        c['text'] = ' '.join(t['d'] for t in c['toks'])
        c['t0'] = max(1 / FPS, c['toks'][0]['s'])
        nxt = chunks[k + 1]['toks'][0]['s'] if k + 1 < len(chunks) else END
        last_e = c['toks'][-1]['e']
        c['t1'] = min(END, nxt if nxt - last_e < 0.5 else last_e + 0.3)
    return chunks

def caption_img(text, hl=False):
    """a normal caption chunk: Figtree bold, white, a 10 px graphite stroke, wide word gaps (the stroke never swallows
    the spaces). Highlighted chunks are glass chips instead (chip_parts)."""
    font = CAP
    pad = 30
    dummy = ImageDraw.Draw(Image.new('L', (1, 1)))
    lines = [text]
    if dummy.textlength(text, font=font) > 960 and ' ' in text:
        ws = text.split(); best = None
        for k in range(1, len(ws)):
            a, b = ' '.join(ws[:k]), ' '.join(ws[k:]); m = max(dummy.textlength(a, font=font), dummy.textlength(b, font=font))
            if best is None or m < best[0]: best = (m, [a, b])
        lines = best[1]
    lh = 88; gap = dummy.textlength(' ', font=font) + 16
    lw = lambda l: sum(dummy.textlength(wd, font=font) for wd in l.split()) + gap * (len(l.split()) - 1)
    w = int(max(lw(l) for l in lines)) + 2 * pad; h = lh * len(lines) + 2 * pad
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for j, l in enumerate(lines):
        x = (w - lw(l)) / 2; y = pad + j * lh
        for wd in l.split():
            d.text((x, y), wd, font=font, fill=(255, 255, 255, 255), stroke_width=10, stroke_fill=STAGE950 + (255,))
            x += dummy.textlength(wd, font=font) + gap
    return np.asarray(im)


# ---------------------------------------------------------------- highlight chips (the long-form keyword pop, locked)
# A graphite glass chip (stage-800, accent hairline + bloom, top highlight, the long panel shadow), the words in Figtree
# 600 white at the title tracking, and the accent line drawn in beneath them. It pops in (0.18 s) and the line sweeps
# in from 0.08 s over 0.32 s; it cuts with the caption.
CHIP_SIZE, CHIP_TRACK, CHIP_PADX, CHIP_PADY, CHIP_SHPAD, CHIP_R = 70, -0.025, 40, 26, 150, 28
CHIP_IN, SWEEP_T0, SWEEP_DUR = 0.18, 0.08, 0.32


def tracked(draw, xy, text, f, fill, track_em):
    """text with letter-spacing, keeping the font's kerning"""
    x, y = xy; extra = track_em * f.size; prev = 0.0
    for i, ch in enumerate(text):
        draw.text((x + prev + i * extra, y), ch, font=f, fill=fill)
        prev = f.getlength(text[:i + 1])
    return prev + extra * (len(text) - 1)


def chip_parts(text, accent='azure'):
    acc = ACCENTS.get(accent, ACCENTS['azure'])
    size = CHIP_SIZE
    while True:                                                   # long phrases shrink to fit the 1080 frame
        f = vfont('Figtree-VF.ttf', size, 600)
        tw = f.getlength(text) + CHIP_TRACK * f.size * (len(text) - 1)
        if tw + 2 * CHIP_PADX <= 980 or size <= 50: break
        size -= 2
    cap = f.getbbox('H')[3] - f.getbbox('H')[1]
    dsc = f.getbbox('gjpqy')[3] - f.getbbox('H')[3]               # descender depth: the line sits below it
    line_gap, line_h = dsc + 14, 5
    cw, ch = tw + 2 * CHIP_PADX, CHIP_PADY + cap + line_gap + line_h + CHIP_PADY
    sp = CHIP_SHPAD; size_px = (int(cw + 2 * sp), int(ch + 2 * sp)); box = (sp, sp, sp + cw, sp + ch); r = CHIP_R
    base = Image.new('RGBA', size_px, (0, 0, 0, 0))

    def soft(rect, rgba, blur):
        m = Image.new('L', size_px, 0); ImageDraw.Draw(m).rounded_rectangle(rect, r, fill=255)
        m = m.filter(ImageFilter.GaussianBlur(blur))
        lay = Image.new('RGBA', size_px, rgba[:3] + (0,)); lay.putalpha(m.point(lambda v: int(v * rgba[3] / 255)))
        return lay
    x0, y0, x1, y1 = box
    base = Image.alpha_composite(base, soft((x0 + 40, y0 + 90, x1 - 40, y1 + 50), (0, 0, 0, 200), 50))   # 0 50 120 -40 shadow
    base = Image.alpha_composite(base, soft((x0 + 30, y0 + 30, x1 - 30, y1 - 30), acc + (150,), 46))    # accent bloom
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, r, fill=GLASS)
    d.rounded_rectangle(box, r, outline=acc + (84,), width=2)                                          # accent hairline
    d.line((x0 + r, y0 + 1.5, x1 - r, y0 + 1.5), fill=(255, 255, 255, 22), width=1)                   # top highlight
    ty = y0 + CHIP_PADY
    tracked(d, (x0 + CHIP_PADX, ty - f.getbbox('H')[1]), text, f, (255, 255, 255, 255), CHIP_TRACK)
    ly = ty + cap + line_gap
    return base, (x0 + CHIP_PADX, ly, x0 + CHIP_PADX + tw, ly + line_h), acc


CHIP_CACHE = {}
def chip_render(k, parts, t_rel):
    """(RGBA PIL image, scale, alpha, y offset) of chip k at t_rel s after its caption starts; frames with the same
    state reuse the same image"""
    pin = min(1.0, max(0.0, t_rel / CHIP_IN))
    sw = min(1.0, max(0.0, (t_rel - SWEEP_T0) / SWEEP_DUR))
    sw = 1 - (1 - sw) ** 3                                        # power3.out
    key = (k, round(pin, 3), round(sw, 3))
    if key not in CHIP_CACHE:
        base, line, acc = parts; im = base
        if sw > 0:                                                # the accent line, with a soft glow, drawn left to right
            x0, y0, x1, y1 = line; xe = x0 + (x1 - x0) * sw
            glow = Image.new('L', im.size, 0); ImageDraw.Draw(glow).rounded_rectangle((x0, y0, xe, y1), 3, fill=255)
            glow = glow.filter(ImageFilter.GaussianBlur(7))
            gl = Image.new('RGBA', im.size, acc + (0,)); gl.putalpha(glow.point(lambda v: int(v * 0.8)))
            im = Image.alpha_composite(im, gl)
            ImageDraw.Draw(im).rounded_rectangle((x0, y0, xe, y1), 3, fill=acc + (255,))
        e = 1 - (1 - pin) ** 3
        CHIP_CACHE[key] = (im, 0.96 + 0.04 * e, min(1.0, pin * 1.6), 12 * (1 - e))
    return CHIP_CACHE[key]


def paste_rgba(dst, im, cx, cy, scale=1.0, alpha=1.0):
    """alpha-over a PIL RGBA image onto the float RGB frame, centred on (cx, cy)"""
    if scale != 1.0:
        im = im.resize((max(1, int(im.size[0] * scale)), max(1, int(im.size[1] * scale))), Image.LANCZOS)
    a = np.asarray(im, np.float32); h, w = a.shape[:2]
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    ys0, ys1 = max(0, y0), min(Hc, y0 + h); xs0, xs1 = max(0, x0), min(Wc, x0 + w)
    if ys1 <= ys0 or xs1 <= xs0: return
    src = a[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]; al = src[..., 3:4] / 255.0 * alpha
    sub = dst[ys0:ys1, xs0:xs1]; sub[:] = sub * (1 - al) + src[..., :3] * al

def caption_center_y(r):
    # outro (CTA): just above the CTA card (top 1344). A webcam face cover-fitted to 1080 wide fills the frame down to
    # ~y 1150, so the old centre band (1037-1306) sat on the chin; centred at 1250 a 1-2 line caption clears both
    if r['i'] == RUNS[-1]['i']: return 1250
    return (941 + 1114) / 2 if r['layout'] == 'split' else (1290 + 1560) / 2

# ---------------------------------------------------------------- shapes
def squircle_mask(x0, y0, w, h, r, n=5.0, ss=2):
    H2, W2 = Hc * ss, Wc * ss
    yy, xx = np.mgrid[0:H2, 0:W2].astype(np.float32) / ss + 0.5 / ss
    cx = np.clip(xx, x0 + r, x0 + w - r); cy = np.clip(yy, y0 + r, y0 + h - r)
    dx = np.abs(xx - cx) / r; dy = np.abs(yy - cy) / r
    inside = (dx ** n + dy ** n <= 1) & (xx >= x0) & (xx <= x0 + w) & (yy >= y0) & (yy <= y0 + h)
    m = inside.astype(np.float32).reshape(Hc, ss, Wc, ss).mean((1, 3))
    return m

def shadow_from(mask):
    sh = np.zeros_like(mask)
    for dy, blur, a in [(60, 120, .16), (24, 48, .10), (4, 10, .06)]:
        m = np.roll(mask, dy, 0); m[:dy] = 0
        sh = 1 - (1 - sh) * (1 - a * cv2.GaussianBlur(m, (0, 0), blur / 2))
    return sh

CARD = dict(x=-65, y=1200, w=1210, h=864, r=200)
CM = squircle_mask(CARD['x'], CARD['y'], CARD['w'], CARD['h'], CARD['r'])
CSH = shadow_from(CM) * (1 - CM)
# constants of the split blend, computed once (same float32 expressions as the per-frame form they replace)
SHADE = 1 - CSH[..., None] * (1 - np.array([24, 24, 32], np.float32) / 255)      # card shadow multiplier
CM3 = CM[..., None]; CM3I = 1 - CM3
Y_CARD = int(np.argmax((CM.max(1) > 0) | (CSH.max(1) > 0)))                     # first row the card or its shadow touches
SCALE_SPLIT = 1.35      # set per short by split_geometry(): webcam = whole face (hair ~1105 .. chin <= ~1895) fits the visible card;
                        # 16:9 camera frame = the spec geometry (1890x1063 at x -405, y 1008)
HAIR_Y, CHIN_Y = 1105, 1895
RAMP = np.ones(Hc, np.float32); RAMP[1200:1240] = np.linspace(1, 0, 40); RAMP[1240:] = 0

# ---------------------------------------------------------------- readers
def reader(path, pix='rgb24', ch=3, size=None, start=None, count=None):
    """decoded frames of a stream; start/count seek frame-exactly to frame `start` of these 60 fps CFR streams (previews)"""
    if size is None:
        o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip().split(',')
        size = (int(o[0]), int(o[1]))
    w, h = size
    pre = ['-ss', f'{(start - 0.5) / FPS:.6f}'] if start else []     # half a frame early: lands on frame `start` whatever the container's timestamp rounding
    post = ['-frames:v', str(count)] if count else []
    p = subprocess.Popen(['ffmpeg', '-v', 'error'] + pre + ['-i', path] + post + ['-f', 'rawvideo', '-pix_fmt', pix, '-'], stdout=subprocess.PIPE)
    n = w * h * ch
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, ch)

def unsharp(img, amt=0.35, sig=1.2):
    bl = cv2.GaussianBlur(img, (0, 0), sig)
    return cv2.addWeighted(img, 1 + amt, bl, -amt, 0)

def pip_fullcam(fr):
    sc = Hc / fr.shape[0]; w = int(round(fr.shape[1] * sc))
    big = cv2.resize(fr, (w, Hc), interpolation=cv2.INTER_LANCZOS4)
    x0 = (w - Wc) // 2
    return unsharp(big[:, x0:x0 + Wc])

SIDE_W = None
def matte_kind(i):
    try: return json.load(open(f'{sk}/cam/r{i}_matte.json', encoding='utf-8')).get('model', 'u2net')
    except (OSError, ValueError): return 'u2net'

def split_frame(bg, fr, al, yf, rvm=False):
    global SIDE_W
    fw = int(round(fr.shape[1] * SCALE_SPLIT)); fh = int(round(fr.shape[0] * SCALE_SPLIT))
    xf = int(round(540 - fw / 2))
    big = unsharp(cv2.resize(fr, (fw, fh), interpolation=cv2.INTER_LANCZOS4)).astype(np.float32)
    A = cv2.resize(al, (fw, fh), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255
    if not rvm: A = cv2.erode(A, np.ones((3, 3), np.uint8), iterations=1)   # u2net's dark rim
    A = cv2.GaussianBlur(A, (0, 0), 0.6 if rvm else 1.2)
    # soft fill for the card strips the portrait webcam can't reach: same frame, enlarged + blurred, about the same centre
    s2 = Wc * 1.12 / fr.shape[1]; fw2, fh2 = int(round(fr.shape[1] * s2)), int(round(fr.shape[0] * s2))
    blur = cv2.GaussianBlur(cv2.resize(fr, (fw2 // 4, fh2 // 4), interpolation=cv2.INTER_AREA), (0, 0), 6)
    blur = cv2.resize(blur, (fw2, fh2), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    cy = yf + fh / 2; xb, yb = int(round(540 - fw2 / 2)), int(round(cy - fh2 / 2))
    foot = np.zeros((Hc, Wc, 3), np.float32); alpha = np.zeros((Hc, Wc), np.float32)
    ys0, ys1 = max(0, yb), min(Hc, yb + fh2); xs0, xs1 = max(0, xb), min(Wc, xb + fw2)
    foot[ys0:ys1, xs0:xs1] = blur[ys0 - yb:ys1 - yb, xs0 - xb:xs1 - xb]
    if SIDE_W is None or SIDE_W.shape[0] != fw:
        SIDE_W = np.clip(np.minimum(np.arange(fw), fw - 1 - np.arange(fw)) / 40.0, 0, 1).astype(np.float32)
    ys0, ys1 = max(0, yf), min(Hc, yf + fh); xs0, xs1 = max(0, xf), min(Wc, xf + fw)
    wgt = SIDE_W[xs0 - xf:xs1 - xf][None, :, None]
    foot[ys0:ys1, xs0:xs1] = big[ys0 - yf:ys1 - yf, xs0 - xf:xs1 - xf] * wgt + foot[ys0:ys1, xs0:xs1] * (1 - wgt)
    alpha[ys0:ys1, xs0:xs1] = A[ys0 - yf:ys1 - yf, xs0 - xf:xs1 - xf] * SIDE_W[xs0 - xf:xs1 - xf][None, :]
    out = bg.astype(np.float32)
    # above the card, its shadow and the head nothing changes (shade 1, card 0, alpha 0), so the blend runs on the rows below y only:
    # the same three float32 expressions as before, on fewer pixels, identical output
    y = max(0, min(Y_CARD, ys0))
    o = out[y:]
    o *= SHADE[y:]
    o[:] = o * CM3I[y:] + foot[y:] * CM3[y:]
    Ah = alpha[y:] * RAMP[y:, None]
    o[:] = o * (1 - Ah[..., None]) + foot[y:] * Ah[..., None]
    return out

def hair_top(matte_path, size):
    w, h = size; tops = []
    for k, a in enumerate(reader(matte_path, 'rgba', 4, (w, h))):
        if k % 6: continue
        col = a[:, int(w * 0.3):int(w * 0.7), 3].max(1)
        idx = np.where(col > 128)[0]
        if len(idx): tops.append(idx[0])
    return float(np.median(tops)), float(np.min(tops))

def chin_max(clip, size):
    import mediapipe as mp
    from mediapipe.tasks import python as mpt
    from mediapipe.tasks.python import vision
    det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path='face_landmarker.task'), num_faces=1))
    ch = []
    for k, fr in enumerate(reader(clip, 'rgb24', 3, tuple(size))):
        if k % 10: continue
        res = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(fr)))
        if res.face_landmarks: ch.append(res.face_landmarks[0][152].y * size[1])
    return float(np.max(ch)) if ch else size[1] * 0.7

def split_geometry():
    """one scale for every split run of the short (cached): whole face visible, hair popping ~95 px above the card"""
    gf = f'{sk}/cam/split_geom.json'
    runs = sorted(int(ri) for ri, p in CAM.items() if p['layout'] == 'split')
    # the cache is keyed by the clips it was measured on (a re-cut that keeps the same run indices still re-measures)
    src = {str(ri): [(f, os.path.getsize(f), int(os.path.getmtime(f) * 1000)) if os.path.exists(f) else (f, None, None)
                     for f in (CAM[str(ri)]['file'], f'{sk}/cam/r{ri}_matte.mov')] for ri in runs}
    if os.path.exists(gf):
        g = json.load(open(gf, encoding='utf-8'))
        if g.get('runs') == runs and g.get('src') == json.loads(json.dumps(src)): return g
    g = dict(runs=runs, src=src, per_run={})
    kinds = {CAM[str(ri)].get('kind', 'pip') for ri in runs}
    if kinds == {'frame'}:
        g.update(scale=1890 / 1920)
        for ri in runs: g['per_run'][str(ri)] = dict(yf=1008)
    else:
        scales = []
        for ri in runs:
            p = CAM[str(ri)]; size = p.get('size', [680, 924])
            try:
                med, mn = hair_top(f'{sk}/cam/r{ri}_matte.mov', size); cm = chin_max(p['file'], size)
            except ValueError:
                raise SystemExit(f'{sk} run {ri} (split): no head found in its matte. The camera is probably hidden in that part of the '
                                 f'source (check {sk}_eyes.png / gaze.py); a split run needs the speaker on camera. Fix shorts.json and re-cut.')
            scales.append((CHIN_Y - HAIR_Y) / max(1, cm - med))
            g['per_run'][str(ri)] = dict(hair_med=med, hair_min=mn, chin_max=cm)
        g['scale'] = float(np.floor(min(min(scales), 2.2) * 100) / 100)
        for ri in runs:
            pr = g['per_run'][str(ri)]; pr['yf'] = int(round(HAIR_Y - g['scale'] * pr['hair_med']))
    json.dump(g, open(gf, 'w'), indent=1)
    return g

# ---------------------------------------------------------------- CTA comment box
CTA_BOX = (43, 1344, 994, 276)
CTA_CACHE = {}
def cta_render(t_rel, spec):
    """returns RGBA (Hc x Wc) numpy or None. The drawing is a pure function of (landing progress, typed chars, posted,
    caret blink, press squash, button colour); frames with the same state reuse the same canvas (the three shadow blurs at 2x
    are the cost), so the outro renders ~60 distinct boxes instead of one per frame. Pixel-identical by construction."""
    land = min(1, max(0, (t_rel - spec['land']) / 0.5))
    if land <= 0: return None
    n = int(max(0, min(len(spec['kw']), (t_rel - spec['type0']) * spec['cps'] + 1e-6))) if t_rel >= spec['type0'] else 0
    posted = t_rel >= spec['press'] + 0.12
    blink = (int((t_rel - spec['type0']) * 2.2) % 2 == 0) if t_rel > spec['type0'] + len(spec['kw']) / spec['cps'] else True
    pp = (t_rel - spec['press']) / 0.24
    sc = 1 - 0.08 * np.sin(np.pi * pp) if 0 <= pp <= 1 else 1
    col = AZURE_INK if 0 <= pp <= 1 else AZURE
    key = (land, n, posted, blink, float(sc), col)
    draw = _cta_draw_full if spec.get('mode') == 'full_video' else _cta_draw
    if key not in CTA_CACHE: CTA_CACHE[key] = draw(land, n, posted, blink, sc, col, spec)
    return CTA_CACHE[key]


def _glass_card(bw, bh, ss, pad):
    """the CTA card's graphite glass: stage-800, white hairline + top highlight, the long panel shadow"""
    im = Image.new('RGBA', (bw * ss + 2 * pad, bh * ss + 2 * pad), (0, 0, 0, 0))
    ox, oy = pad, pad; R = 44 * ss
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((ox + 40 * ss, oy + 90 * ss, ox + bw * ss - 40 * ss, oy + bh * ss + 50 * ss), R, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(50 * ss)); im.putalpha(m.point(lambda v: int(v * 0.8)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((ox, oy, ox + bw * ss, oy + bh * ss), R, fill=STAGE800 + (246,))
    d.rounded_rectangle((ox, oy, ox + bw * ss, oy + bh * ss), R, outline=(255, 255, 255, 34), width=3)
    d.line((ox + R, oy + 3, ox + bw * ss - R, oy + 3), fill=(255, 255, 255, 26), width=2)
    return im, ox, oy


def _play_tile(size):
    """the design system's glossy azure icon tile with a white play glyph (RGBA, size x size)"""
    t = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    g = np.linspace(0, 1, size, dtype=np.float32)[:, None, None]
    top, mid, bot = np.array([143, 203, 255], np.float32), np.array([59, 152, 255], np.float32), np.array([27, 99, 230], np.float32)
    col = np.where(g < 0.45, top + (mid - top) * (g / 0.45), mid + (bot - mid) * ((g - 0.45) / 0.55))
    grad = Image.fromarray(np.repeat(col, size, 1).clip(0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    mk = Image.new('L', (size, size), 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, size - 1, size - 1), int(size * 0.285), fill=255)
    t.paste(grad, (0, 0), mk)
    hl = Image.new('L', (size, size), 0)
    ImageDraw.Draw(hl).ellipse((size * 0.1, size * 0.04, size * 0.9, size * 0.52), fill=95)
    hl = hl.filter(ImageFilter.GaussianBlur(size * 0.04))
    hl = Image.fromarray(np.minimum(np.asarray(hl), np.asarray(mk)))
    white = Image.new('RGBA', (size, size), (255, 255, 255, 0)); white.putalpha(hl)
    t = Image.alpha_composite(t, white)
    c, r = size / 2, size * 0.2
    ImageDraw.Draw(t).polygon([(c - r * 0.75, c - r), (c - r * 0.75, c + r), (c + r * 1.05, c)], fill=(255, 255, 255, 255))
    return t


def _cta_draw_full(land, n, posted, blink, sc, col, spec):
    """the outro card every short ends on (Leon's rule, 2026-10-14): 'Watch the full video', pointing down at the
    full-video link under the short. Graphite glass card, his glossy azure play tile, the line typed in white Figtree 600
    with an azure caret, and an azure arrow button with a soft glow that presses (azure-ink) once the line is typed."""
    x0, y0, bw, bh = CTA_BOX
    e = 1 - (1 - land) ** 3
    ss = 2; pad = 200
    im, ox, oy = _glass_card(bw, bh, ss, pad)
    cy = oy + bh * ss / 2
    ts = 116 * ss; tx0 = ox + 40 * ss
    tile = _play_tile(ts)
    glow = Image.new('L', im.size, 0); ImageDraw.Draw(glow).rounded_rectangle((tx0, cy - ts / 2 + 26 * ss, tx0 + ts, cy + ts / 2 + 26 * ss), int(ts * 0.285), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(22 * ss))
    gl = Image.new('RGBA', im.size, AZURE + (0,)); gl.putalpha(glow.point(lambda v: int(v * 0.5)))
    im = Image.alpha_composite(im, gl); im.alpha_composite(tile, (int(tx0), int(cy - ts / 2)))
    d = ImageDraw.Draw(im)
    txt = spec['kw'][:n]
    ft = vfont('Figtree-VF.ttf', 56 * ss, 600)
    tx = tx0 + ts + 32 * ss; tw = d.textlength(txt, font=ft)
    d.text((tx, cy), txt, font=ft, fill=(255, 255, 255, 255), anchor='lm')
    if not posted and blink:
        d.rounded_rectangle((tx + tw + 6 * ss, cy - 32 * ss, tx + tw + 12 * ss, cy + 32 * ss), 3 * ss, fill=AZURE + (255,))
    # the arrow button: points down at the full-video link under the short
    br = 56 * ss * sc; bxc = ox + bw * ss - 40 * ss - 56 * ss
    glow = Image.new('L', im.size, 0); ImageDraw.Draw(glow).ellipse((bxc - br, cy - br, bxc + br, cy + br), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(16 * ss))
    gl = Image.new('RGBA', im.size, AZURE + (0,)); gl.putalpha(glow.point(lambda v: int(v * 0.55)))
    im = Image.alpha_composite(im, gl); d = ImageDraw.Draw(im)
    d.ellipse((bxc - br, cy - br, bxc + br, cy + br), fill=col + (255,))
    a = 22 * ss * sc; w = max(2, int(7 * ss * sc))
    d.line((bxc, cy - a, bxc, cy + a), fill=(255, 255, 255, 255), width=w)
    d.line((bxc - a * 0.75, cy + a * 0.2, bxc, cy + a), fill=(255, 255, 255, 255), width=w, joint='curve')
    d.line((bxc + a * 0.75, cy + a * 0.2, bxc, cy + a), fill=(255, 255, 255, 255), width=w, joint='curve')
    for px in (bxc, bxc - a * 0.75, bxc + a * 0.75):                      # round caps
        py = cy + a if px == bxc else cy + a * 0.2
        d.ellipse((px - w / 2, py - w / 2, px + w / 2, py + w / 2), fill=(255, 255, 255, 255))
    d.ellipse((bxc - w / 2, cy - a - w / 2, bxc + w / 2, cy - a + w / 2), fill=(255, 255, 255, 255))
    im = im.resize((im.size[0] // ss, im.size[1] // ss), Image.LANCZOS)
    scl = 0.94 + 0.06 * e; W0, H0 = im.size
    im = im.resize((max(1, int(W0 * scl)), max(1, int(H0 * scl))), Image.LANCZOS)
    arr = np.asarray(im).astype(np.float32); arr[..., 3] *= min(1, land * 2.2)
    canvas = np.zeros((Hc, Wc, 4), np.float32)
    px = int(round(x0 + bw / 2 - im.size[0] / 2)); py = int(round(y0 + bh / 2 - im.size[1] / 2 + 40 * (1 - e)))
    ys0, ys1 = max(0, py), min(Hc, py + im.size[1]); xs0, xs1 = max(0, px), min(Wc, px + im.size[0])
    canvas[ys0:ys1, xs0:xs1] = arr[ys0 - py:ys1 - py, xs0 - px:xs1 - px]
    return canvas

def _cta_draw(land, n, posted, blink, sc, col, spec):
    """the comment box in the channel's design system: graphite glass (stage-800), white hairline + top highlight, the
    long panel shadow, a stage-700 avatar, the keyword in Figtree 600 white with an azure caret, an azure Post button
    with a soft glow that darkens to azure-ink on the press"""
    x0, y0, bw, bh = CTA_BOX
    e = 1 - (1 - land) ** 3
    ss = 2; pad = 200
    im = Image.new('RGBA', (bw * ss + 2 * pad, bh * ss + 2 * pad), (0, 0, 0, 0))
    ox, oy = pad, pad; R = 44 * ss
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((ox + 40 * ss, oy + 90 * ss, ox + bw * ss - 40 * ss, oy + bh * ss + 50 * ss), R, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(50 * ss)); im.putalpha(m.point(lambda v: int(v * 0.8)))      # 0 50 120 -40 shadow
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((ox, oy, ox + bw * ss, oy + bh * ss), R, fill=STAGE800 + (246,))
    d.rounded_rectangle((ox, oy, ox + bw * ss, oy + bh * ss), R, outline=(255, 255, 255, 34), width=3)
    d.line((ox + R, oy + 3, ox + bw * ss - R, oy + 3), fill=(255, 255, 255, 26), width=2)
    # default avatar
    cx, cy, rr = ox + 40 * ss + 58 * ss, oy + bh * ss / 2, 58 * ss
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=STAGE700 + (255,))
    d.ellipse((cx - 22 * ss, cy - 36 * ss, cx + 22 * ss, cy + 8 * ss), fill=TEXT_MUTED + (255,))
    d.pieslice((cx - 42 * ss, cy + 12 * ss, cx + 42 * ss, cy + 92 * ss), 180, 360, fill=TEXT_MUTED + (255,))
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(66, 67, 71, 255), width=3)
    # input field: a lighter glass well. PIL replaces pixels instead of blending, so the 6% white lift over stage-800 is
    # mixed here (a translucent fill would punch a see-through hole in the card)
    fx0, fx1 = cx + rr + 26 * ss, ox + bw * ss - 250 * ss
    fy0, fy1 = cy - 58 * ss, cy + 58 * ss
    d.rounded_rectangle((fx0, fy0, fx1, fy1), 58 * ss, fill=(38, 39, 42, 248), outline=(58, 59, 63, 248), width=2)
    txt = spec['kw'][:n]
    ft = vfont('Figtree-VF.ttf', 52 * ss, 600)
    tx = fx0 + 36 * ss; tw = d.textlength(txt, font=ft)
    d.text((tx, cy), txt, font=ft, fill=(255, 255, 255, 255), anchor='lm')
    if not posted and blink:
        d.rounded_rectangle((tx + tw + 6 * ss, cy - 32 * ss, tx + tw + 12 * ss, cy + 32 * ss), 3 * ss, fill=AZURE + (255,))
    # Post button (press = quick squash + azure-ink), with the accent glow
    bxc, byc = ox + bw * ss - 40 * ss - 95 * ss, cy
    hw, hh = 95 * ss * sc, 50 * ss * sc
    glow = Image.new('L', im.size, 0); ImageDraw.Draw(glow).rounded_rectangle((bxc - hw, byc - hh, bxc + hw, byc + hh), hh, fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(16 * ss))
    gl = Image.new('RGBA', im.size, AZURE + (0,)); gl.putalpha(glow.point(lambda v: int(v * 0.55)))
    im = Image.alpha_composite(im, gl); d = ImageDraw.Draw(im)
    d.rounded_rectangle((bxc - hw, byc - hh, bxc + hw, byc + hh), hh, fill=col + (255,))
    fb = vfont('Figtree-VF.ttf', 40 * ss * sc, 600)
    d.text((bxc, byc), 'Post', font=fb, fill=(255, 255, 255, 255), anchor='mm')
    im = im.resize((im.size[0] // ss, im.size[1] // ss), Image.LANCZOS)
    # landing: scale .94->1, y +40->0, opacity
    scl = 0.94 + 0.06 * e; W0, H0 = im.size
    im = im.resize((max(1, int(W0 * scl)), max(1, int(H0 * scl))), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32); a[..., 3] *= min(1, land * 2.2)
    canvas = np.zeros((Hc, Wc, 4), np.float32)
    px = int(round(x0 + bw / 2 - im.size[0] / 2)); py = int(round(y0 + bh / 2 - im.size[1] / 2 + 40 * (1 - e)))
    ys0, ys1 = max(0, py), min(Hc, py + im.size[1]); xs0, xs1 = max(0, px), min(Wc, px + im.size[0])
    canvas[ys0:ys1, xs0:xs1] = a[ys0 - py:ys1 - py, xs0 - px:xs1 - px]
    return canvas

# ---------------------------------------------------------------- cover (frame 0 only)
def cover_rgba(title_lines):
    """frame 0's title in the design system: white Figtree 600 at the headline tracking on a graphite glass card (accent
    hairline + bloom, the long panel shadow) with the azure accent line drawn beneath the words - the keyword-pop chip at
    title size. Centred at y ~432 (the spec's 262-603 band for two lines); the graphic keeps everything below 620."""
    acc = ACCENTS['azure']; track = -0.03; size = 104
    while True:
        ft = vfont('Figtree-VF.ttf', size, 600)
        tws = [ft.getlength(l) + track * ft.size * (len(l) - 1) for l in title_lines]
        if max(tws) <= 900 or size <= 72: break
        size -= 4
    cap = ft.getbbox('H')[3] - ft.getbbox('H')[1]; dsc = ft.getbbox('gjpqy')[3] - ft.getbbox('H')[3]
    lh = int(size * 1.08); padx, pady = 56, 44
    text_h = lh * (len(title_lines) - 1) + cap
    line_gap, line_h = dsc + 18, 6
    bw = int(max(tws) + 2 * padx); bh = int(pady + text_h + line_gap + line_h + pady)
    cyc = 432; bx0, by0 = (Wc - bw) // 2, int(cyc - bh / 2); bx1, by1 = bx0 + bw, by0 + bh; r = 36
    im = Image.new('RGBA', (Wc, Hc), (0, 0, 0, 0))

    def soft(rect, rgba, blur):
        m = Image.new('L', (Wc, Hc), 0); ImageDraw.Draw(m).rounded_rectangle(rect, r, fill=255)
        m = m.filter(ImageFilter.GaussianBlur(blur))
        lay = Image.new('RGBA', (Wc, Hc), rgba[:3] + (0,)); lay.putalpha(m.point(lambda v: int(v * rgba[3] / 255)))
        return lay
    im = Image.alpha_composite(im, soft((bx0 + 40, by0 + 90, bx1 - 40, by1 + 50), (0, 0, 0, 210), 50))
    im = Image.alpha_composite(im, soft((bx0 + 30, by0 + 30, bx1 - 30, by1 - 30), acc + (140,), 50))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((bx0, by0, bx1, by1), r, fill=STAGE800 + (240,))
    d.rounded_rectangle((bx0, by0, bx1, by1), r, outline=acc + (84,), width=2)
    d.line((bx0 + r, by0 + 1.5, bx1 - r, by0 + 1.5), fill=(255, 255, 255, 24), width=1)
    ty = by0 + pady
    for j, (l, tw) in enumerate(zip(title_lines, tws)):
        tracked(d, ((Wc - tw) / 2, ty + j * lh - ft.getbbox('H')[1]), l, ft, (255, 255, 255, 255), track)
    ly = ty + text_h + line_gap; lw = max(tws); lx0 = (Wc - lw) / 2
    glow = Image.new('L', (Wc, Hc), 0); ImageDraw.Draw(glow).rounded_rectangle((lx0, ly, lx0 + lw, ly + line_h), 3, fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    gl = Image.new('RGBA', (Wc, Hc), acc + (0,)); gl.putalpha(glow.point(lambda v: int(v * 0.8)))
    im = Image.alpha_composite(im, gl)
    ImageDraw.Draw(im).rounded_rectangle((lx0, ly, lx0 + lw, ly + line_h), 3, fill=acc + (255,))
    return np.asarray(im).astype(np.float32)

_BBOX = {}
def over(dst, rgba, y=None):
    """alpha-over an RGBA float canvas onto dst, touching only the rows/cols where its alpha is non-zero (elsewhere the
    blend is dst*1 + rgb*0 = dst exactly). The bounding box is cached per canvas object (the CTA canvases are memoised)."""
    key = id(rgba)
    box = _BBOX.get(key)
    if box is None or box[0] is not rgba:
        rows = np.where(rgba[..., 3].any(1))[0]; cols = np.where(rgba[..., 3].any(0))[0]
        box = (rgba, (rows[0], rows[-1] + 1, cols[0], cols[-1] + 1) if len(rows) else None); _BBOX[key] = box
    if box[1] is None: return
    y0, y1, x0, x1 = box[1]
    a = rgba[y0:y1, x0:x1, 3:4] / 255.0
    sub = dst[y0:y1, x0:x1]
    sub[:] = sub * (1 - a) + rgba[y0:y1, x0:x1, :3] * a

# ---------------------------------------------------------------- main loop
chunks = build_chunks()
cap_imgs = [chip_parts(c['text'], S.get('accent', 'azure')) if c['hl'] else caption_img(c['text']) for c in chunks]
json.dump([dict(text=c['text'], hl=c['hl'], t0=round(c['t0'], 3), t1=round(c['t1'], 3)) for c in chunks], open(f'{sk}/captions.json', 'w'), indent=1)

last = RUNS[-1]
if S.get('cta_mode', 'full_video') == 'full_video':
    # Leon's rule (2026-10-14): every short ends by sending viewers to the full video - the card reads "Watch the full
    # video" and its arrow points down at the full-video link (YouTube's related video; "link in bio" on TikTok / IG)
    kw = S.get('cta_text', 'Watch the full video')
    spec = dict(kw=kw, land=0.12, type0=0.45, cps=16.0, mode='full_video')
    spec['type0'] = max(0.3, min(spec['type0'], last['T1'] - last['T0'] - 0.3 - 0.45 - len(kw) / spec['cps']))
    spec['press'] = spec['type0'] + len(kw) / spec['cps'] + 0.45
else:                                              # "cta_mode": "comment": the comment box typing the CTA keyword
    cta_line = [L for L in S['lines'] if L.get('cta')][0]
    kw = S['cta_keyword']
    tw = [w for w in C['words'] if w['line'] == cta_line['id'] and w['w'].lower().strip('.,') == kw.lower()]
    t_kw = (tw[0]['s'] if tw else last['T0'] + 0.8) - last['T0']
    spec = dict(kw=kw, land=0.12, type0=max(0.55, t_kw), cps=10.0)
    # the Post press must finish on screen: when the keyword is the outro's last word, start typing earlier
    spec['type0'] = max(0.55, min(spec['type0'], last['T1'] - last['T0'] - 0.3 - 0.55 - len(kw) / spec['cps']))
    spec['press'] = spec['type0'] + len(kw) / spec['cps'] + 0.55
extra = [dict(t=last['T0'] + spec['land'], type='pop')]
extra += [dict(t=last['T0'] + spec['type0'] + k / spec['cps'], type='key') for k in range(len(kw)) if kw[k] != ' ']
extra += [dict(t=last['T0'] + spec['press'], type='click')]
json.dump(extra, open(f'{sk}/events_extra.json', 'w'), indent=1)
if '--events-only' in sys.argv:
    print(f'{sk}: {len(chunks)} caption chunks -> {sk}/captions.json; {len(extra)} CTA events -> {sk}/events_extra.json'); sys.exit(0)

yf = {}
if any(p['layout'] == 'split' for p in CAM.values()) and not CONCAT:
    GEO = split_geometry(); SCALE_SPLIT = GEO['scale']
    for ri, pr in GEO['per_run'].items():
        yf[int(ri)] = pr['yf']
    print('split geometry: scale', SCALE_SPLIT, {ri: pr for ri, pr in GEO['per_run'].items()})
title = S.get('cover', [S['title']])
COVER = cover_rgba(title)

def frames():
    """yields (n, run, image); image is None for frames a preview doesn't need (decoders still advance, nothing is composited)"""
    for r in RUNS:
        if ONLY is not None and r['i'] not in ONLY: continue
        n0, n1 = round(r['T0'] * FPS), round(r['T1'] * FPS)
        need = lambda n: want is None or n in want
        if want is not None and not any(need(n) for n in range(n0, n1)): continue
        if want is not None:
            # preview: seek each stream straight to the wanted frames instead of decoding the run from its start (same frame
            # data, same composite); a spot-check takes seconds instead of the whole run's decode
            gfx = f'gfx/out60/{sk}_r{r["i"]}.mp4'; cam = CAM.get(str(r['i']), {})
            for n in sorted(x for x in want if n0 <= x < n1):
                k = n - n0
                if r['layout'] == 'fv':
                    yield n, r, next(reader(gfx, start=k, count=1)).astype(np.float32)
                elif r['layout'] == 'fc':
                    fr = next(reader(cam['file'], 'rgb24', 3, start=k, count=1))
                    yield n, r, (fr if cam.get('kind', cam.get('cam')) in ('slice', 'cam4k') else pip_fullcam(fr)).astype(np.float32)
                else:
                    bg = next(reader(gfx, start=k, count=1)); fr = next(reader(cam['file'], 'rgb24', 3, start=k, count=1))
                    ma = next(reader(f'{sk}/cam/r{r["i"]}_matte.mov', 'rgba', 4, tuple(cam.get('size', [680, 924])), start=k, count=1))
                    yield n, r, split_frame(bg, fr, ma[..., 3], yf[r['i']], matte_kind(r['i']) == 'rvm')
            continue
        if r['layout'] == 'fv':
            g = reader(f'gfx/out60/{sk}_r{r["i"]}.mp4')
            for n in range(n0, n1):
                fr = next(g); yield n, r, (fr.astype(np.float32) if need(n) else None)
        elif r['layout'] == 'fc':
            p = CAM[str(r['i'])]
            g = reader(p['file'], 'rgb24', 3)
            for n in range(n0, n1):
                fr = next(g)
                yield n, r, (((fr if p.get('kind', p.get('cam')) in ('slice', 'cam4k') else pip_fullcam(fr)).astype(np.float32)) if need(n) else None)
        else:
            g = reader(f'gfx/out60/{sk}_r{r["i"]}.mp4'); c = reader(CAM[str(r['i'])]['file'], 'rgb24', 3)
            m = reader(f'{sk}/cam/r{r["i"]}_matte.mov', 'rgba', 4, tuple(CAM[str(r['i'])].get('size', [680, 924])))
            rvm = matte_kind(r['i']) == 'rvm'
            for n in range(n0, n1):
                bg, fr, ma = next(g), next(c), next(m)
                yield n, r, (split_frame(bg, fr, ma[..., 3], yf[r['i']], rvm) if need(n) else None)

want = None if PREVIEW is None else {int(round(t * FPS)) for t in PREVIEW}
VENC = ['-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-profile:v', 'high',
        '-r', str(FPS), '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709']

def concat():
    segs = [f'{sk}/seg/run{r["i"]:02d}.mp4' for r in RUNS]
    open(f'{sk}/seg/list.txt', 'w').write(''.join("file '" + os.path.basename(p) + "'\n" for p in segs))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{sk}/seg/list.txt', '-i', f'{sk}/mix.wav', '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', f'{sk}/final_video.mp4'], check=True)
    print('concatenated', len(segs), 'segments ->', f'{sk}/final_video.mp4')

if CONCAT:
    concat(); sys.exit(0)

# ---------------------------------------------------------------- parallel, cached segments
def seg_inputs(r):
    """everything a run's segment depends on: its inputs (path, size, mtime), its captions, the CTA/cover, this code"""
    i = r['i']; files = []
    if r['layout'] in ('fv', 'split'): files.append(f'gfx/out60/{sk}_r{i}.mp4')
    if r['layout'] in ('fc', 'split'): files.append(CAM[str(i)]['file'])
    if r['layout'] == 'split': files += [f'{sk}/cam/r{i}_matte.mov', f'{sk}/cam/split_geom.json']
    fst = [(f, os.path.getsize(f), int(os.path.getmtime(f) * 1000)) if os.path.exists(f) else (f, None, None) for f in files]
    caps = [dict(text=c['text'], hl=c['hl'], t0=round(c['t0'], 4), t1=round(c['t1'], 4)) for c in chunks if c['t1'] > r['T0'] and c['t0'] < r['T1']]
    key = dict(run=r, files=fst, caps=caps, matte=matte_kind(i) if r['layout'] == 'split' else None, cam=CAM[str(i)] if str(i) in CAM else None, scale=SCALE_SPLIT, yf=yf.get(i),
               cta=spec if r is last else None, cover=title if i == 0 else None, code=CODE_HASH, venc=VENC)
    return json.dumps(key, sort_keys=True, default=str), [f for f, s, m in fst if s is None]

if SEGMENTS:
    import hashlib, time
    CODE_HASH = hashlib.md5(open(__file__, 'rb').read()).hexdigest()
    jobs = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else len(RUNS)
    force = '--force' in sys.argv
    os.makedirs(f'{sk}/seg', exist_ok=True)
    todo, kept, missing = [], [], []
    for r in RUNS:
        key, miss = seg_inputs(r)
        if miss: missing += miss
        out = f'{sk}/seg/run{r["i"]:02d}.mp4'; kf = out[:-4] + '.key'
        if not force and os.path.exists(out) and os.path.getsize(out) > 0 and os.path.exists(kf) and open(kf).read() == key:
            kept.append(r['i']); continue
        todo.append((r, out, kf, key))
    if missing: raise SystemExit('missing inputs: ' + ', '.join(sorted(set(missing))) + '  (render the graphics / cam_prep / matte first)')
    print(f'{sk}: {len(todo)} segment(s) to render {[r["i"] for r, *_ in todo]}, {len(kept)} unchanged {kept}, {min(jobs, len(todo)) if todo else 0} at a time', flush=True)
    t0 = time.time(); procs = []; pending = list(todo); failed = []
    while pending or procs:
        while pending and len(procs) < jobs:
            r, out, kf, key = pending.pop(0)
            if os.path.exists(kf): os.remove(kf)
            p = subprocess.Popen([sys.executable, __file__, sk, '--runs', str(r['i']), '--seg-out', out]); procs.append((p, r, out, kf, key))
        time.sleep(0.5)
        for item in procs[:]:
            p, r, out, kf, key = item
            if p.poll() is None: continue
            procs.remove(item)
            if p.returncode != 0: failed.append(r['i']); continue
            open(kf, 'w').write(key)
    # every segment must hold exactly its run's frames (a graphic re-rendering underneath a composite yields a short segment)
    bad = []
    for r in RUNS:
        out = f'{sk}/seg/run{r["i"]:02d}.mp4'
        n = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', out],
                           capture_output=True, text=True).stdout.strip()
        want_n = round(r['T1'] * FPS) - round(r['T0'] * FPS)
        if not n.isdigit() or int(n) != want_n: bad.append((r['i'], n, want_n))
    print(f'{sk}: segments done in {time.time() - t0:.0f}s' + (f'; FAILED runs {failed}' if failed else '') + (f'; FRAME COUNT MISMATCH (run, got, want): {bad}' if bad else ''), flush=True)
    if failed or bad: sys.exit(1)
    if '--no-concat' not in sys.argv: concat()
    sys.exit(0)
if PREVIEW is None:
    if SEG_OUT:
        enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{Wc}x{Hc}', '-r', str(FPS), '-i', '-'] + VENC + [SEG_OUT], stdin=subprocess.PIPE)
    else:
        enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{Wc}x{Hc}', '-r', str(FPS), '-i', '-',
                                '-i', f'{sk}/mix.wav', '-map', '0:v', '-map', '1:a'] + VENC + ['-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', f'{sk}/final_video.mp4'], stdin=subprocess.PIPE)
PDIR = f'{sk}/thumb' if CLEAN else f'{sk}/preview'
os.makedirs(PDIR, exist_ok=True)
count = 0
for n, r, img in frames():
    if img is None: continue
    t = n / FPS
    # captions (never on frame 0)
    if n > 0 and not CLEAN:
        for k, (c, ci) in enumerate(zip(chunks, cap_imgs)):
            if c['t0'] <= t + 1e-6 < c['t1']:
                cy = caption_center_y(r)
                if c['hl']:                                   # the glass chip pops in and draws its accent line
                    im_, scl, al, dy = chip_render(k, ci, t - c['t0'])
                    paste_rgba(img, im_, Wc / 2, cy + dy, scl, al)
                    break
                h, w = ci.shape[:2]
                x0, y0 = (Wc - w) // 2, int(round(cy - h / 2))
                sub = img[y0:y0 + h, x0:x0 + w]; a = ci[..., 3:4] / 255.0
                sub[:] = sub * (1 - a) + ci[..., :3] * a
                break
    if r is last and not CLEAN:
        ov = cta_render(t - r['T0'], spec)
        if ov is not None: over(img, ov)
    if n == 0 and not CLEAN: over(img, COVER)
    np.add(img, 0.5, out=img); np.clip(img, 0, 255, out=img); out = img.astype(np.uint8)   # in place: same values, no temporaries
    if want is not None:
        Image.fromarray(out).save(f'{PDIR}/f_{t:07.3f}.png')
    else:
        enc.stdin.write(out.tobytes())
    count += 1
if PREVIEW is None:
    enc.stdin.close(); enc.wait()
print('frames', count, 'of', NF)
