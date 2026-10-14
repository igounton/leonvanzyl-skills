r"""Local AI music for the hook bed: ACE-Step 1.5 XL (MIT licence, outputs usable commercially), headless.

  python music_gen.py --prompt "..." --seconds 60 --seed N --out path.wav [--bpm 110] [--negative "vocals, singing"]
                      [--structure "[Intro - ...]\n\n[Build - ...]"] [--drop 5.4 --align]
  python music_gen.py --jobs jobs.json            # several tracks, one model load ([{prompt, seed, out, ...}, ...])
  python music_gen.py --analyse a.wav b.wav       # objective report only (loudness, lift, energy, tempo, vocals)

Writes a 48 kHz stereo 24-bit WAV of exactly --seconds (true peak <= -1 dBTP), a sidecar <out>.json (model, seed,
prompts, LM plan, timing, analysis) and prints model / seed / timing. Every RNG is seeded: same seed + prompt + model =
same track. The piece is generated 30 s longer than asked and cut (--gen-seconds): the planner always writes a complete
piece with an ending, which would otherwise fade out inside the bed. Instrumental is forced ([Instrumental] tag in the
lyrics, no words); the analysis measures a vocal stem (HDemucs) so a track that sneaks in a voice can be rejected, and
finds where the intro lifts (kick + bass entry). --drop T --align starts the bed so that lift lands on T.

Runs in its own env (MUSIC_GEN_VENV, default ~/.venvs/music-gen, made by setup.sh from the ACE-Step lockfile). Started
from any other python it re-launches itself there. Nothing from the pro-edit render env is imported.
Weights + code: MUSIC_GEN_HOME (default ~/.cache/pro-edit-models/ace-step-1.5: repo/ = ACE-Step-1.5 git checkout,
checkpoints/ = HF weights). Defaults: DiT acestep-v15-xl-sft (4B, 50 steps, CFG 7, shift 3) + the 5 Hz LM 1.7B planner,
caption passed verbatim. Measured on 16 seeds x 4 hook prompts (Oct 2026): LM 1.7B + verbatim caption gave a soft
intro that lifts in 11/16 with 1 vocal flag; LM 4B with its caption rewrite only 2/16 (4B verbatim 9/16 but 5 vocal
flags). --lm 4B / --rewrite stay available. A 90 s generation takes ~12-15 s on an idle RTX 5090 (+40-60 s model load).

Prompting (ACE-Step): --prompt is the caption = style, mood, instruments, timbre, production; say the arrangement in
time ("opens with X alone, no drums, then Y enters"). Keep tempo/key out of it (use --bpm / --key). --structure is the
"temporal script": section tags only (a typed \n is a newline), e.g.
  "[Intro - solo piano and pads, quiet, no drums, no bass]\n\n[Build - drums and bass enter]\n\n[Main Theme - full]"
The model treats bpm/duration as anchors, not exact commands. Not every seed gives a soft intro: generate a few and
keep the ones with start_offset_s > 0, no vocal flag and small dips.
"""
import argparse, json, os, subprocess, sys, time
from pathlib import Path

HOME = Path(os.environ.get('MUSIC_GEN_HOME', Path.home() / '.cache' / 'pro-edit-models' / 'ace-step-1.5'))
VENV = Path(os.environ.get('MUSIC_GEN_VENV', Path.home() / '.venvs' / 'music-gen'))
SR = 48000
MODELS = {'xl-sft': 'acestep-v15-xl-sft', 'xl-turbo': 'acestep-v15-xl-turbo', 'xl-base': 'acestep-v15-xl-base',
          'sft': 'acestep-v15-sft', 'turbo': 'acestep-v15-turbo', 'base': 'acestep-v15-base'}
LMS = {'4B': 'acestep-5Hz-lm-4B', '1.7B': 'acestep-5Hz-lm-1.7B', '0.6B': 'acestep-5Hz-lm-0.6B'}
DEFAULT_NEG = 'vocals, singing, voice, choir, rap, spoken word, lyrics'


def _venv_python():
    for p in (VENV / 'Scripts' / 'python.exe', VENV / 'bin' / 'python'):
        if p.exists():
            return p
    return None


def _ensure_env():
    """Re-run under the music-gen venv when started from another interpreter."""
    try:
        import acestep  # noqa: F401
        return
    except ImportError:
        pass
    py = _venv_python()
    if py is None or Path(sys.executable).resolve() == py.resolve():
        sys.exit(f'music_gen: ACE-Step env not found at {VENV} - run the music part of setup.sh')
    sys.exit(subprocess.call([str(py), os.path.abspath(__file__), *sys.argv[1:]]))


# ----------------------------------------------------------------------------------------------- analysis
def _lift(mono, sr, intro_win=(0.5, 3.0), body_from=10.0, search=(1.0, 25.0)):
    """Where the intro lifts. RMS in 0.1 s hops, 1 s power-domain smoothing; the lift is the first crossing of 60 % of the
    way from the intro level to the body level, preferably on the < 150 Hz band (kick + bass entering), sharpened to the
    first hit (largest 50 ms jump within -1..+0.5 s)."""
    import numpy as np
    from scipy import signal
    dur = len(mono) / sr
    hop = int(0.1 * sr)
    n = len(mono) // hop
    t = np.arange(n) * 0.1 + 0.05
    to_db = lambda y: 20 * np.log10(np.sqrt(np.mean(y[:n * hop].reshape(n, hop) ** 2, 1) + 1e-12))
    pw = lambda d: 10 * np.log10(np.convolve(10 ** (d / 10), np.ones(10) / 10, mode='same') + 1e-12)
    db = to_db(mono)
    sm = pw(db)
    body_end = min(48.0, dur - 1)
    iw = (t >= intro_win[0]) & (t < intro_win[1])
    bw = (t >= body_from) & (t < body_end)
    intro, body = float(np.median(sm[iw])), float(np.median(sm[bw]))
    sw = (t > search[0]) & (t < search[1])
    cand = np.where(sw & (sm >= intro + 0.6 * (body - intro)))[0]
    lift = float(t[cand[0]]) if len(cand) and body - intro > 2 else None
    lo = signal.sosfilt(signal.butter(4, 150, 'low', fs=sr, output='sos'), mono)
    lsm = pw(to_db(lo))
    li, lb = float(np.median(lsm[iw])), float(np.median(lsm[bw]))
    lc = np.where(sw & (lsm >= li + 0.6 * (lb - li)))[0]
    if len(lc) and lb - li > 6:
        lift = float(t[lc[0]])
        h, w = int(0.01 * sr), int(0.05 * sr)
        i0, i1 = int(max(lift - 1.0, 0) * sr), int(min(lift + 0.5, dur) * sr)
        fr = np.lib.stride_tricks.sliding_window_view(lo[i0:i1], w)[::h]
        e = 10 * np.log10(np.mean(fr ** 2, 1) + 1e-12)
        if len(e) > 6:
            lift = (i0 + (int(np.argmax(e[5:] - e[:-5])) + 5) * h + w // 2) / sr
    return dict(db=db, sm=sm, t=t, intro=intro, body=body, body_end=body_end, lift=lift, low_lift_db=round(lb - li, 1))


def analyse(path, vocal_check=True, drop_target=None):
    """Objective report for a music bed. Pure numpy/scipy + pyloudnorm/librosa/torchaudio when present."""
    import numpy as np, soundfile as sf
    from scipy import signal
    x, sr = sf.read(str(path), dtype='float32', always_2d=True)
    mono = x.mean(1)
    dur = len(x) / sr
    rep = dict(file=str(path), seconds=round(dur, 2), sr=sr, channels=x.shape[1])
    peak = float(np.abs(x).max())
    rep['peak_dbfs'] = round(20 * np.log10(peak + 1e-12), 2)
    up = signal.resample_poly(x, 4, 1, axis=0)
    rep['true_peak_dbtp'] = round(20 * np.log10(float(np.abs(up).max()) + 1e-12), 2)
    rep['clipped_samples'] = int((np.abs(x) >= 0.999).sum())
    try:
        import pyloudnorm as pyln
        m = pyln.Meter(sr)
        rep['lufs_integrated'] = round(float(m.integrated_loudness(x)), 2)
        st = [m.integrated_loudness(x[int(t * sr):int((t + 3) * sr)]) for t in np.arange(0, max(dur - 3, 0.01), 1.0)]
        st = np.array([v if np.isfinite(v) else -70 for v in st])
        rep['short_term_lufs_range'] = round(float(np.percentile(st, 95) - np.percentile(st, 10)), 2)
    except ImportError:
        pass
    L = _lift(mono, sr)
    db, sm, t, intro, body, body_end, lift = L['db'], L['sm'], L['t'], L['intro'], L['body'], L['body_end'], L['lift']
    rep.update(intro_db=round(intro, 1), body_db=round(body, 1), lift_db=round(body - intro, 1),
               low_lift_db=L['low_lift_db'], lift_s=None if lift is None else round(lift, 2))
    seg = lambda a, b: sm[(t >= a) & (t < b)]
    # per-second curve (rounded) for the report
    rep['energy_curve_db'] = [round(float(np.mean(db[i * 10:(i + 1) * 10])), 1) for i in range(int(dur))]
    # dips / gaps between the lift and 50 s
    a = (lift or 6.0) + 1.0
    b = min(50.0, dur)
    body_seg = seg(a, b)
    if len(body_seg):
        rep['min_db_after_lift'] = round(float(body_seg.min()), 1)
        rep['worst_dip_db'] = round(float(body - body_seg.min()), 1)
        raw = db[(t >= a) & (t < b)]
        rep['silent_100ms_windows'] = int((raw < body - 30).sum())        # 30 dB under the body level = a gap
        rep['dips_over_6db_s'] = round(float(((body - body_seg) > 6).sum()) * 0.1, 1)
    # spectral brightness before/after lift (pads-only intro vs full band)
    try:
        import librosa
        y = librosa.resample(mono, orig_sr=sr, target_sr=22050)
        oenv = librosa.onset.onset_strength(y=y, sr=22050)
        tempo, beats = librosa.beat.beat_track(onset_envelope=oenv, sr=22050)
        tempo = float(np.atleast_1d(tempo)[0])
        bt = librosa.frames_to_time(beats, sr=22050)
        rep['tempo_bpm'] = round(tempo, 1)
        if len(bt) > 8:
            ibi = np.diff(bt)
            rep['beat_regularity'] = round(float(1 - np.std(ibi) / np.mean(ibi)), 3)   # 1 = metronomic
        ot = librosa.times_like(oenv, sr=22050)
        on = lambda a_, b_: float(np.mean(oenv[(ot >= a_) & (ot < b_)])) if ((ot >= a_) & (ot < b_)).any() else 0.0
        rep['onset_strength_intro'] = round(on(0.5, 3.0), 3)
        rep['onset_strength_body'] = round(on(10, body_end), 3)
        H, P = librosa.decompose.hpss(librosa.stft(y))
        pe = (np.abs(P) ** 2).sum(0)
        pt = librosa.times_like(pe, sr=22050)
        pdb = lambda a_, b_: 10 * np.log10(np.mean(pe[(pt >= a_) & (pt < b_)]) + 1e-12)
        rep['percussive_lift_db'] = round(float(pdb(10, body_end) - pdb(0.5, 3.0)), 1)
        cen = librosa.feature.spectral_centroid(y=y, sr=22050)[0]
        ct = librosa.times_like(cen, sr=22050)
        rep['centroid_hz_intro'] = int(np.median(cen[(ct >= 0.5) & (ct < 3.0)]))
        rep['centroid_hz_body'] = int(np.median(cen[(ct >= 10) & (ct < body_end)]))
    except ImportError:
        pass
    if vocal_check:
        try:
            rep.update(_vocal_stem(x, sr))
        except Exception as e:  # analysis must never sink a generation
            rep['vocal_check_error'] = repr(e)[:200]
    if drop_target is not None and lift is not None:
        rep['trim_start_for_drop_s'] = round(lift - drop_target, 2)   # >0: start the bed this far in; <0: delay it
    return rep


_HDEMUCS = None


def _vocal_stem(x, sr):
    """Vocal-stem level vs the mix with torchaudio's HDemucs (MUSDB-HQ + extra; weights from download.pytorch.org)."""
    global _HDEMUCS
    import numpy as np, torch, torchaudio
    from torchaudio.pipelines import HDEMUCS_HIGH_MUSDB_PLUS as B
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    if _HDEMUCS is None:
        _HDEMUCS = B.get_model().to(dev).eval()
    wav = torch.from_numpy(x.T.copy())
    if wav.shape[0] == 1:
        wav = wav.repeat(2, 1)
    wav = torchaudio.functional.resample(wav, sr, B.sample_rate)
    ref = wav.mean(0)
    mu, sd = ref.mean(), ref.std() + 1e-8
    chunk = B.sample_rate * 20
    outs = []
    with torch.inference_mode():
        for s in range(0, wav.shape[1], chunk):
            seg = ((wav[:, s:s + chunk] - mu) / sd).unsqueeze(0).to(dev)
            outs.append(_HDEMUCS(seg)[0].cpu())
    src = torch.cat(outs, -1) * sd + mu                       # (4 sources, ch, n): drums, bass, other, vocals
    voc = src[list(getattr(_HDEMUCS, 'sources', ['drums', 'bass', 'other', 'vocals'])).index('vocals')].mean(0).numpy()
    mix = wav.mean(0).numpy()
    w = B.sample_rate
    k = len(mix) // w
    vr = np.sqrt(np.mean(voc[:k * w].reshape(k, w) ** 2, 1) + 1e-12)
    mr = np.sqrt(np.mean(mix[:k * w].reshape(k, w) ** 2, 1) + 1e-12)
    rel = 20 * np.log10(vr / mr)
    loud = mr > 10 ** (-45 / 20)
    rel = rel[loud] if loud.any() else rel
    # instrumental beds typically sit at -25..-40 dB here (lead synths leak a little); sung vocals at -3..-12 dB
    return dict(vocal_stem_db_median=round(float(np.median(rel)), 1), vocal_stem_db_p95=round(float(np.percentile(rel, 95)), 1),
                vocal_seconds_over_m15db=int((rel > -15).sum()))


def _summary(rep):
    keys = ['lufs_integrated', 'true_peak_dbtp', 'clipped_samples', 'tempo_bpm', 'beat_regularity', 'lift_s', 'lift_db',
            'percussive_lift_db', 'worst_dip_db', 'silent_100ms_windows', 'vocal_stem_db_median', 'vocal_stem_db_p95',
            'vocal_seconds_over_m15db', 'trim_start_for_drop_s']
    return '  '.join(f'{k}={rep[k]}' for k in keys if k in rep)


# --------------------------------------------------------------------------------------------- generation
class Engine:
    def __init__(self, model='xl-sft', lm='1.7B', offload=False, flash=None, verbose=False):
        os.environ.setdefault('ACESTEP_CHECKPOINTS_DIR', str(HOME / 'checkpoints'))
        os.environ.setdefault('ACESTEP_PROJECT_ROOT', str(HOME / 'repo'))
        os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
        os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY', '1')
        if not verbose:
            os.environ.setdefault('TQDM_DISABLE', '1')            # the LM's per-token progress bars
        from loguru import logger
        logger.remove()
        logger.add(sys.stderr, level='INFO' if verbose else 'WARNING')
        import torch
        from acestep.gpu_config import get_gpu_config, set_global_gpu_config
        from acestep.handler import AceStepHandler
        from acestep.llm_inference import LLMHandler
        set_global_gpu_config(get_gpu_config())
        t0 = time.time()
        self.ckpt = os.environ['ACESTEP_CHECKPOINTS_DIR']
        self.model = MODELS.get(model, model)
        self.lm = None if str(lm).lower() in ('none', 'off', '0') else LMS.get(lm, lm)
        self.turbo = 'turbo' in self.model
        self.dit = AceStepHandler()
        dev = 'cuda' if torch.cuda.is_available() else 'cpu'
        if flash is None:
            flash = self.dit.is_flash_attention_available(dev)
        msg, ok = self.dit.initialize_service(project_root=str(HOME / 'repo'), config_path=self.model, device=dev,
                                              use_flash_attention=flash, compile_model=False, offload_to_cpu=offload)
        if not ok:
            sys.exit(f'music_gen: DiT init failed: {msg}')
        self.llm = LLMHandler()
        if self.lm:
            msg, ok = self.llm.initialize(checkpoint_dir=self.ckpt, lm_model_path=self.lm, backend='vllm', device=dev,
                                          offload_to_cpu=offload)
            if not ok:   # nano-vllm can be unavailable (no triton/flash-attn): plain PyTorch decoding still works
                print(f'music_gen: LM vllm backend failed ({str(msg)[:120]}), retrying with pt', file=sys.stderr)
                msg, ok = self.llm.initialize(checkpoint_dir=self.ckpt, lm_model_path=self.lm, backend='pt', device=dev,
                                              offload_to_cpu=offload)
            if not ok:
                sys.exit(f'music_gen: LM init failed: {msg}')
        self.device, self.flash = dev, flash
        self.load_s = time.time() - t0
        gpu = torch.cuda.get_device_name(0) if dev == 'cuda' else 'cpu'
        print(f'music_gen: loaded {self.model} + LM {self.lm or "off"} on {gpu} (flash-attn {flash}) in {self.load_s:.1f}s', flush=True)

    def generate(self, prompt, seconds, seed, out, bpm=None, key='', negative=DEFAULT_NEG, structure='[Instrumental]',
                 steps=None, cfg=7.0, shift=3.0, rewrite=False, lm_temperature=0.85, analyse_out=True, drop=None,
                 gen_seconds=None, align=False):
        import numpy as np, soundfile as sf, torch
        from acestep.inference import GenerationParams, GenerationConfig, generate_music
        seed = int(seed) if seed is not None and int(seed) >= 0 else int(np.random.randint(0, 2 ** 31 - 1))
        steps = steps or (8 if self.turbo else 50)
        # The planner writes a complete piece (intro ... ending) for the duration it is given, so a 60 s request
        # ends in a fade around 45-55 s. Generating longer and cutting keeps the energy up to the cut.
        if gen_seconds is None:
            gen_seconds = seconds + 30 if seconds <= 240 else seconds
        gen_seconds = max(float(gen_seconds or seconds), float(seconds))
        # Same text whether it came from a jobs file or a shell, else one seed gives two tracks: a literal \n typed
        # on a command line becomes a newline, CRs (CRLF, $(python -c ...) output on Windows) are dropped.
        prompt = ' '.join((prompt or '').replace('\r', ' ').split())
        structure = (structure or '').replace('\\n', '\n').replace('\r', '')
        lyrics = structure.strip() if structure.strip() else '[Instrumental]'
        if '[instrumental]' not in lyrics.lower():
            lyrics = '[Instrumental]\n\n' + lyrics
        p = GenerationParams(task_type='text2music', caption=prompt, lyrics=lyrics, instrumental=True,
                             vocal_language='unknown', bpm=int(bpm) if bpm else None, keyscale=key or '',
                             timesignature='4', duration=gen_seconds, inference_steps=int(steps), seed=seed,
                             guidance_scale=float(cfg), shift=float(shift), thinking=bool(self.lm),
                             use_cot_caption=bool(rewrite), use_cot_metas=True, use_cot_language=False,
                             lm_temperature=lm_temperature, lm_negative_prompt=negative or 'NO USER INPUT',
                             enable_normalization=True, normalization_db=-1.0)
        cfgo = GenerationConfig(batch_size=1, use_random_seed=False, seeds=[seed], audio_format='wav')
        import random
        t0 = time.time()
        for attempt in range(6):
            # ACE-Step seeds the DiT noise but not the LM's CoT sampling (key/plan): seed every RNG so seed = same track
            random.seed(seed)
            np.random.seed(seed % 2 ** 32)
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
            res = generate_music(self.dit, self.llm, p, cfgo, save_dir=None)
            err = '' if res.success and res.audios else str(res.error or res.status_message)
            if not err or not ('VRAM' in err or 'out of memory' in err.lower()) or attempt == 5:
                break
            # shared GPU: another job (renders) holds the memory - wait for it instead of failing
            print(f'music_gen: {err[:90]} - waiting 30 s for the GPU (attempt {attempt + 1}/5)', file=sys.stderr, flush=True)
            torch.cuda.empty_cache()
            time.sleep(30)
        gen_s = time.time() - t0
        if err:
            raise RuntimeError(f'generation failed: {err}')
        a = res.audios[0]
        wav = a['tensor']
        wav = wav.float().cpu().numpy() if hasattr(wav, 'cpu') else np.asarray(wav, dtype=np.float32)
        if wav.ndim == 1:
            wav = np.stack([wav, wav])
        if wav.shape[0] > wav.shape[1]:
            wav = wav.T
        sr = int(a.get('sample_rate', SR))
        if sr != SR:
            import torchaudio
            wav = torchaudio.functional.resample(torch.from_numpy(wav), sr, SR).numpy()
        if wav.shape[0] == 1:
            wav = np.repeat(wav, 2, 0)
        wav = wav[:2].T                                            # (n, 2)
        n = int(round(seconds * SR))
        offset, raw_lift = 0.0, None
        if drop is not None:
            raw_lift = _lift(wav.mean(1), SR)['lift']
            if align and raw_lift is not None and raw_lift > drop:
                # start the bed (lift - drop) s in, so the lift lands on the edit's drop; short fade over the cut-in
                offset = raw_lift - drop
                s0 = int(round(offset * SR))
                wav = wav[s0:].copy()
                f = int(min(0.5, drop / 2) * SR)
                wav[:f] *= (np.sin(np.linspace(0, np.pi / 2, f, dtype=np.float32)) ** 2)[:, None]
        if len(wav) >= n:
            wav = wav[:n].copy()
            f = int(0.03 * SR)
            wav[-f:] *= np.linspace(1, 0, f, dtype=np.float32)[:, None]   # no click where we cut
        else:
            wav = np.concatenate([wav, np.zeros((n - len(wav), 2), np.float32)])
        from scipy.signal import resample_poly
        pk = float(np.abs(resample_poly(wav, 4, 1, axis=0)).max())   # true peak (4x oversampled)
        if pk > 0.891:                                             # keep the true peak <= -1 dBTP
            wav *= 0.891 / pk
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(out), wav, SR, subtype='PCM_24')
        meta = res.extra_outputs.get('lm_metadata') or {}
        tc = res.extra_outputs.get('time_costs') or {}
        side = dict(model=self.model, lm=self.lm, seed=seed, seconds=seconds, generated_seconds=gen_seconds,
                    lift_in_generation_s=None if raw_lift is None else round(raw_lift, 2), start_offset_s=round(offset, 2),
                    bpm_requested=bpm, key_requested=key,
                    prompt=prompt, structure=lyrics, negative=negative, steps=steps, cfg=cfg, shift=shift,
                    lm_plan={k: (v if isinstance(v, (str, int, float, bool)) or v is None else str(v))
                             for k, v in meta.items() if k != 'audio_codes'},
                    timing=dict(load_s=round(self.load_s, 1), generate_s=round(gen_s, 1),
                                **{k: round(v, 2) for k, v in tc.items() if isinstance(v, (int, float))}),
                    licence='ACE-Step 1.5 (MIT; model card: outputs may be used commercially)')
        line = (f'music_gen: {out.name}  model {self.model}+LM {self.lm or "off"}  seed {seed}  '
                f'{gen_seconds:.0f}s generated (cut to {seconds:.0f}s{f" from {offset:.2f}s" if offset else ""}) in {gen_s:.1f}s')
        if meta.get('bpm') or meta.get('keyscale'):
            line += f'  (LM plan: {meta.get("bpm")} bpm, {meta.get("keyscale")})'
        print(line, flush=True)
        if analyse_out:
            rep = analyse(out, drop_target=drop)
            side['analysis'] = rep
            print('  ' + _summary(rep), flush=True)
        json.dump(side, open(str(out) + '.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        return side


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--prompt', help='caption: style, mood, instruments, timbre, production')
    ap.add_argument('--seconds', type=float, default=60)
    ap.add_argument('--seed', type=int, default=-1)
    ap.add_argument('--out', help='output .wav (48 kHz stereo, 24-bit)')
    ap.add_argument('--bpm', type=int)
    ap.add_argument('--key', default='', help='e.g. "D major", "F# minor"')
    ap.add_argument('--negative', default=DEFAULT_NEG, help='negative prompt for the LM planner')
    ap.add_argument('--structure', default='[Instrumental]', help=r'section tags, e.g. "[Intro - soft piano]\n\n[Build]"')
    ap.add_argument('--gen-seconds', type=float, help='length actually generated before the cut (default seconds+30, '
                    'so the natural ending of the piece falls after the cut); = --seconds keeps that ending')
    ap.add_argument('--drop', type=float, help='where the edit wants the lift (s): reports how far to trim/delay the bed')
    ap.add_argument('--align', action='store_true', help='with --drop: cut the bed so the detected lift lands on --drop '
                    '(when the generated intro is longer than --drop; 0.5 s fade-in over the cut)')
    ap.add_argument('--model', default='xl-sft', help='|'.join(MODELS))
    ap.add_argument('--lm', default='1.7B', help='1.7B | 4B (needs ACE-Step/acestep-5Hz-lm-4B) | 0.6B | none')
    ap.add_argument('--steps', type=int)
    ap.add_argument('--cfg', type=float, default=7.0)
    ap.add_argument('--shift', type=float, default=3.0)
    ap.add_argument('--rewrite', action='store_true', help='let the LM rewrite/expand the caption (looser intro control)')
    ap.add_argument('--offload', action='store_true', help='CPU offload when less than ~16 GB of VRAM is free')
    ap.add_argument('--no-flash', action='store_true')
    ap.add_argument('--no-analyse', action='store_true')
    ap.add_argument('--jobs', help='JSON list of {prompt, seconds, seed, out, bpm, key, negative, structure, drop}')
    ap.add_argument('--analyse', nargs='+', metavar='WAV', help='only analyse existing files')
    ap.add_argument('--verbose', action='store_true')
    a = ap.parse_args()
    _ensure_env()
    if a.analyse:
        for f in a.analyse:
            rep = analyse(f, drop_target=a.drop)
            curve = rep.pop('energy_curve_db')
            print(json.dumps(rep, indent=1))
            print(' energy_curve_db (1 s):', ' '.join(f'{v:.0f}' for v in curve))
        return
    jobs = json.load(open(a.jobs, encoding='utf-8')) if a.jobs else None
    if not jobs:
        if not a.prompt or not a.out:
            ap.error('--prompt and --out are required (or --jobs / --analyse)')
        jobs = [dict(prompt=a.prompt, seconds=a.seconds, seed=a.seed, out=a.out, bpm=a.bpm, key=a.key,
                     negative=a.negative, structure=a.structure, drop=a.drop, gen_seconds=a.gen_seconds, align=a.align)]
    eng = Engine(a.model, a.lm, offload=a.offload, flash=False if a.no_flash else None, verbose=a.verbose)
    t0 = time.time()
    failed = []
    for j in jobs:
        try:
            eng.generate(j['prompt'], float(j.get('seconds', a.seconds)), j.get('seed', a.seed), j['out'],
                         bpm=j.get('bpm', a.bpm), key=j.get('key', a.key), negative=j.get('negative', a.negative),
                         structure=j.get('structure', a.structure), steps=j.get('steps', a.steps),
                         cfg=j.get('cfg', a.cfg), shift=j.get('shift', a.shift), rewrite=j.get('rewrite', a.rewrite),
                         analyse_out=not a.no_analyse, drop=j.get('drop', a.drop),
                         gen_seconds=j.get('gen_seconds', a.gen_seconds), align=j.get('align', a.align))
        except Exception as e:   # one bad job must not sink the batch
            failed.append(j['out'])
            print(f'music_gen: FAILED {j["out"]}: {e}', file=sys.stderr, flush=True)
    print(f'music_gen: {len(jobs) - len(failed)}/{len(jobs)} track(s), total {time.time() - t0 + eng.load_s:.1f}s '
          f'(load {eng.load_s:.1f}s)')
    if failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
