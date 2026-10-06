"""Error-diffusion coding of Screen 4 rows + evaluation over several frames."""
import sys, os, time
import numpy as np
import screen4_sim as S
from screen4_sim import *

def code_fs(img, pal, kcon, clampe=48.0, mu=0.0):
    h = img.shape[0]
    R = img.reshape(h, 32, 8, 3).astype(np.float32)
    A_all, B_all = pal[PI], pal[PJ]                      # (136,3)
    V = B_all - A_all
    den = (V * V * WTS).sum(-1); den = np.where(den == 0, 1, den)
    contrast = (V * V * WTS).sum(-1)
    out = np.zeros_like(R)
    err_next = np.zeros((32, 8, 3), np.float32)
    prev_sel = None
    T = (pair_dist_matrix(pal).astype(np.float32) * mu) if mu > 0 else None
    for r in range(h):
        cur = np.clip(R[r] + err_next, 0, 255)           # (32,8,3)
        c = cur[:, :, None, :]
        t = np.clip((((c - A_all) * V * WTS).sum(-1)) / den, 0, 1)      # (32,8,136)
        m = A_all + t[..., None] * V
        cost = ((((c - m) ** 2) * WTS).sum(-1)).sum(1) + kcon * 8 * contrast     # (32,136)
        if T is not None and prev_sel is not None:
            cost = cost + T[prev_sel]
        sel = cost.argmin(-1); prev_sel = sel
        A = pal[PI[sel]]; B = pal[PJ[sel]]                # (32,3)
        err_next[:] = 0
        e_row = np.zeros((32, 3), np.float32)
        for px in range(8):
            cc = cur[:, px] + e_row
            dA = (((cc - A) ** 2) * WTS).sum(-1); dB = (((cc - B) ** 2) * WTS).sum(-1)
            o = np.where((dB < dA)[:, None], B, A)
            e = np.clip(cc - o, -clampe, clampe)
            out[r, :, px] = o
            e_row = e * 7 / 16
            err_next[:, px] += e * 5 / 16
            if px > 0: err_next[:, px - 1] += e * 3 / 16
            if px < 7: err_next[:, px + 1] += e * 1 / 16
    return out.reshape(h, W, 3)

def refine_float(img, pal, sel, ts, iters=3):
    h = img.shape[0]
    R = img.reshape(h, 32, 8, 3).astype(np.float64)
    pal = pal.astype(np.float64).copy()
    for _ in range(iters):
        A_i = PI[sel]; B_i = PJ[sel]
        t = np.take_along_axis(ts, sel[:, :, None, None], 3)[..., 0].astype(np.float64)
        Ac = pal[A_i][:, :, None, :]; Bc = pal[B_i][:, :, None, :]
        num = np.zeros((16, 3)); den = np.zeros(16)
        ia = np.broadcast_to(A_i[:, :, None], t.shape).ravel(); ib = np.broadcast_to(B_i[:, :, None], t.shape).ravel()
        wa = 1 - t
        np.add.at(num, ia, (wa[..., None] * (R - t[..., None] * Bc)).reshape(-1, 3)); np.add.at(den, ia, (wa ** 2).ravel())
        np.add.at(num, ib, (t[..., None] * (R - wa[..., None] * Ac)).reshape(-1, 3)); np.add.at(den, ib, (t ** 2).ravel())
        upd = den > 1e-3
        pal[upd] = np.clip(num[upd] / den[upd, None], 0, 255)
        cost, ts = row_costs(img, pal.astype(np.float32), 'segment')
        sel = cost.argmin(-1)
    return snap(pal).astype(np.float32)

def code_variant(img, name):
    hb = {'bands48': 48, 'bands24': 24}.get(name.split('+')[-1], None)
    parts = []
    for y0 in range(0, H, hb or H):
        sub = img[y0:y0 + (hb or H)]
        pal = kmeans_palette(sub)
        if name.startswith('nearest'):
            cost, ts = row_costs(sub, pal, 'nearest'); sel = cost.argmin(-1)
            out, _ = render(sub, pal, sel, 'nearest', ts)
        elif name.startswith('ordered'):
            cost, ts = row_costs(sub, pal, 'segment'); sel = cost.argmin(-1)
            if 'refine' in name:
                pal = refine_float(sub, pal, sel, ts); cost, ts = row_costs(sub, pal, 'segment'); sel = cost.argmin(-1)
            out, _ = render(sub, pal, sel, 'segment', ts, y0)
        else:  # fs
            if 'refine' in name:
                cost, ts = row_costs(sub, pal, 'segment'); sel = cost.argmin(-1)
                pal = refine_float(sub, pal, sel, ts)
            mu = 2.0 if 'mu' in name else 0.0
            out = code_fs(sub, pal, S.KCON, mu=mu)
        parts.append(out)
    return np.concatenate(parts, 0)

if __name__ == '__main__':
    fr = load_frames()
    ids = [60, 120, 180, 260, 320, 380, 440]
    names = ['nearest', 'ordered', 'ordered+refine', 'fs', 'fs+refine', 'fs+mu', 'fs+refine+bands48', 'fs+refine+bands24']
    res = {n: [] for n in names}
    for fi in ids:
        src = fr[fi].astype(np.float32)
        for n in names:
            out = code_variant(src, n)
            res[n].append(metrics(src, out))
        print('frame', fi, 'done', flush=True)
    print('variant                 PSNR   blurredPSNR   row-error-flip')
    for n in names:
        a = np.mean(res[n], 0); print(f'{n:22s} {a[0]:6.2f} {a[1]:8.2f} {a[2]:12.2f}')
