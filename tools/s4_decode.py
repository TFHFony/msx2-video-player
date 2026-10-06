"""Decode an encode4 stream (frame header + optional palette + 12288 bytes) -> list of (rgb image)"""
import numpy as np
import encode4 as E

def parse(fb):
    p = 0; frames = []; pal = None
    while p < len(fb):
        fl = fb[p]; p += 1
        if fl & 1:
            raw = fb[p:p + 32]; p += 32
            pal = np.array([[ (raw[2*i] >> 4) * 255 / 7, (raw[2*i+1] & 7) * 255 / 7, (raw[2*i] & 7) * 255 / 7] for i in range(16)], np.float32)
        d = np.frombuffer(fb[p:p + 12288], np.uint8); p += 12288
        frames.append((d, pal.copy()))
    return frames

def to_image(d, pal):
    P = d[:6144].reshape(3, 256, 8); C = d[6144:].reshape(3, 256, 8)
    pat = np.zeros((192, 32), np.uint8); col = np.zeros((192, 32), np.uint8)
    for t in range(3):
        for n in range(256):
            r, c = divmod(n, 32)
            pat[(t*8+r)*8:(t*8+r)*8+8, c] = P[t, n]; col[(t*8+r)*8:(t*8+r)*8+8, c] = C[t, n]
    return E.render_bytes(pat, col, pal)
