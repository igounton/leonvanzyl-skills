#!/bin/bash
# One-time setup for a folder of recordings.
#   bash <skill>/scripts/setup.sh <project_folder>
#   bash <skill>/scripts/setup.sh <video_file>     one video in a folder that also holds other videos (e.g. the finished edit
#                                                   next to its raw recordings): works in <its folder>/shorts/ with a hard link
#                                                   to that video only (a copy if the link fails), so nothing else is processed
# - creates <project>/.venv (local, nothing system-wide; model weights come from the user caches)
# - once per machine: the RVM matting model (~/.cache/pro-edit-models/rvm), the SFX library check, and the music
#   generator (ACE-Step 1.5 XL in ~/.venvs/music-gen; ~37 GB the first time; PRO_EDIT_MUSIC=0 skips it)
# - for every video in the folder root creates <project>/work-<stem>/ with the scripts, the graphics engine,
#   fonts, the face model and a project.json (init_project.py)
export PYTHONUTF8=1   # Python reads/writes UTF-8 on Windows too (cp1252 garbled non-ASCII names in captions)
set -e
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
ARG="${1:-.}"
if [ -f "$ARG" ]; then
  SRC="$(cd "$(dirname "$ARG")" && pwd)/$(basename "$ARG")"
  mkdir -p "$(dirname "$SRC")/shorts"
  [ -e "$(dirname "$SRC")/shorts/$(basename "$SRC")" ] || ln "$SRC" "$(dirname "$SRC")/shorts/" 2>/dev/null || cp "$SRC" "$(dirname "$SRC")/shorts/"
  ARG="$(dirname "$SRC")/shorts"
  echo "single video: working in $ARG (hard link to $(basename "$SRC"))"
fi
PROJ="$(cd "$ARG" && pwd)"
command -v uv >/dev/null || { echo "ERROR: uv not found (https://docs.astral.sh/uv/)"; exit 1; }
command -v ffmpeg >/dev/null || { echo "ERROR: ffmpeg not found"; exit 1; }
command -v node >/dev/null || { echo "ERROR: node (22+) not found"; exit 1; }
SKILL_ABS="$(cd "$SKILL" && (pwd -W 2>/dev/null || pwd))"
cd "$PROJ"
[ -d .venv ] || uv venv .venv --python 3.11
PY=.venv/Scripts/python.exe; [ -f "$PY" ] || PY=.venv/bin/python
if ! "$PY" -c "import faster_whisper, torchaudio, mediapipe, cv2, pyloudnorm, num2words" 2>/dev/null; then
  uv pip install --python "$PY" numpy scipy soundfile pyloudnorm faster-whisper opencv-python pillow mediapipe num2words \
    nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*" onnxruntime-gpu &
  # CUDA PyTorch on NVIDIA machines: wav2vec2 forced alignment runs ~13x faster on the GPU (word edges identical to CPU).
  # cu130 wheels need an NVIDIA driver >= 580; any failure falls back to the CPU build.
  if command -v nvidia-smi >/dev/null 2>&1; then
    ( uv pip install --python "$PY" torch torchaudio --index-url https://download.pytorch.org/whl/cu130       || uv pip install --python "$PY" torch torchaudio --index-url https://download.pytorch.org/whl/cpu ) &
  else
    uv pip install --python "$PY" torch torchaudio --index-url https://download.pytorch.org/whl/cpu &
  fi
  wait
fi
# an existing venv with CPU-only torch on an NVIDIA machine: swap in the CUDA build (same API, identical results)
if command -v nvidia-smi >/dev/null 2>&1 && ! "$PY" -c "import torch, sys; sys.exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
  uv pip install --python "$PY" --reinstall-package torch --reinstall-package torchaudio torch torchaudio     --index-url https://download.pytorch.org/whl/cu130 >/dev/null 2>&1 || true
  "$PY" -c "import torch; print('torch', torch.__version__, 'cuda:', torch.cuda.is_available())"
fi
# a CPU-only `onnxruntime` pulled in by another package shadows onnxruntime-gpu (same import name), so the CUDA provider
# never shows up. Remove it and reinstall the GPU build; matte_gpu.py then runs the matting model on CUDA (~12x faster).
if ! "$PY" -c "import onnxruntime as o, sys; sys.exit(0 if 'CUDAExecutionProvider' in o.get_available_providers() else 1)" 2>/dev/null; then
  uv pip uninstall --python "$PY" onnxruntime >/dev/null 2>&1 || true
  uv pip install --python "$PY" --reinstall onnxruntime-gpu >/dev/null 2>&1 || true
  "$PY" -c "import onnxruntime as o; print('onnxruntime providers:', o.get_available_providers())"
fi
# Robust Video Matting for the split's head pop-out (hair strands, steady, ignores a guitar/lamp touching the head):
# ~120 MB once per machine in a folder shared with davinci-resolve-pro-edit; prep.sh falls back to u2net without it.
RVM_DIR="${PRO_EDIT_MODELS:-$HOME/.cache/pro-edit-models}/rvm"; mkdir -p "$RVM_DIR"
for f in rvm_resnet50_fp32.onnx rvm_mobilenetv3_fp32.onnx; do
  [ -s "$RVM_DIR/$f" ] || curl -fsSL -o "$RVM_DIR/$f" "https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/$f"     || { rm -f "$RVM_DIR/$f"; echo "WARNING: could not download $f - split mattes fall back to u2net"; }
done
# The royalty-free SFX library lives in the skill (assets/sfx: CC0 sounds in git, Mixkit ones downloaded by
# sfx_library.py build, about a minute). Without it audio.py uses its synthesized sounds.
"$PY" "$SKILL/scripts/sfx_library.py" --check >/dev/null 2>&1 || "$PY" "$SKILL/scripts/sfx_library.py" build   || echo "WARNING: SFX library build failed - audio.py will use synthesized sounds"
# Local AI music for every short (music_gen.py, music_takes.py) - ACE-Step 1.5 XL in its own env (MUSIC_GEN_VENV, default
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
shopt -s nullglob nocaseglob
n=0
for V in *.mov *.mp4 *.mkv *.m4v *.mxf; do
  STEM="${V%.*}"; W="work-$STEM"
  mkdir -p "$W/scripts" "$W/gfx/assets" "$W/fonts"
  cp "$SKILL"/scripts/*.py "$SKILL"/scripts/*.sh "$W/scripts/"
  cp "$SKILL"/assets/gfx/* "$W/gfx/"
  cp "$SKILL"/assets/fonts/*.ttf "$W/fonts/"; cp "$SKILL"/assets/fonts/*.ttf "$W/gfx/assets/"
  cp "$SKILL"/assets/models/* "$W/"
  (cd "$W" && "../$PY" scripts/init_project.py "../$V" && "../$PY" -c "import json; p='project.json'; c=json.load(open(p)); c['skill_dir']=r'$SKILL_ABS'; json.dump(c, open(p,'w'), indent=1)")
  # OPTIONAL piggyback: a long-form edit of this video made with davinci-resolve-pro-edit on this machine brings its
  # raw-footage map, captures, logos and voice stem (pipeline.md 1c). None found = standalone shorts, as always.
  (cd "$W" && "../$PY" scripts/import_longform.py --auto) || true
  n=$((n+1))
done
[ $n -gt 0 ] || { echo "ERROR: no video found in $PROJ"; exit 1; }
mkdir -p edit
echo "setup done: .venv + $n work folder(s)"
