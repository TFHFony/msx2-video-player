"""Screen 4 image-quality lab: compares colour-pair selection / dithering / preprocessing variants on single frames
using REALISTIC palettes (one palette per ~3 s segment, trained on other frames of the segment, not on the test frame)."""
import os, sys, time
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageDraw
import screen4_sim as S
import encode4 as E
from screen4_sim import *

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = HERE + '/lab'
GAM = 2.2
CW = np.array([0.30, 0.55, 0.15], np.float32) * 3


def to_lin(v):
    return (np.clip(v, 0, 255) / 255.0) ** GAM


def to_gam(l):
    return np.clip(l, 0, 1) ** (1 / GAM) * 255.0


def load(name):
    return np.fromfile(f'{LAB}/f12_{name}.rgb', np.uint8).reshape(-1, 192, 256, 3)


# ---------------------------------------------------------------- palettes (segment palettes, cached)
SEG = 38


def seg_palette(k, srcname='d3', **kw):
    f = f'{LAB}/pal_{srcname}_seg{k}.npy'
    if os.path.exists(f) and not kw:
        return np.load(f)
    fr = load(srcname)[k * SEG:(k + 1) * SEG]
    pal = E.seg_palette(fr, None, **kw)
    if not kw:
        np.save(f, pal)
    return pal


# ---------------------------------------------------------------- coders
PAIRS = (PI, PJ)


def code_gamma(src, pal, kcon=0.05):
    """current encoder (error diffusion with mixing computed in gamma space)"""
    pat, col, out = E.code_fs_bytes(src, pal, kcon)
    return col, pat, out


def code_lin(src, pal, kcon=0.05, K=8, clampe=0.18, dist='gamma'):
    """error diffusion: colour mixing and error diffusion in LINEAR light, pair and pixel decisions judged in perceptual (gamma) space.
    returns (A_idx (h,32), B_idx (h,32), bits (h,32,8) bool, out image)"""
    h = src.shape[0]
    R = to_lin(src.reshape(h, 32, 8, 3).astype(np.float32))                  # linear 0..1
    Pl = to_lin(pal)                                                         # (16,3) linear
    Al, Bl = Pl[PI], Pl[PJ]
    ts = np.linspace(0, 1, K, dtype=np.float32)
    Mlin = Al[:, None, :] + ts[None, :, None] * (Bl - Al)[:, None, :]       # (136,K,3) mixes
    Mg = (np.clip(Mlin, 0, 1) ** (1 / GAM)) * 255.0
    contrast = (((np.clip(Al, 0, 1) ** (1 / GAM) - np.clip(Bl, 0, 1) ** (1 / GAM)) * 255.0) ** 2 * CW).sum(-1)
    Ag = pal[PI]; Bg = pal[PJ]
    out = np.zeros_like(R)
    A_idx = np.zeros((h, 32), np.int64); B_idx = np.zeros((h, 32), np.int64); bits = np.zeros((h, 32, 8), bool)
    err_next = np.zeros((32, 8, 3), np.float32)
    for r in range(h):
        cur = np.clip(R[r] + err_next, 0, 1)                                 # (32,8,3) linear
        cg = (cur ** (1 / GAM)) * 255.0
        # distance of each pixel to every mix sample of every pair; min over samples, sum over the 8 pixels
        d = (((cg[:, :, None, None, :] - Mg[None, None]) ** 2) * CW).sum(-1)  # (32,8,136,K)
        cost = d.min(-1).sum(1) + kcon * 8 * contrast                         # (32,136)
        sel = cost.argmin(-1)
        a = Al[sel]; b = Bl[sel]; ag = Ag[sel]; bg = Bg[sel]
        A_idx[r] = PI[sel]; B_idx[r] = PJ[sel]
        err_next[:] = 0
        e_row = np.zeros((32, 3), np.float32)
        for px in range(8):
            cc = cur[:, px] + e_row
            ccg = (np.clip(cc, 0, 1) ** (1 / GAM)) * 255.0
            dA = (((ccg - ag) ** 2) * CW).sum(-1); dB = (((ccg - bg) ** 2) * CW).sum(-1)
            pick = dB < dA
            o = np.where(pick[:, None], b, a)
            e = np.clip(cc - o, -clampe, clampe)
            out[r, :, px] = o
            bits[r, :, px] = pick
            e_row = e * 7 / 16
            err_next[:, px] += e * 5 / 16
            if px > 0: err_next[:, px - 1] += e * 3 / 16
            if px < 7: err_next[:, px + 1] += e * 1 / 16
    return A_idx, B_idx, bits, to_gam(out.reshape(h, W, 3))


def bytes_to_state(pat, col):
    """encode4-style (pat, col) bytes -> (A_idx, B_idx, bits)"""
    A = (col & 15).astype(np.int64); B = (col >> 4).astype(np.int64)
    bits = ((pat[:, :, None] >> (7 - np.arange(8))) & 1).astype(bool)
    return A, B, bits


def state_to_img(A, B, bits, pal):
    Pg = pal
    c = np.where(bits[..., None], Pg[B][:, :, None, :], Pg[A][:, :, None, :])
    return c.reshape(A.shape[0], W, 3)


# ---------------------------------------------------------------- direct binary search (vectorised on 9x9-spaced lattices)
def gauss_kernel(sig, rad):
    x = np.arange(-rad, rad + 1)
    g = np.exp(-(x[:, None] ** 2 + x[None] ** 2) / (2 * sig ** 2)); return g / g.sum()


def dbs(src, pal, A, B, bits, sig=1.0, passes=4, weight_pow=True):
    """flip pixels between the two colours of their row so that the blurred (linear light) error shrinks.
    perceptual weighting: error counted in gamma-compressed units (derivative of x^(1/2.2))."""
    h = src.shape[0]
    s = to_lin(src.astype(np.float32))
    Pl = to_lin(pal)
    bits = bits.copy()
    cur = np.where(bits[..., None], Pl[B][:, :, None, :], Pl[A][:, :, None, :]).reshape(h, W, 3)
    alt = np.where(bits[..., None], Pl[A][:, :, None, :], Pl[B][:, :, None, :]).reshape(h, W, 3)
    rad = 4
    g = gauss_kernel(sig, rad)
    g2 = np.zeros((2 * rad + 1, 2 * rad + 1))
    # autocorrelation of g (same as g convolved with g) truncated to 9x9 (sigma*sqrt2 gaussian)
    G2 = gauss_kernel(sig * np.sqrt(2), rad).astype(np.float32)
    g20 = float(G2[rad, rad])
    # f = G2 * (cur - s)
    d = cur - s
    f = np.stack([gaussian_filter(d[..., c], sig * np.sqrt(2), mode='nearest', truncate=rad / (sig * np.sqrt(2))) for c in range(3)], -1).astype(np.float32)
    Ls = (s * np.array([0.30, 0.59, 0.11], np.float32)).sum(-1)
    wp = ((Ls + 0.02) ** (2 * (1 / GAM - 1))).astype(np.float32) if weight_pow else np.ones_like(Ls)
    fpad = np.pad(f, ((rad, rad), (rad, rad), (0, 0)), mode='constant')
    changed_total = 0
    sp = 9
    for it in range(passes):
        changed = 0
        for i0 in range(sp):
            for j0 in range(sp):
                ys, xs = np.meshgrid(np.arange(i0, h, sp), np.arange(j0, W, sp), indexing='ij')
                ys = ys.ravel(); xs = xs.ravel()
                delta = alt[ys, xs] - cur[ys, xs]                        # (N,3)
                same = (np.abs(delta).sum(-1) < 1e-6)
                fp = fpad[ys + rad, xs + rad]
                dE = wp[ys, xs] * (CW * delta * (2 * fp + delta * g20)).sum(-1)
                acc = (dE < -1e-7) & ~same
                if not acc.any():
                    continue
                ya, xa = ys[acc], xs[acc]; da = delta[acc]
                # update state
                bits_row = bits[ya, xa // 8 * 0 + 0] if False else None
                tmp = cur[ya, xa].copy(); cur[ya, xa] = alt[ya, xa]; alt[ya, xa] = tmp
                tx = xa // 8; px = xa % 8
                bits[ya, tx, px] = ~bits[ya, tx, px]
                for dy in range(-rad, rad + 1):
                    for dx in range(-rad, rad + 1):
                        fpad[ya + rad + dy, xa + rad + dx] += da * G2[dy + rad, dx + rad]
                changed += int(acc.sum())
        changed_total += changed
        if changed < 20:
            break
    return bits


# ---------------------------------------------------------------- metrics
def ssim_luma(a, b):
    la = (a * np.array([0.299, 0.587, 0.114])).sum(-1); lb = (b * np.array([0.299, 0.587, 0.114])).sum(-1)
    c1 = (0.01 * 255) ** 2; c2 = (0.03 * 255) ** 2
    mu_a = gaussian_filter(la, 1.5); mu_b = gaussian_filter(lb, 1.5)
    saa = gaussian_filter(la * la, 1.5) - mu_a ** 2; sbb = gaussian_filter(lb * lb, 1.5) - mu_b ** 2; sab = gaussian_filter(la * lb, 1.5) - mu_a * mu_b
    s = ((2 * mu_a * mu_b + c1) * (2 * sab + c2)) / ((mu_a ** 2 + mu_b ** 2 + c1) * (saa + sbb + c2))
    return float(s.mean())


def metrics(ref, out):
    ref = ref.astype(np.float32); out = out.astype(np.float32)
    a = gaussian_filter(ref, (1, 1, 0)); b = gaussian_filter(out, (1, 1, 0))
    psnr_b = 10 * np.log10(255 ** 2 / ((a - b) ** 2).mean())
    la = gaussian_filter(to_lin(ref), (1.0, 1.0, 0)); lb = gaussian_filter(to_lin(out), (1.0, 1.0, 0))
    ga = to_gam(la); gb = to_gam(lb)
    psnr_l = 10 * np.log10(255 ** 2 / ((ga - gb) ** 2).mean())
    return psnr_b, psnr_l, ssim_luma(ref, out)


# ---------------------------------------------------------------- palette optimiser on the 512-colour grid
LEVELS = np.arange(8) * 255.0 / 7.0


def _mix_dist(px_g, a_lin, b_lin, K=6):
    """min over K samples of the weighted gamma-space distance from pixels (N,3 gamma) to the linear-light mix line a..b"""
    ts = np.linspace(0, 1, K, dtype=np.float32)
    m = a_lin[None, :] + ts[:, None] * (b_lin - a_lin)[None, :]                    # (K,3)
    mg = (np.clip(m, 0, 1) ** (1 / GAM)) * 255.0
    d = (((px_g[:, None, :] - mg[None]) ** 2) * CW).sum(-1)                         # (N,K)
    return d.min(1)


VERBOSE = True


def palette_local_search(frames, pal0, sweeps=3, npix=9000, seed=0, K=6, contrast_k=0.0, rad=1):
    rng = np.random.default_rng(seed)
    px = np.concatenate([f[::3, ::3].reshape(-1, 3) for f in frames]).astype(np.float32)
    px = px[rng.choice(len(px), min(npix, len(px)), replace=False)]
    pal = pal0.copy().astype(np.float32)
    pl = to_lin(pal)
    n = len(px)

    def pair_d(i, j, plin):
        return _mix_dist(px, plin[i], plin[j], K)
    # distance matrix for all 136 pairs
    D = np.stack([pair_d(i, j, pl) for i, j in PAIRS_L], 1)                          # (n,136)
    total = D.min(1).sum()
    for sw in range(sweeps):
        improved = 0
        for k in range(16):
            inv = [(a, b) for a, b in PAIRS_L if a == k or b == k]
            not_k = np.array([idx for idx, (a, b) in enumerate(PAIRS_L) if a != k and b != k])
            base = D[:, not_k].min(1)
            cur = np.minimum(base, D[:, [idx for idx, (a, b) in enumerate(PAIRS_L) if a == k or b == k]].min(1)).sum()
            best = (cur, pal[k].copy())
            lv = [int(round(v * 7 / 255)) for v in pal[k]]
            for dr in range(-rad, rad + 1):
                for dg in range(-rad, rad + 1):
                    for db in range(-rad, rad + 1):
                        if dr == dg == db == 0: continue
                        c = np.array([lv[0] + dr, lv[1] + dg, lv[2] + db])
                        if (c < 0).any() or (c > 7).any(): continue
                        cc = (c * 255.0 / 7.0).astype(np.float32); cl = to_lin(cc)
                        dk = np.stack([_mix_dist(px, cl, pl[j], K) for j in range(16)], 1)   # (n,16) incl. j==k as its own colour
                        cost = np.minimum(base, dk.min(1)).sum()
                        if cost < best[0] - 1e-6:
                            best = (cost, cc)
            if not np.allclose(best[1], pal[k]):
                pal[k] = best[1]; pl = to_lin(pal); improved += 1
                for idx, (a, b) in enumerate(PAIRS_L):
                    if a == k or b == k:
                        D[:, idx] = pair_d(a, b, pl)
        newtot = D.min(1).sum()
        if VERBOSE:
            print(f'    palette sweep {sw}: cost {total:.3g} -> {newtot:.3g} ({improved} colours moved)', flush=True)
        total = newtot
        if improved == 0: break
    return pal


PAIRS_L = [(i, j) for i in range(16) for j in range(i, 16)]


# ---------------------------------------------------------------- OKLab distance variant
_M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                [0.2119034982, 0.6806995451, 0.1073969566],
                [0.0883024619, 0.2817188376, 0.6299787005]], np.float32)
_M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                [1.9779984951, -2.4285922050, 0.4505937099],
                [0.0259040371, 0.7827717662, -0.8086757660]], np.float32)
OKW = np.array([1.0, 1.0, 1.0], np.float32)


def lin_to_oklab(l):
    lms = np.cbrt(np.clip(l, 0, 1) @ _M1.T)
    return lms @ _M2.T * 100.0                       # scaled so distances are comparable in magnitude


def code_lin_ok(src, pal, kcon=0.05, K=8, clampe=0.18, lw=1.0):
    """like code_lin but all decisions judged by OKLab distance (L weighted by lw)"""
    h = src.shape[0]
    R = to_lin(src.reshape(h, 32, 8, 3).astype(np.float32))
    Pl = to_lin(pal)
    Al, Bl = Pl[PI], Pl[PJ]
    ts = np.linspace(0, 1, K, dtype=np.float32)
    Mlin = Al[:, None, :] + ts[None, :, None] * (Bl - Al)[:, None, :]
    Mo = lin_to_oklab(Mlin)                                                   # (136,K,3)
    W3 = np.array([lw, 1.0, 1.0], np.float32)
    oa = lin_to_oklab(Al); ob = lin_to_oklab(Bl)
    contrast = (((oa - ob) ** 2) * W3).sum(-1)
    Oa_all = lin_to_oklab(Pl)
    out = np.zeros_like(R)
    A_idx = np.zeros((h, 32), np.int64); B_idx = np.zeros((h, 32), np.int64); bits = np.zeros((h, 32, 8), bool)
    err_next = np.zeros((32, 8, 3), np.float32)
    for r in range(h):
        cur = np.clip(R[r] + err_next, 0, 1)
        co = lin_to_oklab(cur)
        d = (((co[:, :, None, None, :] - Mo[None, None]) ** 2) * W3).sum(-1)
        cost = d.min(-1).sum(1) + kcon * 8 * contrast
        sel = cost.argmin(-1)
        a = Al[sel]; b = Bl[sel]; oas = oa[sel]; obs = ob[sel]
        A_idx[r] = PI[sel]; B_idx[r] = PJ[sel]
        err_next[:] = 0
        e_row = np.zeros((32, 3), np.float32)
        for px in range(8):
            cc = cur[:, px] + e_row
            cco = lin_to_oklab(cc)
            dA = (((cco - oas) ** 2) * W3).sum(-1); dB = (((cco - obs) ** 2) * W3).sum(-1)
            pick = dB < dA
            o = np.where(pick[:, None], b, a)
            e = np.clip(cc - o, -clampe, clampe)
            out[r, :, px] = o
            bits[r, :, px] = pick
            e_row = e * 7 / 16
            err_next[:, px] += e * 5 / 16
            if px > 0: err_next[:, px - 1] += e * 3 / 16
            if px < 7: err_next[:, px + 1] += e * 1 / 16
    return A_idx, B_idx, bits, to_gam(out.reshape(h, W, 3))
