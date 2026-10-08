#!/usr/bin/env python
"""Audio for player6 with the per-frame pause compensated.
The player plays SPF samples per video frame, then pauses (flip, bank switch, retrace wait) for GAP seconds.  Playing
the source contiguously would shift the waveform by GAP every frame (a click at the frame rate, worst on low tones).
Instead sample i of frame k is taken from the source at time  k/FPS + i/R  with R = SPF / (1/FPS - GAP),  so the
slice that falls into the pause is skipped and the waveform stays continuous in time.
usage: make_audio6.py video start_seconds duration_seconds out.raw  [--fps 12] [--spf 1200] [--gap-ms 0.85]"""
import argparse, os, subprocess, sys
import numpy as np
from scipy.signal import firwin, filtfilt
from scipy.interpolate import CubicSpline

ap = argparse.ArgumentParser()
ap.add_argument('video'); ap.add_argument('start', type=float); ap.add_argument('duration', type=float); ap.add_argument('out')
ap.add_argument('--fps', type=float, default=12.0); ap.add_argument('--spf', type=int, default=1200)
ap.add_argument('--gap-ms', type=float, default=0.85)
ap.add_argument('--rate', type=float, default=0, help='playback rate in Hz (default derived from --gap-ms)')
ap.add_argument('--glide', type=int, default=0, help='cross-fade the first N samples of every frame from the value the player is holding after the pause (0 = off)')
ap.add_argument('--glide-n', type=int, default=10, help='typical number of extra samples the player plays while waiting for the retrace')
ap.add_argument('--store', type=int, default=0, help='samples stored per frame (default = spf; the player may play more of them while it waits for the retrace)')
a = ap.parse_args()
ff = os.environ.get('FFMPEG')
if not ff:
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg_path.txt')
    ff = open(p).read().strip() if os.path.exists(p) else 'ffmpeg'
cmd = [ff, '-v', 'error', '-ss', str(a.start), '-i', a.video]
if a.duration > 0: cmd += ['-t', str(a.duration)]
cmd += ['-vn', '-af', 'pan=mono|c0=0.5*c0+0.5*c1', '-ar', '48000', '-f', 's16le', '-ac', '1', '-']
x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, '<i2').astype(np.float64)
R = a.rate if a.rate > 0 else a.spf / (1.0 / a.fps - a.gap_ms / 1000.0)
ST = a.store if a.store > 0 else a.spf
print(f'playback rate R = {R:.1f} Hz, source {len(x) / 48000:.2f} s')
x = filtfilt(firwin(401, 0.43 * R, fs=48000), [1.0], x)      # band-limit below the playback Nyquist
nfr = int(len(x) / 48000 * a.fps)
out = np.zeros(nfr * ST)
for k in range(nfr):
    t0 = k / a.fps
    i0 = max(0, int((t0 - 0.004) * 48000)); i1 = min(len(x), int((t0 + ST / R + 0.004) * 48000))
    cs = CubicSpline(np.arange(i0, i1) / 48000.0, x[i0:i1])
    t = np.minimum(t0 + np.arange(ST) / R, (i1 - 1) / 48000.0)
    out[k * ST:(k + 1) * ST] = cs(t)
if a.glide > 0:
    fr = out.reshape(nfr, ST)
    for k in range(nfr - 1, 0, -1):          # the held value is the last sample played of the previous frame
        held = fr[k - 1, a.spf + a.glide_n - 1]
        w = (np.arange(a.glide) + 1.0) / (a.glide + 1.0)
        fr[k, :a.glide] = (1.0 - w) * held + w * fr[k, :a.glide]
    out = fr.reshape(-1)
peak = np.abs(out).max()
print(f'peak after band-limiting/interpolation: {peak:.0f} ({(np.abs(out) > 32767).sum()} samples above full scale)')
out *= min(1.0, 30000.0 / peak)          # never clip: overshoot of the band-limited signal would crackle
np.rint(out).astype('<i2').tofile(a.out)
print(f'{nfr} frames x {ST} samples = {len(out)} samples -> {a.out}')
