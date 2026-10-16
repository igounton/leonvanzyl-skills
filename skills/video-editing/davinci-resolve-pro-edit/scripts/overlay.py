"""Alpha overlays for the top video track (ProRes 4444 with alpha, timeline resolution), drawn in code:

  words  hook keyword pop in the channel's slide style: a graphite glass chip, Figtree 600 white, the accent line
         drawn in beneath (azure, or "accent": "ember"), an optional Geist Mono "label" eyebrow. (hook only)
         {"id": "w02", "kind": "words", "t0": 6.10, "t1": 7.35, "text": "half the cost", "accent": "azure", "xy": [960, 905]}
  cta    lower-third community card: avatar or logo, a label, the URL typed with a clay caret, then a button press.
         {"id": "c01", "kind": "cta", "t0": 118.2, "t1": 124.6, "url": "skool.com/leonvanzyl",
          "label": "Free AI builder community", "button": "Join", "type_at": 0.9, "logo": "gfx/assets/skool.png"}
         type_at = beat-relative second the typing starts (put it on the word that names the place).

Positions and sizes are layout px (1920x1080) and scale to the timeline. SFX for visible events (pop on landing,
key ticks while typing, click on the press) go to events/<id>.json for audio.py.
Every frame is a pure function of a small state (landing/fade progress, typed characters, caret, press): frames with
the same state reuse the same drawing, and only the drawing's own box is written into a persistent, otherwise
transparent frame, so a 4K overlay no longer allocates and converts a 130 MB canvas per frame. Pixel-identical.
usage: python scripts/overlay.py w02 c01 ... [--preview 0.5] [--tag v2] [--jobs N]   -> media/<id>[_v2].mov (or preview/<id>_<t>.png)
--tag v2 writes a new file for an edit (Resolve holds the old one open): then media_pool_item replace_clip.
--jobs N renders several beats at once, one process each (default 3)."""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, 'scripts'); import config as C, media as M
TAG = ('_' + sys.argv[sys.argv.index('--tag') + 1]) if '--tag' in sys.argv else ''   # edits: a new file, then replace_clip

U = C.UNIT


def font(name, size):
    return ImageFont.truetype(C.FONTS + name, int(round(size * U)))


def shadow_layer(size, box, radius):
    """the spec's three-layer shadow under a rounded box, as an RGBA image"""
    acc = np.zeros(size[::-1], np.float32)
    for dy, blur, a in C.SHADOW:
        m = Image.new('L', size, 0)
        x0, y0, x1, y1 = box
        ImageDraw.Draw(m).rounded_rectangle((x0, y0 + dy * U, x1, y1 + dy * U), int(radius), fill=255)
        m = m.filter(ImageFilter.GaussianBlur(blur / 2 * U))
        acc = 1 - (1 - acc) * (1 - a * np.asarray(m, np.float32) / 255)
    sh = Image.new('RGBA', size, (24, 24, 32, 0)); sh.putalpha(Image.fromarray((acc * 255).astype(np.uint8)))
    return sh


def place(canvas, im, cx, cy, scale=1.0, alpha=1.0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.size[0] * scale)), max(1, int(im.size[1] * scale))), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    a[..., 3] *= alpha
    h, w = a.shape[:2]; x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    ys0, ys1 = max(0, y0), min(C.TH, y0 + h); xs0, xs1 = max(0, x0), min(C.TW, x0 + w)
    if ys1 <= ys0 or xs1 <= xs0: return
    src = a[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]; dst = canvas[ys0:ys1, xs0:xs1]
    sa = src[..., 3:4] / 255; da = dst[..., 3:4] / 255
    oa = sa + da * (1 - sa)
    dst[..., :3] = np.where(oa > 0, (src[..., :3] * sa + dst[..., :3] * da * (1 - sa)) / np.maximum(oa, 1e-6), 0)
    dst[..., 3:4] = oa * 255


# ------------------------------------------------------------------ keyword pops
# The channel's slide system ("Leon YouTube" design system): a graphite glass chip (stage-800 fill, white hairline,
# top highlight, the long panel shadow, the highlighted-panel accent hairline + bloom), Figtree 600 white at the
# title tracking, and the accent line drawn in beneath the words. Accent azure #2F95FF by default, ember #FF8A5B
# with "accent": "ember" (the cognaitiv orange). An optional Geist Mono eyebrow ("label") sits above the words.
ACCENTS = {'azure': (47, 149, 255), 'ember': (255, 138, 91), 'iris': (156, 124, 255), 'mint': (79, 214, 160)}
WORDS_SIZE, WORDS_TRACK = 62, -0.025                       # layout px, em
WORDS_PADX, WORDS_PADY, WORDS_SHPAD, WORDS_RADIUS = 40, 26, 170, 28
GLASS = (24, 25, 28, 224)                                  # stage-800; more opaque than the slides' 62%: no backdrop blur here
SWEEP_T0, SWEEP_DUR = 0.10, 0.40                           # the accent line draws in just after the chip lands


def vfont(name, size, weight):
    f = ImageFont.truetype(C.FONTS + name, int(round(size * U)))
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f


def tracked(draw, xy, text, f, fill, track_em):
    """text with letter-spacing, keeping the font's kerning (advance = width of the prefix difference)"""
    x, y = xy; extra = track_em * f.size; prev = 0.0
    for i, ch in enumerate(text):
        draw.text((x + prev + i * extra, y), ch, font=f, fill=fill)
        prev = f.getlength(text[:i + 1])
    return prev + extra * (len(text) - 1)


def words_parts(b):
    """(chip with shadow + bloom, text layer, accent-line rect, accent colour) - drawn once per beat"""
    text = b['text']; acc = ACCENTS.get(b.get('accent', 'azure'), ACCENTS['azure'])
    f = vfont('Figtree-VF.ttf', WORDS_SIZE, 600)
    d0 = ImageDraw.Draw(Image.new('L', (1, 1)))
    tw = f.getlength(text) + WORDS_TRACK * f.size * (len(text) - 1)
    asc, desc = f.getmetrics(); cap = f.getbbox('H')[3] - f.getbbox('H')[1]
    label = b.get('label'); lf = vfont('GeistMono-VF.ttf', 18, 500) if label else None
    lh = (lf.getbbox('A')[3] + 14 * U) if label else 0
    dsc = f.getbbox('gjpqy')[3] - f.getbbox('H')[3]           # descender depth below the baseline
    line_gap, line_h = dsc + 14 * U, 5 * U
    lw = (lf.getlength(label.upper()) + 0.14 * lf.size * (len(label) - 1)) if label else 0   # a long eyebrow widens the chip
    cw = max(tw, lw) + 2 * WORDS_PADX * U
    ch = WORDS_PADY * U + lh + cap + line_gap + line_h + WORDS_PADY * U
    sp = WORDS_SHPAD * U; size = (int(cw + 2 * sp), int(ch + 2 * sp)); box = (sp, sp, sp + cw, sp + ch); r = int(WORDS_RADIUS * U)
    base = Image.new('RGBA', size, (0, 0, 0, 0))

    def soft(rect, rgba, blur):                             # a blurred rounded rect (shadow / bloom)
        m = Image.new('L', size, 0); ImageDraw.Draw(m).rounded_rectangle(rect, r, fill=255)
        m = m.filter(ImageFilter.GaussianBlur(blur))
        lay = Image.new('RGBA', size, rgba[:3] + (0,)); lay.putalpha(m.point(lambda v: int(v * rgba[3] / 255)))
        return lay
    x0, y0, x1, y1 = box
    base = Image.alpha_composite(base, soft((x0 + 40 * U, y0 + 90 * U, x1 - 40 * U, y1 + 50 * U), (0, 0, 0, 200), 50 * U))   # 0 50 120 -40 shadow
    base = Image.alpha_composite(base, soft((x0 + 30 * U, y0 + 30 * U, x1 - 30 * U, y1 - 30 * U), acc + (150,), 46 * U))      # accent bloom
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, r, fill=GLASS)
    d.rounded_rectangle(box, r, outline=acc + (84,), width=max(1, int(1.5 * U)))                                              # accent hairline
    d.line((x0 + r, y0 + 1.5 * U, x1 - r, y0 + 1.5 * U), fill=(255, 255, 255, 22), width=max(1, int(1 * U)))               # top highlight
    txt = Image.new('RGBA', size, (0, 0, 0, 0)); dt = ImageDraw.Draw(txt)
    ty = y0 + WORDS_PADY * U + lh
    if label:
        tracked(dt, (x0 + WORDS_PADX * U, y0 + WORDS_PADY * U - lf.getbbox('A')[1]), label.upper(), lf, (126, 129, 138, 255), 0.14)
    tracked(dt, (x0 + WORDS_PADX * U, ty - (asc - cap) + 0 * U - f.getbbox('H')[1] + (asc - cap)), text, f, (255, 255, 255, 255), WORDS_TRACK)
    ly = ty + cap + line_gap
    line = (x0 + WORDS_PADX * U, ly, x0 + WORDS_PADX * U + tw, ly + line_h)
    return base, txt, line, acc


def words_state(b, t):
    dur = b['t1'] - b['t0']
    pin = min(1.0, t / 0.26); pout = min(1.0, max(0.0, (dur - t) / 0.18))
    if pin <= 0 or pout <= 0: return None
    sw = min(1.0, max(0.0, (t - SWEEP_T0) / SWEEP_DUR))
    return (round(pin, 3), round(pout, 3), round(M.ease('power3.out')(sw), 3))


def words_draw(b, state, cache):
    if 'parts' not in cache: cache['parts'] = words_parts(b)
    base, txt, line, acc = cache['parts']
    pin, pout, sw = state
    e = M.ease('power3.out')(pin)
    im = Image.alpha_composite(base, txt)
    if sw > 0:                                             # the accent line, with a soft glow, drawn left to right
        x0, y0, x1, y1 = line; xe = x0 + (x1 - x0) * sw
        glow = Image.new('L', im.size, 0); ImageDraw.Draw(glow).rounded_rectangle((x0, y0, xe, y1), int(3 * U), fill=255)
        glow = glow.filter(ImageFilter.GaussianBlur(7 * U))
        gl = Image.new('RGBA', im.size, acc + (0,)); gl.putalpha(glow.point(lambda v: int(v * 0.8)))
        im = Image.alpha_composite(im, gl)
        ImageDraw.Draw(im).rounded_rectangle((x0, y0, xe, y1), int(3 * U), fill=acc + (255,))
    cx, cy = b.get('xy', [960, 905])
    canvas = np.zeros((C.TH, C.TW, 4), np.float32)
    place(canvas, im, cx * U, (cy + 12 * (1 - e)) * U, (0.96 + 0.04 * e) * (0.98 + 0.02 * pout), min(1.0, pin * 1.6) * pout)
    return canvas


def words_events(b):
    """a soft landing and the accent line drawing in (audio.py maps the types to the SFX library)"""
    return [dict(t=round(b['t0'] + 0.02, 3), type='pop'), dict(t=round(b['t0'] + SWEEP_T0, 3), type='highlight')]


# ------------------------------------------------------------------ community CTA card
CTA_BOX = (64, 836, 900, 176)          # x, y, w, h (layout px): bottom-left, clear of the webcam corner


def cta_static(b):
    """the card in the channel's design system: graphite glass (stage-800), white hairline + top highlight, the long
    panel shadow, a Geist Mono label, the URL in Figtree 600 white with an azure caret, an azure button"""
    x, y, w, h = CTA_BOX; r = 28
    pad = 260                                                    # room for the whole shadow falloff (no clipped edge)
    size = (int((w + 2 * pad) * U), int((h + 2 * pad) * U))
    box = (pad * U, pad * U, (pad + w) * U, (pad + h) * U)
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).rounded_rectangle((box[0] + 40 * U, box[1] + 90 * U, box[2] - 40 * U, box[3] + 50 * U), int(r * U), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(50 * U))
    im = Image.new('RGBA', size, (0, 0, 0, 0)); im.putalpha(m.point(lambda v: int(v * 0.8)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, int(r * U), fill=C.STAGE800 + (246,))
    d.rounded_rectangle(box, int(r * U), outline=(255, 255, 255, 34), width=max(1, int(1.5 * U)))
    d.line((box[0] + r * U, box[1] + 1.5 * U, box[2] - r * U, box[1] + 1.5 * U), fill=(255, 255, 255, 26), width=max(1, int(U)))
    ax, ay, ar = box[0] + 34 * U + 54 * U, box[1] + h * U / 2, 54 * U
    if b.get('logo') and os.path.exists(b['logo']):
        lg = Image.open(b['logo']).convert('RGBA').resize((int(2 * ar), int(2 * ar)), Image.LANCZOS)
        mk = Image.new('L', lg.size, 0); ImageDraw.Draw(mk).ellipse((0, 0, lg.size[0] - 1, lg.size[1] - 1), fill=255)
        im.paste(lg, (int(ax - ar), int(ay - ar)), mk)
        d.ellipse((ax - ar, ay - ar, ax + ar, ay + ar), outline=(255, 255, 255, 40), width=max(1, int(1.5 * U)))
    else:
        d.ellipse((ax - ar, ay - ar, ax + ar, ay + ar), fill=(44, 45, 49, 255))
    tx = ax + ar + 28 * U
    if b.get('label'):
        lf = vfont('GeistMono-VF.ttf', 18, 500)
        tracked(d, (tx, box[1] + 40 * U), b['label'].upper(), lf, C.TEXT_MUTED + (255,), 0.14)
    return im, box, tx


def cta_state(b, t):
    dur = b['t1'] - b['t0']
    land = min(1.0, max(0.0, t / 0.5)); out = min(1.0, max(0.0, (dur - t) / 0.35))
    if land <= 0 or out <= 0: return None
    url = b['url']; cps = b.get('cps', 12.0); t0 = b.get('type_at', 0.6)
    n = int(max(0, min(len(url), (t - t0) * cps + 1e-6))) if t >= t0 else 0
    press = t0 + len(url) / cps + 0.45; typed_end = t0 + len(url) / cps
    blink = True if t < typed_end else int((t - typed_end) * 2.2) % 2 == 0
    caret = t < press + 0.12 and blink
    pp = (t - press) / 0.24
    sc = float(1 - 0.08 * np.sin(np.pi * pp)) if 0 <= pp <= 1 else 1
    col = C.AZURE_INK if 0 <= pp <= 1 else C.AZURE
    return (land, out, n, caret, sc, col)


def cta_draw(b, state, cache):
    if 'st' not in cache: cache['st'] = cta_static(b)
    base, box, tx = cache['st']
    land, out, n, caret, sc, col = state
    e = M.ease('power3.out')(land)
    im = base.copy(); d = ImageDraw.Draw(im)
    url = b['url']
    if 'fb' not in cache:                   # the whole URL must fit left of the button: shrink long URLs (never under 30)
        avail = (box[2] - (40 + 160 + 28) * U if b.get('button') else box[2] - 40 * U) - tx
        size = 44
        while size > 30 and vfont('Figtree-VF.ttf', size, 600).getlength(url) > avail: size -= 1
        cache['fb'] = vfont('Figtree-VF.ttf', size, 600)
    fb = cache['fb']
    ty = box[1] + (104 if b.get('label') else 88) * U
    d.text((tx, ty), url[:n], font=fb, fill=(255, 255, 255, 255), anchor='lm')
    if caret:
        cw = fb.getlength(url[:n])
        d.rounded_rectangle((tx + cw + 5 * U, ty - 26 * U, tx + cw + 9 * U, ty + 26 * U), int(2 * U), fill=C.AZURE + (255,))
    if b.get('button'):
        bxc, byc = box[2] - (40 + 80) * U, box[1] + CTA_BOX[3] * U / 2
        hw, hh = 80 * U * sc, 38 * U * sc
        glow = Image.new('L', im.size, 0); ImageDraw.Draw(glow).rounded_rectangle((bxc - hw, byc - hh, bxc + hw, byc + hh), int(hh), fill=255)
        glow = glow.filter(ImageFilter.GaussianBlur(16 * U))
        gl = Image.new('RGBA', im.size, C.AZURE + (0,)); gl.putalpha(glow.point(lambda v: int(v * 0.55)))
        im = Image.alpha_composite(im, gl); d = ImageDraw.Draw(im)
        d.rounded_rectangle((bxc - hw, byc - hh, bxc + hw, byc + hh), int(hh), fill=col + (255,))
        d.text((bxc, byc), b['button'], font=vfont('Figtree-VF.ttf', 32 * sc, 600), fill=(255, 255, 255, 255), anchor='mm')
    canvas = np.zeros((C.TH, C.TW, 4), np.float32)
    x, y, w, h = CTA_BOX
    cx, cy = (x + w / 2) * U, (y + h / 2 + 40 * (1 - e) + 24 * (1 - out)) * U
    place(canvas, im, cx, cy, 0.94 + 0.06 * e, min(1.0, land * 2.2) * out)
    return canvas


def cta_events(b):
    url = b['url']; cps = b.get('cps', 12.0); t0 = b.get('type_at', 0.6)
    ev = [dict(t=b['t0'] + 0.06, type='pop')]
    ev += [dict(t=b['t0'] + t0 + k / cps, type='key') for k in range(len(url))]
    if b.get('button'): ev.append(dict(t=b['t0'] + t0 + len(url) / cps + 0.45, type='click'))
    return ev


KINDS = {'words': (words_state, words_draw), 'cta': (cta_state, cta_draw)}


class Frames:
    """frames by state: the drawing (an RGBA float canvas) is made once per distinct state and kept as its uint8 box;
    each output frame is the persistent transparent frame with that box written in (what np.clip(canvas + 0.5) gave)"""

    def __init__(self, b):
        self.b = b; self.state_fn, self.draw_fn = KINDS[b['kind']]; self.cache = {}; self.boxes = {}
        self.frame = np.zeros((C.TH, C.TW, 4), np.uint8); self.last = None

    def box(self, state):
        if state not in self.boxes:
            canvas = self.draw_fn(self.b, state, self.cache)
            ys, xs = np.where(canvas[..., 3] > 0)
            if len(ys):
                y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
                self.boxes[state] = ((y0, y1, x0, x1), np.clip(canvas[y0:y1, x0:x1] + 0.5, 0, 255).astype(np.uint8))
            else:
                self.boxes[state] = None
        return self.boxes[state]

    def at(self, t):
        """the full RGBA uint8 frame for beat-relative time t (a view of the persistent buffer)"""
        state = self.state_fn(self.b, t)
        box = None if state is None else self.box(state)
        if self.last is not None:                                 # clear what the previous frame drew
            y0, y1, x0, x1 = self.last; self.frame[y0:y1, x0:x1] = 0
        if box is None: self.last = None; return self.frame
        (y0, y1, x0, x1), px = box
        self.frame[y0:y1, x0:x1] = px; self.last = (y0, y1, x0, x1)
        return self.frame


def render(bid, preview=None):
    b = M.beat(bid)
    f0, f1 = M.frames_of(b['t0'], b['t1'])
    os.makedirs(C.MEDIA, exist_ok=True); os.makedirs('preview', exist_ok=True); os.makedirs('events', exist_ok=True)
    ev = cta_events(b) if b['kind'] == 'cta' else words_events(b) if b['kind'] == 'words' else []
    json.dump(ev, open(f'events/{bid}.json', 'w'), indent=1)
    fr = Frames(b)
    if preview is not None:
        for t in preview:
            f = fr.at(t).astype(np.float32)
            # preview on a mid-grey checker so the alpha is visible
            bg = np.full((C.TH, C.TW, 3), 90, np.float32)
            a = f[..., 3:4] / 255
            Image.fromarray((bg * (1 - a) + f[..., :3] * a).astype(np.uint8)).save(f'preview/{bid}_{t:06.2f}.png')
        print(f'{bid}: previews in preview/{bid}_*.png'); return
    out = os.path.join(C.MEDIA, f'{bid}{TAG}.mov')
    enc = M.prores4444(out, C.TW, C.TH)
    for n in range(f1 - f0):
        enc.stdin.write(fr.at(n / C.FPS).tobytes())
    enc.stdin.close(); enc.wait()
    print(f'{bid}: {f1 - f0} frames ({len(fr.boxes)} distinct drawings) -> {out} | {len(ev)} sfx events', flush=True)


def run_parallel(ids, jobs):
    import subprocess, time
    keep = [a for a in sys.argv[1:] if a not in ids and a != '--jobs' and not a.isdigit()]
    procs, pending, failed = [], list(ids), []
    while pending or procs:
        while pending and len(procs) < jobs:
            bid = pending.pop(0); procs.append((bid, subprocess.Popen([sys.executable, __file__, bid] + keep)))
        time.sleep(0.5)
        for item in procs[:]:
            if item[1].poll() is not None:
                procs.remove(item)
                if item[1].returncode: failed.append(item[0]); print(f'FAILED {item[0]} (exit {item[1].returncode})')
    return failed


if __name__ == '__main__':
    argv = sys.argv[1:]
    prev = None; jobs = 3
    if '--tag' in argv: k = argv.index('--tag'); argv = argv[:k] + argv[k + 2:]
    if '--jobs' in argv: k = argv.index('--jobs'); jobs = int(argv[k + 1]); argv = argv[:k] + argv[k + 2:]
    if '--preview' in argv:
        k = argv.index('--preview'); prev = [float(x) for x in argv[k + 1].split(',')]; argv = argv[:k] + argv[k + 2:]
    ids = [a for a in argv if not a.startswith('--')]
    if len(ids) > 1 and jobs > 1 and prev is None:
        sys.exit(1 if run_parallel(ids, jobs) else 0)
    for bid in ids:
        render(bid, prev)
