"""Screen 4 full-refresh encoder, version 2 ("encode6"): linear-light error diffusion + palette search on the 512-colour grid,
segments encoded in parallel on all cores.  Writes the same stream format as encode4.py (the player is unchanged).

  frame header: flags (bit0 = 32-byte palette follows), then 12288 bytes (6 KB patterns + 6 KB colours, VRAM order)
"""
import os, sys, time, argparse
import numpy as np
import multiprocessing as mp
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
H, W = 192, 256


def pack_state(A, B, bits):
    pat = (bits.astype(np.uint8) << (7 - np.arange(8, dtype=np.uint8))).sum(-1).astype(np.uint8)
    col = ((B << 4) | A).astype(np.uint8)
    return pat, col


def tile_err(L, ref_gam_blur, img):
    """per-tile squared error of a candidate image vs the reference, eye model: blur in linear light, compare in gamma space"""
    g = L.to_gam(gaussian_filter(L.to_lin(img.astype(np.float32)), (1, 1, 0)))
    return ((g - ref_gam_blur) ** 2).sum(-1).reshape(24, 8, 32, 8).sum((1, 3))


def work(task):
    import screen4_sim as S
    import encode4 as E
    import s4_lab as L
    L.VERBOSE = False
    path, nframes, start, end, p = task
    t0 = time.time()
    fr = np.memmap(path, np.uint8, 'r', shape=(nframes, H, W, 3))
    seg = np.array(fr[start:end])
    pal = E.seg_palette(seg, None)
    if p['search']:
        refs = seg[np.linspace(0, len(seg) - 1, min(len(seg), 19)).astype(int)]
        pal = L.palette_local_search(refs, pal, sweeps=3, npix=14000)
    # order the palette from dark to light: index 0 (used for the border colour) is always the darkest colour of every segment,
    # and the colours keep a similar order from one segment's palette to the next
    lum = (pal * np.array([0.30, 0.55, 0.15], np.float32)).sum(-1)
    pal = pal[np.argsort(lum, kind='stable')]
    frames = []; psnr = []; reused = []
    prev = None
    for i in range(len(seg)):
        src = seg[i].astype(np.float32)
        A, B, bits, out = L.code_lin(src, pal, p['kcon'], clampe=p['clamp'])
        ref_blur = L.to_gam(gaussian_filter(L.to_lin(src), (1, 1, 0)))
        if prev is not None and p['hyst'] > 0:
            e_new = tile_err(L, ref_blur, out)
            e_old = tile_err(L, ref_blur, L.state_to_img(prev[0], prev[1], prev[2], pal))
            keep = e_old <= e_new * (1 + p['hyst']) + p['habs']
            km = np.repeat(keep, 8, 0)
            A = np.where(km, prev[0], A); B = np.where(km, prev[1], B); bits = np.where(km[..., None], prev[2], bits)
            reused.append(keep.mean())
        prev = (A, B, bits)
        out = L.state_to_img(A, B, bits, pal)
        pat, col = pack_state(A, B, bits)
        frames.append(E.frame_bytes(pat, col))
        g = L.to_gam(gaussian_filter(L.to_lin(out), (1, 1, 0)))
        psnr.append(10 * np.log10(255 ** 2 / ((g - ref_blur) ** 2).mean()))
    q = np.rint(pal * 7 / 255).astype(int)
    palbytes = b''.join(bytes([(int(r) << 4) | int(b), int(g)]) for r, g, b in q)
    return start, palbytes, frames, pal, psnr, (np.mean(reused) if reused else 0.0), time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frames', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--n', type=int, default=0)
    ap.add_argument('--seg', type=int, default=38)
    ap.add_argument('--workers', type=int, default=1, help='parallel processes (default 1)')
    ap.add_argument('--kcon', type=float, default=0.035)
    ap.add_argument('--clamp', type=float, default=0.3)
    ap.add_argument('--hyst', type=float, default=0.4)
    ap.add_argument('--habs', type=float, default=800.0)
    ap.add_argument('--no-search', action='store_true', help='skip the palette search on the 512-colour grid')
    a = ap.parse_args()
    size = os.path.getsize(a.frames); n = size // (H * W * 3)
    if a.n: n = min(n, a.n)
    p = dict(kcon=a.kcon, clamp=a.clamp, hyst=a.hyst, habs=a.habs, search=not a.no_search)
    tasks = [(a.frames, size // (H * W * 3), s, min(n, s + a.seg), p) for s in range(0, n, a.seg)]
    print(f'{n} frames, {len(tasks)} segments, {a.workers} workers', flush=True)
    t0 = time.time(); results = {}
    with mp.Pool(a.workers) as pool:
        for r in pool.imap_unordered(work, tasks):
            results[r[0]] = r
            print(f'  segment at frame {r[0]:5d} done ({r[6]:.0f}s)  [{len(results)}/{len(tasks)}, {time.time()-t0:.0f}s elapsed]', flush=True)
    stream = bytearray(); ps = []; reused = []; pal0 = None
    for s in sorted(results):
        _, palbytes, frames, pal, psnr, reuse, _t = results[s]
        if pal0 is None: pal0 = pal
        for j, fb in enumerate(frames):
            if j == 0:
                stream += bytes([1]) + palbytes
            else:
                stream += bytes([0])
            stream += fb
        ps += psnr; reused.append(reuse)
    open(a.out, 'wb').write(stream)
    open(a.out + '.meta', 'w').write(f'{n}\n')
    np.save(a.out + '.pal.npy', pal0)
    print(f'DONE {len(stream)} bytes, {n} frames, blurred(linear-light) PSNR mean {np.mean(ps):.2f} min {np.min(ps):.1f}, tiles reused {np.mean(reused):.2f}, '
          f'{(time.time()-t0)/60:.1f} min')


if __name__ == '__main__':
    main()
