"""Zoom framings (cam + marks) for every zoom beat -> zoom_specs.json (merged into edit_plan.json by make_plan.py).
Cue times are written as ABSOLUTE programme seconds (from words.py) and converted to beat-relative here.
Rects / fx / fy are SOURCE px (3840x2160). Every view is checked against the held-still PiP (top-right
[3108,18,704,948] or bottom-left [18,1194,704,948] for items 40-63) so the inpainted source PiP stays hidden."""
import json

FPS = 60
snap = lambda t: round(round(t * FPS) / FPS, 4)
plan_t0 = {}            # filled from make_plan's beats (t0 per id) - written here to keep this file standalone
T0 = dict(z01=0.0, z02=27.15, z03=55.35, z04=59.62, z05=70.57, z06=82.87, z07=107.1, z08=183.37, z09=197.53,
          z10=208.43, z11=226.5, z12=256.0, z13=268.8, z13b=276.2, z14=313.32, z15=337.17, z16=371.47,
          z18=396.92, z19=425.22, z21=471.22, z22=526.35, z23=545.0, z24=551.87, z25=557.68, z26=572.6,
          z27=686.17, z28=712.32, z29=726.62, z30=739.13, z31=780.73, z32=803.07, z33=831.58, z34=908.9, z35=925.6)
TR, BL = 'TR', 'BL'
PIP = {k: TR for k in T0}
for k in ('z13b', 'z14', 'z15', 'z16', 'z18', 'z19'): PIP[k] = BL

S = {}
def cam(t, fx, fy, k, dur=0.9, absolute=True, **kw):
    return dict(t=t, dur=dur, fx=fx, fy=fy, k=k, **kw)
def mark(t, typ, rect, t_out=None):
    m = dict(t=t, type=typ, rect=rect)
    if t_out is not None: m['t_out'] = t_out
    return m
def Z(bid, cams=(), marks=()):
    t0 = snap(T0[bid])
    S[bid] = dict(cam=[dict(c, t=round(c['t'] - t0, 3)) for c in cams],
                  marks=[dict(m, t=round(m['t'] - t0, 3), **({'t_out': round(m['t_out'] - t0, 3)} if 't_out' in m else {})) for m in marks])

# ---------------- hook
Z('z01', [cam(0.30, 2250, 1100, 1.4), cam(2.60, 2250, 1080, 1.45, dur=2.8, ease='sine.inOut')],
         [mark(2.85, 'band', [2060, 868, 330, 56])])
Z('z02', [cam(27.40, 1422, 1250, 1.35), cam(37.2, 1500, 1200, 1.38, dur=2.6, ease='sine.inOut')],
         [mark(32.40, 'band', [200, 1548, 1240, 88], 35.0), mark(32.75, 'band', [200, 1648, 900, 88], 35.0)])
# ---------------- Agentic Labs
Z('z03', [cam(55.80, 1500, 1100, 1.3)])
Z('z04', [cam(60.92, 1500, 1060, 1.5)],
         [mark(61.20, 'box', [360, 768, 930, 140], 63.4), mark(63.30, 'band', [1460, 512, 1220, 80])])
Z('z05', [cam(70.87, 1910, 1300, 1.5)],
         [mark(72.01, 'box', [1360, 905, 920, 80], 73.6), mark(73.81, 'band', [1365, 1372, 1100, 62])])
# ---------------- the code panel on the title slide (TR)
Z('z06', [cam(87.72, 2250, 1050, 1.45)],
         [mark(90.63, 'box', [2080, 645, 150, 70], 91.9), mark(91.99, 'box', [2290, 645, 145, 70], 94.7),
          mark(95.54, 'box', [2505, 645, 205, 70])])
Z('z07', [cam(107.40, 2250, 1100, 1.5)],
         [mark(109.26, 'box', [2040, 860, 1450, 590], 115.0), mark(115.26, 'band', [2115, 942, 560, 58])])
Z('z08', [cam(183.57, 2250, 1150, 1.5, dur=0.8)], [mark(185.19, 'band', [2115, 1306, 680, 56])])
Z('z09', [cam(197.83, 2220, 1100, 1.35, dur=1.0)], [mark(200.27, 'box', [2040, 860, 1450, 590])])
# ---------------- his slides (TR)
Z('z10', [cam(209.43, 1324, 1150, 1.45), cam(213.15, 1920, 1080, 1.0, dur=0.7, ease='power3.inOut')],
         [mark(209.91, 'band', [195, 555, 2060, 200], 212.6),
          mark(213.90, 'box', [195, 1060, 670, 570], 214.9), mark(214.98, 'box', [935, 1060, 670, 570], 215.45),
          mark(215.49, 'box', [1675, 1060, 670, 570], 216.3), mark(216.38, 'box', [2415, 1060, 670, 570], 218.7)])
Z('z11', [cam(232.0, 1630, 1080, 1.25, dur=1.0), cam(236.9, 1200, 1300, 1.6, dur=0.6, ease='power3.inOut')],
         [mark(232.32, 'band', [195, 555, 2880, 195], 236.8), mark(238.22, 'box', [195, 1065, 910, 560])])
Z('z12', [cam(256.4, 1200, 1300, 1.7)],
         [mark(257.11, 'band', [285, 1340, 640, 70], 264.4), mark(264.99, 'band', [280, 1412, 270, 60])])
# ---------------- Claude app: AGENTS.md (item 39 TR, then BL)
Z('z13', [cam(271.8, 1900, 1300, 1.5, dur=0.8)], [mark(274.15, 'box', [1620, 1270, 380, 80], 276.1)])
Z('z13b', [cam(276.8, 2516, 1100, 1.45)],
          [mark(277.82, 'band', [1940, 530, 1260, 110], 287.0), mark(288.37, 'band', [1950, 1370, 1700, 150])])
Z('z14', [cam(313.7, 1560, 1050, 1.45, dur=1.0)], [mark(328.0, 'box', [985, 630, 820, 900], 337.1)])
Z('z15', [cam(337.5, 2200, 1080, 1.35)],
         [mark(343.63, 'box', [985, 630, 820, 1450], 346.0), mark(349.8, 'band', [1940, 530, 1420, 240])])
Z('z16', [cam(371.9, 2500, 980, 1.45)],
         [mark(373.69, 'box', [1460, 1100, 880, 80], 380.5), mark(376.17, 'band', [2440, 575, 800, 200], 383.0),
          mark(385.40, 'band', [2520, 830, 1220, 170])])
# ---------------- VS Code hooks demo (BL)
Z('z18', [cam(397.3, 2300, 900, 1.4), cam(412.1, 1650, 900, 1.3, dur=0.6, ease='power3.inOut'),
          cam(424.2, 1920, 1080, 1.0, dur=0.9)],
         [mark(405.74, 'band', [1460, 805, 2000, 200], 412.0), mark(409.68, 'box', [1430, 200, 680, 90], 412.0),
          mark(412.81, 'box', [290, 700, 960, 470], 419.0), mark(420.89, 'box', [300, 700, 500, 70], 424.1)])
Z('z19', [cam(425.6, 2300, 1000, 1.45), cam(439.48, 2500, 1050, 1.6, dur=0.6, ease='power3.inOut')],
         [mark(426.72, 'box', [1690, 525, 420, 70], 439.3), mark(439.73, 'box', [1770, 610, 350, 72], 444.5),
          mark(444.78, 'band', [2060, 1060, 1500, 60]), mark(446.0, 'band', [2060, 1236, 1420, 60])])
# ---------------- Level 2 slides + sources (TR)
Z('z21', [cam(471.5, 1371, 1300, 1.4)],
         [mark(473.5, 'box', [195, 1065, 910, 560], 474.8), mark(474.9, 'box', [1185, 1065, 910, 560])])
Z('z22', [cam(526.65, 1324, 1050, 1.45)], [mark(528.77, 'band', [195, 630, 1790, 105])])
Z('z23', [cam(545.2, 2190, 1200, 1.3)],
         [mark(546.0, 'band', [1025, 548, 2080, 64], 548.2), mark(546.25, 'band', [1025, 632, 2075, 64], 548.2),
          mark(548.32, 'spot', [1160, 1690, 2460, 110])])
Z('z24', [cam(552.17, 1200, 1300, 1.6)], [mark(553.65, 'box', [290, 1350, 1140, 200])])
Z('z25', [cam(558.1, 1700, 1250, 1.45), cam(567.6, 1920, 1080, 1.0, dur=0.85)],
         [mark(563.6, 'band', [940, 1355, 1520, 230], 567.6)])
Z('z26', [cam(572.9, 2280, 1300, 1.6)],
         [mark(573.56, 'box', [1760, 1580, 1010, 90], 575.2), mark(575.40, 'box', [1770, 1350, 1020, 200])])
Z('z27', [cam(686.47, 1200, 1100, 1.6), cam(703.67, 1920, 1080, 1.0, dur=0.9)],
         [mark(692.33, 'box', [70, 1036, 1790, 110], 703.6)])
Z('z28', [cam(712.72, 2200, 1100, 1.8), cam(721.27, 1920, 1080, 1.0, dur=0.85)],
         [mark(719.79, 'box', [2595, 985, 270, 48], 721.2)])
Z('z29', [cam(726.92, 1600, 1180, 1.6)],
         [mark(730.39, 'box', [1280, 985, 560, 52], 733.6), mark(733.14, 'band', [1280, 1150, 1240, 290])])
Z('z30', [cam(739.43, 1640, 1300, 1.5)], [mark(742.07, 'box', [1185, 1065, 910, 560])])
Z('z31', [cam(784.1, 2194, 1300, 1.3)], [mark(786.3, 'box', [2175, 1065, 910, 560])])
Z('z32', [cam(803.37, 1422, 1150, 1.35)],
         [mark(808.0, 'spot', [620, 400, 960, 1600], 810.3), mark(810.45, 'band', [620, 400, 260, 64]),
          mark(814.61, 'box', [628, 730, 945, 405])])
Z('z33', [cam(831.88, 1371, 1100, 1.4)], [mark(834.54, 'box', [190, 610, 540, 90])])
# ---------------- cubefarm: highlights only (moving 3D view; the panel sits at the top of the frame)
Z('z34', [], [mark(910.2, 'box', [680, 100, 260, 50], 912.3), mark(912.45, 'box', [2270, 248, 500, 50], 913.3)])
Z('z35', [], [mark(927.2, 'box', [1010, 530, 560, 240], 931.0), mark(933.45, 'band', [100, 470, 2780, 220])])


def safe(bid, c):
    k, fx, fy = c['k'], c['fx'], c['fy']
    hw, hh = 1920 / k, 1080 / k
    fx = min(max(fx, hw), 3840 - hw); fy = min(max(fy, hh), 2160 - hh)
    if k <= 1.0001: return True, fx, fy
    if PIP[bid] == TR: ok = fx <= 3108 - 1188 / k + 1 and fy >= 966 + 114 / k - 1
    else: ok = fx >= 722 + 1198 / k - 1 and fy <= 1194 - 114 / k + 1
    return ok, fx, fy

bad = 0
for bid, s in S.items():
    for c in s['cam']:
        ok, fx, fy = safe(bid, c)
        if not ok: bad += 1; print('UNSAFE', bid, c, '-> clamped centre', round(fx), round(fy))
json.dump(S, open('zoom_specs.json', 'w'), indent=1)
print(len(S), 'zoom specs written', '' if not bad else f'({bad} unsafe)')
