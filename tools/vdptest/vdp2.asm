; VDP command speed vs size, sprites off. Results at C100h (ticks of 1/50 s)
        DEVICE NOSLOT64K
        ORG 0x4000
        db "AB"
        dw init
        dw 0,0,0,0,0,0
JIFFY   equ 0xFC9E
RES     equ 0xC100
cnt     equ 0xC0F0
tbl     equ 0xC0C0

init:   ld a,5
        call 0x005F
        ; sprites off: R#8 bit1
        ld a,0x0A
        out (0x99),a
        ld a,0x88
        out (0x99),a
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
        call timeit
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
        ld (RES-1),a
.hang:  jr .hang

timeit: ld hl,(JIFFY)
.s:     ld bc,(JIFFY)
        or a
        sbc hl,bc
        ld hl,(JIFFY)
        jr z,.s
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

; generic: count x command, NX,NY (pixels) CMD
        MACRO CMDTEST nx,ny,count,cmd
        ld hl,.src
        ld de,tbl
        ld bc,15
        ldir
        ld hl,count
        ld (cnt),hl
.blk:   di
        ld a,32
        out (0x99),a
        ld a,0x80+17
        out (0x99),a
        ld hl,tbl
        ld bc,0x0F9B
        otir
        ei
.w:     di
        ld a,2
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        in a,(0x99)
        ld b,a
        xor a
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        ei
        ld a,b
        rra
        jr c,.w
        ld hl,(cnt)
        dec hl
        ld (cnt),hl
        ld a,h
        or l
        jr nz,.blk
        ret
.src:   db 0,0, 0,2, 0,0, 0,0, low nx,high nx, low ny,high ny, 0x11,0, cmd
        ENDM

tests:  dw tA,tB,tC,tD,tE,tF,tG,0
tA:     CMDTEST 8,8,2000,0xD0       ; HMMM 8x8
tB:     CMDTEST 16,16,1000,0xD0     ; HMMM 16x16
tC:     CMDTEST 32,32,500,0xD0      ; HMMM 32x32
tD:     CMDTEST 128,64,100,0xD0     ; HMMM 128x64 (4KB)
tE:     CMDTEST 128,64,100,0xC0     ; HMMV 128x64 fill
tF:     CMDTEST 32,32,500,0x90      ; LMMM 32x32 (imp)
; concurrency: start HMMM 256x100 then OTIR 12.8KB while it runs, wait; 20 reps
tG:     ld hl,.src
        ld de,tbl
        ld bc,15
        ldir
        ld hl,20
        ld (cnt),hl
.blk:   di
        ld a,32
        out (0x99),a
        ld a,0x80+17
        out (0x99),a
        ld hl,tbl
        ld bc,0x0F9B
        otir
        ; CPU streams 12.8KB to VRAM page 1 meanwhile (OTIR x100 of 128)
        ei
        di
        ld a,0x00
        out (0x99),a
        ld a,0x40+0x00
        out (0x99),a
        ei
        ld de,100
.o:     ld hl,0x4000
        ld bc,0x8098
        otir
        dec de
        ld a,d
        or e
        jr nz,.o
        ei
.w:     di
        ld a,2
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        in a,(0x99)
        ld b,a
        xor a
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        ei
        ld a,b
        rra
        jr c,.w
        ld hl,(cnt)
        dec hl
        ld (cnt),hl
        ld a,h
        or l
        jr nz,.blk
        ret
.src:   db 0,0, 0,2, 0,0, 0,0, 0,1, 100,0, 0x11,0, 0xD0
        ds 0x8000-$,0xFF
        SAVEBIN "vdp2.rom",0x4000,0x4000
