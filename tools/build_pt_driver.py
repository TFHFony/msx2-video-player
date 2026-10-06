#!/usr/bin/env python
"""Regenerate the PRO-TRACKER (Tyfoon Software 1991) music driver files in tools/music/ from the original source PT_DRIVE.ASC
(the converted driver is already included in the repository, this script is only needed to rebuild it). It
  * converts the MSX-assembler syntax (&H.., &B..) to sjasmplus syntax,
  * removes the disk loader (the song comes from the ROM instead),
  * assembles it (ORG CA00h) to  music/pt_drive.bin,
  * writes the addresses the player needs to  music/pt_syms.inc.

Usage:  python build_pt_driver.py PT_DRIVE.ASC
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_sjasmplus():
    import glob, shutil
    env = os.environ.get('SJASMPLUS')
    if env and os.path.exists(env):
        return env
    for pat in (HERE + '/sjasmplus/**/sjasmplus.exe', HERE + '/sjasmplus/**/sjasmplus'):
        g = glob.glob(pat, recursive=True)
        if g:
            return g[0]
    w = shutil.which('sjasmplus')
    if w:
        return w
    sys.exit('sjasmplus not found: put it on the PATH, set SJASMPLUS, or unpack a release into tools/sjasmplus/')


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    s = open(sys.argv[1], encoding='latin-1').read()
    s = re.sub(r'&H([0-9A-Fa-f]+)', lambda m: '0x' + m.group(1), s)
    s = re.sub(r'&B([01]+)', lambda m: '0b' + m.group(1), s)
    a = s.index('L00012: LD    DE,DMAADR')
    b = s.index(';----------------------------------------------\nL00029:')
    s = s[:a] + 'L00012: RET\n\n' + s[b:]
    c = s.index(';--------------------------------------------------\n; FCB voor LOADER')
    s = s[:c] + '        SAVEBIN "pt_drive.bin",0xCA00,$-0xCA00\n'
    s = s.replace('        ORG   0xCA00', '        DEVICE NOSLOT64K\n        ORG   0xCA00', 1)
    outdir = os.path.join(HERE, 'music')
    os.makedirs(outdir, exist_ok=True)
    asm = os.path.join(outdir, 'pt_drive_noloader.asm')
    open(asm, 'w').write(s)
    r = subprocess.run([find_sjasmplus(), '--nologo', '--sym=pt.sym', 'pt_drive_noloader.asm'], cwd=outdir, capture_output=True, text=True)
    print(r.stdout + r.stderr)
    if r.returncode != 0:
        sys.exit('assembly failed')
    sym = open(os.path.join(outdir, 'pt.sym')).read()

    def addr(n):
        return int(re.search(n + r': EQU 0x([0-9A-F]+)', sym).group(1), 16)
    open(os.path.join(outdir, 'pt_syms.inc'), 'w').write(
        f"DRV_INIT equ 0xCA00\nDRV_STOP equ 0xCA03\nDRV_SWITCH equ 0x{addr('L00017'):04X}\nDRV_RESTORE equ 0x{addr('L00027'):04X}\n")
    print('wrote music/pt_drive.bin and music/pt_syms.inc')


if __name__ == '__main__':
    main()
