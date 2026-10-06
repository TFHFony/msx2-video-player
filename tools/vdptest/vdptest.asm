; VDP / Z80 throughput test ROM (plain 16KB ROM at 4000h). Results (ticks of JIFFY) at C100h.
        DEVICE NOSLOT64K
        ORG 0x4000
        db "AB"
        dw init
        dw 0,0,0,0,0,0

JIFFY   equ 0xFC9E
RES     equ 0xC100

init:   ld a,5
        call 0x005F          ; CHGMOD screen 5
        ei
        ld de,RES
        ld ix,tests
.next:  ld l,(ix+0)
        ld h,(ix+1)
        ld a,h
        or l
        jr z,.done
        inc ix
        inc ix
        push de
        push ix
        ld e,l
        ld d,h
        call timeit          ; HL = ticks
        pop ix
        pop de
        ex de,hl
        ld (hl),e
        inc hl
        ld (hl),d
        inc hl
        ex de,hl
        jr .next
.done:  ld a,0xAA
        ld (RES-1),a         ; done marker
.hang:  jr .hang

tests:  dw t_base, t_otir, t_blk, t_hmmm, t_hmmc, t_blk2, 0

; DE = routine; returns HL = elapsed ticks
timeit: ld hl,(JIFFY)
.s:     ld bc,(JIFFY)
        or a
        sbc hl,bc
        ld hl,(JIFFY)
        jr z,.s             ; wait for tick change
        push hl
        ld hl,.ret
        push hl
        ex de,hl
        jp (hl)
.ret:   ld de,(JIFFY)
        pop hl
        ex de,hl
        or a
        sbc hl,de
        ret

; baseline: 3 x 65536 x (dec bc / ld a,b / or c / jr nz)
t_base: ld e,3
.o:     ld bc,0
.l:     dec bc
        ld a,b
        or c
        jr nz,.l
        dec e
        jr nz,.o
        ret

; 1000 x OTIR of 128 bytes (contiguous)
t_otir: xor a
        out (0x99),a
        ld a,0x40
        out (0x99),a
        ld de,1000
.l:     ld hl,0x4000
        ld bc,0x8098
        otir
        dec de
        ld a,d
        or e
        jr nz,.l
        ret

; 2000 x 8x8 block, per-row address set + 4 OUTI
t_blk:  ld de,2000
        ld (cnt),de
        ld c,0x98
.blk:   ld hl,0x4000
        ld de,0x0000
        REPT 8
        ld a,e
        out (0x99),a
        ld a,d
        or 0x40
        out (0x99),a
        outi
        outi
        outi
        outi
        ld a,e
        add a,0x80
        ld e,a
        jr nc,$+3
        inc d
        ENDR
        ld hl,(cnt)
        dec hl
        ld (cnt),hl
        ld a,h
        or l
        jp nz,.blk
        ret

; 2000 x 8x8 block, set address once, 2 rows of 4 via contiguous OUTI (reference: linear 32 bytes)
t_blk2: ld de,2000
        ld (cnt),de
        ld c,0x98
        xor a
        out (0x99),a
        ld a,0x40
        out (0x99),a
.blk:   ld hl,0x4000
        REPT 32
        outi
        ENDR
        ld hl,(cnt)
        dec hl
        ld (cnt),hl
        ld a,h
        or l
        jp nz,.blk
        ret

; 2000 x HMMM 8x8 page2 -> page0, wait for completion each time
t_hmmm: ld de,2000
        ld (cnt),de
        ld hl,hmmm_src
        ld de,hmmm_tbl
        ld bc,15
        ldir
.blk:   di
        ld a,32
        out (0x99),a
        ld a,0x80+17
        out (0x99),a
        ld hl,hmmm_tbl
        ld bc,0x0F9B
        otir
.w:     ld a,2
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        in a,(0x99)
        rra
        jr c,.w
        xor a
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        ei
        ld a,(hmmm_tbl+4)
        add a,8
        ld (hmmm_tbl+4),a
        ld hl,(cnt)
        dec hl
        ld (cnt),hl
        ld a,h
        or l
        jp nz,.blk
        ret

; 1000 x HMMC 8x8 (32 bytes) with TR polling
t_hmmc: ld de,1000
        ld (cnt),de
.blk:   di
        ld hl,hmmc_src
        ld de,hmmm_tbl
        ld bc,15
        ldir
        ld a,36
        out (0x99),a
        ld a,0x80+17
        out (0x99),a
        ld hl,hmmm_tbl+4     ; DX..CMD (regs 36..46) = 11 bytes, last = command
        ld bc,0x0B9B
        otir
        ld a,0x80+44         ; R#17 = 44, non-incrementing
        out (0x99),a
        ld a,0x80+17
        out (0x99),a
        ld a,2
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        ld hl,0x4000
        ld b,31              ; first byte comes from CLR (R#44); 31 more via TR polling
.p:     in a,(0x99)
        rla
        jr nc,.p
        ld a,(hl)
        inc hl
        out (0x9B),a
        djnz .p
        xor a
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        ei
        ld hl,(cnt)
        dec hl
        ld (cnt),hl
        ld a,h
        or l
        jp nz,.blk
        ret

cnt:    equ 0xC0F0
hmmm_tbl equ 0xC0C0

; R#32.. : SX,SY, DX,DY, NX,NY, CLR,ARG,CMD
hmmm_src: db 0,0, 0,2, 0,0, 0,0, 8,0, 8,0, 0,0, 0xD0
hmmc_src: db 0,0, 0,2, 0,0, 0,0, 8,0, 8,0, 0,0, 0xF0

        ds 0x8000-$,0xFF
        SAVEBIN "vdptest.rom",0x4000,0x4000
