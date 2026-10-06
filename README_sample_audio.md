# Sample-audio branch: NEO16 + SCC test player

Variant of the Screen 4 full-refresh player that plays a **sampled soundtrack through an SCC** instead of MSX-Music.

* ROM layout (NEO16 mapper, 16 KB window at 4000h): bank 0 = player, bank *n* = frame *n-1*:
  flags, 32-byte palette, 1200 signed 8-bit samples, 2 x 6150 bytes of pattern/colour data.
* The SCC must be in another slot (it is found by a slot scan). Sample N is written to wave entry 0 of channel 1 and the
  frequency register is rewritten (deformation register E0h bit 5 = restart wave, period ~F00h so the position stays at 0).
* Video bytes (OUTI) and SCC writes are interleaved in groups of 4 slots, so the sample clock is the instruction flow:
  PAL about 15.4 kHz at 12.5 fps (80 ms), NTSC about 14.7 kHz at 12 fps. The audio source is 14.4 kHz (1200 samples = 1/12 s).
* Build: `python build_rom6.py stream.bin audio_s16le_mono_14400.raw out.rom` (stream.bin from `encode6.py`,
  audio e.g. `ffmpeg -i clip -vn -af "pan=mono|c0=0.5*c0+0.5*c1,aresample=14400" -f s16le -ac 1 audio.raw`).
* openMSX: `-romtype NEO-16 -ext scc`. Verified on real hardware (NEO + SCC cartridge).
* WebMSX needs the SCC deformation register at E0h-FFh in SCC mode (fixed in the WebMSX Wavegame branch).
