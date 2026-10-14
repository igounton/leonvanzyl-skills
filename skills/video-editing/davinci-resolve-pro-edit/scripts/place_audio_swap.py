"""Swap a rebuilt audio layer (audio.py --tag <t>) into an already-built timeline, on NEW tracks.

A rebuild moves sounds (new events, other library picks, different lengths), so media_pool_item replace_clip is not
enough. Instead: put the new layer on fresh tracks, then switch the old PE SFX / Music / Riser tracks off.
1) python scripts/place_audio_swap.py plan --audio-tracks <N> --tag v2
     N = the timeline's current audio track count (probe it). Writes audio_swap_plan.json: the tracks to add
     ("PE SFX v2", "PE SFX 2 v2", "PE SFX 3 v2" when SFX overlap, "PE Music v2", "PE Riser v2"; stereo), the files to
     import and every clip with its track and record frame.
2) after media_pool safe_import_media of plan.import_files (save the result as import_audio_<tag>.json):
   python scripts/place_audio_swap.py ids import_audio_<tag>.json
     -> append_audio_swap.json: rows for ONE media_pool append_to_timeline {clip_infos: <this>} call.
        200+ rows are fine; the reply is too big for the tool output and lands in a file - parse it (count, null ids).
3) timeline set_track_enable false + set_track_name "<name> (old)" on the old PE audio tracks, SaveProject.
Wrap 1-3 in one timeline_versioning begin_run/end_run. Record frames are relative to the timeline start, ends exclusive."""
import sys, os, json

SFX_LANES = ('sfx', 'sfx2', 'sfx3')
NAMES = dict(sfx='PE SFX', sfx2='PE SFX 2', sfx3='PE SFX 3', music='PE Music', riser='PE Riser')


def plan(na, tag):
    A = json.load(open('audio_clips.json'))
    ends = {l: 0 for l in SFX_LANES}; rows = []
    for c in sorted(A['clips'], key=lambda c: c['record_frame']):
        role = c['track']
        if role == 'sfx':                          # greedy: the first lane where it does not overlap
            role = next((l for l in SFX_LANES if c['record_frame'] >= ends[l]), None)
            if role is None: print(f"  dropping an SFX at frame {c['record_frame']} ({c.get('src')}): all lanes busy"); continue
            ends[role] = c['record_frame'] + c['end_frame'] - c['start_frame']
        rows.append(dict(role=role, file=c['file'], record_frame=c['record_frame'], start_frame=c['start_frame'], end_frame=c['end_frame']))
    used = [r for r in ('sfx', 'sfx2', 'sfx3', 'music', 'riser') if any(x['role'] == r for x in rows)]
    idx = {r: na + 1 + k for k, r in enumerate(used)}
    out = dict(tag=tag, tracks=[dict(index=idx[r], name=f'{NAMES[r]} {tag}'.strip(), audio_type='stereo') for r in used],
               import_files=sorted({r['file'] for r in rows}), rows=[dict(r, track_index=idx[r['role']]) for r in rows])
    json.dump(out, open('audio_swap_plan.json', 'w'), indent=1)
    print(f"audio_swap_plan.json: {len(rows)} clips on {[(t['index'], t['name']) for t in out['tracks']]}, "
          f"{len(out['import_files'])} files to import")


def ids(result_path):
    R = json.load(open(result_path, encoding='utf-8')); R = R.get('result', R)
    by = {}
    for c in R.get('clips', []):
        by[os.path.normcase(os.path.abspath(c.get('file_path') or ''))] = c['id']
        by[os.path.basename(c.get('file_path') or c.get('name', '')).lower()] = c['id']
    P = json.load(open('audio_swap_plan.json'))
    rows, lost = [], []
    for r in P['rows']:
        mid = by.get(os.path.normcase(os.path.abspath(r['file']))) or by.get(os.path.basename(r['file']).lower())
        if not mid: lost.append(r['file']); continue
        rows.append(dict(media_pool_item_id=mid, start_frame=r['start_frame'], end_frame=r['end_frame'],
                         record_frame=r['record_frame'], track_index=r['track_index'], media_type=2))
    json.dump(rows, open('append_audio_swap.json', 'w'), indent=1)
    print(f'append_audio_swap.json: {len(rows)} rows', '| NOT IMPORTED:', lost if lost else 'none')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'plan':
        plan(int(a[a.index('--audio-tracks') + 1]), a[a.index('--tag') + 1] if '--tag' in a else '')
    else:
        ids(a[1])
