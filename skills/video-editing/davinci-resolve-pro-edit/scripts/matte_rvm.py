"""Video matting for split beats with Robust Video Matting (RVM, ResNet-50, ONNX on the GPU): a human matting model
with recurrent state, so hair edges are fine and stable from frame to frame, and objects touching the head (a guitar
on the wall behind) stay background. Replaces matte_gpu.py's u2net matte when the model is installed.
Model: rvm_resnet50_fp32.onnx (or rvm_mobilenetv3_fp32.onnx) from github.com/PeterL1n/RobustVideoMatting releases,
looked up in $PRO_EDIT_MODELS/rvm, then ~/.cache/pro-edit-models/rvm (setup.sh downloads it).
Reads split/<id>_cam.mp4 (compose.py --matte makes it), writes split/<id>_matte.mov (FFV1 bgra, alpha = matte), the
same file compose.py reads; a previous matte is kept as split/<id>_matte_prev.mov.
usage: python scripts/matte_rvm.py g02 [--preview 30,229] [--ratio 0.4] [--mobile]"""
import sys, os, shutil, subprocess, glob, site
for _sp in site.getsitepackages():                       # cuDNN / cuBLAS from the nvidia-*-cu12 wheels (Windows DLL path)
    for _d in glob.glob(os.path.join(_sp, 'nvidia', '*', 'bin')):
        os.add_dll_directory(_d); os.environ['PATH'] = _d + os.pathsep + os.environ['PATH']
import numpy as np, cv2
sys.path.insert(0, 'scripts'); import config as C, media as M


def model_path(mobile=False):
    name = 'rvm_mobilenetv3_fp32.onnx' if mobile else 'rvm_resnet50_fp32.onnx'
    for d in (os.environ.get('PRO_EDIT_MODELS'), os.path.join(os.path.expanduser('~'), '.cache', 'pro-edit-models')):
        if d and os.path.exists(os.path.join(d, 'rvm', name)): return os.path.join(d, 'rvm', name)
    return None


def available():
    return model_path() is not None


def session(mobile=False):
    import onnxruntime as ort
    so = ort.SessionOptions(); so.log_severity_level = 3
    return ort.InferenceSession(model_path(mobile), so, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])


def run(frames, sess, ratio, warm=45):
    """frames: (N, h, w, 3) uint8 RGB -> (N, h, w) uint8 alpha. The recurrent state is warmed up on the first `warm`
    frames, then the clip is matted from frame 0 with that state (no 'learning' flicker at the start)."""
    z = np.zeros((1, 1, 1, 1), np.float32); r = [z, z, z, z]
    dr = np.array([ratio], np.float32)
    def step(f, r):
        src = (f.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        out = sess.run(None, {'src': src, 'r1i': r[0], 'r2i': r[1], 'r3i': r[2], 'r4i': r[3], 'downsample_ratio': dr})
        return out[1][0, 0], out[2:]
    for f in frames[:warm]: _, r = step(f, r)
    alphas = np.zeros(frames.shape[:3], np.uint8)
    for n, f in enumerate(frames):
        a, r = step(f, r)
        alphas[n] = np.clip(a * 255 + 0.5, 0, 255).astype(np.uint8)
    return alphas


def matte(bid, ratio=0.4, mobile=False, preview=None):
    cam, mat = f'split/{bid}_cam.mp4', f'split/{bid}_matte.mov'
    p = M.probe(cam); w, h = p['width'], p['height']
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', cam, '-vf', M.dec_vf(cam), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    A = run(frames, session(mobile), ratio)
    if preview:
        os.makedirs('chk', exist_ok=True)
        for n in preview:
            bg = np.full((h, w, 3), 244, np.float32); a = A[n].astype(np.float32)[..., None] / 255
            comp = np.clip(frames[n] * a + bg * (1 - a), 0, 255).astype(np.uint8)
            cv2.imwrite(f'chk/{bid}_rvm_{n}.png', cv2.cvtColor(np.hstack([frames[n], comp]), cv2.COLOR_RGB2BGR))
        return [f'chk/{bid}_rvm_{n}.png' for n in preview]
    if os.path.exists(mat): shutil.copy(mat, f'split/{bid}_matte_prev.mov')
    enc = M.writer_proc(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{w}x{h}', '-r', str(C.FPS), '-i', '-',
                         '-c:v', 'ffv1', '-level', '3', '-slices', '16', '-slicecrc', '0', '-pix_fmt', 'bgra', mat])
    fr = np.zeros((h, w, 4), np.uint8); fr[..., :3] = 255
    for a in A:
        fr[..., 3] = a; enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait()
    ch = np.abs(np.diff(A.astype(np.float32) / 255, axis=0)).sum(axis=(1, 2)).mean()
    print(f'{bid}: RVM matte ({len(A)} frames, ratio {ratio}) -> {mat} | mean frame-to-frame alpha change {ch:.0f} px')
    return mat


if __name__ == '__main__':
    bid = sys.argv[1]
    pv = [int(x) for x in sys.argv[sys.argv.index('--preview') + 1].split(',')] if '--preview' in sys.argv else None
    ratio = float(sys.argv[sys.argv.index('--ratio') + 1]) if '--ratio' in sys.argv else 0.4
    if not available(): raise SystemExit('RVM model missing: run setup.sh (downloads it to ~/.cache/pro-edit-models/rvm)')
    print(matte(bid, ratio, '--mobile' in sys.argv, pv))
