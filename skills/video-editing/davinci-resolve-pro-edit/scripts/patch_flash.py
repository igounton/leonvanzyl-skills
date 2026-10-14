"""Hide a flash of the wrong screen inside a V1 item without touching V1: a V2 clip that holds the last good frame's
screen and pastes the live webcam PiP (rounded mask) from every flash frame, so the speaker keeps moving.
Works on the source's own YUV planes (no colour conversion), like zoom.py.
usage: python scripts/patch_flash.py scan                 lists V1 items whose first/last 40 frames jump to other content
       python scripts/patch_flash.py <id> <good_frame> <first_flash_frame> <last_flash_frame>   (programme frames)
   -> media/<id>.mp4 covering [first_flash_frame, last_flash_frame] inclusive. Plan it as a beat
      {"id": "f01", "kind": "fix", "t0": first/fps, "t1": (last + 1)/fps} so place.py puts it on PE Graphics.
A scan hit is only a candidate (a camera move in a 3D app or a scroll also jumps): LOOK at frame-exact stills
(media.decode_at) of each before patching."""
import sys, os, json
import numpy as np, cv2
sys.path.insert(0, 'scripts'); import config as C, media as M

if sys.argv[1] == 'scan':
    import subprocess
    P = M.program()
    for it in P['items']:
        n = it['src1'] - it['src0']
        for side in ('head', 'tail'):
            k = min(40, n); s0 = (it['src0'] if side == 'head' else it['src1'] - k) / it.get('fps', C.FPS)
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{s0:.4f}', '-i', it['file'], '-frames:v', str(k), '-vf', 'scale=96:54',
                                  '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
            fr = np.frombuffer(raw, np.uint8).reshape(-1, 54, 96).astype(np.float32)
            if len(fr) < 4: continue
            d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)); big = np.where(d > 12)[0]
            if len(big):
                j = big[0] if side == 'tail' else big[-1]
                rec = it['rec0'] + (j + 1 if side == 'head' else n - k + j + 1)
                print(f"V1 item {it['v1']} {side}: content jumps at programme frame ~{rec} ({rec / C.FPS:.2f}s, diff {d[j]:.0f}) - LOOK")
    sys.exit()
bid, good, f0, f1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
seq = M.source_map(f0, f1 + 1)
src = seq[0][0]; p = M.probe(src); W, H = p['width'], p['height']
assert (W, H) == (C.TW, C.TH), 'source and timeline sizes differ'
S = json.load(open('scenes.json'))
item = seq[0][1]['v1']
win = (S['items'].get(str(item)) or {}).get('pip') or S['files'][src]['pip']
x, y, w, h = [v // 2 * 2 for v in win]
pm = M.pip_mask(w, h); masks = [pm, cv2.resize(pm, (w // 2, h // 2), interpolation=cv2.INTER_AREA)]; masks.append(masks[1])
G = [pl.copy() for pl in M.decode_at(M.source_map(good, good + 1), 0, W, H, yuv=True)]
out = os.path.join(C.MEDIA, f'{bid}.mp4')
enc = M.yuv_encoder(out, W, H, src)
for n, planes in enumerate(M.decode(seq, W, H, yuv=True)):
    P = [g.copy() for g in G]
    for c, s in ((0, 1), (1, 2), (2, 2)):
        a = masks[c]
        crop = planes[c][y // s:(y + h) // s, x // s:(x + w) // s].astype(np.float32)
        dst = P[c][y // s:(y + h) // s, x // s:(x + w) // s].astype(np.float32)
        P[c][y // s:(y + h) // s, x // s:(x + w) // s] = np.clip(dst * (1 - a) + crop * a + 0.5, 0, 255).astype(np.uint8)
    for pl in P: enc.stdin.write(np.ascontiguousarray(pl).tobytes())
    if n == 0: cv2.imwrite(f'preview/{bid}_first.png', cv2.cvtColor(M.yuv2rgb(*P, *M.color(src)), cv2.COLOR_RGB2BGR))
enc.stdin.close(); enc.wait()
print(f'{bid}: frames {f0}-{f1} ({f1 - f0 + 1}) -> {out} | screen held from frame {good}, PiP {win} live')
