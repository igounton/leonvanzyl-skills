# Setup and troubleshooting

## Environments
Two Python environments, on purpose: transcription needs CUDA PyTorch and the CrisperWhisper model, rendering needs
OpenCV and MediaPipe. Installing one into the other risks breaking both.

**CrisperWhisper (transcription)** - shared with davinci-resolve-video-edit. `~/.venvs/crisperwhisper` or
`VEDIT_VENV`; interpreter `Scripts/python.exe` (Windows) or `bin/python`. Check:
```bash
"$CW" -c "import torch, crisperwhisper; from huggingface_hub import try_to_load_from_cache as c; print('cuda:', torch.cuda.is_available(), '| model cached:', isinstance(c('nyralabs/CrisperWhisper2.0_large', 'config.json'), str))"
```
If it's missing, ask the user first (about 7 GB with CUDA PyTorch and the model), then:
```bash
VENV="${VEDIT_VENV:-$HOME/.venvs/crisperwhisper}"; mkdir -p "$(dirname "$VENV")"; uv venv "$VENV" --python 3.13
CW="$VENV/Scripts/python.exe"; [ -e "$CW" ] || CW="$VENV/bin/python"
uv pip install -p "$CW" torch torchaudio --index-url https://download.pytorch.org/whl/cu128   # no NVIDIA GPU: drop the index URL
uv pip install -p "$CW" "crisperwhisper[transformers]"
HF_HUB_OFFLINE=0 "$CW" -c "from huggingface_hub import snapshot_download; snapshot_download('nyralabs/CrisperWhisper2.0_large')"
```
The CrisperWhisper 2.0 weights are under the nyra health Non-Commercial Research License (the code is MIT). Tell the
user once before downloading; a monetised video may count as commercial use. If the model is already cached, that
decision was made - don't raise it again. `vedit.py` runs offline against the cache.

**Render env** - `~/.venvs/pro-edit` or `PRO_EDIT_VENV`, Python 3.11 (MediaPipe wheels), created by `setup.sh`
with uv: numpy, scipy, soundfile, pyloudnorm, opencv-python, pillow, mediapipe, plus onnxruntime-gpu with the CUDA
12 runtime wheels (nvidia-cublas-cu12, nvidia-cudnn-cu12) for the split matte on the GPU. An existing env gets
the extra packages the next time `setup.sh` runs. If `onnxruntime.get_available_providers()` lacks
`CUDAExecutionProvider`, a CPU-only `onnxruntime` wheel pulled in by another package is shadowing the GPU build;
`setup.sh` uninstalls it and reinstalls onnxruntime-gpu.

**Also needed:** ffmpeg on PATH (with `h264_nvenc` when there is an NVIDIA GPU - `media.has_nvenc()` tests it;
`PRO_EDIT_X264=1` forces software), Node 22+ for `npx --yes hyperframes` (the first run downloads the CLI; built
and tested with 0.8.96), uv.

## Work and media folders
- `W` (work dir) holds caches, intermediates, drafts and previews. Default under `%LOCALAPPDATA%\video-pro-edit`
  (Windows) or `~/.cache/video-pro-edit`; `PRO_EDIT_WORK_ROOT` moves it. Keep the path short (deep paths break uv).
- `M` (media dir) holds everything Resolve links to. Put it next to the recording's source files. Never under
  AppData: a packaged app (like the Claude desktop app) can virtualise writes there, so the files exist for the
  scripts but not for Resolve.

## Sound-effects library (real SFX, in the skill)
Curated recordings and designed SFX, so the edit doesn't fall back on bland synthesized ones.
- **Where:** the skill's own `assets/sfx/<category>/<name>.wav` + `manifest.json` (`PRO_EDIT_SFX_DIR` moves it).
  `_originals/` keeps the untouched downloads, which are data only. About 32 MB. `sfxlib.root()` finds it from the
  skill, from a work dir (project.json `skill_dir`, written by setup.sh) or the usual install paths.
- **Git:** the 27 CC0 sounds (and their originals) are committed with the skill; `assets/sfx/.gitignore` keeps the 27
  Mixkit sounds out, because Mixkit's licence forbids redistributing the files themselves. A fresh clone therefore has
  27 of the 54 WAVs, and `--check` lists the rest as missing.
- **If sounds are missing on a machine** (a fresh clone, a new PC, a deleted file): from the skill folder, with the
  render env python,
  ```bash
  ~/.venvs/pro-edit/Scripts/python.exe scripts/sfx_library.py --check    # what is missing
  ~/.venvs/pro-edit/Scripts/python.exe scripts/sfx_library.py build      # download + process, about 1 minute
  ```
  `build` downloads each missing original from its source - Mixkit's CDN for the Mixkit sounds, Freesound for CC0 -
  into `assets/sfx/_originals/<source.original>` (the direct link is `source.download_url` in `manifest.json`), then
  processes it into `assets/sfx/<category>/<name>.wav`. Processing is deterministic: a rebuild from a fresh clone
  (tested 2026-10-14) reproduced all 54 files bit-identical. `setup.sh` runs this automatically when `--check` fails.
  If a download fails (a site moved a file): open the sound's `source.page_url`, download it by hand, save it as
  `assets/sfx/_originals/<source.original>` and run `build` again - it only downloads originals that aren't there.
  Without the library at all, `audio.py` falls back to synthesized sounds (it prints which library it loaded).
- **What:** 54 files: highlight 5 (marker strokes, paper swish, shimmer), ding 5, chime 4, pop 4, click 5, typing 6
  (3 single keys, 3 runs of 1.6-2 s), whoosh 6 (light to deep), swoosh_in 2, swoosh_out 2, sting 6 (4 hits, 2 reveal
  shimmers), riser 5, glitch 2, notification 2. All 48 kHz stereo 24-bit, trimmed so the onset sits at 5 ms, with
  5 ms / 20-50 ms fades and the peak at -1 dBFS (the pipeline sets the levels).
- **Manifest, per file:** `duration`, `peak_time` (centre of the loudest 10 ms), `lufs`, `align` (`onset`: sync t=0.005
  to the event; `peak`: put `peak_time` on the cut or join, which is the case for whooshes, swoosh-ins and risers),
  `pick` (the 1-2 recommended per category), `description`, `segment` (the cut taken from the original), and `source`
  (site, id, page URL, direct download URL, author, licence name and URL, sha256 of the original).
- **Rebuild / verify** (render env python): `scripts/sfx_library.py build` downloads anything missing and re-processes
  everything (about 1 min); `--check` exits 1 when the library is incomplete; `list [category]` shows it; `build --force`
  re-downloads; `build --from-manifest <json>` rebuilds from another manifest's URLs. In code:
  `import sfx_library as SFX; SFX.picks('whoosh')`, `SFX.path('ding', 'bell_attention')`.
- **Licences (monetised use is fine, no attribution needed):** 27 files are under the **Mixkit Sound Effects Free
  License** (https://mixkit.co/license/#sfxFree). It allows commercial use, YouTube included, without credit. You may
  not redistribute the files on their own, claim them as yours, or register them with Content ID or another
  rights-management service. 27 are Freesound sounds marked **CC0**
  (http://creativecommons.org/publicdomain/zero/1.0/), each licence checked on its page. These are the HQ previews
  (Ogg, about 192 kbps), because the originals need a login. Sounds with lossy (mp3) or derivative originals were left
  out. Pixabay blocks automated downloads (403) and the Sonniss GDC bundles are multi-GB archives, so neither is used.
  BBC Sound Effects are non-commercial, so they are excluded.
- **Adding a sound:** add a row to `SOURCES` in `sfx_library.py` (CC0 or Mixkit only, check the licence on its page),
  then run `build`.

## Troubleshooting
| Symptom | Fix |
|---|---|
| `vedit prepare`: TypeError on `source_start` | The timeline has titles/generators/transitions on V1: this skill's `vedit.py` skips them (the stock one crashes). Make sure the work dir has this skill's copy. |
| `prepare` warns "record length != source length" / "slipped audio" next to a clip | A transition the editor added: its handle is counted in the video source range. Expected; `program.py` maps it; keep beats off the transition. |
| `source_map` / "the beat overlaps V1 item ... title/generator/transition" | Move the beat's t0/t1 off the transition (look at `transcript.txt` around it). |
| `scenes.py`: a PiP window taller than the screen | The edge scan ran off; the consensus window from the other files is used when the face is inside it (printed). If every file fails, set `files.<path>.pip` in `scenes.json` by hand from a `look.py` frame. |
| Renders crawl at ~4 fps on Windows | Something bypassed `media.reader_proc/writer_proc` (64 MB pipes). Windows' default 4 KB pipe caps raw 4K video at ~60 MB/s. |
| A colour shift at the cut into a zoom or graphic | Footage went through ffmpeg's default RGB conversion (bt601). Zooms must use `decode(..., yuv=True)`; RGB paths must use `media.dec_vf()` / `enc_args()`. |
| `matte_gpu.py` says "CPU fallback" | onnxruntime-gpu is missing or shadowed (see Render env), or `~/.cache/hyperframes/background-removal/models/u2net_human_seg.onnx` isn't cached yet (one CLI run caches it). The fallback is the HyperFrames CLI on the CPU (~2-3 fps); the GPU path does a 300-frame beat in seconds. |
| A full render seems stuck at ~15 fps capture, or 100 Chromes appear | `render_gfx.sh` exports `PRODUCER_ENABLE_BROWSER_POOL=false` and throttles with `RENDER_SLOTS` x `HF_WORKERS`; a bare `npx hyperframes render` from a subagent does neither. Always go through the script. |
| The split's pop-out shows a bit of the background next to the hair | The salient-object matte grabbed an object touching the hair (a guitar headstock on the test). Pick another beat for the split, or shift the hair line (`HAIR_Y` in `compose.py`); a person-segmentation model would fix it but isn't bundled. |
| HyperFrames render fails | Read `gfx/out_hi/<id>.log` or `gfx/draft/<id>.log`; the hyperframes-cli skill covers `lint`, `validate` and `doctor`. |
| Resolve drops an appended clip | Two clips overlapped on one track (Resolve keeps the earlier). `place.py plan` lists overlaps as PROBLEMs - fix the plan. |
| A marker doesn't appear | Its frame already had a marker. Use `place.py ids --existing-markers`. |
| An edited render doesn't show in Resolve | Resolve holds the old file open; render with `--tag v2` and `media_pool_item replace_clip`. |
| `timeline_frame capture` changed the render target | Expected - it renders one frame through Deliver. Tell the user to re-check the Deliver page before their final render. |

## Music generation (optional): ACE-Step 1.5 XL
`scripts/music_gen.py` makes a real instrumental bed (hook music) locally instead of the synthesized `music.py` one.
Model: **ACE-Step 1.5 XL** (StepFun + ACE Studio): the `acestep-v15-xl-sft` 4B diffusion transformer (50 steps, CFG)
planned by the `acestep-5Hz-lm-1.7B` language model, 48 kHz stereo. Picked in Oct 2026 as the best open-weight model
that is MIT-licensed, ungated, scriptable headless, and has explicit instrumental, BPM, key and duration control.

**Licence (monetised videos):** MIT on the code and on every `ACE-Step/*` weights repo (HF licence tag + model card).
The model card says it was trained on licensed, royalty-free/public-domain and synthetic (MIDI-rendered) audio and that
"generated music can be used for commercial purposes". There is no indemnity, and the weights repos have no LICENSE
file of their own (the MIT tag and model card are the grant; an open HF discussion asks them to add one). We don't use
ACE-Step's captioner/transcriber models (based on Qwen2.5-Omni, with a separate licence question).
Other models were ruled out on licence or fit:
- MusicGen/MAGNeT weights are CC-BY-NC, so no monetised use.
- Stable Audio 3 Medium is under the Stability Community Licence (fine under $1M revenue), but its HF repo needs a login
  click-through.
- MiniMax Music 3 requires showing "MiniMax-Music3" on commercial products and an AI-content disclosure (AUP).
- DiffRhythm 2, HeartMuLa, YuE and SongBloom are Apache-2.0 but are song-with-vocals models.
- Tencent SongGeneration/LeVo forbids commercial use.

**What is installed, where.** setup.sh installs all of it, once. `PRO_EDIT_MUSIC=0` skips it; a failure only warns.
- Code: `~/.cache/pro-edit-models/ace-step-1.5/repo`, github.com/ace-step/ACE-Step-1.5 pinned at `ca1e85f`
  (`MUSIC_GEN_HOME` moves the folder).
- Weights: `~/.cache/pro-edit-models/ace-step-1.5/checkpoints`, about 30 GB, pinned to HF revisions in setup.sh:
  - `ACE-Step/Ace-Step1.5` (10 GB): VAE, Qwen3-Embedding-0.6B text encoder, 2B turbo DiT, LM 1.7B
  - `ACE-Step/acestep-v15-xl-sft` (20 GB)
  - optional: `ACE-Step/acestep-5Hz-lm-4B` (8.4 GB) for `--lm 4B`
- Env: `~/.venvs/music-gen` (`MUSIC_GEN_VENV`), Python 3.11 built from the repo's `uv.lock`: torch 2.7.1+cu128 (includes
  sm_120, so RTX 50xx/Blackwell works), flash-attn 2.8.2, triton-windows and nano-vllm, plus librosa and pyloudnorm for
  the analysis.
- Vocal check: torchaudio HDemucs weights in `~/.cache/torch/hub/checkpoints` (from download.pytorch.org, ~320 MB).
- Marker: `~/.cache/pro-edit-models/ace-step-1.5/.installed-<commit>` tells setup.sh the install is done.

To install by hand:
```bash
MH=~/.cache/pro-edit-models/ace-step-1.5; MV=~/.venvs/music-gen
git clone https://github.com/ace-step/ACE-Step-1.5.git "$MH/repo" && git -C "$MH/repo" checkout ca1e85fe9430179831e6bc6be790c332190a3866
(cd "$MH/repo" && UV_PROJECT_ENVIRONMENT="$MV" uv sync --frozen --python 3.11)
uv pip install --python "$MV/Scripts/python.exe" librosa pyloudnorm          # bin/python on Linux/macOS
"$MV/Scripts/python.exe" -c "from huggingface_hub import snapshot_download as g; c=r'$MH/checkpoints'; g('ACE-Step/Ace-Step1.5', local_dir=c); g('ACE-Step/acestep-v15-xl-sft', local_dir=c+'/acestep-v15-xl-sft')"
# optional: g('ACE-Step/acestep-5Hz-lm-4B', local_dir=c+'/acestep-5Hz-lm-4B')
```

**Use.** Run it with any python; it re-launches itself in the music env and imports nothing from the render env.
```bash
python scripts/music_gen.py --prompt "inspirational modern tech background music, instrumental, opens with warm felt piano chords and airy pads alone with no drums, then punchy modern drums, deep warm bass, claps and bright synth plucks lift the energy, optimistic, hopeful" \
  --structure "[Intro - solo piano and pads, quiet, no drums, no bass]\n\n[Build - drums and bass enter, energy lifts]\n\n[Main Theme - full arrangement, uplifting, driving]\n\n[Main Theme - variation, sustained energy]" \
  --bpm 110 --seconds 60 --seed 7 --drop 5.4 --align --out music/cand_1.wav
python scripts/music_gen.py --jobs jobs.json              # many tracks, one model load (keys as the flags)
python scripts/music_gen.py --analyse music/cand_*.wav --drop 5.4
```
- **Output:** a 48 kHz stereo 24-bit WAV of exactly `--seconds`, with the true peak at -1 dBTP or lower. Next to it, `<out>.json`
  records the model, seed, prompts, the LM's plan (BPM, key), the timings and the analysis. Every RNG is seeded, so the
  same seed, prompt and model give the same track.
- **Prompting:** the caption (`--prompt`) carries style, mood, instruments, timbre and production; it is passed
  verbatim. Tempo and key go in `--bpm`/`--key`, not the caption. `--structure` is section tags only, with no words
  (a typed `\n` counts as a newline); the `[Instrumental]` tag is always added. Describe the arrangement in time in
  both: "opens with X alone, no drums, then Y enters".
- **Defaults** (LM 1.7B, verbatim caption) were measured on 16 seeds x 4 hook prompts. A soft intro that lifts came out
  in 11/16 runs, with 1 vocal flag. LM 4B with its caption rewrite managed 2/16; LM 4B verbatim managed 9/16 but with 5
  vocal flags. `--lm 4B` and `--rewrite` are still available.
- **Length:** the planner writes a complete piece with an ending for the duration it gets. A 60 s request therefore fades
  out around 45-55 s, so music_gen generates 30 s more than asked and cuts (`--gen-seconds`).
- **The lift:** where the intro lifts is up to the model, usually after 4 or 8 bars (about 8.5 s or 16-17 s at 110 bpm).
  With `--drop 5.4 --align`, music_gen finds the kick and bass entry (`lift_in_generation_s` in the json). It then
  starts the bed that far minus 5.4 s in, with a 0.5 s fade over the cut, so the lift lands exactly on the edit's drop.
  If the generated intro is shorter than the drop, nothing is cut (`start_offset_s` is 0), and you should pick another
  seed. Without `--align`, the analysis prints `trim_start_for_drop_s` instead.
- **Analysis per track:**
  - level: integrated LUFS, true peak, clipped samples
  - tempo: BPM and beat regularity
  - the lift: intro vs body level (`lift_db`, `low_lift_db`, `percussive_lift_db`, `lift_s`)
  - consistency: worst dip and gaps between the lift and 50 s
  - vocals: the HDemucs vocal stem vs the mix (`vocal_stem_db_p95`). Instrumental beds sit around -25 to -45 dB. Above
    about -20 dB, or `vocal_seconds_over_m15db` > 0, a voice-like part (choir, vocal chop, or sometimes a lead synth)
    crept in: regenerate with another seed.

  Generate a handful of seeds per prompt and keep the ones with an aligned lift, no vocal flag and small dips.
- **Speed (RTX 5090, GPU otherwise idle):** loading the models takes 40-60 s, or up to ~2.5 min with a cold disk cache.
  Then each 60 s bed (90 s generated) takes 12-15 s: about 3 s for the LM plan, 8-12 s for 50 DiT steps plus the VAE,
  and about 2 s for the analysis. A batch of 16 took 4.6 min with `--jobs`.
  - Other configurations: LM 4B is about 14 s per track; the 2B turbo model is about 5 s.
  - VRAM: about 12-15 GB for XL + LM 1.7B (about 4 GB more with LM 4B).
  - When pro-edit renders (zoom/compose) share the GPU, Windows spills VRAM into system RAM and a track can take 20-400 s.
    ACE-Step may also refuse with "Insufficient free VRAM"; music_gen then waits 30 s and retries, up to 5 times, and a
    failed job doesn't stop the rest of a `--jobs` batch.
- **Other models:** `--model xl-turbo|sft|turbo` (`xl-turbo` needs `ACE-Step/acestep-v15-xl-turbo`, which isn't installed
  by default) and `--lm 4B|0.6B|none`. Use `--offload` when less than ~16 GB of VRAM is free.

| Symptom | Fix |
|---|---|
| `music_gen: ACE-Step env not found` | Run setup.sh (or the commands above); `MUSIC_GEN_VENV` must point at the env. |
| Warnings about torchao cpp extensions, "Redirects are currently not supported", bitsandbytes, `torch_dtype`, "Model code mismatch ... Auto-syncing" | Harmless (the last one copies the repo's model code next to the weights once). |
| `LM vllm backend failed ... retrying with pt` | nano-vllm couldn't start (triton/flash-attn); plain PyTorch decoding works, a bit slower. |
| Generation 2-3x slower than usual, load > 60 s | Another job (zoom/compose renders) holds the GPU and Windows spills VRAM to system RAM. Generate when the GPU is free, or use `--offload`. |
| The bed fades out before the cut | `--gen-seconds` was set to `--seconds`; leave the default (seconds + 30). |
| `start_offset_s` 0 / `lift_s` null | No soft intro, or it is shorter than the drop; regenerate with another seed (keep the "no drums" intro wording). |
| Weights download crawls | Unauthenticated HF downloads are rate-limited at times; just let it run (setup.sh resumes). |
