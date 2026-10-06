#!/usr/bin/env python
"""
make_rom.py - turn a video clip (+ a ProTracker song) into an MSX2 NEO8 ROM, "Full Refresh" version.

  * Screen 4 (GRAPHIC 3), 256x192, 16-colour palette (refined per ~3 s segment), 2 colours per 8x1 row, error diffused
  * every frame rewrites all 768 tiles into a hidden table set that is flipped at vblank (no tearing, no stale tiles)
  * optional MSX-Music background music with the PT_DRIVE ProTracker driver (song loops by itself)

Usage examples
  python make_rom.py myclip.mp4 mysong.pro
  python make_rom.py myclip.mp4 mysong.pro --fps 10 --out party.rom
  python make_rom.py myclip.mp4 --no-music --start 12 --duration 60
  python make_rom.py myclip.mp4 mysong.pro --fit letterbox        (keep the full 16:9 picture with black bars)
  python make_rom.py myclip.mp4 mysong.pro --crop-x 0.3           (move the 4:3 crop window to the left)

Needs: Python 3 with numpy, scipy, pillow; ffmpeg (PATH or FFMPEG=...); sjasmplus (PATH, SJASMPLUS=..., or tools/sjasmplus/);
for music: run once  python tools/build_pt_driver.py PT_DRIVE.ASC  (the driver itself is not in the repository).
Run in openMSX:  openmsx -machine Philips_NMS_8250 -ext fmpac -cart out.rom -romtype NEO-8     (ESC quits)
"""
import argparse, math, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, 'tools')


def die(msg):
    print('ERROR: ' + msg)
    sys.exit(1)


def find_ffmpeg():
    if os.environ.get('FFMPEG') and os.path.exists(os.environ['FFMPEG']):
        return os.environ['FFMPEG']
    p = os.path.join(TOOLS, 'ffmpeg_path.txt')
    if os.path.exists(p):
        f = open(p).read().strip()
        if os.path.exists(f):
            return f
    f = shutil.which('ffmpeg')
    if f:
        return f
    die('ffmpeg not found. Install it (e.g. "winget install Gyan.FFmpeg") or put its full path in ' + p)


def run(cmd, env=None, cwd=None, label=''):
    e = dict(os.environ)
    if env:
        e.update({k: str(v) for k, v in env.items()})
    r = subprocess.run(cmd, env=e, cwd=cwd)
    if r.returncode != 0:
        die(f'{label or cmd[0]} failed (exit code {r.returncode})')


def main():
    ap = argparse.ArgumentParser(description='Video clip (+ song) -> MSX2 NEO8 ROM (Screen 4 full refresh)',
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument('video', help='input video (anything ffmpeg can read)')
    ap.add_argument('song', nargs='?', help='ProTracker song (.pro / .PRO, max 8 KB); omit together with --no-music')
    ap.add_argument('--out', help='output ROM (default: <video name>.rom next to the video)')
    ap.add_argument('--no-music', action='store_true', help='build a ROM without music')
    ap.add_argument('--fps', type=float, default=12.0, help='frame rate (6..12.5, default 12). 50 Hz machines run at 50/round(50/fps), 60 Hz at 60/round(60/fps)')
    ap.add_argument('--fit', choices=['crop', 'letterbox', 'stretch'], default='crop',
                    help='how a 16:9 picture is fitted to the 4:3 screen: crop (default), letterbox (black bars) or stretch')
    ap.add_argument('--crop-x', type=float, default=0.5, help='horizontal position of the crop window 0..1 (0.5 = centre)')
    ap.add_argument('--start', type=float, default=0.0, help='start time in seconds')
    ap.add_argument('--duration', type=float, default=0.0, help='duration in seconds (0 = whole clip)')
    ap.add_argument('--denoise', default='3:3:8:6', help='ffmpeg hqdn3d strength (default 3:3:8:6, "off" to disable)')
    ap.add_argument('--segment-seconds', type=float, default=3.2, help='seconds per palette segment (default 3.2)')
    ap.add_argument('--kcon', type=float, default=0.05, help='penalty for high-contrast colour pairs (default 0.05)')
    ap.add_argument('--hyst', type=float, default=0.25, help='temporal stability: keep the previous tile if it is nearly as good (default 0.25, 0 = off)')
    ap.add_argument('--safe', action='store_true', help='spaced VDP writes (slower player, ~98 ms/frame with music: only for ~8 fps)')
    ap.add_argument('--work', help='working folder (default: make_rom_work/<name>)')
    ap.add_argument('--keep-frames', action='store_true', help='keep the extracted raw frames (large) in the working folder')
    a = ap.parse_args()

    # ---------------------------------------------------------------- checks
    for mod in ('numpy', 'scipy', 'PIL'):
        try:
            __import__(mod)
        except ImportError:
            die(f'Python module "{mod}" is missing: pip install numpy scipy pillow')
    if not os.path.isdir(TOOLS):
        die('tools folder not found: ' + TOOLS)
    video = os.path.abspath(a.video)
    if not os.path.exists(video):
        die('video not found: ' + video)
    if a.no_music:
        song = None
    else:
        if not a.song:
            die('no song given (give a .pro file, or use --no-music)')
        song = os.path.abspath(a.song)
        if not os.path.exists(song):
            die('song not found: ' + song)
        for f in ('pt_drive.bin', 'pt_syms.inc'):
            if not os.path.exists(os.path.join(TOOLS, 'music', f)):
                die('music driver not prepared (tools/music/%s missing). Run once:  python tools/build_pt_driver.py PT_DRIVE.ASC' % f)
        sd = open(song, 'rb').read()
        if len(sd) > 0x2000:
            die(f'song is {len(sd)} bytes; the ROM has room for 8192')
        if not sd.startswith(b'PT10MOD'):
            print('WARNING: the song does not start with "PT10MOD" - is it a ProTracker file?')
    ticks50 = int(round(50.0 / a.fps)); ticks60 = int(round(60.0 / a.fps))
    min50, min60 = (4, 5)
    if ticks50 < min50 or ticks60 < min60:
        die(f'--fps {a.fps} is too high for a full refresh (needs >= {min50} ticks at 50 Hz and >= {min60} at 60 Hz, i.e. at most 12.5 fps)')
    fps50 = 50.0 / ticks50; fps60 = 60.0 / ticks60
    fps_src = a.fps
    out = os.path.abspath(a.out) if a.out else os.path.splitext(video)[0] + '.rom'
    name = os.path.splitext(os.path.basename(out))[0]
    work = os.path.abspath(a.work) if a.work else os.path.join(HERE, 'make_rom_work', name)
    os.makedirs(work, exist_ok=True)
    ffmpeg = find_ffmpeg()
    seg = max(8, int(round(a.segment_seconds * fps_src)))

    print('=' * 70)
    print(f'video      : {video}')
    print(f'song       : {song or "(none)"}')
    print(f'output     : {out}')
    print(f'frame rate : source frames at {fps_src:g} fps; plays at {fps50:.2f} fps on 50 Hz and {fps60:.2f} fps on 60 Hz '
          f'({abs(fps50 / fps60 - 1) * 100:.0f}% apart)')
    print(f'palette    : new 16-colour palette every {seg} frames')
    print('=' * 70)

    # ---------------------------------------------------------------- 1. frames
    frames = os.path.join(work, 'frames_256x192.rgb')
    if a.fit == 'crop':
        vf = f"crop=w='min(iw,ih*4/3)':h='min(ih,iw*3/4)':x='(iw-out_w)*{a.crop_x}':y='(ih-out_h)/2',scale=256:192:flags=area"
    elif a.fit == 'letterbox':
        vf = 'scale=256:192:force_original_aspect_ratio=decrease:flags=area,pad=256:192:(ow-iw)/2:(oh-ih)/2:black'
    else:
        vf = 'scale=256:192:flags=area'
    if a.denoise.lower() != 'off':
        vf += f',hqdn3d={a.denoise}'
    vf += f',fps={fps_src:g}'
    cmd = [ffmpeg, '-v', 'error', '-y']
    if a.start > 0:
        cmd += ['-ss', str(a.start)]
    cmd += ['-i', video]
    if a.duration > 0:
        cmd += ['-t', str(a.duration)]
    cmd += ['-an', '-vf', vf, '-pix_fmt', 'rgb24', '-f', 'rawvideo', frames]
    print('[1/3] extracting frames with ffmpeg ...')
    t0 = time.time()
    run(cmd, label='ffmpeg')
    nframes = os.path.getsize(frames) // (256 * 192 * 3)
    if nframes < 3:
        die('ffmpeg produced no frames')
    segs = (nframes + seg - 1) // seg
    est_min = (nframes * 0.4 + segs * 22) / 60
    print(f'      {nframes} frames ({nframes / fps_src:.1f} s) in {time.time() - t0:.0f} s; encoding will take roughly {est_min:.0f} minutes')

    # ---------------------------------------------------------------- 2. encode
    stream = os.path.join(work, 'stream.bin')
    print('[2/3] encoding (palette per segment, error diffusion) ...')
    t0 = time.time()
    run([sys.executable, os.path.join(TOOLS, 'encode4.py'), '--frames', frames, '--seg', str(seg), '--hyst', str(a.hyst),
         '--out', stream], env={'KCON': a.kcon}, cwd=TOOLS, label='encoder')
    print(f'      encoded in {(time.time() - t0) / 60:.1f} minutes')

    # ---------------------------------------------------------------- 3. ROM
    print('[3/3] assembling the player and building the ROM ...')
    env = {'PLAYER': 'player4' if song else 'player4n', 'FT50': ticks50, 'FT60': ticks60}
    if song:
        env['SONG'] = song
    if a.safe:
        env['SAFE'] = '1'
    rom_tmp = os.path.join(work, 'out.rom')
    run([sys.executable, os.path.join(TOOLS, 'build_rom.py'), stream, rom_tmp], env=env, cwd=TOOLS, label='ROM builder')
    shutil.copyfile(rom_tmp, out)
    size = os.path.getsize(out)
    if not a.keep_frames:
        try:
            os.remove(frames)
        except OSError:
            pass

    print('=' * 70)
    print(f'DONE: {out}')
    print(f'      {size / 1048576:.1f} MB, {nframes} frames, {nframes / fps50:.0f} s at 50 Hz / {nframes / fps60:.0f} s at 60 Hz')
    if size > 32 * 1048576:
        print('      WARNING: larger than 32 MB - the NEO8 bank registers address at most 32 MB.')
    elif size > 8 * 1048576:
        print('      NOTE: larger than 8 MB - needs a NEO8/NEO16 cartridge with enough flash (16 MB / 32 MB).')
    print('      openMSX: openmsx -machine Philips_NMS_8250 -ext fmpac -cart "%s" -romtype NEO-8   (ESC quits)' % out)
    print('=' * 70)


if __name__ == '__main__':
    main()
