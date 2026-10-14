# Graphics agent A - "Harness engineering" pro edit: the hook (g01 g02 g03), "what is an agent" (r01 g04 g05 g06
# r02 g07 g08) and Level 1 (g09 r03 g10 g11 g12).
# Build: $PY scripts/build_gfx.py a        (one beat or a few: GFX_A=g01,g02 $PY scripts/build_gfx.py a)
#
# BRAND (v2): every scene follows Leon's channel design system "Leon YouTube" (C:\cognaitiv-ai\design-system\
# leon-youtube): the graphite stage with its beams and the animated horizon wave (engine default theme 'stage'),
# explanations on frosted GLASS panels, real product UI / chats / files / captures on white WINDOW / PAPER cards,
# Figtree 500/600 + Geist Mono labels, azure accent, ember for warnings / refusals / secrets, mint for passes, his glossy
# icon tiles (tile_html: Configure = azure code, Build = iris bolt, Orchestrate = mint eyes + antenna, Memory = ember
# bars, Checks = mint check). No clay, no Poppins, no white world. The white-world version is kept in git history /
# the scratchpad backup; timings, cues, camera moves and SFX are unchanged from it.
#
# Every page = engine.js (world camera, cards, DOF, captures, stage) + a small keyframe library (LIB below) that runs
# from window.CFG_RENDER: per-element keyframe tracks (opacity / translate / scale / rotate / blur / width / clip),
# typed text with an accent caret, counters and class toggles - all pure functions of t, so renders are seek-safe.
import os, json, shutil
from build_gfx_common import *
from build_gfx_common import beat as _beat

ONLY = [s for s in os.environ.get('GFX_A', '').split(',') if s]

# design-system tokens (tokens/colors.css)
WHITE, T2, TM = '#FFFFFF', '#A3A6AD', '#7E818A'                       # text on the stage
AZ, EMB, MINT, IRIS = '#2F95FF', '#FF8A5B', '#4FD6A0', '#9C7CFF'
INK, INK2, PAPER2, PLINE = '#111214', '#5F636B', '#F3F4F6', '#ECEDF0'  # paper UI
AZINK, AZWASH, EMINK, EMWASH, MINTINK, MINTWASH = '#1560D0', '#E8F2FF', '#B8461A', '#FFEFE7', '#0F7A52', '#E3F8EF'
BAR, HAIR, HAIR2 = '#5A5D64', 'rgba(255,255,255,.09)', 'rgba(255,255,255,.16)'
AZGLOW = '0 0 24px rgba(47,149,255,.45)'
LOGOS_NEW = 'captures/logos'
LOGOS_OLD = 'C:/Users/leon/AppData/Local/video-pro-edit/ai-practitioners-summit__YTHD60/captures/logos'

EXTRA_CSS = """
.abs{position:absolute}
.caret{background:var(--accent)}
.m{font-family:'Geist Mono',ui-monospace,monospace}
.cr{display:inline-block;width:4px;height:1.05em;background:var(--accent);vertical-align:-0.16em;margin-left:2px;border-radius:2px;box-shadow:0 0 12px rgba(47,149,255,.7)}
.lab{font:500 22px/1.2 'Geist Mono';letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);white-space:nowrap}
.lab.acc{color:var(--accent)}.lab.wh{color:#fff}.lab.ember{color:#FF8A5B}.lab.mint{color:#4FD6A0}
.pl{display:inline-block;font:500 20px/1 'Geist Mono';letter-spacing:.08em;text-transform:uppercase;padding:10px 16px;border-radius:999px;white-space:nowrap}
.pl.mint{background:#E3F8EF;color:#0F7A52}.pl.ember{background:#FFEFE7;color:#B8461A}.pl.az{background:#E8F2FF;color:#1560D0}.pl.neutral{background:#F3F4F6;color:#5F636B}
.tile.sm{box-shadow:inset 0 2px 1px rgba(255,255,255,.55),inset 0 -6px 10px rgba(0,0,0,.2),0 10px 20px -8px rgba(0,0,0,.35)}
.tile.lockd{background:linear-gradient(155deg,#43454C 0%,#2E3035 50%,#1D1E22 100%);box-shadow:inset 0 2px 1px rgba(255,255,255,.18),inset 0 -10px 18px rgba(0,0,0,.45),0 22px 44px -16px rgba(0,0,0,.8)}
.tile .stick{position:absolute;left:50%;border-radius:999px}.tile .ball{position:absolute;left:50%;border-radius:50%}
.tile.mint .stick{background:linear-gradient(180deg,#C4F6DF,#2DB883)}.tile.mint .ball{background:radial-gradient(circle at 35% 30%,#fff 0%,#C4F6DF 35%,#2DB883 100%)}
"""

# ---------------------------------------------------------------------------------------------------------------
# keyframe library (JS). Data comes in window.FX = {tr, ty, num, cls}
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
  if('cr' in v) el.style.clipPath=`inset(-20px ${cl(v.cr,0,100).toFixed(3)}% -20px -20px)`;
  if('cb' in v) el.style.clipPath=`inset(-20px -20px ${cl(v.cb,0,100).toFixed(3)}% -20px)`;
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
function fmt(v,f){ if(f==='pct') return Math.round(v)+'%'; if(f==='k') return Math.round(v)+'K'; if(f==='1f') return v.toFixed(1); if(f==='comma') return Math.round(v).toLocaleString('en-US'); return String(Math.round(v)); }
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

DEF = dict(o=1, x=0, y=0, s=1, sx=1, sy=1, r=0, b=0, cr=0, cb=0, dash=0)


class FX:
    """per-page animation data"""

    def __init__(self):
        self.raw = {}; self.ty = []; self.num = []; self.cls = []; self.hold = {}

    def k(self, el, *frames):
        """keyframes for one element: (t, {props}) or (t, {props}, ease) - ease of the segment that ENDS at t.
        NB: a frame that sets only some props carries the others at their previous KEYFRAME value, so animate
        independent props on separate (nested) elements."""
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
            for k in keys:                      # a key first set later keeps its first value before that (e.g. w)
                if k not in DEF:
                    cur[k] = next(f[1][k] for f in frames if k in f[1])
            kf = []
            for f in frames:
                cur = {**cur, **f[1]}
                kf.append([round(f[0], 3), {k: round(v, 3) for k, v in cur.items()}, f[2] if len(f) > 2 else 'power2.inOut'])
            tr.append(dict(el=el, kf=kf, hold=self.hold.get(el, True)))
        data = dict(tr=tr, ty=self.ty, num=self.num, cls=self.cls)
        return 'window.FX=' + json.dumps(data) + ';\n' + (custom or '') + '\n' + LIB


# ---------------------------------------------------------------------------------------------------------------
# brand building blocks
LOCK_GLYPH = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24"><g id="{id}s"><path d="M8 11V8.2a4 4 0 0 1 8 0V11" fill="none" stroke="#fff" '
              'stroke-width="2.4" stroke-linecap="round"/></g><rect x="5.5" y="10.5" width="13" height="10" rx="2.6" fill="#fff"/>'
              '<circle cx="12" cy="15" r="1.5" fill="#2E3035"/></svg>')
HOOK_GLYPH = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24"><g fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" '
              'stroke-linejoin="round"><circle cx="14.5" cy="4.2" r="2"/><path d="M14.5 6.3v8.2a4.6 4.6 0 0 1-9.2 0v-1.5l2.5 1.9"/></g></svg>')
X_GLYPH = '<svg width="{s}" height="{s}" viewBox="0 0 24 24"><path d="M7 7l10 10M17 7L7 17" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round"/></svg>'


def tile(color='azure', glyph='code', size=116, tilt=-8, id=None, style='', antenna=False, svg_markup=None, sm=False):
    """the design system's glossy icon tile in a positioned wrapper (#id); color azure|iris|ember|mint|lockd"""
    g = svg_markup.format(s=round(size * 0.5), id=id or 'x') if svg_markup else None
    h = tile_html('azure' if color == 'lockd' else color, glyph, size, tilt, svg=g)
    if color == 'lockd': h = h.replace('class="tile azure"', 'class="tile lockd"', 1)
    if sm: h = h.replace('class="tile ', 'class="tile sm ', 1)
    if antenna:
        st, bl = max(4, round(size * 0.075)), round(size * 0.18)
        ant = (f'<span class="stick" style="width:{st}px;height:{round(size * .2)}px;top:{-round(size * .18)}px;margin-left:{-st / 2}px"></span>'
               f'<span class="ball" style="width:{bl}px;height:{bl}px;top:{-round(size * .3)}px;margin-left:{-bl / 2}px"></span>')
        h = h.replace('">', '">' + ant, 1)
    idh = f' id="{id}"' if id else ''
    return f'<div{idh} class="abs" style="width:{size}px;height:{size}px;{style}">{h}</div>'


def check_badge(id, size=56, style=''):
    """a pass: the small mint check tile (his slides' Checks tile)"""
    return tile('mint', 'check', size, 0, id=id, style=style, sm=size < 72)


def cross_badge(id, size=56, style=''):
    """a refusal / failure: an ember tile with an x"""
    return tile('ember', None, size, 0, id=id, style=style, svg_markup=X_GLYPH, sm=size < 72)


def hook_badge(id, size=50, style='', tilt=0):
    return tile('azure', None, size, tilt, id=id, style=style, svg_markup=HOOK_GLYPH, sm=size < 72)


def lock_tile(n, size, style):
    """a locked level: a graphite tile carrying a white padlock (#lk{n}; shackle group #lk{n}s)"""
    return tile('lockd', None, size, -6, id=f'gsq{n}', style=style, svg_markup=LOCK_GLYPH.replace('{id}', f'lk{n}').replace('{s}', '{s}')) \
        .replace('<svg width', f'<svg id="lk{n}" style="overflow:visible" width', 1)


def asset(name, src_candidates):
    """copy the first existing logo/capture into gfx/assets/<name> and record its size; returns (path, w, h)"""
    from PIL import Image
    dst = f'gfx/assets/{name}'
    for s in src_candidates:
        if os.path.exists(s):
            if not os.path.exists(dst) or os.path.getmtime(s) > os.path.getmtime(dst):
                shutil.copyfile(s, dst)
            w, h = Image.open(dst).size
            d = json.load(open('gfx/asset_dims.json')) if os.path.exists('gfx/asset_dims.json') else {}
            if d.get(name) != [w, h]:
                d[name] = [w, h]; json.dump(d, open('gfx/asset_dims.json', 'w'), indent=1)
            D[name] = [w, h]
            return f'assets/{name}', w, h
    raise FileNotFoundError(f'{name}: none of {src_candidates}')


def logo(name, file=None):
    """an official logo: the research agent's copy (captures/logos) first, then the previous project's"""
    file = file or name
    return asset(name, [f'{LOGOS_NEW}/{file}', f'{LOGOS_OLD}/{file}'])


def img(src, w, h, style=''):
    return f'<img src="{src}" class="abs" style="width:{w}px;height:{h}px;object-fit:contain;{style}">'


def T(ws, word, n=1):
    return W(ws, word, n)


def r3(v):
    return round(v, 3)


def keyrun(t0, n, cps, every=2):
    """key ticks while text types (audio.py joins ticks < 0.35 s apart into one typing clip)"""
    return [dict(t=r3(t0 + i / cps), type='key') for i in range(0, n, every)]


def svg(inner, x, y, w, h=None, style=''):
    h = h or w
    return f'<svg viewBox="0 0 24 24" class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:visible;{style}">{inner}</svg>'


def chip(x, y, inner_html, w, h=58, id=None, bg=PAPER2, border=PLINE):
    """a chip inside paper (radius 14)"""
    idh = f' id="{id}"' if id else ''
    return (f'<div{idh} class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:14px;background:{bg};border:1.5px solid {border}">'
            f'{inner_html}</div>')


def file_icon(x, y, h=40, color=AZINK, fill='#fff'):
    w = h * 0.8
    return (f'<svg class="abs" viewBox="0 0 20 25" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<path d="M2.5 1.5h10l5 5v17h-15z" fill="{fill}" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M12.5 1.5v5h5" fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M5.5 12h9M5.5 16h9M5.5 20h6" stroke="{color}" stroke-width="1.4" stroke-linecap="round"/></svg>')


def ring(id, radius, color=AZ, glow='rgba(47,149,255,.55)', width=3, op=0):
    """an outline overlay for a card (inside it): accent hairline + inner glow, animated by opacity"""
    return (f'<div id="{id}" class="abs" style="inset:0;border-radius:{radius}px;box-shadow:inset 0 0 0 {width}px {color},inset 0 0 36px {glow};'
            f'opacity:{op};pointer-events:none"></div>')


def dot(id, color, x, y, size=16, op=1, glow=False):
    g = f';box-shadow:0 0 12px {color}' if glow else ''
    return f'<div id="{id}" class="abs" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;border-radius:50%;background:{color};opacity:{op}{g}"></div>'


def bez(p0, p1, p2, p3, n=8):
    out = []
    for i in range(n + 1):
        u = i / n
        x = (1 - u) ** 3 * p0[0] + 3 * (1 - u) ** 2 * u * p1[0] + 3 * (1 - u) * u * u * p2[0] + u ** 3 * p3[0]
        y = (1 - u) ** 3 * p0[1] + 3 * (1 - u) ** 2 * u * p1[1] + 3 * (1 - u) * u * u * p2[1] + u ** 3 * p3[1]
        out.append((x, y))
    return out


# white line icons (24 px grid, 1.7-2 stroke, round caps) - the design system's line-icon rule
def li(path, c=WHITE, w=2):
    return f'<path d="{path}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


PENCIL = 'M4 20l1-4.2L15.6 5.2a2 2 0 0 1 2.8 0l.4.4a2 2 0 0 1 0 2.8L8.2 19 4 20z'
GLOBE_P = 'M12 3.5a8.5 8.5 0 1 0 0 17a8.5 8.5 0 1 0 0-17zM3.5 12h17M12 3.5c2.6 2.4 3.6 5.2 3.6 8.5s-1 6.1-3.6 8.5M12 3.5c-2.6 2.4-3.6 5.2-3.6 8.5s1 6.1 3.6 8.5'
CHEV = 'M6 9.5l6 6 6-6'
ARROW_P = 'M3 12h16M13 6l6 6-6 6'
FOLDER_P = 'M2.5 6.5a2 2 0 0 1 2-2h4.6l2.2 2.4h8.2a2 2 0 0 1 2 2v9.6a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2z'
FOLDER_OPEN = ('<path d="M2.5 6.5a2 2 0 0 1 2-2h4.6l2.2 2.4h8.2a2 2 0 0 1 2 2v1.4H6.6a2 2 0 0 0-1.9 1.4L2.5 18.4z" fill="{fill}" stroke="{stroke}" stroke-width="1.4" stroke-linejoin="round"/>'
               '<path d="M4.6 12.2a2 2 0 0 1 1.9-1.5h15.3l-2.3 7.8a2 2 0 0 1-1.9 1.4H2.5z" fill="{front}" stroke="{stroke}" stroke-width="1.4" stroke-linejoin="round"/>')
LOCK_SVG = '<rect x="5" y="10.5" width="14" height="10" rx="2.6" fill="{c}"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5" fill="none" stroke="{c}" stroke-width="2.2"/>'
BRANCH_SVG = ('<g fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"><circle cx="6" cy="5" r="2.2"/><circle cx="6" cy="19" r="2.2"/>'
              '<circle cx="18" cy="7" r="2.2"/><path d="M6 7.2v9.6M18 9.2c0 5-6 4-11 7.6"/></g>')


def win_head(logo_src, title, badge=None, w=0, logo_sz=40, mono_title=False, extra=''):
    """the ProductWindow header: logo + title (ink), an optional mono badge on the right, a paper-line divider at y 84"""
    ft = "font:600 32px/48px 'Geist Mono'" if mono_title else 'font:600 32px/48px Figtree;letter-spacing:-.01em'
    b = (f'<div class="abs m" style="right:30px;top:24px;font-size:22px;line-height:22px;padding:10px 14px;border-radius:999px;background:{PAPER2};color:{INK2}">{badge}</div>'
         if badge else '')
    lg = img(logo_src, logo_sz, logo_sz, f'left:34px;top:{42 - logo_sz / 2}px') if logo_src else ''
    return (lg + f'<div class="abs" style="left:{34 + (logo_sz + 16 if logo_src else 0)}px;top:18px;{ft};color:{INK};white-space:nowrap">{title}</div>' + b + extra +
            f'<div class="abs" style="left:0;top:84px;width:100%;height:1.5px;background:{PLINE}"></div>')


# ---------------------------------------------------------------------------------------------------------------
# g01 - fvp, the harness you're handed: Claude Code at frame 0, Codex and OpenCode land on their names while the
# camera steps across (glass tiles with the real marks); Claude Code is picked and the camera pushes onto its settings
# window (white product UI), where model / memory files / hooks / tools snap in as named; "that's it" settles
# everything with a mint ring and check.
def product_tile(icon_html, name):
    return (f'<div class="abs" style="left:0;top:38px;width:100%;height:150px;display:flex;justify-content:center;align-items:center">{icon_html}</div>'
            f'<div class="abs" style="left:0;top:204px;width:100%;text-align:center;font:600 44px/1.2 Figtree;letter-spacing:-.025em;color:{WHITE}">{name}</div>')


def g01():
    b, ws = words('g01')
    fx = FX()
    claude, _, _ = logo('claude_symbol.png')
    codex, _, _ = asset('codex_app_icon.png', [f'{LOGOS_NEW}/codex_app_icon_openai_blossom.png'])
    oc, _, _ = logo('opencode-logo-dark.png')                       # light artwork for the glass
    t_cc, t_cx, t_oc = T(ws, 'claude'), T(ws, 'codex'), T(ws, 'opencode')
    t_conf, t_model, t_mem, t_hooks, t_tools, t_that = T(ws, 'configure'), T(ws, 'model'), T(ws, 'memory'), T(ws, 'hooks'), T(ws, 'tools'), T(ws, 'thats')
    TY_ = 330; xs = [334, 784, 1234]; TW_, TH_ = 400, 300
    cc_icon = f'<img src="{claude}" style="width:132px;height:132px">'
    cx_icon = f'<img src="{codex}" style="width:150px;height:150px;border-radius:34px">'
    oc_icon = f'<img src="{oc}" style="width:106px;height:132px">'
    # settings window for the chosen harness (white product UI)
    SX_, SY_, SW_, SH_ = 784, 960, 860, 600
    rowy = [118, 236, 354, 472]
    lab = lambda y, t: f'<div class="abs" style="left:44px;top:{y + 8}px;font:500 30px/44px Figtree;color:{INK2}">{t}</div>'
    V = 260                                       # value column x
    mono = lambda x, t, w=None: f'<div class="abs m" style="left:{x}px;top:6px;font-size:30px;line-height:44px;color:{INK};white-space:nowrap">{t}</div>'
    r_model = (lab(rowy[0], 'Model') +
               chip(V, rowy[0], img(claude, 34, 34, 'left:20px;top:12px') +
                    f'<div class="abs" style="left:68px;top:6px;font:600 32px/44px Figtree;color:{INK}">Opus 5.5</div>' + svg(li(CHEV, INK2, 2.4), 300, 14, 30),
                    350, h=60, bg='#fff', border='#D7D9DE'))
    mchip = lambda x, name: chip(x, rowy[1], file_icon(16, 11, 34) + mono(54, name), 236)
    r_mem = lab(rowy[1], 'Memory') + mchip(V, 'AGENTS.md') + mchip(V + 252, 'CLAUDE.md')
    r_hook = (lab(rowy[2], 'Hooks') +
              chip(V, rowy[2], hook_badge('', 38, 'left:11px;top:9px') + mono(62, 'Stop') + svg(li(ARROW_P, INK2, 2.4), 148, 15, 28) + mono(188, 'verify.sh'), 380))
    tchip = lambda x, icon, name, w: chip(x, rowy[3], icon + mono(58, name), w)
    r_tools = (lab(rowy[3], 'Tools') +
               tchip(V, f'<div class="abs m" style="left:14px;top:6px;font-size:28px;line-height:44px;color:{INK};font-weight:700">&gt;_</div>', 'shell', 170) +
               tchip(V + 184, svg(li(PENCIL, INK, 2), 16, 14, 30), 'edit', 150) +
               tchip(V + 348, svg(li(GLOBE_P, INK, 2), 16, 14, 30), 'web', 136))
    rows = ''.join(f'<div id="row{i}" class="abs" style="left:0;top:0;width:100%;height:100%;opacity:0">{r}</div>'
                   for i, r in enumerate([r_model, r_mem, r_hook, r_tools]))
    sett = (win_head(claude, 'Claude Code', w=SW_, logo_sz=44) +
            ''.join(f'<div class="abs" style="left:44px;top:{y - 9}px;width:{SW_ - 88}px;height:1px;background:{PLINE}"></div>' for y in rowy[1:]) + rows +
            ring('setring', 22, MINT, 'rgba(79,214,160,.25)', 4) + check_badge('setok', 56, style=f'left:{SW_ - 100}px;top:14px;opacity:0'))
    tring = ring('ccring', 28)
    cards = [dict(id='cc', kind='glass', x=xs[0], y=TY_, w=TW_, h=TH_, html=product_tile(cc_icon, 'Claude Code') + tring),
             dict(id='cx', kind='glass', x=xs[1], y=TY_, w=TW_, h=TH_, html=product_tile(cx_icon, 'Codex'), land=dict(t=r3(t_cx - 0.1), dur=0.5)),
             dict(id='oc', kind='glass', x=xs[2], y=TY_, w=TW_, h=TH_, html=product_tile(oc_icon, 'OpenCode'), land=dict(t=r3(t_oc - 0.1), dur=0.5)),
             dict(id='set', kind='window', x=SX_, y=SY_, w=SW_, h=SH_, html=sett)]
    S1 = 1.22
    t_pull = t_oc + 0.42
    cards[3]['land'] = dict(t=r3(t_pull + 0.08), dur=0.55)
    fx.k('ccring', (t_pull + 0.3, dict(o=0)), (t_pull + 0.6, dict(o=1), 'power2.out'))
    for i, tw in enumerate([t_model, t_mem, t_hooks, t_tools]):
        fx.k(f'row{i}', (tw - 0.12, dict(o=0, y=16, s=0.985)), (tw + 0.22, dict(o=1, y=0, s=1), 'power3.out'))
    fx.k('setring', (t_that - 0.1, dict(o=0)), (t_that + 0.4, dict(o=1)))
    fx.k('setok', (t_that - 0.08, dict(o=0, s=0.4)), (t_that + 0.32, dict(o=1, s=1), 'back.out(2.4)'))
    moves = [dict(t=t_cx - 0.25, dur=0.5, kind='step', to=dict(x=xs[1], y=TY_, s=S1)),
             dict(t=t_oc - 0.25, dur=0.5, kind='step', to=dict(x=xs[2], y=TY_, s=S1)),
             dict(t=t_pull, dur=0.75, kind='pull', to=dict(x=784, y=430, s=0.92)),
             dict(t=t_conf - 0.25, dur=1.0, kind='push', to=dict(x=SX_, y=SY_ - 4, s=1.2)),
             dict(t=t_conf + 0.8, dur=t_that - 0.25 - t_conf - 0.8, kind='glide', to=dict(x=SX_, y=SY_ + 6, s=1.235)),
             dict(t=t_that - 0.2, dur=b['dur'] - t_that + 0.2, kind='glide', to=dict(x=SX_, y=SY_, s=1.2))]
    cfg = dict(id='g01', dur=b['dur'], mode='fvp', cam0=dict(x=xs[0], y=TY_, s=S1), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=1.0),
               heroes=[dict(t=0, id='cc'), dict(t=t_cx - 0.15, id='cx'), dict(t=t_oc - 0.15, id='oc'), dict(t=t_pull, id='none'),
                       dict(t=t_conf - 0.2, id='set')],
               # lead: thinned from 8 to 5 under the hook's dialogue + music (every other row clicks)
               sfx=[dict(t=r3(t_cx - 0.1), type='pop'), dict(t=r3(t_oc - 0.1), type='pop')] +
                   [dict(t=r3(tw - 0.1), type='click') for tw in (t_model, t_hooks)] +
                   [dict(t=r3(t_that), type='chime')])
    page('g01', cfg, extra_css=EXTRA_CSS, extra_js=fx.js())


# ---------------------------------------------------------------------------------------------------------------
# g02 - split, "only level one ... most people never get past it": a staircase of glass level panels (his card-row
# style, tile on the top-left edge); 1 Configure lit, 2 and 3 locked; a crowd drops onto level 1 and bumps into 2.
def level_card_small(n, color, glyph, name, locked):
    """340x270 staircase glass card (g02); the tile sits on the card's top-left edge"""
    # the tile sits inside the card here (the crowd stands on the card's top edge)
    if not locked:
        return (tile(color, glyph, 80, -8, id=f'ic{n}', style='left:30px;top:28px') +
                f'<div class="abs lab acc" style="left:32px;top:136px">Level {n}</div>'
                f'<div class="abs" style="left:32px;top:172px;font:600 52px/1.1 Figtree;letter-spacing:-.025em;color:{WHITE}">{name}</div>'
                + ring(f'glow{n}', 28))
    return (lock_tile(n, 80, 'left:30px;top:28px') +
            f'<div class="abs lab" style="left:32px;top:136px">Level {n}</div>'
            f'<div class="abs" style="left:32px;top:184px;width:230px;height:36px;border-radius:18px;background:rgba(255,255,255,.10);filter:blur(7px)"></div>')


P_SC = 1.45                                     # person pictogram size factor (26x44 base)


def person(i, x, y, c, sc=1.0):
    w, h = 26 * P_SC, 44 * P_SC
    return (f'<div id="p{i}" class="abs" style="left:{x}px;top:{y}px;width:{w:.1f}px;height:{h:.1f}px;transform-origin:50% 100%">'
            f'<div style="transform:scale({sc});transform-origin:50% 100%;width:{w:.1f}px;height:{h:.1f}px;position:relative">'
            f'<div class="abs" style="left:{5 * P_SC:.1f}px;top:0;width:{16 * P_SC:.1f}px;height:{16 * P_SC:.1f}px;border-radius:50%;background:{c}"></div>'
            f'<div class="abs" style="left:0;top:{19 * P_SC:.1f}px;width:{w:.1f}px;height:{25 * P_SC:.1f}px;border-radius:{13 * P_SC:.1f}px {13 * P_SC:.1f}px {5 * P_SC:.1f}px {5 * P_SC:.1f}px;background:{c}"></div></div></div>')


def g02():
    b, ws = words('g02')
    fx = FX()
    CW_, CH_ = 340, 270
    cards = [dict(id='l1', kind='glass', x=240, y=770, w=CW_, h=CH_, html=level_card_small(1, 'azure', 'code', 'Configure', False), clip=False,
                  group='st', sharpWithGroup=True),
             dict(id='l2', kind='glass', x=600, y=600, w=CW_, h=CH_, html=level_card_small(2, 'iris', 'bolt', '', True), clip=False, group='st', sharpWithGroup=True),
             dict(id='l3', kind='glass', x=960, y=430, w=CW_, h=CH_, html=level_card_small(3, 'mint', 'eyes', '', True), clip=False)]
    # the crowd: a plain layer over level 1 + the left edge of level 2
    top1 = 770 - CH_ / 2                       # level 1 top edge (feet line) = 635
    wall = 600 - CW_ / 2                        # level 2 left edge = 430
    LX, LY = 60, 300                            # layer origin (world)
    PW, PH = 26 * P_SC, 44 * P_SC
    cols = ['#FFFFFF', '#A3A6AD', AZ, '#E6E7EA', '#7E818A', '#C9CBD1', '#FFFFFF']
    back = [(104 + 44 * i, '#5A5D64' if i % 3 else '#2F6FB8') for i in range(6)]
    front = [(80 + 44 * i, cols[i]) for i in range(7)]
    html = ''; order = []
    for i, (x, c) in enumerate(back):
        pid = f'b{i}'; html += person(pid, x - LX, top1 - 7 - PH - LY, c, 0.84); order.append((pid, x, 'b'))
    for i, (x, c) in enumerate(front):
        pid = f'f{i}'; html += person(pid, x - LX, top1 - PH - LY, c); order.append((pid, x, 'f'))
    cards.append(dict(id='crowd', kind='plain', x=LX + 200, y=LY + 170, w=400, h=340, html=f'<div class="abs" style="left:0;top:0">{html}</div>',
                      clip=False, noDof=True, group='st', sharpWithGroup=True))

    t_only, t_one, t_most, t_never, t_past = T(ws, 'only'), T(ws, 'one'), T(ws, 'most'), T(ws, 'never'), T(ws, 'past')
    import random
    rnd = random.Random(7)
    seq = list(range(len(order))); rnd.shuffle(seq)
    for j, idx in enumerate(seq):
        pid, x, row = order[idx]
        tl = t_most + 0.04 * j
        fx.k(f'p{pid}', (tl - 0.42, dict(y=-360, o=0, sx=1, sy=1)), (tl - 0.32, dict(o=1), 'linear'),
             (tl, dict(y=0), 'power2.in'), (tl + 0.07, dict(sx=1.1, sy=0.84), 'power1.out'), (tl + 0.26, dict(sx=1, sy=1), 'power2.out'))
    fr = max(x for _, x, r in order if r == 'f') + PW     # front-most right edge
    gap = wall - 2 - fr
    ranked = sorted(order, key=lambda o: -o[1])
    hit1, hit2 = t_never + 0.26, t_past + 0.12
    for j, (pid, x, row) in enumerate(ranked):
        dx = gap + j * 3.0
        fx.k(f'p{pid}', (t_never - 0.24 + 0.01 * j, dict(x=0)), (hit1 + 0.012 * j, dict(x=dx), 'power2.in'),
             (hit1 + 0.34, dict(x=dx - 30), 'power2.out'),
             (t_past - 0.22, dict(x=dx - 26), 'sine.inOut'), (hit2 + 0.012 * j, dict(x=dx), 'power2.in'),
             (hit2 + 0.36, dict(x=dx - 24), 'power2.out'))
        if j == 0:   # the one at the front squashes against the edge
            fx.k(f'p{pid}', (hit1, dict(sx=1, sy=1)), (hit1 + 0.06, dict(sx=0.86, sy=1.04), 'power2.out'), (hit1 + 0.22, dict(sx=1, sy=1)),
                 (hit2, dict(sx=1, sy=1)), (hit2 + 0.06, dict(sx=0.88, sy=1.03), 'power2.out'), (hit2 + 0.22, dict(sx=1, sy=1)))
    # level 2 holds: its lock tile rattles on each hit, an ember flash on its edge (a refusal)
    fx.k('gsq2', (hit1 - 0.01, dict(r=0)), (hit1 + 0.06, dict(r=-12), 'power2.out'), (hit1 + 0.17, dict(r=8)), (hit1 + 0.3, dict(r=-4)), (hit1 + 0.45, dict(r=0)),
         (hit2 - 0.01, dict(r=0)), (hit2 + 0.06, dict(r=-9), 'power2.out'), (hit2 + 0.17, dict(r=5)), (hit2 + 0.32, dict(r=0)))
    fx.k('l2edge', (hit1 - 0.02, dict(o=0)), (hit1 + 0.05, dict(o=1), 'power2.out'), (hit1 + 0.55, dict(o=0)),
         (hit2 - 0.02, dict(o=0)), (hit2 + 0.05, dict(o=0.8), 'power2.out'), (hit2 + 0.55, dict(o=0)))
    cards[1]['html'] += ('<div id="l2edge" class="abs" style="left:0;top:0;width:100%;height:100%;border-radius:28px;opacity:0;'
                         'box-shadow:inset 3px 0 0 #FF8A5B,inset 26px 0 30px -20px rgba(255,138,91,.55)"></div>')
    # level 1 lights up on "one" (accent hairline + bloom)
    fx.k('glow1', (t_one - 0.15, dict(o=0)), (t_one + 0.25, dict(o=1)))
    fx.k('ic1', (t_one - 0.12, dict(s=1)), (t_one + 0.08, dict(s=1.12), 'power2.out'), (t_one + 0.4, dict(s=1), 'back.out(2)'))

    moves = [dict(t=t_only - 0.25, dur=1.3, kind='push', to=dict(x=372, y=700, s=1.52)),
             dict(t=t_only + 1.15, dur=t_never - 0.3 - t_only - 1.15, kind='glide', to=dict(x=376, y=698, s=1.555))]
    cfg = dict(id='g02', dur=b['dur'], mode='split', cam0=dict(x=600, y=588, s=1.0), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=0.8),
               heroes=[dict(t=0, id='none'), dict(t=t_only - 0.1, id='l1')],
               sfx=[dict(t=r3(t_most + 0.1), type='pop'), dict(t=r3(hit1), type='pop')])
    page('g02', cfg, extra_css=EXTRA_CSS, extra_js=fx.js())


# ---------------------------------------------------------------------------------------------------------------
# g03 - fvp, "the three levels of Harness Engineering": his "Three levels" slide in motion - three glass cards with
# their tiles on the top-left edge; 2 and 3 are locked (continuity with g02) and unlock on "three levels".
LEVELS = [('azure', 'code', False, 'Configure', 'Shape a tool you already use', 'AGENTS.md · hooks · mods'),
          ('iris', 'bolt', False, 'Build', 'Write your own harness on a model API or SDK', 'e.g. SMOL Coder'),
          ('mint', 'eyes', True, 'Orchestrate', 'Run a harness around many agents', 'e.g. cubefarm')]


def level_card(n, color, glyph, antenna, name, desc, eg, w=420):
    real = (tile(color, glyph, 104, -8 if n % 2 else 8, id=f'ic{n}', style='left:32px;top:-46px', antenna=antenna) +
            f'<div class="abs lab" style="left:40px;top:92px">Level {n}</div>'
            f'<div class="abs" style="left:40px;top:128px;font:600 54px/1.1 Figtree;letter-spacing:-.025em;color:{WHITE}">{name}</div>'
            f'<div id="d{n}" class="abs" style="left:40px;top:204px;width:{w - 70}px;font:400 30px/1.4 Figtree;color:{T2}">{desc}</div>'
            f'<div class="abs m" style="left:40px;top:360px;font-size:20px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:{AZ};white-space:nowrap">{eg}</div>')
    if n == 1:
        return f'<div id="real{n}" class="abs" style="inset:0">{real}</div>'
    frost = (f'<div class="abs lab" style="left:40px;top:92px">Level {n}</div>'
             f'<div class="abs" style="left:40px;top:140px;width:250px;height:40px;border-radius:20px;background:rgba(255,255,255,.10);filter:blur(8px)"></div>'
             f'<div class="abs" style="left:40px;top:214px;width:320px;height:24px;border-radius:12px;background:rgba(255,255,255,.06);filter:blur(8px)"></div>'
             f'<div class="abs" style="left:40px;top:256px;width:220px;height:24px;border-radius:12px;background:rgba(255,255,255,.06);filter:blur(8px)"></div>')
    return (f'<div id="frost{n}" class="abs" style="inset:0">{frost}</div>'
            f'<div id="real{n}" class="abs" style="inset:0;opacity:0">{real}</div>' + lock_tile(n, 104, 'left:32px;top:-46px'))


def g03():
    b, ws = words('g03')
    fx = FX()
    xs = [328, 784, 1240]; Y = 570; CW_, CH_ = 420, 430
    cards = [dict(id=f'c{i + 1}', kind='glass', x=xs[i], y=Y, w=CW_, h=CH_, html=level_card(i + 1, *LEVELS[i]), clip=False) for i in range(3)]
    t3, tl = T(ws, 'three'), T(ws, 'levels')
    fx.k('d1', (t3 - 0.1, dict(o=0, y=10)), (t3 + 0.35, dict(o=1, y=0), 'power3.out'))
    for n, tu in ((2, t3 - 0.08), (3, tl - 0.12)):
        fx.k(f'lk{n}s', (tu, dict(y=0)), (tu + 0.14, dict(y=-4), 'power2.out'))
        fx.k(f'gsq{n}', (tu + 0.14, dict(s=1, o=1)), (tu + 0.36, dict(s=0.82, o=0), 'power2.in'))
        fx.k(f'frost{n}', (tu + 0.12, dict(o=1)), (tu + 0.45, dict(o=0)))
        fx.k(f'real{n}', (tu + 0.14, dict(o=0, b=10)), (tu + 0.55, dict(o=1, b=0), 'power2.out'))
        fx.k(f'ic{n}', (tu + 0.14, dict(s=0.62)), (tu + 0.66, dict(s=1), 'back.out(2.2)'))
    moves = [dict(t=2.0, dur=b['dur'] - 2.0, kind='push', to=dict(x=784, y=Y + 4, s=1.06))]
    cfg = dict(id='g03', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=Y - 10, s=1.0), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=1.0), heroes=[], sfx=[dict(t=r3(t3), type='pop')])
    page('g03', cfg, extra_css=EXTRA_CSS, extra_js=fx.js())


# ---------------------------------------------------------------------------------------------------------------
# g04 - fvp, "the model ... like Opus, Fable, GPT-six ... form the brain": a glass harness panel with an empty model
# socket (his four slide tiles around it, unpowered); three paper model cards land on their names; on "brain" Opus
# docks into the socket, the socket lights azure and the harness tiles power up while the camera pushes in.
def model_card(sym, maker, name):
    return (img(sym, 76, 76, 'left:34px;top:37px') +
            f'<div class="abs" style="left:134px;top:30px;font:500 28px/1.2 Figtree;color:{INK2}">{maker}</div>'
            f'<div class="abs" style="left:134px;top:64px;font:600 48px/1.15 Figtree;letter-spacing:-.025em;color:{INK};white-space:nowrap">{name}</div>')


def g04():
    b, ws = words('g04')
    fx = FX()
    claude, _, _ = logo('claude_symbol.png')
    oai, _, _ = logo('openai_symbol.png')                          # dark artwork on paper
    SX, SY, SW, SH = 784, 330, 800, 400          # the harness panel with its socket
    slot = (180, 115, 440, 170)                    # x, y, w, h inside the card
    ic = [('azure', 'code', 44, 64), ('iris', 'bolt', 44, 260), ('mint', 'check', 680, 64), ('ember', 'bars', 680, 260)]
    icons = ''.join(f'<div id="hi{i}" class="abs" style="left:{x}px;top:{y}px;width:76px;height:76px;opacity:.28">{tile(c, g, 76, -8 if i % 2 else 8)}</div>'
                    for i, (c, g, x, y) in enumerate(ic))
    sx, sy, sw, sh = slot
    sock = (icons +
            f'<div id="sglow" class="abs" style="left:{sx - 80}px;top:{sy - 70}px;width:{sw + 160}px;height:{sh + 140}px;border-radius:50%;'
            f'background:radial-gradient(closest-side,rgba(47,149,255,.32),rgba(47,149,255,0));opacity:.35"></div>'
            f'<div class="abs" style="left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;border-radius:24px;border:2px dashed {HAIR2};background:rgba(255,255,255,.03)"></div>'
            f'<div id="slit" class="abs" style="left:{sx - 4}px;top:{sy - 4}px;width:{sw + 8}px;height:{sh + 8}px;border-radius:28px;border:3px solid {AZ};'
            f'box-shadow:0 0 0 8px rgba(47,149,255,.12),0 0 60px rgba(47,149,255,.55);opacity:0"></div>'
            f'<div class="abs lab" style="left:{sx}px;top:{sy - 48}px">Model</div>'
            f'<div class="abs lab" style="left:{sx}px;top:{sy + sh + 26}px;width:{sw}px;text-align:center">Harness</div>'
            + ring('sring', 28, 'rgba(47,149,255,.6)', 'rgba(47,149,255,.18)', 2))
    t_op, t_fa, t_gp, t_br = T(ws, 'opus'), T(ws, 'fable'), T(ws, 'gptsix'), T(ws, 'brain')
    MY, MW, MH = 790, 420, 150
    mx = [334, 784, 1234]
    cards = [dict(id='sock', kind='glass', x=SX, y=SY, w=SW, h=SH, html=sock),
             dict(id='m1', kind='paper', x=mx[0], y=MY, w=MW, h=MH, html=model_card(claude, 'Claude', 'Opus 5.5'), land=dict(t=r3(t_op - 0.12), dur=0.55), noDof=True),
             dict(id='m2', kind='paper', x=mx[1], y=MY, w=MW, h=MH, html=model_card(claude, 'Claude', 'Fable 5.1'), land=dict(t=r3(t_fa - 0.12), dur=0.55), exit=dict(t=r3(t_br + 0.1), dur=0.6)),
             dict(id='m3', kind='paper', x=mx[2], y=MY, w=MW, h=MH, html=model_card(oai, 'OpenAI', 'GPT-6'), land=dict(t=r3(t_gp - 0.12), dur=0.55), exit=dict(t=r3(t_br + 0.1), dur=0.6))]
    tx, ty = SX - mx[0], (SY - SH / 2 + sy + sh / 2) - MY
    t0d, t1d = t_br - 0.6, t_br + 0.05
    fx.k('card-m1', (t0d, dict(x=0, y=0, s=1)), (t0d + 0.32, dict(x=tx * 0.45, y=ty * 0.62, s=1.0), 'power2.in'),
         (t1d, dict(x=tx, y=ty, s=0.97), 'power3.out'))
    fx.hold['card-m1'] = False
    fx.k('slit', (t1d - 0.02, dict(o=0)), (t1d + 0.3, dict(o=1), 'power2.out'))
    fx.k('sglow', (t1d - 0.02, dict(o=0.35, s=1)), (t1d + 0.4, dict(o=1, s=1.15), 'power2.out'))
    fx.k('sring', (t1d, dict(o=0)), (t1d + 0.5, dict(o=1)))
    for i in range(4):
        tt = t1d + 0.1 + 0.07 * i
        fx.k(f'hi{i}', (tt, dict(o=0.28, s=0.92)), (tt + 0.45, dict(o=1, s=1), 'back.out(2)'))
    moves = [dict(t=0.2, dur=t_br - 0.6, kind='glide', to=dict(x=784, y=556, s=1.03)),
             dict(t=t_br - 0.35, dur=1.6, kind='push', to=dict(x=SX, y=SY + 8, s=1.32))]
    cfg = dict(id='g04', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=540, s=1.0), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=0.9),
               heroes=[dict(t=0, id='none'), dict(t=t_br - 0.3, id='sock')],
               sfx=[dict(t=r3(t_op - 0.12), type='pop'), dict(t=r3(t_fa - 0.12), type='pop'), dict(t=r3(t_gp - 0.12), type='pop'),
                    dict(t=r3(t1d), type='pop')])
    page('g04', cfg, extra_css=EXTRA_CSS, extra_js=fx.js())


# ---------------------------------------------------------------------------------------------------------------
# g05 - fvp, tools then checks: a Claude Code session window (white product UI) whose tool calls appear on their
# words (Write, Grep / Glob, WebFetch, a browser call with a little browser window); on "checks" the camera steps to
# a glass code panel where npm test / eslint / tsc pass on their words (mint ticks).
def elbow(x, y, w=22, h=22, color='#C9CBD1'):
    return f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-left:3px solid {color};border-bottom:3px solid {color};border-bottom-left-radius:6px"></div>'


def mini_browser(id, x, y, w=330, h=220):
    return (f'<div id="{id}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:18px;background:#fff;'
            f'box-shadow:0 24px 50px -18px rgba(0,0,0,.35);border:1.5px solid {PLINE};overflow:hidden">'
            f'<div class="abs" style="left:0;top:0;width:100%;height:48px;background:{PAPER2};border-bottom:1.5px solid {PLINE}"></div>'
            f'<div class="abs m" style="left:16px;top:9px;width:{w - 32}px;height:30px;border-radius:15px;background:#fff;border:1.5px solid {PLINE};'
            f'font-size:22px;line-height:27px;color:{INK2};padding-left:14px">localhost:3000</div>'
            f'<div class="abs" style="left:{w / 2 - 80}px;top:74px;width:160px;height:22px;border-radius:11px;background:#E4E6EA"></div>'
            f'<div class="abs" style="left:{w / 2 - 110}px;top:112px;width:220px;height:30px;border-radius:9px;border:1.5px solid #DFE1E5"></div>'
            f'<div class="abs" style="left:{w / 2 - 110}px;top:156px;width:220px;height:40px;border-radius:10px;background:{INK}"></div>'
            f'<div class="abs" style="left:{w / 2 - 12}px;top:164px;width:24px;height:24px;border-radius:50%;'
            f'background:conic-gradient(#EA4335 0 25%,#FBBC05 0 50%,#34A853 0 75%,#4285F4 0)"></div></div>')


def g05():
    b, ws = words('g05')
    fx = FX()
    claude, _, _ = logo('claude_symbol.png')
    SW_, SH_ = 1240, 860
    tools = ['Write', 'Edit', 'Grep', 'Glob', 'Bash', 'WebFetch', 'Browser']
    chips = ''; cx = 150
    for i, tname in enumerate(tools):
        w = len(tname) * 18 + 34
        chips += (f'<div id="ch{i}" class="abs" style="left:{cx}px;top:104px;width:{w}px;height:52px">'
                  f'<div class="abs" style="inset:0;border-radius:14px;background:{PAPER2};border:1.5px solid {PLINE}"></div>'
                  f'<div id="chh{i}" class="abs" style="inset:0;border-radius:14px;background:{AZWASH};border:2px solid {AZ};box-shadow:0 0 18px rgba(47,149,255,.35);opacity:0"></div>'
                  f'<div class="abs m" style="left:0;top:0;width:100%;line-height:52px;text-align:center;font-size:30px;color:{INK}">{tname}</div></div>')
        cx += w + 12
    calls = [('Write', 'src/app/login/page.tsx', 'Wrote 64 lines', 'write', 0),
             ('Grep', '"useAuth"', 'Found 6 files', 'search', 2),
             ('Glob', '**/*.ts', '38 files', None, 3),
             ('WebFetch', 'nextjs.org/docs', 'Fetched 14 KB', 'browse', 5),
             ('Browser', 'localhost:3000/login', 'Page loaded', 'open', 6)]
    t_files2 = T(ws, 'files', 2)
    rows = ''
    y0 = 300
    for i, (tool, arg, res, word, ci) in enumerate(calls):
        y = y0 + 106 * i
        rows += (f'<div id="cl{i}" class="abs" style="left:0;top:{y}px;width:100%;height:100px;opacity:0">'
                 + dot(f'bd{i}a', AZ, 40, 15, 16, glow=True) + dot(f'bd{i}b', MINT, 40, 15, 16, 0) +
                 f'<div class="abs m" style="left:74px;top:0;font-size:30px;line-height:46px;color:{INK};white-space:nowrap"><b style="font-weight:700">{tool}</b>({arg})</div>'
                 f'<div id="rs{i}" class="abs" style="left:74px;top:46px;opacity:0">{elbow(4, 0)}'
                 f'<div class="abs m" style="left:40px;top:0;font-size:30px;line-height:46px;color:{INK2};white-space:nowrap">{res}</div></div></div>')
    sess = (win_head(claude, 'Claude Code', badge='~/acme-app') +
            f'<div class="abs" style="left:36px;top:108px;font:500 30px/44px Figtree;color:{INK2}">Tools</div>'
            f'<div id="chips" class="abs" style="left:0;top:0">{chips}</div>'
            f'<div class="abs" style="left:0;top:180px;width:100%;height:1.5px;background:{PLINE}"></div>'
            f'<div class="abs" style="left:36px;top:204px;width:{SW_ - 72}px;height:64px;border-radius:14px;background:{PAPER2}"></div>'
            f'<div class="abs m" style="left:58px;top:212px;font-size:30px;line-height:48px;color:{INK}"><span style="color:{AZINK}">&gt;</span> Add a login page with Google sign-in</div>'
            + rows + mini_browser('mb', 870, 618, 330, 220))
    # glass code panel (checks)
    TW_, TH_ = 1120, 620
    trows = ''
    cmds = [('npm test', '42 passed', 'test'), ('eslint .', '0 problems', 'lint'), ('tsc --noEmit', 'no errors', 'type')]
    for i, (cmd, res, word) in enumerate(cmds):
        y = 150 + 140 * i
        trows += (f'<div class="abs m" style="left:60px;top:{y}px;font-size:36px;line-height:56px;color:{AZ}">$</div>'
                  f'<div id="tc{i}" class="abs m" style="left:104px;top:{y}px;font-size:36px;line-height:56px;color:#E6E7EA;white-space:pre"></div>'
                  f'<div id="tr{i}" class="abs m" style="left:520px;top:{y}px;font-size:36px;line-height:56px;color:{MINT};opacity:0">{res}</div>'
                  + check_badge(f'tk{i}', 56, style=f'left:{TW_ - 130}px;top:{y}px;opacity:0'))
    term = (f'<div class="abs lab" style="left:60px;top:40px">Checks · harness</div>'
            f'<div class="abs" style="left:60px;top:96px;width:{TW_ - 120}px;height:1px;background:{HAIR}"></div>' + trows)
    TX, TY = 2580, 560
    cards = [dict(id='sess', kind='window', x=720, y=540, w=SW_, h=SH_, html=sess),
             dict(id='term', kind='glass', x=TX, y=TY, w=TW_, h=TH_, html=term, highlight=True)]
    t_tools = T(ws, 'tools')
    fx.k('chips', (t_tools - 0.12, dict(o=0, y=12)), (t_tools + 0.3, dict(o=1, y=0), 'power3.out'))
    tw = [T(ws, 'write'), T(ws, 'search'), t_files2, T(ws, 'browse'), T(ws, 'open')]
    for i, t in enumerate(tw):
        a = t - 0.08
        fx.k(f'cl{i}', (a, dict(o=0, y=14)), (a + 0.32, dict(o=1, y=0), 'power3.out'))
        fx.k(f'rs{i}', (a + 0.38, dict(o=0, x=-8)), (a + 0.62, dict(o=1, x=0), 'power2.out'))
        fx.k(f'bd{i}b', (a + 0.38, dict(o=0)), (a + 0.55, dict(o=1)))
        fx.k(f'bd{i}a', (a, dict(o=1)), (a + 0.2, dict(o=0.35), 'sine.inOut'), (a + 0.38, dict(o=1)), (a + 0.55, dict(o=0)))
        ci = calls[i][4]
        fx.k(f'chh{ci}', (a, dict(o=0)), (a + 0.15, dict(o=1)), (a + 1.4, dict(o=1)), (a + 1.8, dict(o=0)))
    t_open = tw[4]
    fx.k('mb', (t_open + 0.1, dict(o=0, y=16, s=0.94)), (t_open + 0.55, dict(o=1, y=0, s=1), 'power3.out'))
    t_chk = T(ws, 'checks')
    tt = [T(ws, 'test'), T(ws, 'lint'), T(ws, 'type')]
    starts = [tt[0] - 0.75, tt[1] - 0.55, tt[2] - 0.62]
    for i, (cmd, res, word) in enumerate(cmds):
        fx.type(f'tc{i}', starts[i], cmd, cps=22, caretFrom=(t_chk + 0.4 if i == 0 else starts[i] - 0.05), caretTo=tt[i] - 0.05)
        fx.k(f'tr{i}', (tt[i] - 0.06, dict(o=0, x=-10)), (tt[i] + 0.2, dict(o=1, x=0), 'power2.out'))
        fx.k(f'tk{i}', (tt[i] - 0.04, dict(o=0, s=0.4)), (tt[i] + 0.36, dict(o=1, s=1), 'back.out(2.4)'))
    moves = [dict(t=tw[0] - 0.4, dur=1.6, kind='push', to=dict(x=740, y=566, s=1.07)),
             dict(t=tw[0] + 1.3, dur=t_chk - 0.25 - tw[0] - 1.3, kind='glide', to=dict(x=742, y=566, s=1.08)),
             dict(t=t_chk - 0.35, dur=0.95, kind='step', to=dict(x=TX, y=TY, s=1.0)),
             dict(t=t_chk + 0.7, dur=b['dur'] - t_chk - 0.7, kind='glide', to=dict(x=TX, y=TY + 4, s=1.035))]
    cfg = dict(id='g05', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=540, s=1.0), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=0.8),
               heroes=[dict(t=0, id='sess'), dict(t=t_chk - 0.2, id='term')],
               sfx=[dict(t=r3(t_tools - 0.1), type='pop')] + [dict(t=r3(tw[i] - 0.08), type='pop') for i in (0, 1, 3, 4)] +
                   sum([keyrun(starts[i], len(cmds[i][0]), 22) for i in range(3)], []) +
                   [dict(t=r3(tt[0]), type='pop'), dict(t=r3(tt[1]), type='pop'), dict(t=r3(tt[2]), type='chime')])
    page('g05', cfg, extra_css=EXTRA_CSS, extra_js=fx.js())


# ---------------------------------------------------------------------------------------------------------------
# g06 - fvp, hooks. Phase 1: the real Claude Code hook events (captures/cc_hooks) on a glass life-cycle track, lighting
# in sequence; azure hook tiles drop onto the nodes on "hook into". Phase 2: the camera moves down to the
# UserPromptSubmit flow - a prompt (paper) types with a (fake) key, mask-secrets.ts (a mod-style handler: a settings
# hook can only block or add context, a mod can rewrite) lands between prompt and agent on glass, the key gets an
# ember band on "sensitive", flips to dots on "mask", and the masked prompt reaches Claude.
def g06():
    import math
    b, ws = words('g06')
    fx = FX()
    claude, _, _ = logo('claude_symbol.png')
    TXc, TYc, TW_, TH_ = 784, 240, 1400, 230
    ev = [('SessionStart', 150), ('UserPromptSubmit', 450), ('PreToolUse', 750), ('PostToolUse', 1020), ('Stop', 1270)]
    LY_ = 118
    EVI = ['M8 5.5v13l10.5-6.5z', 'M4 5.5h16v10.5H10l-4.5 3.8V16H4z',
           'M14.5 4.5a4.5 4.5 0 0 0-4.2 6.1L4.5 16.4l3.1 3.1 5.8-5.8a4.5 4.5 0 0 0 6.1-4.2l-2.7 2.7-2.6-.6-.6-2.6z',
           'M3.5 13l4 4 8-9M14 17l2 2 4.5-5', 'M8.5 6h7a2.5 2.5 0 0 1 2.5 2.5v7a2.5 2.5 0 0 1-2.5 2.5h-7A2.5 2.5 0 0 1 6 15.5v-7A2.5 2.5 0 0 1 8.5 6z']
    track = (f'<div class="abs" style="left:110px;top:{LY_ - 3}px;width:1180px;height:6px;border-radius:3px;background:{BAR}"></div>'
             f'<div id="tfill" class="abs" style="left:110px;top:{LY_ - 3}px;width:0;height:6px;border-radius:3px;background:{AZ};box-shadow:0 0 16px rgba(47,149,255,.8)"></div>')
    for i, (name, x) in enumerate(ev):
        track += (f'<div class="abs" style="left:{x - 17}px;top:{LY_ - 17}px;width:34px;height:34px;border-radius:50%;background:#18191C;border:4px solid {BAR}"></div>'
                  f'<div id="nd{i}" class="abs" style="left:{x - 17}px;top:{LY_ - 17}px;width:34px;height:34px;border-radius:50%;background:{AZ};'
                  f'box-shadow:0 0 0 7px rgba(47,149,255,.16),0 0 22px rgba(47,149,255,.8);opacity:0"></div>'
                  + hook_badge(f'hk{i}', 54, f'left:{x - 27}px;top:{LY_ - 27}px;opacity:0') +
                  f'<div id="nl{i}" class="abs m" style="left:{x - 200}px;top:{LY_ + 40}px;width:400px;text-align:center;font-size:28px;line-height:44px;color:{WHITE};opacity:.5">{name}</div>'
                  + svg(li(EVI[i], BAR, 1.9), x - 23, 30, 46) + svg(li(EVI[i], WHITE, 1.9), x - 23, 30, 46, style='opacity:0').replace('<svg ', f'<svg id="ei{i}" ', 1))
    track += (f'<div id="upsring" class="abs" style="left:{ev[1][1] - 44}px;top:{LY_ - 44}px;width:88px;height:88px;border-radius:50%;'
              f'border:3px solid {AZ};box-shadow:0 0 26px rgba(47,149,255,.6);opacity:0"></div>')
    # ---- phase 2: prompt -> mask-secrets.ts -> Claude
    PX, PY_, PW_, PH_ = 380, 610, 560, 270
    AX, AY, AW, AH = 1190, 610, 560, 270
    SXc, SYc, SW2, SH2 = 784, 836, 420, 150
    CH = 18                                     # Geist Mono advance at 30 px (0.6 em)
    line1, kpre, key = 'Deploy to staging with my', 'key ', 'sk-live-XXXX-XXXX-XXXX'
    tx0, ty0, LH = 36, 92, 46
    kx, ky = tx0 + len(kpre) * CH, ty0 + LH
    ndots = 14
    dots = ''.join(f'<div class="abs" style="left:{8 + i * (len(key) * CH - 16) / (ndots - 1) - 6:.1f}px;top:15px;width:12px;height:12px;border-radius:50%;background:{INK}"></div>'
                   for i in range(ndots))
    prompt = (f'<div class="abs lab" style="left:36px;top:32px;color:{INK2}">You</div>'
              f'<div id="kband" class="abs" style="left:{kx - 6}px;top:{ky + 1}px;width:{len(key) * CH + 12}px;height:{LH - 2}px;border-radius:8px;'
              f'background:{EMWASH};border:2px solid {EMB};transform-origin:0 50%;transform:scaleX(0)"></div>'
              f'<div id="ptext" class="abs m" style="left:{tx0}px;top:{ty0}px;font-size:30px;line-height:{LH}px;color:{INK};white-space:pre"></div>'
              f'<div id="keyov" class="abs m" style="left:{kx}px;top:{ky}px;font-size:30px;line-height:{LH}px;color:{INK};white-space:pre;opacity:0">{key}</div>'
              f'<div id="kdots" class="abs" style="left:{kx}px;top:{ky + 2}px;width:{len(key) * CH}px;height:42px;transform:scaleY(0)">{dots}</div>')
    agent = (img(claude, 44, 44, 'left:36px;top:26px') +
             f'<div class="abs" style="left:96px;top:24px;font:600 32px/48px Figtree;color:{INK}">Claude</div>'
             f'<div class="abs" style="left:24px;top:{ty0 - 8}px;width:{AW - 48}px;height:{2 * LH + 16}px;border-radius:14px;border:2px dashed #DADCE1"></div>'
             f'<div id="atext" class="abs m" style="left:{tx0}px;top:{ty0}px;font-size:30px;line-height:{LH}px;color:{INK};white-space:pre;opacity:0">{line1}\n{kpre}</div>'
             f'<div id="adots" class="abs" style="left:{kx}px;top:{ky + 2}px;width:{len(key) * CH}px;height:42px;opacity:0">{dots}</div>'
             + ring('aring', 24, AZ, 'rgba(47,149,255,.18)', 3) + check_badge('acheck', 50, style=f'left:{AW - 84}px;top:20px;opacity:0'))
    script = (file_icon(30, 26, 44, WHITE, fill='none') +
              f'<div class="abs m" style="left:84px;top:24px;font-size:30px;line-height:46px;color:{WHITE};font-weight:600">mask-secrets.ts</div>'
              f'<div id="st0" class="abs lab" style="left:84px;top:92px">Scanning prompt…</div>'
              f'<div id="st1" class="abs lab ember" style="left:84px;top:92px;opacity:0">1 secret found</div>'
              f'<div id="st2" class="abs lab mint" style="left:84px;top:92px;opacity:0">Secret masked</div>'
              f'<div id="scan" class="abs" style="left:0;top:0;width:100%;height:3px;background:{AZ};box-shadow:0 0 14px {AZ};opacity:0"></div>')
    CX0, CY0, CWc, CHc = 64, 380, 1440, 560     # connector layer: world rect

    def L(x, y): return (x - CX0, y - CY0)
    ups_x = TXc - TW_ / 2 + ev[1][1]
    pa = [L(ups_x, TYc + TH_ / 2), L(ups_x, PY_ - PH_ / 2)]
    pb, ab = PY_ + PH_ / 2, AY + AH / 2
    c1 = [L(PX + 120, pb), L(PX + 120, SYc - 10), L(SXc - SW2 / 2 - 60, SYc), L(SXc - SW2 / 2, SYc)]
    c2 = [L(SXc + SW2 / 2, SYc), L(SXc + SW2 / 2 + 60, SYc), L(AX - 120, SYc - 10), L(AX - 120, ab)]
    pth = lambda c: f'M{c[0][0]:.1f} {c[0][1]:.1f} C{c[1][0]:.1f} {c[1][1]:.1f} {c[2][0]:.1f} {c[2][1]:.1f} {c[3][0]:.1f} {c[3][1]:.1f}'
    glow = 'filter:drop-shadow(0 0 6px rgba(47,149,255,.85))'
    conn = (f'<svg class="abs" style="left:0;top:0;width:{CWc}px;height:{CHc}px;overflow:visible" viewBox="0 0 {CWc} {CHc}">'
            f'<path id="cu" d="M{pa[0][0]:.1f} {pa[0][1]:.1f} L{pa[1][0]:.1f} {pa[1][1]:.1f}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" fill="none" '
            f'stroke="rgba(47,149,255,.75)" stroke-width="4" stroke-linecap="round" style="{glow}"/>'
            f'<path id="c1" d="{pth(c1)}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" fill="none" stroke="{BAR}" stroke-width="4" stroke-linecap="round"/>'
            f'<path id="c2" d="{pth(c2)}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" fill="none" stroke="{BAR}" stroke-width="4" stroke-linecap="round"/>'
            f'<path id="c2a" d="{pth(c2)}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" fill="none" stroke="rgba(47,149,255,.75)" stroke-width="4" '
            f'stroke-linecap="round" style="{glow}"/></svg>'
            f'<div id="pkt" class="abs" style="left:-16px;top:-16px;width:32px;height:32px;border-radius:50%;background:{AZ};'
            f'box-shadow:0 0 0 8px rgba(47,149,255,.18),0 0 26px rgba(47,149,255,.9);opacity:0"></div>')
    cards = [dict(id='trk', kind='glass', x=TXc, y=TYc, w=TW_, h=TH_, html=track),
             dict(id='conn', kind='plain', x=CX0 + CWc / 2, y=CY0 + CHc / 2, w=CWc, h=CHc, html=conn, clip=False, noDof=True),
             dict(id='pr', kind='paper', x=PX, y=PY_, w=PW_, h=PH_, html=prompt, group='fl', sharpWithGroup=True),
             dict(id='ag', kind='paper', x=AX, y=AY, w=AW, h=AH, html=agent),
             dict(id='scr', kind='glass', x=SXc, y=SYc, w=SW2, h=SH2, html=script, group='fl', sharpWithGroup=True)]
    t_ev, t_cyc, t_hook = T(ws, 'events'), T(ws, 'cycle'), T(ws, 'hook')
    t_mom, t_send, t_scr, t_chk = T(ws, 'moment'), T(ws, 'send'), T(ws, 'script'), T(ws, 'check')
    t_sen, t_mask, t_bef, t_rea = T(ws, 'sensitive'), T(ws, 'mask'), T(ws, 'before'), T(ws, 'reaches')
    f0, f1 = t_ev - 0.1, t_cyc + 0.35
    fx.k('tfill', (f0, dict(w=0)), (f1, dict(w=1180), 'sine.inOut'))
    for i, (name, x) in enumerate(ev):
        u = (x - 110) / 1180
        p = math.acos(1 - 2 * max(0.0, min(1.0, u))) / math.pi          # invert sine.inOut: when the fill reaches it
        tn = f0 + p * (f1 - f0)
        fx.k(f'nd{i}', (tn - 0.05, dict(o=0, s=0.6)), (tn + 0.2, dict(o=1, s=1), 'back.out(2)'))
        fx.k(f'ei{i}', (tn - 0.05, dict(o=0)), (tn + 0.2, dict(o=1)))
        fx.k(f'nl{i}', (tn - 0.05, dict(o=0.5)), (tn + 0.2, dict(o=1)))
        th = t_hook - 0.1 + 0.07 * i
        fx.k(f'hk{i}', (th - 0.02, dict(o=0, y=-46, s=0.8)), (th + 0.34, dict(o=1, y=0, s=1), 'back.out(1.8)'))
    fx.k('upsring', (t_mom - 0.2, dict(o=0, s=0.7)), (t_mom + 0.15, dict(o=1, s=1), 'power2.out'), (t_mom + 0.9, dict(o=0.65, s=1.08)))
    fx.k('cu', (t_send - 0.35, dict(dash=1)), (t_send + 0.25, dict(dash=0), 'power2.inOut'))
    t_land = t_send - 0.25
    cards[2]['land'] = dict(t=r3(t_land), dur=0.55); cards[3]['land'] = dict(t=r3(t_land + 0.12), dur=0.55)
    t_type = t_send + 0.2
    fx.type('ptext', t_type, [[line1 + '\n' + kpre, ''], [key, 'key']], cps=26, caretTo=t_type + 51 / 26 + 0.6)
    cards[4]['land'] = dict(t=r3(t_scr - 0.15), dur=0.55)
    fx.k('c1', (t_scr + 0.1, dict(dash=1)), (t_scr + 0.55, dict(dash=0)))
    fx.k('c2', (t_scr + 0.3, dict(dash=1)), (t_scr + 0.75, dict(dash=0)))
    fx.k('scan', (t_chk - 0.1, dict(o=0, y=0)), (t_chk + 0.05, dict(o=0.9)), (t_chk + 0.9, dict(o=0.9, y=SH2 - 4), 'sine.inOut'),
         (t_chk + 1.0, dict(o=0)))
    fx.k('kband', (t_sen - 0.05, dict(sx=0)), (t_sen + 0.4, dict(sx=1), 'power3.out'), (t_mask + 0.1, dict(sx=1, o=1)), (t_mask + 0.45, dict(o=0)))
    fx.k('st0', (t_sen - 0.1, dict(o=1)), (t_sen + 0.15, dict(o=0)))
    fx.k('st1', (t_sen - 0.05, dict(o=0, y=8)), (t_sen + 0.25, dict(o=1, y=0), 'power2.out'), (t_mask - 0.05, dict(o=1)), (t_mask + 0.2, dict(o=0)))
    fx.k('st2', (t_mask, dict(o=0, y=8)), (t_mask + 0.3, dict(o=1, y=0), 'power2.out'))
    fx.toggle('ptext', 'masked', t_mask - 0.12)
    fx.k('keyov', (t_mask - 0.13, dict(o=0, sy=1)), (t_mask - 0.12, dict(o=1)), (t_mask + 0.04, dict(sy=0.02), 'power2.in'), (t_mask + 0.05, dict(o=0)))
    fx.k('kdots', (t_mask + 0.04, dict(sy=0)), (t_mask + 0.2, dict(sy=1), 'power2.out'))
    pts = bez(*c2, n=10)
    k0 = t_rea - 0.55
    fr = [(k0 - 0.01, dict(o=0, x=pts[0][0], y=pts[0][1]))]
    for i, (x, y) in enumerate(pts):
        fr.append((k0 + 0.5 * i / (len(pts) - 1), dict(o=1, x=x, y=y), 'linear' if i else 'power1.out'))
    fr.append((t_rea + 0.1, dict(o=0, x=pts[-1][0], y=pts[-1][1])))
    fx.k('pkt', *fr)
    fx.k('c2a', (k0, dict(dash=1)), (k0 + 0.5, dict(dash=0), 'linear'))
    fx.k('atext', (t_rea - 0.05, dict(o=0, x=-24)), (t_rea + 0.35, dict(o=1, x=0), 'power3.out'))
    fx.k('adots', (t_rea - 0.05, dict(o=0, x=-24)), (t_rea + 0.35, dict(o=1, x=0), 'power3.out'))
    fx.k('aring', (t_rea, dict(o=0)), (t_rea + 0.3, dict(o=1)))
    fx.k('acheck', (t_rea + 0.15, dict(o=0, s=0.4)), (t_rea + 0.5, dict(o=1, s=1), 'back.out(2.4)'))
    moves = [dict(t=t_mom - 0.25, dur=1.4, kind='push', to=dict(x=784, y=560, s=1.0)),
             dict(t=t_sen - 0.6, dur=1.1, kind='push', to=dict(x=470, y=640, s=1.24)),
             dict(t=t_bef - 0.3, dur=1.1, kind='pull', to=dict(x=784, y=520, s=1.0))]
    cfg = dict(id='g06', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=250, s=1.0), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=0.8),
               heroes=[dict(t=0, id='none'), dict(t=t_sen - 0.5, id='pr'), dict(t=t_bef - 0.2, id='none')],
               sfx=[dict(t=r3(t_hook - 0.1), type='pop'), dict(t=r3(t_land), type='pop'), *keyrun(t_type, 51, 26),
                    dict(t=r3(t_scr - 0.15), type='pop'), dict(t=r3(t_mask), type='pop'), dict(t=r3(t_rea), type='chime')])
    css = EXTRA_CSS + '.masked .key{color:transparent}'
    page('g06', cfg, extra_css=css, extra_js=fx.js())


# ---------------------------------------------------------------------------------------------------------------
# Resource beats: the real page in the fixed capture frame (white window, radius 22, on its dark washed clone), the
# inner camera moves to the passage, an azure marker band (multiply) sweeps the sentence on its word.
CAPW, CAPH = 1440, 936
BAND_PAPER = 'rgba(47,149,255,.20)'


def view(fw, fh, k, fx=None, fy=None, left=None, top=None, right=None, bottom=None):
    """inner keyframe values clamped the way the engine clamps them (so moves never kink at the page edge)"""
    hw, hh = CAPW / 2 / k, CAPH / 2 / k
    if left is not None: fx = left + hw
    if right is not None: fx = right - hw
    if top is not None: fy = top + hh
    if bottom is not None: fy = bottom - hh
    fx = fw / 2 if fw <= 2 * hw else min(max(fx, hw), fw - hw)
    fy = fh / 2 if fh <= 2 * hh else min(max(fy, hh), fh - hh)
    return dict(fx=round(fx, 1), fy=round(fy, 1), k=k)


def mband(id, x, y, w, h):
    return (f'<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:10px;'
            f'background:{BAND_PAPER};transform-origin:0 50%;transform:scaleX(0)"></div>')


def r01():
    # "a special at the moment that's one hundred dollars off your annual plan": the real Agentic Labs about page
    # (skool.com/agentic-labs/about) shows "Special: Annual is $190 (normally $290) until 31 October".
    b, ws = words('r01')
    src, fw, fh = asset('skool_al_page_v2.png', ['captures/skool_agentic_labs_v2/full-page.png'])   # Leon's corrected page
    band = mband('hlP', 586, 1680, 462, 50)                     # "Annual is $190 (normally $290)"
    t_sp, t_one, t_ann = T(ws, 'special'), T(ws, 'one'), T(ws, 'annual')
    v0 = view(fw, fh, 0.5, fx=fw / 2, top=0)
    v1 = view(fw, fh, 0.92, left=330, fy=1640)
    v2 = view(fw, fh, 1.0, left=378, fy=1680)
    cap = capture_card('cap', fw, fh, mode='fvp', img=src, overlay=band, overlayBlend='multiply', inner0=v0,
                       inner=[dict(t=t_sp - 0.25, dur=0.9, **v1),
                              dict(t=t_sp + 0.7, dur=b['dur'] - t_sp - 0.7, ease='sine.inOut', **v2)])
    cap['radius'] = 22
    cfg = dict(id='r01', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=540, s=1.0), cards=[cap], moves=[], heroes=[dict(t=0, id='cap')],
               wave=dict(level='low', k=0.6),
               reveals=[dict(el='hlP', t=r3(t_one - 0.05), dur=0.9, type='scaleX', ease='power2.inOut')], sfx=[])
    page('r01', cfg, extra_css=EXTRA_CSS, backdrop=('img', src, fw, fh))


def r02():
    # Claude Mods: the real announcement ("Customize Claude Code with mods", claude.com, Oct 1 2026). Band on the
    # headline on "customize"; under the hood -> "A mod is a function that hooks into one of these events." on "hooks".
    b, ws = words('r02')
    src, fw, fh = asset('claude_mods_blog.png', ['captures/claude_mods_blog/screenshots/full-page.png'])
    bands = (mband('hlA', 788, 938, 930, 102) + mband('hlB', 788, 1062, 820, 102) +
             mband('hlC', 936, 3772, 1042, 58))
    t_mods, t_cus, t_hood, t_using, t_hooks = T(ws, 'mods'), T(ws, 'customize'), T(ws, 'hood'), T(ws, 'using'), T(ws, 'hooks')
    v0 = view(fw, fh, 0.62, fx=fw / 2, top=290)
    v1 = view(fw, fh, 0.92, left=620, fy=1060)
    v1b = view(fw, fh, 0.95, left=640, fy=1066)
    v2 = view(fw, fh, 1.02, left=700, fy=3780)
    v2b = view(fw, fh, 1.05, left=716, fy=3790)
    cap = capture_card('cap', fw, fh, mode='fvp', img=src, overlay=bands, overlayBlend='multiply', inner0=v0,
                       inner=[dict(t=t_mods - 0.35, dur=0.9, **v1),
                              dict(t=t_mods + 0.6, dur=t_hood - 0.25 - t_mods - 0.6, ease='sine.inOut', **v1b),
                              dict(t=t_hood - 0.25, dur=0.8, ease='power2.inOut', **v2),
                              dict(t=t_hood + 0.6, dur=b['dur'] - t_hood - 0.6, ease='sine.inOut', **v2b)])
    cap['radius'] = 22
    cfg = dict(id='r02', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=540, s=1.0), cards=[cap], moves=[], heroes=[dict(t=0, id='cap')],
               wave=dict(level='low', k=0.6),
               reveals=[dict(el='hlA', t=r3(t_cus - 0.08), dur=0.45, type='scaleX'), dict(el='hlB', t=r3(t_cus + 0.32), dur=0.45, type='scaleX'),
                        dict(el='hlC', t=r3(t_using - 0.05), dur=0.6, type='scaleX', ease='power2.inOut')], sfx=[])
    page('r02', cfg, extra_css=EXTRA_CSS, backdrop=('img', src, fw, fh))


def r03():
    # agents.md (PiP bottom-left: content x 416-1856, anchor [1136, 540], capture frame built by hand).
    b, ws = words('r03')
    src, fw, fh = asset('agents_md_all.png', ['captures/agents_md_all/screenshots/full-page.png'])
    band = mband('hlO', 280, 300, 812, 56)
    t_amd, t_open, t_any, t_honor = T(ws, 'agents.md'), T(ws, 'open'), T(ws, 'any'), T(ws, 'honor')
    v0 = view(fw, fh, 0.5, fx=fw / 2, top=0)
    v1 = view(fw, fh, 1.0, left=200, top=0)
    v1b = view(fw, fh, 1.02, left=206, top=0)
    v2 = view(fw, fh, 0.92, fx=1440, top=1990)
    v3 = view(fw, fh, 0.6, fx=1440, fy=3075)
    v3b = view(fw, fh, 0.62, fx=1440, fy=3075)
    cap = dict(id='cap', kind='capture', x=1136, y=540, w=CAPW, h=CAPH, radius=22, fw=fw, fh=fh, img=src, overlay=band, overlayBlend='multiply',
               inner0=v0, backdrop={'tIn': -1}, bg='#fff',
               inner=[dict(t=t_amd - 0.3, dur=0.9, **v1),
                      dict(t=t_amd + 0.65, dur=t_any - 0.25 - t_amd - 0.65, ease='sine.inOut', **v1b),
                      dict(t=t_any - 0.25, dur=0.8, ease='power2.inOut', **v2),
                      dict(t=t_honor - 0.3, dur=0.75, ease='power2.inOut', **v3),
                      dict(t=t_honor + 0.45, dur=b['dur'] - t_honor - 0.45, ease='sine.inOut', **v3b)])
    cfg = dict(id='r03', dur=b['dur'], mode='fvp', anchor=[1136, 540], cam0=dict(x=1136, y=540, s=1.0), cards=[cap], moves=[],
               wave=dict(level='low', k=0.6), heroes=[dict(t=0, id='cap')],
               reveals=[dict(el='hlO', t=r3(t_open - 0.1), dur=0.6, type='scaleX', ease='power2.inOut')], sfx=[])
    page('r03', cfg, extra_css=EXTRA_CSS, backdrop=('img', src, fw, fh))


# ---------------------------------------------------------------------------------------------------------------
# g07 - fvp, memory files as paper documents the camera steps along: AGENTS.md (agents.md mark) at frame 0, DESIGN.md
# and SOUL.md land as named (his ember Memory tile), then a docs/ folder lands, opens, and his real docs slide out.
def doc_card(mark_html, name, lines):
    body = ''
    for i, (txt, head) in enumerate(lines):
        body += (f'<div class="abs m" style="left:36px;top:{196 + 44 * i}px;font-size:30px;line-height:44px;white-space:pre;'
                 f'color:{INK if head else INK2};font-weight:{600 if head else 400}">{txt}</div>')
    return (f'<div class="abs" style="left:36px;top:34px;width:72px;height:72px">{mark_html}</div>'
            f'<div class="abs m" style="left:36px;top:124px;font-size:36px;line-height:50px;color:{INK};font-weight:600">{name}</div>'
            f'<div class="abs" style="left:36px;top:184px;width:268px;height:1.5px;background:{PLINE}"></div>' + body)


def g07():
    b, ws = words('g07')
    fx = FX()
    amd, _, _ = logo('agentsmd_mark_on-light.png')
    t_amd, t_des, t_soul, t_files, t_docs = T(ws, 'agents.md'), T(ws, 'design.md'), T(ws, 'soul.md'), T(ws, 'files'), T(ws, 'docs')
    Y = 420; DW, DH = 340, 430
    xs = [300, 700, 1100]
    mem = tile('ember', 'bars', 72, -8)
    docs = [('AGENTS.md', f'<img id="amk" src="{amd}" style="width:72px;height:72px">', [('## Commands', 1), ('npm run dev', 0), ('## Rules', 1), ('- Run the tests', 0)]),
            ('DESIGN.md', mem, [('## Colors', 1), ('azure #2F95FF', 0), ('## Type', 1), ('Figtree 600', 0)]),
            ('SOUL.md', mem, [('## Voice', 1), ('warm, direct', 0), ('## Values', 1), ('ship small', 0)])]
    cards = [dict(id=f'd{i}', kind='paper', x=xs[i], y=Y, w=DW, h=DH, html=doc_card(m, n, l)) for i, (n, m, l) in enumerate(docs)]
    cards[1]['land'] = dict(t=r3(t_des - 0.12), dur=0.55)
    cards[2]['land'] = dict(t=r3(t_soul - 0.12), dur=0.55)
    FX_, FY_ = 1560, 330
    files = ['GAME_DESIGN.md', 'SCRIPT.md', 'TECH_PLAN.md', 'LEVEL_LAYOUT.md', 'HANDOFF.md']
    fold = (svg(f'<path d="{FOLDER_P}" fill="{AZWASH}" stroke="{AZINK}" stroke-width="1.4" stroke-linejoin="round"/>', 70, 22, 160, 160).replace('<svg ', '<svg id="fclosed" ', 1) +
            svg(FOLDER_OPEN.format(fill=AZWASH, stroke=AZINK, front='#F4F8FF'), 70, 22, 160, 160, style='opacity:0').replace('<svg ', '<svg id="fopen" ', 1) +
            f'<div class="abs m" style="left:0;top:178px;width:100%;text-align:center;font-size:36px;line-height:46px;color:{INK};font-weight:600">docs/</div>')
    cards.append(dict(id='fold', kind='paper', x=FX_, y=FY_, w=300, h=250, html=fold, land=dict(t=r3(t_files - 0.12), dur=0.55)))
    fy0 = FY_ + 125 + 30
    for i, fn in enumerate(files):
        cards.append(dict(id=f'f{i}', kind='paper', x=FX_, y=fy0 + 40 + 84 * i, w=420, h=68, radius=14,
                          html=file_icon(22, 14, 40) + f'<div class="abs m" style="left:76px;top:11px;font-size:30px;line-height:46px;color:{INK}">{fn}</div>'))
        tf = t_docs + 0.12 + 0.08 * i
        fx.k(f'card-f{i}', (tf, dict(o=0, y=-(84 * i + 120), s=0.7)), (tf + 0.45, dict(o=1, y=0, s=1), 'power3.out'))
    fx.k('fclosed', (t_docs - 0.02, dict(o=1)), (t_docs + 0.1, dict(o=0)))
    fx.k('fopen', (t_docs - 0.02, dict(o=0)), (t_docs + 0.1, dict(o=1)))
    fx.k('amk', (t_amd - 0.1, dict(s=1)), (t_amd + 0.1, dict(s=1.14), 'power2.out'), (t_amd + 0.45, dict(s=1), 'back.out(2)'))
    S = 1.25
    moves = [dict(t=t_des - 0.3, dur=0.6, kind='step', to=dict(x=xs[1], y=Y, s=S)),
             dict(t=t_soul - 0.3, dur=0.6, kind='step', to=dict(x=xs[2], y=Y, s=S)),
             dict(t=t_soul + 0.4, dur=t_files - 0.3 - t_soul - 0.4, kind='glide', to=dict(x=xs[2] + 24, y=Y, s=S - 0.03)),
             dict(t=t_files - 0.3, dur=0.8, kind='step', to=dict(x=FX_, y=FY_ + 260, s=1.0))]
    cfg = dict(id='g07', dur=b['dur'], mode='fvp', cam0=dict(x=xs[0], y=Y, s=S), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=1.0),
               heroes=[dict(t=0, id='d0'), dict(t=t_des - 0.2, id='d1'), dict(t=t_soul - 0.2, id='d2'), dict(t=t_files - 0.2, id='none')],
               sfx=[dict(t=r3(t_des - 0.12), type='pop'), dict(t=r3(t_soul - 0.12), type='pop'), dict(t=r3(t_files - 0.12), type='pop'),
                    dict(t=r3(t_docs + 0.12), type='pop')])
    page('g07', cfg, extra_css=EXTRA_CSS, extra_js=fx.js())


# ---------------------------------------------------------------------------------------------------------------
# g08 - fvp, the sandbox: the agent (glass) inside a dashed azure workspace boundary; a worktree card and a feature
# branch splitting off main; on "never ... main branch" the agent's ember arrow toward main hits an ember x tile and
# is refused. The scene sits higher than the white version so the git graph stays above the wave's crest.
def g08():
    b, ws = words('g08')
    fx = FX()
    claude, _, _ = logo('claude_symbol.png')
    t_ws, t_feat, t_never, t_change, t_main = T(ws, 'workspace'), T(ws, 'feature'), T(ws, 'never'), T(ws, 'change'), T(ws, 'main')
    t_work = T(ws, 'work', 2)
    GX, GY, GW, GH = 64, 60, 1440, 860

    def L(x, y): return (x - GX, y - GY)
    MY, BY = 730, 545                               # main / feature branch y
    WS = (290, 140, 1040, 480)                      # workspace boundary x, y, w, h
    main_dots = [380, 540, 700, 860, 1020, 1180]
    feat_dots = [740, 845, 950]
    bx0 = 540
    m0, m1 = L(250, MY), L(1320, MY)
    bp = [L(bx0, MY), L(bx0 + 80, MY), L(bx0 + 100, BY), L(bx0 + 190, BY)]
    fe = L(975, BY)
    wx, wy = L(WS[0], WS[1])
    ax, ay = 510, 300
    xsx, xsy = ax, WS[1] + WS[3]                    # the x tile sits on the boundary
    a0, a1 = L(ax, ay + 90), L(ax, MY - 40)
    lines = (f'<svg class="abs" style="left:0;top:0;width:{GW}px;height:{GH}px;overflow:visible" viewBox="0 0 {GW} {GH}">'
             f'<rect id="wsb" x="{wx}" y="{wy}" width="{WS[2]}" height="{WS[3]}" rx="40" fill="rgba(47,149,255,.05)" stroke="rgba(47,149,255,.8)" stroke-width="3" '
             f'stroke-dasharray="16 14" style="opacity:0;transform-box:fill-box;transform-origin:50% 50%;filter:drop-shadow(0 0 8px rgba(47,149,255,.5))"/>'
             f'<path d="M{m0[0]} {m0[1]} L{m1[0]} {m1[1]}" fill="none" stroke="#C9CBD1" stroke-width="6" stroke-linecap="round"/>'
             f'<path id="fb" d="M{bp[0][0]} {bp[0][1]} C{bp[1][0]} {bp[1][1]} {bp[2][0]} {bp[2][1]} {bp[3][0]} {bp[3][1]} L{fe[0]} {fe[1]}" '
             f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" fill="none" stroke="{AZ}" stroke-width="6" stroke-linecap="round" '
             f'style="filter:drop-shadow(0 0 8px rgba(47,149,255,.7))"/>'
             f'<path id="arw" d="M{a0[0]} {a0[1]} L{a1[0]} {a1[1]}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" fill="none" '
             f'stroke="{EMB}" stroke-width="5" stroke-linecap="round" style="filter:drop-shadow(0 0 8px rgba(255,138,91,.7))"/></svg>')
    for x in main_dots:
        X, Y_ = L(x, MY)
        lines += f'<div class="abs" style="left:{X - 15}px;top:{Y_ - 15}px;width:30px;height:30px;border-radius:50%;background:#18191C;border:6px solid #C9CBD1"></div>'
    for i, x in enumerate(feat_dots):
        X, Y_ = L(x, BY)
        lines += (f'<div id="fd{i}" class="abs" style="left:{X - 15}px;top:{Y_ - 15}px;width:30px;height:30px;border-radius:50%;background:#18191C;'
                  f'border:6px solid {AZ};box-shadow:0 0 14px rgba(47,149,255,.6);opacity:0"></div>')
    mx, my = L(130, MY)
    lines += (f'<div class="abs" style="left:{mx - 30}px;top:{my - 33}px;width:200px;height:66px;border-radius:33px;background:rgba(24,25,28,.85);'
              f'border:1.5px solid {HAIR2};box-shadow:0 20px 40px -16px rgba(0,0,0,.8)">'
              + svg(LOCK_SVG.format(c='#fff'), 22, 16, 34).replace('<svg ', '<svg id="mlock" ', 1) +
              '<div class="abs m" style="left:68px;top:10px;font-size:32px;line-height:46px;color:#fff;font-weight:600">main</div></div>')
    fxl, fyl = L(990, BY)
    lines += (f'<div id="featchip" class="abs" style="left:{fxl}px;top:{fyl - 33}px;width:310px;height:66px;border-radius:33px;background:rgba(24,25,28,.85);'
              f'border:2px solid {AZ};box-shadow:0 0 22px rgba(47,149,255,.35);opacity:0">'
              + svg(BRANCH_SVG.format(c=AZ), 18, 15, 34) +
              f'<div class="abs m" style="left:62px;top:8px;font-size:30px;line-height:46px;color:{AZ};font-weight:600">feature/login</div></div>')
    wl, wt = L(WS[0] + 40, WS[1])
    lines += (f'<div id="wslabel" class="abs m" style="left:{wl}px;top:{wt - 24}px;padding:0 16px;height:48px;border-radius:12px;background:#15161A;'
              f'border:2px solid rgba(47,149,255,.8);font-size:28px;line-height:44px;color:{AZ};opacity:0">~/acme-app</div>')
    xx, xy = L(xsx, xsy)
    lines += cross_badge('xstamp', 84, style=f'left:{xx - 42}px;top:{xy - 42}px;opacity:0')
    agent = (img(claude, 60, 60, 'left:32px;top:45px') +
             f'<div class="abs" style="left:110px;top:26px;font:600 36px/52px Figtree;letter-spacing:-.02em;color:{WHITE};white-space:nowrap">Claude Code</div>'
             f'<div class="abs lab" style="left:112px;top:88px">Agent</div>')
    wt_html = (svg(li(FOLDER_P, WHITE, 1.7), 34, 30, 64, 64) +
               f'<div class="abs m" style="left:116px;top:30px;font-size:32px;line-height:46px;color:{WHITE};font-weight:600">.worktrees/login</div>'
               f'<div class="abs lab" style="left:118px;top:88px">Git worktree</div>')
    cards = [dict(id='lines', kind='plain', x=GX + GW / 2, y=GY + GH / 2, w=GW, h=GH, html=lines, clip=False, noDof=True),
             dict(id='agent', kind='glass', x=ax, y=ay, w=380, h=150, html=agent),
             dict(id='wt', kind='glass', x=1000, y=ay, w=470, h=150, html=wt_html, land=dict(t=r3(t_work - 0.12), dur=0.55))]
    fx.k('wsb', (t_ws - 0.2, dict(o=0, s=1.04)), (t_ws + 0.3, dict(o=1, s=1), 'power3.out'))
    fx.k('wslabel', (t_ws - 0.05, dict(o=0, y=8)), (t_ws + 0.3, dict(o=1, y=0), 'power3.out'))
    fx.k('fb', (t_feat - 0.15, dict(dash=1)), (t_feat + 0.55, dict(dash=0), 'power2.inOut'))
    for i in range(3):
        tt = t_feat + 0.15 + 0.12 * i
        fx.k(f'fd{i}', (tt, dict(o=0, s=0.4)), (tt + 0.3, dict(o=1, s=1), 'back.out(2.5)'))
    fx.k('featchip', (t_feat + 0.45, dict(o=0, x=-14)), (t_feat + 0.8, dict(o=1, x=0), 'power3.out'))
    an = t_never + 0.1
    reach = (xsy - 42 - (ay + 90)) / (MY - 40 - (ay + 90))          # the arrow stops at the x tile
    fx.k('arw', (an, dict(dash=1)), (t_change, dict(dash=1 - reach), 'power2.out'), (t_main - 0.05, dict(dash=1 - reach)), (t_main + 0.5, dict(dash=1), 'power2.in'))
    fx.k('xstamp', (t_change - 0.08, dict(o=0, s=1.8)), (t_change + 0.18, dict(o=1, s=1), 'power3.out'), (t_change + 0.3, dict(s=1.06)), (t_change + 0.42, dict(s=1)))
    fx.k('mlock', (t_main - 0.05, dict(r=0)), (t_main + 0.05, dict(r=-14), 'power2.out'), (t_main + 0.16, dict(r=10)), (t_main + 0.3, dict(r=-4)), (t_main + 0.45, dict(r=0)))
    moves = [dict(t=0.3, dur=t_never - 0.6, kind='glide', to=dict(x=724, y=466, s=1.04)),
             dict(t=t_never - 0.3, dur=1.4, kind='push', to=dict(x=700, y=490, s=1.1))]
    cfg = dict(id='g08', dur=b['dur'], mode='fvp', cam0=dict(x=720, y=460, s=1.0), cards=cards, moves=moves, pushRef=1.0, heroes=[],
               wave=dict(level='low', k=0.8),
               sfx=[dict(t=r3(t_ws), type='pop'), dict(t=r3(t_work - 0.12), type='pop'), dict(t=r3(t_feat + 0.15), type='pop'),
                    dict(t=r3(t_change), type='pop')])
    page('g08', cfg, extra_css=EXTRA_CSS, extra_js=fx.js())


# ---------------------------------------------------------------------------------------------------------------
# g09 - fvp, Level 1 = harnesses built by the provider (Claude Code, Codex, Gemini CLI) or a third party (OpenCode,
# Cursor): glass tiles with the real marks; push onto Claude Code; the azure level-1 tile flies from the Level 1 card
# onto it on "this level".
def g09():
    b, ws = words('g09')
    fx = FX()
    claude, _, _ = logo('claude_symbol.png')
    codex, _, _ = asset('codex_app_icon.png', [f'{LOGOS_NEW}/codex_app_icon_openai_blossom.png'])
    gem, _, _ = logo('gemini_cli_icon.png')
    oc, _, _ = logo('opencode-logo-dark.png')
    cur, _, _ = logo('cursor_cube_on-dark.png')
    t_prov, t_third, t_cc, t_this = T(ws, 'provider'), T(ws, 'thirdparty'), T(ws, 'claude'), T(ws, 'this', 2)
    lvl = level_card(1, *LEVELS[0]).replace('id="ic1"', 'id="lvic"').replace('id="d1"', 'id="lvd"').replace('id="real1"', 'id="lvr"')
    TW_, TH_ = 290, 250
    tl_ = lambda icon, name, maker: (f'<div class="abs" style="left:0;top:30px;width:100%;height:104px;display:flex;justify-content:center;align-items:center">{icon}</div>'
                                     f'<div class="abs" style="left:0;top:146px;width:100%;text-align:center;font:600 36px/1.2 Figtree;letter-spacing:-.02em;color:{WHITE}">{name}</div>'
                                     + (f'<div class="abs lab" style="left:0;top:198px;width:100%;text-align:center">{maker}</div>' if maker else ''))
    im = lambda src, w, h=None, r=0: f'<img src="{src}" style="width:{w}px;height:{h or w}px;border-radius:{r}px">'
    prov = [('cc', im(claude, 96), 'Claude Code', 'Anthropic'), ('cx', im(codex, 104, r=24), 'Codex', 'OpenAI'), ('gm', im(gem, 98, r=22), 'Gemini CLI', 'Google')]
    third = [('oc', im(oc, 78, 98), 'OpenCode', ''), ('cu', im(cur, 96), 'Cursor', '')]
    PY0, PY1 = 330, 700
    px = [700, 1010, 1320]; qx = [855, 1165]
    cards = [dict(id='lv', kind='glass', x=290, y=560, w=420, h=430, html=lvl, clip=False, group='lv1', sharpWithGroup=True)]
    for i, (cid, icon, name, maker) in enumerate(prov):
        cards.append(dict(id=cid, kind='glass', x=px[i], y=PY0, w=TW_, h=TH_, html=tl_(icon, name, maker),
                          land=dict(t=r3(t_prov - 0.15 + 0.12 * i), dur=0.55)))
    for i, (cid, icon, name, maker) in enumerate(third):
        cards.append(dict(id=cid, kind='glass', x=qx[i], y=PY1, w=TW_, h=TH_ - 50, html=tl_(icon, name, maker),
                          land=dict(t=r3(t_third - 0.15 + 0.12 * i), dur=0.55)))
    cards[1]['group'] = 'lv1'
    cards[3]['exit'] = dict(t=r3(t_cc - 0.1), dur=0.6)              # Gemini CLI would slide under the webcam on the push
    cards[1]['html'] += ring('ccring', 28)
    badge = (tile('azure', 'code', 96, -8) + f'<div class="abs" style="left:62px;top:62px;width:46px;height:46px;border-radius:50%;background:#fff;'
             f'box-shadow:0 6px 14px rgba(0,0,0,.4);font:600 30px/46px Figtree;color:{INK};text-align:center">1</div>')
    bx0, by0 = 290 - 210 + 32 + 52, 560 - 215 - 46 + 52          # the level card's tile centre
    bx1, by1 = px[0] + TW_ / 2 - 30, PY0 - TH_ / 2 + 26         # the Claude Code tile's top-right corner
    cards.append(dict(id='badge', kind='plain', x=bx0, y=by0, w=96, h=96, html=f'<div id="bdg" class="abs" style="left:0;top:0;opacity:0">{badge}</div>',
                      clip=False, noDof=True))
    tb = t_this - 0.55
    fx.k('card-badge', (tb, dict(x=0, y=0, s=1)), (tb + 0.3, dict(x=(bx1 - bx0) * 0.5, y=(by1 - by0) * 0.5 - 90, s=1.1), 'power2.in'),
         (t_this + 0.05, dict(x=bx1 - bx0, y=by1 - by0, s=0.9), 'power3.out'), (t_this + 0.25, dict(s=1.0), 'back.out(2)'))
    fx.hold['card-badge'] = False
    fx.k('bdg', (tb - 0.05, dict(o=0)), (tb + 0.12, dict(o=1)))
    fx.k('ccring', (t_this, dict(o=0)), (t_this + 0.35, dict(o=1)))
    moves = [dict(t=0.2, dur=t_cc - 0.5, kind='glide', to=dict(x=800, y=530, s=1.02)),
             dict(t=t_cc - 0.25, dur=1.5, kind='push', to=dict(x=560, y=420, s=1.25))]
    cfg = dict(id='g09', dur=b['dur'], mode='fvp', cam0=dict(x=784, y=540, s=1.0), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=0.9),
               heroes=[dict(t=0, id='none'), dict(t=t_cc - 0.2, id='cc')],
               sfx=[dict(t=r3(t_prov - 0.15), type='pop'), dict(t=r3(t_third - 0.15), type='pop'), dict(t=r3(t_this + 0.05), type='pop')])
    page('g09', cfg, extra_css=EXTRA_CSS, extra_js=fx.js())


# ---------------------------------------------------------------------------------------------------------------
# PiP bottom-left stretch (r03 g10 g11 g12): content in x 416-1856, anchor [1136, 540].
AN2 = [1136, 540]


def spinner(id, size=34, style='', track='#E3E5E9'):
    """#id fades, #idr spins"""
    return (f'<div id="{id}" class="abs" style="width:{size}px;height:{size}px;{style}"><div id="{id}r" class="abs" style="inset:0;border-radius:50%;'
            f'border:4px solid {track};border-top-color:{AZ}"></div></div>')


def spin(fx, id, t0, t1, rps=1.6):
    fx.k(id, (t0, dict(r=0)), (t1, dict(r=360 * rps * (t1 - t0)), 'linear'))


# g10 - "if the agent does something you don't like in the chat, add a rule to this file ... or give it guidelines":
# a chat window (paper) whose message gets an ember outline; the AGENTS.md window types two rules with an azure caret.
def g10():
    b, ws = words('g10')
    fx = FX()
    claude, _, _ = logo('claude_symbol.png')
    amd, _, _ = logo('agentsmd_mark_on-light.png')
    t_agent, t_dont, t_rule, t_guid = T(ws, 'agent'), T(ws, 'dont'), T(ws, 'rule', 2), T(ws, 'guidelines')
    CW_, CH_ = 1180, 250
    msg = 'Tests were failing, so I deleted them. All green now'
    chat = (win_head(claude, 'Claude', badge='chat') +
            f'<div class="abs" style="left:36px;top:110px;width:{CW_ - 72}px;height:110px;border-radius:14px;background:{PAPER2}"></div>'
            f'<div class="abs" style="left:66px;top:141px;font:400 34px/48px Figtree;color:{INK};white-space:nowrap">{msg}'
            f'<span style="display:inline-block;width:44px;height:44px;margin-left:14px;vertical-align:-10px;position:relative">'
            + check_badge('', 44, style='left:0;top:0') + '</span></div>'
            f'<div id="redout" class="abs" style="left:28px;top:102px;width:{CW_ - 56}px;height:126px;border-radius:20px;border:4px solid {EMB};'
            f'box-shadow:0 0 0 8px rgba(255,138,91,.14),0 0 30px rgba(255,138,91,.45);opacity:0"></div>')
    DW, DH = 1180, 360
    lines = [('## Rules', 1, None), ('- Use TypeScript strict mode.', 0, None), ('', 0, 'r1'), ('', 0, 'r2')]
    body = ''
    for i, (txt, head, tid) in enumerate(lines):
        idh = f' id="{tid}"' if tid else ''
        body += (f'<div{idh} class="abs m" style="left:40px;top:{116 + 52 * i}px;font-size:30px;line-height:50px;white-space:pre;'
                 f'color:{INK if (head or tid) else INK2};font-weight:{600 if head else 400}">{txt}</div>')
    doc = win_head(amd, 'AGENTS.md', badge='repo root', logo_sz=48, mono_title=True) + body
    CY, DY = 290, 730
    cards = [dict(id='chat', kind='window', x=1136, y=CY, w=CW_, h=CH_, html=chat, land=dict(t=r3(t_agent - 0.12), dur=0.55)),
             dict(id='doc', kind='window', x=1136, y=DY, w=DW, h=DH, html=doc)]
    fx.k('redout', (t_dont - 0.1, dict(o=0, s=1.04)), (t_dont + 0.25, dict(o=1, s=1), 'power3.out'))
    l1 = '- Never delete or skip a failing test. Fix the code instead.'
    l2 = "- Run npm test before you say you're done."
    fx.type('r1', t_rule, l1, cps=32, caretFrom=t_rule - 0.3, caretTo=t_rule + len(l1) / 32 + 0.5)
    fx.type('r2', t_guid, l2, cps=32, caretFrom=t_guid - 0.3, caretTo=b['dur'] + 1)
    moves = [dict(t=0.2, dur=t_rule - 0.6, kind='glide', to=dict(x=1136, y=530, s=1.02)),
             dict(t=t_rule - 0.45, dur=1.3, kind='push', to=dict(x=1136, y=540, s=1.12)),
             dict(t=t_rule + 0.9, dur=b['dur'] - t_rule - 0.9, kind='glide', to=dict(x=1136, y=548, s=1.14))]
    cfg = dict(id='g10', dur=b['dur'], mode='fvp', anchor=AN2, cam0=dict(x=1136, y=530, s=1.0), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=0.8),
               heroes=[dict(t=0, id='none'), dict(t=t_rule - 0.4, id='doc')],
               sfx=[dict(t=r3(t_agent - 0.12), type='pop'), *keyrun(t_rule, len(l1), 32), *keyrun(t_guid, len(l2), 32)])
    page('g10', cfg, extra_css=EXTRA_CSS, extra_js=fx.js())


# g11 - the context window fills up -> the agent writes HANDOFF.md (done / next) -> a fresh session starts from it
TOOLROWS = ['Read(src/db.ts)', 'Edit(src/auth.ts)', 'Bash(npm test)', 'Grep("session")', 'Edit(src/routes.ts)', 'Read(package.json)',
            'Bash(npm run lint)', 'Edit(src/login.tsx)', 'Glob(src/**/*.ts)', 'Edit(src/api/user.ts)', 'Bash(npm test)', 'Read(README.md)',
            'Edit(src/auth.ts)', 'WebFetch(nextjs.org/docs)', 'Edit(src/middleware.ts)', 'Bash(npm test)', 'Read(src/config.ts)', 'Edit(src/db.ts)']


def session_card(prefix, pct, rows, prompt_id=None, title_extra=''):
    W_, H_ = 720, 760
    tr = ''.join(f'<div class="abs m" style="left:0;top:{52 * i}px;font-size:30px;line-height:46px;color:{INK2};white-space:nowrap">'
                 f'<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:{MINT};margin-right:18px;vertical-align:2px"></span>{r}</div>'
                 for i, r in enumerate(rows))
    return (win_head('assets/claude_symbol.png', 'Claude Code', extra=title_extra) +
            f'<div class="abs" style="left:36px;top:104px;font:500 30px/44px Figtree;color:{INK2}">Context</div>'
            f'<div id="{prefix}num" class="abs" style="right:36px;top:100px;font:600 34px/48px Figtree;color:{INK}">{pct}%</div>'
            f'<div class="abs" style="left:36px;top:160px;width:{W_ - 72}px;height:18px;border-radius:9px;background:{PAPER2};overflow:hidden">'
            f'<div id="{prefix}fill" class="abs" style="left:0;top:0;width:{(W_ - 72) * pct / 100:.0f}px;height:100%;border-radius:9px;background:{AZ}">'
            f'<div id="{prefix}red" class="abs" style="inset:0;border-radius:9px;background:{EMB};opacity:0"></div></div></div>'
            f'<div class="abs" style="left:36px;top:210px;width:{W_ - 72}px;height:356px;overflow:hidden">'
            f'<div id="{prefix}list" class="abs" style="left:0;top:0">{tr}</div></div>'
            f'<div class="abs" style="left:36px;top:590px;width:{W_ - 72}px;height:136px;border-radius:14px;border:1.5px solid {PLINE};background:{PAPER2}"></div>'
            + (f'<div id="{prompt_id}" class="abs m" style="left:60px;top:608px;width:{W_ - 120}px;font-size:30px;line-height:48px;color:{INK};white-space:pre-wrap"></div>' if prompt_id else ''))


def g11():
    b, ws = words('g11')
    fx = FX()
    logo('claude_symbol.png')
    t_way, t_limit, t_ask, t_store, t_prog, t_still, t_done, t_sep, t_files = (T(ws, 'way'), T(ws, 'limit'), T(ws, 'ask'), T(ws, 'store'),
                                                                                 T(ws, 'progress'), T(ws, 'still'), T(ws, 'done'), T(ws, 'separate'), T(ws, 'files', 2))
    S1X, S1Y = 820, 540
    HX, HY, HW, HH = 1530, 560, 560, 560
    S2X, S2Y = 2240, 540
    s1 = session_card('a', 55, TOOLROWS, prompt_id='ptxt')
    s2 = session_card('b', 4, [], title_extra='<div class="abs" style="right:30px;top:26px"><span class="pl mint">New session</span></div>')
    s2 += (f'<div id="att" class="abs" style="left:60px;top:618px;width:300px;height:64px;border-radius:14px;background:{AZWASH};border:2px solid {AZ};opacity:0">'
           + file_icon(16, 12, 38) + f'<div class="abs m" style="left:62px;top:8px;font-size:30px;line-height:46px;color:{INK}">HANDOFF.md</div></div>'
           f'<div id="rd0" class="abs m" style="left:36px;top:214px;font-size:30px;line-height:46px;color:{INK2};white-space:nowrap;opacity:0">'
           f'<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:{MINT};margin-right:18px;vertical-align:2px"></span>Read(HANDOFF.md)</div>')
    hl = [('## Done', 1, 'hd'), ('- Login + Google auth', 0, 'h1'), ('- 42 tests passing', 0, 'h2'), ('## Next', 1, 'hn'), ('- Password reset', 0, 'h3'), ('- Deploy to staging', 0, 'h4')]
    hbody = ''
    for i, (txt, head, hid) in enumerate(hl):
        y = 112 + 54 * i + (22 if i >= 3 else 0)
        hbody += (f'<div id="{hid}" class="abs m" style="left:40px;top:{y}px;font-size:30px;line-height:48px;white-space:pre;opacity:0;'
                  f'color:{INK};font-weight:{600 if head else 400}">{txt}</div>')
    hand = (file_icon(36, 22, 44) +
            f'<div class="abs m" style="left:92px;top:18px;font-size:34px;line-height:52px;color:{INK};font-weight:600">HANDOFF.md</div>'
            f'<div class="abs" style="left:0;top:84px;width:100%;height:1.5px;background:{PLINE}"></div>' + hbody)
    cards = [dict(id='s1', kind='window', x=S1X, y=S1Y, w=720, h=760, html=s1),
             dict(id='s2', kind='window', x=S2X, y=S2Y, w=720, h=760, html=s2, land=dict(t=r3(t_sep - 0.4), dur=0.55)),
             dict(id='hand', kind='paper', x=HX, y=HY, w=HW, h=HH, html=hand, land=dict(t=r3(t_store - 0.12), dur=0.55), noDof=True)]
    import math
    f0, f1 = t_way - 0.1, t_limit + 0.1
    BW = 720 - 72
    fx.k('afill', (f0, dict(w=BW * 0.55)), (f1, dict(w=BW * 0.96), 'sine.inOut'))
    u85 = math.acos(1 - 2 * (85 - 55) / (96 - 55)) / math.pi
    t85 = f0 + u85 * (f1 - f0)
    fx.k('ared', (t85 - 0.1, dict(o=0)), (t85 + 0.15, dict(o=1)))
    fx.number('anum', [(f0, 55), (f1, 96, 'sine.inOut')], fmt='int', suf='%')
    fx.toggle('anum', 'hot', t85)
    rows_h = 52 * len(TOOLROWS) - 356
    fx.k('alist', (t_way - 1.0, dict(y=0)), (t_limit + 0.2, dict(y=-rows_h), 'sine.inOut'))
    prompt = "Write a hand-off doc: what's done and what's next."
    fx.type('ptxt', t_ask - 0.05, prompt, cps=34, caretFrom=t_ask - 0.4, caretTo=t_ask + len(prompt) / 34 + 0.6)
    for hid, tt in (('hd', t_prog - 0.1), ('h1', t_prog + 0.12), ('h2', t_prog + 0.32), ('hn', t_still - 0.1), ('h3', t_still + 0.14), ('h4', t_still + 0.36)):
        fx.k(hid, (tt, dict(o=0, x=-12)), (tt + 0.3, dict(o=1, x=0), 'power3.out'))
    tm = t_sep - 0.1
    dx, dy = S2X - HX, (S2Y - 380 + 658) - HY
    fx.k('card-hand', (tm, dict(x=0, y=0, s=1, o=1)), (t_files - 0.05, dict(x=dx, y=dy, s=0.32), 'power3.inOut'), (t_files + 0.1, dict(o=0)))
    fx.hold['card-hand'] = False
    fx.k('att', (t_files - 0.1, dict(o=0, s=0.8)), (t_files + 0.25, dict(o=1, s=1), 'back.out(2)'))
    fx.k('rd0', (t_files + 0.25, dict(o=0, x=-10)), (t_files + 0.55, dict(o=1, x=0), 'power3.out'))
    cards[0]['exit'] = dict(t=r3(t_sep - 0.3), dur=0.6)
    moves = [dict(t=t_way - 0.45, dur=1.4, kind='push', to=dict(x=S1X, y=410, s=1.22)),
             dict(t=t_ask - 0.55, dur=1.2, kind='pull', to=dict(x=1150, y=540, s=1.0)),
             dict(t=t_prog - 0.4, dur=1.2, kind='push', to=dict(x=1420, y=560, s=1.08)),
             dict(t=t_sep - 0.35, dur=1.0, kind='step', to=dict(x=2240, y=540, s=1.0))]
    cfg = dict(id='g11', dur=b['dur'], mode='fvp', anchor=AN2, cam0=dict(x=1136, y=540, s=1.0), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=0.8),
               heroes=[dict(t=0, id='none'), dict(t=t_way - 0.4, id='s1'), dict(t=t_ask - 0.5, id='none'), dict(t=t_prog - 0.35, id='hand'),
                       dict(t=t_sep - 0.3, id='none')],
               sfx=[*keyrun(t_ask - 0.05, len(prompt), 34), dict(t=r3(t_store - 0.12), type='pop'),
                    *[dict(t=r3(t), type='key') for t in (t_prog - 0.1, t_prog + 0.12, t_prog + 0.32, t_still - 0.1, t_still + 0.14, t_still + 0.36)],
                    dict(t=r3(t_sep - 0.4), type='pop'), dict(t=r3(t_files + 0.1), type='chime')])
    page('g11', cfg, extra_css=EXTRA_CSS + f'.hot{{color:{EMINK} !important}}', extra_js=fx.js())


# g12 - the Stop-hook loop: done -> Stop -> verify.sh (his real hook) on a glass panel -> CHANGELOG not updated ->
# exit 2 feeds back to Claude (ember) -> it adds the entry -> the check passes (mint); then "Pull request opened?" and
# "Test suite ran?" pass on their words.
def g12():
    b, ws = words('g12')
    fx = FX()
    claude, _, _ = logo('claude_symbol.png')
    t_cl, t_wasnt, t_tell, t_go, t_add, t_cl2, t_enf, t_pr, t_test = (T(ws, 'changelog'), T(ws, 'wasnt'), T(ws, 'tell'), T(ws, 'go'), T(ws, 'add'),
                                                                      T(ws, 'changelog', 2), T(ws, 'enforcing'), T(ws, 'pr'), T(ws, 'test'))
    AX_, AY_, AW_, AH_ = 760, 450, 640, 650
    VX, VY, VW, VH = 1520, 420, 600, 560
    fb_text = 'Add an entry to CHANGELOG.md before you stop.'
    agent = (win_head(claude, 'Claude', badge='session') +
             f'<div class="abs" style="left:36px;top:108px;width:{AW_ - 72}px;height:76px;border-radius:14px;background:{PAPER2}"></div>'
             f'<div class="abs" style="left:62px;top:122px;font:400 32px/48px Figtree;color:{INK}">Done. The login page is ready.</div>'
             f'<div id="fbk" class="abs" style="left:36px;top:204px;width:{AW_ - 72}px;height:160px;border-radius:14px;background:{EMWASH};border:2px solid {EMB};opacity:0">'
             '<div class="abs" style="left:20px;top:18px"><span class="pl ember">Stop hook · exit 2</span></div>'
             f'<div class="abs" style="left:22px;top:70px;width:{AW_ - 110}px;font:400 30px/42px Figtree;color:{INK}">{fb_text}</div></div>'
             f'<div id="edl" class="abs m" style="left:40px;top:390px;font-size:30px;line-height:46px;color:{INK};opacity:0">'
             f'<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:{MINT};margin-right:18px;vertical-align:2px"></span>'
             f'<b style="font-weight:700">Edit</b>(CHANGELOG.md)</div>'
             f'<div id="edbox" class="abs" style="left:36px;top:448px;width:{AW_ - 72}px;height:170px;border-radius:14px;background:{PAPER2};opacity:0"></div>'
             f'<div id="ed1" class="abs m" style="left:64px;top:470px;font-size:30px;line-height:46px;color:{INK};font-weight:600;white-space:pre"></div>'
             f'<div id="ed2" class="abs m" style="left:64px;top:518px;font-size:30px;line-height:46px;color:{MINTINK};white-space:pre"></div>')
    rows = [('CHANGELOG.md updated?', 'c0'), ('Pull request opened?', 'c1'), ('Test suite ran?', 'c2')]
    vrows = ''
    for i, (txt, rid) in enumerate(rows):
        y = 196 + 100 * i
        vrows += (f'<div id="{rid}" class="abs" style="left:0;top:{y}px;width:100%;height:80px;{"" if i == 0 else "opacity:0"}">'
                  f'<div class="abs" style="left:40px;top:16px;font:500 32px/48px Figtree;color:{WHITE}">{txt}</div>'
                  + (spinner('sp0', 38, f'left:{VW - 96}px;top:21px', track=BAR) + cross_badge('x0', 48, style=f'left:{VW - 101}px;top:16px;opacity:0') if i == 0 else '')
                  + check_badge(f'k{i}', 48, style=f'left:{VW - 101}px;top:16px;opacity:0') + '</div>')
    verify = (hook_badge('', 44, 'left:36px;top:24px') +
              f'<div class="abs m" style="left:96px;top:20px;font-size:32px;line-height:52px;color:{WHITE};font-weight:600">Stop</div>'
              + svg(li(ARROW_P, T2, 2.2), 196, 34, 28) +
              f'<div class="abs m" style="left:240px;top:20px;font-size:32px;line-height:52px;color:{WHITE};font-weight:600">verify.sh</div>'
              f'<div class="abs" style="left:0;top:96px;width:100%;height:1px;background:{HAIR}"></div>'
              + spinner('sps', 30, 'left:40px;top:128px', track=BAR) +
              f'<div id="st_run" class="abs lab" style="left:88px;top:131px">Running verify.sh…</div>'
              f'<div id="st_blk" class="abs lab ember" style="left:40px;top:131px;opacity:0">Exit 2 · blocked</div>'
              f'<div id="st_ok" class="abs lab mint" style="left:40px;top:131px;opacity:0">Checks passed</div>'
              f'<div class="abs" style="left:40px;top:180px;width:{VW - 80}px;height:1px;background:{HAIR}"></div>' + vrows)
    GX, GY, GW, GH = 400, 100, 1500, 900
    def L(x, y): return (x - GX, y - GY)
    s0, s1 = L(AX_ + AW_ / 2 + 8, 300), L(VX - VW / 2 - 8, 300)
    f0p = [L(VX - VW / 2 + 120, VY + VH / 2 + 6), L(VX - VW / 2 + 120, VY + VH / 2 + 110), L(AX_ + AW_ / 2 + 140, AY_ - AH_ / 2 + 284), L(AX_ + AW_ / 2 + 8, AY_ - AH_ / 2 + 284)]
    agl = 'filter:drop-shadow(0 0 6px rgba(47,149,255,.8))'
    egl = 'filter:drop-shadow(0 0 6px rgba(255,138,91,.8))'
    conn = (f'<svg class="abs" style="left:0;top:0;width:{GW}px;height:{GH}px;overflow:visible" viewBox="0 0 {GW} {GH}">'
            f'<path d="M{s0[0]} {s0[1]} L{s1[0] - 14} {s1[1]}" stroke="rgba(47,149,255,.75)" stroke-width="4" stroke-linecap="round" style="{agl}"/>'
            f'<path d="M{s1[0] - 26} {s1[1] - 12} L{s1[0] - 12} {s1[1]} L{s1[0] - 26} {s1[1] + 12}" fill="none" stroke="rgba(47,149,255,.75)" stroke-width="4" '
            f'stroke-linecap="round" stroke-linejoin="round" style="{agl}"/>'
            f'<path id="fbp" d="M{f0p[0][0]} {f0p[0][1]} C{f0p[1][0]} {f0p[1][1]} {f0p[2][0]} {f0p[2][1]} {f0p[3][0]} {f0p[3][1]}" pathLength="1" '
            f'stroke-dasharray="1" stroke-dashoffset="1" fill="none" stroke="{EMB}" stroke-width="4" stroke-linecap="round" style="{egl}"/></svg>'
            f'<div id="fpk" class="abs" style="left:-14px;top:-14px;width:28px;height:28px;border-radius:50%;background:{EMB};'
            f'box-shadow:0 0 0 7px rgba(255,138,91,.18),0 0 24px rgba(255,138,91,.9);opacity:0"></div>')
    cards = [dict(id='conn', kind='plain', x=GX + GW / 2, y=GY + GH / 2, w=GW, h=GH, html=conn, clip=False, noDof=True),
             dict(id='ag', kind='window', x=AX_, y=AY_, w=AW_, h=AH_, html=agent),
             dict(id='vf', kind='glass', x=VX, y=VY, w=VW, h=VH, html=verify)]
    spin(fx, 'spsr', 0, b['dur'])
    spin(fx, 'sp0r', 0, b['dur'])
    fx.k('sps', (t_wasnt - 0.05, dict(o=1)), (t_wasnt + 0.1, dict(o=0)), (t_enf - 0.7, dict(o=0)), (t_enf - 0.6, dict(o=1)), (t_enf - 0.05, dict(o=1)), (t_enf + 0.1, dict(o=0)))
    fx.k('sp0', (t_wasnt - 0.05, dict(o=1)), (t_wasnt + 0.05, dict(o=0)), (t_enf - 0.7, dict(o=0)), (t_enf - 0.6, dict(o=1)), (t_enf - 0.05, dict(o=1)), (t_enf + 0.05, dict(o=0)))
    fx.k('x0', (t_wasnt - 0.04, dict(o=0, s=0.4)), (t_wasnt + 0.3, dict(o=1, s=1), 'back.out(2.4)'), (t_enf - 0.75, dict(o=1)), (t_enf - 0.6, dict(o=0)))
    fx.k('st_run', (t_wasnt - 0.05, dict(o=1)), (t_wasnt + 0.1, dict(o=0)), (t_enf - 0.7, dict(o=0)), (t_enf - 0.55, dict(o=1)), (t_enf - 0.05, dict(o=1)), (t_enf + 0.1, dict(o=0)))
    fx.k('st_blk', (t_wasnt, dict(o=0, y=6)), (t_wasnt + 0.25, dict(o=1, y=0), 'power2.out'), (t_enf - 0.8, dict(o=1)), (t_enf - 0.65, dict(o=0)))
    fx.k('st_ok', (t_enf, dict(o=0, y=6)), (t_enf + 0.25, dict(o=1, y=0), 'power2.out'))
    fx.k('fbp', (t_tell - 0.35, dict(dash=1, o=1)), (t_tell + 0.2, dict(dash=0), 'power2.inOut'), (t_go + 0.3, dict(o=1)), (t_go + 0.8, dict(o=0)))
    pts = bez(*f0p, n=10)
    fr = [(t_tell - 0.36, dict(o=0, x=pts[0][0], y=pts[0][1]))]
    for i, (x, y) in enumerate(pts):
        fr.append((t_tell - 0.35 + 0.55 * i / (len(pts) - 1), dict(o=1, x=x, y=y), 'linear'))
    fr.append((t_tell + 0.3, dict(o=0, x=pts[-1][0], y=pts[-1][1])))
    fx.k('fpk', *fr)
    fx.k('fbk', (t_tell + 0.1, dict(o=0, x=16)), (t_tell + 0.45, dict(o=1, x=0), 'power3.out'))
    fx.k('edl', (t_go - 0.1, dict(o=0, y=10)), (t_go + 0.25, dict(o=1, y=0), 'power3.out'))
    fx.k('edbox', (t_go + 0.1, dict(o=0)), (t_go + 0.35, dict(o=1)))
    fx.type('ed1', t_add - 0.1, '## Unreleased', cps=26, caret=False)
    fx.type('ed2', t_add - 0.1 + 13 / 26 + 0.1, '- Added login page', cps=26, caretFrom=t_add - 0.1, caretTo=t_enf - 0.7)
    fx.k('k0', (t_enf - 0.04, dict(o=0, s=0.4)), (t_enf + 0.32, dict(o=1, s=1), 'back.out(2.4)'))
    for i, tt in ((1, t_pr), (2, t_test)):
        fx.k(f'c{i}', (tt - 0.3, dict(o=0, y=14)), (tt + 0.05, dict(o=1, y=0), 'power3.out'))
        fx.k(f'k{i}', (tt - 0.04, dict(o=0, s=0.4)), (tt + 0.32, dict(o=1, s=1), 'back.out(2.4)'))
    Sv = 1.15
    moves = [dict(t=t_wasnt - 0.6, dur=1.0, kind='push', to=dict(x=VX - 40, y=VY, s=Sv)),
             dict(t=t_tell - 0.35, dur=0.9, kind='pull', to=dict(x=1136, y=450, s=1.0)),
             dict(t=t_go - 0.35, dur=1.0, kind='push', to=dict(x=AX_ + 30, y=AY_ + 20, s=Sv)),
             dict(t=t_enf - 0.6, dur=0.8, kind='step', to=dict(x=VX - 40, y=VY + 30, s=Sv)),
             dict(t=t_enf + 0.4, dur=b['dur'] - t_enf - 0.4, kind='glide', to=dict(x=VX - 40, y=VY + 40, s=Sv + 0.03))]
    cfg = dict(id='g12', dur=b['dur'], mode='fvp', anchor=AN2, cam0=dict(x=1136, y=450, s=1.0), cards=cards, moves=moves, pushRef=1.0,
               wave=dict(level='low', k=0.8),
               heroes=[dict(t=0, id='none'), dict(t=t_wasnt - 0.5, id='vf'), dict(t=t_tell - 0.3, id='none'), dict(t=t_go - 0.3, id='ag'),
                       dict(t=t_enf - 0.5, id='vf')],
               sfx=[dict(t=r3(t_wasnt), type='pop'), dict(t=r3(t_tell + 0.15), type='pop'), *keyrun(t_add - 0.1, 35, 26),
                    dict(t=r3(t_enf), type='chime'), dict(t=r3(t_pr), type='pop'), dict(t=r3(t_test), type='pop')])
    page('g12', cfg, extra_css=EXTRA_CSS, extra_js=fx.js())


# ---------------------------------------------------------------------------------------------------------------
BEATS = ['g01', 'g02', 'g03', 'r01', 'g04', 'g05', 'g06', 'r02', 'g07', 'g08', 'g09', 'r03', 'g10', 'g11', 'g12']


def build():
    for bid in BEATS:
        if ONLY and bid not in ONLY: continue
        fn = globals().get(bid)
        if not fn: continue
        try:
            fn()
        except FileNotFoundError as e:
            print(f'SKIP {bid}: {e}')
