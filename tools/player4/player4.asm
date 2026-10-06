; MSX2 Screen 4 full-refresh video player for the NEO8 mapper.
; Every frame = 6 KB pattern + 6 KB colour table written into the hidden table set, then flipped at vblank
; (R#4 / R#3 / R#10).  Name table is a static identity map.  Interrupts stay disabled; ticks are counted from
; the VDP vertical-retrace bit (S#2 bit 6).  Stream starts at segment 2, read through windows 8000h/A000h.
        DEVICE NOSLOT64K
        ORG 0x4000
        db "AB"
        dw init
        dw 0,0,0,0,0,0
        ORG 0x4020
meta_pal:     ds 32            ; 16 x (R*16+B, G)
meta_frames:  dw 0
meta_fticks50: db 5
meta_fticks60: db 6
meta_border:  db 0
meta_nopace:  db 0
meta_songlen: dw 0             ; patched: length of the song in segment 2

vrprev   equ 0xC000
tcount   equ 0xC001
late     equ 0xC002           ; word
frameno  equ 0xC004           ; word
chunk    equ 0xC006
strp     equ 0xC00C           ; word
segcur   equ 0xC00E           ; word
framesleft equ 0xC010         ; word
fticks   equ 0xC015
cursel   equ 0xC016           ; table set being written (0/1)
rg1      equ 0xC017
dbg_req  equ 0xC020
dbg_ack  equ 0xC021
lastj    equ 0xC018
tmpj     equ 0xC019
songlen  equ 0xC01A           ; word
palflag  equ 0xC022
JIFFY    equ 0xFC9E
copier   equ 0xC100           ; song copy routine (runs from RAM)
palbuf   equ 0xC040           ; 32 bytes

        MACRO WO
        outi
        IFDEF SAFE
        nop
        ENDIF
        ENDM

        MACRO VREG val,reg
        ld a,val
        out (0x99),a
        ld a,0x80+reg
        out (0x99),a
        ENDM

        INCLUDE "../music/pt_syms.inc"
        ORG 0x4050
init:   ld a,1                ; NEO8: window 6000h = segment 1, 4000h = segment 0
        ld (0x6800),a
        xor a
        ld (0x6801),a
        ld (0x6000),a
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
        ld h,0x80
        call 0x0024           ; ENASLT: page 2 = our cartridge
        ld a,4
        call 0x005F           ; CHGMOD screen 4
        di
        ld a,(0xF3E0)         ; RG1SAV
        ld (rg1),a
        and 0xBF              ; blank the display until the first frame is ready
        out (0x99),a
        ld a,0x81
        out (0x99),a
        ld a,(0xFFE8)         ; RG9SAV: 50/60 Hz
        ld b,a
        and 0x7F              ; 192 lines
        out (0x99),a
        ld a,0x89
        out (0x99),a
        ld a,5
        bit 1,b
        jr nz,.pal50
        ld a,(meta_fticks60)
        jr .setf
.pal50: ld a,(meta_fticks50)
.setf:  ld (fticks),a
        VREG 0x2A,8           ; sprites off, TP=1 (colour 0 uses palette entry 0, not the backdrop)
        ld a,(meta_border)
        out (0x99),a
        ld a,0x87
        out (0x99),a
        VREG 0,16             ; palette
        ld hl,meta_pal
        ld bc,0x209A
        otir
        VREG 0,14             ; R#14 = 0
        VREG 0,2              ; name table at 0000h
        xor a                 ; identity name table: 0..255 three times
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
        ld (late),a
        ld (late+1),a
        ld (frameno),a
        ld (frameno+1),a
        ld (dbg_req),a
        ld (dbg_ack),a
        ld (vrprev),a
        ld (tcount),a
        ld (cursel),a
        ld hl,(JIFFY)         ; tick counting uses the BIOS jiffy counter (BIOS keeps status register 0 selected)
        ld a,l
        ld (lastj),a
        ld a,1                ; show set 1 (blank) until the first frame is flipped in
        call flip
        ; ---- RAMAD0/1 (RAM slot of pages 0/1, needed by the music driver) are only set by a disk ROM, so derive
        ;      them from the slot of page 3 (the RAM mapper slot has RAM in all four pages)
        in a,(0xA8)
        rlca
        rlca
        and 3
        ld c,a
        ld b,0
        ld hl,0xFCC1          ; EXPTBL
        add hl,bc
        ld a,(hl)
        and 0x80
        jr z,.ramslot
        ld a,(0xFFFF)         ; expanded: sub-slot register of page 3 (inverted)
        cpl
        and 0xC0
        rrca
        rrca
        rrca
        rrca
        or 0x80
.ramslot:
        or c
        ld (0xF341),a
        ld (0xF342),a
        ; ---- music: driver to RAM, song to RAM page 0 (read by the driver from there), start the interrupt player
        ld hl,2
        ld (segcur),hl
        call setbank          ; window 8000h = segment 2 (song)
        ld hl,drvbin
        ld de,0xCA00
        ld bc,drvend-drvbin
        ldir
        ld hl,(meta_songlen)
        ld (songlen),hl
        ld hl,copysong
        ld de,copier
        ld bc,copyend-copysong
        ldir
        call copier
        call DRV_INIT         ; hooks H.TIMI, enables interrupts

restart:
        ld hl,3
        ld (segcur),hl
        call setbank
        ld hl,0x8000
        ld (strp),hl
        ld hl,(meta_frames)
        ld (framesleft),hl

nextframe:
        ld a,(dbg_req)
        or a
        jr z,.nodbg
        ld a,1
        ld (dbg_ack),a
.hw:    ld a,(dbg_req)
        or a
        jr nz,.hw
        xor a
        ld (dbg_ack),a
.nodbg:
        ld a,(0xFBEC)         ; NEWKEY row 7 (kept up to date by the BIOS interrupt): ESC = bit 2
        and 4
        jp z,quit
        ld hl,(strp)
        ld a,(hl)             ; frame header: bit0 = a new palette (32 bytes) follows
        inc hl
        ld (palflag),a
        rra
        jr nc,.nopal
        ld de,palbuf
        ld bc,32
        ldir
.nopal:
        ; ---- write the frame (6 chunks of 2 KB) into the hidden table set
        ld a,(cursel)
        ld e,a
        add a,a
        add a,e               ; *3
        add a,a               ; *6
        ld e,a
        ld d,0
        ld iy,chtab
        add iy,de
        add iy,de
        add iy,de             ; chtab + set*18
        xor a
        ld (chunk),a
.chunk: di
        ld a,(iy+2)           ; R#14 = A16..A14 of the chunk
        out (0x99),a
        ld a,0x8E
        out (0x99),a
        ld a,(iy+0)
        out (0x99),a
        ld a,(iy+1)
        out (0x99),a
        ei
        ld c,0x98
        ld e,8
.w:     REPT 256
        WO
        ENDR
        call statpoll         ; keep counting vblanks while we stream
        dec e
        jp nz,.w
        ld a,h                ; slide the 16 KB data window after 8 KB
        cp 0xA0
        jr c,.nos
        sub 0x20
        ld h,a
        push hl
        ld hl,(segcur)
        inc hl
        ld (segcur),hl
        call setbank
        pop hl
.nos:   inc iy
        inc iy
        inc iy
        ld a,(chunk)
        inc a
        ld (chunk),a
        cp 6
        jp c,.chunk
        ld (strp),hl
        ; ---- pace: flip exactly when the frame period elapses (vblank edge)
        ld a,(meta_nopace)
        or a
        jr nz,.flip
.pw:    call statpoll
        ld a,(tcount)
        ld b,a
        ld a,(fticks)
        sub b
        jr z,.flip
        jr nc,.pw
.flip:  ld a,(cursel)
        call flip
        ld a,(meta_nopace)
        or a
        jr nz,.nolate
        ld a,(tcount)
        ld b,a
        ld a,(fticks)
        ld c,a
        ld a,b
        sub c
        jr nc,.pos
        xor a
.pos:   jr z,.noL
        push af
        ld hl,(late)
        inc hl
        ld (late),hl
        pop af
        cp c
        jr c,.noL
        ld a,c
.noL:   ld (tcount),a
.nolate:
        ld a,(rg1)            ; display on (after the first flip)
        di
        out (0x99),a
        ld a,0x81
        out (0x99),a
        ei
        ld a,(cursel)
        xor 1
        ld (cursel),a
        ld hl,(frameno)
        inc hl
        ld (frameno),hl
        ld hl,(framesleft)
        dec hl
        ld (framesleft),hl
        ld a,h
        or l
        jp nz,nextframe
        jp restart

quit:   call DRV_STOP
        rst 0

; A = table set to display: R#4 (patterns), R#3/R#10 (colours)
flip:   di
        ld l,a
        add a,a
        add a,l               ; *3
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
        ei
        ret

setbank:
        ld hl,(segcur)
        ld a,l
        ld (0x7000),a
        ld a,h
        ld (0x7001),a
        inc hl
        ld a,l
        ld (0x7800),a
        ld a,h
        ld (0x7801),a
        ret

; count BIOS jiffy ticks since the last call into tcount. Preserves BC,DE,HL.
statpoll:
        push af
        push hl
        ld a,(JIFFY)
        ld (tmpj),a
        ld hl,lastj
        sub (hl)
        jr z,.none
        ld hl,tcount
        add a,(hl)
        jr nc,.ok
        ld a,255
.ok:    ld (hl),a
        ld a,(tmpj)
        ld (lastj),a
.none:  pop hl
        pop af
        ret

; per set: R#4 value, R#3 value, R#10 value
fliptab:
        db 0x07, 0x7F, 0x01   ; set 0: patterns 2000h, colours 4000h
        db 0x0F, 0x7F, 0x02   ; set 1: patterns 6000h, colours 8000h

        MACRO CH addr
        db (addr & 0xFF), (((addr >> 8) & 0x3F) | 0x40), (addr >> 14)
        ENDM
chtab:  CH 0x2000
        CH 0x2800
        CH 0x3000
        CH 0x4000
        CH 0x4800
        CH 0x5000
        CH 0x6000
        CH 0x6800
        CH 0x7000
        CH 0x8000
        CH 0x8800
        CH 0x9000

; runs from RAM: swap RAM into pages 0/1, copy the song to 0000h, restore (song is read by the driver from there)
copysong:
        call DRV_SWITCH
        ld hl,0x8000
        ld de,0x0000
        ld bc,(songlen)
        ldir
        jp DRV_RESTORE
copyend:

drvbin: INCBIN "../music/pt_drive.bin"
drvend:

        ds 0x8000-$,0xFF
        SAVEBIN "player4.bin",0x4000,0x4000
