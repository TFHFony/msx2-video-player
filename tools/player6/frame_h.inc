restart:
        ld hl,1
        ld (bankno),hl
        ld hl,(nframes)
        ld (fleft),hl
firstframe:
        call setlad_h
        ld a,(bankno)
        ld (0x6000),a
        ld a,(bankno+1)
        ld (0x6001),a
        ld a,(0x4000)
        ld (palflag),a
        ld de,0x4042
        ld hl,0x4600
        ld c,0x98
        ld a,0
        out (0x99),a
        ld a,142
        out (0x99),a
        ld a,0
        out (0x99),a
        ld a,96
        out (0x99),a
        ld b,B0
        jp F0body
F0body:
callp0: call ladderP
        ld a,1
        out (0x99),a
        ld a,142
        out (0x99),a
        ld a,0
        out (0x99),a
        ld a,64
        out (0x99),a
        ld b,B0
callp1: call ladderP
tailA:
calltlA: call tl0
; ------------- after set 0 has been written: flip to it, prepare set 1
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,7
        out (0x99),a
        ld a,132
        out (0x99),a
        ld a,127
        out (0x99),a
        ld a,131
        out (0x99),a
        ld a,1
        out (0x99),a
        ld a,138
        out (0x99),a
        ld (tailend),de
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld hl,(tailend)
        ld bc,-(0x4040+1202)
        add hl,bc
        ld a,(lvl)
        ld b,a
        ld a,h
        or a
        jr nz,.ao0
        ld a,l
        cp 100
        jr nc,.ao0
        cp 3
        jr c,.al0
        cp 10
        jr c,.ak0
.am0:
        ld a,b
        cp NLEV-1
        jr nc,.ak0
        inc b
        jr .ak0
.al0:
        ld a,b
        or a
        jr z,.ak0
        dec b
        jr .ak0
.ao0:
        ld a,b
        sub 3
        jr nc,.ap0
        xor a
.ap0:
        ld b,a
.ak0:
        ld a,b
        ld (lvl),a
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,(lvl)
        add a,a
        ld c,a
        ld b,0
        ld hl,ladtab
        add hl,bc
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld (callp0+1),hl
        ld (callp1+1),hl
        ld (callp2+1),hl
        ld (callp3+1),hl
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld hl,tltab
        add hl,bc
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld (calltlA+1),hl
        ld (calltlB+1),hl
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,(rg1)
        out (0x99),a
        ld a,0x81
        out (0x99),a
        ld hl,(bankno)
        inc hl
        ld (bankno),hl
        ld hl,(fleft)
        dec hl
        ld (fleft),hl
        ld a,h
        or l
        jp z,restart_0
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
p6_0:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,(palflag)
        rra
        jr nc,.np0
        ld a,0
        out (0x99),a
        ld a,144
        out (0x99),a
        ld hl,0x4001
        ld bc,0x209A
        otir
.np0:
        ld a,(bankno)
        ld (0x6000),a
        ld a,(bankno+1)
        ld (0x6001),a
        ld de,0x4040
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,(0x4000)
        ld (palflag),a
        in a,(0xAA)
        and 0xF0
        or 7
        out (0xAA),a
        in a,(0xA9)
        and 4
        jp z,quit
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,1
        out (0x99),a
        ld a,142
        out (0x99),a
        ld a,0
        out (0x99),a
        ld a,96
        out (0x99),a
        ld b,B0
        ld hl,0x4600
        ld c,0x98
        jp F1body
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
restart_0:
        ld hl,1
        ld (bankno),hl
        ld hl,(nframes)
        ld (fleft),hl
        jp p6_0
F1body:
callp2: call ladderP
        ld a,2
        out (0x99),a
        ld a,142
        out (0x99),a
        ld a,0
        out (0x99),a
        ld a,64
        out (0x99),a
        ld b,B0
callp3: call ladderP
tailB:
calltlB: call tl0
; ------------- after set 1 has been written: flip to it, prepare set 0
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,15
        out (0x99),a
        ld a,132
        out (0x99),a
        ld a,127
        out (0x99),a
        ld a,131
        out (0x99),a
        ld a,2
        out (0x99),a
        ld a,138
        out (0x99),a
        ld (tailend),de
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld hl,(tailend)
        ld bc,-(0x4040+1202)
        add hl,bc
        ld a,(lvl)
        ld b,a
        ld a,h
        or a
        jr nz,.ao1
        ld a,l
        cp 100
        jr nc,.ao1
        cp 3
        jr c,.al1
        cp 10
        jr c,.ak1
.am1:
        ld a,b
        cp NLEV-1
        jr nc,.ak1
        inc b
        jr .ak1
.al1:
        ld a,b
        or a
        jr z,.ak1
        dec b
        jr .ak1
.ao1:
        ld a,b
        sub 3
        jr nc,.ap1
        xor a
.ap1:
        ld b,a
.ak1:
        ld a,b
        ld (lvl),a
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,(lvl)
        add a,a
        ld c,a
        ld b,0
        ld hl,ladtab
        add hl,bc
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld (callp0+1),hl
        ld (callp1+1),hl
        ld (callp2+1),hl
        ld (callp3+1),hl
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld hl,tltab
        add hl,bc
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld (calltlA+1),hl
        ld (calltlB+1),hl
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,(rg1)
        out (0x99),a
        ld a,0x81
        out (0x99),a
        ld hl,(bankno)
        inc hl
        ld (bankno),hl
        ld hl,(fleft)
        dec hl
        ld (fleft),hl
        ld a,h
        or l
        jp z,restart_1
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
p6_1:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,(palflag)
        rra
        jr nc,.np1
        ld a,0
        out (0x99),a
        ld a,144
        out (0x99),a
        ld hl,0x4001
        ld bc,0x209A
        otir
.np1:
        ld a,(bankno)
        ld (0x6000),a
        ld a,(bankno+1)
        ld (0x6001),a
        ld de,0x4040
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,(0x4000)
        ld (palflag),a
        in a,(0xAA)
        and 0xF0
        or 7
        out (0xAA),a
        in a,(0xA9)
        and 4
        jp z,quit
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        ld a,0
        out (0x99),a
        ld a,142
        out (0x99),a
        ld a,0
        out (0x99),a
        ld a,96
        out (0x99),a
        ld b,B0
        ld hl,0x4600
        ld c,0x98
        jp F0body
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
restart_1:
        ld hl,1
        ld (bankno),hl
        ld hl,(nframes)
        ld (fleft),hl
        jp p6_1
setlad_h: ld a,(lvl)
        add a,a
        ld c,a
        ld b,0
        ld hl,ladtab
        add hl,bc
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld (callp0+1),hl
        ld (callp1+1),hl
        ld (callp2+1),hl
        ld (callp3+1),hl
        ld hl,tltab
        add hl,bc
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld (calltlA+1),hl
        ld (calltlB+1),hl
        ret
quit:   xor a
        ld (0x6000),a
        ld (0x6001),a
        ld a,0
        out (0x99),a
        ld a,0x8F
        out (0x99),a
        rst 0
