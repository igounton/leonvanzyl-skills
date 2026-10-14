"""Stop before rendering if any on-screen text of a short is garbled (mojibake) or empty.
Windows' cp1252 default once turned "Bölük" into "BÃ¶lÃ¼k" in a caption chip; nothing else caught it (the voice proof
can't see captions). Checks the plan (cover, highlights, line text), the cut's words, the captions and the CTA events.
usage: python scripts/check_text.py s1 [s2 ...]        (finish.sh runs it first; exit 1 = fix the text, then re-run)
Repair stored text in place with s.encode('cp1252').decode('utf-8') rather than re-aligning (word edges stay put)."""
import json, os, re, sys

# UTF-8 read as cp1252: a lead byte shown as Â/Ã/Ä/Å followed by a continuation byte's cp1252 glyph, or "â€" (quotes,
# dashes). "SÃO" (a real Ã before a letter) is not flagged.
CONT = ('\x80-\xbf€‚ƒ„…†‡ˆ‰Š‹ŒŽ'
        '‘’“”•–—˜™š›œžŸ')
BAD = re.compile(f'[Â-Å][{CONT}]|â€|�')


def strings(x, path=''):
    if isinstance(x, str): yield path, x
    elif isinstance(x, dict):
        for k, v in x.items(): yield from strings(v, f'{path}.{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from strings(v, f'{path}[{i}]')


def load(p):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


bad = 0
for sk in sys.argv[1:]:
    srcs = {'shorts.json': (load('shorts.json') or {}).get(sk), 'cut.json words': ((load('cut.json') or {}).get(sk) or {}).get('words'),
            f'{sk}/captions.json': load(f'{sk}/captions.json'), f'{sk}/events_extra.json': load(f'{sk}/events_extra.json')}
    for name, d in srcs.items():
        if d is None: continue
        for path, s in strings(d):
            if BAD.search(s):
                bad += 1; print(f'{sk}: garbled text in {name}{path}: {ascii(s[:80])}  (should it be {ascii(s.encode("cp1252", "ignore").decode("utf-8", "ignore"))}?)')
    caps = srcs[f'{sk}/captions.json']
    items = caps if isinstance(caps, list) else (caps or {}).get('chunks', [])
    for c in items or []:
        if isinstance(c, dict) and 'text' in c and not str(c['text']).strip():
            bad += 1; print(f'{sk}: empty caption chunk at {c.get("t0")}')
    if not bad: print(f'{sk}: on-screen text OK')
sys.exit(1 if bad else 0)
