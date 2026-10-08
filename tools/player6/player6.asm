; MSX2 Screen 4 full-refresh video player with SAMPLED AUDIO through an SCC (NEO16 mapper test player).
; Every frame lives in its own 16 KB bank (NEO16 window at 4000h):
;     4000h  flags (bit0 = palette follows)       4001h  palette (32 bytes)
;     4040h  1200 signed 8-bit samples            4600h  6150 bytes patterns (6144 + 6 spill) + 6150 bytes colours
; The SCC sits in page 2 (found by a slot scan).  The player runs from RAM (page 3).  Interrupts stay off; the sample
; clock is the instruction flow itself: video bytes (OUTI) and SCC writes are interleaved in groups of four "slots"
; (1 sample + 10/10/10/11 OUTI).  Each sample is written to wave RAM entry 0 of SCC channel 1 and the frequency
; register is rewritten (deformation bit 5 restarts the wave, the period is ~4000 so the position stays at 0).
        DEVICE NOSLOT64K
        ORG 0x4000
        db "AB"
        dw init
        dw 0,0,0,0,0,0
        ORG 0x4020
meta_frames:  dw 0
meta_border:  db 0
meta_pal:     ds 32            ; 16 x (R*16+B, G)

; ---- RAM variables
cursel   equ 0xC000           ; table set being written (0/1)
rg1      equ 0xC001
palflag  equ 0xC002
ownslot  equ 0xC003
cand     equ 0xC004
idx      equ 0xC005
isntsc   equ 0xC006
bankno   equ 0xC008           ; word
nframes  equ 0xC00A           ; word
fleft    equ 0xC00C           ; word
sccslot  equ 0xC00E
lvl      equ 0xC010
idle     equ 0xC012           ; word
RAMCODE  equ 0xC100

        MACRO VREG val,reg
        ld a,val
        out (0x99),a
        ld a,0x80+reg
        out (0x99),a
        ENDM

        ORG 0x4050
init:   di
        ld hl,(meta_frames)
        ld (nframes),hl
        xor a
        ld (0x6000),a         ; NEO16: page-1 window = bank 0 (our boot bank), high bits 0
        ld (0x6001),a
        call 0x0138           ; RSLREG
        rrca
        rrca
        and 3
        ld c,a
        ld b,0
        ld hl,0xFCC1          ; EXPTBL
        add hl,bc
        or (hl)
        ld c,a
        inc hl
        inc hl
        inc hl
        inc hl
        ld a,(hl)
        and 0x0C
        or c
        ld (ownslot),a        ; slot of this cartridge (page 1)
        ; ---- find the SCC: scan all slots except ours
        xor a
        ld (idx),a
.lp:    ld a,(idx)
        and 3
        ld e,a
        ld d,0
        ld hl,0xFCC1
        add hl,de
        ld a,(hl)
        and 0x80
        ld c,a                ; 0x80 if primary slot is expanded
        ld a,(idx)
        rrca
        rrca
        and 3                 ; sub slot number
        jr z,.s0
        ld b,a
        ld a,c
        or a
        jr z,.skip            ; sub slots only exist in expanded slots
        ld a,b
.s0:    add a,a
        add a,a
        or c
        ld c,a
        ld a,(idx)
        and 3
        or c
        ld (cand),a
        ld hl,ownslot
        cp (hl)
        jr z,.skip
        call trysc
        jr z,.found
.skip:  ld a,(idx)
        inc a
        ld (idx),a
        cp 16
        jr c,.lp
        ; ---- not found: message
        call 0x006C           ; INITXT
        ld hl,msg_noscc
.pm:    ld a,(hl)
        or a
        jr z,.halt
        call 0x00A2           ; CHPUT
        inc hl
        jr .pm
.halt:  jr .halt
.found: ld a,(cand)
        ld (sccslot),a
        ; ---- initialise the SCC: SCC mode, channel 1 only, volume max, restart-on-frequency-write, period 0F00h
        ld a,0x3F
        ld (0x9000),a
        ld hl,0x9800          ; clear channel 1 wave
        ld b,32
        xor a
.cw:    ld (hl),a
        inc hl
        djnz .cw
        ld hl,0x988A          ; volumes: ch1 = 15, others 0
        ld (hl),0x0F
        inc hl
        xor a
        ld (hl),a
        inc hl
        ld (hl),a
        inc hl
        ld (hl),a
        inc hl
        ld (hl),a
        ld a,0x20
        ld (0x98E0),a         ; deformation: bit 5 = restart wave on every frequency write
        ld a,PERIODHI
        ld (0x9881),a         ; period high nibble
        xor a
        ld (0x9880),a
        ld a,1
        ld (0x988F),a         ; channel 1 on
        ; ---- video
        ld a,4
        call 0x005F           ; CHGMOD screen 4
        di
        ld a,(0xF3E0)         ; RG1SAV
        ld (rg1),a
        and 0xBF              ; display off until the first frame is ready
        out (0x99),a
        ld a,0x81
        out (0x99),a
        ld a,(0xFFE8)         ; RG9SAV: 50/60 Hz, 192 lines
        ld b,a
        and 0x7F
        out (0x99),a
        ld a,0x89
        out (0x99),a
        xor a
        bit 1,b
        jr nz,.pal50
        inc a
.pal50: ld (isntsc),a
        VREG 0x2A,8           ; sprites off, TP=1
        ld a,(meta_border)
        out (0x99),a
        ld a,0x87
        out (0x99),a
        VREG 0,16             ; palette
        ld hl,meta_pal
        ld bc,0x209A
        otir
        VREG 0,14
        VREG 0,2              ; name table at 0000h
        xor a                 ; identity name table 0..255 x 3
        out (0x99),a
        ld a,0x40
        out (0x99),a
        ld d,3
.nt:    xor a
        ld b,0
.ntl:   out (0x98),a
        inc a
        djnz .ntl
        dec d
        jr nz,.nt
        xor a
        ld (cursel),a
        ld a,2                ; status register 2 stays selected
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        ; ---- copy the player into RAM (page 3) and start it
        ld hl,ramimg
        ld de,RAMCODE
        ld bc,ramimg_end-ramimg
        ldir
        ld a,(isntsc)
        or a
        IFDEF ADAPT
        ld a,LEVP
        jr z,.lsel
        ld a,LEVN
.lsel:  ld (lvl),a
        ELSE
        ld hl,ladderP
        jr z,.lsel
        ld hl,ladderN
.lsel:  ld (callp0+1),hl
        ld (callp1+1),hl
        ld (callp2+1),hl
        ld (callp3+1),hl
        ENDIF
        ld a,1                ; show set 1 (blank) until the first flip
        call flip_
        jp restart

; Z = SCC found in slot (cand) page 2.  Writes into the page 2 area of the candidate slot.
trysc:  ld a,(cand)
        ld h,0x80
        call 0x0024           ; ENASLT page 2
        ld a,(0xA000)         ; RAM?  (would read back the complement)
        ld b,a
        cpl
        ld c,a
        ld (0xA000),a
        ld a,(0xA000)
        cp c
        jr nz,.notram
        ld a,b
        ld (0xA000),a
        or 1                  ; NZ
        ret
.notram:ld a,0x3F
        ld (0x9000),a         ; Konami SCC mapper: bank 3Fh = SCC registers
        ld a,0x55
        ld (0x9800),a
        ld a,(0x9800)
        cp 0x55
        ret nz
        ld a,0xAA
        ld (0x9800),a
        ld a,(0x9800)
        cp 0xAA
        ret

msg_noscc: db "SCC not found.",13,10,"Insert an SCC cartridge.",0

; ---------------------------------------------------------------- player image (runs at RAMCODE)
ramimg:
        DISP RAMCODE

; A = table set to display: R#4 (patterns), R#3/R#10 (colours)
flip_:  ld l,a
        add a,a
        add a,l
        ld e,a
        ld d,0
        ld hl,fliptab
        add hl,de
        ld a,(hl)
        out (0x99),a
        ld a,0x84
        out (0x99),a
        inc hl
        ld a,(hl)
        out (0x99),a
        ld a,0x83
        out (0x99),a
        inc hl
        ld a,(hl)
        out (0x99),a
        ld a,0x8A
        out (0x99),a
        ret

fliptab:
        db 0x07, 0x7F, 0x01   ; set 0: patterns 2000h, colours 4000h
        db 0x0F, 0x7F, 0x02   ; set 1: patterns 6000h, colours 8000h

        MACRO SETA r14,lo,hi
        ld a,r14
        out (0x99),a
        ld a,0x8E
        out (0x99),a
        ld a,lo
        out (0x99),a
        ld a,hi|0x40
        out (0x99),a
        ENDM

        include "ladders.inc"       ; generated by build_rom6.py (SAMP groups, ladders, B0, ...)

        IFDEF ADAPT
setlad: ld a,(lvl)
        add a,a
        ld e,a
        ld d,0
        ld hl,ladtab
        add hl,de
        ld e,(hl)
        inc hl
        ld d,(hl)
        ex de,hl
        ld (callp0+1),hl
        ld (callp1+1),hl
        ld (callp2+1),hl
        ld (callp3+1),hl
        IFDEF TAIL
        ld a,(lvl)
        add a,a
        ld e,a
        ld d,0
        ld hl,tltab
        add hl,de
        ld e,(hl)
        inc hl
        ld d,(hl)
        ex de,hl
        ld (calltl+1),hl
        ENDIF
        ret
        ENDIF

restart:
        ld hl,1
        ld (bankno),hl
        ld hl,(nframes)
        ld (fleft),hl
nextframe:
        IFDEF ADAPT
        call setlad
        ENDIF
        in a,(0xAA)           ; ESC?
        and 0xF0
        or 7
        out (0xAA),a
        in a,(0xA9)
        and 4
        jp z,quit
        ld a,(bankno)
        ld (0x6000),a
        ld a,(bankno+1)
        ld (0x6001),a
        ld a,(0x4000)
        ld (palflag),a
        ld de,0x4040
        ld hl,0x4600
        ld c,0x98
        ld a,(cursel)
        or a
        jp nz,set1_
        SETA 0,0x00,0x20      ; patterns of set 0: 2000h
        ld b,B0
callp0: call ladderP
        SETA 1,0x00,0x00      ; colours of set 0: 4000h
        ld b,B0
callp1: call ladderP
        jp tail_
set1_:  SETA 1,0x00,0x20      ; patterns of set 1: 6000h
        ld b,B0
callp2: call ladderP
        SETA 2,0x00,0x00      ; colours of set 1: 8000h
        ld b,B0
callp3: call ladderP
        IFDEF TAIL
tail_:
calltl: call tl0              ; keeps playing samples until the retrace edge (patched per level)
        ld hl,-(0x4040+1200)
        add hl,de
        ld (idle),hl          ; number of extra samples played while waiting
        ELSE
        IFDEF ADAPT
tail_:  ld de,0
.tl:    inc de                ; 40 cycles per round: counts the idle time left in this frame
        in a,(0x99)
        and 0x40
        jr z,.tl
        ld (idle),de
        ELSE
tail_:  in a,(0x99)           ; wait for the vertical-retrace edge that ends the frame period
        and 0x40
        jr z,tail_
        ENDIF
        ENDIF
        ld a,(cursel)
        call flip_
        ld a,(palflag)        ; a new palette takes effect together with the table flip
        rra
        jr nc,.nopal
        VREG 0,16
        ld hl,0x4001
        ld bc,0x209A
        otir
.nopal:
        IFDEF ADAPT
        ld a,(lvl)            ; adapt the slot padding so that a few spare slots are left per frame
        ld b,a
        IFDEF TAIL
        ld a,(idle+1)
        or a
        jr nz,.ao             ; edge missed by a whole field: back off hard
        ld a,(idle)
        cp 100
        jr nc,.ao
        cp 6
        jr c,.al
        cp 14
        jr c,.ak
        ELSE
        ld a,(idle+1)
        cp 3
        jr nc,.ao             ; edge missed by a whole field: back off hard
        or a
        jr nz,.am
        ld a,(idle)
        cp 15
        jr c,.al
        cp 65
        jr c,.ak
        ENDIF
.am:    ld a,b
        cp NLEV-1
        jr nc,.ak
        inc b
        jr .ak
.al:    ld a,b
        or a
        jr z,.ak
        dec b
        jr .ak
.ao:    ld a,b
        sub 3
        jr nc,.ap
        xor a
.ap:    ld b,a
.ak:    ld a,b
        ld (lvl),a
        ENDIF
        ld a,(rg1)            ; display on
        out (0x99),a
        ld a,0x81
        out (0x99),a
        ld a,(cursel)
        xor 1
        ld (cursel),a
        ld hl,(bankno)
        inc hl
        ld (bankno),hl
        ld hl,(fleft)
        dec hl
        ld (fleft),hl
        ld a,h
        or l
        jp nz,nextframe
        jp restart

quit:   xor a
        ld (0x6000),a
        ld (0x6001),a
        ld a,0
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        rst 0

        ENT
ramimg_end:

        ds 0x8000-$,0xFF
        SAVEBIN "player6.bin",0x4000,0x4000
