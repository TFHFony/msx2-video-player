# msx2-video-player

Play a video clip with background music on a plain **MSX2** (V9938, 64 KB RAM) from a **NEO8** mapper cartridge.
`make_rom.py` turns any video (+ a ProTracker song) into a ROM image.

* **Screen 4 (GRAPHIC 3)**, 256x192, 16 colours from the 512-colour palette, two colours per 8x1 pixel row
* **Full refresh**: every frame rewrites all 768 tiles (6 KB patterns + 6 KB colours) into a hidden pair of tables that is flipped at
  vblank with three VDP register writes - no tearing, no stale blocks
* Picture quality comes from the encoder (linear-light error diffusion inside the two-colour rows, a palette searched on the 512-colour grid for
  each ~3 s segment, temporal tile hysteresis), not from the player, which is a plain streaming loop
* **12 fps** on NTSC (5 vblanks per frame) / 12.5 fps on PAL (4 vblanks per frame), 10 fps is exact on both
* Optional **MSX-Music** (YM2413) background music, interrupt driven, using the PRO-TRACKER V1.0 driver by Tyfoon Software (included, see below)
* **Branch `sample-audio`:** instead of a tracker song the clip's own **sampled soundtrack** plays through an **SCC** (Konami SCC cartridge) from a **NEO16** mapper ROM,
  about 15 kHz, 8 bit, kept in step with the video frames (see [README_sample_audio.md](README_sample_audio.md))

Made by Claude & The File-Hunter of FONY. Released under the [Unlicense](LICENSE) (public domain).

## Quick start

```
pip install numpy scipy pillow          # plus ffmpeg and sjasmplus on the PATH (or see "Requirements")
python make_rom.py myclip.mp4 mysong.pro               # -> myclip.rom
openmsx -machine Philips_NMS_8250 -ext fmpac -cart myclip.rom -romtype NEO-8     # ESC quits
```

More options (frame rate, 16:9 letterbox/crop window, trimming, no music, ...): see [README_make_rom.md](README_make_rom.md).

## Requirements

* Python 3 with `numpy`, `scipy`, `pillow`
* [ffmpeg](https://ffmpeg.org/) (on the PATH, or `FFMPEG=/path/to/ffmpeg`)
* [sjasmplus](https://github.com/z00m128/sjasmplus) (on the PATH, `SJASMPLUS=...`, or unpacked into `tools/sjasmplus/`)
* The music driver is the PRO-TRACKER V1.0 driver by **Tyfoon Software (1991)**, included here in the version this project needs: the disk loader is removed and the source is converted to sjasmplus syntax
  (`tools/music/pt_drive_noloader.asm`, assembled binary `tools/music/pt_drive.bin`, addresses in `tools/music/pt_syms.inc`).
  `tools/build_pt_driver.py` can regenerate these from the original `PT_DRIVE.ASC`.
  The song must be a ProTracker `.PRO` file of at most 8 KB (MSX-Music); it loops by itself (no song is included).
* openMSX for testing (`-ext fmpac` gives the MSX-Music chip on a plain MSX2 machine)

## How it works

```
video --ffmpeg--> 256x192 frames --tools/encode6.py (or encode4.py)--> stream.bin --tools/build_rom.py--> NEO8 ROM
                                      (palette per segment,           (player4.asm + song + stream,
                                       error diffusion, hysteresis)    patched meta data)
```

ROM layout (8 KB NEO8 segments): 0-1 player code (the PT driver binary rides along and is copied to RAM at `CA00h`),
2 the song (copied into RAM page 0, where the driver reads it), 3.. the video stream.
Each frame in the stream: a flag byte, an optional 32-byte palette, then 12288 bytes of table data.

The player (`tools/player4/player4.asm`) per frame: stream the 12 KB from ROM into the hidden table set with unrolled `OUTI`
(through a 16 KB sliding ROM window), wait for the frame period, flip the tables (+ palette) on a vblank edge.

### Measured (openMSX, PAL, Z80 3.58 MHz; the fast player was also run on real MSX2 hardware at 50 and 60 Hz)

| | frame write time | notes |
|---|---|---|
| 12 KB, back-to-back `OUTI` | 64 ms | no music |
| + MSX-Music interrupt player | 78 ms | about 13 ms per 100 ms for the PT driver + BIOS interrupt |
| 12 fps frame period | 80 ms (50 Hz, 4 ticks) / 83.3 ms (60 Hz, 5 ticks) | thin margin; use `--fps 10` for more |
| 10 fps frame period | 100 ms / 100 ms | comfortable |

Spaced-out writes (`--safe`, `OUTI`+`NOP`, for VDPs that cannot take 16-cycle writes) need 81 ms without and 98.5 ms with music, so they
only fit around 8-10 fps.

### Things that bit us (worth knowing if you write your own)

* **R#8 bit 5 (TP) must be 1** (`R#8 = 0x2A`) or palette colour 0 is shown as the backdrop colour (black) instead of its palette entry.
* With interrupts enabled the BIOS interrupt acknowledges the VDP by reading **status register 0**. Never leave S#2 selected; count ticks
  from `JIFFY` (`FC9Eh`) and wrap every two-byte VDP control sequence in `DI`/`EI`.
* The PT driver pages RAM into pages 0/1 during each interrupt and reads its song from address 0. It uses `RAMAD0/1` (`F341h/F342h`),
  which are only set when a disk ROM is present - the player derives them from the page-3 RAM slot.
* NEO8 bank registers: `6000h/6001h`, `6800h/6801h`, `7000h/7001h`, `7800h/7801h` (low byte, high nibble) for the four 8 KB windows
  at `4000h/6000h/8000h/A000h`. Set window 6000h explicitly if code reaches into it.
* openMSX romtype name for NEO8 is `NEO-8`.

## Sampled audio through the SCC (branch `sample-audio`)

An MSX2 has no timer interrupt to clock a sample player, and the video loop leaves no CPU time for one. This branch lets the **instruction flow
itself be the sample clock**: video bytes (`OUTI`) and SCC writes are interleaved in groups of four slots (one sample plus 10/10/10/11
video bytes), so the 12 KB frame and the audio are produced by the same loop.

* The SCC (in another slot, found by a slot scan) plays 8-bit samples: each one is written to wave entry 0 of channel 1 and the frequency register is
  rewritten with the deformation register set to "restart wave on frequency write" (the period stays at about 0F00h so the wave position never advances).
* 1200 samples per video frame (14.4 kHz source = 1/12 s), played at about 14.5 kHz on NTSC and 15.2 kHz on PAL, so sound and picture stay locked.
* The ROM is NEO16: one 16 KB bank per frame (palette, samples, video data); the player runs from RAM.
* The player measures the time left per frame and adds or removes `NOP`s in the slot loop, so it also keeps its frame period on slower machines
  (it was needed on the Panasonic FS-A1ST turbo R in Z80 mode). While it waits for the retrace it keeps playing samples, and the per-frame
  housekeeping (table flip, bank switch, level control, ESC) is spread over sample slots, so the sample clock never stops at a frame boundary.
* Verified in openMSX on a PAL MSX2 (NMS8250), an NTSC MSX2 (FS-A1) and a turbo R (FS-A1ST); a first 10 second version was also run on real hardware.

```
python make_audio6.py clip.mkv 0 0 audio.raw --rate 14546 --store 1472      # band-limited soundtrack on the video timeline
VARIANT=h python tools/build_rom6.py stream.bin audio.raw out.rom             # stream.bin from tools/encode6.py
openmsx -machine Philips_NMS_8250 -cart out.rom -romtype NEO-16 -ext scc
```

The details, the variants that were tried and what they measured are in [README_sample_audio.md](README_sample_audio.md).

## Repository layout

```
make_rom.py               the one-command front end
README_make_rom.md        all options of make_rom.py
tools/encode6.py          encoder v2 (default): linear-light dithering + palette search, segments can be encoded in parallel
tools/encode4.py          classic encoder (frames -> stream)
tools/s4_lab.py           coder / palette-search / metric functions used by encode6 (also an image-quality test bench)
tools/screen4_sim.py      colour-pair / dithering / palette code used by the encoder (also a single-frame comparison tool)
tools/s4_fs.py            single-frame experiments (error diffusion, palette refinement, per-band palettes)
tools/s4_decode.py        decode a stream back to images
tools/build_rom.py        stream + player + song -> ROM
tools/build_pt_driver.py  regenerate tools/music/ from the original PT_DRIVE.ASC (optional)
tools/music/              PRO-TRACKER driver (Tyfoon Software 1991) without its loader: source, binary, symbols
tools/player4/            Z80 player with music;  tools/player4n/  without music
tools/player6/            Z80 player with SCC sampled audio (branch sample-audio); tools/build_rom6.py, make_audio6.py, gen_frame_h.py build it
tools/run/                openMSX test scripts (halt at frame N and dump VRAM, per-frame timing, FM write counting, SCC write timing and continuity)
tools/vdptest/            small test ROMs that measured Z80/VDP throughput (OUTI, OTIR, HMMM, HMMC ...)
```

## Not included

The sample video, built ROMs, any song, ffmpeg and sjasmplus.
