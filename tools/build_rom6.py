#!/usr/bin/env python
"""Build a NEO16 ROM for player6 (video + 1200 SCC samples per frame).
usage: build_rom6.py stream.bin audio_s16le_mono.raw out.rom
bank 0 = player; bank n (n>=1) = frame n-1:
  4000h flags, 4001h palette(32), 4040h 1280 samples (signed 8 bit), 4600h patterns 6144+6 spill, colours 6144+6 spill"""
import os, struct, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SPF = 1200
PART = 6150


def find_sjasmplus():
    import glob, shutil
    env = os.environ.get('SJASMPLUS')
    if env and os.path.exists(env):
        return env
    for pat in (HERE + '/sjasmplus/**/sjasmplus.exe', HERE + '/sjasmplus/**/sjasmplus', HERE + '/../../.claude/msx-video-tools/sjasmplus/**/sjasmplus.exe'):
        g = glob.glob(pat, recursive=True)
        if g:
            return g[0]
    w = shutil.which('sjasmplus')
    if w:
        return w
    sys.exit('sjasmplus not found')


def main():
    stream = open(sys.argv[1], 'rb').read()
    nfr = int(open(sys.argv[1] + '.meta').read())
    aud = np.fromfile(sys.argv[2], '<i2').astype(np.float64)
    out = sys.argv[3]
    gain = float(os.environ.get('GAIN', '0'))
    if gain <= 0:
        gain = 0.97 * 127.0 / max(1.0, np.abs(aud).max() / 256.0 * 256.0 / 256.0) / 256.0 * 256.0
        gain = 0.97 * 32767.0 / max(1.0, np.abs(aud).max())
    rng = np.random.default_rng(1)
    s8 = np.clip(np.rint(aud * gain / 256.0 + (rng.random(len(aud)) - rng.random(len(aud))) * 0.5), -128, 127).astype(np.int8)
    need = nfr * SPF
    if len(s8) < need:
        s8 = np.concatenate([s8, np.zeros(need - len(s8), np.int8)])
    r = subprocess.run([find_sjasmplus(), '--nologo', 'player6.asm'], cwd=HERE + '/player6', capture_output=True, text=True)
    print(r.stdout, r.stderr)
    assert r.returncode == 0
    boot = bytearray(open(HERE + '/player6/player6.bin', 'rb').read())
    assert len(boot) == 0x4000
    p = 0
    banks = []
    pal0 = None
    for n in range(nfr):
        flags = stream[p]; p += 1
        pal = b'\0' * 32
        if flags & 1:
            pal = stream[p:p + 32]; p += 32
            if pal0 is None:
                pal0 = pal
        pat = stream[p:p + 6144]; col = stream[p + 6144:p + 12288]; p += 12288
        b = bytearray(0x4000)
        b[0] = flags & 1
        b[1:33] = pal
        b[0x40:0x40 + SPF] = s8[n * SPF:(n + 1) * SPF].tobytes()
        b[0x600:0x600 + 6144] = pat
        b[0x600 + PART:0x600 + PART + 6144] = col
        banks.append(bytes(b))
    assert p == len(stream), (p, len(stream))
    struct.pack_into('<H', boot, 0x20, nfr)
    lum = [0.3 * (pal0[2 * i] >> 4) + 0.55 * pal0[2 * i + 1] + 0.15 * (pal0[2 * i] & 15) for i in range(16)]
    boot[0x22] = int(np.argmin(lum))
    boot[0x23:0x43] = pal0
    rom = bytes(boot) + b''.join(banks)
    open(out, 'wb').write(rom)
    print(f'ROM {out}: {len(rom)} bytes, {len(rom) // 0x4000} banks, {nfr} frames, audio gain {gain:.3f}')


if __name__ == '__main__':
    main()
