# Graphics agent B - shorts s2 "30,000 tokens before you type" (s2_r0 r1 r2 r3 r5 r6) and s3 "What an AI agent actually
# is" (s3_r0 r2 r3 r4 r5 r7 r8). Build: $PY scripts/build_gfx.py b      (one or a few: GFX_B=s2_r0,s3_r2 ...)
#
# Leon's "Leon YouTube" design system on the engine's stage theme: graphite stage + wave, explanations on GLASS, real UI
# and pages on white WINDOW / PAPER / capture frames, Figtree 600 + Geist Mono labels, azure accent, ember for limits,
# mint for passes, his glossy icon tiles (Instructions = azure code, Tools = iris bolt, Checks = mint check, Memory =
# ember bars, his iris robot tile with the antenna for "agent"). Patterns copied from the long-form edit (gfx_a.py g04
# model socket / g05 checks terminal, gfx_b.py g15 context budget at true scale / g16 SMOL strip), re-laid out for 9:16.
# Every time-driven thing is a pure function of t (FX keyframe tracks + CUSTOM), so renders are seek-safe.
import os, json
from build_gfx_common import *

ONLY = [s for s in os.environ.get('GFX_B', '').split(',') if s]

WHITE, T2, TM = '#FFFFFF', '#A3A6AD', '#7E818A'
AZ, EMB, MINT, IRIS = '#2F95FF', '#FF8A5B', '#4FD6A0', '#9C7CFF'
INK, INK2, PAPER2, PLINE = '#111214', '#5F636B', '#F3F4F6', '#ECEDF0'
AZINK, AZWASH = '#1560D0', '#E8F2FF'
BAR, HAIR, HAIR2 = '#5A5D64', 'rgba(255,255,255,.09)', 'rgba(255,255,255,.16)'

EXTRA_CSS = """
.abs{position:absolute}
.fx{display:flex;align-items:center}
.m{font-family:'Geist Mono',ui-monospace,monospace;font-weight:500}
.cr{display:inline-block;width:4px;height:1.05em;background:var(--accent);vertical-align:-0.16em;margin-left:2px;border-radius:2px;box-shadow:0 0 12px rgba(47,149,255,.7)}
.lab{font:500 30px/1.2 'Geist Mono';letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);white-space:nowrap}
.lab.acc{color:var(--accent)}.lab.wh{color:#fff}.lab.ember{color:#FF8A5B}.lab.mint{color:#4FD6A0}
.chipd{position:absolute;font:500 30px/46px 'Geist Mono';height:48px;padding:0 14px;border-radius:12px;background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.10);color:#E6E7EA;white-space:nowrap}
.chipd.az{background:rgba(47,149,255,.16);border-color:rgba(47,149,255,.5);color:#CFE7FF}
.tile.sm{box-shadow:inset 0 2px 1px rgba(255,255,255,.55),inset 0 -6px 10px rgba(0,0,0,.2),0 10px 20px -8px rgba(0,0,0,.35)}
.tile .stick{position:absolute;left:50%;border-radius:999px}.tile .ball{position:absolute;left:50%;border-radius:50%}
.tile.iris .stick{background:linear-gradient(180deg,#E2D8FF,#7B57F0)}.tile.iris .ball{background:radial-gradient(circle at 35% 30%,#fff 0%,#D6C8FF 35%,#7B57F0 100%);box-shadow:0 0 14px rgba(156,124,255,.7)}
.tile.mint .stick{background:linear-gradient(180deg,#C4F6DF,#2DB883)}.tile.mint .ball{background:radial-gradient(circle at 35% 30%,#fff 0%,#C4F6DF 35%,#2DB883 100%)}
.cell{position:absolute;border-radius:9px;border:2px dashed rgba(255,255,255,.17);background:rgba(255,255,255,.025)}
.gc{position:absolute;border-radius:10px;box-shadow:inset 0 2px 1px rgba(255,255,255,.45),inset 0 -8px 12px rgba(0,0,0,.22)}
.gc.az{background:linear-gradient(155deg,#8FCBFF 0%,#3B98FF 45%,#1B63E6 100%)}
.gc.ir{background:linear-gradient(155deg,#D6C8FF 0%,#A385FF 45%,#6C46EC 100%)}
.gc.gr{background:linear-gradient(155deg,#E6E7EA 0%,#A3A6AD 55%,#6E717A 100%)}
.spin{border-radius:50%;border:5px solid rgba(47,149,255,.22);border-top-color:#2F95FF}
"""

# ---------------------------------------------------------------------------------------------------------------
# keyframe library (from the long-form gfx_a.py): per-element tracks of o/x/y/s/sx/sy/r/b/w/h, numbers, class toggles,
# typed text; window.CUSTOM(t, cam, helpers) for anything else.
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
  if('dash' in v) el.style.strokeDashoffset=v.dash;
}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function typer(ty,t){
  const el=$(ty.el); if(!el) return;
  const total=ty.segs.reduce((n,s)=>n+s[0].length,0);
  const n=cl(Math.floor((t-ty.t0)*ty.cps+1e-6),0,total);
  let left=n, h='';
  for(const s of ty.segs){ if(left<=0) break; const part=s[0].slice(0,left); left-=part.length;
    h+= s[1]? `<span class="${s[1]}">${esc(part)}</span>` : esc(part); }
  const tEnd=ty.t0+total/ty.cps;
  const cf=ty.caretFrom!=null?ty.caretFrom:ty.t0-0.35, ct=ty.caretTo!=null?ty.caretTo:tEnd+0.9;
  if(ty.caret!==false && t>=cf && t<ct){ const on=(t<tEnd&&t>=ty.t0)||Math.floor((t-cf)*2.2)%2===0; h+=`<span class="cr" style="opacity:${on?1:0}"></span>`; }
  if(el.__h!==h){ el.innerHTML=h; el.__h=h; }
}
function fmt(v,f){ if(f==='pct') return Math.round(v)+'%'; if(f==='k') return Math.round(v)+'K'; if(f==='1f') return v.toFixed(1); return String(Math.round(v)); }
const prev=window.CFG_RENDER;
window.CFG_RENDER=function(t,cam){
  for(const tr of FX.tr){ if(tr.hold===false && t<tr.kf[0][0]) continue; const el=$(tr.el); if(el) apply(el,at(tr.kf,t)); }
  for(const ty of FX.ty) typer(ty,t);
  for(const nu of FX.num){ const el=$(nu.el); if(!el) continue; const v=at(nu.kf.map(k=>[k[0],{v:k[1]},k[2]]),t).v; const s=(nu.pre||'')+fmt(v,nu.fmt)+(nu.suf||''); if(el.textContent!==s) el.textContent=s; }
  for(const c of FX.cls){ const el=$(c.el); if(el) el.classList.toggle(c.cls, t>=c.on && (c.off==null||t<c.off)); }
  if(window.CUSTOM) window.CUSTOM(t,cam,{at,ez,cl,$});
  if(prev) prev(t,cam);
};
})();
"""

DEF = dict(o=1, x=0, y=0, s=1, sx=1, sy=1, r=0, b=0, dash=0)


class FX:
    def __init__(self):
        self.raw = {}; self.ty = []; self.num = []; self.cls = []; self.hold = {}

    def k(self, el, *frames):
        """keyframes (t, {props}) or (t, {props}, ease) - ease of the segment that ENDS at t. Props not set in a frame keep
        their previous keyframe value, so animate independent props on separate nested elements."""
        self.raw.setdefault(el, []).extend(frames)
        return self

    def type(self, el, t0, segs, cps=24, **kw):
        if isinstance(segs, str): segs = [[segs, '']]
        self.ty.append(dict(el=el, t0=round(t0, 3), cps=cps, segs=segs, **kw))

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
        data = dict(tr=tr, ty=self.ty, num=self.num, cls=self.cls)
        return 'window.FX=' + json.dumps(data) + ';\n' + (custom or '') + '\n' + LIB

    def pop(self, el, t, s0=0.5, ease='back.out(2.2)', dur=0.42):
        """an element popping in (opacity + scale) at t"""
        self.k(el, (t, dict(o=0, s=s0)), (t + dur * 0.45, dict(o=1), 'power2.out'), (t + dur, dict(s=1), ease))


def r3(v):
    return round(v, 3)


def sfx(*evs):
    return [dict(t=r3(t), type=k) for t, k in evs]


def mk(rid, cfg, fx=None, custom='', **kw):
    if ONLY and rid not in ONLY: return
    cfg.setdefault('wave', dict(level='low', k=0.9))
    page(rid, cfg, extra_css=EXTRA_CSS, extra_js=(fx or FX()).js(custom), **kw)


# ---------------------------------------------------------------------------------------------------------------
# brand pieces
LINE = {
    'plug': '<path d="M9 3v5M15 3v5M6.5 8h11v3a5.5 5.5 0 01-11 0zM12 16.5V21"/>',
    'cube': '<path d="M12 2.8l8 4.4v9.6l-8 4.4-8-4.4V7.2z"/><path d="M4 7.2l8 4.4 8-4.4M12 11.6v9.6"/>',
    'robot': '<rect x="4" y="7.5" width="16" height="11.5" rx="4"/><path d="M12 7.5V4"/><circle cx="12" cy="3.2" r="1.1"/><path d="M9.3 12v2.4M14.7 12v2.4"/>',
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'x': '<path d="M7 7l10 10M17 7L7 17"/>',
    'file': '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
    'pencil': '<path d="M4 20l1-4.2L15.6 5.2a2 2 0 0 1 2.8 0l.4.4a2 2 0 0 1 0 2.8L8.2 19 4 20z"/>',
    'edit': '<path d="M12 20h8"/><path d="M16.5 3.5a2.1 2.1 0 013 3L7 19l-4 1 1-4z"/>',
    'term': '<path d="M5 8l4 4-4 4M11 17h8"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
    'globe': '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.6 2.4 3.6 5.2 3.6 8.5s-1 6.1-3.6 8.5M12 3.5c-2.6 2.4-3.6 5.2-3.6 8.5s1 6.1 3.6 8.5"/>',
}


def line_ico(name, size, color='#fff', width=2.0, style=''):
    return (f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;flex:none;{style}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{LINE[name]}</svg>')


def tile(color='azure', glyph='code', size=116, tilt=-8, id=None, style='', antenna=False, svg_markup=None, sm=False):
    """the design system's glossy icon tile in a positioned wrapper (#id)"""
    g = svg_markup.format(s=round(size * 0.5)) if svg_markup else None
    h = tile_html(color, glyph, size, tilt, svg=g)
    if sm: h = h.replace('class="tile ', 'class="tile sm ', 1)
    if antenna:
        st, bl = max(4, round(size * 0.075)), round(size * 0.18)
        ant = (f'<span class="stick" style="width:{st}px;height:{round(size * .2)}px;top:{-round(size * .18)}px;margin-left:{-st / 2}px"></span>'
               f'<span class="ball" style="width:{bl}px;height:{bl}px;top:{-round(size * .3)}px;margin-left:{-bl / 2}px"></span>')
        h = h.replace('">', '">' + ant, 1)
    idh = f' id="{id}"' if id else ''
    return f'<div{idh} class="abs" style="width:{size}px;height:{size}px;{style}">{h}</div>'


def line_tile(color, name, size, tilt=-8, id=None, style=''):
    svgm = (f'<svg width="{{s}}" height="{{s}}" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" '
            f'stroke-linecap="round" stroke-linejoin="round">{LINE[name]}</svg>')
    return tile(color, None, size, tilt, id=id, style=style, svg_markup=svgm)


def robot(size, id=None, style='', tilt=-8):
    """Leon's agent tile from his title slide: iris, two eyes, an antenna ball on top"""
    return tile('iris', 'eyes', size, tilt, id=id, style=style, antenna=True)


def harness_tiles(size, gap, id_prefix=None, style=''):
    """his four 'Agent = model + harness' slide tiles as a 2x2 cluster (Instructions, Tools, Checks, Memory)"""
    spec = [('azure', 'code', -8), ('iris', 'bolt', 8), ('mint', 'check', 8), ('ember', 'bars', -8)]
    h = ''
    for i, (c, g, tl) in enumerate(spec):
        x, y = (i % 2) * (size + gap), (i // 2) * (size + gap)
        h += tile(c, g, size, tl, id=f'{id_prefix}{i}' if id_prefix else None, style=f'left:{x}px;top:{y}px', sm=True)
    W2 = 2 * size + gap
    return f'<div class="abs" style="width:{W2}px;height:{W2}px;{style}">{h}</div>'


def img(src, w=None, h=None, style=''):
    wh = (f'width:{w}px;' if w else '') + (f'height:{h}px;' if h else '')
    return f'<img src="{src}" style="{wh}display:block;object-fit:contain;{style}">'


def ring(id, radius, color=AZ, glow='rgba(47,149,255,.55)', width=3, op=0):
    return (f'<div id="{id}" class="abs" style="inset:0;border-radius:{radius}px;box-shadow:inset 0 0 0 {width}px {color},inset 0 0 36px {glow};'
            f'opacity:{op};pointer-events:none"></div>')


def chip_w(text, fs=30):
    return round(len(text) * fs * 0.6 + 30)


def chip_rows(names, maxw, gap=12, rowh=58, fs=30):
    pos, x, y = [], 0, 0
    for n in names:
        w = chip_w(n, fs)
        if x + w > maxw and x > 0: x, y = 0, y + rowh
        pos.append((x, y, w)); x += w + gap
    return pos


GLASS = ('background:rgba(24,25,28,.62);backdrop-filter:blur(24px) saturate(140%);-webkit-backdrop-filter:blur(24px) saturate(140%);'
         'border:1px solid rgba(255,255,255,.09);box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 50px 120px -40px rgba(0,0,0,.85);color:#fff;')


# =============================================================================================================== SHORT 2
# s2_r0 - split hook (cover-safe). Frame 0: the official Claude Code wordmark at y ~760 (the cover title sits above).
# On "single" the camera steps down to the REAL Claude Code CLI (6.mkv, long-form 12:02-12:19) in a window: the empty
# prompt ("Try refactor <filepath>"), "/context" typed (real frames), Spinning..., then the real /context screen; the
# inner camera pulls out to the whole usage grid and pushes onto "36.2k/1m tokens (4%)" on "30,000" (azure outline).
CTX_STATES = ['a', 't1', 't2', 't3', 't4', 't5', 't6', 'sp']


def s2_r0():
    r, ws = words('s2', 0)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    FW_, FH_ = D['b_ctx_c.png']
    WW, WH, HD = 1000, 820, 84
    DY = 1080                                         # the step: frame-0 camera sits DY above the landing camera
    wy = 480 + DY                                     # window centre (world) -> lands at screen 480 (70..890)
    t_step = T('single') - 0.25
    t_type = T('to') - 0.12                           # "/" ... "/context" typed (the real frames)
    seq = [('t1', t_type), ('t2', t_type + 0.17), ('t3', t_type + 0.27), ('t4', t_type + 0.37), ('t5', t_type + 0.51),
           ('t6', t_type + 0.65), ('sp', t_type + 0.83)]
    t_res = T('already') + 0.1                        # the /context result appears
    t_push = T('30000') - 0.45
    ring_x0, ring_x1, ring_y0, ring_y1 = 1270, 1840, 633, 687   # "36.2k/1m tokens (4%)" (measured, F px)
    ov = ''.join(f'<img id="cs_{s}" src="assets/b_ctx_{s}.png" style="position:absolute;left:0;top:0;width:{FW_}px;height:{FH_}px;opacity:{1 if s == "a" else 0}">'
                 for s in CTX_STATES)
    ov += (f'<div id="ctxring" style="position:absolute;left:{ring_x0}px;top:{ring_y0}px;width:{ring_x1 - ring_x0}px;height:{ring_y1 - ring_y0}px;'
           f'border-radius:14px;border:5px solid {AZ};background:rgba(47,149,255,.14);box-shadow:0 0 34px rgba(47,149,255,.75),inset 0 0 22px rgba(47,149,255,.35);'
           f'transform-origin:0 50%;transform:scaleX(0)"></div>')
    # inner camera (F px at the card centre; the white header covers the top HD px of the card)
    v_type = dict(fx=694, fy=612, k=0.72)             # banner + prompt + menu
    v_all = dict(fx=969, fy=760, k=0.55)              # the whole usage grid + "Opus 5.5 / 36.2k/1m tokens"
    v_num = dict(fx=1765, fy=845, k=0.98)             # the right column, 36.2k readable at ~39 px
    term = dict(id='term', kind='media', x=540, y=wy, w=WW, h=WH, radius=24, bg='#0B0B0B', img='assets/b_ctx_c.png', fw=FW_, fh=FH_,
                inner0=v_type, overlay=ov,
                inner=[dict(t=r3(t_res - 0.35), dur=0.55, **v_all), dict(t=r3(t_push), dur=1.3, **v_num)])
    claude = 'assets/b_lf_claude_symbol.png'
    hdr = dict(id='hdr', kind='plain', x=540, y=wy - WH / 2 + HD / 2, w=WW, h=HD, noDof=True, html=(
        f'<div class="abs" style="inset:0;background:#fff;border-radius:24px 24px 0 0;border-bottom:1.5px solid {PLINE}"></div>'
        f'<div class="abs fx" style="left:32px;top:0;height:{HD}px;gap:16px">{img(claude, 44, 44)}'
        f'<div style="font:600 34px/1 Figtree;letter-spacing:-.01em;color:{INK}">Claude Code</div></div>'
        f'<div class="abs m" style="right:28px;top:20px;font-size:30px;line-height:44px;padding:0 16px;border-radius:999px;background:{PAPER2};color:{INK2}">v2.1.296</div>'))
    lg = dict(id='lg', kind='logo', x=540, y=760, w=700, h=round(700 * 358 / 2400), html=logo_html('assets/b_lf_cc_wordmark_ondark.png'))
    # phase switches: the typed states replace each other at their times; the result (base image) shows from t_res
    custom = ('window.CUSTOM=function(t){const S=%s;let cur="a";for(const [s,ts] of S){if(t>=ts)cur=s;}if(t>=%f)cur="";'
              'for(const s of %s){const e=document.getElementById("cs_"+s);const o=(s===cur)?1:0;if(e.__o!==o){e.style.opacity=o;e.__o=o;}}};'
              % (json.dumps([[s, r3(ts)] for s, ts in seq]), t_res, json.dumps(CTX_STATES)))
    moves = [dict(t=r3(t_step), dur=0.55, kind='step', to=dict(x=540, y=470 + DY, s=1.0)),
             dict(t=r3(t_push + 1.35), dur=r3(r['dur'] - t_push - 1.35), kind='glide', to=dict(x=540, y=470 + DY + 3, s=1.02))]
    t_ring = T('30000') + 0.57
    cfg = dict(id='s2_r0', dur=r['dur'], mode='split', cam0=dict(x=540, y=470, s=1.0), cards=[lg, term, hdr], moves=moves, pushRef=1.0,
               heroes=[dict(t=0, id='lg'), dict(t=r3(t_step + 0.05), id='term')],
               reveals=[dict(el='ctxring', t=r3(t_ring), dur=0.55, type='scaleX', ease='power2.inOut')],
               sfx=sfx((t_type, 'key'), (seq[-1][1] - 0.05, 'key')),
               thumb=[[r3(t_ring + 0.6), r['dur']]], wave=dict(level='low', k=0.9))
    mk('s2_r0', cfg, fx, custom)


# s2_r1 - fv, the real Ollama docs "Context length" page in the capture frame: frame 0 shows the page with its llama mark
# and title; the inner camera pushes onto the VRAM defaults; band "4k context" on "tiny", band "< 24 GiB VRAM" on
# "consumer grade hardware".
def s2_r1():
    r, ws = words('s2', 1)
    T = lambda w, n=1: W(ws, w, n)
    fw, fh = D['b_ollama_ctx.png']
    bands = (f'<div id="ob1" class="band" style="position:absolute;left:1206px;top:640px;width:150px;height:54px"></div>'
             f'<div id="ob2" class="band" style="position:absolute;left:1000px;top:640px;width:212px;height:54px"></div>')
    capw, caph = 1032, 1040
    v0 = dict(fx=capw / 2 / 0.62, fy=caph / 2 / 0.62, k=0.62)
    v1 = dict(fx=1196, fy=735, k=1.28)
    v2 = dict(fx=1200, fy=742, k=1.31)
    t_push = T('very') - 0.35
    cap = capture_card('cap', fw, fh, img='assets/b_ollama_ctx.png', overlay=bands, overlayBlend='multiply', inner0=v0,
                       inner=[dict(t=r3(t_push), dur=0.85, **v1), dict(t=r3(t_push + 0.85), dur=r3(r['dur'] - t_push - 0.85), ease='sine.inOut', **v2)])
    cfg = dict(id='s2_r1', dur=r['dur'], mode='fv', cam0=dict(x=540, y=720, s=1), cards=[cap], moves=[], heroes=[dict(t=0, id='cap')],
               reveals=[dict(el='ob1', t=r3(T('tiny') + 0.02), dur=0.5, type='scaleX'),
                        dict(el='ob2', t=r3(T('consumer') - 0.05), dur=0.7, type='scaleX', ease='power2.inOut')],
               sfx=[], wave=dict(level='low', k=0.6))
    mk('s2_r1', cfg, backdrop=('img', 'assets/b_ollama_ctx.png', fw, fh))


# ----- context windows at TRUE scale: one cell = 1K tokens (the /context grid's language). 32K = 4 x 8, 64K = 4 x 16.
def tank_html(rows, cw, chh, gap, pad, prefix, cols=4):
    h = ''
    for rr in range(rows):            # row 0 = bottom
        for c in range(cols):
            x = pad + c * (cw + gap); y = pad + (rows - 1 - rr) * (chh + gap)
            h += f'<div id="{prefix}{rr}_{c}" class="cell" style="left:{x}px;top:{y}px;width:{cw}px;height:{chh}px"></div>'
    return h


def tank_size(rows, cw, chh, gap, pad, cols=4):
    return 2 * pad + cols * (cw + gap) - gap, 2 * pad + rows * (chh + gap) - gap


# s2_r2 - split: the 32K window (frame 0, pushed in) gets its "32K" on "32,000"; on "64,000" the camera pulls back and
# the 64K window lands beside it, twice as tall.
def s2_r2():
    r, ws = words('s2', 2)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    CW, CH, G, P = 84, 36, 8, 20
    w32, h32 = tank_size(8, CW, CH, G, P); w64, h64 = tank_size(16, CW, CH, G, P)
    BOT = 890
    x32, x64 = 300, 780
    y32, y64 = BOT - h32 / 2, BOT - h64 / 2

    def label(id, txt, w):
        return (f'<div id="{id}" class="abs" style="left:0;top:-112px;width:{w}px;transform-origin:0 100%">'
                f'<span style="font:600 92px/1 Figtree;letter-spacing:-.03em;color:#fff">{txt}</span>'
                f'<span class="lab" style="margin-left:18px">tokens</span></div>')
    k32 = dict(id='k32', kind='glass', highlight=True, x=x32, y=y32, w=w32, h=h32, clip=False,
               html=tank_html(8, CW, CH, G, P, 'a') + label('l32', '32K', 420))
    k64 = dict(id='k64', kind='glass', x=x64, y=y64, w=w64, h=h64, clip=False,
               html=tank_html(16, CW, CH, G, P, 'b') + label('l64', '64K', 420), land=dict(t=r3(T('64000') - 0.12), dur=0.6))
    t32 = T('32000') - 0.15
    fx.pop('l32', t32, s0=0.6)
    fx.pop('l64', T('64000') + 0.12, s0=0.6)
    # the 32 cells light up bottom->top on "32,000" (a sweep of azure outlines), then settle
    custom = r"""window.CUSTOM=function(t,cam,H){const t0=%f;for(let r=0;r<8;r++){const p=H.cl((t-(t0+r*0.045))/0.22,0,1),q=H.cl((t-(t0+r*0.045+0.35))/0.5,0,1);
      const v=p*(1-q*0.75);for(let c=0;c<4;c++){const e=document.getElementById('a'+r+'_'+c);
      e.style.borderColor='rgba('+Math.round(255+(47-255)*v)+','+Math.round(255+(149-255)*v)+','+Math.round(255+(255-255)*v)+','+(0.17+0.6*v).toFixed(3)+')';
      e.style.background='rgba(47,149,255,'+(0.025+0.16*v).toFixed(3)+')';}}};""" % (t32 + 0.1)
    t_pull = T('64000') - 0.4
    cam0 = dict(x=x32, y=y32 - 10, s=1.3)
    moves = [dict(t=0.1, dur=r3(t_pull - 0.15), kind='glide', to=dict(x=x32, y=y32 - 14, s=1.33)),
             dict(t=r3(t_pull), dur=0.95, kind='pull', to=dict(x=540, y=472, s=1.0)),
             dict(t=r3(t_pull + 1.0), dur=r3(r['dur'] - t_pull - 1.0), kind='glide', to=dict(x=540, y=470, s=1.015))]
    cfg = dict(id='s2_r2', dur=r['dur'], mode='split', cam0=cam0, cards=[k32, k64], moves=moves, pushRef=1.3,
               heroes=[dict(t=0, id='k32'), dict(t=r3(t_pull + 0.2), id='none')],
               sfx=sfx((t32, 'pop'), (T('64000') - 0.12, 'pop')),
               thumb=[[r3(T('64000') + 0.7), r['dur']]], wave=dict(level='low', k=0.9))
    mk('s2_r2', cfg, fx, custom)


# s2_r3 - fv: Claude Code's ~30K harness (30 cells: system prompt azure, tool definitions iris, memory/skills grey) hovers
# over the 32K window, creeps toward it on "inject Claude Code's" and drops in on "30,000": 94% full, the 2 free cells
# pulse ember, the window glows ember.
def s2_r3():
    r, ws = words('s2', 3)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    CW, CH, G, P = 112, 48, 8, 24
    tw, th = tank_size(8, CW, CH, G, P)
    TX, TY = 400, 1204 - th / 2                       # the 32K window, bottom edge at 1204
    # payload: 30 cells in the window's own grid (row 0 = bottom)
    cells = ''
    n = 0
    for rr in range(8):
        for c in range(4):
            if n >= 30: break
            cls = 'az' if n < 4 else ('ir' if n < 28 else 'gr')
            x = c * (CW + G); y = (7 - rr) * (CH + G)
            cells += f'<div class="gc {cls}" style="left:{x}px;top:{y}px;width:{CW}px;height:{CH}px"></div>'
            n += 1
    BW, BH = 4 * (CW + G) - G, 8 * (CH + G) - G
    land_y = TY - th / 2 + P + BH / 2                 # block centre when it sits in the window
    hover = 610                                       # how far above its landing place it starts
    pay = dict(id='pay', kind='plain', x=TX, y=land_y - hover, w=BW, h=BH, clip=False, noDof=True,
               html=f'<div id="payi" class="abs" style="inset:0;transform-origin:50% 100%">{cells}</div>')
    free = ''.join(f'<div id="fr{c}" class="abs" style="left:{P + c * (CW + G)}px;top:{P}px;width:{CW}px;height:{CH}px;border-radius:9px;'
                   f'background:{EMB};box-shadow:0 0 26px rgba(255,138,91,.8);opacity:0"></div>' for c in (2, 3))
    tank = dict(id='tank', kind='glass', x=TX, y=TY, w=tw, h=th, clip=False,
                html=tank_html(8, CW, CH, G, P, 'c') + free +
                ring('tring', 32, EMB, 'rgba(255,138,91,.35)', 3))
    RX = 700                                          # right column (left edge, world)
    right = dict(id='right', kind='plain', x=880, y=720, w=360, h=1100, clip=False, noDof=True, html=(
        f'<div id="ccl" class="abs" style="left:{RX - 700}px;top:{168 - 170}px;width:360px">{img("assets/b_lf_cc_wordmark_ondark.png", 340)}'
        f'<div style="font:600 58px/1 Figtree;letter-spacing:-.025em;color:#fff;margin-top:26px">≈30K</div>'
        f'<div class="lab" style="margin-top:12px">tokens</div></div>'
        f'<div id="frl" class="abs fx" style="left:{RX - 700}px;top:{764 - 170 - 28}px;gap:14px;opacity:0">'
        f'<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="{EMB}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12H5M10 6l-6 6 6 6"/></svg>'
        f'<span style="font:600 48px/1 Figtree;color:{EMB}">2K free</span></div>'
        f'<div id="pctw" class="abs" style="left:{RX - 700}px;top:{880 - 170}px;opacity:0"><div id="pct" style="font:600 128px/1 Figtree;letter-spacing:-.035em;color:{EMB}">0%</div>'
        f'<div class="lab" style="margin-top:14px">full</div></div>'
        f'<div class="abs" style="left:{RX - 700}px;top:{1150 - 170}px"><span style="font:600 64px/1 Figtree;letter-spacing:-.025em;color:#fff">32K</span>'
        f'<span class="lab" style="margin-left:14px">window</span></div>'))
    t_creep, t_drop, t_hit = T('cannot') + 0.2, T('codes') - 0.05, T('30000') + 0.02
    fx.hold['card-pay'] = True
    fx.k('card-pay', (0, dict(y=0)), (t_creep, dict(y=0)), (t_drop, dict(y=120), 'sine.inOut'), (t_hit, dict(y=hover), 'power2.in'))
    fx.k('payi', (t_hit - 0.01, dict(sy=1)), (t_hit + 0.07, dict(sy=0.94), 'power2.out'), (t_hit + 0.3, dict(sy=1), 'back.out(2)'))
    fx.k('ccl', (t_hit - 0.3, dict(o=1)), (t_hit + 0.15, dict(o=0)))
    fx.k('tring', (t_hit, dict(o=0)), (t_hit + 0.35, dict(o=1)))
    fx.k('pctw', (t_hit + 0.05, dict(o=0, y=14)), (t_hit + 0.4, dict(o=1, y=0), 'power3.out'))
    fx.number('pct', [(t_hit + 0.05, 0), (t_hit + 0.65, 94, 'power2.out')], fmt='pct')
    fx.k('frl', (t_hit + 0.45, dict(o=0, x=-16)), (t_hit + 0.8, dict(o=1, x=0), 'power2.out'))
    custom = r"""window.CUSTOM=function(t){const t0=%f;const p=Math.max(0,Math.min(1,(t-t0)/0.4));
      const v=p*(0.62+0.38*Math.sin((t-t0)*5.4));for(const c of [2,3]){document.getElementById('fr'+c).style.opacity=v.toFixed(3);}};""" % (t_hit + 0.5)
    moves = [dict(t=0.0, dur=r3(t_hit - 0.1), kind='glide', to=dict(x=540, y=724, s=1.02)),
             dict(t=r3(t_hit + 0.15), dur=1.25, kind='push', to=dict(x=580, y=930, s=1.14))]
    cfg = dict(id='s2_r3', dur=r['dur'], mode='fv', accent='ember', cam0=dict(x=540, y=720, s=1.0), cards=[tank, pay, right], moves=moves,
               pushRef=1.2, heroes=[dict(t=0, id='none')],
               sfx=sfx((t_hit, 'pop')), thumb=[[r3(t_hit + 1.45), r['dur']]], wave=dict(level='low', k=0.9))
    mk('s2_r3', cfg, fx, custom)


# ----- the harness stack (long-form g16): glass blocks whose heights / ejections / marks are pure functions of t
def stack_blocks(SW, spec):
    """spec: list of (id, h, icon_html, title, body_html, marked)"""
    out = ''
    for bid, h, icon, title, body, marked in spec:
        mk_ = (f'<div id="{bid}_mk" class="abs" style="left:-7px;width:{SW + 14}px;top:-7px;height:{h + 14}px;border-radius:32px;'
               f'border:3px dashed {EMB};box-shadow:0 0 24px rgba(255,138,91,.35);opacity:0"></div>' if marked else '')
        gh = (f'<div id="{bid}_gh" class="abs" style="left:0;width:{SW}px;top:0;height:{h}px;border-radius:28px;border:2px dashed rgba(255,255,255,.16);opacity:0"></div>'
              if marked else '')
        out += (f'{gh}<div id="{bid}" class="abs" style="left:0;top:0;width:{SW}px;height:{h}px;border-radius:28px;overflow:hidden;{GLASS}">'
                f'<div class="abs fx" style="left:28px;top:22px;gap:18px"><div style="position:relative;width:56px;height:56px;flex:none">{icon}</div>'
                f'<div style="font:600 38px/1 Figtree;letter-spacing:-.02em">{title}</div></div>'
                f'{body}<div id="{bid}_st" class="abs" style="left:20px;right:20px;top:48px;height:5px;border-radius:3px;background:{EMB};'
                f'box-shadow:0 0 10px rgba(255,138,91,.8);transform-origin:0 50%;transform:scaleX(0)"></div></div>{mk_}')
    return out


def ntile(name):
    return (f'<div style="width:56px;height:56px;border-radius:16px;flex:none;display:flex;align-items:center;justify-content:center;'
            f'background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12)">{line_ico(name, 30, "#E6E7EA", 1.9)}</div>')


def mini(names, color=T2):
    return ''.join(f'<div class="chipd" style="position:relative;color:{color}">{n}</div>' for n in names)


STACK_JS = r"""
window.CUSTOM=function(t,cam,H){
  const d=CFG.data, P=(t0,dur,e)=>{const x=H.cl((t-t0)/dur,0,1);return e?H.ez(e)(x):x;};
  let y=0;
  d.ids.forEach((id,k)=>{
    const sh=d.shrink[id]; const h=sh?H.at([[sh[0],{v:d.H[k]}],[sh[0]+0.6,{v:sh[1]},'power3.inOut']],t).v:d.H[k];
    const te=d.ej[id]; const pe=te!=null?P(te+0.22,0.5,'power3.inOut'):0, po=te!=null?P(te+0.22,0.45,'power2.in'):0;
    const el=H.$(id); el.style.height=h.toFixed(2)+'px'; el.style.top=y.toFixed(2)+'px';
    const tr='translateX('+(po*300).toFixed(2)+'px) rotate('+(po*4).toFixed(2)+'deg) scale('+(1-0.06*po).toFixed(4)+')';
    el.style.transform=tr; el.style.opacity=(1-po).toFixed(3);
    const mk=H.$(id+'_mk'); if(mk){ mk.style.top=(y-7).toFixed(2)+'px'; mk.style.transform=tr;
      const tm=d.mark[id]; const pulse=0.78+0.22*Math.sin((t-(tm||0))*5);
      mk.style.opacity=(tm==null?0:P(tm,0.3)*pulse*(1-(te!=null?P(te,0.25):0))).toFixed(3); }
    const gh=H.$(id+'_gh'); if(gh){ gh.style.top=y.toFixed(2)+'px'; gh.style.height=h.toFixed(2)+'px'; gh.style.opacity=(d.ghost&&te!=null?P(te+0.4,0.4):0).toFixed(3); }
    if(te!=null) H.$(id+'_st').style.transform='scaleX('+P(te,0.25,'power2.out').toFixed(4)+')';
    y+=(h+d.gap)*(d.ghost?1:(1-pe));
  });
  if(d.scan!=null){ const ps=P(d.scan,0.95,'power1.inOut'); const sc=H.$('scan'); sc.style.top=(ps*d.H0).toFixed(2)+'px'; sc.style.opacity=Math.sin(Math.PI*ps).toFixed(3); }
  if(d.trim!=null){ const pt=P(d.trim,0.5,'power2.inOut');
    document.querySelectorAll('.cct').forEach((e,i)=>{const q=P(d.trim+i*0.03,0.3,'power2.in'); e.style.opacity=(1-q).toFixed(3); e.style.transform='scale('+(1-0.25*q).toFixed(3)+')';});
    document.querySelectorAll('.smt').forEach((e,i)=>{const q=P(d.trim+0.3+i*0.04,0.35,'back.out(2)'); e.style.opacity=H.cl(q*2,0,1).toFixed(3); e.style.transform='scale('+(0.7+0.3*q).toFixed(3)+')';}); }
  if(d.sys!=null){ const ps=P(d.sys,0.6,'power3.inOut');
    document.querySelectorAll('.sysl').forEach((e,i)=>{ if(i>0) e.style.opacity=(1-ps).toFixed(3); else e.style.width=(d.l0*(1-ps)+d.l1*ps).toFixed(1)+'px'; }); }
  if(d.fans){ const rr=Math.max(0,t-d.spinT), R=0.8; const ang=d.spin0*t+(d.spin1-d.spin0)*(rr<R?rr*rr/(2*R):rr-R/2);
    d.fans.forEach((f,i)=>{ const e=H.$(f); if(e) e.style.transform='rotate('+((ang+i*20)%%360).toFixed(1)+'deg)'; }); }
  if(d.led){ const e=H.$(d.led); if(e) e.style.opacity=(0.25+0.75*P(d.spinT,0.6)).toFixed(3); }
};
""".replace('%%', '%')

CC_TOOLS = ['Bash', 'Read', 'Edit', 'Write', 'Grep', 'Glob', 'WebFetch', 'WebSearch', 'Task', 'TodoWrite', 'NotebookEdit', 'Skill', 'ExitPlanMode']
SMOL_TOOLS = ['read', 'write', 'edit', 'list', 'search', 'plan', 'run_command', 'task']   # smolcoder's eight flat tools (its changelog)


def tool_chips(names, cls, maxw, extra=''):
    return ''.join(f'<div class="chipd {extra} {cls}" style="left:{x}px;top:{y}px">{n}</div>' for n, (x, y, w) in zip(names, chip_rows(names, maxw)))


# s2_r5 - fv. Phase 1: the REAL SMOL Coder CLI (6.mkv, long-form 11:21) in the capture frame, the inner camera pushes onto
# the SMOL logo on "SMOL Coder". One whip (whoosh at its midpoint) down to the strip: a heavy harness stack (system prompt,
# Claude Code's tool list, skills, MCP tools, sub-agents) under the SMOL Coder logo; an azure scan on "strips away",
# skills are struck and ejected on "anything", the tool list trims to SMOL Coder's eight real tools on "open weight model",
# the system prompt shrinks to a sliver, and MCP tools + sub-agents are marked ember on "never need" (struck in s2_r6).
def s2_r5():
    r, ws = words('s2', 5)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    fw, fh = D['b_smol_cli.mp4']
    t_whip = T('harness') + 0.12
    cap = capture_card('cap', fw, fh, inner0=dict(fx=780, fy=790, k=0.66), backdrop={'tIn': -1, 'tOut': r3(t_whip + 0.2)},
                       inner=[dict(t=r3(T('smol') - 0.3), dur=0.65, fx=590, fy=560, k=1.0)])
    cap['bg'] = '#0C0C0C'
    OY = 2400                                         # phase 2 sits below
    SW = 900
    sysl = ''.join(f'<div class="abs sysl" style="left:30px;top:{100 + i * 18}px;width:{w}px;height:10px;border-radius:5px;background:rgba(255,255,255,.16)"></div>'
                   for i, w in enumerate([780, 720, 760, 420]))
    cc = tool_chips(CC_TOOLS, 'cct', SW - 60)
    sm = tool_chips(SMOL_TOOLS, 'smt', SW - 60, 'az')
    spec = [('bk_sys', 170, tile('azure', 'code', 56, -8), 'System prompt', sysl, False),
            ('bk_tool', 290, tile('iris', 'bolt', 56, 8), 'Tools', f'<div class="abs" style="left:30px;top:96px">{cc}{sm}</div>', False),
            ('bk_skl', 104, ntile('cube'), 'Skills', f'<div class="abs fx" style="right:28px;top:29px;gap:10px">{mini(["skill-creator", "claude-api"])}</div>', True),
            ('bk_mcp', 104, ntile('plug'), 'MCP tools', f'<div class="abs fx" style="right:28px;top:29px;gap:10px">{mini(["Claude Docs"])}</div>', True),
            ('bk_sub', 104, ntile('robot'), 'Sub-agents', f'<div class="abs fx" style="right:28px;top:29px;gap:10px">{mini(["Explore", "Plan"])}</div>', True)]
    GAP = 16
    H0 = sum(s[1] for s in spec) + GAP * (len(spec) - 1)
    STOP = 352 + OY                                   # stack top (world)
    scan = (f'<div id="scan" class="abs" style="left:-30px;width:{SW + 60}px;top:0;height:4px;border-radius:2px;background:{AZ};'
            f'box-shadow:0 0 24px 6px rgba(47,149,255,.55);opacity:0"></div>')
    stack = dict(id='stack', kind='plain', clip=False, x=540, y=STOP + H0 / 2, w=SW, h=H0, html=stack_blocks(SW, spec) + scan)
    smol = dict(id='smol', kind='glass', highlight=True, x=540, y=OY + 205, w=560, h=170,
                html=f'<div class="abs fx" style="inset:0;justify-content:center">{img("assets/b_lf_smol_logo_alpha.png", 420)}</div>')
    t_scan, t_any, t_open, t_model, t_never = T('strips'), T('anything'), T('open'), T('model'), T('never')
    data = dict(ids=[s[0] for s in spec], H=[s[1] for s in spec], gap=GAP, H0=H0, ghost=False,
                ej=dict(bk_skl=t_any), mark=dict(bk_skl=t_scan + 0.45, bk_mcp=t_never - 0.05, bk_sub=t_never + 0.08),
                shrink=dict(bk_tool=[t_open + 0.3, 222], bk_sys=[t_model, 100]),
                scan=t_scan, trim=t_open - 0.1, sys=t_model, l0=780, l1=300)
    # as the harness slims, the camera pushes in on what is left (SMOL tile top 2520 .. lean stack bottom ~3330)
    t_slim = t_open + 0.25
    moves = [dict(t=r3(t_whip), kind='whip', to=dict(x=540, y=720 + OY, s=1.0), via=dict(x=540, y=720 + OY / 2, s=0.86)),
             dict(t=r3(t_whip + 1.1), dur=r3(t_slim - t_whip - 1.15), kind='glide', to=dict(x=540, y=716 + OY, s=1.02)),
             dict(t=r3(t_slim), dur=r3(r['dur'] - t_slim - 0.05), kind='push', to=dict(x=540, y=2925, s=1.14))]
    cfg = dict(id='s2_r5', dur=r['dur'], mode='fv', cam0=dict(x=540, y=720, s=1), cards=[cap, smol, stack], moves=moves, pushRef=1.2,
               heroes=[dict(t=0, id='cap'), dict(t=r3(t_whip + 0.45), id='none')], data=data,
               sfx=sfx((t_whip + 0.45, 'whoosh'), (t_any, 'click'), (t_open, 'click'), (t_never, 'click')),
               wave=dict(level='low', k=0.8))
    mk('s2_r5', cfg, fx, STACK_JS, videos=[('cap', 'assets/b_smol_cli.mp4', fw, fh)], backdrop=('video', 'assets/b_smol_cli.mp4', fw, fh))


# s2_r6 - split: an open-weight model on your own hardware (glass: a consumer GPU, Ollama, Qwen3.8 27B - the model Leon
# runs in SMOL Coder) above the lean SMOL harness; its fans spin up on "hardware"; MCP tools and sub-agents (marked in
# s2_r5) are struck and ejected on their names, leaving empty slots.
def s2_r6():
    r, ws = words('s2', 6)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    fan = lambda i, l: (f'<div id="fan{i}" class="abs" style="left:{l}px;top:28px;width:132px;height:132px;border-radius:50%;border:7px solid #0B0C0E;'
                        'background:radial-gradient(circle,#18191C 0 17%,transparent 18%),repeating-conic-gradient(from 0deg,#5A5D64 0deg 20deg,#212226 20deg 45deg)"></div>')
    gpu = (f'<div class="abs" style="left:34px;top:34px;width:360px;height:190px;border-radius:22px;background:linear-gradient(160deg,#2C2D31,#111214);'
           f'box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 0 0 1px rgba(255,255,255,.06)">{fan(0, 26)}{fan(1, 200)}'
           f'<div id="led" class="abs" style="left:24px;right:24px;bottom:12px;height:6px;border-radius:3px;background:{AZ};box-shadow:0 0 14px rgba(47,149,255,.9);opacity:.25"></div></div>')
    mach = dict(id='mach', kind='glass', highlight=True, x=540, y=190, w=1000, h=258, html=(
        gpu + f'<div class="abs fx" style="left:440px;top:0;height:258px;gap:30px">{img("assets/b_lf_ollama_white.png", None, 132)}'
        f'<div><div style="font:600 56px/1 Figtree;letter-spacing:-.025em">Qwen3.8 27B</div>'
        f'<div class="m" style="font-size:30px;color:{T2};margin-top:16px">Q6_K · Ollama</div></div></div>'))
    SW = 900
    sysl = ''.join(f'<div class="abs sysl" style="left:30px;top:84px;width:{w}px;height:10px;border-radius:5px;background:rgba(255,255,255,.16)"></div>'
                   for i, w in enumerate([300]))
    sm = tool_chips(SMOL_TOOLS, '', SW - 60, 'az')
    spec = [('bk_sys', 96, tile('azure', 'code', 52, -8), 'System prompt', sysl.replace('top:84px', 'top:40px;left:420px'), False),
            ('bk_tool', 214, tile('iris', 'bolt', 52, 8), 'Tools', f'<div class="abs" style="left:30px;top:88px">{sm}</div>', False),
            ('bk_mcp', 96, ntile('plug'), 'MCP tools', f'<div class="abs fx" style="right:28px;top:25px;gap:10px">{mini(["Claude Docs"])}</div>', True),
            ('bk_sub', 96, ntile('robot'), 'Sub-agents', f'<div class="abs fx" style="right:28px;top:25px;gap:10px">{mini(["Explore", "Plan"])}</div>', True)]
    GAP = 14
    H0 = sum(s[1] for s in spec) + GAP * (len(spec) - 1)
    STOP = 348
    stack = dict(id='stack', kind='plain', clip=False, x=540, y=STOP + H0 / 2, w=SW, h=H0, html=stack_blocks(SW, spec))
    t_hw, t_mcp, t_sub = T('hardware'), T('mcp'), T('subagents.')
    # the ejected blocks leave a cross tile where they were
    xt = lambda i, y: tile('ember', None, 64, 0, id=f'xx{i}', style=f'left:{SW - 92}px;top:{y}px;opacity:0',
                           svg_markup='<svg width="{s}" height="{s}" viewBox="0 0 24 24"><path d="M7 7l10 10M17 7L7 17" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round"/></svg>', sm=True)
    y_mcp = 96 + GAP + 214 + GAP; y_sub = y_mcp + 96 + GAP
    stack['html'] += xt(0, y_mcp + 16) + xt(1, y_sub + 16)
    fx.pop('xx0', t_mcp + 0.5, s0=0.4); fx.pop('xx1', t_sub + 0.5, s0=0.4)
    data = dict(ids=[s[0] for s in spec], H=[s[1] for s in spec], gap=GAP, H0=H0, ghost=True,
                ej=dict(bk_mcp=t_mcp, bk_sub=t_sub), mark=dict(bk_mcp=-1.0, bk_sub=-1.0), shrink={},
                scan=None, trim=None, sys=None, fans=['fan0', 'fan1'], spin0=60, spin1=520, spinT=t_hw - 0.3, led='led')
    moves = [dict(t=0.0, dur=r['dur'], kind='glide', to=dict(x=540, y=474, s=1.03))]
    cfg = dict(id='s2_r6', dur=r['dur'], mode='split', cam0=dict(x=540, y=470, s=1.0), cards=[mach, stack], moves=moves, pushRef=1.03,
               heroes=[dict(t=0, id='none')], data=data,
               sfx=sfx((t_mcp, 'click'), (t_sub, 'click')), thumb=[[r3(t_mcp + 1.0), r3(t_sub - 0.05)]], wave=dict(level='low', k=0.9))
    mk('s2_r6', cfg, fx, STACK_JS)


# =============================================================================================================== SHORT 3
EQ_X, EQ_Y, EQ_W, EQ_H = 540, 680, 1000, 420        # the equation card (s3_r0 end = s3_r2 start), bottom edge 890
EQ_COLS = [175, 500, 825]                             # column centres inside the card
EQ_OPS = [338, 662]


def eq_card(model_html, harness_html, model_label='', harness_label='', label_op=1):
    tl = 70; ty = 280
    col = lambda cx, inner, label, lid, op: (f'<div class="abs" style="left:{cx - 110}px;top:{tl}px;width:220px;height:180px;display:flex;align-items:center;justify-content:center">{inner}</div>'
                                             f'<div id="{lid}" class="abs" style="left:{cx - 170}px;top:{ty}px;width:340px;text-align:center;font:600 60px/1.1 Figtree;'
                                             f'letter-spacing:-.025em;color:#fff;opacity:{op}">{label}</div>')
    op = lambda cx, s: f'<div class="abs" style="left:{cx - 40}px;top:{tl + 40}px;width:80px;text-align:center;font:600 92px/1 Figtree;color:{T2}">{s}</div>'
    return (col(EQ_COLS[0], f'<div style="position:relative;width:170px;height:170px">{robot(170, style="left:0;top:0", tilt=-8)}</div>', 'Agent', 'eqA', 1) +
            op(EQ_OPS[0], '=') + col(EQ_COLS[1], model_html, model_label, 'eqM', label_op) + op(EQ_OPS[1], '+') +
            col(EQ_COLS[2], harness_html, harness_label, 'eqH', label_op))


def qslot(id):
    return (f'<div id="{id}" style="position:relative;width:170px;height:170px;border-radius:44px;border:3px dashed rgba(47,149,255,.55);'
            f'background:rgba(47,149,255,.06);display:flex;align-items:center;justify-content:center;font:600 104px/1 Figtree;color:{AZ}">?</div>')


# s3_r0 - split hook (cover-safe). Frame 0: one glass "agent" chip at y ~760 below the cover title. On "agent" the word
# echoes: chips of the ways it is used everywhere pop in all over the stage; on "But what exactly" they collapse into
# the centre and the glass equation card lands: Agent = ? + ? (the ?s pulse on "agent?").
ECHO = [('AI agents', 64, 270, 110), ('agentic', 56, 790, 150), ('coding agent', 52, 380, 245), ('Agent SDK', 50, 850, 300),
        ('sub-agents', 46, 190, 370), ('agent swarm', 50, 640, 405), ('multi-agent', 46, 320, 505), ('AGENTS.md', 42, 840, 520),
        ('agent mode', 44, 170, 610), ('agentic AI', 46, 650, 600)]


def s3_r0():
    r, ws = words('s3', 0)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    t_ag, t_but, t_q = T('agent'), T('but'), T('agent', 2)
    chips = ''
    for i, (txt, fs, x, y) in enumerate(ECHO):
        mono = txt == 'AGENTS.md'
        font = f"500 {fs - 4}px/1 'Geist Mono'" if mono else f'600 {fs}px/1 Figtree;letter-spacing:-.02em'
        chips += (f'<div class="abs" style="left:{x}px;top:{y}px"><div id="ec{i}" class="abs" style="left:0;top:0">'
                  f'<div class="abs" style="left:0;top:0;transform:translate(-50%,-50%)">'
                  f'<div id="eci{i}" style="padding:{round(fs * 0.36)}px {round(fs * 0.55)}px;border-radius:{round(fs * 0.5)}px;{GLASS}font:{font};white-space:nowrap;opacity:0">{txt}</div>'
                  f'</div></div></div>')
    echo = dict(id='echo', kind='plain', x=540, y=480, w=1080, h=960, clip=False, noDof=True,
                html=f'<div class="abs" style="left:0;top:0;width:1080px;height:960px">{chips}</div>')
    main = dict(id='ag', kind='plain', x=540, y=760, w=2, h=2, clip=False, noDof=True,
                html=(f'<div class="abs" style="left:1px;top:1px"><div id="agw" class="abs" style="left:0;top:0">'
                      f'<div class="abs" style="left:0;top:0;transform:translate(-50%,-50%)"><div class="fx" style="gap:30px;padding:30px 52px 30px 34px;border-radius:44px;{GLASS}'
                      f'border-color:rgba(47,149,255,.4);box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 0 110px -30px rgba(47,149,255,.8),0 50px 120px -40px rgba(0,0,0,.85)">'
                      f'<div style="position:relative;width:112px;height:112px;flex:none">{robot(112, style="left:0;top:0")}</div>'
                      f'<div style="font:600 104px/1 Figtree;letter-spacing:-.03em;color:#fff">agent</div></div></div></div></div>'))
    eq = dict(id='eq', kind='glass', highlight=True, x=EQ_X, y=EQ_Y, w=EQ_W, h=EQ_H, clip=False,
              html=eq_card(qslot('q1'), qslot('q2')), land=dict(t=r3(t_but + 0.32), dur=0.55))
    # echo: pops on "agent" ... "so many times", gentle drift, then all collapse into the equation card on "But what"
    cx, cy = 540, 680                                 # collapse point (the echo layer's coords = world coords)
    for i, (txt, fs, x, y) in enumerate(ECHO):
        tin = t_ag - 0.1 + 0.105 * i
        tout = t_but - 0.15 + 0.03 * i
        dx, dy = (cx - x) * 0.92, (cy - y) * 0.92
        fx.k(f'eci{i}', (tin, dict(o=0, s=0.55)), (tin + 0.2, dict(o=1), 'power2.out'), (tin + 0.42, dict(s=1), 'back.out(2.4)'),
             (tout, dict(o=1, s=1)), (tout + 0.42, dict(o=0, s=0.4), 'power2.in'))
        drift = 14 if i % 2 else -14
        fx.k(f'ec{i}', (tin, dict(x=0, y=0)), (tout, dict(x=drift, y=-10), 'sine.inOut'), (tout + 0.42, dict(x=dx, y=dy), 'power2.in'))
    # the frame-0 chip goes the same way
    fx.k('agw', (t_but - 0.2, dict(o=1, s=1, y=0)), (t_but + 0.25, dict(o=0, s=0.6, y=-80), 'power2.in'))
    for q in ('q1', 'q2'):
        fx.k(q, (t_q - 0.12, dict(s=1)), (t_q + 0.08, dict(s=1.12), 'power2.out'), (t_q + 0.45, dict(s=1), 'back.out(2)'))
    moves = [dict(t=0.0, dur=r['dur'], kind='glide', to=dict(x=540, y=468, s=1.025))]
    cfg = dict(id='s3_r0', dur=r['dur'], mode='split', cam0=dict(x=540, y=470, s=1.0), cards=[echo, eq, main], moves=moves, pushRef=1.03,
               heroes=[dict(t=0, id='none')], sfx=sfx((t_ag - 0.1, 'pop'), (t_but + 0.32, 'pop')), wave=dict(level='low', k=0.9))
    mk('s3_r0', cfg, fx)


# s3_r2 - split: the equation from s3_r0 (frame 0 = its end state) fills in: the model tile (azure sparkle) lands on
# "model", the harness (his four slide tiles: instructions, tools, checks, memory) on "harness".
def s3_r2():
    r, ws = words('s3', 2)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    t_m, t_h = T('model') - 0.2, T('harness.') - 0.2
    model = (f'<div style="position:relative;width:170px;height:170px">{qslot("q1")}'
             f'<div id="mt" class="abs" style="left:0;top:0;opacity:0">{tile("azure", "sparkle", 170, 8)}</div></div>')
    harness = (f'<div style="position:relative;width:170px;height:170px">'
               f'<div class="abs" style="left:0;top:0">{qslot("q2")}</div>'
               f'<div class="abs" style="left:-6px;top:-6px">{harness_tiles(84, 14, "hh")}</div></div>')
    model = model.replace(qslot('q1'), f'<div class="abs" style="left:0;top:0">{qslot("q1")}</div>')
    html = eq_card(model, harness, 'Model', 'Harness', label_op=0)
    eq = dict(id='eq', kind='glass', highlight=True, x=EQ_X, y=EQ_Y, w=EQ_W, h=EQ_H, clip=False, html=html)
    fx.k('q1', (t_m, dict(o=1)), (t_m + 0.18, dict(o=0)))
    fx.pop('mt', t_m, s0=0.4, dur=0.5)
    fx.k('eqM', (t_m + 0.08, dict(o=0, y=14)), (t_m + 0.4, dict(o=1, y=0), 'power3.out'))
    fx.k('q2', (t_h, dict(o=1)), (t_h + 0.18, dict(o=0)))
    for i in range(4):
        fx.pop(f'hh{i}', t_h + 0.06 * i, s0=0.3, dur=0.45)
    fx.k('eqH', (t_h + 0.1, dict(o=0, y=14)), (t_h + 0.42, dict(o=1, y=0), 'power3.out'))
    moves = [dict(t=0.0, dur=r['dur'], kind='glide', to=dict(x=540, y=468, s=1.03))]
    cfg = dict(id='s3_r2', dur=r['dur'], mode='split', cam0=dict(x=540, y=470, s=1.0), cards=[eq], moves=moves, pushRef=1.03,
               heroes=[dict(t=0, id='eq')], sfx=sfx((t_m, 'pop'), (t_h, 'pop')),
               thumb=[[r3(t_h + 0.62), r['dur']]], wave=dict(level='low', k=0.9))
    mk('s3_r2', cfg, fx)


# s3_r3 - fv: the model tile (frame 0, pushed in) then three REAL model pages land on their names: Anthropic's "Claude
# Opus 5.5" and "Claude Fable 5.1" announcement heroes and OpenAI's GPT-6 Astra model page header, each with its maker's
# logo tile on the edge.
def model_card(src, logo, iw, ih, paper=False):
    inner = (f'<div class="abs" style="inset:0;border-radius:24px;overflow:hidden;background:{"#fff" if paper else "#000"}">'
             + (f'<div class="abs fx" style="inset:0;justify-content:center">{img(src, iw, ih)}</div>' if paper else img(src, 1000, 300, 'object-fit:cover'))
             + '</div>')
    badge = (f'<div class="abs fx" style="left:-26px;top:-34px;width:104px;height:104px;border-radius:30px;background:#fff;justify-content:center;'
             f'box-shadow:0 18px 40px -12px rgba(0,0,0,.7),inset 0 -6px 12px rgba(0,0,0,.06)">{img(logo, 64, 64)}</div>')
    return inner + badge


def s3_r3():
    r, ws = words('s3', 3)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    hd = dict(id='hd', kind='glass', x=540, y=196, w=420, h=150, html=(
        f'<div class="abs fx" style="inset:0;justify-content:center;gap:26px"><div style="position:relative;width:96px;height:96px">{tile("azure", "sparkle", 96, 8, style="left:0;top:0")}</div>'
        f'<div style="font:600 60px/1 Figtree;letter-spacing:-.025em">Model</div></div>'))
    claude, oai = 'assets/b_lf_claude_symbol.png', 'assets/b_lf_openai_symbol.png'
    ys = [455, 765, 1075]
    names = [('opus', T('opus')), ('fable', T('fable')), ('gpt6.', T('gpt6.'))]
    cards = [hd]
    for i, ((nm, tw), y) in enumerate(zip(names, ys)):
        if i == 0: html = model_card('assets/b_hero_opus.jpg', claude, 1000, 300)
        elif i == 1: html = model_card('assets/b_hero_fable.jpg', claude, 1000, 300)
        else: html = model_card('assets/b_hero_gpt6.png', oai, 1000, 197, paper=True)
        cards.append(dict(id=f'c{i}', kind='media', x=540, y=y, w=1000, h=300, clip=False, bg='#fff', html=html,
                          land=dict(t=r3(tw - 0.14), dur=0.55)))
    t_pull = T('language') - 0.1
    moves = [dict(t=0.0, dur=r3(t_pull), kind='glide', to=dict(x=540, y=206, s=1.58)),
             dict(t=r3(t_pull), dur=1.05, kind='pull', to=dict(x=540, y=724, s=1.0)),
             dict(t=r3(t_pull + 1.1), dur=r3(r['dur'] - t_pull - 1.1), kind='glide', to=dict(x=540, y=720, s=1.01))]
    cfg = dict(id='s3_r3', dur=r['dur'], mode='fv', cam0=dict(x=540, y=206, s=1.62), cards=cards, moves=moves, pushRef=1.6,
               heroes=[dict(t=0, id='none')], sfx=sfx(*[(tw - 0.14, 'pop') for _, tw in names]),
               thumb=[[r3(names[2][1] + 0.45), r['dur']]], wave=dict(level='low', k=0.8))
    mk('s3_r3', cfg, fx)


# s3_r4 - split (the long-form g04 model socket): the three models as paper chips above a glass harness with an empty
# MODEL socket and his four slide tiles unpowered; on "brain" Opus 5.5 docks into the socket (azure), the other two
# fade, and on "operation" the harness tiles power up while the camera pushes in.
def mchip(logo, name):
    return (f'<div class="abs fx" style="inset:0;justify-content:center;gap:18px">{img(logo, 54, 54)}'
            f'<div style="font:600 42px/1 Figtree;letter-spacing:-.02em;color:{INK};white-space:nowrap">{name}</div></div>')


SOCK_W, SOCK_H = 360, 132


def harness_panel(sock_inner='', powered=False):
    """glass harness: the MODEL socket in the middle, his four tiles in the corners (#hp0..3, dim unless powered)"""
    ic = [('azure', 'code', 60, 60, -8), ('iris', 'bolt', 840, 60, 8), ('mint', 'check', 60, 420, 8), ('ember', 'bars', 840, 420, -8)]
    tiles = ''.join(f'<div id="hp{i}" class="abs" style="left:{x}px;top:{y}px;width:100px;height:100px;opacity:{1 if powered else .26}">{tile(c, g, 100, tl, style="left:0;top:0")}</div>'
                    for i, (c, g, x, y, tl) in enumerate(ic))
    sx, sy = 500 - SOCK_W / 2, 290 - SOCK_H / 2
    ends = [((160, 110), (sx, 262)), ((840, 110), (sx + SOCK_W, 262)), ((160, 470), (sx, 318)), ((840, 470), (sx + SOCK_W, 318))]
    paths = ''.join(f'<path id="hw{i}" d="M{x0} {y0} C {(x0 + x1) / 2} {y0}, {(x0 + x1) / 2} {y1}, {x1} {y1}" fill="none" stroke="{AZ}" stroke-width="4" '
                    f'stroke-linecap="round" stroke-dasharray="400" stroke-dashoffset="{0 if powered else 400}" style="filter:drop-shadow(0 0 7px rgba(47,149,255,.9))"/>'
                    for i, ((x0, y0), (x1, y1)) in enumerate(ends))
    wires = f'<svg class="abs" style="left:0;top:0;overflow:visible" width="1000" height="580">{paths}</svg>'
    return (wires + tiles +
            f'<div id="sglow" class="abs" style="left:{sx - 90}px;top:{sy - 80}px;width:{SOCK_W + 180}px;height:{SOCK_H + 160}px;border-radius:50%;'
            f'background:radial-gradient(closest-side,rgba(47,149,255,.34),rgba(47,149,255,0));opacity:{1 if powered else .3}"></div>'
            f'<div class="abs" style="left:{sx}px;top:{sy}px;width:{SOCK_W}px;height:{SOCK_H}px;border-radius:26px;border:2px dashed {HAIR2};background:rgba(255,255,255,.03)"></div>'
            f'<div id="slit" class="abs" style="left:{sx - 5}px;top:{sy - 5}px;width:{SOCK_W + 10}px;height:{SOCK_H + 10}px;border-radius:30px;border:3px solid {AZ};'
            f'box-shadow:0 0 0 8px rgba(47,149,255,.12),0 0 60px rgba(47,149,255,.55);opacity:{1 if powered else 0}"></div>'
            f'<div class="abs lab" style="left:{sx}px;top:{sy - 50}px">Model</div>' + sock_inner)


def s3_r4():
    r, ws = words('s3', 4)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    claude, oai = 'assets/b_lf_claude_symbol.png', 'assets/b_lf_openai_symbol.png'
    CY_, CW_, CH_ = 150, 320, 120
    xs = [190, 540, 890]
    HPX, HPY, HPW, HPH = 540, 590, 1000, 580          # panel 300..880
    t_br, t_op, t_mod = T('brain'), T('operation.'), T('models')
    t0d, t1d = t_br - 0.62, t_br + 0.02
    chips = []
    for i, (lg, nm) in enumerate([(claude, 'Opus 5.5'), (claude, 'Fable 5.1'), (oai, 'GPT-6')]):
        c = dict(id=f'm{i}', kind='paper', x=xs[i], y=CY_, w=CW_, h=CH_, html=mchip(lg, nm) + ring(f'mr{i}', 24, AZ, 'rgba(47,149,255,.25)', 3), noDof=True)
        if i: c['exit'] = dict(t=r3(t_br - 0.1), dur=0.5)
        chips.append(c)
    panel = dict(id='hp', kind='glass', x=HPX, y=HPY, w=HPW, h=HPH, html=harness_panel())
    # Opus flies into the socket (socket centre in world = panel top-left + (500, 290))
    sxw, syw = HPX - HPW / 2 + 500, HPY - HPH / 2 + 290
    tx, ty = sxw - xs[0], syw - CY_
    fx.hold['card-m0'] = False
    fx.k('card-m0', (t0d, dict(x=0, y=0, s=1)), (t0d + 0.3, dict(x=tx * 0.42, y=ty * 0.6, s=1.03), 'power2.in'), (t1d, dict(x=tx, y=ty, s=1.0), 'power3.out'))
    for i in range(3):
        fx.k(f'mr{i}', (t_mod - 0.1 + 0.06 * i, dict(o=0)), (t_mod + 0.15 + 0.06 * i, dict(o=1)), (t_mod + 0.75, dict(o=0.0)))
    fx.k('slit', (t1d - 0.02, dict(o=0)), (t1d + 0.3, dict(o=1), 'power2.out'))
    fx.k('sglow', (t1d - 0.02, dict(o=0.3, s=1)), (t1d + 0.4, dict(o=1, s=1.12), 'power2.out'))
    for i in range(4):
        tt = t_op - 0.12 + 0.07 * i
        fx.k(f'hp{i}', (tt, dict(o=0.26, s=0.92)), (tt + 0.45, dict(o=1, s=1), 'back.out(2)'))
        fx.k(f'hw{i}', (tt - 0.15, dict(dash=400)), (tt + 0.3, dict(dash=0), 'power2.out'))
    moves = [dict(t=0.1, dur=r3(t_br - 0.5), kind='glide', to=dict(x=540, y=472, s=1.015)),
             dict(t=r3(t_br - 0.35), dur=1.4, kind='push', to=dict(x=540, y=508, s=1.12))]
    cfg = dict(id='s3_r4', dur=r['dur'], mode='split', cam0=dict(x=540, y=470, s=1.0), cards=[panel] + chips, moves=moves, pushRef=1.2,
               heroes=[dict(t=0, id='none')], sfx=sfx((t1d, 'pop')),
               thumb=[[r3(t_op + 0.6), r['dur']]], wave=dict(level='low', k=0.9))
    mk('s3_r4', cfg, fx)


# s3_r5 - fv: the model (Opus docked, continuity) at the centre, pushed in; on "harness" the camera pulls back while the
# harness boundary draws itself around it; on "environment" his four slide cards (Instructions, Tools, Checks, Memory,
# his own wording from the "Agent = model + harness" slide) land around the model; on "functions" their wires light
# and pulses flow into the model.
SLIDE = [('azure', 'code', 'Instructions', 'AGENTS.md: what to do, and what never to do'),
         ('iris', 'bolt', 'Tools', 'Shell, file edits, a browser, MCP servers'),
         ('mint', 'check', 'Checks', 'Tests, linters and hooks that prove it works'),
         ('ember', 'bars', 'Memory', 'Progress notes and git history between sessions')]


def slide_card(i, w):
    c, g, title, body = SLIDE[i]
    return (tile(c, g, 96, -8 if i % 2 == 0 else 8, style='left:26px;top:-44px') +
            f'<div class="abs" style="left:32px;top:76px;font:600 48px/1.1 Figtree;letter-spacing:-.025em;color:#fff">{title}</div>'
            f'<div class="abs" style="left:32px;top:142px;width:{w - 60}px;font:400 31px/1.35 Figtree;color:{T2}">{body}</div>')


def core_html():
    claude = 'assets/b_lf_claude_symbol.png'
    return (f'<div class="abs lab" style="left:40px;top:26px">Model</div>'
            f'<div class="abs fx" style="left:40px;top:76px;width:380px;height:100px;border-radius:22px;background:#fff;justify-content:center;gap:18px;'
            f'box-shadow:0 0 0 3px {AZ},0 0 40px rgba(47,149,255,.55)">{img(claude, 56, 56)}'
            f'<div style="font:600 46px/1 Figtree;letter-spacing:-.02em;color:{INK}">Opus 5.5</div></div>')


def s3_r5():
    r, ws = words('s3', 5)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    t_h, t_env, t_fn = T('harness'), T('environment'), T('functions.')
    CXc, CYc = 540, 700
    core = dict(id='core', kind='glass', highlight=True, x=CXc, y=CYc, w=460, h=210, html=core_html(), noDof=True)
    KW, KH = 476, 266
    pos = [(286, 372), (794, 372), (286, 1040), (794, 1040)]
    cards = []
    for i, (x, y) in enumerate(pos):
        cards.append(dict(id=f'k{i}', kind='glass', x=x, y=y, w=KW, h=KH, clip=False, html=slide_card(i, KW),
                          land=dict(t=r3(t_env - 0.22 + 0.1 * i), dur=0.55), noDof=True))
    # boundary + wires (one plain layer under everything)
    BX0, BY0, BX1, BY1 = 22, 150, 1058, 1206
    per = 2 * (BX1 - BX0 + BY1 - BY0)
    wires = ''
    for i, (x, y) in enumerate(pos):
        x0 = x + (KW / 2 - 40) * (1 if i % 2 == 0 else -1); y0 = y + (KH / 2) * (1 if i < 2 else -1)
        x1 = CXc + (150 if i % 2 else -150); y1 = CYc + (105 if i >= 2 else -105)
        wires += (f'<path id="wp{i}" d="M{x0} {y0} C {x0} {(y0 + y1) / 2}, {x1} {(y0 + y1) / 2}, {x1} {y1}" fill="none" stroke="{AZ}" stroke-width="4" '
                  f'stroke-linecap="round" style="filter:drop-shadow(0 0 8px rgba(47,149,255,.9))" stroke-dasharray="900" stroke-dashoffset="900"/>'
                  f'<circle id="pl{i}" r="9" fill="#CFE7FF" style="filter:drop-shadow(0 0 10px #2F95FF)" opacity="0"/>')
    layer = (f'<svg class="abs" style="left:0;top:0;overflow:visible" width="1080" height="1400" viewBox="0 0 1080 1400">'
             f'<rect id="bnd" x="{BX0}" y="{BY0}" width="{BX1 - BX0}" height="{BY1 - BY0}" rx="56" fill="rgba(47,149,255,.025)" stroke="{AZ}" stroke-width="3" '
             f'stroke-dasharray="{per}" stroke-dashoffset="{per}" style="filter:drop-shadow(0 0 10px rgba(47,149,255,.7))"/>{wires}</svg>'
             f'<div id="bl" class="abs lab acc" style="left:{BX0 + 40}px;top:{BY0 - 50}px;opacity:0">Harness</div>')
    under = dict(id='under', kind='plain', x=540, y=700, w=1080, h=1400, clip=False, noDof=True,
                 html=f'<div class="abs" style="left:0;top:0;width:1080px;height:1400px">{layer}</div>')
    fx.k('bnd', (t_h - 0.1, dict(dash=per)), (t_h + 1.05, dict(dash=0), 'power2.inOut'))
    fx.k('bl', (t_h + 0.5, dict(o=0, x=-12)), (t_h + 0.9, dict(o=1, x=0), 'power2.out'))
    for i in range(4):
        fx.k(f'wp{i}', (t_fn - 0.55 + 0.06 * i, dict(dash=900)), (t_fn - 0.05 + 0.06 * i, dict(dash=0), 'power2.inOut'))
    custom = r"""window.CUSTOM=function(t,cam,H){const t0=%f;for(let i=0;i<4;i++){const p=document.getElementById('wp'+i);const c=document.getElementById('pl'+i);
      if(!p.__L) p.__L=p.getTotalLength(); const L=p.__L; const u=t-(t0+0.06*i); if(u<0){c.setAttribute('opacity',0);continue;}
      const f=(u*0.9)%%1; const pt=p.getPointAtLength(L*f); c.setAttribute('cx',pt.x.toFixed(1)); c.setAttribute('cy',pt.y.toFixed(1));
      c.setAttribute('opacity',(Math.min(1,u*4)*Math.sin(Math.PI*f)).toFixed(3));}
      const g=document.getElementById('card-core'); const q=H.cl((t-t0)/0.4,0,1);
      g.style.boxShadow='inset 0 1px 0 rgba(255,255,255,.06),0 0 '+(110+60*q*(0.6+0.4*Math.sin((t-t0)*6))).toFixed(1)+'px -30px rgba(47,149,255,.9),0 50px 120px -40px rgba(0,0,0,.85)';};"""% (t_fn + 0.0)
    moves = [dict(t=0.0, dur=r3(t_h - 0.25), kind='glide', to=dict(x=CXc, y=CYc, s=1.62)),
             dict(t=r3(t_h - 0.2), dur=1.35, kind='pull', to=dict(x=540, y=718, s=1.0)),
             dict(t=r3(t_h + 1.2), dur=r3(r['dur'] - t_h - 1.2), kind='glide', to=dict(x=540, y=716, s=1.015))]
    cfg = dict(id='s3_r5', dur=r['dur'], mode='fv', cam0=dict(x=CXc, y=CYc, s=1.6), cards=[under] + cards + [core], moves=moves, pushRef=1.6,
               heroes=[dict(t=0, id='none')], sfx=sfx((t_env - 0.22, 'pop')),
               thumb=[[r3(t_fn + 0.2), r['dur']]], wave=dict(level='low', k=0.8))
    mk('s3_r5', cfg, fx, custom)


# s3_r7 - fv: the Tools card (his iris bolt tile) as the hero with six empty slots; Claude Code's real tools snap in on
# "tools"; on "access" the wire to the model lights and the model glows.
TOOLS7 = [('file', 'Read'), ('pencil', 'Write'), ('edit', 'Edit'), ('term', 'Bash'), ('search', 'Grep'), ('globe', 'WebFetch')]


def s3_r7():
    r, ws = words('s3', 7)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    t_tools, t_acc = T('tools'), T('access')
    TW_, TH_ = 1000, 640
    slots = ''
    for i, (ic, nm) in enumerate(TOOLS7):
        x = 40 + (i % 2) * 470; y = 150 + (i // 2) * 150
        slots += f'<div class="abs" style="left:{x}px;top:{y}px;width:450px;height:124px;border-radius:22px;border:2px dashed {HAIR2}"></div>'
        slots += (f'<div id="tc{i}" class="abs fx" style="left:{x}px;top:{y}px;width:450px;height:124px;border-radius:22px;background:#fff;gap:22px;padding-left:30px;'
                  f'box-shadow:0 20px 40px -18px rgba(0,0,0,.7);opacity:0">{line_ico(ic, 46, INK, 2.1)}'
                  f'<div class="m" style="font-size:44px;color:{INK}">{nm}</div></div>')
    tools = dict(id='tools', kind='glass', highlight=True, x=540, y=470, w=TW_, h=TH_, clip=False, html=(
        tile('iris', 'bolt', 110, 8, style='left:30px;top:-52px') +
        f'<div class="abs" style="left:170px;top:30px;font:600 58px/1 Figtree;letter-spacing:-.025em">Tools</div>'
        f'<div class="abs lab" style="right:40px;top:44px">Harness</div>' + slots))
    core = dict(id='core', kind='glass', x=540, y=1094, w=460, h=210, html=core_html(), noDof=True)
    wire = dict(id='wire', kind='plain', x=540, y=890, w=20, h=200, clip=False, noDof=True, html=(
        f'<div class="abs" style="left:8px;top:0;width:4px;height:200px;border-radius:2px;background:{BAR}"></div>'
        f'<div id="wl" class="abs" style="left:8px;top:0;width:4px;height:200px;border-radius:2px;background:{AZ};box-shadow:0 0 14px rgba(47,149,255,.9);transform-origin:50% 0;transform:scaleY(0)"></div>'
        f'<div id="wd" class="abs" style="left:1px;top:0;width:18px;height:18px;border-radius:50%;background:#CFE7FF;box-shadow:0 0 14px #2F95FF;opacity:0"></div>'))
    for i in range(6):
        ti = t_tools - 0.2 + 0.11 * i
        fx.k(f'tc{i}', (ti, dict(o=0, y=70, s=1.08)), (ti + 0.12, dict(o=1), 'power2.out'), (ti + 0.36, dict(y=0, s=1), 'back.out(1.8)'))
    fx.k('wl', (t_acc - 0.3, dict(sy=0)), (t_acc + 0.1, dict(sy=1), 'power2.inOut'))
    custom = r"""window.CUSTOM=function(t){const t0=%f;const d=document.getElementById('wd');const u=t-t0;if(u<0){d.style.opacity=0;return;}
      const f=(u*1.4)%%1;d.style.transform='translateY('+(f*182).toFixed(1)+'px)';d.style.opacity=(Math.min(1,u*5)*Math.sin(Math.PI*f)).toFixed(3);
      const c=document.getElementById('card-core');const q=Math.min(1,u/0.35);c.style.borderColor='rgba(47,149,255,'+(0.09+0.4*q).toFixed(3)+')';
      c.style.boxShadow='inset 0 1px 0 rgba(255,255,255,.06),0 0 '+(120*q).toFixed(1)+'px -30px rgba(47,149,255,.85),0 50px 120px -40px rgba(0,0,0,.85)';};"""% (t_acc + 0.05)
    moves = [dict(t=0.0, dur=r['dur'], kind='glide', to=dict(x=540, y=716, s=1.02))]
    cfg = dict(id='s3_r7', dur=r['dur'], mode='fv', cam0=dict(x=540, y=720, s=1.0), cards=[wire, tools, core], moves=moves, pushRef=1.05,
               heroes=[dict(t=0, id='none')], sfx=sfx((t_tools - 0.2, 'pop'), (t_tools + 0.35, 'pop')),
               thumb=[[r3(t_acc + 0.2), r['dur']]], wave=dict(level='low', k=0.8))
    mk('s3_r7', cfg, fx, custom)


# s3_r8 - split (the long-form g05 checks terminal): his Checks card as a glass terminal with three checks queued; they
# arm on "checks", run one after another, and pass in mint on "test suites", "lint", "type check".
CHECKS = [('npm test', 'passed'), ('npm run lint', 'no problems'), ('npx tsc --noEmit', 'no errors')]


def s3_r8():
    r, ws = words('s3', 8)
    T = lambda w, n=1: W(ws, w, n)
    fx = FX()
    PW_, PH_ = 1000, 740
    t_enf, t_chk, t_exe = T('enforces'), T('checks'), T('executed')
    t_ok = [T('suites') - 0.05, T('lint') - 0.02, T('check.') - 0.05]
    t_run = [t_exe - 0.05, t_ok[0] + 0.12, t_ok[1] + 0.12]
    rows = ''
    for i, (cmd, res) in enumerate(CHECKS):
        y = 200 + i * 168
        rows += (f'<div class="abs" style="left:40px;top:{y - 16}px;width:{PW_ - 80}px;height:1px;background:{HAIR}"></div>' if i else '')
        rows += (f'<div id="dg{i}" class="abs" style="left:46px;top:{y + 14}px;width:30px;height:30px;border-radius:50%;background:{BAR}"></div>'
                 f'<div id="da{i}" class="abs" style="left:46px;top:{y + 14}px;width:30px;height:30px;border-radius:50%;background:{AZ};box-shadow:0 0 14px rgba(47,149,255,.8);opacity:0"></div>'
                 f'<div id="sp{i}" class="abs spin" style="left:40px;top:{y + 8}px;width:42px;height:42px;opacity:0"></div>'
                 f'<div class="abs m" style="left:110px;top:{y}px;font-size:44px;line-height:58px;white-space:nowrap"><span style="color:{AZ}">$</span> '
                 f'<span id="cm{i}" style="color:{T2}">{cmd}</span></div>'
                 f'<div id="rs{i}" class="abs m" style="left:146px;top:{y + 66}px;font-size:34px;line-height:44px;color:{MINT};opacity:0">✓ {res}</div>'
                 + tile('mint', 'check', 72, 0, id=f'tk{i}', style=f'left:{PW_ - 120}px;top:{y - 4}px;opacity:0', sm=True))
    panel = dict(id='chk', kind='glass', highlight=True, x=540, y=506, w=PW_, h=PH_, clip=False, html=(
        tile('mint', 'check', 112, 8, id='ct', style='left:30px;top:-54px') +
        f'<div class="abs" style="left:172px;top:34px;font:600 58px/1 Figtree;letter-spacing:-.025em">Checks</div>'
        f'<div class="abs lab" style="right:40px;top:48px">Harness</div>'
        f'<div class="abs" style="left:40px;top:128px;width:{PW_ - 80}px;height:1px;background:{HAIR2}"></div>' + rows +
        ring('cring', 32, AZ, 'rgba(47,149,255,.3)', 3)))
    fx.k('cring', (t_enf - 0.1, dict(o=0)), (t_enf + 0.35, dict(o=1)), (t_enf + 1.2, dict(o=0.55)))
    fx.k('ct', (t_enf - 0.05, dict(s=1)), (t_enf + 0.15, dict(s=1.14), 'power2.out'), (t_enf + 0.5, dict(s=1), 'back.out(2)'))
    for i in range(3):
        fx.k(f'da{i}', (t_chk - 0.1 + 0.08 * i, dict(o=0)), (t_chk + 0.1 + 0.08 * i, dict(o=1)), (t_run[i], dict(o=1)), (t_run[i] + 0.08, dict(o=0)))
        fx.k(f'sp{i}', (t_run[i], dict(o=0)), (t_run[i] + 0.1, dict(o=1)), (t_ok[i] - 0.05, dict(o=1)), (t_ok[i] + 0.05, dict(o=0)))
        fx.k(f'dg{i}', (t_ok[i] - 0.02, dict(o=1)), (t_ok[i] + 0.05, dict(o=0)))
        fx.k(f'rs{i}', (t_ok[i] - 0.02, dict(o=0, x=-10)), (t_ok[i] + 0.22, dict(o=1, x=0), 'power2.out'))
        fx.pop(f'tk{i}', t_ok[i] - 0.03, s0=0.4, dur=0.4)
    custom = r"""window.CUSTOM=function(t){const R=%s,K=%s;for(let i=0;i<3;i++){const s=document.getElementById('sp'+i);s.style.transform='rotate('+((t*420)%%360).toFixed(1)+'deg)';
      const c=document.getElementById('cm'+i);c.style.color=t>=R[i]?'#FFFFFF':'#A3A6AD';}};"""% (json.dumps([r3(x) for x in t_run]), json.dumps([r3(x) for x in t_ok]))
    moves = [dict(t=0.0, dur=r['dur'], kind='glide', to=dict(x=540, y=474, s=1.03))]
    cfg = dict(id='s3_r8', dur=r['dur'], mode='split', accent='azure', cam0=dict(x=540, y=470, s=1.0), cards=[panel], moves=moves, pushRef=1.03,
               heroes=[dict(t=0, id='chk')], sfx=sfx((t_ok[0], 'pop'), (t_ok[1], 'pop'), (t_ok[2], 'chime')),
               wave=dict(level='low', k=0.9))
    mk('s3_r8', cfg, fx, custom)


def build():
    for f in (s2_r0, s2_r1, s2_r2, s2_r3, s2_r5, s2_r6, s3_r0, s3_r2, s3_r3, s3_r4, s3_r5, s3_r7, s3_r8):
        f()
