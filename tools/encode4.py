"""Screen 4 (GRAPHIC 3) full-refresh video encoder.
Every frame = 6 KB pattern table + 6 KB colour table (identity-mapped name table), error-diffused 2-colour rows,
one global 16-colour palette, temporal hysteresis so static areas keep their previous tile bytes.

Frame layout (12288 bytes): pattern bytes for the 3 screen thirds (2048 each), then colour bytes for the 3 thirds.
Within a third: tile index n = (tile_row_in_third * 32 + tile_col), 8 bytes per tile (one per pixel row).
"""
import sys, os, time, argparse
import numpy as np
from scipy.ndimage import gaussian_filter
import screen4_sim as S
from screen4_sim import *

HERE = os.path.dirname(os.path.abspath(__file__))
NT = 24 * 32


def code_fs_bytes(img, pal, kcon, clampe=48.0):
    """error-diffusion coding; returns (pat (H,32) uint8, col (H,32) uint8, out image)"""
    h = img.shape[0]
    R = img.reshape(h, 32, 8, 3).astype(np.float32)
    A_all, B_all = pal[PI], pal[PJ]
    V = B_all - A_all
    den = (V * V * WTS).sum(-1); den = np.where(den == 0, 1, den)
    contrast = (V * V * WTS).sum(-1)
    out = np.zeros_like(R)
    pat = np.zeros((h, 32), np.uint8); col = np.zeros((h, 32), np.uint8)
    err_next = np.zeros((32, 8, 3), np.float32)
    for r in range(h):
        cur = np.clip(R[r] + err_next, 0, 255)
        c = cur[:, :, None, :]
        t = np.clip((((c - A_all) * V * WTS).sum(-1)) / den, 0, 1)
        m = A_all + t[..., None] * V
        cost = ((((c - m) ** 2) * WTS).sum(-1)).sum(1) + kcon * 8 * contrast
        sel = cost.argmin(-1)
        A = pal[PI[sel]]; B = pal[PJ[sel]]
        err_next[:] = 0
        e_row = np.zeros((32, 3), np.float32)
        bits = np.zeros((32,), np.uint8)
        for px in range(8):
            cc = cur[:, px] + e_row
            dA = (((cc - A) ** 2) * WTS).sum(-1); dB = (((cc - B) ** 2) * WTS).sum(-1)
            pick = dB < dA
            o = np.where(pick[:, None], B, A)
            e = np.clip(cc - o, -clampe, clampe)
            out[r, :, px] = o
            bits |= (pick.astype(np.uint8) << (7 - px))
            e_row = e * 7 / 16
            err_next[:, px] += e * 5 / 16
            if px > 0: err_next[:, px - 1] += e * 3 / 16
            if px < 7: err_next[:, px + 1] += e * 1 / 16
        pat[r] = bits
        col[r] = ((PJ[sel] << 4) | PI[sel]).astype(np.uint8)
    return pat, col, out.reshape(h, W, 3)


def render_bytes(pat, col, pal):
    """(H,32) pattern/colour bytes -> RGB image (H,W,3)"""
    bits = ((pat[:, :, None] >> (7 - np.arange(8))) & 1).astype(bool)            # (H,32,8)
    fg = pal[(col >> 4)][:, :, None, :]; bg = pal[(col & 15)][:, :, None, :]
    return np.where(bits[..., None], fg, bg).reshape(pat.shape[0], W, 3)


def tile_order(arr):
    """(H,32) per-pixel-row bytes -> bytes in VRAM order (3 thirds x [tile_row(8) x tile_col(32)] x 8 rows)"""
    a = arr.reshape(24, 8, 32).transpose(0, 2, 1)                                  # (tile_row, tile_col, 8)
    return a.reshape(3, 8 * 32, 8).reshape(-1)                                     # third-major, tile n = r*32+c


def frame_bytes(pat, col):
    return tile_order(pat).tobytes() + tile_order(col).tobytes()


def dedupe(pal, px):
    pal = pal.copy()
    d = lambda a, b: (((a - b) ** 2) * WTS).sum(-1)
    seen = {}
    for i in range(16):
        key = tuple(pal[i].tolist())
        if key in seen:
            far = d(px[:, None, :], pal[None]).min(1)
            pal[i] = snap(px[far.argmax()])
        else:
            seen[key] = i
    return pal


def seg_palette(fr, init=None, nrefine=6, seed=1, nref=8):
    """palette for a set of frames; if init is given, refine it (keeps colour indices stable between segments)"""
    px = np.concatenate([fr[i].reshape(-1, 3) for i in np.linspace(0, len(fr) - 1, min(len(fr), 6)).astype(int)])
    pal = kmeans_palette(px, seed=seed) if init is None else init.copy()
    ref = np.linspace(0, len(fr) - 1, min(len(fr), nref)).astype(int)
    for it in range(nrefine):
        num = np.zeros((16, 3)); den = np.zeros(16)
        for i in ref:
            img = fr[i].astype(np.float32)
            cost, ts = row_costs(img, pal, 'segment')
            sel = cost.argmin(-1)
            R = img.reshape(H, 32, 8, 3).astype(np.float64)
            A_i = PI[sel]; B_i = PJ[sel]
            t = np.take_along_axis(ts, sel[:, :, None, None], 3)[..., 0].astype(np.float64)
            Ac = pal.astype(np.float64)[A_i][:, :, None, :]; Bc = pal.astype(np.float64)[B_i][:, :, None, :]
            ia = np.broadcast_to(A_i[:, :, None], t.shape).ravel(); ib = np.broadcast_to(B_i[:, :, None], t.shape).ravel()
            wa = 1 - t
            np.add.at(num, ia, (wa[..., None] * (R - t[..., None] * Bc)).reshape(-1, 3)); np.add.at(den, ia, (wa ** 2).ravel())
            np.add.at(num, ib, (t[..., None] * (R - wa[..., None] * Ac)).reshape(-1, 3)); np.add.at(den, ib, (t ** 2).ravel())
        upd = den > 1e-3
        newp = pal.astype(np.float64).copy()
        newp[upd] = np.clip(num[upd] / den[upd, None], 0, 255)
        pal = snap(newp).astype(np.float32)
        pal = dedupe(pal, px[::20])
    return pal


def global_palette(fr, nsamp=24, nrefine=6, seed=1):
    ids = np.linspace(0, len(fr) - 1, nsamp).astype(int)
    return seg_palette(fr[ids], None, nrefine, seed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frames', default=HERE + '/frames_256x192_10fps.rgb')
    ap.add_argument('--n', type=int, default=0)
    ap.add_argument('--out', default=HERE + '/s4_stream.bin')
    ap.add_argument('--hyst', type=float, default=0.25, help='keep previous tile if its error <= new*(1+hyst)+abs')
    ap.add_argument('--seg', type=int, default=0, help='frames per palette segment (0 = one global palette)')
    ap.add_argument('--habs', type=float, default=400.0)
    a = ap.parse_args()
    fr = np.fromfile(a.frames, np.uint8).reshape(-1, H, W, 3)
    if a.n: fr = fr[:a.n]
    t0 = time.time()
    seg = a.seg or len(fr)
    stream = bytearray(); prev_pat = prev_col = None; ps = []; reused = []; pals = []
    pal = None
    for n in range(len(fr)):
        newseg = (n % seg == 0)
        if newseg:
            chunk = fr[n:n + seg]
            pal = seg_palette(chunk, pal if a.seg and pal is not None else None) if a.seg else global_palette(fr)
            prev_pat = prev_col = None
            pals.append(pal)
            print(f'  segment at frame {n}: palette ready [{time.time()-t0:.0f}s]', flush=True)
        src = fr[n].astype(np.float32)
        pat, col, out = code_fs_bytes(src, pal, S.KCON)
        if prev_pat is not None and a.hyst > 0:
            sb = gaussian_filter(src, (1, 1, 0))
            e_new = ((gaussian_filter(out, (1, 1, 0)) - sb) ** 2).sum(-1).reshape(24, 8, 32, 8).sum((1, 3))
            po = render_bytes(prev_pat, prev_col, pal)
            e_old = ((gaussian_filter(po, (1, 1, 0)) - sb) ** 2).sum(-1).reshape(24, 8, 32, 8).sum((1, 3))
            keep = e_old <= e_new * (1 + a.hyst) + a.habs
            km = np.repeat(keep, 8, 0)
            pat = np.where(km, prev_pat, pat); col = np.where(km, prev_col, col)
            reused.append(keep.mean())
        out = render_bytes(pat, col, pal)
        aa = gaussian_filter(src, (1, 1, 0)); bb = gaussian_filter(out, (1, 1, 0))
        ps.append(10 * np.log10(255 ** 2 / ((aa - bb) ** 2).mean()))
        # frame header: flags (bit0 = palette follows) [+ 32 palette bytes]
        if newseg:
            q = np.rint(pal * 7 / 255).astype(int)
            pb = bytearray()
            for r_, g_, b_ in q:
                pb += bytes([(int(r_) << 4) | int(b_), int(g_)])
            stream += bytes([1]) + bytes(pb)
        else:
            stream += bytes([0])
        stream += frame_bytes(pat, col)
        prev_pat, prev_col = pat, col
        if n % 25 == 0:
            print(f'frame {n}/{len(fr)} psnr {np.mean(ps):.2f} reused {np.mean(reused) if reused else 0:.2f} [{time.time()-t0:.0f}s]', flush=True)
    pal = pals[0]
    print(f'DONE {len(stream)} bytes, {len(fr)} frames, blurred PSNR mean {np.mean(ps):.2f} min {np.min(ps):.1f}, tiles reused {np.mean(reused) if reused else 0:.2f}')
    open(a.out, 'wb').write(stream)
    np.save(a.out + '.pal.npy', pal)
    open(a.out + '.meta', 'w').write(f'{len(fr)}\n')


if __name__ == '__main__':
    main()
