#!/usr/bin/env python
"""Build a NEO16 ROM for player6 (video + 1200 SCC samples per frame).
usage: build_rom6.py stream.bin audio_s16le_mono.raw out.rom
bank 0 = player; bank n (n>=1) = frame n-1:
  4000h flags, 4001h palette(32), 4040h 1280 samples (signed 8 bit), 4600h patterns 6144+6 spill, colours 6144+6 spill"""
import os, struct, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))


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

VARIANTS = {
    # name: samples/frame, OUTI per slot (4 slots), fixed pads (PAL, NTSC) or None, adaptive start levels, no frequency write
    'base':   dict(spf=1200, k=[10, 10, 10, 11], pads=([1, 0, 1, 0], [3, 2, 3, 2]), adapt=None, nofreq=False),
    's1152':  dict(spf=1152, k=[10, 11, 11, 11], pads=([0, 0, 0, 0], [3, 2, 3, 2]), adapt=None, nofreq=False),
    'adapt':  dict(spf=1200, k=[10, 10, 10, 11], pads=None, adapt=(3, 8), nofreq=False),
    'tail':   dict(spf=1200, k=[10, 10, 10, 11], pads=None, adapt=(3, 8), nofreq=False, tail=True, astore=1472),
    'hw1280': dict(spf=1280, k=[10, 10, 10, 9], pads=None, adapt=(11, 16), nofreq=True),
}
NLEV = 28


def group_text(k, pads, nofreq):
    out = []
    for n, p in zip(k, pads):
        out += ['        ld a,(de)', '        inc de', '        ld (0x9800),a']
        if not nofreq:
            out.append('        ld (0x9880),a')
        out += ['        outi'] * n + ['        nop'] * p
    return out


def make_includes(v):
    spf = v['spf']; k = v['k']
    groups = spf // 8
    ksum = sum(k)
    part = groups * ksum
    b0 = part % 256
    for i in range(1, groups):
        assert (b0 - i * ksum) % 256 != 0, 'B counter would hit zero early'
    L = [f'B0 equ {b0}', f'PERIODHI equ {0 if v["nofreq"] else 15}']
    if v['adapt']:
        L += [f'NLEV equ {NLEV}', f'LEVP equ {v["adapt"][0]}', f'LEVN equ {v["adapt"][1]}']
        for lev in range(NLEV):
            pads = [(lev + 3) // 4, (lev + 2) // 4, (lev + 1) // 4, lev // 4]
            L.append(f'lad{lev}:')
            L += group_text(k, pads, v['nofreq'])
            L += [f'        jp nz,lad{lev}', '        ret']
        L.append('ladderP equ lad0')
        if v.get('tail'):
            for lev in range(NLEV):
                ts = 230.25 + 1.25 * lev
                want = ts - 80
                best = min(((abs(14 * n + 3 + 5 * m - want), n, m) for n in range(1, 40) for m in range(3)))
                _, n, m = best
                L += [f'tl{lev}:', '        ld a,(de)', '        inc de', '        ld (0x9800),a']
                if not v['nofreq']:
                    L.append('        ld (0x9880),a')
                L += ['        in a,(0x99)', '        and 0x40', '        ret nz', f'        ld b,{n}', f'        djnz $'] + ['        nop'] * m + [f'        jp tl{lev}']
            L.append('tltab:')
            L += [f'        dw tl{lev}' for lev in range(NLEV)]
        L.append('ladtab:')
        L += [f'        dw lad{lev}' for lev in range(NLEV)]
    else:
        for name, pads in zip(('ladderP', 'ladderN'), v['pads']):
            L.append(f'{name}:')
            L += group_text(k, pads, v['nofreq'])
            L += [f'        jp nz,{name}', '        ret']
    return chr(10).join(L) + chr(10), spf, part


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
    variant = os.environ.get('VARIANT', 'base')
    v = VARIANTS[variant]
    inc, SPF, PART = make_includes(v)
    open(HERE + '/player6/ladders.inc', 'w').write(inc)
    AST = v.get('astore', SPF)
    need = nfr * AST
    if len(s8) < need:
        s8 = np.concatenate([s8, np.zeros(need - len(s8), np.int8)])
    r = subprocess.run([find_sjasmplus(), '--nologo'] + (['-DADAPT'] if v['adapt'] else []) + (['-DTAIL'] if v.get('tail') else []) + ['player6.asm'], cwd=HERE + '/player6', capture_output=True, text=True)
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
        b[0x40:0x40 + AST] = s8[n * AST:(n + 1) * AST].tobytes()
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
    print(f'variant {variant}: {SPF} samples/frame, part {PART} bytes')
    print(f'ROM {out}: {len(rom)} bytes, {len(rom) // 0x4000} banks, {nfr} frames, audio gain {gain:.3f}')


if __name__ == '__main__':
    main()
