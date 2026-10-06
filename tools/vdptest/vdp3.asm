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

; CMDTEST sx,sy,dx,dy,nx,ny,arg,count : same-page HMMM, timing with poll
        MACRO CMDTEST sx,sy,dx,dy,nx,ny,arg,count
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
.src:   db sx,0, sy,0, dx,0, dy,0, nx,0, ny,0, 0,arg, 0xD0
        ENDM

tests:  dw tA,tB,tC,tD,tE,tF,tG,0
tA:     CMDTEST 0,10,0,16,8,8,0,1000       ; page0 src above dest? (sy=10,dy=16: vy=-6 -> would need DIY; here DIY=0 forced)
tB:     CMDTEST 0,16,0,10,8,8,0,1000       ; src below, DIY=0 (vy>0)
tC:     CMDTEST 0,30,0,40,8,8,8,1000       ; vy<0 with DIY=1 start at bottom: sy=30+7.. approximate
tD:     CMDTEST 0,20,0,20,64,8,0,500       ; wide 64x8 plain
tE:     CMDTEST 0,27,0,37,64,8,8,500       ; wide 64x8 DIY=1
tF:     CMDTEST 8,40,0,40,8,8,4,1000       ; DIX=1 same row
tG:     CMDTEST 0,0,0,100,8,8,0,1000       ; far apart plain 8x8
        ds 0x8000-$,0xFF
        SAVEBIN "vdp3.rom",0x4000,0x4000
