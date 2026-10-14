"""The "Compositions" section of GFX_BRIEF.md, straight from the cut: every run that needs a graphic (split / fv) with its
layout, duration and words at run-relative start times, the cover-safe note on each r0, and the full-cam runs between
them as context. Paste it under "## Compositions", then add one "Idea:" line per composition (what it shows, the real
source, what lands on which word). Re-run after any cut change: the times move.
usage: $PY scripts/brief_runs.py [s1 s2 ...]        (all shorts in shorts.json if none given)"""
import json, sys

S = json.load(open('shorts.json', encoding='utf-8')); C = json.load(open('cut.json', encoding='utf-8'))
LAY = {'split': 'split', 'fv': 'fv', 'fc': 'full cam'}
for sk in sys.argv[1:] or [k for k in S if k in C]:
    s, c = S[sk], C[sk]
    cover = ' / '.join(s.get('cover', []))
    print(f'\n### Short {sk} "{s.get("title", "")}"' + (f' (cover "{cover}")' if cover else ''))
    for r in c['runs']:
        ws = [w for w in c['words'] if r['T0'] - 0.02 <= w['s'] < r['T1'] - 0.02]
        words = ' '.join(f"{w['w']}@{max(w['s'] - r['T0'], 0):.2f}" for w in ws)
        if r['layout'] == 'fc':
            print(f"  (run {r['i']} full cam {r['dur']:.2f} s: \"{r.get('text', '')}\")")
            continue
        note = ' - cover-safe frame 0 (keep everything below y 620 at t 0)' if r['i'] == 0 else ''
        print(f"- `{sk}_r{r['i']}` {LAY[r['layout']]} {r['dur']:.2f} s{note}: {words}")
        print('  Idea: <what it shows, the real source / footage, what lands on which word>')
