# make_rom.py — video clip (+ song) -> MSX2 NEO8 ROM (Full Refresh version)

    python make_rom.py myclip.mp4 mysong.pro                  # 12 fps, music, output myclip.rom next to the video
    python make_rom.py myclip.mp4 mysong.pro --fps 10 --out party.rom
    python make_rom.py myclip.mp4 --no-music --start 12 --duration 60
    python make_rom.py myclip.mp4 mysong.pro --fit letterbox  # keep the whole 16:9 picture (black bars) instead of cropping to 4:3
    python make_rom.py myclip.mp4 mysong.pro --crop-x 0.3     # move the 4:3 crop window to the left (0 = left edge, 1 = right edge)

Options: --fps (6..12.5, default 12), --fit crop|letterbox|stretch, --crop-x, --start/--duration (seconds), --denoise (ffmpeg hqdn3d, "off"),
--segment-seconds (palette every N s, default 3.2), --kcon, --hyst, --safe, --work, --keep-frames, --no-music.

* Frame rate: the ROM shows one frame every N vblanks, N = round(50/fps) on 50 Hz and round(60/fps) on 60 Hz. 12 fps gives 12.5 fps (PAL) / 12 fps
  (NTSC); 10 fps is exact on both. A full refresh needs at least 4 ticks (50 Hz) / 5 ticks (60 Hz), so 12.5 fps is the maximum.
* The song must be a ProTracker .PRO file of at most 8 KB (MSX-Music). It loops by itself. The PRO-TRACKER driver (Tyfoon Software 1991, loader removed) is included in tools/music/.
* Time: roughly 0.4 s per frame plus ~20 s per palette segment (about 15 minutes for a 2-minute clip at 12 fps).
* ROM size ~ 12 KB per frame (12 fps: 2 minutes = ~17 MB). The NEO8 bank registers address at most 32 MB.
* Needs Python 3 with numpy, scipy, pillow, ffmpeg (PATH or FFMPEG=...) and sjasmplus (PATH, SJASMPLUS=..., or tools/sjasmplus/).
* Intermediate files (stream.bin, palette, ...) go to make_rom_work/<name>/ ; the raw frames are deleted afterwards unless --keep-frames.
* Test in openMSX:  openmsx -machine Philips_NMS_8250 -ext fmpac -cart out.rom -romtype NEO-8     (ESC quits)

## Encoder engines
* `--engine v2` (default): linear-light error diffusion, a palette search on the 512-colour grid (so each ~3 s segment gets a palette that
  really fits its colours) and stronger temporal stability (tile hysteresis 0.4). In our tests about +3 dB (blurred PSNR in linear light) and
  visibly more natural skin tones than `classic`, with less flicker in static areas. About 3-4x slower than classic.
  Palettes are sorted dark to light, so palette entry 0 (the border colour) is always the darkest colour.
  It runs on **one process by default**. Each palette segment is independent, so `--workers N` encodes N segments in parallel.
* `--engine classic`: the original single-process encoder (`tools/encode4.py`).
* Same stream format and the same player either way.
