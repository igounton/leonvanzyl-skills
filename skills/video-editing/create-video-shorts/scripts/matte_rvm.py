"""Head pop-out mattes for split runs with Robust Video Matting (RVM, ResNet-50, ONNX on the GPU): a human matting model
with recurrent state, so hair edges are fine and steady from frame to frame, and objects touching the head (a guitar on
the wall behind it) stay background. It replaced u2net (matte_gpu.py), whose soft low-res blob grabbed the guitar behind
the speaker's ear on and off (lessons.md). matte_gpu.py stays the fallback when the model is missing.
Model: rvm_resnet50_fp32.onnx (github.com/PeterL1n/RobustVideoMatting releases, ~100 MB), looked up in
$PRO_EDIT_MODELS/rvm, then ~/.cache/pro-edit-models/rvm (setup.sh downloads it; shared with davinci-resolve-pro-edit).
Same output as matte_gpu.py: <sk>/cam/r<i>_matte.mov (FFV1 bgra: rgb = the clip frame, alpha = the matte, same size and
frame count, so the matte stays frame-locked with the card), plus <sk>/cam/r<i>_matte.json {"model": "rvm"} - compose.py
skips the 1 px erosion u2net needed for its dark rim.
Each run streams: the recurrent state warms up on the run's first 45 frames, then the run is matted from frame 0 with
that state (no "learning" flicker at the cut). Runs go in parallel on one session (--jobs).
usage: python scripts/matte_rvm.py s1:0,3,5 s2:0,3 [--jobs 4] [--ratio R] [--preview]"""
import os, sys, glob, site, json, subprocess, time
for _sp in site.getsitepackages():                     # cuDNN / cuBLAS from the nvidia-*-cu12 wheels (Windows DLL path)
    for _d in glob.glob(os.path.join(_sp, 'nvidia', '*', 'bin')):
        os.add_dll_directory(_d); os.environ['PATH'] = _d + os.pathsep + os.environ['PATH']
import numpy as np, cv2
from concurrent.futures import ThreadPoolExecutor

WARM = 45
TOP_FEATHER = 14       # source rows faded in at the clip's top edge (the webcam window border: nothing real pops out there)
TOP_RAMP = np.linspace(0, 1, TOP_FEATHER, dtype=np.float32) ** 1.5


def model_path(mobile=False):
    name = 'rvm_mobilenetv3_fp32.onnx' if mobile else 'rvm_resnet50_fp32.onnx'
    for d in (os.environ.get('PRO_EDIT_MODELS'), os.path.join(os.path.expanduser('~'), '.cache', 'pro-edit-models')):
        if d and os.path.exists(os.path.join(d, 'rvm', name)): return os.path.join(d, 'rvm', name)
    return None


def available():
    if model_path() is None: return False
    try:
        import onnxruntime as ort
        return 'CUDAExecutionProvider' in ort.get_available_providers()
    except ImportError:
        return False


def size_of(path):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', path],
                       capture_output=True, text=True).stdout.strip().split(',')
    return int(o[0]), int(o[1])


def frames(path, w, h, count=None):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path] + (['-frames:v', str(count)] if count else []) +
                         ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.wait()


def matte_run(sess, sk, i, ratio=None, preview=False):
    src, out = f'{sk}/cam/r{i}.mkv', f'{sk}/cam/r{i}_matte.mov'
    w, h = size_of(src)
    # RVM's guidance: ~0.25 for HD, 0.125 for 4K; a webcam window (~700x950) matted at 0.4 keeps the hair strands
    dr = np.array([ratio or min(0.4, max(0.125, 400 / max(w, h)))], np.float32)
    z = np.zeros((1, 1, 1, 1), np.float32)

    def step(f, r):
        o = sess.run(None, {'src': (f.astype(np.float32) / 255).transpose(2, 0, 1)[None], 'r1i': r[0], 'r2i': r[1],
                            'r3i': r[2], 'r4i': r[3], 'downsample_ratio': dr})
        return o[1][0, 0], o[2:]
    t0 = time.time(); r = [z, z, z, z]
    for f in frames(src, w, h, WARM): _, r = step(f, r)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{w}x{h}', '-r', '60', '-i', '-',
                            '-c:v', 'ffv1', '-level', '3', '-slices', '16', '-slicecrc', '0', '-pix_fmt', 'bgra', out], stdin=subprocess.PIPE)
    k = 0; prev = None; change = 0.0; shot = None
    for f in frames(src, w, h):
        a, r = step(f, r)
        a = a.astype(np.float32); a[:TOP_FEATHER] *= TOP_RAMP[:, None]
        al = np.clip(a * 255 + 0.5, 0, 255).astype(np.uint8)
        enc.stdin.write(np.dstack([f, al]).tobytes())
        if prev is not None: change += float(np.abs(al.astype(np.int16) - prev).sum()) / 255
        prev = al.astype(np.int16); k += 1
        if preview and shot is None and k == WARM:
            bg = np.full_like(f, 244, dtype=np.float32); aa = al.astype(np.float32)[..., None] / 255
            shot = np.hstack([f, np.clip(f * aa + bg * (1 - aa), 0, 255).astype(np.uint8)])
    enc.stdin.close(); enc.wait()
    json.dump(dict(model='rvm', file=os.path.basename(model_path()), downsample_ratio=float(dr[0]), frames=k), open(f'{sk}/cam/r{i}_matte.json', 'w'))
    if shot is not None:
        os.makedirs('chk', exist_ok=True); cv2.imwrite(f'chk/{sk}_r{i}_rvm.png', cv2.cvtColor(shot, cv2.COLOR_RGB2BGR))
    print(f'{sk} r{i}: RVM {k} frames {w}x{h} (ratio {dr[0]:.2f}) in {time.time() - t0:.1f}s, mean alpha change '
          f'{change / max(1, k - 1):.0f} px/frame -> {out}', flush=True)


if __name__ == '__main__':
    args = sys.argv[1:]; jobs = 4; ratio = None
    if '--jobs' in args: k = args.index('--jobs'); jobs = int(args[k + 1]); del args[k:k + 2]
    if '--ratio' in args: k = args.index('--ratio'); ratio = float(args[k + 1]); del args[k:k + 2]
    preview = '--preview' in args; args = [a for a in args if a != '--preview']
    if not available(): sys.exit('RVM unavailable (model missing or no CUDA onnxruntime): use matte_gpu.py; setup.sh downloads the model')
    import onnxruntime as ort
    so = ort.SessionOptions(); so.log_severity_level = 3
    sess = ort.InferenceSession(model_path(), so, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    print('matte on GPU: Robust Video Matting', os.path.basename(model_path()), flush=True)
    todo = [(spec.split(':')[0], int(i)) for spec in args for i in spec.split(':')[1].split(',')]
    t_all = time.time()
    with ThreadPoolExecutor(max(1, min(jobs, len(todo)))) as ex:
        list(ex.map(lambda a: matte_run(sess, a[0], a[1], ratio, preview), todo))
    print(f'all {len(todo)} mattes in {time.time() - t_all:.1f}s')
