# Sample-audio branch: NEO16 + SCC test player

Variant of the Screen 4 full-refresh player that plays a **sampled soundtrack through an SCC** instead of MSX-Music.

* ROM layout (NEO16 mapper, 16 KB window at 4000h): bank 0 = player, bank *n* = frame *n-1*:
  flags, 32-byte palette, 1200 signed 8-bit samples, 2 x 6150 bytes of pattern/colour data.
* The SCC must be in another slot (it is found by a slot scan). Sample N is written to wave entry 0 of channel 1 and the
  frequency register is rewritten (deformation register E0h bit 5 = restart wave, period ~F00h so the position stays at 0).
* Video bytes (OUTI) and SCC writes are interleaved in groups of 4 slots, so the sample clock is the instruction flow:
  PAL about 15.4 kHz at 12.5 fps (80 ms), NTSC about 14.7 kHz at 12 fps. The audio source is 14.4 kHz (1200 samples = 1/12 s).
* Build (recommended, `tail` variant): 
  `python make_audio6.py clip.mkv 0 0 audio.raw --rate 14546 --store 1472` then
  `VARIANT=tail python build_rom6.py stream.bin audio.raw out.rom` (stream.bin from `encode6.py`).
  `make_audio6.py` band-limits the soundtrack and samples it on the video timeline (sample i of frame k at k/12 + i/R).
* openMSX: `-romtype NEO-16 -ext scc`. Verified on real hardware (NEO + SCC cartridge).
* WebMSX needs the SCC deformation register at E0h-FFh in SCC mode (fixed in the WebMSX Wavegame branch).

## Variants (build_rom6.py, env VARIANT=...)
* `base`   1200 samples/frame, fixed padding (PAL ~15.4 kHz, NTSC ~14.7 kHz), 1.8-2.1 ms hold gap per frame.
* `s1152`  1152 samples/frame, more timing margin (PAL ~15.0 kHz, NTSC ~14.2 kHz).
* `adapt`  1200 samples/frame, the player measures the idle time left per frame (counts rounds of the retrace wait) and
  adds/removes nops in the slot loop so the gap stays about 0.6-2.6k cycles on any machine (28 ladder levels).
* `hw1280` as adapt, but 1280 samples/frame (16 kHz) without the frequency rewrite: needs a real SCC (or emulator) whose
  channel output follows wave writes with the period set to 0; silent in openMSX.
* `tail` (recommended) as adapt, but the wait for the retrace plays further samples at the same rate (the block holds 1472
  samples per frame; the extra ones continue the timeline) and the idle count is in samples, kept at 6-13 per frame.
  Longest pause between two samples: 0.36 ms (0.59 ms on a palette-change frame), against 0.85 ms before. Verified in openMSX
  on PAL (NMS8250), NTSC (FS-A1) and turbo R (FS-A1ST): every frame takes exactly 4 (PAL) / 5 (NTSC) fields.
* `hw1280` was tried on real hardware and is silent: a real SCC does not follow wave writes without a frequency write.
