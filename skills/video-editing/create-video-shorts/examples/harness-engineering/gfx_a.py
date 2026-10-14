# Graphics agent A - shorts s1 ("Same model, 10x the score") and s5 ("My AI agent swarm in 3D").
# Build: $PY scripts/build_gfx.py a        (a few only: GFX_A=s1_r0,s5_r3 $PY scripts/build_gfx.py a)
# Assets: scripts/prep_assets_a.py (raw 6.mkv / 8.mkv stills and clips via longform_program.json, research captures, logos).
#
# Brand: Leon's "Leon YouTube" design system (engine theme 'stage'): graphite stage + wave, glass panels for diagrams,
# white paper / windows for real pages and UI, Figtree 600 + Geist Mono labels, azure accent, ember for limits, mint for
# passes, his glossy icon tiles. Patterns from the long-form reference edit (davinci-resolve-pro-edit examples/
# harness-engineering gfx_a.py / gfx_b.py): the FX keyframe library (pure functions of t), tiles, rings, chips, bands.
#
# Video cards: HyperFrames videos are root children ABOVE the world viewport (z-index 3). So
#  - anything drawn over live footage (highlight bands, logo chips) is a root-level layer (z-index 4/5); bands on footage
#    ride a layer that copies the video's transform + clip every frame (CFG.vov, see AFTER_JS);
#  - in a split the footage is masked by hand to the world's fade (y 900 -> 1060) so it never shows in the caption band.
import os, json
from build_gfx_common import *

ONLY = [s for s in os.environ.get('GFX_A', '').split(',') if s]

WHITE, T2, TM = '#FFFFFF', '#A3A6AD', '#7E818A'
AZ, EMB, MINT, IRIS = '#2F95FF', '#FF8A5B', '#4FD6A0', '#9C7CFF'
INK, INK2, PAPER2, PLINE = '#111214', '#5F636B', '#F3F4F6', '#ECEDF0'
HAIR = 'rgba(255,255,255,.09)'

EXTRA_CSS = """
.abs{position:absolute}
.m{font-family:'Geist Mono',ui-monospace,monospace}
.lab{font:500 30px/1.2 'Geist Mono';letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);white-space:nowrap}
.lab.acc{color:var(--accent)}.lab.wh{color:#fff}.lab.ember{color:#FF8A5B}.lab.mint{color:#4FD6A0}.lab.ink2{color:#5F636B}
.tile.lockd{background:linear-gradient(155deg,#43454C 0%,#2E3035 50%,#1D1E22 100%);box-shadow:inset 0 2px 1px rgba(255,255,255,.18),inset 0 -10px 18px rgba(0,0,0,.45),0 22px 44px -16px rgba(0,0,0,.8)}
.tile.lockd svg{opacity:.38}
.gl{background:rgba(24,25,28,.74);backdrop-filter:blur(24px) saturate(140%);-webkit-backdrop-filter:blur(24px) saturate(140%);
 border:1px solid rgba(255,255,255,.12);box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 40px 90px -30px rgba(0,0,0,.9);color:#fff}
.bandd{background:rgba(47,149,255,.24);border-bottom:4px solid #2F95FF;box-shadow:0 0 22px rgba(47,149,255,.45);border-radius:8px;transform-origin:0 50%;transform:scaleX(0)}
.ringd{border:4px solid #2F95FF;border-radius:16px;box-shadow:0 0 26px rgba(47,149,255,.6),inset 0 0 22px rgba(47,149,255,.28);transform-origin:0 50%;transform:scaleX(0)}
"""

# ------------------------------------------------------------------------------------------------- keyframe library
LIB = r"""
(function(){
const cl=(v,a,b)=>Math.max(a,Math.min(b,v));
const EZ={}; const ez=(n)=>{n=n||'power2.inOut'; if(n==='linear') return (p)=>p; return EZ[n]||(EZ[n]=gsap.parseEase(n));};
const EL={}; const $=(id)=>EL[id]||(EL[id]=document.getElementById(id));
const FX=window.FX||{tr:[],ty:[],num:[],cls:[]};
function at(kf,t){
  if(t<=kf[0][0]) return kf[0][1];
  for(let i=0;i<kf.length-1;i++){
    const a=kf[i],b=kf[i+1];
    if(t<b[0]){ const p=ez(b[2])(cl((t-a[0])/Math.max(1e-6,b[0]-a[0]),0,1)); const o={};
      for(const k in b[1]){ const va=a[1][k], vb=b[1][k]; o[k]=(k==='s'||k==='sx'||k==='sy')&&va>0&&vb>0? va*Math.pow(vb/va,p): va+(vb-va)*p; } return o; }
  }
  return kf[kf.length-1][1];
}
function apply(el,v){
  if('o' in v) el.style.opacity=cl(v.o,0,1);
  if('x' in v||'y' in v||'s' in v||'sx' in v||'sy' in v||'r' in v){
    const s=('s' in v)?v.s:1; el.style.transform=`translate(${(v.x||0).toFixed(2)}px,${(v.y||0).toFixed(2)}px) rotate(${(v.r||0).toFixed(3)}deg) scale(${(s*(('sx' in v)?v.sx:1)).toFixed(4)},${(s*(('sy' in v)?v.sy:1)).toFixed(4)})`; }
  if('b' in v) el.style.filter=v.b>0.05?`blur(${v.b.toFixed(2)}px)`:'none';
  if('w' in v) el.style.width=v.w.toFixed(2)+'px';
  if('h' in v) el.style.height=v.h.toFixed(2)+'px';
  if('mix' in v) el.style.setProperty('--mix',v.mix.toFixed(3));
}
function fmt(v,f){ if(f==='pct') return Math.round(v)+'%'; if(f==='1f') return v.toFixed(1); return String(Math.round(v)); }
function mask(el,Ty,S){ const a=(900-Ty)/S, b=(1060-Ty)/S;
  const g=`linear-gradient(to bottom,#000 0px,#000 ${a.toFixed(2)}px,rgba(0,0,0,0) ${b.toFixed(2)}px)`;
  el.style.webkitMaskImage=g; el.style.maskImage=g; }
const RX=/translate\(([^,]+)px,\s*([^)]+)px\)\s*scale\(([^)]+)\)/;
function after(t){
  const split=CFG.mode==='split';
  if(split) document.querySelectorAll('video.fg').forEach(v=>{ const m=RX.exec(v.style.transform); if(m) mask(v,+m[2],+m[3]); });
  for(const o of (CFG.vov||[])){ const v=$('v-'+o.card), el=$(o.el); if(!v||!el) continue;
    el.style.transform=v.style.transform; el.style.clipPath=v.style.clipPath; el.style.opacity=v.style.opacity;
    if(split){ const m=RX.exec(v.style.transform); if(m) mask(el,+m[2],+m[3]); } }
}
const prev=window.CFG_RENDER;
window.CFG_RENDER=function(t,cam){
  for(const tr of FX.tr){ if(tr.hold===false && t<tr.kf[0][0]) continue; const el=$(tr.el); if(el) apply(el,at(tr.kf,t)); }
  for(const nu of FX.num){ const el=$(nu.el); if(!el) continue; const v=at(nu.kf.map(k=>[k[0],{v:k[1]},k[2]]),t).v; const s=(nu.pre||'')+fmt(v,nu.fmt)+(nu.suf||''); if(el.textContent!==s) el.textContent=s; }
  for(const c of FX.cls){ const el=$(c.el); if(el) el.classList.toggle(c.cls, t>=c.on && (c.off==null||t<c.off)); }
  after(t);
  if(prev) prev(t,cam);
};
})();
"""

DEF = dict(o=1, x=0, y=0, s=1, sx=1, sy=1, r=0, b=0)


class FX:
    """per-page animation data: keyframe tracks (t, {props}, ease-of-the-segment-ending-at-t), counters, class toggles"""

    def __init__(self):
        self.raw = {}; self.num = []; self.cls = []; self.hold = {}

    def k(self, el, *frames):
        self.raw.setdefault(el, []).extend(frames)
        return self

    def number(self, el, kf, fmt='int', pre='', suf=''):
        self.num.append(dict(el=el, kf=[[round(a, 3), b, (c[0] if c else 'power2.inOut')] for a, b, *c in kf], fmt=fmt, pre=pre, suf=suf))

    def toggle(self, el, cls, on, off=None):
        self.cls.append(dict(el=el, cls=cls, on=round(on, 3), off=off))

    def js(self, custom=''):
        tr = []
        for el, frames in self.raw.items():
            frames = sorted(frames, key=lambda f: f[0])
            keys = set()
            for f in frames: keys.update(f[1].keys())
            cur = {k: DEF.get(k, 0) for k in keys}
            for k in keys:
                if k not in DEF: cur[k] = next(f[1][k] for f in frames if k in f[1])
            kf = []
            for f in frames:
                cur = {**cur, **f[1]}
                kf.append([round(f[0], 3), {k: round(v, 3) for k, v in cur.items()}, f[2] if len(f) > 2 else 'power2.inOut'])
            tr.append(dict(el=el, kf=kf, hold=self.hold.get(el, True)))
        return 'window.FX=' + json.dumps(dict(tr=tr, num=self.num, cls=self.cls)) + ';\n' + (custom or '') + '\n' + LIB


# ------------------------------------------------------------------------------------------------- building blocks
def r3(v):
    return round(v, 3)


def tile(color='azure', glyph='code', size=116, tilt=-8, id=None, style='', svg_markup=None, antenna=False):
    """his glossy icon tile in a positioned wrapper (#id); color azure|iris|ember|mint|lockd"""
    h = tile_html('azure' if color == 'lockd' else color, glyph, size, tilt, svg=svg_markup)
    if color == 'lockd': h = h.replace('class="tile azure"', 'class="tile lockd"', 1)
    if antenna:
        st, bl = max(4, round(size * 0.075)), round(size * 0.18)
        ant = (f'<span style="position:absolute;left:50%;width:{st}px;height:{round(size * .2)}px;top:{-round(size * .18)}px;margin-left:{-st / 2}px;'
               f'border-radius:999px;background:linear-gradient(180deg,#C4F6DF,#2DB883)"></span>'
               f'<span style="position:absolute;left:50%;width:{bl}px;height:{bl}px;top:{-round(size * .3)}px;margin-left:{-bl / 2}px;border-radius:50%;'
               f'background:radial-gradient(circle at 35% 30%,#fff 0%,#C4F6DF 35%,#2DB883 100%);box-shadow:0 0 12px rgba(79,214,160,.6)"></span>')
        h = h.replace('">', '">' + ant, 1)
    idh = f' id="{id}"' if id else ''
    return f'<div{idh} class="abs" style="width:{size}px;height:{size}px;{style}">{h}</div>'


def img(src, w, h, style=''):
    return f'<img src="{src}" class="abs" style="width:{w}px;height:{h}px;object-fit:contain;{style}">'


def ring(id, radius, color=AZ, glow='rgba(47,149,255,.45)', width=3, op=0):
    return (f'<div id="{id}" class="abs" style="inset:0;border-radius:{radius}px;box-shadow:inset 0 0 0 {width}px {color},inset 0 0 40px {glow};'
            f'opacity:{op};pointer-events:none"></div>')


def band(id, x, y, w, h, cls='band'):
    return f'<div id="{id}" class="{cls}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>'


def vov(card, fw, fh, inner, blend='multiply'):
    """a root-level layer that rides a live footage card (copies its transform / clip each frame): bands over video"""
    bl = f'mix-blend-mode:{blend};' if blend else ''
    return (f'<div id="vo-{card}" style="position:absolute;left:0;top:0;width:{fw}px;height:{fh}px;transform-origin:0 0;z-index:4;'
            f'pointer-events:none;{bl}">{inner}</div>')


def gchip(id, x, y, w, h, icon_html, name, size=44, style='', z=5):
    """a glass chip at SCREEN coordinates (root level, above live footage): an official logo + its product name"""
    return (f'<div id="{id}" class="gl" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;z-index:{z};'
            f'display:flex;align-items:center;gap:20px;padding:0 30px;opacity:0;{style}">{icon_html}'
            f'<div style="font:600 {size}px/1 Figtree;letter-spacing:-.02em;color:#fff;white-space:nowrap">{name}</div></div>')


def land(fx, el, t, dy=46, dur=0.5):
    """pop a root element in (fade + rise + scale), the engine's landing feel"""
    fx.k(el, (t, dict(o=0, y=dy, s=0.92)), (t + dur, dict(o=1, y=0, s=1), 'power3.out'))


def leave(fx, el, t, dur=0.35, dy=24):
    fx.k(el, (t, dict(o=1, y=0, s=1)), (t + dur, dict(o=0, y=dy, s=0.96), 'power2.in'))


def view(fw, fh, k, fx=None, fy=None, left=None, top=None, cw=1032, ch=1040):
    """inner-camera keyframe values clamped the way the engine clamps them (capture frame 1032x1040)"""
    hw, hh = cw / 2 / k, ch / 2 / k
    if left is not None: fx = left + hw
    if top is not None: fy = top + hh
    fx = fw / 2 if fw <= 2 * hw else min(max(fx, hw), fw - hw)
    fy = fh / 2 if fh <= 2 * hh else min(max(fy, hh), fh - hh)
    return dict(fx=round(fx, 1), fy=round(fy, 1), k=k)


def mk(rid, cfg, fx=None, extra_html='', videos=(), backdrop=None, css=''):
    if ONLY and rid not in ONLY: return
    cfg.setdefault('wave', dict(level='low', k=1.0))
    page(rid, cfg, extra_html=extra_html, extra_css=EXTRA_CSS + css, videos=videos, backdrop=backdrop,
         extra_js=(fx or FX()).js())


A = 'assets/'


# ================================================================================================= SHORT s1
def s1_r0():
    """split hook (cover-safe): Grok Code Fast 1's real pass rate from Can Bolük's edit-tool benchmark, drawn at true
    scale on a highlighted glass panel. Frame 0 = the panel's header (Grok mark + name) below the cover title; on "Grok"
    the camera steps up so the panel lands (bottom edge 890); on "only" the ember bar creeps to 6.7 % and the number
    lands on "6.7%"; then the bar starts to climb in azure (it reaches 68.3 % in the next, full-cam run)."""
    r, ws = words('s1', 0)
    fx = FX()
    PW, PH, PX, PY = 960, 680, 540, 600
    TX0, TW = 52, 856
    t_g, t_only, t_67 = W(ws, 'grok'), W(ws, 'only'), W(ws, '6.7')
    ticks = ''.join(f'<div class="abs" style="left:{TX0 + TW * p / 100 - 1}px;top:492px;width:2px;height:56px;background:rgba(255,255,255,.14)"></div>'
                    f'<div class="abs m" style="left:{TX0 + TW * p / 100 - 60}px;top:562px;width:120px;text-align:center;font-size:30px;line-height:36px;'
                    f'color:{TM}">{p}{"%" if p == 100 else ""}</div>' for p in (0, 25, 50, 75, 100))
    w67 = TW * 0.067
    html = (img(A + 'a_grok.png', 104, 104, 'left:52px;top:46px') +
            f'<div class="abs" style="left:184px;top:42px;font:600 66px/1.1 Figtree;letter-spacing:-.03em;color:#fff;white-space:nowrap">Grok Code Fast 1</div>'
            f'<div class="abs lab" style="left:186px;top:126px">Pass rate · edit benchmark</div>'
            f'<div class="abs" style="left:52px;top:196px;width:{PW - 104}px;height:1px;background:{HAIR}"></div>'
            f'<div id="num" class="abs" style="left:40px;top:214px;font:600 250px/1 Figtree;letter-spacing:-.045em;color:{EMB};'
            f'text-shadow:0 0 70px rgba(255,138,91,.45);transform-origin:0 70%;opacity:0">6.7%</div>'
            f'<div id="etool" class="abs" style="right:52px;top:300px;text-align:right;opacity:0"><div class="lab">Edit tool</div>'
            f'<div class="m" style="margin-top:10px;font-size:44px;line-height:1;font-weight:600;letter-spacing:.06em;color:{EMB}">PATCH</div></div>'
            f'<div class="abs" style="left:{TX0}px;top:500px;width:{TW}px;height:40px;border-radius:20px;background:rgba(255,255,255,.06);'
            f'box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)"></div>' + ticks +
            f'<div id="bar" class="abs" style="left:{TX0}px;top:500px;width:0;height:40px;border-radius:20px;'
            f'background:linear-gradient(90deg,#FF6F3C,#FF9A6E);box-shadow:0 0 26px rgba(255,138,91,.6)"></div>'
            f'<div id="barx" class="abs" style="left:{TX0 + w67 - 20}px;top:500px;width:0;height:40px;border-radius:20px;opacity:0;'
            f'background:linear-gradient(90deg,rgba(47,149,255,.0),#2F95FF 40%,#7DC0FF);box-shadow:0 0 30px rgba(47,149,255,.75)"></div>'
            + ring('pring', 32, 'rgba(47,149,255,.55)', 'rgba(47,149,255,.14)', 2, 1))
    cards = [dict(id='panel', kind='glass', highlight=True, x=PX, y=PY, w=PW, h=PH, html=html)]
    fx.k('bar', (t_only - 0.08, dict(w=0)), (t_only + 0.3, dict(w=w67), 'power2.out'))
    fx.k('num', (t_67 - 0.12, dict(o=0, s=0.82, y=20)), (t_67 + 0.26, dict(o=1, s=1, y=0), 'back.out(1.8)'))
    fx.k('etool', (t_67 + 0.05, dict(o=0, x=16)), (t_67 + 0.4, dict(o=1, x=0), 'power2.out'))
    t_c = 3.42
    fx.k('barx', (t_c, dict(w=20, o=0)), (t_c + 0.12, dict(o=1), 'linear'), (r['dur'], dict(w=20 + TW * 0.14), 'power2.in'))
    t_s = t_g - 0.25
    bot = PY + PH / 2                             # panel bottom (world); camera keeps it at screen y ~885 while pushing
    cy = lambda s, yb=885: r3(bot - (yb - 470) / s)
    moves = [dict(t=r3(t_s), dur=0.5, kind='step', to=dict(x=540, y=cy(1.0, 890), s=1.0)),
             dict(t=r3(t_s + 0.62), dur=1.3, kind='push', to=dict(x=540, y=cy(1.08), s=1.08)),
             dict(t=r3(t_s + 1.95), dur=r3(r['dur'] - t_s - 1.95), kind='glide', to=dict(x=540, y=cy(1.095), s=1.095))]
    cfg = dict(id='s1_r0', dur=r['dur'], mode='split', cam0=dict(x=540, y=r3(PY - (640 + PH / 2 - 470)), s=1.0), cards=cards, moves=moves, pushRef=1.0,
               heroes=[dict(t=0, id='panel')], sfx=[dict(t=r3(t_67 - 0.12), type='pop')],
               thumb=[[r3(t_67 + 0.2), t_c]])
    mk('s1_r0', cfg, fx)


def s1_r2():
    """fv: 'only changing the harness ... took the same model and improved its outputs'. One model (his iris sparkle
    tile) sits in a basic harness (graphite slots, dashed frame) with a low ember output meter. On "changing the
    harness" the harness morphs: the graphite slots flip to his Configure / Build / Checks / Memory tiles, the wires
    and frame light azure. The model never moves (a white pulse on "same model"). On "improved" the meter jumps to mint."""
    r, ws = words('s1', 2)
    fx = FX()
    t_ch, t_h, t_same, t_imp = W(ws, 'changing'), W(ws, 'harness'), W(ws, 'same'), W(ws, 'improved')
    HW_, HH_, HX, HY = 840, 760, 540, 520
    MC = (420, 352)                               # model centre in the harness card
    slots = [(64, 104, 'azure', 'code'), (656, 104, 'iris', 'bolt'), (64, 548, 'mint', 'check'), (656, 548, 'ember', 'bars')]
    SZ = 120
    wires_a = ''.join(f'<line x1="{x + SZ / 2}" y1="{y + SZ / 2}" x2="{MC[0]}" y2="{MC[1]}" stroke="rgba(255,255,255,.16)" stroke-width="3" stroke-dasharray="10 10"/>'
                      for x, y, *_ in slots)
    wires_b = ''.join(f'<line x1="{x + SZ / 2}" y1="{y + SZ / 2}" x2="{MC[0]}" y2="{MC[1]}" stroke="#2F95FF" stroke-width="4" stroke-linecap="round"/>'
                      for x, y, *_ in slots)
    old = ''.join(tile('lockd', g, SZ, -6 if i % 2 else 6, id=f'old{i}', style=f'left:{x}px;top:{y}px') for i, (x, y, c, g) in enumerate(slots))
    new = ''.join(tile(c, g, SZ, -6 if i % 2 else 6, id=f'new{i}', style=f'left:{x}px;top:{y}px;opacity:0') for i, (x, y, c, g) in enumerate(slots))
    MS = 230
    hcard = (f'<svg class="abs" style="left:0;top:0;width:{HW_}px;height:{HH_}px;overflow:visible">{wires_a}</svg>'
             f'<svg id="wb" class="abs" style="left:0;top:0;width:{HW_}px;height:{HH_}px;overflow:visible;opacity:0;'
             f'filter:drop-shadow(0 0 10px rgba(47,149,255,.8))">{wires_b}</svg>'
             f'<div id="hdash" class="abs" style="left:16px;top:16px;right:16px;bottom:16px;border-radius:24px;border:2px dashed rgba(255,255,255,.16)"></div>'
             f'<div class="abs lab" style="left:{MC[0] - 150}px;top:48px;width:300px;text-align:center">Harness</div>'
             + old + new +
             f'<div id="mglow" class="abs" style="left:{MC[0] - 210}px;top:{MC[1] - 210}px;width:420px;height:420px;border-radius:50%;'
             f'background:radial-gradient(closest-side,rgba(156,124,255,.38),rgba(156,124,255,0));opacity:.7"></div>'
             + tile('iris', 'sparkle', MS, -6, id='model', style=f'left:{MC[0] - MS / 2}px;top:{MC[1] - MS / 2}px') +
             f'<div id="mring" class="abs" style="left:{MC[0] - MS / 2 - 22}px;top:{MC[1] - MS / 2 - 22}px;width:{MS + 44}px;height:{MS + 44}px;'
             f'border-radius:76px;border:4px solid #fff;box-shadow:0 0 34px rgba(255,255,255,.55);opacity:0"></div>'
             f'<div class="abs lab wh" style="left:{MC[0] - 150}px;top:{MC[1] + MS / 2 + 34}px;width:300px;text-align:center">Model</div>'
             + ring('hring', 32, AZ, 'rgba(47,149,255,.30)', 3))
    MW_, MH_, MY = 840, 230, 1055
    TW_ = 640
    meter = (f'<div class="abs lab" style="left:48px;top:38px">Output</div>'
             f'<div class="abs" style="left:48px;top:112px;width:{TW_}px;height:48px;border-radius:24px;background:rgba(255,255,255,.06);'
             f'box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)"></div>'
             f'<div id="mfe" class="abs" style="left:48px;top:112px;width:0;height:48px;border-radius:24px;background:linear-gradient(90deg,#FF6F3C,#FF9A6E);'
             f'box-shadow:0 0 22px rgba(255,138,91,.5)"></div>'
             f'<div id="mfm" class="abs" style="left:48px;top:112px;width:0;height:48px;border-radius:24px;opacity:0;'
             f'background:linear-gradient(90deg,#1CA271,#5AD9A6 60%,#B8F4DA);box-shadow:0 0 30px rgba(79,214,160,.7)"></div>'
             + tile('mint', 'check', 72, 0, id='mok', style=f'left:{48 + TW_ + 26}px;top:100px;opacity:0'))
    cards = [dict(id='h', kind='glass', x=HX, y=HY, w=HW_, h=HH_, html=hcard),
             dict(id='m', kind='glass', x=540, y=MY, w=MW_, h=MH_, html=meter)]
    fx.k('mfe', (0.3, dict(w=0)), (1.15, dict(w=TW_ * 0.28), 'power2.out'))
    for i in range(4):
        a = t_ch - 0.12 + 0.13 * i
        fx.k(f'old{i}', (a, dict(o=1, s=1)), (a + 0.24, dict(o=0, s=0.55), 'power2.in'))
        fx.k(f'new{i}', (a + 0.16, dict(o=0, s=0.5)), (a + 0.62, dict(o=1, s=1), 'back.out(2.2)'))
    fx.k('hdash', (t_h - 0.2, dict(o=1)), (t_h + 0.25, dict(o=0)))
    fx.k('wb', (t_h - 0.15, dict(o=0)), (t_h + 0.35, dict(o=1), 'power2.out'))
    fx.k('hring', (t_h - 0.1, dict(o=0)), (t_h + 0.45, dict(o=1)))
    fx.k('mring', (t_same - 0.1, dict(o=0, s=1.08)), (t_same + 0.22, dict(o=1, s=1), 'power2.out'), (t_same + 0.85, dict(o=0, s=1.0)))
    fx.k('model', (t_same - 0.05, dict(s=1)), (t_same + 0.15, dict(s=1.06), 'power2.out'), (t_same + 0.5, dict(s=1), 'back.out(2)'))
    fx.k('mfe', (t_imp - 0.06, dict(o=1)), (t_imp + 0.3, dict(o=0)))
    fx.k('mfm', (t_imp - 0.08, dict(o=0, w=TW_ * 0.28)), (t_imp + 0.06, dict(o=1), 'linear'), (t_imp + 0.75, dict(w=TW_ * 0.88), 'power3.out'))
    fx.k('mok', (t_imp + 0.42, dict(o=0, s=0.4)), (t_imp + 0.8, dict(o=1, s=1), 'back.out(2.4)'))
    # bottom edge pinned at screen y 1225 while the camera pushes (cam.y = 1170 - 505 / s)
    cy = lambda s: r3(1170 - 505 / s)
    moves = [dict(t=0.2, dur=r3(t_ch - 0.5), kind='glide', to=dict(x=540, y=cy(1.02), s=1.02)),
             dict(t=r3(t_ch - 0.3), dur=1.4, kind='push', to=dict(x=540, y=cy(1.08), s=1.08)),
             dict(t=r3(t_ch + 1.2), dur=r3(r['dur'] - t_ch - 1.2), kind='glide', to=dict(x=540, y=cy(1.1), s=1.1))]
    cfg = dict(id='s1_r2', dur=r['dur'], mode='fv', cam0=dict(x=540, y=cy(1.0), s=1.0), cards=cards, moves=moves, pushRef=1.2,
               heroes=[dict(t=0, id='none')], sfx=[dict(t=r3(t_ch + 0.05), type='pop'), dict(t=r3(t_imp + 0.05), type='chime')],
               thumb=[[r3(t_imp + 0.85), r['dur']]])
    mk('s1_r2', cfg, fx)


def s1_r3():
    """split: 'LangChain did this experiment a while back where they took GPT-5.2'. Frame 0 = the real LangChain blog post
    (tags, title, author + date) in a white browser window, camera pushed in; LangChain's logo lands above it on
    "LangChain" while the camera pulls back; the model chip (OpenAI mark, GPT-5.2-Codex, the model the post names)
    lands on "GPT-5.2"."""
    r, ws = words('s1', 3)
    fx = FX()
    t_lc, t_gpt = W(ws, 'langchain'), W(ws, 'gpt5.2')
    fw, fh = D['a_lc_head.png']
    BW = 1000; k = BW / fw; BH_img = round(fh * k); HB = 76
    BY0 = 364; BH = HB + BH_img; BY = BY0 + BH / 2
    dots = ''.join(f'<div class="abs" style="left:{30 + 30 * i}px;top:30px;width:16px;height:16px;border-radius:50%;background:#D7D9DE"></div>' for i in range(3))
    head = (dots + f'<div class="abs" style="left:136px;top:14px;width:{BW - 172}px;height:48px;border-radius:24px;background:{PAPER2}"></div>'
            f'<div class="abs m" style="left:164px;top:18px;font-size:30px;line-height:40px;color:{INK2};white-space:nowrap">langchain.com/blog</div>'
            f'<div class="abs" style="left:0;top:{HB}px;width:100%;height:1.5px;background:{PLINE}"></div>')
    bhtml = head + f'<img src="{A}a_lc_head.png" class="abs" style="left:0;top:{HB}px;width:{BW}px;height:{BH_img}px">'
    lw, lh = D['a_langchain_wm.png']; LW = 640; LH = round(lh * LW / lw)
    CW_, CH_, CY = 720, 170, 800
    chip = (img(A + 'a_openai_ink.png', 100, 100, 'left:42px;top:35px') +
            f'<div class="abs lab ink2" style="left:172px;top:28px">Model</div>'
            f'<div class="abs" style="left:170px;top:66px;font:600 68px/1.1 Figtree;letter-spacing:-.025em;color:{INK};white-space:nowrap">GPT-5.2-Codex</div>')
    cards = [dict(id='logo', kind='logo', x=540, y=r3(BY0 - 50 - LH / 2), w=LW, h=LH, html=logo_html(A + 'a_langchain_wm.png'),
                  land=dict(t=r3(t_lc - 0.12), dur=0.55)),
             dict(id='blog', kind='window', x=540, y=BY, w=BW, h=BH, html=bhtml),
             dict(id='chip', kind='paper', x=540, y=CY, w=CW_, h=CH_, html=chip, land=dict(t=r3(t_gpt - 0.12), dur=0.55))]
    moves = [dict(t=r3(t_lc - 0.3), dur=1.1, kind='pull', to=dict(x=540, y=470, s=1.0)),
             dict(t=r3(t_lc + 0.85), dur=r3(r['dur'] - t_lc - 0.85), kind='glide', to=dict(x=540, y=476, s=1.025))]
    cfg = dict(id='s1_r3', dur=r['dur'], mode='split', cam0=dict(x=540, y=BY, s=1.06), cards=cards, moves=moves, pushRef=1.2,
               heroes=[dict(t=0, id='blog')], sfx=[dict(t=r3(t_gpt - 0.12), type='pop')],
               thumb=[[r3(t_gpt + 0.5), r['dur']]])
    mk('s1_r3', cfg, fx)


def s1_r5():
    """fv: 'and they actually managed to get better results out of the model'. The real LangChain post in the capture
    frame: the deepagents-cli result paragraph; the inner camera pushes onto it on "managed", a marker band sweeps
    "13.7 points from 52.8 to 66.5" on "better", a second "kept the model fixed, gpt-5.2-codex" on "model"."""
    r, ws = words('s1', 5)
    fw, fh = D['a_lc_page.png']
    t_man, t_bet, t_mod = W(ws, 'managed'), W(ws, 'better'), W(ws, 'model')
    bands = band('hlA', 726, 2170, 594, 64) + band('hlB', 934, 2228, 636, 64)
    v0 = view(fw, fh, 0.72, fx=1440, fy=2330)
    v1 = view(fw, fh, 0.95, left=706, fy=2236)
    v2 = view(fw, fh, 0.98, left=706, fy=2236)
    cap = capture_card('cap', fw, fh, img=A + 'a_lc_page.png', overlay=bands, overlayBlend='multiply', inner0=v0,
                       inner=[dict(t=r3(t_man - 0.25), dur=0.65, **v1),
                              dict(t=r3(t_man + 0.45), dur=r3(r['dur'] - t_man - 0.45), ease='sine.inOut', **v2)])
    cfg = dict(id='s1_r5', dur=r['dur'], mode='fv', cam0=dict(x=540, y=720, s=1.0), cards=[cap], moves=[], heroes=[dict(t=0, id='cap')],
               wave=dict(level='low', k=0.6),
               reveals=[dict(el='hlA', t=r3(t_bet - 0.08), dur=0.5, type='scaleX'), dict(el='hlB', t=r3(t_mod - 0.12), dur=0.45, type='scaleX')],
               sfx=[])
    mk('s1_r5', cfg, None, backdrop=('img', A + 'a_lc_page.png', fw, fh))


def s1_r7():
    """split: 'from a 53% roundabout to about 66%'. LangChain's real Terminal Bench 2.0 result at true scale on a
    highlighted glass chart, same model (GPT-5.2-Codex) in the header: the before column rises to 52.8 % (graphite)
    on "53%", a dashed line holds that level; the after column rises past it to 66.5 % (azure, glowing) on "66%",
    the +13.7 gain lights mint, ranks Top 30 -> Top 5."""
    r, ws = words('s1', 7)
    fx = FX()
    PW, PH = 1000, 820
    BASE, SC = 700, 440                           # baseline y, px per 100 %
    C1, C2, CW = 360, 700, 230
    h1, h2 = SC * 0.528, SC * 0.665
    t_53, t_to, t_66 = W(ws, '53'), W(ws, 'to', 2), W(ws, '66.')
    grid = ''.join(f'<div class="abs" style="left:200px;top:{BASE - SC * p / 100}px;width:740px;height:1px;background:rgba(255,255,255,{.07 if p else .18})"></div>'
                   f'<div class="abs m" style="left:84px;top:{BASE - SC * p / 100 - 18}px;width:96px;text-align:right;font-size:30px;line-height:36px;color:{TM}">{p}</div>'
                   for p in (0, 25, 50, 75, 100))
    slot = lambda cx: (f'<div class="abs" style="left:{cx - CW / 2}px;top:{BASE - SC}px;width:{CW}px;height:{SC}px;border-radius:18px 18px 0 0;'
                       f'background:rgba(255,255,255,.035)"></div>')
    col = lambda cid, cx, bg, glow, vid, vcol, vglow: (
        f'<div id="{cid}" class="abs" style="left:{cx - CW / 2}px;bottom:{PH - BASE}px;width:{CW}px;height:0;border-radius:18px 18px 4px 4px;'
        f'background:{bg};box-shadow:{glow};overflow:visible">'
        f'<div id="{vid}w" class="abs" style="left:-60px;top:-104px;width:{CW + 120}px;text-align:center;opacity:0">'
        f'<span id="{vid}" style="font:600 82px/1 Figtree;letter-spacing:-.03em;color:{vcol};text-shadow:{vglow}">0.0%</span></div></div>')
    html = (img(A + 'a_openai_white.png', 62, 62, 'left:52px;top:46px') +
            f'<div class="abs" style="left:132px;top:40px;font:600 56px/1.1 Figtree;letter-spacing:-.025em;color:#fff;white-space:nowrap">GPT-5.2-Codex</div>'
            f'<div class="abs lab acc" style="left:54px;top:122px">Terminal Bench 2.0</div>'
            + img(A + 'a_langchain_wm.png', 250, 46, 'right:52px;top:60px') +
            f'<div class="abs" style="left:52px;top:186px;width:{PW - 104}px;height:1px;background:{HAIR}"></div>'
            + grid + slot(C1) + slot(C2) +
            col('c1', C1, 'linear-gradient(180deg,#6A6D75,#4A4D54)', 'inset 0 1px 0 rgba(255,255,255,.18)', 'v1', '#E6E7EA', 'none') +
            col('c2', C2, 'linear-gradient(180deg,#7DC0FF,#2F95FF 45%,#1B63E6)', '0 0 50px rgba(47,149,255,.55),inset 0 2px 0 rgba(255,255,255,.4)',
                'v2', '#fff', '0 0 40px rgba(47,149,255,.8)') +
            f'<div id="ref" class="abs" style="left:{C1 - CW / 2}px;top:{BASE - h1 - 1.5}px;width:{C2 + CW / 2 - (C1 - CW / 2)}px;height:0;'
            f'border-top:3px dashed rgba(255,255,255,.42);opacity:0"></div>'
            f'<div id="gain" class="abs m" style="left:{C2 + CW / 2 + 16}px;top:{BASE - (h1 + h2) / 2 - 20}px;font-size:34px;line-height:40px;'
            f'font-weight:600;color:{MINT};text-shadow:0 0 18px rgba(79,214,160,.6);opacity:0">+13.7</div>'
            f'<div id="gbar" class="abs" style="left:{C2 + CW / 2 + 4}px;top:{BASE - h2}px;width:4px;height:{h2 - h1}px;border-radius:2px;'
            f'background:{MINT};box-shadow:0 0 14px rgba(79,214,160,.7);opacity:0"></div>'
            f'<div class="abs lab" style="left:{C1 - 160}px;top:722px;width:320px;text-align:center">Before</div>'
            f'<div class="abs lab wh" style="left:{C2 - 160}px;top:722px;width:320px;text-align:center">After</div>'
            f'<div class="abs lab" style="left:{C1 - 160}px;top:764px;width:320px;text-align:center">Top 30</div>'
            f'<div id="rk2" class="abs lab acc" style="left:{C2 - 160}px;top:764px;width:320px;text-align:center">Top 5</div>'
            + ring('cring', 32, 'rgba(47,149,255,.55)', 'rgba(47,149,255,.12)', 2, 1))
    cards = [dict(id='chart', kind='glass', highlight=True, x=540, y=470, w=PW, h=PH, html=html)]
    a1, a2 = t_53 - 0.55, t_to - 0.05
    fx.k('c1', (a1, dict(h=0)), (t_53 + 0.12, dict(h=h1), 'power2.out'))
    fx.k('v1w', (a1, dict(o=0)), (a1 + 0.2, dict(o=1)))
    fx.number('v1', [(a1, 0), (t_53 + 0.12, 52.8, 'power2.out')], fmt='1f', suf='%')
    fx.k('ref', (t_53 + 0.2, dict(o=0)), (t_53 + 0.55, dict(o=1)))
    fx.k('c2', (a2, dict(h=0)), (t_66 + 0.05, dict(h=h2), 'power2.inOut'))
    fx.k('v2w', (a2, dict(o=0)), (a2 + 0.2, dict(o=1)))
    fx.number('v2', [(a2, 0), (t_66 + 0.05, 66.5, 'power2.inOut')], fmt='1f', suf='%')
    fx.k('gbar', (t_66 + 0.05, dict(o=0)), (t_66 + 0.35, dict(o=1)))
    fx.k('gain', (t_66 + 0.1, dict(o=0, x=-10)), (t_66 + 0.42, dict(o=1, x=0), 'power2.out'))
    fx.k('rk2', (t_66, dict(s=1)), (t_66 + 0.16, dict(s=1.12), 'power2.out'), (t_66 + 0.5, dict(s=1), 'back.out(2)'))
    moves = [dict(t=0.15, dur=r3(r['dur'] - 0.15), kind='glide', to=dict(x=540, y=462, s=1.025))]
    cfg = dict(id='s1_r7', dur=r['dur'], mode='split', cam0=dict(x=540, y=470, s=1.0), cards=cards, moves=moves, pushRef=1.1,
               heroes=[dict(t=0, id='chart')], sfx=[dict(t=r3(t_66 + 0.08), type='chime')],
               thumb=[[r3(t_66 + 0.55), r['dur']]])
    mk('s1_r7', cfg, fx)


def s1_r8():
    """fv: 'this really popular post on X from Can Bölük'. The X article exactly as Leon had it open (6.mkv, final 9:19)
    in the capture frame: the whole post at frame 0; the inner camera moves to the engagement row on "popular" (band:
    101 replies, 237 reposts, 1.6K likes, 353K views), to the author on "Can Bölük" (band on the name), and an azure
    outline draws round the cover's "The Harness Is the Bottleneck." on "sorry" - the next (full-cam) line quotes it."""
    r, ws = words('s1', 8)
    fw, fh = D['a_x_post.png']
    t_pop, t_can, t_sorry = W(ws, 'popular'), W(ws, 'can'), W(ws, 'sorry')
    bands = (band('hlP', 38, 1418, 1284, 92, 'bandd') + band('hlN', 172, 146, 300, 66, 'bandd') +
             band('hlB', 124, 366, 412, 246, 'ringd'))
    v0 = view(fw, fh, 0.62, fx=fw / 2, fy=860)
    v1 = view(fw, fh, 0.78, fx=700, fy=1190)
    v2 = view(fw, fh, 1.0, fx=600, fy=560)
    v3 = view(fw, fh, 0.72, fx=748, fy=800)
    cap = capture_card('cap', fw, fh, img=A + 'a_x_post.png', overlay=bands, inner0=v0,
                       inner=[dict(t=r3(t_pop - 0.3), dur=0.6, **v1),
                              dict(t=r3(t_can - 0.32), dur=0.62, **v2),
                              dict(t=r3(t_sorry - 0.2), dur=1.0, ease='sine.inOut', **v3)])
    cap['bg'] = '#000'
    cfg = dict(id='s1_r8', dur=r['dur'], mode='fv', cam0=dict(x=540, y=720, s=1.0), cards=[cap], moves=[], heroes=[dict(t=0, id='cap')],
               wave=dict(level='low', k=0.6),
               reveals=[dict(el='hlP', t=r3(t_pop + 0.05), dur=0.5, type='scaleX'), dict(el='hlN', t=r3(t_can + 0.05), dur=0.4, type='scaleX'),
                        dict(el='hlB', t=r3(t_sorry - 0.05), dur=0.5, type='scaleX')],
               sfx=[], thumb=[[r3(t_sorry + 0.85), r['dur']]])
    mk('s1_r8', cfg, None, backdrop=('img', A + 'a_x_post.png', fw, fh))


# ================================================================================================= SHORT s5
def s5_r0():
    """split hook (cover-safe): the real cubefarm 3D office (8.mkv 41.3-44.0, the walk in) in a media card. Frame 0:
    the card's top below the cover title (y 640); on "agent" the camera steps up and the card lands (bottom 890); his
    mint Orchestrate tile + "cubefarm" (level 3 in the long-form) settles above it."""
    r, ws = words('s5', 0)
    fx = FX()
    fw, fh = D['a_s5_r0.mp4']
    CW_ = 1040; CH_ = round(fh * CW_ / fw)
    CY = 890 - CH_ / 2
    t_ag = W(ws, 'agent')
    lock = (tile('mint', 'eyes', 70, -8, antenna=True, style='left:0;top:6px') +
            f'<div class="abs" style="left:96px;top:4px;font:600 66px/1.1 Figtree;letter-spacing:-.03em;color:#fff;white-space:nowrap">cubefarm</div>')
    cards = [dict(id='vid', kind='media', x=540, y=CY, w=CW_, h=CH_, bg='#d9c3a5', fw=fw, fh=fh, inner0=dict(fx=fw / 2, fy=fh / 2, k=CW_ / fw)),
             dict(id='lock', kind='plain', x=540, y=CY - CH_ / 2 - 66, w=380, h=84, html=lock, clip=False, noDof=True,
                  land=dict(t=r3(t_ag + 0.35), dur=0.55))]
    cards[0]['inner'] = []
    t_s = t_ag - 0.25
    cam_land = dict(x=540, y=470, s=1.0)
    cy0 = CY - (640 + CH_ / 2 - 470)
    moves = [dict(t=r3(t_s), dur=0.55, kind='step', to=cam_land),
             dict(t=r3(t_s + 0.6), dur=r3(r['dur'] - t_s - 0.6), kind='glide', to=dict(x=540, y=478, s=1.02))]
    cfg = dict(id='s5_r0', dur=r['dur'], mode='split', cam0=dict(x=540, y=r3(cy0), s=1.0), cards=cards, moves=moves, pushRef=1.0,
               heroes=[dict(t=0, id='vid')], sfx=[], thumb=[[r3(t_ag + 0.95), r['dur']]])
    mk('s5_r0', cfg, fx, videos=[('vid', A + 'a_s5_r0.mp4', fw, fh)])


def s5_r1():
    """fv: 'my coding agent swarm represented in 3D space ... these guys are working on an actual project'. The synced
    cubefarm footage (8.mkv 44.0-51.6: walking the floor past Guido, Radia #297, to Margaret #294 with her git log) in
    the capture frame; the inner camera glides with the walk, pulls wide on "3D space", pushes onto Margaret at her
    desk on "working on an actual project"."""
    r, ws = words('s5', 1)
    fw, fh = D['a_s5_r1.mp4']
    t_3d, t_work, t_proj = W(ws, '3d'), W(ws, 'working'), W(ws, 'project.')
    v0 = view(fw, fh, 0.9, fx=1020, fy=640)
    v1 = view(fw, fh, 0.86, fx=900, fy=650)
    v2 = view(fw, fh, 0.80, fx=931, fy=648)
    v3 = view(fw, fh, 1.12, fx=1240, fy=560)
    v4 = view(fw, fh, 1.15, fx=1220, fy=575)
    cap = capture_card('cap', fw, fh, inner0=v0,
                       inner=[dict(t=0.15, dur=r3(t_3d - 0.6), ease='sine.inOut', **v1),
                              dict(t=r3(t_3d - 0.3), dur=0.9, **v2),
                              dict(t=r3(t_work - 0.2), dur=0.95, **v3),
                              dict(t=r3(t_work + 0.8), dur=r3(r['dur'] - t_work - 0.8), ease='sine.inOut', **v4)])
    cfg = dict(id='s5_r1', dur=r['dur'], mode='fv', cam0=dict(x=540, y=720, s=1.0), cards=[cap], moves=[], heroes=[dict(t=0, id='cap')],
               wave=dict(level='low', k=0.6), sfx=[], thumb=[[r3(t_work + 0.8), r['dur']]])
    mk('s5_r1', cfg, None, videos=[('cap', A + 'a_s5_r1.mp4', fw, fh)], backdrop=('video', A + 'a_s5_r1_bd.mp4', fw, fh))


def s5_r2():
    """split: 'Each of these agents are running a coding harness.' Margaret coding at her desk (synced 8.mkv 60.8-63.9)
    in a media card; the three harnesses cubefarm agents run (README: Claude Code, Codex or OpenCode) land beneath it as
    glass chips with their official logos on "running a coding harness"."""
    r, ws = words('s5', 2)
    fx = FX()
    fw, fh = D['a_s5_r2.mp4']
    CW_ = 960; CH_ = round(fh * CW_ / fw)
    VY = 40 + 16 + CH_ / 2
    t_run = W(ws, 'running')
    chip = lambda icon, name: (f'<div class="abs" style="inset:0;display:flex;align-items:center;justify-content:center;gap:18px">{icon}'
                               f'<div style="font:600 42px/1 Figtree;letter-spacing:-.02em;color:#fff;white-space:nowrap">{name}</div></div>')
    specs = [('cc', 'Claude Code', f'<img src="{A}a_claude.png" style="width:60px;height:60px">', 380),
             ('cx', 'Codex', f'<img src="{A}a_codex.png" style="width:66px;height:66px;border-radius:15px">', 270),
             ('oc', 'OpenCode', f'<img src="{A}a_opencode.png" style="width:50px;height:62px">', 330)]
    gap = 18; tot = sum(s[3] for s in specs) + gap * 2; x = 540 - tot / 2
    cards = [dict(id='vid', kind='media', x=540, y=VY, w=CW_, h=CH_, bg='#d9c3a5', fw=fw, fh=fh, inner0=dict(fx=fw / 2, fy=fh / 2, k=CW_ / fw), inner=[])]
    sfx = []
    for i, (cid, name, icon, w) in enumerate(specs):
        tl = t_run - 0.1 + 0.3 * i
        cards.append(dict(id=cid, kind='glass', x=x + w / 2, y=820, w=w, h=124, html=chip(icon, name), radius=30, noDof=True,
                          land=dict(t=r3(tl), dur=0.5)))
        sfx.append(dict(t=r3(tl), type='pop'))
        x += w + gap
    moves = [dict(t=0.1, dur=r3(r['dur'] - 0.1), kind='glide', to=dict(x=540, y=474, s=1.02))]
    cfg = dict(id='s5_r2', dur=r['dur'], mode='split', cam0=dict(x=540, y=470, s=1.0), cards=cards, moves=moves, pushRef=1.0,
               heroes=[dict(t=0, id='vid')], sfx=sfx, thumb=[[r3(t_run + 1.15), r['dur']]])
    mk('s5_r2', cfg, fx, videos=[('vid', A + 'a_s5_r2.mp4', fw, fh)])


def s5_r3():
    """fv: 'this could be Claude Code, it could be Codex. If I run to any of these monitors, I can actually see ... this
    guy is actually running Claude Opus.' Synced cubefarm footage (8.mkv 64.3-72.6): Claude Code and Codex glass chips
    land over the footage on their names; the inner camera pushes onto Margaret's monitor on "monitors"; her terminal
    opens (real); the camera frames its header and pushes onto "claude-opus-5-5 · high effort", marker band on "Claude"."""
    r, ws = words('s5', 3)
    fx = FX()
    fw, fh = D['a_s5_r3.mp4']
    t_cc, t_cx, t_mon, t_see, t_opus = W(ws, 'claude'), W(ws, 'codex.'), W(ws, 'monitors'), W(ws, 'see'), W(ws, 'claude', 2)
    t_run = W(ws, 'run')
    v0 = view(fw, fh, 0.70, fx=1250, fy=720)
    v1 = view(fw, fh, 0.73, fx=1380, fy=760)
    v2 = view(fw, fh, 0.98, fx=1340, fy=700)
    v3 = view(fw, fh, 0.76, fx=1000, fy=690)
    v4 = view(fw, fh, 1.08, fx=1880, fy=400)
    cap = capture_card('cap', fw, fh, inner0=v0,
                       inner=[dict(t=0.1, dur=r3(t_run - 0.5), ease='sine.inOut', **v1),
                              dict(t=r3(t_run - 0.25), dur=0.8, **v2),
                              dict(t=r3(t_see - 0.45), dur=0.7, **v3),
                              dict(t=r3(t_opus - 0.6), dur=0.6, **v4)])
    chips = (gchip('gcc', 104, 1062, 470, 126, f'<img src="{A}a_claude.png" style="width:72px;height:72px">', 'Claude Code') +
             gchip('gcx', 600, 1062, 330, 126, f'<img src="{A}a_codex.png" style="width:78px;height:78px;border-radius:18px">', 'Codex'))
    land(fx, 'gcc', t_cc - 0.12); land(fx, 'gcx', t_cx - 0.12)
    for el in ('gcc', 'gcx'): leave(fx, el, t_run - 0.2)
    cfg = dict(id='s5_r3', dur=r['dur'], mode='fv', cam0=dict(x=540, y=720, s=1.0), cards=[cap], moves=[], heroes=[dict(t=0, id='cap')],
               wave=dict(level='low', k=0.6),
               sfx=[dict(t=r3(t_cc - 0.12), type='pop'), dict(t=r3(t_cx - 0.12), type='pop')],
               thumb=[[r3(t_opus + 0.45), r['dur']]])
    mk('s5_r3', cfg, fx, extra_html=chips, videos=[('cap', A + 'a_s5_r3.mp4', fw, fh)], backdrop=('video', A + 'a_s5_r3_bd.mp4', fw, fh))


def s5_r5():
    """fv: 'this also uses the Kanban board. And these are hooked up to actual GitHub issues.' Synced footage (8.mkv
    81.9-88.1): the 3D whiteboard, then the full-screen Kanban board; the GitHub mark lands on "GitHub", the inner
    camera pushes onto In progress and a band marks issue #294 on "issues"."""
    r, ws = words('s5', 5)
    fx = FX()
    fw, fh = D['a_s5_r5.mp4']
    t_kb, t_gh, t_iss = W(ws, 'kanban'), W(ws, 'github'), W(ws, 'issues.')
    v0 = view(fw, fh, 0.74, fx=1220, fy=700)
    v1 = view(fw, fh, 0.80, fx=1280, fy=560)
    v2 = view(fw, fh, 0.78, fx=1000, fy=650)
    v3 = view(fw, fh, 1.25, fx=760, fy=420)
    cap = capture_card('cap', fw, fh, inner0=v0,
                       inner=[dict(t=r3(t_kb - 0.3), dur=0.7, **v1),
                              dict(t=2.62, dur=0.6, **v2),
                              dict(t=r3(t_gh - 0.35), dur=0.75, **v3)])
    over = vov('cap', fw, fh, band('hl294', 716, 378, 356, 104))
    chip = gchip('ggh', 640, 1078, 360, 126, f'<img src="{A}a_github_white.png" style="width:70px;height:68px">', 'GitHub')
    land(fx, 'ggh', t_gh - 0.12)
    cfg = dict(id='s5_r5', dur=r['dur'], mode='fv', cam0=dict(x=540, y=720, s=1.0), cards=[cap], moves=[], heroes=[dict(t=0, id='cap')],
               wave=dict(level='low', k=0.6), vov=[dict(card='cap', el='vo-cap')],
               reveals=[dict(el='hl294', t=r3(t_iss - 0.1), dur=0.5, type='scaleX')],
               sfx=[dict(t=r3(t_gh - 0.12), type='pop')], thumb=[[r3(t_iss + 0.45), r['dur']]])
    mk('s5_r5', cfg, fx, extra_html=over + chip, videos=[('cap', A + 'a_s5_r5.mp4', fw, fh)], backdrop=('video', A + 'a_s5_r5_bd.mp4', fw, fh))


def s5_r6():
    """split: 'when I click on any of these, we can actually jump to the actual pull request sitting on GitHub.' The real
    Kanban board (In QA) with Leon's own cursor moving onto "PR #300" and clicking it (8.mkv 89.8-90.8, held); the click
    lands on "click" (band on the link); a whip on "jump" to the real PR page (8.mkv 94.3: #300, Open), bands on its
    title on "pull request", an azure outline on GitHub's own header on "GitHub"."""
    r, ws = words('s5', 6)
    fx = FX()
    bw, bh = D['a_s5_r6_board.mp4']
    pw, ph = D['a_s5_pr.png']
    t_click, t_jump, t_pull, t_gh = W(ws, 'click'), W(ws, 'jump'), W(ws, 'pull'), W(ws, 'github.')
    BW_ = 1000; BH_ = round(bh * BW_ / bw)
    PW_ = 1000; PH_ = round(ph * PW_ / pw)
    PX = 1940
    pr_ov = (band('hlT1', 44, 214, 1392, 62, 'bandd') + band('hlT2', 44, 284, 816, 66, 'bandd') + band('hlG', 90, 16, 368, 80, 'ringd'))
    cards = [dict(id='board', kind='media', x=540, y=470, w=BW_, h=BH_, bg='#FFFDF6', fw=bw, fh=bh, inner0=dict(fx=bw / 2, fy=bh / 2, k=BW_ / bw), inner=[]),
             dict(id='pr', kind='media', x=PX, y=470, w=PW_, h=PH_, bg='#0D1117', img=A + 'a_s5_pr.png', fw=pw, fh=ph,
                  inner0=dict(fx=pw / 2, fy=ph / 2, k=PW_ / pw), inner=[], overlay=pr_ov)]
    over = vov('board', bw, bh, band('hlL', 518, 176, 158, 50))
    t_click_real = 1.0                       # the click in the footage (8.mkv 90.82) = clip 1.0 s
    t_w = t_jump - 0.3
    moves = [dict(t=0.1, dur=r3(t_w - 0.15), kind='glide', to=dict(x=556, y=458, s=1.035)),
             dict(t=r3(t_w), kind='whip', to=dict(x=PX, y=452, s=1.06), via=dict(x=1240, y=470, s=0.86))]
    cfg = dict(id='s5_r6', dur=r['dur'], mode='split', cam0=dict(x=540, y=470, s=1.0), cards=cards, moves=moves, pushRef=1.2,
               heroes=[dict(t=0, id='board'), dict(t=r3(t_w + 0.45), id='pr')], vov=[dict(card='board', el='vo-board')],
               reveals=[dict(el='hlL', t=r3(t_click_real - 0.02), dur=0.35, type='scaleX'),
                        dict(el='hlT1', t=r3(t_pull - 0.06), dur=0.45, type='scaleX'), dict(el='hlT2', t=r3(t_pull + 0.3), dur=0.4, type='scaleX'),
                        dict(el='hlG', t=r3(t_gh - 0.1), dur=0.4, type='scaleX')],
               sfx=[dict(t=t_click_real, type='click'), dict(t=r3(t_w + 0.45), type='whoosh')],
               thumb=[[r3(t_pull + 0.75), r3(t_gh - 0.12)]])
    mk('s5_r6', cfg, fx, extra_html=over, videos=[('board', A + 'a_s5_r6_board.mp4', bw, bh)])


def build():
    for f in (s1_r0, s1_r2, s1_r3, s1_r5, s1_r7, s1_r8, s5_r0, s5_r1, s5_r2, s5_r3, s5_r5, s5_r6):
        f()
