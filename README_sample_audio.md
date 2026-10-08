# Sampled audio through an SCC

The Screen 4 full-refresh video player with the clip's own soundtrack, played as 8-bit samples by an **SCC**, from a **NEO16** mapper ROM.

## Requirements

* MSX2 (PAL or NTSC) with a **NEO16**-capable cartridge (NEO mapper, 16 KB banks, up to 64 MB) and an **SCC** cartridge (Konami SCC) in another slot
* openMSX: `-romtype NEO-16 -ext scc`

## How it works

* **ROM layout:** bank 0 = player; bank *n* = frame *n-1*, mapped at 4000h-7FFFh (register 6000h low byte, 6001h high nibble):
  `4000h` flags (bit 0 = a new palette follows), `4001h` palette (32 bytes), `4040h` 1472 signed 8-bit samples, `4600h` 2 x 6150 bytes of pattern/colour data.
  3455 frames of the Bittersweet Symphony clip make a 56.6 MB ROM.
* **The SCC lives in page 2.** The player scans all slots for it (writes 3Fh to the Konami bank register at 9000h and checks that wave RAM at 9800h reads back,
  while 0A000h does not behave like RAM). The player code runs from RAM (page 3); the ROM bank window stays in page 1.
* **One sample = two writes.** Sample *n* is written to wave entry 0 of channel 1 (9800h), then the frequency register (9880h) is rewritten. The deformation register
  (98E0h, bit 5) restarts the wave on every frequency write and the period high nibble is 0Fh, so the wave position never leaves entry 0 before the next sample arrives.
  A real SCC does not follow wave writes without the frequency write (variant `hw1280` was silent on real hardware).
* **The instruction flow is the sample clock.** There is no timer interrupt on an MSX2, and the video loop leaves no spare CPU time, so video bytes and samples are interleaved:
  groups of four slots, each = 1 sample (43 cycles) + 10/10/10/11 `OUTI`. A counter trick keeps the loop tight: `OUTI` decrements B, so B reaches zero exactly
  after the last group (an odd number of `OUTI` per group makes the first zero unique) and `JP NZ` needs no extra counter.
* **1200 samples per frame**, so sound and picture stay locked: 14.4 kHz source = 1/12 s per frame; played at about 14.5 kHz on NTSC and 15.2 kHz on PAL
  (PAL plays the whole clip 4% faster, like the picture).
* **Adaptive timing.** The number of `NOP`s per group is a "level" (28 of them). After each frame the player looks at how many spare samples it played while waiting for the retrace
  and moves one level up or down, so the frame always ends just before the vertical-retrace edge on any machine. A fixed padding broke on the Panasonic FS-A1ST (turbo R in Z80 mode):
  a third of the frames took one field too long, a 12 ms hole in the sound.
* **Nothing pauses the sound.** While waiting for the retrace the player keeps playing samples at the same rate (the block holds 1472 samples per frame, the extra ones continue the timeline),
  and the housekeeping after the edge (table flip, palette, level control, bank switch, ESC, VDP address) is spread over eight sample slots
  (`tools/gen_frame_h.py` generates that code and counts cycles). The longest pause between two samples is 0.10-0.11 ms (the VDP address set between the pattern and colour part of a frame);
  a palette change (every ~3 s) adds one 0.2 ms burst.
* **Audio timeline.** `make_audio6.py` band-limits the soundtrack (below 0.43 x the playback rate) and samples it on the video timeline:
  sample *i* of frame *k* is taken at *k*/12 + *i*/R (R = 14546 Hz). The mismatch between R and the real rate of a machine shows up as a small time jump at the frame boundary; it was measured
  from the SCC write times (`tools/run/cont.py`): about 5 samples per frame for the fixed-pause version, 1.4-2 samples (rms) for the final one.

## Build

```
python tools/encode6.py --frames frames.rgb --seg 38 --workers 4 --out stream.bin          # 256x192 rgb24 frames at 12 fps, see make_rom.py for the ffmpeg line
python tools/make_audio6.py clip.mkv 0 0 audio.raw --rate 14546 --store 1472                 # start 0, duration 0 = whole file
VARIANT=h python tools/build_rom6.py stream.bin audio.raw out.rom
openmsx -machine Philips_NMS_8250 -cart out.rom -romtype NEO-16 -ext scc                     # ESC quits (and restarts)
```

## Variants (`VARIANT=...`)

| variant | idea | longest pause between samples | verdict |
|---|---|---|---|
| `base` | 1200 samples/frame, fixed padding | 1.8 / 2.1 ms (PAL / NTSC) | runs over on a turbo R |
| `s1152` | 1152 samples/frame | 2.8 ms | still runs over on a turbo R |
| `adapt` | measures the idle time per frame, adapts the padding | 0.9 ms | correct timing everywhere |
| `tail` | keeps playing samples while waiting for the retrace | 0.36 ms | better |
| **`h`** | housekeeping spread over sample slots (recommended) | **0.10 ms** | seamless at the frame boundary |
| `hw1280` | 1280 samples/frame without the frequency write | - | silent on a real SCC |

`make_audio6.py --glide N` additionally cross-fades the first N samples of every frame from the value the player holds after the pause (not needed with `h`).

## Lessons

* Frame-locked audio cannot be both continuous and anchored to the video unless the real sample rate equals the design rate; the adaptive levels get within about 0.4%.
* openMSX only refreshes the SCC output after a frequency write; WebMSX needed its SCC deformation register moved to E0h-FFh (SCC mode) for the restart trick to work.
* A frame that ends just after the vertical-retrace window waits for a whole extra field: keep a few spare samples (the level control keeps 3-10).
