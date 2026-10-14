# Graphics agent B: Level 2 + Level 3 beats of the "Harness engineering" pro edit, in Leon's "Leon YouTube" design system
# (graphite stage, glass panels for diagrams, white window/paper for real UI, Figtree + Geist Mono, azure accent, ember
# for limits/waiting, mint for passes, glossy icon tiles). The white-world version is kept in scripts/old_gfx_b_white.py.
# g13 g14 r04 g15 g16 g17 g18 g19 g20 g21 r05 r06 - build with `python scripts/build_gfx.py b`.
# Every beat is one page(); custom per-frame UI lives in a CFG_RENDER (pure function of t). Timings, cues, camera moves
# and SFX are unchanged from the approved white-world edit.
from build_gfx_common import *
import math

# ------------------------------------------------------------------------------------------------ shared look
AZ, EM, MI, IR = '#2F95FF', '#FF8A5B', '#4FD6A0', '#9C7CFF'
TS, TM = '#A3A6AD', '#7E818A'                      # text-secondary, text-muted (on the stage)
INK, INK2 = '#111214', '#5F636B'                   # text on paper

LINE = {  # 24-unit line glyphs (white strokes, round caps) for icons outside tiles
    'lock': '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8.2 10.5V8a3.8 3.8 0 017.6 0v2.5"/>',
    'user': '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.8 20c1.2-3.6 4-5.4 7.2-5.4s6 1.8 7.2 5.4"/>',
    'sliders': '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2.2"/><circle cx="9" cy="17" r="2.2"/>',
    'plug': '<path d="M9 3v5M15 3v5M6.5 8h11v3a5.5 5.5 0 01-11 0zM12 16.5V21"/>',
    'cube': '<path d="M12 2.8l8 4.4v9.6l-8 4.4-8-4.4V7.2z"/><path d="M4 7.2l8 4.4 8-4.4M12 11.6v9.6"/>',
    'robot': '<rect x="4" y="7.5" width="16" height="11.5" rx="4"/><path d="M12 7.5V4"/><circle cx="12" cy="3.2" r="1.1"/><path d="M9.3 12v2.4M14.7 12v2.4"/>',
    'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'pause': '<path d="M9 6.5v11M15 6.5v11"/>',
}


def line_ico(name, size, color='#fff', width=2.0, style=''):
    return (f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;flex:none;{style}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{LINE[name]}</svg>')


def tile_svg(name, size, width=2.4):
    """a white line glyph sized for a tile_html of `size`"""
    ic = round(size * 0.5)
    return (f'<svg width="{ic}" height="{ic}" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round">{LINE[name]}</svg>')


def tile(color, glyph, size, tilt=-8, svg=None):
    return tile_html(color, glyph, size, tilt, svg=svg)


def robot_tile(size, tilt=-8):
    """Leon's Orchestrate tile: the mint tile with two eyes and an antenna ball on top"""
    ah = round(size * 0.2)
    return (f'<div style="position:relative;width:{size}px;height:{size}px;flex:none;transform:rotate({tilt}deg)">'
            f'<div class="abs" style="left:{size / 2 - 2.5:.1f}px;top:{-ah}px;width:5px;height:{ah + 4}px;border-radius:3px;background:#5AD9A6"></div>'
            f'<div class="abs" style="left:{size / 2 - size * 0.075:.1f}px;top:{-ah - size * 0.12:.1f}px;width:{size * 0.15:.1f}px;height:{size * 0.15:.1f}px;'
            f'border-radius:50%;background:linear-gradient(155deg,#C4F6DF,#4FD6A0);box-shadow:0 0 12px rgba(79,214,160,.6)"></div>'
            f'{tile_html("mint", "eyes", size, 0)}</div>')


def mint_check(s=34, style=''):
    return (f'<div style="width:{s}px;height:{s}px;border-radius:50%;background:{MI};flex:none;display:flex;align-items:center;justify-content:center;'
            f'box-shadow:0 0 16px rgba(79,214,160,.45);{style}">{line_ico("check", round(s * 0.62), "#0B2A1D", 3)}</div>')


def tog(tid, on=False):
    return (f'<div class="tog" id="{tid}" style="background:{AZ if on else "rgb(62,64,70)"}">'
            f'<div class="kn" style="transform:translateX({28 if on else 0}px)"></div></div>')


def img(src, w=None, h=None, style=''):
    wh = (f'width:{w}px;' if w else '') + (f'height:{h}px;' if h else '')
    return f'<img src="{src}" style="{wh}display:block;object-fit:contain;{style}">'


def pill(text, tone='azure', size=24, pid='', style=''):
    idp = f'id="{pid}" ' if pid else ''
    return f'<div {idp}class="pl {tone}" style="font-size:{size}px;{style}">{text}</div>'


def avatar(ini, col, s=72):
    grad = {'azure': '#8FCBFF 0%,#3B98FF 45%,#1B63E6 100%', 'ember': '#FFCBB3 0%,#FF9063 45%,#E5561F 100%',
            'mint': '#B8F4DA 0%,#5AD9A6 45%,#1CA271 100%', 'iris': '#D6C8FF 0%,#A385FF 45%,#6C46EC 100%'}[col]
    return (f'<div style="width:{s}px;height:{s}px;border-radius:50%;flex:none;background:linear-gradient(155deg,{grad});display:flex;align-items:center;'
            f'justify-content:center;font:600 {round(s * 0.44)}px/1 Figtree;color:#fff;box-shadow:inset 0 2px 2px rgba(255,255,255,.45),inset 0 -8px 14px rgba(0,0,0,.25)">{ini}</div>')


GLASS = ('background:rgba(24,25,28,.62);backdrop-filter:blur(24px) saturate(140%);-webkit-backdrop-filter:blur(24px) saturate(140%);'
         'border:1px solid rgba(255,255,255,.09);box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 50px 120px -40px rgba(0,0,0,.85);color:#fff;')
PAPER = 'background:#fff;box-shadow:0 34px 80px -24px rgba(0,0,0,.8);color:#111214;'

BCSS = """
.fx{display:flex;align-items:center}
.abs{position:absolute}
.gm{font-family:'Geist Mono',monospace;font-weight:500}
.cell{background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.08);border-radius:16px}
.chipd{font:500 28px/44px 'Geist Mono';height:46px;padding:0 14px;border-radius:12px;background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.10);color:#E6E7EA;white-space:nowrap}
.pl{display:inline-block;font:500 24px/1 'Geist Mono';letter-spacing:.04em;padding:9px 16px;border-radius:999px;white-space:nowrap}
.pl.azure{background:#E8F2FF;color:#1560D0}.pl.mint{background:#E3F8EF;color:#0F7A52}.pl.ember{background:#FFEFE7;color:#B8461A}
.pl.iris{background:#F0EBFF;color:#5B3FD1}.pl.neutral{background:#F3F4F6;color:#5F636B}
.tog{position:relative;width:68px;height:40px;border-radius:20px;flex:none}
.tog .kn{position:absolute;left:4px;top:4px;width:32px;height:32px;border-radius:16px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.35)}
.spin{border-radius:50%;border:4px solid rgba(47,149,255,.25);border-top-color:#2F95FF}
"""

BJS = r"""
window.B = (function () {
  const E = (n) => (n === 'linear' ? (p) => p : gsap.parseEase(n));
  const cl = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, p) => a + (b - a) * p;
  const P = (t, t0, d, e) => { const x = cl((t - t0) / (d || 1e-6), 0, 1); return e ? E(e)(x) : x; };
  const C = {};
  const $ = (id) => { if (!C[id]) C[id] = document.getElementById(id); return C[id]; };
  const mixc = (c1, c2, p) => 'rgb(' + c1.map((v, i) => Math.round(lerp(v, c2[i], p))).join(',') + ')';
  // a toggle on the stage: off = graphite, on = azure with a soft glow
  function tog(id, v) { const el = $(id); if (!el) return; el.style.background = mixc([62, 64, 70], [47, 149, 255], v);
    el.style.boxShadow = '0 0 ' + (20 * v).toFixed(1) + 'px rgba(47,149,255,' + (0.5 * v).toFixed(3) + ')';
    el.querySelector('.kn').style.transform = 'translateX(' + (28 * v).toFixed(2) + 'px)'; }
  // quadratic bezier point
  function qb(a, c, b, p) { const q = 1 - p; return [q * q * a[0] + 2 * q * p * c[0] + p * p * b[0], q * q * a[1] + 2 * q * p * c[1] + p * p * b[1]]; }
  return { E, cl, lerp, P, $, mixc, tog, qb };
})();
"""


def mk(bid, cfg, html_css='', js='', **kw):
    cfg.setdefault('accent', 'azure')
    cfg.setdefault('wave', dict(level='low', k=1.0))
    page(bid, cfg, extra_css=BCSS + html_css, extra_js=BJS + js, **kw)


def sfx(*evs):
    return [dict(t=round(t, 3), type=k) for t, k in evs]


# ------------------------------------------------------------------------------------------------ g13
def g13():
    """acme-harness, an org's custom harness, as a glass admin console above its developers: wires connect on
    "control", ember shields land on "developers", policy rows stamp in on "policies", three specific tools switch on
    (azure) on "tools", deploy-to-prod and network access switch off with an ember lock on "limiting" / "capabilities"."""
    b, ws = words('g13')
    T = lambda w, n=1: W(ws, w, n)
    CX, CY, CW, CH = 784, 400, 1420, 560             # console card (world)
    cols = [(40, 460), (540, 400), (980, 400)]       # inner x, width
    ROW_Y = [200, 286, 372, 458]                     # inner y of rows

    def col_head(x, w, icon, title):
        return f'<div class="abs fx" style="left:{x}px;top:124px;width:{w}px;gap:18px">{icon}<div style="font:600 34px/1 Figtree;letter-spacing:-.02em">{title}</div></div>'

    def row(x, w, y, inner, rid='', style=''):
        idp = f'id="{rid}" ' if rid else ''
        return (f'<div {idp}class="abs fx cell" style="left:{x}px;top:{y}px;width:{w}px;height:72px;padding:0 20px;gap:14px;'
                f'font:500 30px/1 Figtree;color:#fff;transform-origin:30% 50%;{style}">{inner}</div>')

    h = [f'<div class="abs fx" style="left:0;top:0;right:0;height:100px;padding:0 40px;gap:22px">'
         f'{tile("ember", "shield", 58, -8)}<div style="font:600 40px/1 Figtree;letter-spacing:-.025em">acme-harness</div>'
         f'<div class="label" style="margin-left:auto">Admin console</div></div>'
         f'<div class="abs" style="left:0;right:0;top:100px;height:1px;background:rgba(255,255,255,.09)"></div>']
    (x1, w1), (x2, w2), (x3, w3) = cols
    h.append(col_head(x1, w1, tile('ember', 'shield', 48, -8), 'Policies'))
    h.append(col_head(x2, w2, tile('iris', 'bolt', 48, 8), 'Allowed tools'))
    h.append(col_head(x3, w3, tile('azure', '', 48, -8, svg=tile_svg('sliders', 48)), 'Capabilities'))
    for i, txt in enumerate(['Require PR review', 'No secrets in prompts']):
        h.append(f'<div id="ph{i}" class="abs" style="left:{x1}px;top:{ROW_Y[i]}px;width:{w1}px;height:72px;border-radius:16px;border:2px dashed rgba(255,255,255,.16)"></div>')
        h.append(row(x1, w1, ROW_Y[i], mint_check(34) + f'<span>{txt}</span>', rid=f'pr{i}', style='opacity:0'))
    for i, txt in enumerate(['Read files', 'Edit files', 'Run tests', 'Browse web']):
        h.append(row(x2, w2, ROW_Y[i], f'<span id="tl{i}">{txt}</span><div style="margin-left:auto">{tog(f"tt{i}")}</div>'))
    for i, txt in enumerate(['Deploy to prod', 'Network access']):
        h.append(row(x3, w3, ROW_Y[i], f'<span id="cl{i}">{txt}</span><div id="clk{i}" style="margin-left:auto;opacity:0">{line_ico("lock", 30, EM, 2.2)}</div>'
                                       f'<div>{tog(f"ct{i}", True)}</div>'))
    console = dict(id='con', kind='glass', highlight=True, x=CX, y=CY, w=CW, h=CH, html=''.join(h))

    # developers: glass cards with an avatar and their agent (the mint Orchestrate tile); an ember shield lands on each
    DY, DXS = 830, [274, 614, 954, 1294]
    people = [('S', 'Sam', 'azure'), ('P', 'Priya', 'ember'), ('J', 'Jon', 'mint'), ('M', 'Mia', 'iris')]
    cards = [console]
    for i, (ini, name, col) in enumerate(people):
        dh = (f'<div class="abs fx" style="left:26px;top:0;bottom:0;gap:22px">'
              f'<div style="position:relative;width:76px;height:76px;flex:none">{avatar(ini, col, 76)}'
              f'<div class="abs" style="right:-14px;bottom:-12px">{tile("mint", "eyes", 38, 0)}</div></div>'
              f'<div style="font:600 32px/1 Figtree;letter-spacing:-.02em">{name}</div></div>'
              f'<div id="shd{i}" class="abs" style="right:18px;top:16px;opacity:0">{tile("ember", "shield", 40, 8)}</div>')
        cards.append(dict(id=f'dev{i}', kind='glass', x=DXS[i], y=DY, w=280, h=130, html=dh))
    # wires console -> developers (dashed azure, flowing, glowing)
    wh = ''.join(f'<div id="w{i}" class="abs" style="left:{x - 1.5 - 64}px;top:0;width:3px;height:86px;transform-origin:50% 0;transform:scaleY(0);'
                 f'background:repeating-linear-gradient(to bottom,rgba(47,149,255,.85) 0 10px,transparent 10px 20px);filter:drop-shadow(0 0 5px rgba(47,149,255,.8))"></div>'
                 for i, x in enumerate(DXS))
    cards.insert(0, dict(id='wires', kind='plain', x=784, y=680 + 43, w=1440, h=86, html=wh))

    t_ctl, t_dev, t_pol = T('control'), T('developers'), T('policies')
    t_spec, t_tools, t_lim, t_cap = T('specific'), T('tools'), T('limiting'), T('capabilities')
    data = dict(tWire=t_ctl, tShield=t_dev, stamps=[t_pol, t_pol + 0.5], toolsOn=[t_tools, t_tools + 0.14, t_tools + 0.28],
                capsOff=[t_lim + 0.05, t_cap])
    sy = 440
    moves = [dict(t=0.0, dur=T('enforcing') - 0.3, kind='glide', to=dict(x=784, y=490, s=1.03)),
             dict(t=T('enforcing') - 0.25, dur=1.2, kind='push', to=dict(x=540, y=sy, s=1.25)),
             dict(t=t_spec - 0.25, dur=0.6, kind='step', to=dict(x=814, y=sy, s=1.25)),
             dict(t=t_lim - 0.25, dur=0.6, kind='step', to=dict(x=1110, y=sy, s=1.25))]
    js = r"""
window.CFG_RENDER = function (t, cam) {
  const d = CFG.data;
  for (let i = 0; i < 4; i++) {
    const p = B.P(t, d.tWire + i * 0.08, 0.55, 'power2.out'); const w = B.$('w' + i);
    w.style.transform = 'scaleY(' + p.toFixed(4) + ')'; w.style.backgroundPosition = '0 ' + (t * 34).toFixed(2) + 'px';
    const q = B.P(t, d.tShield + i * 0.07, 0.42, 'back.out(2.2)'); const s = B.$('shd' + i);
    s.style.opacity = B.cl(q * 3, 0, 1); s.style.transform = 'scale(' + B.lerp(0.4, 1, q).toFixed(4) + ')';
  }
  d.stamps.forEach((ts, i) => { const p = B.P(t, ts, 0.32, 'power3.out'); const r = B.$('pr' + i);
    r.style.opacity = B.cl(p * 2.5, 0, 1); r.style.transform = 'scale(' + B.lerp(1.28, 1, p).toFixed(4) + ')';
    B.$('ph' + i).style.opacity = 1 - B.cl(p * 3, 0, 1); });
  d.toolsOn.forEach((ts, i) => B.tog('tt' + i, B.P(t, ts, 0.26, 'power2.inOut')));
  d.capsOff.forEach((ts, i) => { const v = 1 - B.P(t, ts, 0.26, 'power2.inOut'); B.tog('ct' + i, v);
    B.$('cl' + i).style.color = B.mixc([255, 255, 255], [126, 129, 138], 1 - v);
    const lk = B.P(t, ts + 0.1, 0.3, 'back.out(2)'); const l = B.$('clk' + i);
    l.style.opacity = B.cl(lk * 2, 0, 1); l.style.transform = 'scale(' + B.lerp(0.5, 1, lk).toFixed(3) + ')'; });
};
"""
    cfg = dict(id='g13', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=500, s=1.0), cards=cards, moves=moves, pushRef=1.03,
               heroes=[dict(t=0, id='none'), dict(t=moves[1]['t'] + 0.1, id='con')], data=data, wave=dict(level='low', k=0.8),
               sfx=sfx((t_dev, 'pop'), (t_pol, 'pop'), (t_tools, 'click'), (t_lim + 0.05, 'click'), (t_cap, 'click')))
    mk('g13', cfg, js=js)


# ------------------------------------------------------------------------------------------------ g15
def g15():
    """The context budget, honest proportions at 32 world px per 1K tokens. Claude Code (paper chip) injects its payload
    block by block (system prompt azure, memory files ember, tool definitions iris); a local model (Ollama, qwen3) with a
    tiny window and a consumer GPU on glass; then a glass panel with a 32K and a 64K window. Claude Code's ~30K drops
    into both: 94% (ember, 2K free pulsing) and 47%."""
    b, ws = words('g15')
    T = lambda w, n=1: W(ws, w, n)
    K = 32                                      # world px per 1K tokens
    X0 = 304                                    # left edge of every bar
    PY, PH = 510, 120                           # payload row
    B32, B64 = 830, 1070                        # bar rows (centre y)
    sysw, memw, toolw = 4 * K, 1 * K, 25 * K    # 4K + 1K + 25K = 30K

    t_sys, t_mem, t_tools = T('system'), T('memory'), T('tools')
    t_small, t_tiny, t_cons = T('small'), T('tiny'), T('consumergrade')
    t_32, t_64 = T('thirtytwo'), T('sixtyfour')
    t_30, t_k = T('thirty'), T('thousand', 3)
    t_harness, t_ctx = T('harness', 2), T('context', 4)

    cc = dict(id='cc', kind='paper', x=784, y=255, w=580, h=160,
              html=f'<div class="abs fx" style="inset:0;justify-content:center">{img("assets/b_cc_wordmark.png", 452)}</div>')
    blk = 'position:absolute;top:0;height:{h}px;display:flex;flex-direction:column;justify-content:center;color:#fff;'
    small_txt = lambda s: f'<div class="lodS" style="font:600 30px/1.08 Figtree;letter-spacing:-.01em">{s}</div>'
    G_AZ, G_EM, G_IR = ('linear-gradient(160deg,#5DAAFF,#1B63E6)', 'linear-gradient(160deg,#FFA47F,#E5561F)', 'linear-gradient(160deg,#B69CFF,#6C46EC)')
    hi = 'box-shadow:inset 0 2px 0 rgba(255,255,255,.28),inset 0 -10px 18px rgba(0,0,0,.18);'
    pay_inner = (
        f'<div id="b_sys" style="{blk.format(h=PH)}left:0;width:{sysw}px;padding-left:14px;border-radius:22px 0 0 22px;background:{G_AZ};{hi}">{small_txt("System<br>prompt")}</div>'
        f'<div id="b_mem" style="{blk.format(h=PH)}left:{sysw}px;width:{memw}px;background:{G_EM};{hi}"></div>'
        f'<div id="b_tool" style="{blk.format(h=PH)}left:{sysw + memw}px;width:{toolw}px;padding-left:30px;border-radius:0 22px 22px 0;background:{G_IR};{hi}">'
        f'<div class="lodS" style="font:600 30px/1.1 Figtree">Tool definitions</div>'
        f'<div class="lodS gm" style="font-size:28px;line-height:1.2;opacity:.82;margin-top:8px">Bash Read Edit Write Grep Glob WebFetch …</div></div>'
        f'<div id="b_big" class="abs fx" style="left:{sysw + memw + 30}px;top:0;height:{PH}px;gap:20px;opacity:0;color:#fff">'
        f'<div style="font:600 58px/1 Figtree;letter-spacing:-.025em;white-space:nowrap">Claude Code</div>'
        f'<div id="b_30" style="font:500 52px/1 Figtree;opacity:0;white-space:nowrap">≈30K tokens</div></div>')
    mem_lbl = (f'<div id="b_meml" class="abs lodS" style="left:{sysw + memw / 2 - 120}px;top:-76px;width:240px;text-align:center;font:500 30px/1 Figtree;color:{EM}">'
               f'Memory files<div style="width:3px;height:22px;background:{EM};margin:8px auto 0;border-radius:2px"></div></div>')
    track = f'<div id="b_track" class="abs" style="left:0;top:0;width:{30 * K}px;height:{PH}px;border-radius:22px;border:2px dashed rgba(255,255,255,.18)"></div>'
    pay = dict(id='pay', kind='plain', clip=False, x=X0 + 15 * K, y=PY, w=30 * K, h=PH, html=track + pay_inner + mem_lbl)
    pay2 = dict(id='pay2', kind='plain', clip=False, x=X0 + 15 * K, y=PY, w=30 * K, h=PH,
                html=pay_inner.replace('id="b_', 'id="c_').replace('class="lodS', 'class="lodS2'))

    # local model (Ollama) + consumer GPU, on glass
    MX, GX, RY = 1720, 2250, 400
    model = dict(id='model', kind='glass', x=MX, y=RY, w=540, h=290, land=dict(t=t_small, dur=0.55), html=(
        f'<div class="abs fx" style="left:44px;top:44px;gap:30px">{img("assets/b_ollama_white.png", None, 118)}'
        f'<div><div class="gm" style="font-size:52px;font-weight:600;line-height:1">qwen3</div>'
        f'<div style="font:500 46px/1 Figtree;color:{TS};margin-top:14px">via Ollama</div></div></div>'
        f'<div id="tinyw" class="abs fx" style="left:44px;bottom:42px;gap:18px;opacity:0">'
        f'<div style="width:{6 * K}px;height:46px;border-radius:12px;background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.22)"></div>'
        f'<div style="font:600 46px/1 Figtree">context</div></div>'))
    fan = lambda i, l: (f'<div id="fan{i}" class="abs" style="left:{l}px;top:30px;width:136px;height:136px;border-radius:50%;border:7px solid #0B0C0E;'
                        'background:radial-gradient(circle,#18191C 0 17%,transparent 18%),repeating-conic-gradient(from 0deg,#5A5D64 0deg 20deg,#212226 20deg 45deg)"></div>')
    gpu = dict(id='gpu', kind='glass', x=GX, y=RY, w=440, h=290, land=dict(t=t_cons, dur=0.55), html=(
        f'<div class="abs" style="left:30px;top:26px;width:380px;height:196px;border-radius:22px;background:linear-gradient(160deg,#2C2D31,#111214);'
        f'box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 0 0 1px rgba(255,255,255,.06)">{fan(0, 26)}{fan(1, 206)}'
        f'<div class="abs" style="left:24px;right:24px;bottom:12px;height:5px;border-radius:3px;background:{AZ};box-shadow:0 0 12px rgba(47,149,255,.8)"></div></div>'
        f'<div class="abs" style="left:56px;top:222px;width:186px;height:16px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.32) 0 12px,transparent 12px 18px)"></div>'
        f'<div class="abs" style="right:34px;bottom:14px;font:600 46px/1 Figtree">8 GB</div>'))

    def bar(bid, kk, y, tl):
        w = kk * K
        ticks = ''.join(f'<div class="abs" style="left:{i * 8 * K}px;top:12px;width:2px;height:{PH - 24}px;background:rgba(255,255,255,.08)"></div>' for i in range(1, kk // 8))
        h = (f'<div class="abs" style="left:0;top:-84px;font:600 66px/1 Figtree;letter-spacing:-.025em">{kk}K</div>'
             f'<div class="abs" style="left:0;top:0;width:{w}px;height:{PH}px;border-radius:22px;background:rgba(255,255,255,.04);'
             f'box-shadow:inset 0 0 0 2px rgba(255,255,255,.12)">{ticks}'
             f'<div id="{bid}_free" class="abs" style="right:3px;top:3px;bottom:3px;width:{w - 30 * K - 6}px;border-radius:0 19px 19px 0;background:{EM};'
             f'box-shadow:0 0 30px rgba(255,138,91,.6);opacity:0"></div></div>'
             f'<div id="{bid}_pct" class="abs" style="left:{w + 28}px;top:{PH / 2 - 30}px;font:600 60px/1 Figtree;letter-spacing:-.02em;opacity:0">0%</div>')
        return dict(id=bid, kind='plain', clip=False, x=X0 + w / 2, y=y, w=w, h=PH, land=dict(t=tl, dur=0.55), html=h)

    bar32, bar64 = bar('bar32', 32, B32, t_32), bar('bar64', 64, B64, t_64)
    # the two windows sit on one glass panel (BarRows in a GlassPanel), so nothing reads on the wave's crest
    panel = dict(id='bars', kind='glass', x=X0 - 70 + 2305 / 2, y=(B32 + B64) / 2 - 57, w=2305, h=540, land=dict(t=t_32, dur=0.55),
                 html='')
    free_lbl = dict(id='freel', kind='plain', clip=False, x=X0 + 31 * K, y=B32 + PH / 2 + 50, w=200, h=60,
                    html=f'<div id="freelt" class="abs" style="left:-40px;top:0;width:280px;text-align:center;font:600 52px/1 Figtree;color:{EM};opacity:0">2K free</div>')
    t_out = t_ctx - 0.45
    for c in (cc, model, gpu): c['exit'] = dict(t=t_out, dur=0.6)
    cards = [cc, panel, bar32, bar64, model, gpu, pay2, pay, free_lbl]

    cam_a = dict(x=784, y=420, s=1.3)
    cam_b = dict(x=1975, y=405, s=1.25)
    cam_c = dict(x=1377, y=650, s=0.6)
    cam_d = dict(x=932, y=B32 + 40, s=1.0)
    moves = [dict(t=0.0, dur=t_small - 0.6, kind='glide', to=dict(x=784, y=425, s=1.34)),
             dict(t=t_small - 0.55, dur=1.1, kind='step', to=cam_b),
             dict(t=t_tiny - 0.25, dur=3.0, kind='glide', to=dict(x=1990, y=405, s=1.28)),
             dict(t=t_32 - 0.45, dur=1.3, kind='pull', to=cam_c),
             dict(t=t_64 + 0.8, dur=5.0, kind='glide', to=dict(x=1380, y=660, s=0.62)),
             dict(t=t_ctx - 0.5, dur=1.4, kind='push', to=cam_d)]
    data = dict(K=K, PH=PH, sys=t_sys, mem=t_mem, tools=t_tools, tiny=t_tiny, drop=t_30 - 0.8, drop2=t_k - 0.85,
                d1=B32 - PY, d2=B64 - PY, t30=t_30, pulse=t_harness)
    js = r"""
window.CFG_RENDER = function (t, cam) {
  const d = CFG.data;
  const blockIn = (id, t0) => { const p = B.P(t, t0, 0.55, 'power3.out'); const e = B.$(id);
    e.style.opacity = B.cl(p * 2.5, 0, 1); e.style.transform = 'translateY(' + B.lerp(-230, 0, p).toFixed(2) + 'px) scaleY(' + B.lerp(0.8, 1, p).toFixed(4) + ')'; };
  blockIn('b_sys', d.sys); blockIn('b_mem', d.mem); blockIn('b_tool', d.tools);
  const ml = B.P(t, d.mem + 0.15, 0.4, 'power2.out');
  const lod = t >= d.drop ? 0 : B.cl((cam.s - 0.7) / 0.18, 0, 1);
  document.querySelectorAll('.lodS').forEach((e) => { if (e.id !== 'b_meml') e.style.opacity = lod; });
  B.$('b_meml').style.opacity = ml * lod;
  B.$('b_big').style.opacity = 1 - lod;
  B.$('tinyw').style.opacity = B.P(t, d.tiny, 0.4, 'power2.out');
  B.$('fan0').style.transform = 'rotate(' + (t * 300).toFixed(1) + 'deg)'; B.$('fan1').style.transform = 'rotate(' + (t * 300 + 20).toFixed(1) + 'deg)';
  const p1 = B.P(t, d.drop, 0.8, 'power3.inOut'), p2 = B.P(t, d.drop2, 0.95, 'power3.inOut');
  const pay = B.$('card-pay'), pay2 = B.$('card-pay2');
  pay.style.transform = 'translateY(' + (p1 * d.d1).toFixed(2) + 'px)';
  pay2.style.transform = 'translateY(' + (p2 * d.d2).toFixed(2) + 'px)';
  pay2.style.opacity = t >= d.drop2 ? 1 : 0;
  B.$('b_track').style.opacity = 1 - B.P(t, d.drop, 0.3);
  document.querySelectorAll('.lodS2').forEach((e) => { e.style.opacity = lod; });
  B.$('c_big').style.opacity = 1 - lod;
  const t30 = B.P(t, d.t30, 0.5, 'power2.out'); B.$('b_30').style.opacity = t30; B.$('c_30').style.opacity = t30;
  const f1 = B.P(t, d.drop + 0.8, 0.7, 'power2.out'), f2 = B.P(t, d.drop2 + 0.95, 0.7, 'power2.out');
  B.$('bar32_pct').style.opacity = B.cl(f1 * 3, 0, 1); B.$('bar32_pct').textContent = Math.round(94 * f1) + '%';
  B.$('bar64_pct').style.opacity = B.cl(f2 * 3, 0, 1); B.$('bar64_pct').textContent = Math.round(47 * f2) + '%';
  B.$('bar32_pct').style.color = B.mixc([255, 255, 255], [255, 138, 91], f1);
  B.$('bar64_pct').style.color = '#A3A6AD';
  const pu = B.P(t, d.pulse, 0.5, 'power2.out');
  B.$('bar32_free').style.opacity = pu * (0.55 + 0.35 * Math.sin((t - d.pulse) * 5.2));
  B.$('freelt').style.opacity = pu;
};
"""
    cfg = dict(id='g15', dur=b['dur'], mode='fvp', cam0=cam_a, cards=cards, moves=moves, pushRef=1.5,
               heroes=[dict(t=0, id='none')], data=data, wave=dict(level='low', k=0.9),
               sfx=sfx((t_sys, 'pop'), (t_mem, 'pop'), (t_tools, 'pop'), (t_small, 'pop'), (t_cons, 'pop'),
                       (t_32, 'pop'), (t_64, 'pop'), (t_30, 'pop')))
    mk('g15', cfg, js=js)


# ------------------------------------------------------------------------------------------------ g16
def g16():
    """SMOL Coder strips a heavy harness: an azure scan marks what an open-weight model never needs; skills, MCP tools
    and sub-agents get an ember outline, are struck through and ejected on their names; the tool list trims to four
    (the keepers turn azure); the system prompt shrinks to a sliver. A glass context meter (of a 32K window, continuity
    with g15) rolls from ~30K (ember) down to SMOL's ~1.4K (azure)."""
    b, ws = words('g16')
    T = lambda w, n=1: W(ws, w, n)
    SW, SX = 820, 640                              # stack width, left (world)
    GAP = 16
    t_strip, t_never = T('strips'), T('never')
    t_mcp, t_sub, t_lim = T('mcp'), T('subagents'), T('limited')
    t_sys, t_tiny, t_opt = T('system'), T('tiny'), T('optimized')

    def chip_layout(names, maxw, x0=0, y0=0, gap=12, rowh=56):
        pos, x, y = [], x0, y0
        for n in names:
            w = round(len(n) * 16.8 + 30)
            if x + w > x0 + maxw: x, y = x0, y + rowh
            pos.append((x, y, w)); x += w + gap
        return pos
    tools = ['Bash', 'Read', 'Edit', 'Write', 'Grep', 'Glob', 'WebFetch', 'WebSearch', 'Task', 'TodoWrite', 'NotebookEdit', 'LS']
    keep = ['Read', 'Edit', 'Bash', 'Grep']
    full = chip_layout(tools, SW - 60)
    trim = dict(zip(keep, chip_layout(keep, SW - 60)))
    chips = []
    for i, (n, (x, y, w)) in enumerate(zip(tools, full)):
        x2, y2 = (trim[n][0], trim[n][1]) if n in trim else (x, y)
        chips.append(dict(i=i, x=x, y=y, x2=x2, y2=y2, keep=n in keep))
    chip_html = ''.join(f'<div id="tc{c["i"]}" class="abs chipd" style="left:{c["x"]}px;top:{c["y"]}px">{n}</div>' for c, n in zip(chips, tools))

    def ntile(name):   # a neutral glass-coloured icon square for the parts that will be cut
        return (f'<div style="width:54px;height:54px;border-radius:15px;flex:none;display:flex;align-items:center;justify-content:center;'
                f'background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12)">{line_ico(name, 30, "#E6E7EA", 1.9)}</div>')

    def block(bid, h, icon, title, body, marked=False):
        mk_ = (f'<div id="{bid}_mk" class="abs" style="left:-6px;width:{SW + 12}px;top:-6px;height:{h + 12}px;border-radius:32px;'
               f'border:2px dashed {EM};box-shadow:0 0 24px rgba(255,138,91,.35);opacity:0"></div>' if marked else '')
        return (f'<div id="{bid}" class="abs" style="left:0;top:0;width:{SW}px;height:{h}px;border-radius:28px;overflow:hidden;{GLASS}">'
                f'<div class="abs fx" style="left:28px;top:24px;gap:18px">{icon}<div style="font:600 36px/1 Figtree;letter-spacing:-.02em">{title}</div></div>'
                f'{body}<div id="{bid}_st" class="abs" style="left:20px;right:20px;top:50px;height:4px;border-radius:2px;background:{EM};'
                f'box-shadow:0 0 10px rgba(255,138,91,.7);transform-origin:0 50%;transform:scaleX(0)"></div></div>{mk_}')
    lines = ''.join(f'<div class="abs sysl" style="left:28px;top:{100 + i * 20}px;width:{w}px;height:10px;border-radius:5px;background:rgba(255,255,255,.14)"></div>'
                    for i, w in enumerate([740, 690, 720, 410]))
    mini = lambda names: ''.join(f'<div class="chipd" style="color:{TS}">{n}</div>' for n in names)
    avs = ''.join(f'<div style="margin-left:-12px;border-radius:50%;box-shadow:0 0 0 3px #18191C">{avatar("", c, 46)}</div>' for c in ['azure', 'ember', 'mint'])
    blocks = [  # id, height, html ; heights also drive the stack layout in JS
        ('bk_sys', 182, block('bk_sys', 182, tile('azure', 'code', 56, -8), 'System prompt', lines)),
        ('bk_tool', 262, block('bk_tool', 262, tile('iris', 'bolt', 56, 8), 'Tools', f'<div class="abs" style="left:30px;top:96px">{chip_html}</div>')),
        ('bk_mcp', 104, block('bk_mcp', 104, ntile('plug'), 'MCP tools', f'<div class="abs fx" style="right:28px;top:29px;gap:10px">{mini(["github", "playwright"])}</div>', True)),
        ('bk_sub', 104, block('bk_sub', 104, ntile('robot'), 'Sub-agents', f'<div class="abs fx" style="right:38px;top:29px">{avs}</div>', True)),
        ('bk_skl', 104, block('bk_skl', 104, ntile('cube'), 'Skills', f'<div class="abs fx" style="right:28px;top:29px;gap:10px">{mini(["pdf", "docx", "xlsx"])}</div>', True)),
    ]
    H0 = sum(h for _, h, _ in blocks) + GAP * (len(blocks) - 1)
    scan = (f'<div id="scan" class="abs" style="left:-30px;width:{SW + 60}px;top:0;height:4px;border-radius:2px;background:{AZ};'
            f'box-shadow:0 0 24px 6px rgba(47,149,255,.55);opacity:0"></div>')
    stack = dict(id='stack', kind='plain', clip=False, x=SX + SW / 2, y=540, w=SW, h=H0, html=''.join(h for _, _, h in blocks) + scan)
    smol = dict(id='smol', kind='glass', x=330, y=360, w=470, h=230, html=(
        f'<div class="abs" style="left:0;right:0;top:40px;display:flex;justify-content:center">{img("assets/b_smol_logo_alpha.png", 370)}</div>'
        f'<div class="abs gm" style="left:0;right:0;bottom:26px;text-align:center;font-size:28px;color:{TS}">coder · smolcoder.dev</div>'))
    meter = dict(id='meter', kind='glass', x=330, y=680, w=470, h=270, html=(
        '<div class="abs label" style="left:40px;top:40px">Context used</div>'
        f'<div id="mnum" class="abs" style="left:38px;top:86px;font:600 88px/1 Figtree;letter-spacing:-.03em;color:{EM}">≈30K</div>'
        '<div class="abs" style="left:40px;right:40px;top:204px;height:18px;border-radius:9px;background:rgba(255,255,255,.08);overflow:hidden">'
        f'<div id="mbar" style="height:100%;width:94%;border-radius:9px;background:{EM}"></div></div>'
        '<div class="abs label" style="right:40px;top:40px">of 32K</div>'))
    data = dict(H=[h for _, h, _ in blocks], ids=[i for i, _, _ in blocks], gap=GAP, H0=H0,
                scan=t_strip, mark=t_strip + 0.3,
                ej=dict(bk_skl=t_never, bk_mcp=t_mcp, bk_sub=t_sub), trim=t_lim, sys=t_sys, tiny=t_tiny, opt=t_opt,
                chips=chips, toolH2=150, sysH2=124,
                # token shares (K): system 4, tools 19, mcp 2, sub-agents 1, skills 4 -> 30 ; smol: 0.4 + 1.0
                tok=dict(bk_sys=4, bk_tool=19, bk_mcp=2, bk_sub=1, bk_skl=4), tokSys2=0.4, tokTool2=1.0)
    js = r"""
window.CFG_RENDER = function (t, cam) {
  const d = CFG.data;
  const hs = {}, out = {};
  const pTrim = B.P(t, d.trim + 0.35, 0.6, 'power3.inOut'), pSys = B.P(t, d.tiny, 0.6, 'power3.inOut');
  d.ids.forEach((id, i) => { hs[id] = d.H[i]; out[id] = 0; });
  hs.bk_tool = B.lerp(d.H[1], d.toolH2, pTrim); hs.bk_sys = B.lerp(d.H[0], d.sysH2, pSys);
  let y = 0;
  d.ids.forEach((id, k) => {
    const te = d.ej[id];
    const pe = te != null ? B.P(t, te + 0.22, 0.5, 'power3.inOut') : 0;
    const po = te != null ? B.P(t, te + 0.22, 0.45, 'power2.in') : 0;
    out[id] = po;
    const el = B.$(id);
    el.style.height = hs[id].toFixed(2) + 'px';
    el.style.top = y.toFixed(2) + 'px';
    const tr = 'translateX(' + (po * 260).toFixed(2) + 'px) rotate(' + (po * 4).toFixed(2) + 'deg) scale(' + (1 - 0.06 * po).toFixed(4) + ')';
    el.style.transform = tr; el.style.opacity = 1 - po;
    const mk = B.$(id + '_mk');
    if (mk) { mk.style.top = (y - 6).toFixed(2) + 'px'; mk.style.transform = tr;
      mk.style.opacity = (B.P(t, d.mark + 0.12 * k, 0.3) * 0.9 * (1 - B.P(t, te, 0.2))).toFixed(3); }
    if (te != null) B.$(id + '_st').style.transform = 'scaleX(' + B.P(t, te, 0.25, 'power2.out').toFixed(4) + ')';
    y += (hs[id] + d.gap) * (1 - pe);
  });
  const H = y - d.gap;
  B.$('card-stack').style.transform = 'translateY(' + ((d.H0 - H) / 2).toFixed(2) + 'px)';
  const ps = B.P(t, d.scan, 1.1, 'power1.inOut');
  const sc = B.$('scan'); sc.style.top = (ps * d.H0).toFixed(2) + 'px'; sc.style.opacity = Math.sin(Math.PI * ps).toFixed(3);
  d.chips.forEach((c) => { const e = B.$('tc' + c.i);
    if (c.keep) { e.style.left = B.lerp(c.x, c.x2, pTrim).toFixed(2) + 'px'; e.style.top = B.lerp(c.y, c.y2, pTrim).toFixed(2) + 'px';
      e.style.background = 'rgba(47,149,255,' + (0.06 + 0.12 * pTrim).toFixed(3) + ')'; e.style.borderColor = 'rgba(47,149,255,' + (0.1 + 0.4 * pTrim).toFixed(3) + ')';
      e.style.color = B.mixc([230, 231, 234], [207, 231, 255], pTrim); }
    else { const q = B.P(t, d.trim + c.i * 0.025, 0.3, 'power2.in'); e.style.opacity = 1 - q; e.style.transform = 'scale(' + (1 - 0.3 * q).toFixed(3) + ')'; } });
  document.querySelectorAll('.sysl').forEach((e, i) => { if (i > 0) e.style.opacity = 1 - pSys; else e.style.width = B.lerp(740, 300, pSys).toFixed(1) + 'px'; });
  const k = d.tok;
  const tok = k.bk_sys * (1 - pSys) + d.tokSys2 * pSys + k.bk_tool * (1 - pTrim) + d.tokTool2 * pTrim
      + k.bk_mcp * (1 - out.bk_mcp) + k.bk_sub * (1 - out.bk_sub) + k.bk_skl * (1 - out.bk_skl);
  B.$('mnum').textContent = '≈' + (tok >= 9.95 ? Math.round(tok) : tok.toFixed(1)) + 'K';
  B.$('mbar').style.width = (100 * tok / 32).toFixed(2) + '%';
  const g = B.cl((30 - tok) / 26, 0, 1);              // ember while the harness is heavy, azure once it is lean
  const col = B.mixc([255, 138, 91], [47, 149, 255], g);
  B.$('mnum').style.color = col; B.$('mbar').style.background = col;
  B.$('mbar').style.boxShadow = '0 0 14px ' + col;
};
"""
    moves = [dict(t=0.0, dur=t_opt - 0.6, kind='glide', to=dict(x=784, y=540, s=1.03)),
             dict(t=t_opt - 0.35, dur=1.4, kind='push', to=dict(x=777, y=530, s=1.055))]
    cfg = dict(id='g16', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=540, s=1.0), cards=[smol, meter, stack], moves=moves, pushRef=1.2,
               heroes=[dict(t=0, id='none')], data=data, wave=dict(level='low', k=0.9),
               sfx=sfx((t_never, 'click'), (t_mcp, 'click'), (t_sub, 'click'), (t_lim, 'click'), (t_tiny, 'click'), (t_opt, 'chime')))
    mk('g16', cfg, js=js)


# ------------------------------------------------------------------------------------------------ g20 + g21
OPEN_ISSUE = ('<svg viewBox="0 0 16 16" style="width:{s}px;height:{s}px;flex:none"><circle cx="8" cy="8" r="6.6" fill="none" stroke="#0F7A52" stroke-width="1.6"/>'
              '<circle cx="8" cy="8" r="1.7" fill="#0F7A52"/></svg>')
LABELS = {'ready': ('mint', 'ready'), 'run': ('azure', 'factory:running')}
PR_ICON = ('<svg viewBox="0 0 16 16" style="width:{s}px;height:{s}px;flex:none"><path fill="#0F7A52" d="M5.45 5.15A2.25 2.25 0 1 0 3.75 5.4v5.2a2.25 2.25 0 1 0 1.5 0V5.4c.07-.08.14-.16.2-.25zM4.5 12.5a.75.75 0 1 1 0 1.5.75.75 0 0 1 0-1.5zm0-9.5a.75.75 0 1 1 0 1.5.75.75 0 0 1 0-1.5zm6.03 1.22-.97-.97a.25.25 0 0 1 .18-.43h2.51c.14 0 .25.11.25.25v2.51a.25.25 0 0 1-.43.18l-.97-.97L9.8 6.6a1 1 0 0 0-.3.7v3.3a2.25 2.25 0 1 1-1.5 0V7.3a2.5 2.5 0 0 1 .73-1.77zM8.75 12.5a.75.75 0 1 1 0 1.5.75.75 0 0 1 0-1.5z"/></svg>')


def gh_label(lid, kind, fs=34, style=''):
    tone, txt = LABELS[kind]
    return f'<div id="{lid}" class="abs pl {tone}" style="font-size:{fs}px;opacity:0;transform-origin:0 50%;{style}">{txt}</div>'


def factory(bid):
    """THE SOFTWARE FACTORY SWARM, one world for g20 and g21. Everything is a function of factory time F (seconds since
    g20's start); each beat renders its own window of it (camera, wave and all), so g21's frame 0 is exactly the frame
    after g20's last one. Left: two app repos as white GitHub windows. Middle: the Factory workflow on glass (GitHub
    Actions, the private software-factory repo). Right: the agent swarm (worker pool) on highlighted glass, one sandbox per worker
    (Claude Code / Codex / SMOL Coder), paused when idle. Connectors glow azure while an issue travels them.
    g20: push to the pool on "swarm"; 10 then 20 workers pop in; they pause ("in the background"); the Codex, Claude
    Code and SMOL Coder workers light up on their names. g21: pull back; an issue gets the `ready` label, flies to the
    factory, the factory claims a free worker (azure flash) and the issue docks into it (busy: azure ring, spinner, #41);
    more issues stream in until all 20 are busy; the next issue waits in the factory (ember pulse, the factory looks
    again); one worker finishes (PR, checks passed in mint) and frees up; the waiting issue docks into it."""
    b20, w20 = words('g20')
    b21, w21 = words('g21')
    OFF = round(b21['t0'] - b20['t0'], 4)                 # g21 starts at F = 21.7333
    A = lambda w, n=1: W(w20, w, n)                        # g20 word -> F
    Bw = lambda w, n=1: OFF + W(w21, w, n)                 # g21 word -> F

    # ---------------- world geometry (overview camera s 0.77; content x 0..1836)
    RX, RW, RH = 220, 440, 350                             # repos column
    FX, FW, FH = 715, 430, 540                             # factory card
    PX0, PW, PH, PY = 990, 846, 836, 540                   # pool card (left, w, h, centre y)
    PXc, PT = PX0 + PW / 2, PY - PH / 2
    WW, WH, WG, GX0, GY0 = 178, 124, 16, 43, 112           # worker card + grid origin inside the pool
    COLS = 4
    types = ['claude', 'codex', 'claude', 'smol',
             'codex', 'claude', 'smol', 'codex',
             'claude', 'codex', 'claude', 'codex',
             'smol', 'claude', 'codex', 'claude',
             'codex', 'smol', 'claude', 'codex']
    cnt = {'claude': 0, 'codex': 0, 'smol': 0}
    workers = []
    for i, ty in enumerate(types):
        cnt[ty] += 1
        r, c = divmod(i, COLS)
        lx, ly = GX0 + c * (WW + WG), GY0 + r * (WH + WG)
        workers.append(dict(i=i, ty=ty, name=f'{ty}-{cnt[ty]}', lx=lx, ly=ly, x=PX0 + lx + WW / 2, y=PT + ly + WH / 2))

    # ---------------- times (F)
    t_fac, t_swarm, t_ten, t_twenty = A('software'), A('swarm'), A('ten'), A('twenty')
    t_bg, t_codex, t_claude, t_own = A('background'), A('codex'), A('claude'), A('your')
    t_wait1 = Bw('waiting'); t_whenever = Bw('whenever'); t_change = Bw('change'); t_sf2 = Bw('software', 2)
    t_alloc = Bw('allocate'); t_coding = Bw('coding'); t_all = Bw('all')
    t_deal = Bw('deal'); t_becomes = Bw('becomes'); t_avail = Bw('available', 2)
    t_allocating = Bw('allocating'); t_next = Bw('next')

    W_FIRST, W_FREE = 8, 7                                 # first claimed worker (claude-4), the one that finishes (codex-3)
    for w in workers:
        w['tin'] = (t_ten if w['i'] < 10 else t_twenty) + 0.035 * (w['i'] % 10)
        w['tdim'] = t_bg + 0.03 * w['i']
    FAC = (FX, PY - FH / 2 + 300 + 95)                      # where issues sit inside the factory (its dashed slot)
    chips = []
    RY1, RY2 = 540 - 195, 540 + 195                         # repo card centres
    rowA = (RX - RW / 2 + 190, RY1 - RH / 2 + 104 + 40)     # cubefarm #41 row (chip start)
    rowB = (RX - RW / 2 + 190, RY2 - RH / 2 + 222 + 40)     # smolcoder #19 row
    tA_lift, tA_fac = t_change + 0.75, t_sf2 - 0.05
    tA_go = t_alloc + 1.35
    chips.append(dict(id='A', num='#41', big=True, tOn=tA_lift, tDock=t_coding,
                      segs=[dict(t0=tA_lift, d=tA_fac - tA_lift, a=rowA, b=FAC, arc=-120),
                            dict(t0=tA_go, d=t_coding - tA_go, a=FAC, b=(workers[W_FIRST]['x'], workers[W_FIRST]['y']), arc=-90)],
                      labels=[(tA_lift, 'ready'), (t_alloc, 'run')]))
    workers[W_FIRST]['busy'] = t_coding; workers[W_FIRST]['num'] = '#41'; workers[W_FIRST]['claim'] = t_alloc
    rest = sorted([w for w in workers if w['i'] != W_FIRST], key=lambda w: (w['x'], w['y']))
    t_c0 = t_all - 0.3
    for k, w in enumerate(rest):
        t0 = t_c0 + 0.075 * k
        w['busy'] = t0 + 0.55; w['num'] = f'#{43 + k}'
        chips.append(dict(id=f'c{k}', num=w['num'], big=False, tOn=t0, tDock=t0 + 0.55,
                          segs=[dict(t0=t0, d=0.55, a=FAC, b=(w['x'], w['y']), arc=-40 - 25 * (k % 3))], labels=[]))
    ex = RX + RW / 2 - 70
    for k, (sx, sy) in enumerate([(ex, rowA[1]), (ex, rowA[1] + 118), (ex, rowB[1] - 118), (ex, rowB[1]), (ex, rowA[1] + 60), (ex, rowB[1] - 60)]):
        t0 = t_all - 1.05 + 0.12 * k
        chips.append(dict(id=f'f{k}', num=['#42', '#43', '#18', '#44', '#45', '#46'][k], big=False, tOn=t0, tDock=t0 + 0.7, fade=True,
                          segs=[dict(t0=t0, d=0.7, a=(sx, sy), b=FAC, arc=-60)], labels=[]))
    tB_lift, tB_fac = t_deal - 1.4, t_deal
    tB_go = t_allocating - 0.3
    chips.append(dict(id='B', num='#19', big=True, tOn=tB_lift, tDock=t_next,
                      segs=[dict(t0=tB_lift, d=tB_fac - tB_lift, a=rowB, b=FAC, arc=-90),
                            dict(t0=tB_go, d=t_next - tB_go, a=FAC, b=(workers[W_FREE]['x'], workers[W_FREE]['y']), arc=-160)],
                      labels=[(tB_lift - 0.35, 'ready'), (tB_go, 'run')], wait=(tB_fac, tB_go)))
    workers[W_FREE]['free'] = t_becomes; workers[W_FREE]['busy2'] = t_next; workers[W_FREE]['num2'] = '#19'
    nm = {w['i']: w['name'] for w in workers}

    # ---------------- cards
    def repo(cid, name, y, issues):
        rows = ''
        for k, (num, title, lid) in enumerate(issues):
            ty = 104 + 118 * k
            rows += (f'<div id="rh_{lid}" class="abs" style="left:12px;right:12px;top:{ty - 14}px;height:112px;border-radius:16px;background:#E8F2FF;opacity:0"></div>'
                     f'<div class="abs fx" style="left:30px;top:{ty}px;gap:12px">{OPEN_ISSUE.format(s=38)}'
                     f'<div style="font:600 44px/1 Figtree;letter-spacing:-.02em;color:{INK};white-space:nowrap">{num} <span style="font-weight:500;color:{INK2}">{title}</span></div></div>'
                     + gh_label(f'lr_{lid}', 'ready', style=f'left:30px;top:{ty + 52}px') + gh_label(f'lx_{lid}', 'run', style=f'left:30px;top:{ty + 52}px'))
        h = (f'<div class="abs fx" style="left:30px;top:26px;gap:16px">{img("assets/b_github.png", 48, 48)}'
             f'<div style="font:600 46px/1 Figtree;letter-spacing:-.025em;color:{INK}">{name}</div></div>'
             f'<div class="abs" style="left:0;right:0;top:90px;height:1px;background:#ECEDF0"></div>{rows}')
        return dict(id=cid, kind='window', x=RX, y=y, w=RW, h=RH, html=h)
    repo1 = repo('repo1', 'cubefarm', RY1, [('#41', 'Day/night', 'a41'), ('#42', 'Pet dog', 'a42')])
    repo2 = repo('repo2', 'smolcoder', RY2, [('#18', '/export', 'b18'), ('#19', 'Themes', 'b19')])
    fac = dict(id='fac', kind='glass', x=FX, y=PY, w=FW, h=FH, html=(
        f'<div id="facglow" class="abs" style="inset:0;border-radius:28px;box-shadow:inset 0 0 0 2px {AZ},0 0 60px rgba(47,149,255,.6),inset 0 0 40px rgba(47,149,255,.25);opacity:0"></div>'
        f'<div class="abs fx" style="left:32px;top:30px;gap:18px">{img("assets/b_gh_actions_dark.png", 64, 64)}'
        f'<div style="font:600 50px/1 Figtree;letter-spacing:-.025em">Factory</div></div>'
        f'<div class="abs fx lodF gm" style="left:34px;top:116px;gap:10px;font-size:28px;color:{TM}">{line_ico("lock", 28, TM, 2)}software-factory</div>'
        f'<div class="abs fx" style="left:34px;top:176px;gap:16px">'
        f'<div style="position:relative;width:34px;height:34px;flex:none"><div id="fdot" style="position:absolute;inset:7px;border-radius:50%;background:#5A5D64"></div>'
        f'<div id="fspin" class="spin" style="position:absolute;inset:0;opacity:0"></div></div>'
        f'<div style="position:relative;height:50px;width:300px">'
        + ''.join(f'<div id="fst{k}" class="abs" style="left:0;top:0;font:600 44px/50px Figtree;letter-spacing:-.02em;color:{EM if k == 3 else "#fff"};white-space:nowrap;opacity:{1 if k == 0 else 0}">{s}</div>'
                  for k, s in enumerate(['idle', 'running', '→ ' + nm[W_FIRST], 'waiting…', '→ ' + nm[W_FREE]]))
        + f'</div></div>'
        f'<div id="fslot" class="abs" style="left:12px;right:12px;top:300px;height:190px;border-radius:22px;border:2px dashed rgba(255,255,255,.16)"></div>'))
    wk = ''
    for w in workers:
        logo = {'claude': img('assets/b_claude_symbol.png', 56, 56), 'codex': img('assets/b_codex.png', 56, 56, 'border-radius:14px'),
                'smol': img('assets/b_smol_logo_alpha.png', 112, 34, 'margin-top:12px')}[w['ty']]
        ring = f'left:{w["lx"] - 6}px;top:{w["ly"] - 6}px;width:{WW + 12}px;height:{WH + 12}px;border-radius:26px'
        wk += (f'<div id="wslot{w["i"]}" class="abs" style="left:{w["lx"]}px;top:{w["ly"]}px;width:{WW}px;height:{WH}px;border-radius:20px;border:2px dashed rgba(255,255,255,.14)"></div>'
               f'<div id="wk{w["i"]}" class="abs" style="left:{w["lx"]}px;top:{w["ly"]}px;width:{WW}px;height:{WH}px;border-radius:20px;opacity:0;'
               f'background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.10);box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 18px 30px -16px rgba(0,0,0,.7)">'
               f'<div id="wc{w["i"]}" class="abs" style="inset:0"><div class="abs" style="left:18px;top:16px">{logo}</div>'
               f'<div id="wp{w["i"]}" class="abs" style="right:12px;top:14px">{line_ico("pause", 36, "rgba(255,255,255,.55)", 2.6)}</div>'
               f'<div id="wn{w["i"]}" class="abs gm" style="left:20px;bottom:14px;font-size:28px;line-height:1;color:{TS}">{w["name"]}</div></div>'
               f'<div id="ws{w["i"]}" class="abs spin" style="right:16px;top:18px;width:36px;height:36px;opacity:0"></div>'
               f'<div id="wi{w["i"]}" class="abs" style="left:18px;bottom:12px;font:600 44px/1 Figtree;letter-spacing:-.02em;color:#fff;opacity:0">{w.get("num", "")}</div>'
               f'<div id="wi2{w["i"]}" class="abs" style="left:18px;bottom:12px;font:600 44px/1 Figtree;letter-spacing:-.02em;color:#fff;opacity:0">{w.get("num2", "")}</div>'
               f'</div>'
               f'<div id="wr{w["i"]}" class="abs" style="{ring};border:3px solid {AZ};box-shadow:0 0 24px rgba(47,149,255,.45),inset 0 0 18px rgba(47,149,255,.18);opacity:0"></div>'
               f'<div id="wf{w["i"]}" class="abs" style="{ring};border:4px solid {AZ};box-shadow:0 0 30px rgba(47,149,255,.7);opacity:0"></div>'
               f'<div id="wh{w["i"]}" class="abs" style="{ring};border:2px solid rgba(47,149,255,.7);box-shadow:0 0 28px rgba(47,149,255,.4);opacity:0"></div>')
    pool = dict(id='pool', kind='glass', highlight=True, x=PXc, y=PY, w=PW, h=PH, html=(
        f'<div class="abs fx" style="left:44px;top:28px;gap:20px">{robot_tile(60, 0)}'
        f'<div style="font:600 46px/1 Figtree;letter-spacing:-.025em">Agent Swarm</div></div>'
        f'<div class="abs" style="right:46px;top:34px;height:50px;width:420px">'
        f'<div id="pc0" class="abs" style="right:0;top:0;font:600 46px/50px Figtree;letter-spacing:-.02em;white-space:nowrap">0 workers</div>'
        f'<div id="pc1" class="abs" style="right:0;top:0;font:600 46px/50px Figtree;letter-spacing:-.02em;color:{AZ};white-space:nowrap;opacity:0">0 / 20 busy</div></div>'
        f'<div id="psweep" class="abs" style="left:0;top:96px;width:240px;bottom:0;background:linear-gradient(90deg,rgba(255,138,91,0),rgba(255,138,91,.16),rgba(255,138,91,0));opacity:0"></div>'
        + wk))
    # connectors: repo -> factory -> pool; graphite at rest, azure and glowing while an issue travels them
    wpaths = {'w1': f'M{RX + RW / 2},{RY1} C{RX + RW / 2 + 40},{RY1} {FX - FW / 2 - 40},{PY - 120} {FX - FW / 2},{PY - 120}',
              'w2': f'M{RX + RW / 2},{RY2} C{RX + RW / 2 + 40},{RY2} {FX - FW / 2 - 40},{PY + 120} {FX - FW / 2},{PY + 120}',
              'w3': f'M{FX + FW / 2},{PY} L{PX0},{PY}'}
    wsvg = ('<svg width="2000" height="1080" style="position:absolute;left:0;top:0;overflow:visible">'
            + ''.join(f'<path d="{p}" fill="none" stroke="#5A5D64" stroke-width="4" stroke-linecap="round"/>' for p in wpaths.values())
            + ''.join(f'<path id="{k}a" d="{p}" fill="none" stroke="{AZ}" stroke-width="5" stroke-linecap="round" stroke-dasharray="12 12" '
                      f'style="filter:drop-shadow(0 0 6px rgba(47,149,255,.9))" opacity="0"/>' for k, p in wpaths.items())
            + '</svg>')
    wires = dict(id='wires', kind='plain', clip=False, x=1000, y=540, w=2000, h=1080, html=wsvg)
    # chips (issues on paper) and the PR card live on an overlay card that covers the world (world px = card px)
    BCW = 400
    ch = ''
    for c in chips:
        if c['big']:
            inner = (f'<div class="abs fx" style="left:22px;top:20px;gap:12px">{OPEN_ISSUE.format(s=38)}<div style="font:600 46px/1 Figtree;letter-spacing:-.02em;color:{INK}">{c["num"]}</div></div>'
                     + gh_label(f'cr_{c["id"]}', 'ready', style='left:22px;top:86px') + gh_label(f'cx_{c["id"]}', 'run', style='left:22px;top:86px'))
            ch += (f'<div id="ch_{c["id"]}" class="abs" style="left:0;top:0;width:{BCW}px;height:156px;border-radius:24px;{PAPER}opacity:0;transform-origin:0 0">{inner}</div>'
                   f'<div id="chp_{c["id"]}" class="abs" style="left:0;top:0;width:{BCW}px;height:156px;border-radius:24px;box-shadow:0 0 0 4px {EM},0 0 40px rgba(255,138,91,.6);opacity:0;transform-origin:0 0"></div>')
        else:
            ch += (f'<div id="ch_{c["id"]}" class="abs fx" style="left:0;top:0;height:66px;padding:0 18px;gap:10px;border-radius:18px;{PAPER}opacity:0;transform-origin:0 0">{OPEN_ISSUE.format(s=30)}'
                   f'<div style="font:600 44px/1 Figtree;letter-spacing:-.02em;color:{INK}">{c["num"]}</div></div>')
    wf = workers[W_FREE]
    pr = (f'<div id="prc" class="abs" style="left:{wf["x"] - 300}px;top:{wf["y"] - 212}px;width:400px;height:160px;border-radius:24px;{PAPER}opacity:0;transform-origin:50% 100%">'
          f'<div class="abs fx" style="left:28px;top:26px;gap:14px">{PR_ICON.format(s=40)}<div style="font:600 46px/1 Figtree;letter-spacing:-.02em;color:{INK}">PR #87</div></div>'
          f'<div class="abs pl mint" style="left:26px;top:90px;display:flex;align-items:center;gap:10px;font-size:30px;padding:7px 18px 7px 8px">{mint_check(32)}checks passed</div></div>')
    over = dict(id='over', kind='plain', clip=False, x=1000, y=540, w=2000, h=1080, noDof=True, forceSharp=True, html=ch + pr)

    # ---------------- camera (F), then cut per beat
    cam_ov = dict(x=918, y=540, s=0.77)
    cam_pool = dict(x=1413, y=540, s=1.07)
    moves = [dict(t=0.0, dur=t_swarm - 0.3, kind='glide', to=dict(x=918, y=540, s=0.785)),
             dict(t=t_swarm - 0.35, dur=1.6, kind='push', to=cam_pool),
             dict(t=t_bg + 0.6, dur=t_whenever - (t_bg + 0.6) - 0.5, kind='glide', to=dict(x=1413, y=540, s=1.1)),
             dict(t=t_whenever - 0.5, dur=1.4, kind='pull', to=cam_ov),
             dict(t=t_whenever + 1.0, dur=OFF + b21['dur'] - (t_whenever + 1.0), kind='glide', to=dict(x=918, y=540, s=0.785))]
    casc_end = t_c0 + 0.075 * 18 + 0.7
    data = dict(OFF=0, workers=[dict(i=w['i'], ty=w['ty'], tin=w['tin'], tdim=w['tdim'], busy=w.get('busy'), claim=w.get('claim'),
                                     free=w.get('free'), busy2=w.get('busy2')) for w in workers],
                hl=dict(codex=[t_codex, t_claude - 0.15], claude=[t_claude, t_own - 0.15], smol=[t_own, t_wait1 + 0.6]),
                chips=chips, t_fac=t_fac, t_ten=t_ten, t_twenty=t_twenty, t_coding=t_coding,
                fst=[[0, 0], [tA_fac, 1], [t_alloc, 2], [t_coding, 1], [t_deal, 3], [tB_go, 4], [t_next, 1]],
                t_running=tA_fac, t_wait=(tB_fac, tB_go), sweeps=[t_deal + 0.5, t_deal + 1.7, t_deal + 2.9],
                pr=(t_becomes, t_allocating - 0.2), rows=dict(a41=[t_change, t_alloc], a42=[t_all - 1.05, t_all - 0.45], b18=[t_all - 0.81, t_all - 0.2],
                                                               b19=[tB_lift - 0.35, tB_go]),
                wires=dict(w1=[[tA_lift - 0.1, tA_fac + 0.2], [t_all - 1.05, t_all - 0.3]],
                           w2=[[t_all - 0.8, t_all - 0.25], [tB_lift - 0.1, tB_fac + 0.2]],
                           w3=[[tA_go - 0.1, t_coding + 0.1], [t_c0, casc_end], [tB_go - 0.1, t_next + 0.1]]))
    js = r"""
window.CFG_RENDER = function (t, cam) {
  const d = CFG.data, F = t + d.OFF;
  const P = (t0, du, e) => B.P(F, t0, du, e);
  const lod = B.cl((cam.s - 0.95) / 0.2, 0, 1);
  const nIn = d.workers.filter((w) => F >= w.tin).length;
  const nBusy = d.workers.filter((w) => (w.busy != null && F >= w.busy && !(w.free != null && F >= w.free && !(w.busy2 != null && F >= w.busy2)))).length;
  const showBusy = F >= d.t_coding;
  B.$('pc0').textContent = nIn + ' workers'; B.$('pc0').style.opacity = showBusy ? 0 : 1;
  B.$('pc1').textContent = nBusy + ' / 20 busy'; B.$('pc1').style.opacity = showBusy ? 1 : 0;
  d.workers.forEach((w) => {
    const i = w.i, el = B.$('wk' + i);
    const pin = P(w.tin, 0.45, 'back.out(1.6)');
    let dim = P(w.tdim, 0.6, 'power2.inOut');
    const h = d.hl[w.ty]; let hl = 0;
    if (h) hl = P(h[0] - 0.05, 0.35, 'power2.out') * (1 - P(h[1], 0.45, 'power2.inOut'));
    let busy = w.busy != null ? P(w.busy, 0.3, 'power2.out') : 0;
    let fr = 0;
    if (w.free != null) { fr = P(w.free, 0.35, 'power2.inOut'); busy *= 1 - fr; }
    let busy2 = w.busy2 != null ? P(w.busy2, 0.3, 'power2.out') : 0;
    busy = Math.max(busy, busy2);
    const claim = w.claim != null ? P(w.claim, 0.25, 'power2.out') : 0;
    dim = dim * (1 - Math.max(busy, hl, claim * 0.6, fr * (1 - busy2)));
    const breathe = 0.04 * Math.sin(F * 1.7 + i * 0.9) * dim;
    el.style.opacity = Math.min(1, pin * 1.6).toFixed(3);
    const wc = B.$('wc' + i);
    wc.style.opacity = (1 - 0.6 * dim + breathe).toFixed(3);
    wc.style.filter = dim > 0.01 ? 'grayscale(' + (0.85 * dim).toFixed(3) + ')' : 'none';
    el.style.background = 'rgba(' + (busy > 0.01 ? '47,149,255,' + (0.055 + 0.07 * busy).toFixed(3) : '255,255,255,.055') + ')';
    const bump = (w.busy != null ? Math.sin(Math.PI * P(w.busy - 0.05, 0.35)) : 0) + (w.busy2 != null ? Math.sin(Math.PI * P(w.busy2 - 0.05, 0.35)) : 0);
    el.style.transform = 'scale(' + (B.lerp(0.6, 1, pin) * (1 + 0.05 * hl + 0.06 * bump)).toFixed(4) + ')';
    B.$('wslot' + i).style.opacity = (1 - Math.min(1, pin * 2)).toFixed(3);
    B.$('wp' + i).style.opacity = (1 - busy).toFixed(3);
    const sp = B.$('ws' + i); sp.style.opacity = busy.toFixed(3); sp.style.transform = 'rotate(' + ((F * 400 + i * 37) % 360).toFixed(1) + 'deg)';
    const b2 = w.busy2 != null ? busy2 : 0;
    B.$('wn' + i).style.opacity = ((1 - busy) * lod).toFixed(3);
    B.$('wi' + i).style.opacity = (busy * (1 - b2)).toFixed(3);
    B.$('wi2' + i).style.opacity = b2.toFixed(3);
    B.$('wr' + i).style.opacity = busy.toFixed(3);
    B.$('wh' + i).style.opacity = (hl * pin).toFixed(3);
    // claim flash (azure) and free flash (mint)
    const f = B.$('wf' + i);
    let fo = 0, fs = 1, col = '#2F95FF', glow = 'rgba(47,149,255,.7)';
    if (w.claim != null && F >= w.claim) { const q = P(w.claim, 0.7, 'power2.out'); fo = (1 - q) * 0.95; fs = 1 + 0.35 * q; }
    if (w.free != null && F >= w.free) { const q = P(w.free + 0.1, 0.8, 'power2.out'); fo = (1 - q) * 0.95; fs = 1 + 0.35 * q; col = '#4FD6A0'; glow = 'rgba(79,214,160,.75)'; }
    f.style.opacity = fo.toFixed(3); f.style.transform = 'scale(' + fs.toFixed(4) + ')'; f.style.borderColor = col; f.style.boxShadow = '0 0 30px ' + glow;
  });
  B.$('facglow').style.opacity = (0.9 * Math.sin(Math.PI * P(d.t_fac, 1.2))).toFixed(3);
  let st = 0; d.fst.forEach((s) => { if (F >= s[0]) st = s[1]; });
  for (let k = 0; k < 5; k++) B.$('fst' + k).style.opacity = k === st ? 1 : 0;
  const running = F >= d.t_running && st !== 0;
  const fsn = B.$('fspin');
  fsn.style.opacity = running ? 1 : 0; B.$('fdot').style.opacity = running ? 0 : 1;
  fsn.style.transform = 'rotate(' + ((F * 360) % 360).toFixed(1) + 'deg)';
  fsn.style.borderColor = st === 3 ? 'rgba(255,138,91,.25)' : 'rgba(47,149,255,.25)'; fsn.style.borderTopColor = st === 3 ? '#FF8A5B' : '#2F95FF';
  document.querySelectorAll('.lodF').forEach((e) => { e.style.opacity = lod; });
  let sw = 0, sx = 0;
  d.sweeps.forEach((s0) => { if (F >= s0 && F < s0 + 0.9) { const q = (F - s0) / 0.9; sw = Math.sin(Math.PI * q); sx = q; } });
  B.$('psweep').style.opacity = sw.toFixed(3); B.$('psweep').style.transform = 'translateX(' + (sx * 600).toFixed(1) + 'px)';
  // connectors glow while an issue travels them
  Object.keys(d.wires).forEach((k) => { let a = 0; d.wires[k].forEach((iv) => { a = Math.max(a, P(iv[0], 0.25) * (1 - P(iv[1], 0.35))); });
    const e = B.$(k + 'a'); e.setAttribute('opacity', a.toFixed(3)); e.style.strokeDashoffset = (-F * 90).toFixed(1); });
  Object.keys(d.rows).forEach((k) => { const [t0, t1] = d.rows[k];
    const r = P(t0, 0.3, 'back.out(2)'), xo = P(t1, 0.1), x = P(t1 + 0.08, 0.3, 'back.out(1.8)');
    const lr = B.$('lr_' + k), lx = B.$('lx_' + k);
    lr.style.opacity = (Math.min(1, r * 2) * (1 - xo)).toFixed(3); lr.style.transform = 'scale(' + B.lerp(0.5, 1, r).toFixed(4) + ')';
    lx.style.opacity = Math.min(1, x * 2).toFixed(3); lx.style.transform = 'scale(' + B.lerp(0.5, 1, x).toFixed(4) + ')';
    B.$('rh_' + k).style.opacity = (0.95 * Math.sin(Math.PI * P(t0 - 0.1, 1.4))).toFixed(3); });
  d.chips.forEach((c) => {
    const el = B.$('ch_' + c.id);
    if (F < c.tOn || F > c.tDock + 0.3) { el.style.opacity = 0; const pp = B.$('chp_' + c.id); if (pp) pp.style.opacity = 0; return; }
    let pos = c.segs[0].a;
    c.segs.forEach((s) => { if (F >= s.t0) { const p = P(s.t0, s.d, 'power3.inOut');
      const ctrl = [(s.a[0] + s.b[0]) / 2, (s.a[1] + s.b[1]) / 2 + s.arc]; pos = B.qb(s.a, ctrl, s.b, p); } });
    const appear = P(c.tOn, Math.min(0.6, c.segs[0].d * 0.55), 'power2.out');
    const dock = P(c.tDock - 0.12, 0.38, 'power2.in');
    const sc = B.lerp(c.big ? 0.3 : 0.45, 1, appear) * (1 - 0.65 * dock);
    const w = el.offsetWidth, h = el.offsetHeight;
    el.style.opacity = (Math.min(1, appear * 2.5) * (1 - dock)).toFixed(3);
    el.style.transform = 'translate(' + (pos[0] - w * sc / 2).toFixed(2) + 'px,' + (pos[1] - h * sc / 2).toFixed(2) + 'px) scale(' + sc.toFixed(4) + ')';
    if (c.big) {
      let lab = null; c.labels.forEach((l) => { if (F >= l[0]) lab = l[1]; });
      const lr = B.$('cr_' + c.id), lx = B.$('cx_' + c.id);
      lr.style.opacity = lab === 'ready' ? 1 : 0; lx.style.opacity = lab === 'run' ? 1 : 0;
      const pp = B.$('chp_' + c.id);
      if (c.wait) { const on = F >= c.wait[0] && F < c.wait[1] ? 1 : 0;
        pp.style.transform = el.style.transform;
        pp.style.opacity = (on * (0.5 + 0.4 * Math.sin((F - c.wait[0]) * 6))).toFixed(3); }
    }
  });
  const pr = B.$('prc'), pa = P(d.pr[0], 0.5, 'back.out(1.7)'), pz = P(d.pr[1], 0.5, 'power2.in');
  pr.style.opacity = (Math.min(1, pa * 2) * (1 - pz)).toFixed(3);
  pr.style.transform = 'translateY(' + (B.lerp(90, 0, pa) - 60 * pz).toFixed(2) + 'px) scale(' + B.lerp(0.5, 1, pa).toFixed(4) + ')';
};
"""
    sfx_all = [(t_ten, 'pop'), (t_twenty, 'pop'),
               (t_change, 'click'), (t_alloc, 'click'), (t_coding, 'pop'), (t_all + 0.1, 'pop'),
               (tB_lift - 0.35, 'click'), (t_becomes, 'pop'), (t_avail, 'chime'), (t_next, 'pop')]
    heroes = [dict(t=0, id='none'), dict(t=t_swarm - 0.25, id='pool')]
    if bid == 'g20':
        b, off = b20, 0.0
    else:
        b, off = b21, OFF
    sh = lambda t: round(t - off, 4)
    cfg = dict(id=bid, dur=b['dur'], mode='fvp', cam0=cam_ov, pushRef=0.79, heroes=[dict(h, t=sh(h['t'])) for h in heroes],
               cards=[wires, repo1, repo2, fac, pool, over],
               moves=[dict(m, t=sh(m['t'])) for m in moves],
               wave=dict(level='low', k=1.0, t0=off),          # the wave is time-driven too: g21 continues g20's
               data=dict(data, OFF=off),
               sfx=sfx(*[(sh(t), k) for t, k in sfx_all if 0 <= t - off < b['dur']]))
    mk(bid, cfg, js=js)


# ------------------------------------------------------------------------------------------------ g18
def g18():
    """An orchestration harness (Leon's mint Orchestrate tile, highlighted glass) wires to three coding harnesses on
    glass (Claude Code, Codex, SMOL Coder) on "multiple coding harnesses"; a white job queue lands on "long-running
    jobs"; on "each job is executed by a specific coding agent or harness" azure job chips travel the glowing wires into
    specific harnesses, which turn busy."""
    b, ws = words('g18')
    T = lambda w, n=1: W(ws, w, n)
    t_mult, t_long, t_each = T('multiple'), T('longrunning'), T('each')
    t_exec, t_coding2, t_harn3 = T('executed'), T('coding', 2), T('harness', 3)
    OX, OY, OW, OH = 900, 250, 600, 176
    HY, HW, HH = 770, 400, 236
    HX = [334, 784, 1234]
    QX, QY, QW, QH = 324, 330, 440, 380
    orch = dict(id='orch', kind='glass', highlight=True, x=OX, y=OY, w=OW, h=OH, html=(
        f'<div class="abs fx" style="left:40px;top:0;bottom:0;gap:30px;padding-top:12px">{robot_tile(96, -8)}'
        f'<div><div style="font:600 54px/1 Figtree;letter-spacing:-.025em">Orchestrator</div>'
        f'<div style="position:relative;height:30px;margin-top:16px;width:320px">'
        + ''.join(f'<div id="os{k}" class="abs label{" accent" if k else ""}" style="left:0;top:0;font-size:26px;white-space:nowrap;opacity:{1 if k == 0 else 0}">{s}</div>'
                  for k, s in enumerate(['0 jobs running', '1 job running', '2 jobs running', '3 jobs running']))
        + '</div></div></div>'))
    st = lambda i: (f'<div class="abs fx" style="left:30px;bottom:24px;gap:14px;height:44px">'
                    f'<div style="position:relative;width:34px;height:34px"><div id="hd{i}" class="abs" style="inset:8px;border-radius:50%;background:#5A5D64"></div>'
                    f'<div id="hs{i}" class="abs spin" style="inset:0;opacity:0"></div></div>'
                    f'<div style="position:relative;width:300px;height:44px"><div id="hi{i}" class="abs" style="font:500 34px/44px Figtree;color:{TS}">idle</div>'
                    f'<div id="hr{i}" class="abs gm" style="font-size:30px;line-height:44px;color:{AZ};white-space:nowrap;opacity:0"></div></div></div>'
                    f'<div id="hring{i}" class="abs" style="inset:0;border-radius:28px;box-shadow:inset 0 0 0 2px {AZ},0 0 50px -10px rgba(47,149,255,.8);opacity:0"></div>')
    hcards = [
        dict(id='h0', kind='glass', x=HX[0], y=HY, w=HW, h=HH, land=dict(t=t_mult, dur=0.55),
             html=f'<div class="abs" style="left:34px;top:46px">{img("assets/b_cc_wordmark_dark.png", 330)}</div>' + st(0)),
        dict(id='h1', kind='glass', x=HX[1], y=HY, w=HW, h=HH, land=dict(t=t_mult + 0.28, dur=0.55),
             html=f'<div class="abs fx" style="left:34px;top:32px;gap:20px">{img("assets/b_codex.png", 76, 76, "border-radius:18px")}'
                  f'<div style="font:600 50px/1 Figtree;letter-spacing:-.025em">Codex</div></div>' + st(1)),
        dict(id='h2', kind='glass', x=HX[2], y=HY, w=HW, h=HH, land=dict(t=t_mult + 0.56, dur=0.55),
             html=f'<div class="abs" style="left:34px;top:40px">{img("assets/b_smol_logo_alpha.png", 250)}</div>' + st(2)),
    ]
    jobs = [('#12', 'auth-flow', '6 h'), ('#13', 'billing', '1 d'), ('#14', 'search', '9 h'), ('#15', 'dark-mode', '2 d')]
    rows = ''.join(f'<div id="jr{k}" class="abs fx" style="left:24px;right:24px;top:{100 + k * 66}px;height:56px;border-radius:14px;background:#F3F4F6;padding:0 16px;gap:14px;white-space:nowrap">'
                   f'<div class="gm" style="font-size:28px;color:#1560D0">{n}</div><div class="gm" style="font-size:28px;color:{INK}">{t}</div>'
                   f'<div class="fx" style="margin-left:auto;gap:8px;font:500 28px/1 Figtree;color:{INK2}">{line_ico("clock", 26, INK2, 2)}{d}</div></div>'
                   for k, (n, t, d) in enumerate(jobs))
    queue = dict(id='queue', kind='window', x=QX, y=QY, w=QW, h=QH, land=dict(t=t_long, dur=0.55), html=(
        f'<div class="abs fx" style="left:28px;top:26px;gap:16px">{tile("azure", "bars", 48, -8)}'
        f'<div style="font:600 36px/1 Figtree;letter-spacing:-.02em;color:{INK}">Job queue</div></div>' + rows))
    ox0, oy0 = OX, OY + OH / 2
    paths = [f'M{ox0},{oy0} C{ox0},{oy0 + 140} {x},{HY - HH / 2 - 150} {x},{HY - HH / 2}' for x in HX]
    svg = (f'<svg width="1600" height="1000" viewBox="0 0 1600 1000" style="position:absolute;left:0;top:0;overflow:visible">'
           + ''.join(f'<path id="wp{i}" d="{p}" fill="none" stroke="#5A5D64" stroke-width="4" stroke-linecap="round"/>' for i, p in enumerate(paths))
           + ''.join(f'<path id="wq{i}" d="{p}" fill="none" stroke="{AZ}" stroke-width="5" stroke-linecap="round" stroke-dasharray="14 14" '
                     f'style="filter:drop-shadow(0 0 6px rgba(47,149,255,.9))" opacity="0"/>' for i, p in enumerate(paths))
           + f'<path id="wjq" d="M{QX + QW / 2},{QY - 60} C{QX + QW / 2 + 40},{QY - 60} {OX - OW / 2 - 40},{OY} {OX - OW / 2},{OY}" fill="none" stroke="#5A5D64" stroke-width="4" stroke-linecap="round"/>'
           + '</svg>')
    chips = ''.join(f'<div id="jc{k}" class="abs gm" style="left:0;top:0;height:54px;padding:0 18px;border-radius:27px;background:{AZ};color:#fff;font-size:30px;'
                    f'line-height:54px;opacity:0;box-shadow:0 0 0 1px rgba(255,255,255,.25),0 0 28px rgba(47,149,255,.75)">{jobs[k][0]}</div>' for k in range(3))
    wires = dict(id='wires', kind='plain', clip=False, x=800, y=500, w=1600, h=1000, noDof=True, html=svg)
    over = dict(id='jobs', kind='plain', clip=False, x=800, y=500, w=1600, h=1000, noDof=True, forceSharp=True, html=chips)
    arr = [t_exec, t_coding2, t_harn3]
    dep = [t_each, t_coding2 - 1.05, t_harn3 - 1.0]
    data = dict(mult=t_mult, long=t_long, dep=dep, arr=arr, HX=HX, HY=HY - HH / 2 + 40, OX=OX, OY=OY + OH / 2 - 10,
                QX=QX + QW / 2 - 70, QY=[QY - QH / 2 + 128 + k * 66 for k in range(3)], jobs=[j[0] for j in jobs])
    js = r"""
window.CFG_RENDER = function (t, cam) {
  const d = CFG.data;
  for (let i = 0; i < 3; i++) {
    const w = B.$('wp' + i), L = w.getTotalLength();
    const p = B.P(t, d.mult + 0.1 + i * 0.28, 0.7, 'power2.inOut');
    w.style.strokeDasharray = L; w.style.strokeDashoffset = (L * (1 - p)).toFixed(1);
    const q = B.$('wq' + i); const on = B.P(t, d.dep[i] + 0.35, 0.2) * (1 - B.P(t, d.arr[i], 0.4));
    q.setAttribute('opacity', on.toFixed(3)); q.style.strokeDashoffset = (-t * 120).toFixed(1);
  }
  const wq = B.$('wjq'), Lq = wq.getTotalLength(), pq = B.P(t, d.long + 0.2, 0.6, 'power2.inOut');
  wq.style.strokeDasharray = Lq; wq.style.strokeDashoffset = (Lq * (1 - pq)).toFixed(1);
  for (let k = 0; k < 3; k++) {
    const c = B.$('jc' + k), t0 = d.dep[k], t1 = d.arr[k];
    const tm = t0 + 0.42 * (t1 - t0);
    let x, y;
    if (t < tm) { const p = B.P(t, t0, tm - t0, 'power2.inOut'); x = B.lerp(d.QX, d.OX, p); y = B.lerp(d.QY[k], d.OY, p) - 60 * Math.sin(Math.PI * p); }
    else { const p = B.P(t, tm, t1 - tm, 'power2.inOut'); const path = B.$('wp' + k), L = path.getTotalLength(); const pt = path.getPointAtLength(L * p);
      x = pt.x; y = pt.y; if (p >= 1) y = d.HY; }
    const vis = B.P(t, t0, 0.2) * (1 - B.P(t, t1 + 0.05, 0.25));
    const w = c.offsetWidth, h = c.offsetHeight;
    c.style.opacity = vis.toFixed(3); c.style.transform = 'translate(' + (x - w / 2).toFixed(1) + 'px,' + (y - h / 2).toFixed(1) + 'px)';
    const r = B.$('jr' + k); r.style.opacity = (1 - 0.65 * B.P(t, t0, 0.3)).toFixed(3);
    const bz = B.P(t, t1, 0.3, 'power2.out');
    B.$('hs' + k).style.opacity = bz; B.$('hd' + k).style.opacity = 1 - bz;
    B.$('hs' + k).style.transform = 'rotate(' + ((t * 400) % 360).toFixed(1) + 'deg)';
    B.$('hi' + k).style.opacity = 1 - bz; const hr = B.$('hr' + k); hr.style.opacity = bz; hr.textContent = 'running ' + d.jobs[k];
    B.$('hring' + k).style.opacity = bz;
  }
  let nr = 0; d.arr.forEach((ta) => { if (t >= ta) nr++; });
  for (let k = 0; k < 4; k++) B.$('os' + k).style.opacity = k === nr ? 1 : 0;
};
"""
    moves = [dict(t=t_mult - 0.3, dur=1.3, kind='pull', to=dict(x=790, y=505, s=1.0)),
             dict(t=t_mult + 1.1, dur=b['dur'] - t_mult - 1.1, kind='glide', to=dict(x=790, y=510, s=1.035))]
    cfg = dict(id='g18', dur=b['dur'], mode='fvp', cam0=dict(x=OX, y=OY + 60, s=1.32), cards=[wires, orch, queue] + hcards + [over],
               moves=moves, pushRef=1.4, heroes=[dict(t=0, id='none')], data=data, wave=dict(level='low', k=1.0),
               sfx=sfx((t_mult, 'pop'), (t_long, 'pop'), (t_exec, 'pop'), (t_coding2, 'pop'), (t_harn3, 'pop')))
    mk('g18', cfg, js=js)


# ------------------------------------------------------------------------------------------------ g19
def g19():
    """An AutoForge-style board as a white product window (his AutoForge icon, Pending / In Progress / Done, tag and
    status pills in the design system's colours). One feature at a time moves through; the backlog rolls up to the
    hundreds on "hundreds", a time readout flips hours -> days -> weeks on the words, the done counter climbs into the
    hundreds, every finished card shows a mint "tests passed" pill (chime on "test it"), and the autopilot toggle
    switches on (azure) on "autopilot"."""
    b, ws = words('g19')
    T = lambda w, n=1: W(ws, w, n)
    t_hund, t_hours, t_days, t_weeks = T('hundreds'), T('hours'), T('days'), T('weeks')
    t_baby, t_test, t_auto = T('babysit'), T('test'), T('autopilot')
    BX, BY, BW, BH = 784, 545, 1400, 880
    COLX, COLW, CARD_H, CARD_G, TOP = [36, 488, 940], 424, 150, 12, 196
    P = 1.6
    c_hit = t_test - 0.5
    n0 = 4
    cyc0 = c_hit - P * math.floor(c_hit / P)
    feats = [('functional', 'Create a task'), ('style', 'Nav bar & sidebar'), ('functional', 'Task detail modal'), ('UI', 'Rebrand to PlanForge'),
             ('functional', 'Filter by status'), ('functional', 'Due-date reminders'), ('style', 'Dark mode'), ('functional', 'Drag to reorder'),
             ('functional', 'Search tasks'), ('UI', 'Empty states'), ('functional', 'Export to CSV'), ('functional', 'Recurring tasks'),
             ('style', 'Mobile layout'), ('functional', 'Tag colours'), ('functional', 'Undo delete'), ('UI', 'Onboarding tour'), ('functional', 'Sub-tasks'),
             ('functional', 'Share a list'), ('style', 'Focus rings'), ('functional', 'Bulk edit')]
    tagc = {'functional': 'azure', 'style': 'ember', 'UI': 'iris'}
    cards_html = ''
    for j, (tag, title) in enumerate(feats):
        cards_html += (f'<div id="fc{j}" class="abs" style="left:0;top:0;width:{COLW}px;height:{CARD_H}px;border-radius:18px;background:#fff;border:1px solid #ECEDF0;opacity:0">'
                       f'<div class="abs" style="left:20px;top:16px">{pill(tag, tagc[tag], 22)}</div>'
                       f'<div class="abs gm" style="right:22px;top:20px;font-size:26px;color:{INK2}">#{20 + j}</div>'
                       f'<div class="abs" style="left:22px;top:66px;font:600 32px/1 Figtree;letter-spacing:-.015em;color:{INK};white-space:nowrap">{title}</div>'
                       f'<div id="fs{j}" class="abs" style="left:20px;bottom:12px">{pill("pending", "neutral", 22)}</div>'
                       f'<div id="fr{j}" class="abs pl azure" style="left:20px;bottom:12px;display:flex;align-items:center;gap:10px;font-size:22px;padding:6px 14px 6px 8px;opacity:0">'
                       f'<div id="fsp{j}" class="spin" style="width:24px;height:24px;border-width:3px"></div>running</div>'
                       f'<div id="fd{j}" class="abs pl mint" style="left:20px;bottom:12px;display:flex;align-items:center;gap:9px;font-size:22px;padding:5px 14px 5px 6px;opacity:0;transform-origin:0 50%">'
                       f'{mint_check(26)}tests passed</div></div>')
    colhead = lambda x, name, cid: (f'<div class="abs fx" style="left:{x + 8}px;top:128px;gap:14px"><div style="font:600 36px/1 Figtree;letter-spacing:-.02em;color:{INK}">{name}</div>'
                                    f'<div id="{cid}" class="pl neutral" style="font-size:24px;min-width:52px;text-align:center">0</div></div>')
    head = (f'<div class="abs fx" style="left:34px;top:0;height:104px;gap:18px">{img("assets/b_autoforge_icon.png", 62, 62)}'
            f'<div style="font:600 38px/1 Figtree;color:{INK};letter-spacing:.04em">AUTOFORGE</div>'
            f'<div class="fx" style="margin-left:18px;height:52px;padding:0 18px;border-radius:14px;background:#F3F4F6;gap:10px">'
            f'<span class="gm" style="font-size:28px;color:{INK}">project-planner</span></div></div>'
            f'<div class="abs fx" style="right:34px;top:0;height:104px;gap:30px">'
            f'<div class="fx" style="gap:12px">{line_ico("clock", 36, INK2, 2)}<div style="position:relative;width:190px;height:44px;overflow:hidden">'
            + ''.join(f'<div id="tm{k}" class="abs" style="left:0;top:0;font:600 36px/44px Figtree;letter-spacing:-.015em;color:{INK};white-space:nowrap">{s}</div>'
                      for k, s in enumerate(['45 min', '4 hours', '2 days', '3 weeks']))
            + f'</div></div><div class="fx" style="gap:14px"><div style="font:600 32px/1 Figtree;color:{INK}">Autopilot</div>'
              f'<div class="tog" id="auto" style="background:#D5D7DC"><div class="kn"></div></div></div></div>'
            f'<div class="abs" style="left:0;right:0;top:104px;height:1px;background:#ECEDF0"></div>'
            + colhead(COLX[0], 'Pending', 'cnt0') + colhead(COLX[1], 'In Progress', 'cnt1') + colhead(COLX[2], 'Done', 'cnt2')
            + ''.join(f'<div class="abs" style="left:{x}px;top:{TOP - 14}px;width:{COLW}px;height:{BH - TOP - 22}px;border-radius:20px;background:#F3F4F6"></div>' for x in COLX)
            + f'<div class="abs" style="left:{COLX[1]}px;top:{TOP - 14}px;width:{COLW}px;height:5px;border-radius:3px;background:{AZ}"></div>'
            + f'<div class="abs" style="left:{COLX[2]}px;top:{TOP - 14}px;width:{COLW}px;height:5px;border-radius:3px;background:{MI}"></div>'
            + cards_html)
    board = dict(id='board', kind='window', x=BX, y=BY, w=BW, h=BH, html=head)
    data = dict(P=P, cyc0=cyc0, n0=n0, N=len(feats), COLX=COLX, TOP=TOP + 6, STEP=CARD_H + CARD_G, hund=t_hund,
                tm=[0, t_hours, t_days, t_weeks], test=t_test, auto=t_auto, cyc_hit=c_hit)
    js = r"""
window.CFG_RENDER = function (t, cam) {
  const d = CFG.data, TR = 0.6;
  const cyc = (k) => d.cyc0 + (k - d.n0) * d.P;
  let n = 0; for (let k = 0; k < d.N; k++) if (cyc(k) <= t) n = k + 1;
  const slot = (j, m) => (j >= m ? [0, j - m] : (j === m - 1 ? [1, 0] : [2, m - 2 - j]));
  const p = n > 0 ? B.P(t, cyc(n - 1), TR, 'power3.inOut') : 1;
  for (let j = 0; j < d.N; j++) {
    const a = slot(j, Math.max(0, n - 1)), b = slot(j, n);
    const xa = d.COLX[a[0]], ya = d.TOP + a[1] * d.STEP, xb = d.COLX[b[0]], yb = d.TOP + b[1] * d.STEP;
    const x = B.lerp(xa, xb, p), y = B.lerp(ya, yb, p) - (a[0] !== b[0] ? 26 * Math.sin(Math.PI * p) : 0);
    const V = 4;
    let o = 1;
    if (b[1] >= V && a[1] >= V) o = 0; else if (b[1] >= V) o = 1 - p; else if (a[1] >= V) o = p;
    const e = B.$('fc' + j);
    e.style.opacity = o.toFixed(3);
    e.style.transform = 'translate(' + x.toFixed(2) + 'px,' + y.toFixed(2) + 'px)';
    e.style.boxShadow = a[0] !== b[0] && p < 1 ? '0 ' + (24 * Math.sin(Math.PI * p)).toFixed(1) + 'px 40px rgba(17,18,20,' + (0.22 * Math.sin(Math.PI * p)).toFixed(3) + ')' : '0 2px 6px rgba(17,18,20,.05)';
    const st = b[0] === 2 && p > 0.5 ? 2 : (b[0] === 1 && p > 0.5 ? 1 : a[0]);
    B.$('fs' + j).style.opacity = st === 0 ? 1 : 0; B.$('fr' + j).style.opacity = st === 1 ? 1 : 0;
    const fd = B.$('fd' + j); fd.style.opacity = st === 2 ? 1 : 0;
    B.$('fsp' + j).style.transform = 'rotate(' + ((t * 420) % 360).toFixed(1) + 'deg)';
    if (Math.abs(cyc(j + 1) - d.cyc_hit) < 0.01) { const q = B.P(t, d.test, 0.45, 'back.out(2.4)');
      fd.style.transform = 'scale(' + (1 + 0.18 * Math.sin(Math.PI * q)).toFixed(4) + ')'; }
  }
  const roll = B.P(t, d.hund, 0.9, 'power2.out');
  const lapse = (tt) => tt < d.tm[1] ? 0.4 * tt : (tt < d.tm[2] ? 1.8 + 30 * (tt - d.tm[1]) : (tt < d.tm[3] ? 18 + 60 * (tt - d.tm[2]) : 90 + 22 * (tt - d.tm[3])));
  const done = Math.round(7 + lapse(Math.max(0, t)) + n - d.n0);
  const total = Math.round(B.lerp(36, 330, roll));
  B.$('cnt0').textContent = Math.max(3, total - done - 1); B.$('cnt1').textContent = 1; B.$('cnt2').textContent = done;
  for (let i = 0; i < 4; i++) { const e = B.$('tm' + i); const into = B.P(t, d.tm[i], 0.35, 'power2.inOut'), out = i < 3 ? B.P(t, d.tm[i + 1], 0.35, 'power2.inOut') : 0;
    const vis = i === 0 ? 1 - out : into * (1 - out);
    e.style.opacity = vis.toFixed(3); e.style.transform = 'translateY(' + (i === 0 ? -44 * out : 44 * (1 - into) - 44 * out).toFixed(1) + 'px)'; }
  // the autopilot toggle on paper: grey -> azure
  const v = B.P(t, d.auto, 0.25, 'power2.inOut'), tg = B.$('auto');
  tg.style.background = B.mixc([213, 215, 220], [47, 149, 255], v); tg.style.boxShadow = '0 0 ' + (18 * v).toFixed(1) + 'px rgba(47,149,255,' + (0.5 * v).toFixed(3) + ')';
  tg.querySelector('.kn').style.transform = 'translateX(' + (28 * v).toFixed(2) + 'px)';
};
"""
    moves = [dict(t=0.0, dur=t_baby - 0.4, kind='glide', to=dict(x=784, y=540, s=1.03)),
             dict(t=t_baby - 0.25, dur=1.6, kind='push', to=dict(x=1040, y=420, s=1.22))]
    cfg = dict(id='g19', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=540, s=1.0), cards=[board], moves=moves, pushRef=1.3,
               heroes=[dict(t=0, id='none')], data=data, wave=dict(level='low', k=0.8), sfx=sfx((t_test, 'chime'), (t_auto, 'click')))
    mk('g19', cfg, js=js)


# ------------------------------------------------------------------------------------------------ g14
YT = {  # his real uploads (vidIQ metadata, 2026-10-13): id -> (title, duration)
    '4r80bMX_kGg': ('OpenCode + Ollama: I Replaced Claude Code With This (Full Setup)', '11:17'),
    '3x2q6-5XbQ8': ('Claude Code + Ollama = Free Forever', '9:15'),
    'N7Hkqznvc7I': ('Qwen 3.8 + DeepSeek Harness Is My New Free Claude Code', '17:33'),
    'cUwH8wxYDx8': ('Pi + Ollama I Replaced Claude Code With This FREE Local Agent', '21:02'),
    'u2vaM7ppzuE': ('I Built the Best Free Claude Code for Local AI', '14:34'),
    'AsvzMlLyQ38': ('I Built the Simplest Software Factory (You Can Copy It)', '27:34'),
}
VERIFIED = ('<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px;flex:none"><circle cx="12" cy="12" r="10" fill="#5F636B"/>'
            '<path d="M7.5 12.3l3 3 6-6.3" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def g14():
    """His channel as a white product window on the stage: his real channel header (avatar, @leonvanzyl, 105K
    subscribers) over a wall of 12 real thumbnails. On "open-weight models" his four local-model videos light up (the
    rest dim, an azure outline marks the four); then each comes forward over a dark veil as a white YouTube card (real
    thumbnail, real title, duration) on its name: OpenCode, Claude Code, DeepSeek Harness, Pi."""
    b, ws = words('g14')
    T = lambda w, n=1: W(ws, w, n)
    t_ow, t_oc, t_cc, t_ds, t_pi = T('openweight'), T('opencode'), T('claude'), T('deepseek'), T('pi')
    PX, PY, PW, PH = 784, 545, 1440, 850
    TW_, TH_, G = 318, 179, 24
    L0, T0 = (PW - (4 * TW_ + 3 * G)) / 2, 196
    wall = [['AsvzMlLyQ38', '4r80bMX_kGg', 'NBZmxhcz5lo', 'u2vaM7ppzuE'],
            ['WjOcStPCbgk', 'gYtQ1LKSgXY', 'lGWFlpffWk4', '3x2q6-5XbQ8'],
            ['N7Hkqznvc7I', 'nKiPOxDpcJY', 'cUwH8wxYDx8', 'opus']]
    order = ['4r80bMX_kGg', '3x2q6-5XbQ8', 'N7Hkqznvc7I', 'cUwH8wxYDx8']
    slots, th = {}, ''
    for r, row in enumerate(wall):
        for c, vid in enumerate(row):
            x, y = L0 + c * (TW_ + G), T0 + r * (TH_ + G)
            slots[vid] = (PX - PW / 2 + x, PY - PH / 2 + y)
            src = 'assets/b_yt_opus.jpg' if vid == 'opus' else f'assets/b_yt_{vid}.jpg'
            th += (f'<div id="wt_{vid}" class="abs" style="left:{x}px;top:{y}px;width:{TW_}px;height:{TH_}px;border-radius:14px;overflow:hidden;background:#ddd">'
                   f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;display:block"></div>'
                   f'<div id="wtr_{vid}" class="abs" style="left:{x - 6}px;top:{y - 6}px;width:{TW_ + 12}px;height:{TH_ + 12}px;border-radius:19px;'
                   f'border:4px solid {AZ};box-shadow:0 0 24px rgba(47,149,255,.45);opacity:0"></div>')
    head = (f'<div class="abs fx" style="left:{L0}px;top:40px;gap:26px"><img src="assets/avatar.png" style="width:110px;height:110px;border-radius:50%;object-fit:cover">'
            f'<div><div class="fx" style="gap:12px"><div style="font:600 52px/1 Figtree;letter-spacing:-.025em;color:{INK}">Leon van Zyl</div>{VERIFIED.format(s=34)}</div>'
            f'<div style="font:400 32px/1 Figtree;color:{INK2};margin-top:14px">@leonvanzyl · 105K subscribers</div></div></div>'
            f'<div class="abs" style="right:{L0}px;top:66px">{img("assets/b_youtube_logo.png", 200)}</div>')
    page_ = dict(id='page', kind='window', x=PX, y=PY, w=PW, h=PH, html=head + th)
    veil = dict(id='veil', kind='plain', x=PX, y=PY, w=PW, h=PH, noDof=True,
                html='<div id="veilb" class="abs" style="inset:0;border-radius:22px;background:rgba(11,12,14,.78);opacity:0"></div>')
    CW, CH, CX, CY = 900, 742, 784, 548
    BT = 840 / TW_
    fronts = []
    for k, vid in enumerate(order):
        title, dur = YT[vid]
        h = (f'<div id="fp{k}" class="abs" style="inset:0;border-radius:24px;{PAPER}opacity:0"></div>'
             f'<div class="abs" style="left:30px;top:30px;width:840px;height:473px;border-radius:16px;overflow:hidden">'
             f'<img src="assets/b_yt_{vid}.jpg" style="width:100%;height:100%;object-fit:cover;display:block">'
             f'<div class="abs gm" style="right:14px;bottom:14px;padding:4px 12px;border-radius:10px;background:rgba(0,0,0,.82);color:#fff;font-size:28px">{dur}</div></div>'
             f'<div id="ft{k}" style="position:absolute;left:30px;top:528px;width:840px;opacity:0">'
             f'<div style="font:600 44px/1.2 Figtree;letter-spacing:-.02em;color:{INK};display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">{title}</div>'
             f'<div class="fx" style="gap:16px;margin-top:20px"><img src="assets/avatar.png" style="width:56px;height:56px;border-radius:50%;object-fit:cover">'
             f'<div style="font:500 34px/1 Figtree;color:{INK2}">Leon van Zyl</div>{VERIFIED.format(s=28)}</div></div>')
        fronts.append(dict(id=f'f{k}', kind='plain', clip=False, x=CX, y=CY, w=CW, h=CH, noDof=True, forceSharp=True, html=h))
    t_in = [t_oc - 0.25, t_cc - 0.25, t_ds - 0.25, t_pi - 0.25]
    t_out = t_in[1:] + [99]
    data = dict(order=order, tin=t_in, tout=t_out, ow=t_ow, local=order,
                slot=[[slots[v][0] - (CX - CW / 2) - 30 / BT, slots[v][1] - (CY - CH / 2) - 30 / BT] for v in order],
                k0=1 / BT, all=[v for row in wall for v in row])
    js = r"""
window.CFG_RENDER = function (t, cam) {
  const d = CFG.data;
  const hl = B.P(t, d.ow, 0.5, 'power2.out');
  d.all.forEach((v) => { const e = B.$('wt_' + v); const loc = d.local.indexOf(v) >= 0;
    e.style.opacity = loc ? 1 : (1 - 0.6 * hl).toFixed(3); e.style.filter = loc || hl < 0.01 ? 'none' : 'grayscale(' + (0.8 * hl).toFixed(3) + ')';
    B.$('wtr_' + v).style.opacity = 0; });
  let veil = 0;
  d.order.forEach((v, k) => {
    const pin = B.P(t, d.tin[k], 0.62, 'power3.inOut'), pout = B.P(t, d.tout[k], 0.62, 'power3.inOut');
    const p = pin * (1 - pout);
    veil = Math.max(veil, p);
    const el = B.$('card-f' + k);
    const s = B.lerp(d.k0, 1, p), tx = B.lerp(d.slot[k][0], 0, p), ty = B.lerp(d.slot[k][1], 0, p);
    el.style.transformOrigin = '0 0';
    el.style.transform = 'translate(' + tx.toFixed(2) + 'px,' + ty.toFixed(2) + 'px) scale(' + s.toFixed(4) + ')';
    el.style.opacity = p > 0.001 ? 1 : 0;
    B.$('fp' + k).style.opacity = B.cl((p - 0.15) / 0.5, 0, 1).toFixed(3);
    B.$('ft' + k).style.opacity = B.cl((p - 0.55) / 0.4, 0, 1).toFixed(3);
    B.$('wt_' + v).style.visibility = p > 0.001 ? 'hidden' : 'visible';
    const r = B.$('wtr_' + v); r.style.opacity = (hl * (p > 0.001 ? 0 : 1)).toFixed(3);
  });
  B.$('veilb').style.opacity = veil.toFixed(3);
};
"""
    moves = [dict(t=0.0, dur=b['dur'], kind='glide', to=dict(x=784, y=540, s=1.03))]
    cfg = dict(id='g14', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=540, s=1.0), cards=[page_, veil] + fronts, moves=moves, pushRef=1.1,
               heroes=[dict(t=0, id='none')], data=data, wave=dict(level='low', k=0.8),
               sfx=sfx((t_oc, 'pop'), (t_cc, 'pop'), (t_ds, 'pop'), (t_pi, 'pop')))
    mk('g14', cfg, js=js)


# ------------------------------------------------------------------------------------------------ r04 / r05 / r06
BAND = 'background:rgba(47,149,255,.26);border-radius:8px;transform-origin:0 50%;transform:scaleX(0)'   # azure marker, multiply on the page


def watch(bid, asset, word, band_w):
    """his real YouTube watch page (logged out, player cued so the real thumbnail shows) in the capture window on the
    dark stage: a slow push; an azure marker band sweeps the real title on the word that names it"""
    b, ws = words(bid)
    fw, fh = D[asset]
    band = f'<div id="hl{bid}" style="position:absolute;left:18px;top:1278px;width:{band_w}px;height:60px;{BAND}"></div>'
    cap = capture_card('cap', fw, fh, mode='fvp', img=f'assets/{asset}', overlay=band, overlayBlend='multiply',
                       inner0=dict(fx=1000, fy=790, k=0.72),
                       inner=[dict(t=0.0, dur=b['dur'], fx=950, fy=835, k=0.76, ease='sine.inOut')])
    cap['radius'] = 22
    tw = W(ws, word)
    cfg = dict(id=bid, dur=b['dur'], mode='fvp', cam0=dict(x=784, y=540, s=1.0), cards=[cap], moves=[], heroes=[dict(t=0, id='cap')],
               reveals=[dict(el=f'hl{bid}', t=tw, dur=0.55, type='scaleX')], sfx=[], accent='azure', wave=dict(level='low', k=0.8))
    page(bid, cfg, backdrop=('img', f'assets/{asset}', fw, fh))


def r06():
    """the real cubefarm repo (re-shot 2026-10-13) in the capture window on the dark stage: an azure band on
    "cubefarm Public" on "open source", then the inner camera moves to the README's Get started and a band lands on
    `npx cubefarm` on "use them today"."""
    b, ws = words('r06')
    fw, fh = D['b_cubefarm.png']
    bands = (f'<div id="hlA" style="position:absolute;left:262px;top:386px;width:330px;height:62px;{BAND}"></div>'
             f'<div id="hlB" style="position:absolute;left:300px;top:3234px;width:232px;height:58px;{BAND}"></div>')
    t_open, t_use = W(ws, 'open'), W(ws, 'use')
    cap = capture_card('cap', fw, fh, mode='fvp', img='assets/b_cubefarm.png', overlay=bands, overlayBlend='multiply',
                       inner0=dict(fx=820, fy=755, k=0.95),
                       inner=[dict(t=t_open - 0.55, dur=0.6, fx=820, fy=660, k=1.12),
                              dict(t=t_open + 0.9, dur=0.8, fx=980, fy=3060, k=0.98)])
    cap['radius'] = 22
    cfg = dict(id='r06', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=540, s=1.0), cards=[cap], moves=[], heroes=[dict(t=0, id='cap')],
               reveals=[dict(el='hlA', t=t_open, dur=0.5, type='scaleX'), dict(el='hlB', t=t_use, dur=0.5, type='scaleX')], sfx=[],
               accent='azure', wave=dict(level='low', k=0.8))
    page('r06', cfg, backdrop=('img', 'assets/b_cubefarm.png', fw, fh))


# ------------------------------------------------------------------------------------------------ g17
def g17():
    """acme-harness (the same org as g13) as a highlighted glass hub: provider plugs on white paper chips on the left
    (Claude connected, an ember lock on its cable on "locked"; OpenAI plugs in and the lock opens on "OpenAI"; Gemini and
    a local Ollama join on "change the providers"), a model selector cycles on "models", the developers on glass on the
    right (Sam, Priya, Jon from g13) all carry the same tool row (one azure band sweeps all three on "consistent"). Then
    its glass admin panels below: policies stamp in on "policies", the tools allowlist ticks (mint) on "tools", roles
    (Admin / Developer / Viewer) land on "administrative rights"."""
    b, ws = words('g17')
    T = lambda w, n=1: W(ws, w, n)
    t_locked, t_openai, t_tools1, t_cons = T('locked'), T('openai'), T('tools'), T('consistent')
    t_change, t_prov2, t_models, t_ctrl = T('change'), T('providers', 2), T('models'), T('controlled')
    t_org, t_pol, t_tools2, t_admin, t_rights = T('organizational'), T('policies'), T('tools', 2), T('administrative'), T('rights')
    t_really = T('cool') - 0.6
    HX, HY, HW, HH = 784, 445, 480, 470
    PRX, PRW, PRH = 214, 300, 104
    PRY = [250, 380, 510, 640]
    SX, SW, SH = 1312, 360, 150
    SY = [285, 445, 605]
    provs = [('claude', 'b_claude_symbol.png', 'Claude', 0.0), ('openai', 'b_openai_symbol.png', 'OpenAI', t_openai),
             ('gemini', 'b_gemini_cli.png', 'Gemini', t_prov2), ('ollama', 'b_ollama.png', 'Ollama', t_prov2 + 0.25)]
    cards = []
    for k, (pid, logo, name, tl) in enumerate(provs):
        c = dict(id=f'p_{pid}', kind='paper', x=PRX, y=PRY[k], w=PRW, h=PRH, html=(
            f'<div class="abs fx" style="left:26px;top:0;bottom:0;gap:20px">{img("assets/" + logo, 56, 56, "border-radius:12px")}'
            f'<div style="font:600 36px/1 Figtree;letter-spacing:-.02em;color:{INK}">{name}</div></div>'
            f'<div class="abs" style="right:24px;top:{PRH / 2 - 9}px;width:18px;height:18px;border-radius:50%;background:{MI};box-shadow:0 0 0 5px rgba(79,214,160,.22)"></div>'))
        if tl > 0: c['land'] = dict(t=tl, dur=0.55)
        cards.append(c)
    tool_chips = ''.join(f'<div class="chipd">{n}</div>' for n in ['read', 'edit', 'bash'])
    models = [('b_claude_symbol.png', 'claude-opus-5.5'), ('b_openai_white.png', 'gpt-6'), ('b_ollama_white.png', 'qwen3'), ('b_claude_symbol.png', 'claude-fable-5.1')]
    sel = ''.join(f'<div id="ms{k}" class="abs fx" style="left:20px;top:0;bottom:0;gap:16px;opacity:{1 if k == 0 else 0}">{img("assets/" + lg, 40, 40)}'
                  f'<div class="gm" style="font-size:30px;color:#E6E7EA">{nm}</div></div>' for k, (lg, nm) in enumerate(models))
    hub = dict(id='hub', kind='glass', highlight=True, x=HX, y=HY, w=HW, h=HH, html=(
        f'<div id="hubglow" class="abs" style="inset:0;border-radius:28px;box-shadow:inset 0 0 0 2px {AZ},0 0 70px rgba(47,149,255,.55);opacity:0"></div>'
        f'<div class="abs fx" style="left:34px;top:30px;gap:18px">{tile("ember", "shield", 60, -8)}<div style="font:600 40px/1 Figtree;letter-spacing:-.025em">acme-harness</div></div>'
        f'<div class="abs label" style="left:36px;top:132px">Model</div>'
        f'<div id="msel" class="abs" style="left:34px;right:34px;top:170px;height:78px;border-radius:18px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);overflow:hidden">{sel}'
        f'<svg class="abs" viewBox="0 0 24 24" style="right:20px;top:23px;width:30px;height:30px" fill="none" stroke="{TS}" stroke-width="2.2" stroke-linecap="round"><path d="M7 10l5 5 5-5"/></svg></div>'
        f'<div class="abs label" style="left:36px;top:294px">Tools</div>'
        f'<div id="htools" class="abs fx" style="left:34px;top:334px;gap:12px">{tool_chips}</div>'))
    cards.append(hub)
    people = [('S', 'Sam', 'azure'), ('P', 'Priya', 'ember'), ('J', 'Jon', 'mint')]
    for k, (ini, name, col) in enumerate(people):
        cards.append(dict(id=f'seat{k}', kind='glass', x=SX, y=SY[k], w=SW, h=SH, html=(
            f'<div class="abs fx" style="left:22px;top:16px;gap:16px">{avatar(ini, col, 56)}<div style="font:600 34px/1 Figtree;letter-spacing:-.02em">{name}</div></div>'
            f'<div id="sband{k}" class="abs" style="left:12px;right:12px;top:80px;height:60px;border-radius:14px;background:rgba(47,149,255,.22);'
            f'box-shadow:inset 3px 0 0 {AZ};transform-origin:0 50%;transform:scaleX(0)"></div>'
            f'<div class="abs fx" style="left:22px;top:87px;gap:10px">{tool_chips}</div>')))
    hl_, hr_ = HX - HW / 2, HX + HW / 2
    cab = ''.join(f'<path id="cp{k}" d="M{PRX + PRW / 2},{PRY[k]} C{PRX + PRW / 2 + 80},{PRY[k]} {hl_ - 80},{HY - 60 + 40 * k} {hl_},{HY - 60 + 40 * k}" '
                  f'fill="none" stroke="{AZ}" stroke-opacity=".7" stroke-width="4" stroke-linecap="round" style="filter:drop-shadow(0 0 5px rgba(47,149,255,.7))"/>' for k in range(4))
    cab += ''.join(f'<path id="cs{k}" d="M{hr_},{HY - 40 + 40 * k} C{hr_ + 60},{HY - 40 + 40 * k} {SX - SW / 2 - 60},{SY[k]} {SX - SW / 2},{SY[k]}" '
                   f'fill="none" stroke="{AZ}" stroke-opacity=".7" stroke-width="4" stroke-linecap="round" style="filter:drop-shadow(0 0 5px rgba(47,149,255,.7))"/>' for k in range(3))
    lx, ly = (PRX + PRW / 2 + hl_) / 2, (PRY[0] + HY - 60) / 2
    lock = f'<div id="lock" class="abs" style="left:{lx - 30}px;top:{ly - 30}px;width:60px;height:60px;opacity:0">{tile("ember", "", 60, 0, svg=tile_svg("lock", 60))}</div>'
    cables = dict(id='cables', kind='plain', clip=False, x=800, y=700, w=1600, h=1400, noDof=True,
                  html=f'<svg width="1600" height="1400" style="position:absolute;left:0;top:0;overflow:visible">{cab}</svg>{lock}')
    cards.insert(0, cables)
    LY = 1250
    pol_rows = ''.join(f'<div id="pr{k}" class="abs fx cell" style="left:24px;right:24px;top:{104 + 84 * k}px;height:70px;'
                       f'padding:0 14px;gap:12px;font:500 30px/1 Figtree;white-space:nowrap;opacity:0;transform-origin:30% 50%">'
                       f'{mint_check(32)}{txt}</div>' for k, txt in enumerate(['Require PR review', 'No secrets in prompts', 'Audit every session']))
    tl_rows = ''.join(f'<div class="abs fx" style="left:30px;top:{104 + 54 * k}px;gap:18px">'
                      f'<div id="tb{k}" style="width:38px;height:38px;border-radius:10px;border:2px solid rgba(255,255,255,.22);display:flex;align-items:center;justify-content:center">'
                      f'<div id="tbc{k}" style="opacity:0">{line_ico("check", 26, "#0B2A1D", 3)}</div></div>'
                      f'<div class="gm" style="font-size:30px;color:#E6E7EA">{n}</div></div>' for k, n in enumerate(['read', 'edit', 'bash', 'web_fetch', 'deploy']))
    role_rows = ''.join(f'<div id="rr{k}" class="abs fx cell" style="left:24px;right:24px;top:{104 + 84 * k}px;height:70px;padding:0 18px;gap:14px;opacity:0">'
                        f'<div style="font:600 32px/1 Figtree;color:{c}">{r}</div><div class="gm" style="margin-left:auto;font-size:28px;color:{TS}">{p}</div></div>'
                        for k, (r, p, c) in enumerate([('Admin', 'all', AZ), ('Developer', 'tools', '#fff'), ('Viewer', 'read', '#fff')]))
    panel = lambda pid, x, icon, title, body: dict(id=pid, kind='glass', x=x, y=LY, w=456, h=380, html=(
        f'<div class="abs fx" style="left:26px;top:26px;gap:16px">{icon}<div style="font:600 36px/1 Figtree;letter-spacing:-.02em">{title}</div></div>' + body))
    cards += [panel('pol', 296, tile('ember', 'shield', 52, -8), 'Policies', pol_rows),
              panel('tal', 784, tile('iris', 'bolt', 52, 8), 'Tool allowlist', tl_rows),
              panel('rol', 1272, tile('azure', '', 52, -8, svg=tile_svg('user', 52)), 'Roles', role_rows)]
    data = dict(lock=t_locked, openai=t_openai, prov2=t_prov2, cons=t_cons, models=t_models, ctrl=t_ctrl,
                pol=[t_pol, t_pol + 0.45, t_pol + 0.9], tl=[t_tools2, t_tools2 + 0.18, t_tools2 + 0.36], roles=[t_admin, t_admin + 0.3, t_rights],
                mt=[0, t_models, t_models + 0.5, t_models + 1.0])
    js = r"""
window.CFG_RENDER = function (t, cam) {
  const d = CFG.data;
  const draw = (id, t0) => { const p = B.$(id), L = p.getTotalLength(), q = t0 <= 0 ? 1 : B.P(t, t0, 0.6, 'power2.inOut');
    p.style.strokeDasharray = L; p.style.strokeDashoffset = (L * (1 - q)).toFixed(1); };
  draw('cp0', 0); draw('cp1', d.openai + 0.1); draw('cp2', d.prov2 + 0.1); draw('cp3', d.prov2 + 0.35);
  for (let k = 0; k < 3; k++) draw('cs' + k, 0);
  const lk = B.$('lock'), on = B.P(t, d.lock, 0.35, 'back.out(2.2)'), off = B.P(t, d.openai, 0.35, 'power2.in');
  lk.style.opacity = (Math.min(1, on * 2) * (1 - off)).toFixed(3); lk.style.transform = 'scale(' + (B.lerp(0.4, 1, on) * (1 + 0.3 * off)).toFixed(4) + ')';
  for (let k = 0; k < 3; k++) B.$('sband' + k).style.transform = 'scaleX(' + B.P(t, d.cons - 0.1 + 0.08 * k, 0.5, 'power3.out').toFixed(4) + ')';
  for (let k = 0; k < 4; k++) { const e = B.$('ms' + k); const pin = k === 0 ? 1 : B.P(t, d.mt[k], 0.22, 'power2.out');
    const pout = k < 3 ? B.P(t, d.mt[k + 1], 0.18, 'power2.in') : 0;
    e.style.opacity = (pin * (1 - pout)).toFixed(3); e.style.transform = 'translateY(' + ((1 - pin) * 30 - pout * 30).toFixed(1) + 'px)'; }
  const act = t >= d.models && t < d.models + 1.6;
  B.$('msel').style.borderColor = act ? '#2F95FF' : 'rgba(255,255,255,.14)'; B.$('msel').style.boxShadow = act ? '0 0 24px rgba(47,149,255,.45)' : 'none';
  B.$('hubglow').style.opacity = (0.9 * Math.sin(Math.PI * B.P(t, d.ctrl, 1.4))).toFixed(3);
  d.pol.forEach((ts, k) => { const p = B.P(t, ts, 0.32, 'power3.out'), e = B.$('pr' + k); e.style.opacity = B.cl(p * 2.5, 0, 1); e.style.transform = 'scale(' + B.lerp(1.25, 1, p).toFixed(4) + ')'; });
  d.tl.forEach((ts, k) => { const p = B.P(t, ts, 0.25, 'back.out(2)'); B.$('tbc' + k).style.opacity = B.cl(p, 0, 1); B.$('tbc' + k).style.transform = 'scale(' + B.lerp(0.4, 1, p).toFixed(3) + ')';
    const q = B.P(t, ts, 0.2); const bx = B.$('tb' + k);
    bx.style.background = 'rgba(79,214,160,' + q.toFixed(3) + ')'; bx.style.borderColor = q > 0.5 ? '#4FD6A0' : 'rgba(255,255,255,.22)';
    bx.style.boxShadow = '0 0 ' + (16 * q).toFixed(1) + 'px rgba(79,214,160,' + (0.45 * q).toFixed(3) + ')'; });
  d.roles.forEach((ts, k) => { const p = B.P(t, ts, 0.45, 'power3.out'), e = B.$('rr' + k); e.style.opacity = B.cl(p * 2, 0, 1); e.style.transform = 'translateY(' + B.lerp(40, 0, p).toFixed(1) + 'px)'; });
};
"""
    moves = [dict(t=t_locked - 0.3, dur=1.0, kind='push', to=dict(x=560, y=440, s=1.12)),
             dict(t=t_tools1 - 0.25, dur=0.7, kind='step', to=dict(x=1010, y=445, s=1.12)),
             dict(t=t_change - 0.25, dur=0.6, kind='step', to=dict(x=560, y=450, s=1.12)),
             dict(t=t_models - 0.25, dur=0.5, kind='step', to=dict(x=850, y=440, s=1.12)),
             dict(t=t_ctrl - 0.25, dur=1.1, kind='pull', to=dict(x=784, y=450, s=1.04)),
             dict(t=t_org - 0.25, dur=1.0, kind='push', to=dict(x=296, y=LY, s=1.12)),
             dict(t=t_tools2 - 0.25, dur=0.6, kind='step', to=dict(x=784, y=LY, s=1.12)),
             dict(t=t_admin - 0.25, dur=0.6, kind='step', to=dict(x=1272, y=LY, s=1.12)),
             dict(t=t_really - 0.25, dur=1.3, kind='pull', to=dict(x=784, y=LY + 30, s=1.0))]
    cfg = dict(id='g17', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=450, s=1.04), cards=cards, moves=moves, pushRef=1.3,
               heroes=[dict(t=0, id='none')], data=data, wave=dict(level='low', k=0.8),
               sfx=sfx((t_locked, 'click'), (t_openai, 'pop'), (t_prov2, 'pop'), (t_models, 'click'), (t_pol, 'pop'), (t_tools2, 'click'), (t_admin, 'pop')))
    mk('g17', cfg, js=js)


def build():
    g13()
    g14()
    watch('r04', 'b_watch_smol.png', 'smol', 840)
    g15()
    g16()
    g17()
    g18()
    g19()
    watch('r05', 'b_watch_factory.png', 'building', 1010)
    r06()
    factory('g20')
    factory('g21')
