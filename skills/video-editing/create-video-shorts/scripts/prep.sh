#!/bin/bash
# Main-agent work after the cut, in one call, while the graphics subagents build their compositions:
#   frame-exact camera clips for every camera run (all runs in parallel, NVDEC)
#   -> the matte for every split run of every short in ONE GPU call (RVM; u2net if the model is missing)
#   -> captions.json + events_extra.json per short (so audio.py can run)
#   -> one full-resolution frame of the cover and of every split run (if its graphic is already rendered) -> chk/<sk>_splits.png
#   bash scripts/prep.sh s1 [s2 ...]
export PYTHONUTF8=1   # Python reads/writes UTF-8 on Windows too (cp1252 garbled non-ASCII names in captions)
set -u
cd "$(dirname "$0")/.."
PY=../.venv/Scripts/python.exe; [ -f "$PY" ] || PY=../.venv/bin/python
mkdir -p logs chk
SKS="$*"; [ -n "$SKS" ] || SKS=$("$PY" -c "import json; print(' '.join(json.load(open('shorts.json'))))")
t0=$(date +%s)
since() { echo "[$(( $(date +%s) - t0 ))s] $*"; }
"$PY" scripts/cam_prep.py $SKS 2>&1 | tee logs/cam_prep.log | grep -E "run|camera runs"
SPLITS=$("$PY" - $SKS <<'EOF'
import json, sys
out = []
for sk in sys.argv[1:]:
    p = json.load(open(f'{sk}/cam/plan.json'))
    runs = sorted(int(i) for i, e in p.items() if e['layout'] == 'split')
    if runs: out.append(sk + ':' + ','.join(map(str, runs)))
print(' '.join(out))
EOF
)
if [ -n "$SPLITS" ]; then
  since "matting split runs: $SPLITS"
  # Robust Video Matting first (hair strands, no guitar/lamp grabbed with the head); u2net (matte_gpu.py) as the fallback
  if "$PY" -c "import sys; sys.path.insert(0, 'scripts'); import matte_rvm; sys.exit(0 if matte_rvm.available() else 1)" 2>/dev/null; then
    "$PY" scripts/matte_rvm.py $SPLITS --jobs 4 2>&1 | tee logs/matte.log | grep -E "matte on|frames|all |Error|error"
  else
    echo "RVM model or CUDA missing (setup.sh downloads the model): falling back to u2net"
    "$PY" scripts/matte_gpu.py $SPLITS --jobs 4 2>&1 | tee logs/matte.log | grep -E "matte on|frames|all "
  fi
fi
for sk in $SKS; do "$PY" scripts/compose.py $sk --events-only 2>&1 | tail -1; done
# one full-resolution frame per split run (needs that run's graphic) + the cover frame
for sk in $SKS; do
  SPEC=$("$PY" - $sk <<'EOF'
import json, os, sys
sk = sys.argv[1]; C = json.load(open('cut.json'))[sk]
runs = [r for r in C['runs'] if r['layout'] == 'split' and os.path.exists(f'gfx/out60/{sk}_r{r["i"]}.mp4')]
if runs: print(','.join(str(r['i']) for r in runs), ' ', ','.join(f'{(r["T0"] + r["T1"]) / 2:.3f}' for r in runs) + ('' if runs[0]['i'] else ',0'))
EOF
)
  if [ -n "$SPEC" ]; then
    set -- $SPEC
    since "$sk: full-resolution frames of split runs $1"
    if "$PY" scripts/compose.py $sk --runs $1 --preview $2 > logs/preview_$sk.log 2>&1; then
      "$PY" scripts/sheet.py "$sk/preview/*.png" chk/${sk}_splits.png 4; grep "split geometry" logs/preview_$sk.log
    else
      echo "$sk: split check FAILED:"; grep -vE "Warning|warn|^\s" logs/preview_$sk.log | tail -3
    fi
  else
    since "$sk: no split graphic rendered yet; run the split check later: compose.py $sk --runs <i> --preview <t>"
  fi
done
since "prep done. LOOK at chk/<sk>_splits.png: whole face (hair to chin) inside the card, hair ~95 px above its edge"
