"""print programme word start times in a window: python scripts/words.py t0 t1"""
import json, sys
P = json.load(open('program.json', encoding='utf-8'))
t0, t1 = float(sys.argv[1]), float(sys.argv[2])
print(' '.join(f"{w['w']}@{w['s']:.2f}" for w in P['words'] if t0 <= w['s'] < t1 and not w.get('tag')))
