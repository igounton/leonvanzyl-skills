"""Generate one HyperFrames composition per graphic run (split / full-visual) from compact configs.
Each page = shared engine.js + a CFG object. Times are run-relative seconds; W(...) looks up a word start."""
import json, os, re
import os as _os
_os.chdir(_os.path.dirname(_os.path.abspath(__file__))+'/..')
C = json.load(open('cut.json', encoding='utf-8'))
import glob as _glob
D = {}   # asset_dims.json plus one asset_dims_<tag>.json per graphics subagent (so parallel asset preps never race)
for _f in sorted(_glob.glob('gfx/asset_dims*.json')): D.update(json.load(open(_f, encoding='utf-8')))
OUT = 'gfx'
SFX = {}  # run id -> list of events (run-relative)
THUMBS = {}  # run id -> thumbnail candidates (run-relative): [a, b] = a window where the hero is landed and the camera at rest, or a time

def words(sk, ri):
    r = C[sk]['runs'][ri]
    return r, [dict(w=w['w'], t=round(w['s'] - r['T0'], 3)) for w in C[sk]['words'] if r['T0'] - 0.06 <= w['s'] < r['T1'] - 0.03]

def W(ws, text, n=1):
    k = 0
    for w in ws:
        if re.sub(r'[^a-z0-9$.]', '', w['w'].lower()) == text.lower():
            k += 1
            if k == n: return w['t']
    raise KeyError(text)

CSS = """
@font-face{font-family:Figtree;src:url(assets/Figtree-VF.ttf);font-weight:300 900}
@font-face{font-family:'Geist Mono';src:url(assets/GeistMono-VF.ttf);font-weight:100 900}
@font-face{font-family:Poppins;src:url(assets/Poppins-Regular.ttf);font-weight:400}
@font-face{font-family:Poppins;src:url(assets/Poppins-Medium.ttf);font-weight:500}
@font-face{font-family:Poppins;src:url(assets/Poppins-SemiBold.ttf);font-weight:600}
@font-face{font-family:Poppins;src:url(assets/Poppins-Bold.ttf);font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
:root{--stage-950:#0B0C0E;--stage-900:#111214;--stage-800:#18191C;--stage-700:#212226;--stage-600:#2C2D31;
--hairline:rgba(255,255,255,.09);--hairline-strong:rgba(255,255,255,.16);--text:#FFFFFF;--text-secondary:#A3A6AD;--text-muted:#7E818A;
--azure:#2F95FF;--ember:#FF8A5B;--iris:#9C7CFF;--mint:#4FD6A0;--azure-ink:#1560D0;--ember-ink:#B8461A;--iris-ink:#5B3FD1;--mint-ink:#0F7A52;
--azure-wash:#E8F2FF;--ember-wash:#FFEFE7;--iris-wash:#F0EBFF;--mint-wash:#E3F8EF;--paper:#FFFFFF;--paper-2:#F3F4F6;--paper-line:#ECEDF0;
--ink:#111214;--ink-2:#5F636B;--bar-rest:#5A5D64;--code-text:#E6E7EA;--code-keyword:#7DB8FF;--code-string:#9BE3B9;--code-number:#C7A9FF;
--code-comment:#6E717A;--accent:var(--azure);--accent-ink:var(--azure-ink);--accent-wash:var(--azure-wash)}
#root.acc-ember{--accent:var(--ember);--accent-ink:var(--ember-ink);--accent-wash:var(--ember-wash)}
html,body{width:1080px;height:1920px;overflow:hidden;background:#111214}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Figtree,sans-serif;color:#fff;font-variant-numeric:tabular-nums}
#ground{position:absolute;inset:0;background:radial-gradient(ellipse 90% 40% at 50% -6%,rgba(255,255,255,.10) 0%,rgba(255,255,255,0) 70%),
 linear-gradient(180deg,#18191C 0%,#111214 52%,#0B0C0E 100%)}
.beam{position:absolute;top:-300px;filter:blur(46px);background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,0))}
#beam-a{left:200px;width:200px;height:1500px;transform:rotate(14deg)}#beam-b{left:700px;width:180px;height:1400px;transform:rotate(-12deg);opacity:.8}
#wave{position:absolute;left:0;top:0;width:1080px;height:1920px}
#vignette{position:absolute;inset:0;background:radial-gradient(140% 100% at 50% 30%,rgba(0,0,0,0) 55%,rgba(0,0,0,.5) 100%)}
#root.paper #ground{background:radial-gradient(ellipse 120% 90% at 50% 36%,#FFFFFF 0%,#FAFAF8 45%,#F3F3F0 100%)}
#root.paper{font-family:Poppins,sans-serif;color:#111}#root.paper .beam,#root.paper #wave,#root.paper #vignette{display:none}
#viewport{position:absolute;inset:0;z-index:2}
#world{position:absolute;left:0;top:0;width:10px;height:10px;transform-origin:0 0}
.card{position:absolute;transform-origin:50% 50%}
.card img{display:block}
.inner{position:absolute;inset:0}
.bd{position:absolute;left:0;top:0;transform-origin:0 0;z-index:0}
#bd-wash{position:absolute;inset:0;background:#111214;opacity:0;z-index:1}#root.paper #bd-wash{background:#fff}
video.fg{position:absolute;left:0;top:0;transform-origin:0 0;z-index:3}
.caret{display:inline-block;width:4px;height:1.05em;background:var(--accent);vertical-align:-0.15em;margin-left:3px;border-radius:2px}
/* type, from the design system: Figtree 500/600 (display -0.035em, headline -0.03em, title -0.025em), Geist Mono labels.
   Shorts sizes: nothing under 30 px. */
.display{font:600 128px/1 Figtree;letter-spacing:-.035em}.h1{font:600 96px/1.02 Figtree;letter-spacing:-.03em}
.h2{font:600 54px/1.1 Figtree;letter-spacing:-.025em}.sub{font:500 46px/1.15 Figtree;letter-spacing:-.01em;color:var(--accent)}
.body{font:400 32px/1.4 Figtree;color:var(--text-secondary)}.caption{font:400 30px/1.45 Figtree;color:var(--text-muted)}
.label{font:500 30px/1.2 'Geist Mono';letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted)}
.label.accent{color:var(--accent)}.label.white{color:#fff}.accent{color:var(--accent)}.secondary{color:var(--text-secondary)}.muted{color:var(--text-muted)}
.mono{font:500 32px/1.55 'Geist Mono';color:var(--code-text)}.code-k{color:var(--code-keyword)}.code-s{color:var(--code-string)}.code-n{color:var(--code-number)}.code-c{color:var(--code-comment)}
.ink{color:var(--ink)}.ink2{color:var(--ink-2)}
.pill{display:inline-block;font:500 30px/1.2 'Geist Mono';letter-spacing:.08em;text-transform:uppercase;padding:8px 18px;border-radius:999px;background:var(--accent-wash);color:var(--accent-ink)}
.pill.mint{background:var(--mint-wash);color:var(--mint-ink)}.pill.ember{background:var(--ember-wash);color:var(--ember-ink)}.pill.neutral{background:var(--paper-2);color:var(--ink-2)}
.hair{height:1px;background:var(--hairline)}
/* highlight band on a captured page: under a mix-blend-mode:multiply screenshot (light pages), an azure wash */
.band{background:#CFE4FF;transform-origin:0 50%;border-radius:8px;transform:scaleX(0)}
/* glossy icon tiles (IconTile): .tile.azure|iris|ember|mint, size by width/height, radius 28.5% */
.tile{position:relative;display:flex;align-items:center;justify-content:center;border-radius:28.5%}
.tile.azure{background:linear-gradient(155deg,#8FCBFF 0%,#3B98FF 45%,#1B63E6 100%);box-shadow:inset 0 3px 2px rgba(255,255,255,.55),inset 0 -12px 20px rgba(6,26,84,.45),0 26px 50px -14px rgba(47,149,255,.7)}
.tile.iris{background:linear-gradient(155deg,#D6C8FF 0%,#A385FF 45%,#6C46EC 100%);box-shadow:inset 0 3px 2px rgba(255,255,255,.6),inset 0 -12px 20px rgba(40,14,120,.45),0 26px 50px -14px rgba(156,124,255,.7)}
.tile.ember{background:linear-gradient(155deg,#FFCBB3 0%,#FF9063 45%,#E5561F 100%);box-shadow:inset 0 3px 2px rgba(255,255,255,.6),inset 0 -12px 20px rgba(110,30,0,.4),0 26px 50px -14px rgba(255,138,91,.65)}
.tile.mint{background:linear-gradient(155deg,#B8F4DA 0%,#5AD9A6 45%,#1CA271 100%);box-shadow:inset 0 3px 2px rgba(255,255,255,.6),inset 0 -12px 20px rgba(0,70,45,.4),0 26px 50px -14px rgba(79,214,160,.6)}
.tile::before{content:'';position:absolute;left:10%;right:10%;top:6%;height:44%;border-radius:40% 40% 60% 60%/50% 50% 70% 70%;background:linear-gradient(180deg,rgba(255,255,255,.45),rgba(255,255,255,0))}
.tile svg{position:relative;filter:drop-shadow(0 2px 3px rgba(0,0,0,.3))}
#root.paper .h1,#root.paper .h2{font-family:Poppins;font-weight:700}#root.paper .caret{background:#D97757}#root.paper .band{background:#FBEEE8}
"""

def still(rid, cfg, marks, pad=0.05):
    """thumbnail marks clipped to where nothing moves: camera moves (glides excepted), focus changes, inner-camera moves,
    landings, exits and reveals. A window keeps its longest still stretch; a time moves to the end of the move it falls in."""
    busy = []
    for m in cfg.get('moves', []):
        if m.get('kind') == 'glide': continue
        busy.append((m['t'], m['t'] + (m.get('out', 0.45) + m.get('in', 0.6) if m.get('kind') == 'whip' else m['dur'])))
    busy += [(h['t'], h['t'] + 0.5) for h in cfg.get('heroes', []) if h['t'] > 0]
    busy += [(r['t'], r['t'] + r.get('dur', 0.5)) for r in cfg.get('reveals', [])]
    for c in cfg.get('cards', []):
        busy += [(k['t'], k['t'] + k.get('dur', 0.55)) for k in c.get('inner') or []]
        for key, d in (('land', 0.55), ('exit', 0.35)):
            if c.get(key): busy.append((c[key]['t'], c[key]['t'] + c[key].get('dur', d)))
    busy = sorted((a - pad, b + pad) for a, b in busy)
    out = []
    for m in marks:
        if isinstance(m, (list, tuple)):
            pieces, a = [], m[0]
            for b0, b1 in busy:
                if b1 <= a or b0 >= m[1]: continue
                if b0 > a: pieces.append((a, b0))
                a = max(a, b1)
            if a < m[1]: pieces.append((a, m[1]))
            best = max(pieces, key=lambda p: p[1] - p[0], default=None)
            if best and best[1] - best[0] >= 1 / 60: out.append([round(best[0], 3), round(best[1], 3)])
            else: print(f'{rid}: thumb {m} is all movement; dropped')
        else:
            t = m
            for b0, b1 in busy:
                if b0 < t < b1: t = b1
            if t < cfg['dur']: out.append(round(t, 3))
            else: print(f'{rid}: thumb {m} is all movement; dropped')
    return out

def page(rid, cfg, extra_html='', extra_css='', videos=(), backdrop=None, extra_js=''):
    dur = cfg['dur']
    THUMBS[rid] = still(rid, cfg, cfg.pop('thumb', []))
    split_mask = ''
    if cfg['mode'] == 'split':
        split_mask = '#viewport{-webkit-mask-image:linear-gradient(to bottom,#000 0,#000 900px,transparent 1060px);mask-image:linear-gradient(to bottom,#000 0,#000 900px,transparent 1060px)}'
    vid_html = ''
    filters = ['<filter id="mb-world" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur id="mbg-world" stdDeviation="0 0"/></filter>']
    for c in cfg['cards']:
        if c.get('inner') is not None or c.get('video'):
            filters.append(f'<filter id="mb-{c["id"]}" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur id="mbg-{c["id"]}" stdDeviation="0 0"/></filter>')
    for i, (cid, src, fw, fh) in enumerate(videos):
        vid_html += f'<video id="v-{cid}" data-card="{cid}" class="clip fg" src="{src}" data-start="0" data-duration="{dur}" data-track-index="{2+i}" muted playsinline style="width:{fw}px;height:{fh}px"></video>\n'
    bd_html = ''
    if backdrop:
        kind, src, fw, fh = backdrop
        if kind == 'video':
            bd_html = f'<video id="v-bd" data-backdrop="1" class="clip bd" src="{src}" data-start="0" data-duration="{dur}" data-track-index="1" muted playsinline style="width:{fw}px;height:{fh}px;opacity:0"></video>'
        else:
            bd_html = f'<img id="bd-img" class="bd" src="{src}" style="width:{fw}px;height:{fh}px;opacity:0">'
        bd_html += '<div id="bd-wash"></div>'
    html = f"""<!doctype html>
<html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="gsap.min.js"></script>
<style>{CSS}{split_mask}{extra_css}</style></head>
<body>
<div id="root" class="{'paper' if cfg.get('theme') == 'paper' else 'stage'}{' acc-' + cfg['accent'] if cfg.get('accent') and cfg.get('accent') != 'azure' else ''}" data-composition-id="{rid}" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
<div id="ground"></div><div class="beam" id="beam-a"></div><div class="beam" id="beam-b"></div><canvas id="wave" width="1080" height="1920"></canvas><div id="vignette"></div>
{bd_html}
<div id="viewport"><div id="world"></div></div>
{vid_html}
{extra_html}
<svg width="0" height="0" style="position:absolute">{''.join(filters)}</svg>
</div>
<script>window.CFG={json.dumps(cfg)};</script>
<script>{extra_js}</script>
<script src="engine.js"></script>
</body></html>"""
    open(f'{OUT}/{rid}.html', 'w', encoding='utf8').write(html)
    SFX[rid] = cfg.get('sfx', [])

def capture_card(cid, fw, fh, x=540, y=720, inner0=None, inner=(), backdrop=True, land=None, **kw):
    c = dict(id=cid, kind='capture', x=x, y=y, w=1032, h=1040, fw=fw, fh=fh, inner=list(inner), backdrop={'tIn': -1} if backdrop is True else backdrop, bg='#fff', **kw)
    if inner0: c['inner0'] = inner0
    if land: c['land'] = land
    return c

LOGO_HTML = '<img src="assets/claude-logo.svg" style="width:100%;height:100%;display:block">'


def logo_html(src):
    return f'<img src="{src}" style="width:100%;height:100%;object-fit:contain;display:block">'


# ---- the design system's glossy icon tiles (IconTile) and their glyphs (white, on a 24-unit grid)
GLYPHS = {
    'code': dict(stroke='M8.5 7.5 4 12l4.5 4.5M15.5 7.5 20 12l-4.5 4.5M13.2 5.5l-2.4 13'),
    'arrow': dict(stroke='M5 12h13M13 6.5l5.5 5.5-5.5 5.5'),
    'check': dict(stroke='M5 12.5l4.5 4.5L19 7.5'),
    'shield': dict(stroke='M12 3.2 19 6v5.6c0 4.3-2.9 7.9-7 9.2-4.1-1.3-7-4.9-7-9.2V6z', fill='M12 8.2l1 2.6 2.6 1-2.6 1-1 2.6-1-2.6-2.6-1 2.6-1z', width=2.2),
    'sparkle': dict(fill='M11 4l1.9 5.1L18 11l-5.1 1.9L11 18l-1.9-5.1L4 11l5.1-1.9zM18.5 14.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z'),
    'bolt': dict(fill='M13.5 2.5 5 13.5h6l-1.5 8 9-11.5h-6z'),
    'bars': dict(fill='M6.6 5.5h10.8a1.6 1.6 0 0 1 0 3.2H6.6a1.6 1.6 0 0 1 0-3.2zM6.6 10.4h6.3a1.6 1.6 0 0 1 0 3.2H6.6a1.6 1.6 0 0 1 0-3.2zM6.6 15.3h2.3a1.6 1.6 0 0 1 0 3.2H6.6a1.6 1.6 0 0 1 0-3.2z'),
    'eyes': dict(fill='M8.4 7a2 2 0 0 1 2 2v6a2 2 0 0 1-4 0V9a2 2 0 0 1 2-2zM15.6 7a2 2 0 0 1 2 2v6a2 2 0 0 1-4 0V9a2 2 0 0 1 2-2z'),
}


def tile_html(color='azure', glyph='code', size=140, tilt=-8, svg=None):
    """a glossy 3D icon tile (Leon YouTube design system): color azure|iris|ember|mint, glyph from GLYPHS, or your own
    <svg> markup for the glyph (white). Use it inside a card's html or as a 'plain' card's html."""
    g = GLYPHS.get(glyph, GLYPHS['code']); icon = round(size * 0.5)
    paths = ''
    if g.get('stroke'): paths += f'<path d="{g["stroke"]}" fill="none" stroke="#fff" stroke-width="{g.get("width", 2.6)}" stroke-linecap="round" stroke-linejoin="round"/>'
    if g.get('fill'): paths += f'<path d="{g["fill"]}" fill="#fff"/>'
    glyph_svg = svg or f'<svg width="{icon}" height="{icon}" viewBox="0 0 24 24">{paths}</svg>'
    return f'<div class="tile {color}" style="width:{size}px;height:{size}px;transform:rotate({tilt}deg)">{glyph_svg}</div>'


