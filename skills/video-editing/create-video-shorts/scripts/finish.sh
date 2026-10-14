#!/bin/bash
# Final assembly of one short in one call: the music take (music_takes.py --ensure), audio (SFX, riser, music, stems, mix) and every compose segment in parallel,
# then the stream-copy concat, verify_final, and delivery into ../edit/short-NN_<slug>/. Alongside the concat it renders the
# thumbnail candidates the graphics marked (gfx/thumbs.json; clean frames, one seek each) -> chk/<sk>_thumbs.png.
#   bash scripts/finish.sh s1 [NN slug]        e.g. bash scripts/finish.sh s1 01 half-the-price-of-opus
# Segments are cached by their inputs: after an edit only the runs that changed are re-rendered (seconds to a minute).
# Run it only after every render_full.sh has printed "done" for this short's graphics (a segment composited while its
# graphic is still being written would be short; the frame-count check catches that and fails).
export PYTHONUTF8=1   # Python reads/writes UTF-8 on Windows too (cp1252 garbled non-ASCII names in captions)
set -u
cd "$(dirname "$0")/.."
PY=../.venv/Scripts/python.exe; [ -f "$PY" ] || PY=../.venv/bin/python
sk=$1; NN=${2:-}; SLUG=${3:-}
mkdir -p logs chk
t0=$(date +%s)
since() { echo "[$(( $(date +%s) - t0 ))s] $*"; }
# garbled on-screen text (mojibake) stops everything before a frame is rendered
"$PY" scripts/check_text.py $sk || { echo "fix the text above (check_text.py docstring), then re-run finish.sh"; exit 1; }
# the music takes (music_takes.py, usually started in the background after cut.sh): wait for a running job, or generate
# now; with no GPU / music env the pick is missing and audio.py uses the synthesized bed
( "$PY" scripts/music_takes.py $sk --ensure > logs/music_$sk.log 2>&1; "$PY" scripts/audio.py $sk > logs/audio_$sk.log 2>&1 ) &
AU=$!
"$PY" scripts/compose.py $sk --segments --no-concat 2>&1 | tee logs/segments_$sk.log | grep -E "segment|FAILED|MISMATCH|missing|geometry"
SEG=${PIPESTATUS[0]}
wait $AU || { echo "audio failed:"; tail -20 logs/audio_$sk.log; exit 1; }
grep -E "music take|no usable take" logs/music_$sk.log; grep -E "^music|mix_lufs" logs/audio_$sk.log
[ "$SEG" -eq 0 ] || { echo "segments failed (see logs/segments_$sk.log)"; exit 1; }
"$PY" scripts/thumbnail.py $sk > logs/thumbs_$sk.log 2>&1 &
TH=$!
"$PY" scripts/compose.py $sk --concat
"$PY" scripts/verify_final.py $sk/final_video.mp4 chk/${sk}_final.png 2>&1 | grep -vE "^\s*$" | tail -6
wait $TH && grep -E " s  run " logs/thumbs_$sk.log || { echo "thumbnail candidates: none rendered:"; tail -3 logs/thumbs_$sk.log; }
if [ -n "$NN" ] && [ -n "$SLUG" ]; then
  D=../edit/short-${NN}_${SLUG}; mkdir -p "$D/stems"
  cp $sk/final_video.mp4 "$D/final.mp4"; cp $sk/stems/*.wav "$D/stems/"
  # every music take as an MP3, so the user can pick another by ear (music_takes.py <sk> --pick <k>, then finish.sh)
  # a given track (shorts.json music.file, e.g. the long-form hook track after a rejected take) is delivered and marked instead
  MF=$("$PY" -c "import json; m=json.load(open('$sk/music.json')); print(m['file'] if m.get('source')=='file' else '')" 2>/dev/null)
  if ls $sk/music/take_*.wav >/dev/null 2>&1 || [ -n "$MF" ]; then
    mkdir -p "$D/music_takes"; rm -f "$D/music_takes/"*.mp3
    USED=$("$PY" -c "import json; print(json.load(open('$sk/music/pick.json'))['take'])" 2>/dev/null); [ -n "$MF" ] && USED=none
    for f in $sk/music/take_*.wav; do [ -f "$f" ] || continue; k=$(basename "$f" .wav); k=${k#take_}
      ffmpeg -v error -y -i "$f" -c:a libmp3lame -b:a 256k "$D/music_takes/take_$k$([ "$k" = "$USED" ] && echo ' (in the short)').mp3"; done
    [ -n "$MF" ] && ffmpeg -v error -y -i "$MF" -c:a libmp3lame -b:a 256k "$D/music_takes/$(basename "${MF%.*}") (in the short).mp3"
  fi
  since "delivered $D/final.mp4 + stems/ (pick the thumbnail: thumbnail.py $sk --pick <t> $NN $SLUG; write report.md there and the PUBLISH.md section)"
fi
since "$sk finished. LOOK at chk/${sk}_final.png and chk/${sk}_thumbs.png"
