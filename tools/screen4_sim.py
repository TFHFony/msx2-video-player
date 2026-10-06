"""Screen 4 (GRAPHIC 3) single-frame coding experiments: 2 colours per 8x1 row, 16-colour palette.
Compares colour-pair selection / dithering / palette strategies, incl. per-band palettes (line interrupt)."""
import sys, os, time
import numpy as np
from scipy.cluster.vq import kmeans2
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageDraw

W, H = 256, 192
WTS = np.array([0.30, 0.55, 0.15], np.float32) * 3
KCON = float(os.environ.get('KCON', '0.05'))
HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [(i, j) for i in range(16) for j in range(i, 16)]
PI = np.array([p[0] for p in PAIRS]); PJ = np.array([p[1] for p in PAIRS])
BAYER8 = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38],
                   [60, 28, 52, 20, 62, 30, 54, 22], [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                   [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]], np.float32)
THR = (BAYER8 + 0.5) / 64.0


def load_frames():
    return np.fromfile(HERE + '/frames_256x192_10fps.rgb', np.uint8).reshape(-1, H, W, 3)


def snap(c):
    return np.clip(np.rint(c / 255.0 * 7), 0, 7) * 255.0 / 7.0


def kmeans_palette(px, k=16, seed=1):
    px = px.reshape(-1, 3).astype(np.float64)
    if len(px) > 60000:
        px = px[np.random.default_rng(seed).integers(0, len(px), 60000)]
    best = None
    for s in range(3):
        cen, lab = kmeans2(px * np.sqrt(WTS), k, minit='++', seed=seed + s, iter=25)
        err = ((px * np.sqrt(WTS) - cen[lab]) ** 2).sum()
        if best is None or err < best[0]:
            best = (err, cen / np.sqrt(WTS))
    return snap(best[1]).astype(np.float32)


def pair_dist_matrix(pal):
    d = lambda a, b: (((a - b) ** 2) * WTS).sum(-1)
    A, B = pal[PI], pal[PJ]
    straight = d(A[:, None], A[None]) + d(B[:, None], B[None])
    cross = d(A[:, None], B[None]) + d(B[:, None], A[None])
    return np.minimum(straight, cross)


def row_costs(img, pal, mode):
    """img (h,W,3); returns node cost (h,32,136) plus helper arrays for rendering"""
    h = img.shape[0]
    R = img.reshape(h, 32, 8, 3).astype(np.float32)
    A, B = pal[PI], pal[PJ]
    if mode == 'nearest':
        D = (((R[:, :, :, None, :] - pal[None, None, None]) ** 2) * WTS).sum(-1)       # (h,32,8,16)
        cost = np.minimum(D[..., PI], D[..., PJ]).sum(2)
        return cost, None
    V = B - A
    den = (V * V * WTS).sum(-1)
    den = np.where(den == 0, 1, den)
    contrast = (V * V * WTS).sum(-1)
    cost = np.empty((h, 32, len(PAIRS)), np.float32)
    ts = np.empty((h, 32, 8, len(PAIRS)), np.float32)
    for r0 in range(0, h, 16):
        c = R[r0:r0 + 16, :, :, None, :]
        t = np.clip((((c - A) * V * WTS).sum(-1)) / den, 0, 1)                       # (16,32,8,136)
        m = A + t[..., None] * V
        cost[r0:r0 + 16] = ((((c - m) ** 2) * WTS).sum(-1)).sum(2) + KCON * 8 * contrast
        ts[r0:r0 + 16] = t
    return cost, ts


def dp_pairs(cost, pal, mu):
    """choose a pair per (row, tile column) minimising node cost + mu * pair-change cost down each column"""
    h = cost.shape[0]
    if mu <= 0:
        return cost.argmin(-1)
    T = pair_dist_matrix(pal).astype(np.float32) * mu                                # (136,136)
    acc = cost[0].copy()                                                             # (32,136)
    back = np.zeros((h, 32, len(PAIRS)), np.int16)
    for r in range(1, h):
        tot = acc[:, :, None] + T[None]                                              # (32,q,p)
        back[r] = tot.argmin(1)
        acc = cost[r] + tot.min(1)
    out = np.zeros((h, 32), np.int64)
    out[-1] = acc.argmin(-1)
    for r in range(h - 1, 0, -1):
        out[r - 1] = np.take_along_axis(back[r], out[r][:, None], 1)[:, 0]
    return out


def render(img, pal, sel, mode, ts, row_off=0):
    h = img.shape[0]
    R = img.reshape(h, 32, 8, 3)
    A = pal[PI[sel]][:, :, None, :]; B = pal[PJ[sel]][:, :, None, :]                 # (h,32,1,3)
    if mode == 'nearest':
        dA = (((R - A) ** 2) * WTS).sum(-1); dB = (((R - B) ** 2) * WTS).sum(-1)
        bit = dB < dA
    else:
        t = np.take_along_axis(ts, sel[:, :, None, None], 3)[..., 0]                 # (h,32,8)
        thr = THR[(np.arange(h) + row_off) % 8][:, None, :]
        bit = t > thr
    out = np.where(bit[..., None], B, A)
    return out.reshape(h, W, 3), (sel, bit)


def refine_palette(img, pal, sel, ts, iters=4):
    """move palette colours so the coded mixtures fit the image better (weighted least squares)"""
    h = img.shape[0]
    R = img.reshape(h, 32, 8, 3).astype(np.float64)
    pal = pal.astype(np.float64).copy()
    for _ in range(iters):
        A_i = PI[sel]; B_i = PJ[sel]
        t = np.take_along_axis(ts, sel[:, :, None, None], 3)[..., 0].astype(np.float64)   # (h,32,8)
        Ac = pal[A_i][:, :, None, :]; Bc = pal[B_i][:, :, None, :]
        num = np.zeros((16, 3)); den = np.zeros(16)
        # A role: weight (1-t)
        wa = (1 - t)
        na = wa[..., None] * (R - t[..., None] * Bc)
        np.add.at(num, np.broadcast_to(A_i[:, :, None], t.shape).ravel(), na.reshape(-1, 3))
        np.add.at(den, np.broadcast_to(A_i[:, :, None], t.shape).ravel(), (wa ** 2).ravel())
        nb = t[..., None] * (R - (1 - t[..., None]) * Ac)
        np.add.at(num, np.broadcast_to(B_i[:, :, None], t.shape).ravel(), nb.reshape(-1, 3))
        np.add.at(den, np.broadcast_to(B_i[:, :, None], t.shape).ravel(), (t ** 2).ravel())
        upd = den > 1e-6
        pal[upd] = num[upd] / den[upd, None]
        pal = snap(np.clip(pal, 0, 255))
        # recode with new palette (ideal-mix selection)
        cost, ts = row_costs(img, pal.astype(np.float32), 'segment')
        sel = cost.argmin(-1)
    return pal.astype(np.float32)


def code_image(img, variant, band=None):
    """returns output image (H,W,3) and palette(s)"""
    hb = band or H
    outs = []
    for y0 in range(0, H, hb):
        sub = img[y0:y0 + hb]
        pal = kmeans_palette(sub)
        mode = 'nearest' if variant['sel'] == 'nearest' else 'segment'
        cost, ts = row_costs(sub, pal, mode)
        sel = dp_pairs(cost, pal, variant.get('mu', 0))
        if variant.get('refine'):
            if mode == 'nearest':
                cost, ts = row_costs(sub, pal, 'segment')
                sel = dp_pairs(cost, pal, variant.get('mu', 0))
            pal = refine_palette(sub, pal, sel, ts, variant['refine'])
            cost, ts = row_costs(sub, pal, 'segment')
            sel = dp_pairs(cost, pal, variant.get('mu', 0))
            mode = 'segment'
        out, _ = render(sub, pal, sel, mode if variant.get('dither', mode == 'segment') else 'nearest', ts, y0)
        outs.append(out)
    return np.concatenate(outs, 0)


def metrics(src, out):
    mse = ((src - out) ** 2).mean()
    p = 10 * np.log10(255 ** 2 / mse)
    a = gaussian_filter(src, (1, 1, 0)); b = gaussian_filter(out, (1, 1, 0))
    pb = 10 * np.log10(255 ** 2 / ((a - b) ** 2).mean())
    e = (out - src).reshape(H, 32, 8, 3).mean(2)          # signed error of each 8-px row segment
    streak = np.abs(np.diff(e, axis=0)).mean()             # how much that error flips between neighbouring rows
    return p, pb, streak


VARIANTS = [
    ('A nearest (like egg ROM)', dict(sel='nearest')),
    ('B nearest + DP mu=8', dict(sel='nearest', mu=8)),
    ('C mix-select + dither', dict(sel='segment', dither=True)),
    ('D mix + dither + DP mu=8', dict(sel='segment', mu=8)),
    ('E D + palette refine', dict(sel='segment', mu=8, refine=4)),
    ('F E + 4 bands (48 lines)', dict(sel='segment', mu=8, refine=4), 48),
    ('G E + 8 bands (24 lines)', dict(sel='segment', mu=8, refine=4), 24),
    ('H E + 12 bands (16 lines)', dict(sel='segment', mu=8, refine=4), 16),
]

if __name__ == '__main__':
    fr = load_frames()
    ids = [int(x) for x in sys.argv[1:]] or [120, 260, 380]
    for fi in ids:
        src = fr[fi].astype(np.float32)
        tiles = [Image.fromarray(src.astype(np.uint8))]; names = ['source']
        print('frame', fi)
        for v in VARIANTS:
            t0 = time.time()
            out = code_image(src, v[1], v[2] if len(v) > 2 else None)
            p, pb, j = metrics(src, out)
            print(f'  {v[0]:34s} PSNR {p:5.2f}  blurred {pb:5.2f}  row-error flip {j:.2f}  [{time.time()-t0:.0f}s]', flush=True)
            tiles.append(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))); names.append(v[0])
        z = 2
        cols = 3; rows = (len(tiles) + cols - 1) // cols
        M = Image.new('RGB', (W * z * cols, H * z * rows))
        for i, (im, nm) in enumerate(zip(tiles, names)):
            im = im.resize((W * z, H * z), Image.NEAREST)
            d = ImageDraw.Draw(im); d.rectangle([0, 0, 260, 12], fill=(0, 0, 0)); d.text((2, 0), nm, fill=(255, 255, 255))
            M.paste(im, ((i % cols) * W * z, (i // cols) * H * z))
        M.save(HERE + f'/s4_cmp_{fi}.png')
