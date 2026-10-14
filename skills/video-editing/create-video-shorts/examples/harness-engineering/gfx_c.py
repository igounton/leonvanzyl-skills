# Graphics agent C: short s4 "20 AI agents, one factory" - s4_r0 s4_r2 s4_r3 s4_r4 s4_r5 s4_r6.
# ONE continuous software-factory world (the long-form g20/g21 factory() re-laid out for 9:16): every state is a pure
# function of factory time F = the short's own time (run T0 + t), so each composition renders its own window of it and
# the story carries across the cuts, including over the full-cam run r1 that sits between r0 and r2.
# World (world px = screen px at camera s 1), top to bottom: two app repos as white GitHub windows (cubefarm, smolcoder),
# the Factory on glass (GitHub Actions, the private software-factory repo), the Agent Swarm on highlighted glass
# (Leon's mint Orchestrate robot tile; 5 x 4 = 20 workers: Claude Code / Codex / your own harness = his iris "Build" tile).
# Never Upstash: no name, logo or "Box" anywhere.
# Build: $PY scripts/build_gfx.py c
from build_gfx_common import *

AZ, EM, MI, IR = '#2F95FF', '#FF8A5B', '#4FD6A0', '#9C7CFF'
TS, TM = '#A3A6AD', '#7E818A'
INK, INK2 = '#111214', '#5F636B'

LINE = {
    'lock': '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8.2 10.5V8a3.8 3.8 0 017.6 0v2.5"/>',
    'robot': '<rect x="4" y="7.5" width="16" height="11.5" rx="4"/><path d="M12 7.5V4"/><circle cx="12" cy="3.2" r="1.1"/><path d="M9.3 12v2.4M14.7 12v2.4"/>',
    'pause': '<path d="M9 6.5v11M15 6.5v11"/>',
}


def line_ico(name, size, color='#fff', width=2.0, style=''):
    return (f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;flex:none;{style}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{LINE[name]}</svg>')


def robot_tile(size, tilt=0):
    """Leon's Orchestrate tile: the mint tile with two eyes and an antenna ball on top (long-form gfx_b.robot_tile)"""
    ah = round(size * 0.2)
    return (f'<div style="position:relative;width:{size}px;height:{size}px;flex:none;transform:rotate({tilt}deg)">'
            f'<div class="abs" style="left:{size / 2 - 2.5:.1f}px;top:{-ah}px;width:5px;height:{ah + 4}px;border-radius:3px;background:#5AD9A6"></div>'
            f'<div class="abs" style="left:{size / 2 - size * 0.075:.1f}px;top:{-ah - size * 0.12:.1f}px;width:{size * 0.15:.1f}px;height:{size * 0.15:.1f}px;'
            f'border-radius:50%;background:linear-gradient(155deg,#C4F6DF,#4FD6A0);box-shadow:0 0 12px rgba(79,214,160,.6)"></div>'
            f'{tile_html("mint", "eyes", size, 0)}</div>')


def img(src, w=None, h=None, style=''):
    wh = (f'width:{w}px;' if w else '') + (f'height:{h}px;' if h else '')
    return f'<img src="{src}" style="{wh}display:block;object-fit:contain;{style}">'


OPEN_ISSUE = ('<svg viewBox="0 0 16 16" style="width:{s}px;height:{s}px;flex:none"><circle cx="8" cy="8" r="6.6" fill="none" stroke="#0F7A52" stroke-width="1.6"/>'
              '<circle cx="8" cy="8" r="1.7" fill="#0F7A52"/></svg>')
LABELS = {'ready': ('mint', 'ready'), 'run': ('azure', 'factory:running')}
CURSOR = ('<svg viewBox="0 0 24 24" style="width:58px;height:58px;display:block;filter:drop-shadow(0 6px 10px rgba(0,0,0,.55))">'
          '<path d="M5 3.2v16.4l4.3-4.1 2.9 6.3 2.9-1.3-2.9-6.2 5.9-.3z" fill="#fff" stroke="#111214" stroke-width="1.4" stroke-linejoin="round"/></svg>')


def gh_label(lid, kind, fs=36, style=''):
    tone, txt = LABELS[kind]
    return f'<div id="{lid}" class="abs pl {tone}" style="font-size:{fs}px;opacity:0;transform-origin:0 50%;{style}">{txt}</div>'


GLASS_PAPER = 'background:#fff;box-shadow:0 34px 80px -24px rgba(0,0,0,.8);color:#111214;'

CCSS = """
.fx{display:flex;align-items:center}
.abs{position:absolute}
.gm{font-family:'Geist Mono',monospace;font-weight:500}
.pl{display:inline-block;font:500 36px/1 'Geist Mono';letter-spacing:.03em;padding:10px 18px;border-radius:999px;white-space:nowrap}
.pl.azure{background:#E8F2FF;color:#1560D0}.pl.mint{background:#E3F8EF;color:#0F7A52}.pl.ember{background:#FFEFE7;color:#B8461A}
.spin{border-radius:50%;border:5px solid rgba(47,149,255,.25);border-top-color:#2F95FF}
.wk{position:absolute;border-radius:22px;background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.10);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 18px 30px -16px rgba(0,0,0,.7)}
.ring{position:absolute;border-radius:28px;pointer-events:none}
"""
FV_MASK = ('#viewport{-webkit-mask-image:linear-gradient(to bottom,#000 0,#000 1238px,transparent 1292px);'
           'mask-image:linear-gradient(to bottom,#000 0,#000 1238px,transparent 1292px)}')

CJS = r"""
window.B = (function () {
  const E = (n) => (n === 'linear' ? (p) => p : gsap.parseEase(n));
  const cl = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, p) => a + (b - a) * p;
  const P = (t, t0, d, e) => { const x = cl((t - t0) / (d || 1e-6), 0, 1); return e ? E(e)(x) : x; };
  const C = {};
  const $ = (id) => { if (!(id in C)) C[id] = document.getElementById(id); return C[id]; };
  function qb(a, c, b, p) { const q = 1 - p; return [q * q * a[0] + 2 * q * p * c[0] + p * p * b[0], q * q * a[1] + 2 * q * p * c[1] + p * p * b[1]]; }
  return { E, cl, lerp, P, $, qb };
})();
window.CFG_RENDER = function (t, cam) {
  const d = CFG.data, F = t + d.OFF;
  const P = (t0, du, e) => B.P(F, t0, du, e);
  const lod = B.cl((cam.s - 0.86) / 0.1, 0, 1);
  // ---------------- workers
  let nIn = 0, nBusy = 0;
  let hlAnyG = 0; const hlv = {};
  Object.keys(d.hl).forEach((ty) => { const h = d.hl[ty]; const v = P(h[0], 0.3, 'power2.out') * (1 - P(h[1], 0.45, 'power2.inOut')); hlv[ty] = v; hlAnyG = Math.max(hlAnyG, v); });
  d.workers.forEach((w) => {
    const i = w.i, el = B.$('wk' + i);
    const pin = P(w.tin, 0.42, 'back.out(1.7)');
    if (F >= w.tin + 0.1) nIn++;
    const flip = P(w.tflip, 0.36, 'power2.inOut');
    const base = P(w.tdim, 0.6, 'power2.inOut') * (1 - 0.5 * P(w.tflip + 0.16, 0.35, 'power2.out'));
    const hlMine = hlv[w.ty] || 0;
    const busy = w.busy != null ? P(w.busy, 0.3, 'power2.out') : 0;
    if (w.busy != null && F >= w.busy) nBusy++;
    const claim = w.claim != null ? P(w.claim, 0.25, 'power2.out') : 0;
    let dim = (1 - hlMine) * B.lerp(base, 0.92, hlAnyG);
    dim *= 1 - Math.max(busy, claim * 0.8);
    const breathe = 0.05 * Math.sin(F * 1.8 + i * 0.9) * dim;
    el.style.opacity = Math.min(1, pin * 1.6).toFixed(3);
    const bump = (w.busy != null ? Math.sin(Math.PI * P(w.busy - 0.05, 0.35)) : 0) + 0.07 * Math.sin(Math.PI * flip);
    el.style.transform = 'scale(' + (B.lerp(0.55, 1, pin) * (1 + 0.05 * hlMine + 0.06 * bump)).toFixed(4) + ')';
    el.style.background = busy > 0.01 ? 'rgba(47,149,255,' + (0.055 + 0.09 * busy).toFixed(3) + ')' : 'rgba(255,255,255,.055)';
    const wc = B.$('wc' + i);
    wc.style.opacity = (1 - 0.58 * dim + breathe).toFixed(3);
    wc.style.filter = dim > 0.01 ? 'grayscale(' + (0.9 * dim).toFixed(3) + ')' : 'none';
    B.$('wslot' + i).style.opacity = (1 - Math.min(1, pin * 2)).toFixed(3);
    // the flip: the generic robot turns into the agent's real harness logo ("a mix of agents")
    const fr = B.$('wfr' + i), bk = B.$('wbk' + i);
    if (flip < 0.5) { fr.style.opacity = 1; fr.style.transform = 'perspective(320px) rotateY(' + (flip * 180).toFixed(1) + 'deg)'; bk.style.opacity = 0; }
    else { fr.style.opacity = 0; bk.style.opacity = 1; bk.style.transform = 'perspective(320px) rotateY(' + (-(1 - flip) * 180).toFixed(1) + 'deg)'; }
    const nA = 1 - P(w.tflip + 0.08, 0.2), nB = P(w.tflip + 0.14, 0.2);
    B.$('wna' + i).style.opacity = (nA * (1 - busy) * lod).toFixed(3);
    B.$('wnb' + i).style.opacity = (nB * (1 - busy) * lod).toFixed(3);
    B.$('wp' + i).style.opacity = (P(w.tdim, 0.4) * (1 - busy) * (1 - 0.5 * hlMine)).toFixed(3);
    const sp = B.$('ws' + i); sp.style.opacity = busy.toFixed(3); sp.style.transform = 'rotate(' + ((F * 400 + i * 37) % 360).toFixed(1) + 'deg)';
    B.$('wi' + i).style.opacity = busy.toFixed(3);
    B.$('wr' + i).style.opacity = busy.toFixed(3);
    B.$('wh' + i).style.opacity = (hlMine * pin * (1 - busy)).toFixed(3);
    const f = B.$('wf' + i);
    let fo = 0, fs = 1;
    if (w.claim != null && F >= w.claim) { const q = P(w.claim, 0.75, 'power2.out'); fo = (1 - q) * 0.95; fs = 1 + 0.35 * q; }
    f.style.opacity = fo.toFixed(3); f.style.transform = 'scale(' + fs.toFixed(4) + ')';
  });
  // ---------------- pool header counter, sweeps, the full-pool ember glow
  const c2 = P(d.t_count2, 0.3);
  B.$('pc0').textContent = nIn + ' agents'; B.$('pc0').style.opacity = (1 - c2).toFixed(3);
  const col = nBusy >= 20 ? '#FF8A5B' : nBusy > 0 ? '#2F95FF' : '#A3A6AD';
  B.$('pcn').textContent = nBusy; B.$('pcn').style.color = col; B.$('pc1').style.opacity = c2.toFixed(3);
  let sw = 0, sx = 0;
  d.sweeps.forEach((s0) => { if (F >= s0 && F < s0 + 1.1) { const q = (F - s0) / 1.1; sw = Math.sin(Math.PI * q); sx = q; } });
  B.$('psweep').style.opacity = sw.toFixed(3); B.$('psweep').style.transform = 'translateX(' + (-320 + sx * 1330).toFixed(1) + 'px)';
  B.$('pember').style.opacity = (P(d.t_full, 0.35, 'power2.out') * (0.8 + 0.2 * Math.sin((F - d.t_full) * 9))).toFixed(3);
  // ---------------- factory
  let fg = 0; d.facglow.forEach((s0) => { fg = Math.max(fg, 0.9 * Math.sin(Math.PI * P(s0, 1.2))); });
  B.$('facglow').style.opacity = fg.toFixed(3);
  let st = 0; d.fst.forEach((s) => { if (F >= s[0]) st = s[1]; });
  for (let k = 0; k < 4; k++) B.$('fst' + k).style.opacity = k === st ? 1 : 0;
  const fsn = B.$('fspin'), running = st !== 0;
  fsn.style.opacity = running ? 1 : 0; B.$('fdot').style.opacity = running ? 0 : 1;
  fsn.style.transform = 'rotate(' + ((F * 360) % 360).toFixed(1) + 'deg)';
  fsn.style.borderColor = st === 3 ? 'rgba(255,138,91,.25)' : 'rgba(47,149,255,.25)'; fsn.style.borderTopColor = st === 3 ? '#FF8A5B' : '#2F95FF';
  B.$('fsoft').style.opacity = lod.toFixed(3);
  // ---------------- connectors: base wires appear with what they connect; azure + flowing while an issue travels them
  Object.keys(d.wbase).forEach((k) => { B.$(k + 'b').setAttribute('opacity', P(d.wbase[k], 0.45).toFixed(3)); });
  Object.keys(d.wires).forEach((k) => { let a = 0; d.wires[k].forEach((iv) => { a = Math.max(a, P(iv[0], 0.25) * (1 - P(iv[1], 0.35))); });
    const e = B.$(k + 'a'); e.setAttribute('opacity', a.toFixed(3)); e.style.strokeDashoffset = (-F * 90).toFixed(1); });
  // ---------------- repo rows: highlight + labels (ready -> factory:running)
  Object.keys(d.rows).forEach((k) => { const [t0, t1] = d.rows[k];
    const r = P(t0, 0.3, 'back.out(2)'), xo = P(t1, 0.1), x = P(t1 + 0.08, 0.3, 'back.out(1.8)');
    const lr = B.$('lr_' + k), lx = B.$('lx_' + k);
    lr.style.opacity = (Math.min(1, r * 2) * (1 - xo)).toFixed(3); lr.style.transform = 'scale(' + B.lerp(0.5, 1, r).toFixed(4) + ')';
    lx.style.opacity = Math.min(1, x * 2).toFixed(3); lx.style.transform = 'scale(' + B.lerp(0.5, 1, x).toFixed(4) + ')';
    B.$('rh_' + k).style.opacity = (0.95 * Math.sin(Math.PI * P(t0 - 0.1, 1.4))).toFixed(3); });
  // ---------------- issue chips flying along bezier arcs
  d.chips.forEach((c) => {
    const el = B.$('ch_' + c.id), pp = B.$('chp_' + c.id);
    if (F < c.tOn || F > c.tDock + 0.3) { el.style.opacity = 0; if (pp) pp.style.opacity = 0; return; }
    let pos = c.segs[0].a;
    c.segs.forEach((s) => { if (F >= s.t0) { const p = P(s.t0, s.d, 'power3.inOut');
      const ctrl = [(s.a[0] + s.b[0]) / 2 + (s.ax || 0), (s.a[1] + s.b[1]) / 2 + s.arc]; pos = B.qb(s.a, ctrl, s.b, p); } });
    const appear = P(c.tOn, Math.min(0.5, c.segs[0].d * 0.55), 'power2.out');
    const dock = P(c.tDock - 0.12, 0.38, 'power2.in');
    const sc = B.lerp(c.big ? 0.3 : 0.45, 1, appear) * (1 - 0.65 * dock);
    const w = c.w, h = c.h;
    el.style.opacity = (Math.min(1, appear * 2.5) * (1 - dock)).toFixed(3);
    el.style.transform = 'translate(' + (pos[0] - w * sc / 2).toFixed(2) + 'px,' + (pos[1] - h * sc / 2).toFixed(2) + 'px) scale(' + sc.toFixed(4) + ')';
    if (c.big) {
      let lab = null; c.labels.forEach((l) => { if (F >= l[0]) lab = l[1]; });
      B.$('cr_' + c.id).style.opacity = lab === 'ready' ? 1 : 0; B.$('cx_' + c.id).style.opacity = lab === 'run' ? 1 : 0;
      if (c.wait) { const on = P(c.wait[0], 0.25);
        pp.style.transform = el.style.transform;
        pp.style.opacity = (on * (0.6 + 0.4 * Math.sin((F - c.wait[0]) * 9))).toFixed(3); }
    }
  });
  // ---------------- the cursor that labels the issue
  const cu = d.cur, ce = B.$('cursor');
  let cp = cu.pts[0];
  for (let k = 1; k < cu.pts.length; k++) { const a = cu.pts[k - 1], b = cu.pts[k];
    if (F >= a[0]) { const p = P(a[0], b[0] - a[0], 'power2.inOut'); cp = [0, B.lerp(a[1], b[1], p), B.lerp(a[2], b[2], p)]; } }
  const co = P(cu.tIn, 0.25) * (1 - P(cu.tOut, 0.3));
  const press = 1 - 0.16 * Math.sin(Math.PI * P(cu.click - 0.07, 0.2));
  ce.style.opacity = co.toFixed(3);
  ce.style.transform = 'translate(' + (cp[1] - 10).toFixed(1) + 'px,' + (cp[2] - 6).toFixed(1) + 'px) scale(' + press.toFixed(3) + ')';
};
"""


def mk(rid, cfg, fv=False):
    cfg.setdefault('accent', 'azure')
    page(rid, cfg, extra_css=CCSS + (FV_MASK if fv else ''), extra_js=CJS)


def sfx(*evs):
    return [dict(t=round(t, 3), type=k) for t, k in evs]


# ------------------------------------------------------------------------------------------------ world geometry
RW, RH, RY = 500, 370, 185                         # repo windows (two, side by side)
RX1, RX2 = 278, 802
FX, FW, FH, FY = 540, 1000, 250, 605               # factory (glass), y 480..730
PW, PH, PT = 1010, 792, 850                        # pool (glass, highlighted), y 850..1642
PX, PY = 540, PT + PH / 2
PL = PX - PW / 2                                   # pool left (35)
WW, WH, WG, GX0, GY0, COLS = 178, 150, 16, 28, 116, 5
FAC = (FX - FW / 2 + 516 + 230, FY - FH / 2 + 30 + 95)   # centre of the factory's dashed issue slot (786, 605)
TYPES = ['claude', 'codex', 'custom', 'claude', 'codex',
         'codex', 'custom', 'claude', 'codex', 'claude',
         'claude', 'claude', 'codex', 'custom', 'claude',
         'custom', 'codex', 'claude', 'codex', 'custom']
W_FIRST = 7                                        # the worker the factory claims in r5 (claude-3)

# camera views (world point at the anchor; split anchor 540,470 / fv anchor 540,720)
V0 = dict(x=540, y=320, s=1.0)                     # split, r0 frame 0: the factory at screen y 630-880 (cover-safe)
VPOOL = dict(x=540, y=PY - 24, s=1.0)              # split: the whole swarm, screen y 98-890
VFP = dict(x=540, y=PT + PH - 495, s=1.0)          # fv: factory (53-303) over the swarm (423-1215)
VRF = dict(x=540, y=600, s=1.0)                    # fv: repos (120-490) + factory (600-850) + the swarm's header and first row (to 1236)
V5 = dict(x=540, y=870, s=1.0)                     # split, r5 frame 0: factory (80-330) over the swarm's first rows


def run(ri):
    r, ws = words('s4', ri)
    return r, ws, (lambda w, n=1: r['T0'] + W(ws, w, n))


def world():
    r0, w0, A0 = run(0)
    r2, w2, A2 = run(2)
    r3, w3, A3 = run(3)
    r4, w4, A4 = run(4)
    r5, w5, A5 = run(5)
    r6, w6, A6 = run(6)
    T = {k: r['T0'] for k, r in ((0, r0), (2, r2), (3, r3), (4, r4), (5, r5), (6, r6))}

    workers, cnt = [], {}
    for i, ty in enumerate(TYPES):
        cnt[ty] = cnt.get(ty, 0) + 1
        rr, cc = divmod(i, COLS)
        lx, ly = GX0 + cc * (WW + WG), GY0 + rr * (WH + WG)
        workers.append(dict(i=i, ty=ty, name=f'{ty}-{cnt[ty]}', lx=lx, ly=ly, x=PL + lx + WW / 2, y=PT + ly + WH / 2))
    # pop-in ripple from the pool's centre on "agent swarm" (r0), dim on "in the background", flip on "mix" (r2)
    cx0, cy0 = PX, PT + GY0 + 2 * (WH + WG) - WG / 2
    order = sorted(range(20), key=lambda i: (workers[i]['x'] - cx0) ** 2 + (workers[i]['y'] - cy0) ** 2)
    rank = {i: k for k, i in enumerate(order)}
    t_pop = A0('swarm.') - 0.1
    for w in workers:
        k = rank[w['i']]
        w['tin'] = t_pop + 0.022 * k
        w['tdim'] = A2('background.') - 0.12 + 0.025 * w['i']
        w['tflip'] = A2('mix') - 0.24 + 0.024 * k
    names = {w['i']: w['name'] for w in workers}

    # issue A (#41 Day/night, cubefarm): labelled `ready` on "change", flies to the factory by "projects", the factory
    # claims claude-3 on "allocate" (label -> factory:running), the issue docks into it on "coding agents"
    rowA = (RX1 - RW / 2 + 250, 112 + 50)                   # cubefarm row #41 (chip start)
    rowB = (RX2 - RW / 2 + 250, 112 + 128 + 50)             # smolcoder row #19
    t_change, t_proj = A4('change'), A4('projects')
    tA_on, tA_fac = t_change + 0.42, t_proj + 0.26
    t_alloc, t_coding = A5('allocate'), A5('coding')
    tA_go = T[5] + 2.0
    wf = workers[W_FIRST]
    chips = [dict(id='A', num='#41', title='Day/night', big=True, tOn=tA_on, tDock=t_coding, w=430, h=150,
                  segs=[dict(t0=tA_on, d=tA_fac - tA_on, a=rowA, b=FAC, arc=40, ax=-150),
                        dict(t0=tA_go, d=t_coding - tA_go, a=FAC, b=(wf['x'], wf['y']), arc=30, ax=-60)],
                  labels=[(tA_on, 'ready'), (t_alloc, 'run')])]
    wf['claim'] = t_alloc; wf['busy'] = t_coding; wf['num'] = '#41'
    # r6: issues pour in from the repos (above the frame) and the factory hands one to every free worker; the pool is
    # full (20/20) on "busy"; the next issue (#19 Themes) waits in the factory (ember)
    t_busy = A6('busy')
    t_c0 = T[6] + 0.08
    rest = sorted([w for w in workers if w['i'] != W_FIRST], key=lambda w: (w['x'] - FAC[0]) ** 2 + (w['y'] - FAC[1]) ** 2)
    step = (t_busy - 0.02 - 0.55 - t_c0) / (len(rest) - 1)
    for k, w in enumerate(rest):
        t0 = t_c0 + step * k
        w['busy'] = t0 + 0.55; w['num'] = f'#{42 + k}'
        chips.append(dict(id=f'c{k}', num=w['num'], big=False, tOn=t0, tDock=t0 + 0.55, w=170, h=70,
                          segs=[dict(t0=t0, d=0.55, a=FAC, b=(w['x'], w['y']), arc=-40 - 25 * (k % 3))], labels=[]))
    feed = [(RX1 + 60, 300), (RX2 - 40, 162), (RX1 - 80, 290), (RX2 + 60, 290), (RX1 + 120, 162), (RX2 - 120, 300)]
    for k, (sx, sy) in enumerate(feed):
        t0 = T[6] - 0.45 + 0.17 * k
        chips.append(dict(id=f'f{k}', num=f'#{42 + k}', big=False, tOn=t0, tDock=t0 + 0.62,
                          w=170, h=70, segs=[dict(t0=t0, d=0.62, a=(sx, sy), b=FAC, arc=-50)], labels=[]))
    tB_on, tB_fac = T[6] + 0.75, t_busy - 0.06
    chips.append(dict(id='B', num='#19', title='Themes', big=True, tOn=tB_on, tDock=999, w=430, h=150,
                      segs=[dict(t0=tB_on, d=tB_fac - tB_on, a=rowB, b=FAC, arc=-60)],
                      labels=[(tB_on, 'ready')], wait=(t_busy, 999)))

    # the cursor that adds the `ready` label: in on "whenever", click on "change"
    t_when = A4('whenever')
    cur = dict(pts=[[t_when - 0.1, 610, 430], [t_change - 0.12, 236, 150], [t_change + 0.5, 236, 150], [t_change + 1.1, 330, 250]],
               tIn=t_when - 0.1, tOut=t_change + 0.55, click=t_change)

    ev = dict(OFF=0, workers=[dict(i=w['i'], ty=w['ty'], tin=w['tin'], tdim=w['tdim'], tflip=w['tflip'], busy=w.get('busy'),
                                   claim=w.get('claim')) for w in workers],
              hl=dict(codex=[A3('codex') - 0.05, A3('claude') - 0.15], claude=[A3('claude') - 0.05, A3('own') - 0.15],
                      custom=[A3('own') - 0.05, T[4] + 0.35]),
              chips=chips, cur=cur, t_count2=A4('waiting') - 0.1, sweeps=[A4('waiting') - 0.15],
              t_full=t_busy, facglow=[A0('factory') - 0.1, A4('factory') - 0.1],
              fst=[[0, 0], [tA_fac, 1], [t_alloc, 2], [t_coding, 1], [t_busy, 3]],
              wbase=dict(w1=0.2, w2=0.2, w3=2.1),
              rows=dict(a41=[t_change, t_alloc], b19=[tB_on - 0.3, 999]),
              wires=dict(w1=[[tA_on - 0.1, tA_fac + 0.2], [T[6] - 0.45, T[6] + 0.6]],
                         w2=[[T[6] - 0.45, T[6] + 0.6], [tB_on - 0.1, tB_fac + 0.2]],
                         w3=[[tA_go - 0.1, t_coding + 0.1], [t_c0 - 0.05, t_busy + 0.15]]))
    return dict(workers=workers, names=names, chips=chips, ev=ev, T=T, A=dict(A0=A0, A2=A2, A3=A3, A4=A4, A5=A5, A6=A6),
                runs={0: r0, 2: r2, 3: r3, 4: r4, 5: r5, 6: r6}, ws={0: w0, 2: w2, 3: w3, 4: w4, 5: w5, 6: w6})


# ------------------------------------------------------------------------------------------------ cards
def cards(Wd, land_repos=None, land_pool=None):
    workers, chips, names = Wd['workers'], Wd['chips'], Wd['names']

    def repo(cid, name, x, issues):
        rows = ''
        for k, (num, title, lid) in enumerate(issues):
            ty = 112 + 128 * k
            rows += ((f'<div id="rh_{lid}" class="abs" style="left:12px;right:12px;top:{ty - 14}px;height:120px;border-radius:16px;background:#E8F2FF;opacity:0"></div>' if lid else '')
                     + f'<div class="abs fx" style="left:30px;top:{ty}px;gap:14px">{OPEN_ISSUE.format(s=40)}'
                     f'<div style="font:600 44px/1 Figtree;letter-spacing:-.02em;color:{INK};white-space:nowrap">{num} <span style="font-weight:500;color:{INK2}">{title}</span></div></div>'
                     + (gh_label(f'lr_{lid}', 'ready', style=f'left:30px;top:{ty + 54}px') + gh_label(f'lx_{lid}', 'run', style=f'left:30px;top:{ty + 54}px') if lid else ''))
        h = (f'<div class="abs fx" style="left:30px;top:24px;gap:16px">{img("assets/c_github.png", 50, 50)}'
             f'<div style="font:600 46px/1 Figtree;letter-spacing:-.025em;color:{INK}">{name}</div></div>'
             f'<div class="abs" style="left:0;right:0;top:94px;height:2px;background:#ECEDF0"></div>{rows}')
        c = dict(id=cid, kind='window', x=x, y=RY, w=RW, h=RH, html=h)
        if land_repos is not None: c['land'] = dict(t=land_repos, dur=0.55)
        return c
    repo1 = repo('repo1', 'cubefarm', RX1, [('#41', 'Day/night', 'a41'), ('#42', 'Pet dog', None)])
    repo2 = repo('repo2', 'smolcoder', RX2, [('#18', '/export', None), ('#19', 'Themes', 'b19')])

    fst = ['idle', 'running', '→ ' + names[W_FIRST], 'waiting…']
    fac = dict(id='fac', kind='glass', x=FX, y=FY, w=FW, h=FH, html=(
        f'<div id="facglow" class="abs" style="inset:0;border-radius:32px;box-shadow:inset 0 0 0 2px {AZ},0 0 70px rgba(47,149,255,.6),inset 0 0 44px rgba(47,149,255,.22);opacity:0"></div>'
        f'<div class="abs fx" style="left:38px;top:30px;gap:20px">{img("assets/c_gh_actions.png", 72, 72)}'
        f'<div style="font:600 58px/1 Figtree;letter-spacing:-.025em">Factory</div></div>'
        f'<div id="fsoft" class="abs fx gm" style="left:40px;top:122px;gap:12px;font-size:30px;color:{TM}">{line_ico("lock", 30, TM, 2)}software-factory</div>'
        f'<div class="abs fx" style="left:40px;top:178px;gap:18px">'
        f'<div style="position:relative;width:38px;height:38px;flex:none"><div id="fdot" class="abs" style="inset:8px;border-radius:50%;background:#5A5D64"></div>'
        f'<div id="fspin" class="abs spin" style="inset:0;opacity:0"></div></div>'
        f'<div style="position:relative;height:50px;width:420px">'
        + ''.join(f'<div id="fst{k}" class="abs" style="left:0;top:0;font:600 44px/50px Figtree;letter-spacing:-.02em;color:{EM if k == 3 else ("#fff" if k else TS)};white-space:nowrap;opacity:{1 if k == 0 else 0}">{s}</div>'
                  for k, s in enumerate(fst))
        + '</div></div>'
        f'<div class="abs" style="left:516px;top:30px;width:460px;height:190px;border-radius:24px;border:2px dashed rgba(255,255,255,.16)"></div>'))

    wk = ''
    for w in workers:
        i = w['i']
        logo = {'claude': img('assets/c_claude.png', 76, 76),
                'codex': img('assets/c_codex.png', 76, 76, 'border-radius:19px'),
                'custom': tile_html('iris', 'bolt', 76, 0)}[w['ty']]
        robot = (f'<div style="width:76px;height:76px;border-radius:21px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);'
                 f'display:flex;align-items:center;justify-content:center">{line_ico("robot", 54, "#fff", 1.9)}</div>')
        ring = f'left:{w["lx"] - 6}px;top:{w["ly"] - 6}px;width:{WW + 12}px;height:{WH + 12}px'
        wk += (f'<div id="wslot{i}" class="abs" style="left:{w["lx"]}px;top:{w["ly"]}px;width:{WW}px;height:{WH}px;border-radius:22px;border:2px dashed rgba(255,255,255,.13)"></div>'
               f'<div id="wk{i}" class="wk" style="left:{w["lx"]}px;top:{w["ly"]}px;width:{WW}px;height:{WH}px;opacity:0">'
               f'<div id="wc{i}" class="abs" style="inset:0">'
               f'<div id="wfr{i}" class="abs" style="left:16px;top:13px">{robot}</div>'
               f'<div id="wbk{i}" class="abs" style="left:16px;top:13px;opacity:0">{logo}</div>'
               f'<div id="wp{i}" class="abs" style="right:14px;top:20px;opacity:0">{line_ico("pause", 38, "rgba(255,255,255,.6)", 2.6)}</div>'
               f'<div id="wna{i}" class="abs gm" style="left:20px;bottom:16px;font-size:30px;line-height:1;color:{TS};white-space:nowrap">agent-{i + 1}</div>'
               f'<div id="wnb{i}" class="abs gm" style="left:20px;bottom:16px;font-size:30px;line-height:1;color:{TS};white-space:nowrap;opacity:0">{w["name"]}</div></div>'
               f'<div id="ws{i}" class="abs spin" style="right:16px;top:20px;width:38px;height:38px;opacity:0"></div>'
               f'<div id="wi{i}" class="abs" style="left:20px;bottom:12px;font:600 46px/1 Figtree;letter-spacing:-.02em;color:#fff;opacity:0">{w.get("num", "")}</div>'
               f'</div>'
               f'<div id="wr{i}" class="ring" style="{ring};border:3px solid {AZ};box-shadow:0 0 26px rgba(47,149,255,.5),inset 0 0 18px rgba(47,149,255,.2);opacity:0"></div>'
               f'<div id="wf{i}" class="ring" style="{ring};border:4px solid {AZ};box-shadow:0 0 34px rgba(47,149,255,.75);opacity:0"></div>'
               f'<div id="wh{i}" class="ring" style="{ring};border:3px solid {AZ};box-shadow:0 0 30px rgba(47,149,255,.55),inset 0 0 22px rgba(47,149,255,.18);opacity:0"></div>')
    pool = dict(id='pool', kind='glass', highlight=True, x=PX, y=PY, w=PW, h=PH, html=(
        f'<div id="psweep" class="abs" style="left:0;top:100px;width:320px;bottom:0;background:linear-gradient(90deg,rgba(47,149,255,0),rgba(47,149,255,.2),rgba(47,149,255,0));opacity:0"></div>'
        f'<div id="pember" class="abs" style="inset:0;border-radius:32px;box-shadow:inset 0 0 0 2px {EM},inset 0 0 60px rgba(255,138,91,.22),0 0 90px rgba(255,138,91,.5);opacity:0"></div>'
        f'<div class="abs fx" style="left:40px;top:34px;gap:22px">{robot_tile(62, 0)}'
        f'<div style="font:600 52px/1 Figtree;letter-spacing:-.025em">Agent Swarm</div></div>'
        f'<div class="abs" style="right:40px;top:38px;height:56px;width:460px">'
        f'<div id="pc0" class="abs" style="right:0;top:0;font:600 46px/56px Figtree;letter-spacing:-.02em;white-space:nowrap;color:#fff">0 agents</div>'
        f'<div id="pc1" class="abs" style="right:0;top:0;font:600 46px/56px Figtree;letter-spacing:-.02em;white-space:nowrap;color:#fff;opacity:0">'
        f'<span id="pcn">0</span> / 20 busy</div></div>'
        + wk))
    if land_pool is not None: pool['land'] = dict(t=land_pool, dur=0.55)

    # connectors (world px; the card's top-left is world 0,0)
    wpaths = {'w1': f'M{RX1},{RH} C{RX1},{RH + 70} 650,{FY - FH / 2 - 60} 650,{FY - FH / 2}',
              'w2': f'M{RX2},{RH} C{RX2},{RH + 60} 900,{FY - FH / 2 - 50} 900,{FY - FH / 2}',
              'w3': f'M{FAC[0]},{FY + FH / 2} L{FAC[0]},{PT}'}
    wsvg = ('<svg width="1080" height="1700" style="position:absolute;left:0;top:0;overflow:visible">'
            + ''.join(f'<path id="{k}b" d="{p}" fill="none" stroke="#5A5D64" stroke-width="4" stroke-linecap="round" opacity="0"/>' for k, p in wpaths.items())
            + ''.join(f'<path id="{k}a" d="{p}" fill="none" stroke="{AZ}" stroke-width="5" stroke-linecap="round" stroke-dasharray="12 12" '
                      f'style="filter:drop-shadow(0 0 6px rgba(47,149,255,.9))" opacity="0"/>' for k, p in wpaths.items())
            + '</svg>')
    wires = dict(id='wires', kind='plain', clip=False, x=540, y=850, w=1080, h=1700, html=wsvg)

    # issue chips (white paper) + the cursor, on an overlay card covering the world (card px = world px)
    ch = ''
    for c in chips:
        if c['big']:
            inner = (f'<div class="abs fx" style="left:24px;top:22px;gap:12px">{OPEN_ISSUE.format(s=40)}'
                     f'<div style="font:600 46px/1 Figtree;letter-spacing:-.02em;color:{INK};white-space:nowrap">{c["num"]} '
                     f'<span style="font-weight:500;font-size:42px;color:{INK2}">{c["title"]}</span></div></div>'
                     + gh_label(f'cr_{c["id"]}', 'ready', 34, 'left:24px;top:84px') + gh_label(f'cx_{c["id"]}', 'run', 34, 'left:24px;top:84px'))
            ch += (f'<div id="ch_{c["id"]}" class="abs" style="left:0;top:0;width:{c["w"]}px;height:{c["h"]}px;border-radius:24px;{GLASS_PAPER}opacity:0;transform-origin:0 0">{inner}</div>'
                   f'<div id="chp_{c["id"]}" class="abs" style="left:0;top:0;width:{c["w"]}px;height:{c["h"]}px;border-radius:24px;box-shadow:0 0 0 5px {EM},0 0 44px rgba(255,138,91,.7);opacity:0;transform-origin:0 0"></div>')
        else:
            ch += (f'<div id="ch_{c["id"]}" class="abs fx" style="left:0;top:0;width:{c["w"]}px;height:{c["h"]}px;justify-content:center;gap:10px;border-radius:18px;{GLASS_PAPER}opacity:0;transform-origin:0 0">{OPEN_ISSUE.format(s=32)}'
                   f'<div style="font:600 44px/1 Figtree;letter-spacing:-.02em;color:{INK}">{c["num"]}</div></div>')
    ch += f'<div id="cursor" class="abs" style="left:0;top:0;opacity:0;transform-origin:10px 6px">{CURSOR}</div>'
    over = dict(id='over', kind='plain', clip=False, x=540, y=850, w=1080, h=1700, noDof=True, forceSharp=True, html=ch)
    return [wires, repo1, repo2, fac, pool, over]


# ------------------------------------------------------------------------------------------------ compositions
def comp(Wd, ri, mode, cam0, moves, heroes, sfx_ev, thumb=(), pushRef=1.0, land_repos=None, land_pool=None):
    r = Wd['runs'][ri]
    off = round(r['T0'], 4)
    cfg = dict(id=f's4_r{ri}', dur=r['dur'], mode=mode, cam0=cam0, pushRef=pushRef, heroes=heroes,
               cards=cards(Wd, land_repos, land_pool), moves=moves,
               wave=dict(level='low', k=1.0, t0=off),          # the wave is time-driven too: one continuous stage
               data=dict(Wd['ev'], OFF=off), sfx=sfx(*sfx_ev))
    if thumb: cfg['thumb'] = [list(x) for x in thumb]
    mk(cfg['id'], cfg, fv=(mode == 'fv'))


def build():
    Wd = world()
    ws = Wd['ws']

    # r0 split 3.83 s (cover-safe frame 0): the Factory alone under the cover title (y 630-880); the two app repos land
    # above it; it glows on "factory"; whip down to the Agent Swarm on "agent", the 20 workers pop into it on "swarm".
    w0 = ws[0]
    t_whip = W(w0, 'agent') - 0.5
    comp(Wd, 0, 'split', V0,
         moves=[dict(t=0.15, dur=t_whip - 0.2, kind='glide', to=dict(x=540, y=316, s=1.025)),
                dict(t=t_whip, kind='whip', to=VPOOL, via=dict(x=540, y=(V0['y'] + VPOOL['y']) / 2, s=0.82)),
                dict(t=t_whip + 1.08, dur=Wd['runs'][0]['dur'] - t_whip - 1.08, kind='glide', to=dict(VPOOL, s=1.01))],
         heroes=[dict(t=0, id='fac'), dict(t=t_whip + 0.45, id='pool')],
         sfx_ev=[(0.2, 'pop'), (t_whip + 0.45, 'whoosh'), (W(w0, 'swarm.') - 0.05, 'pop')],
         thumb=[(W(w0, 'swarm.') + 0.75, Wd['runs'][0]['dur'])],
         land_repos=0.2, land_pool=t_whip)

    # r2 fv 3.55 s: the factory over the swarm; the workers pause "in the background"; on "mix" the generic robots
    # flip into their real harness logos (Claude Code / Codex / your own harness).
    w2 = ws[2]
    comp(Wd, 2, 'fv', VFP,
         moves=[dict(t=0.1, dur=Wd['runs'][2]['dur'] - 0.1, kind='glide', to=dict(x=540, y=VFP['y'] + 14, s=1.02))],
         heroes=[dict(t=0, id='pool')], pushRef=1.02,
         sfx_ev=[(W(w2, 'mix') - 0.1, 'pop')])

    # r3 split 6.6 s: the swarm; the Codex workers light up on "Codex"; push in on the Claude Code workers on
    # "Claude Code"; pull back and your-own-harness workers light up on "own coding harness".
    w3 = ws[3]
    t_cl, t_maybe = W(w3, 'claude'), W(w3, 'maybe')
    push_to = dict(x=443, y=1330, s=1.45)
    comp(Wd, 3, 'split', VPOOL,
         moves=[dict(t=0.1, dur=t_cl - 0.45, kind='glide', to=dict(VPOOL, s=1.015)),
                dict(t=t_cl - 0.35, dur=1.15, kind='push', to=push_to),
                dict(t=t_cl + 0.85, dur=t_maybe - t_cl - 0.8, kind='glide', to=dict(x=447, y=1326, s=1.47)),
                dict(t=t_maybe + 0.05, dur=1.1, kind='pull', to=VPOOL),
                dict(t=t_maybe + 1.2, dur=Wd['runs'][3]['dur'] - t_maybe - 1.2, kind='glide', to=dict(VPOOL, s=1.012))],
         heroes=[dict(t=0, id='pool')],
         sfx_ev=[],
         thumb=[(t_cl + 0.85, t_maybe + 0.05)])

    # r4 fv 7.38 s: the swarm "waiting for work" (counter 0 / 20 busy, a slow azure sweep); on "software factory" the
    # camera rises to the repos above the factory; a cursor labels cubefarm #41 `ready` on "change"; the issue flies
    # into the factory by "projects" (the factory starts running).
    w4 = ws[4]
    t_sw = W(w4, 'software')
    comp(Wd, 4, 'fv', VFP,
         moves=[dict(t=0.1, dur=t_sw - 0.4, kind='glide', to=dict(x=540, y=VFP['y'] + 6, s=1.012)),
                dict(t=t_sw - 0.25, dur=1.35, kind='push', to=VRF),
                dict(t=t_sw + 1.15, dur=Wd['runs'][4]['dur'] - t_sw - 1.15, kind='glide', to=dict(VRF, y=VRF['y'] - 4, s=1.012))],
         heroes=[dict(t=0, id='none')], pushRef=1.05,
         sfx_ev=[(W(w4, 'change'), 'click'), (W(w4, 'projects') + 0.24, 'pop')])

    # r5 split 5.17 s: the factory holds #41 over the swarm; on "allocate" it claims claude-3 (azure flash, label ->
    # factory:running); the camera follows the issue down and it docks into the worker on "coding agents" (busy).
    w5 = ws[5]
    comp(Wd, 5, 'split', V5,
         moves=[dict(t=0.1, dur=2.05, kind='glide', to=dict(V5, s=1.012)),
                dict(t=2.2, dur=1.2, kind='push', to=VPOOL),
                dict(t=3.45, dur=Wd['runs'][5]['dur'] - 3.45, kind='glide', to=dict(VPOOL, s=1.012))],
         heroes=[dict(t=0, id='none')], pushRef=1.05,
         sfx_ev=[(W(w5, 'allocate'), 'click'), (W(w5, 'coding'), 'pop')],
         thumb=[(W(w5, 'coding') + 0.4, Wd['runs'][5]['dur'])])

    # r6 fv 2.17 s: issues pour through the factory into every free worker; 20 / 20 busy on "busy" (ember); the next
    # issue (#19) waits in the factory with an ember pulse.
    w6 = ws[6]
    comp(Wd, 6, 'fv', VFP,
         moves=[dict(t=0.1, dur=Wd['runs'][6]['dur'] - 0.1, kind='glide', to=dict(x=540, y=VFP['y'] + 10, s=1.015))],
         heroes=[dict(t=0, id='none')], pushRef=1.05,
         sfx_ev=[(0.62, 'pop')],
         thumb=[(W(w6, 'busy') + 0.18, Wd['runs'][6]['dur'])])
