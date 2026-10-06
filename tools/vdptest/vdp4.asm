        DEVICE NOSLOT64K
        ORG 0x4000
        db "AB"
        dw init
        dw 0,0,0,0,0,0
JIFFY   equ 0xFC9E
RES     equ 0xC100
init:   ld a,5
        call 0x005F
        ld a,0x0A
        out (0x99),a
        ld a,0x88
        out (0x99),a
        ld a,(0xFFE8)
        or 0x80
        out (0x99),a
        ld a,0x89
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

; 2000 copies, DI throughout with S#2 selected, tight poll, outi-chain issue (same as player)
        MACRO T4 count,ent
        ld de,count
.blk:   di
        ld hl,ent
        call issue
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
        dec de
        ld a,d
        or e
        jr nz,.blk
        ret
        ENDM
tests:  dw t1,t2,t3,0
t1:     T4 2000,e1
t2:     T4 1000,e2
t3:     T4 1000,e3
issue:  ld a,32
        out (0x99),a
        ld a,0x91
        out (0x99),a
        ld c,0x9B
        outi
        xor a
        out (c),a
        outi
        out (c),a
        outi
        out (c),a
        outi
        out (c),a
        outi
        out (c),a
        ld a,8
        out (c),a
        xor a
        out (c),a
        out (c),a
        outi
        ld a,0xD0
        out (c),a
        ret
e1:     db 0,10,0,16,8,0       ; sx,sy,dx,dy,nx,arg  8x8 same page
e2:     db 0,16,0,10,64,0      ; 64x8
e3:     db 0,200,0,100,8,8     ; DIY
        ds 0x8000-$,0xFF
        SAVEBIN "vdp4.rom",0x4000,0x4000
