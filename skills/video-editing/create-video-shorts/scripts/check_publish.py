"""Check edit/PUBLISH.md against the publishing rules (editing-spec 8b) before handing it over.
usage: $PY scripts/check_publish.py [../edit/PUBLISH.md]      exit 1 on a broken rule; warnings don't fail
Errors: YouTube title over 54 characters, emoji or # in it, or a duplicate; the two community lines missing or changed;
not exactly three hashtags (or filler tags) on the description's last line; a TikTok hook of 100+ or an Instagram hook of
125+ characters; no "Watch the full video" CTA line; URLs in the TikTok / Instagram captions; 3-5 hashtags broken
(Instagram max 5); a missing thumbnail file. Warnings: no power word in the title, a long description or TikTok caption."""
import os, re, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else '../edit/PUBLISH.md'
SKOOL = ['🎁 Get the resources from this video + my free AI builder course: https://skool.com/leonvanzyl',
         '🚀 Go deeper inside Agentic Labs: AI coding courses, live Q&A, weekly challenges, and direct access to me: https://skool.com/agentic-labs']
POWER = ('secret', 'hidden', 'truth', 'finally', 'never', 'stop', 'instantly', 'free', 'proven', 'insane', 'brutal', 'mistake',
         'beats', 'killer', 'dead', 'exposed', 'shocking', 'surprised', 'nobody', 'wrong', 'worst', 'best', 'only', 'crazy')
FILLER = {'#shorts', '#short', '#viral', '#fyp', '#foryou', '#foryoupage', '#trending'}
TAG = re.compile(r'^#[A-Za-z0-9]+$')
EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿]')

text = open(PATH, encoding='utf-8').read()
base = os.path.dirname(os.path.abspath(PATH))
errs, warns, titles = [], [], {}


def tags(line, lo, hi, where):
    t = line.split()
    if not lo <= len(t) <= hi: errs.append(f'{where}: {len(t)} hashtags on the last line (want {lo}-{hi})')
    for x in t:
        if not TAG.match(x): errs.append(f'{where}: "{x}" is not a CamelCase hashtag')
        if x.lower() in FILLER: errs.append(f'{where}: filler hashtag {x}')


def block_after(sec, marker, start=0):
    i = sec.find(marker, start)
    if i < 0: return None, -1
    m = re.search(r'```\n(.*?)\n```', sec[i:], re.S)
    return (m.group(1), i + m.end()) if m else (None, -1)


for sec in re.split(r'\n(?=## Short )', text)[1:]:
    name = sec.splitlines()[0][3:].split('  ')[0]
    m = re.search(r'!\[[^\]]*\]\(([^)]+)\)', sec)
    if not m or not os.path.exists(os.path.join(base, m.group(1))): errs.append(f'{name}: thumbnail file missing ({m.group(1) if m else "no image"})')
    yt = sec.find('### YouTube Shorts'); tt = sec.find('### TikTok'); ig = sec.find('### Instagram Reels')
    if min(yt, tt, ig) < 0: errs.append(f'{name}: needs the YouTube Shorts, TikTok and Instagram Reels subsections'); continue
    title, _ = block_after(sec, '**Title**', yt)
    desc, _ = block_after(sec, '**Description**', yt)
    ttc, _ = block_after(sec, '**Caption**', tt)
    igc, _ = block_after(sec, '**Caption**', ig)
    if title is None or desc is None or ttc is None or igc is None: errs.append(f'{name}: a copy block is missing'); continue
    title = title.strip()
    if len(title) > 54: errs.append(f'{name}: YouTube title is {len(title)} characters (54 at most): {title}')
    if '#' in title or EMOJI.search(title): errs.append(f'{name}: no emoji or hashtags in the title')
    if not any(re.search(rf'\b{p}\b', title, re.I) for p in POWER): warns.append(f'{name}: no power word in the title: {title}')
    if title.lower() in titles: errs.append(f'{name}: same title as {titles[title.lower()]}')
    titles[title.lower()] = name
    paras = desc.split('\n\n')
    if len(paras[0]) > 220: warns.append(f'{name}: description opener is {len(paras[0])} characters (about 200 at most)')
    for s in SKOOL:
        if s not in desc: errs.append(f'{name}: description is missing the exact line "{s[:40]}..."')
    tags(desc.strip().splitlines()[-1], 3, 3, f'{name} YouTube')
    if '**Related video:**' not in sec[yt:tt]: errs.append(f'{name}: no Related video line')
    for cap, where, hook_max, hi in ((ttc, 'TikTok', 100, 5), (igc, 'Instagram', 125, 5)):
        lines = cap.strip().splitlines()
        if len(lines[0]) >= hook_max: errs.append(f'{name} {where}: hook is {len(lines[0])} characters (under {hook_max})')
        if '🎬 Watch the full video' not in cap: errs.append(f'{name} {where}: no "🎬 Watch the full video ..." CTA line')
        if re.search(r'https?://|www\.', cap): errs.append(f'{name} {where}: URLs are not clickable in captions; remove them')
        tags(lines[-1], 3, hi, f'{name} {where}')
    if len(ttc) > 420: warns.append(f'{name} TikTok: caption is {len(ttc)} characters (about 300 is the target)')
    print(f'{name}: title {len(title)}, TikTok hook {len(ttc.splitlines()[0])}, Instagram hook {len(igc.splitlines()[0])}')

for w in warns: print('warning:', w)
for e in errs: print('ERROR:', e)
print('PUBLISH.md OK' if not errs else f'{len(errs)} error(s)')
sys.exit(1 if errs else 0)
