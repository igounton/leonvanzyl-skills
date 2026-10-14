#!/bin/bash
# One-time setup of a work dir for one timeline.
#   bash <skill>/scripts/setup.sh <work_dir> <media_dir>
# - makes sure the render env exists (PRO_EDIT_VENV, default ~/.venvs/pro-edit: numpy/scipy/opencv/mediapipe/pyloudnorm,
#   nothing system-wide). Transcription uses the separate CrisperWhisper env (VEDIT_VENV) and is never touched here.
# - copies the scripts, the graphics engine, fonts and face models into the work dir, and writes project.json
# - media_dir is where finished renders go; Resolve links to them, so put it next to the project's source media
set -e
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
W="$1"; M="$2"
[ -n "$W" ] && [ -n "$M" ] || { echo "usage: setup.sh <work_dir> <media_dir>"; exit 1; }
command -v uv >/dev/null || { echo "ERROR: uv not found (https://docs.astral.sh/uv/)"; exit 1; }
command -v ffmpeg >/dev/null || { echo "ERROR: ffmpeg not found"; exit 1; }
command -v node >/dev/null || { echo "ERROR: node (22+) not found"; exit 1; }
VENV="${PRO_EDIT_VENV:-$HOME/.venvs/pro-edit}"
PY="$VENV/Scripts/python.exe"; [ -e "$PY" ] || PY="$VENV/bin/python"
if [ ! -e "$PY" ]; then mkdir -p "$(dirname "$VENV")"; uv venv "$VENV" --python 3.11; PY="$VENV/Scripts/python.exe"; [ -e "$PY" ] || PY="$VENV/bin/python"; fi
if ! "$PY" -c "import numpy, scipy, soundfile, pyloudnorm, cv2, PIL, mediapipe, onnxruntime" 2>/dev/null; then
  uv pip install --python "$PY" numpy scipy soundfile pyloudnorm opencv-python pillow mediapipe \
    onnxruntime-gpu nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"      # the split matte on the GPU (matte_gpu.py)
fi
# a CPU-only `onnxruntime` pulled in by another package shadows onnxruntime-gpu (same import name): the CUDA provider
# never shows up and the matte falls back to the CPU CLI. Remove it and reinstall the GPU build.
if ! "$PY" -c "import onnxruntime as o, sys; sys.exit(0 if 'CUDAExecutionProvider' in o.get_available_providers() else 1)" 2>/dev/null; then
  uv pip uninstall --python "$PY" onnxruntime >/dev/null 2>&1 || true
  uv pip install --python "$PY" --reinstall onnxruntime-gpu >/dev/null 2>&1 || true
  "$PY" -c "import onnxruntime as o; print('onnxruntime providers:', o.get_available_providers())"
fi
# Robust Video Matting for split beats (fine hair, stable over time, ignores a guitar/lamp touching the head):
# ~120 MB once per machine in a shared folder; compose.py --matte falls back to u2net when it is missing.
RVM_DIR="${PRO_EDIT_MODELS:-$HOME/.cache/pro-edit-models}/rvm"; mkdir -p "$RVM_DIR"
for f in rvm_resnet50_fp32.onnx rvm_mobilenetv3_fp32.onnx; do
  [ -s "$RVM_DIR/$f" ] || curl -fsSL -o "$RVM_DIR/$f" "https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/$f"     || { rm -f "$RVM_DIR/$f"; echo "WARNING: could not download $f - split mattes fall back to u2net"; }
done
# The royalty-free SFX library (highlight swishes, dings, whooshes, stings, real key strokes; Freesound CC0 + Mixkit
# licence, ~32 MB) lives in the skill: assets/sfx (PRO_EDIT_SFX_DIR moves it). Built in about a minute when a copy of
# the skill arrives without the audio (git keeps only its manifest). Without it audio.py uses synthesized sounds.
"$PY" "$SKILL/scripts/sfx_library.py" --check >/dev/null 2>&1 || "$PY" "$SKILL/scripts/sfx_library.py" build \
  || echo "WARNING: SFX library build failed - audio.py will use synthesized sounds"
# Optional: local AI music for the hook bed (music_gen.py) - ACE-Step 1.5 XL in its own env (MUSIC_GEN_VENV, default
# ~/.venvs/music-gen) with code + weights under MUSIC_GEN_HOME (default ~/.cache/pro-edit-models/ace-step-1.5).
# ~37 GB on first run (CUDA PyTorch env ~7 GB, weights ~30 GB). Skipped when installed; PRO_EDIT_MUSIC=0 skips it;
# a failure only prints a warning (music.py's synthesized beds still work).
install_music_gen() {
  local MH="${MUSIC_GEN_HOME:-$HOME/.cache/pro-edit-models/ace-step-1.5}" MV="${MUSIC_GEN_VENV:-$HOME/.venvs/music-gen}"
  local COMMIT=ca1e85fe9430179831e6bc6be790c332190a3866       # ACE-Step-1.5 main, 2026-08-29 (Windows: torch 2.7.1+cu128)
  local MARK="$MH/.installed-$COMMIT" MPY
  MPY="$MV/Scripts/python.exe"; [ -e "$MPY" ] || MPY="$MV/bin/python"
  if [ -e "$MARK" ] && "$MPY" -c "import acestep, librosa, pyloudnorm" 2>/dev/null; then
    echo "music gen: ready ($MV)"; return 0
  fi
  command -v git >/dev/null || { echo "git not found"; return 1; }
  echo "music gen: installing ACE-Step 1.5 (one-time, ~37 GB) ..."
  mkdir -p "$MH" "$(dirname "$MV")"
  [ -d "$MH/repo/.git" ] || git clone --quiet https://github.com/ace-step/ACE-Step-1.5.git "$MH/repo" || return 1
  git -C "$MH/repo" fetch --quiet origin 2>/dev/null; git -C "$MH/repo" checkout --quiet "$COMMIT" || return 1
  (cd "$MH/repo" && UV_PROJECT_ENVIRONMENT="$MV" uv sync --frozen --python 3.11) || return 1
  MPY="$MV/Scripts/python.exe"; [ -e "$MPY" ] || MPY="$MV/bin/python"
  uv pip install --python "$MPY" librosa pyloudnorm || return 1
  "$MPY" - "$MH/checkpoints" <<'PYEOF' || return 1
import sys
from huggingface_hub import snapshot_download as get
ck = sys.argv[1]
get('ACE-Step/Ace-Step1.5', revision='19671f406d603126926c1b7e2adc169acbcade22', local_dir=ck)   # VAE, text encoder, 2B turbo, LM 1.7B
get('ACE-Step/acestep-v15-xl-sft', revision='d06de46b4622f781cf07f4a013a67d591ca52819', local_dir=ck + '/acestep-v15-xl-sft')
# optional bigger planner (music_gen --lm 4B, +8.4 GB): ACE-Step/acestep-5Hz-lm-4B @ 0a3ec94b557aea7d508da38b31cfe7341f6ff737
from torchaudio.pipelines import HDEMUCS_HIGH_MUSDB_PLUS as B; B.get_model()    # vocal check in the analysis
PYEOF
  "$MPY" -c "import torch; c=torch.cuda.is_available(); print('music gen: torch', torch.__version__, torch.cuda.get_device_name(0) if c else 'NO CUDA GPU - generation will be very slow')" || return 1
  touch "$MARK"; echo "music gen: installed ($MV, weights in $MH/checkpoints)"
}
if [ "${PRO_EDIT_MUSIC:-1}" != "0" ]; then
  install_music_gen || echo "WARNING: music gen (ACE-Step) install failed - music_gen.py unavailable, synthesized music.py still works"
fi
mkdir -p "$W/scripts" "$W/gfx/assets" "$W/fonts" "$W/models" "$M"
cp "$SKILL"/scripts/*.py "$SKILL"/scripts/*.sh "$W/scripts/"
cp "$SKILL"/assets/gfx/* "$W/gfx/"
cp "$SKILL"/assets/fonts/*.ttf "$W/fonts/"; cp "$SKILL"/assets/fonts/*.ttf "$W/gfx/assets/"
cp "$SKILL"/assets/models/* "$W/models/"
M_ABS="$(cd "$M" && (pwd -W 2>/dev/null || pwd))"
SKILL_ABS="$(cd "$SKILL" && (pwd -W 2>/dev/null || pwd))"
(cd "$W" && "$PY" - "$M_ABS" "$SKILL_ABS" <<'PYEOF'
import json, os, sys
p = 'project.json'
c = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
c['media_dir'] = sys.argv[1].replace('\\', '/')
c['skill_dir'] = sys.argv[2].replace('\\', '/')     # sfxlib finds the skill's assets/sfx through it
json.dump(c, open(p, 'w', encoding='utf-8'), indent=1)
PYEOF
)
echo "setup done: work dir $W | media dir $M_ABS | render python $PY"
