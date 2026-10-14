# Prints the numbers a short's report.md needs: lines with source ranges, runs, SFX events (absolute time + level),
# riser, music, final file facts and loudness, the picked thumbnail. usage: python scripts/report_data.py s3
import json, subprocess, sys, re
sk = sys.argv[1]
C = json.load(open('cut.json', encoding='utf-8'))[sk]; S = json.load(open('shorts.json', encoding='utf-8'))[sk]
print(f'# {sk}: {S["title"]}  cover={S.get("cover")}  cta={S.get("cta_keyword")}')
print('\n## lines (source s)')
for L in S['lines']:
    ps = [p for p in C['pieces'] if p['line'] == L['id']]
    print(f"{L['id']} | {min(p['src0'] for p in ps):.2f}-{max(p['src1'] for p in ps):.2f} | pieces={len(ps)} | {L['layout']}"
          f"{' sw=' + str([(s['t'], s['layout']) for s in L.get('switches', [])]) if L.get('switches') else ''} | {L['text']}")
print('\n## runs')
for r in C['runs']:
    print(f"{r['i']} | {r['layout']} | {r['T0']:.3f}-{r['T1']:.3f} | {r['dur']:.2f} | {r.get('text', '')[:90]}")
END = C['runs'][-1]['T1']
print(f'END={END:.3f}')
import os
M = json.load(open(f'{sk}/music.json', encoding='utf-8')) if os.path.exists(f'{sk}/music.json') else {}
if os.path.exists(f'{sk}/sfx_log.json'):                       # written by audio.py: what actually plays, and how loud
    print('\n## sfx (absolute s, sound, level vs voice peak, source)')
    for e in json.load(open(f'{sk}/sfx_log.json', encoding='utf-8')):
        print(f"{e['t']:.3f} | {e['type']} | {e['sound']} | {e['level_db']} dB | {e.get('src')}")
    print(f"library: {M.get('sfx_library') or 'none (synthesized sounds)'}")
else:
    ev = json.load(open('gfx/sfx_events.json', encoding='utf-8'))
    print('\n## sfx (absolute s) - run audio.py for the sounds and levels')
    for r in C['runs']:
        for e in ev.get(f'{sk}_r{r["i"]}', []):
            print(f"{r['T0'] + e['t']:.3f} | {e['type']} | run {r['i']}")
print(f"\n## riser: {M.get('riser', 'synth_riser')}, loudest moment on the hook join {C['runs'][0]['T1']:.3f} s, -12 dB vs voice peak")
alts = M.pop('alternatives', None) or []
print('## music', json.dumps({k: v for k, v in M.items() if k not in ('sfx_library',)}))
for a in alts: print(f"   alternative take {a['take']}: score {a['score']} ({a['why']}) {a['file']}")
geo = f'{sk}/cam/split_geom.json'
try:
    g = json.load(open(geo, encoding='utf-8')); print('## split geom', {k: v for k, v in g.items() if k not in ('src',)})
except Exception as e: print('no split geom', e)
p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,profile,width,height,r_frame_rate,nb_frames,sample_rate,channels:format=duration',
                    '-of', 'compact', f'{sk}/final_video.mp4'], capture_output=True, text=True).stdout
print('\n## file\n' + p.strip())
r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', f'{sk}/final_video.mp4', '-map', '0:a', '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                   capture_output=True, text=True).stderr
summ = r[r.rfind('Summary:'):]
I = re.search(r'I:\s+(-?[\d.]+) LUFS', summ); TP = re.search(r'Peak:\s+(-?[\d.]+) dBFS', summ)
print(f"## loudness integrated {I.group(1) if I else '?'} LUFS, true peak {TP.group(1) if TP else '?'} dBFS")
try:
    th = json.load(open(f'{sk}/thumbnail.json', encoding='utf-8'))
    print(f"## thumbnail {th['t']} s (run {th['run']}, {th['layout']}), q{th['quality']} {th['bytes'] / 1e6:.2f} MB; candidates: "
          + ', '.join(f"{c['t']} s r{c['run']} sharp {c['sharpness']} {c['mouth']}".rstrip() for c in th.get('candidates', [])))
except Exception as e: print('no thumbnail picked yet', e)
