"""Assemble player, patch metadata, append stream -> NEO8 ROM image."""
import subprocess, sys, os, struct, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
stream_path = sys.argv[1] if len(sys.argv) > 1 else HERE + '/stream.bin'
out = sys.argv[2] if len(sys.argv) > 2 else HERE + '/video.rom'
def _find_sjasmplus():
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


asm = _find_sjasmplus()
defs = ['-DSAFE'] if os.environ.get('SAFE') else []
PD = os.environ.get('PLAYER', 'player')
r = subprocess.run([asm, '--nologo'] + defs + [PD + '.asm'], cwd=HERE + '/' + PD, capture_output=True, text=True)
print(r.stdout, r.stderr)
assert r.returncode == 0
rom = bytearray(open(HERE + '/' + PD + '/' + PD + '.bin', 'rb').read())
assert len(rom) == 0x4000
pal = np.load(stream_path + '.pal.npy') if os.path.exists(stream_path + '.pal.npy') else np.load(HERE + '/pal_final.npy')
pal = np.rint(pal * 7 / 255).astype(int) if pal.max() > 7 else pal
for i in range(16):
    r_, g_, b_ = pal[i] if i < len(pal) else (0, 0, 0)
    rom[0x20 + 2 * i] = (int(r_) << 4) | int(b_)
    rom[0x21 + 2 * i] = int(g_)
nfr = int(open(stream_path + '.meta').read())
struct.pack_into('<H', rom, 0x40, nfr)
rom[0x42] = int(os.environ.get('FT50', '5')); rom[0x43] = int(os.environ.get('FT60', '6'))
lum = [(0.3*c[0]+0.55*c[1]+0.15*c[2]) for c in pal]
rom[0x44] = int(np.argmin(lum))
rom[0x45] = 1 if os.environ.get('NOPACE') else 0
rom[0x46] = int(os.environ.get('DBG','0'))
song_path = os.environ.get('SONG')
if song_path:
    song = open(song_path, 'rb').read()
    assert len(song) <= 0x2000
    struct.pack_into('<H', rom, 0x46, len(song))
    rom += song + bytes([0xFF]) * (0x2000 - len(song))
data = open(stream_path, 'rb').read()
rom += data
while len(rom) % 0x2000: rom.append(0xFF)
open(out, 'wb').write(rom)
print(f'ROM {out}: {len(rom)} bytes, {len(rom)//8192} segments, frames {nfr}')
