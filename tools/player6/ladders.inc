B0 equ 6
PERIODHI equ 15
NLEV equ 28
LEVP equ 3
LEVN equ 8
lad0:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        jp nz,lad0
        ret
lad1:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        jp nz,lad1
        ret
lad2:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        jp nz,lad2
        ret
lad3:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        jp nz,lad3
        ret
lad4:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        jp nz,lad4
        ret
lad5:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        jp nz,lad5
        ret
lad6:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        jp nz,lad6
        ret
lad7:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        jp nz,lad7
        ret
lad8:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        jp nz,lad8
        ret
lad9:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        jp nz,lad9
        ret
lad10:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        jp nz,lad10
        ret
lad11:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        jp nz,lad11
        ret
lad12:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        jp nz,lad12
        ret
lad13:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        jp nz,lad13
        ret
lad14:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        jp nz,lad14
        ret
lad15:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        jp nz,lad15
        ret
lad16:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        jp nz,lad16
        ret
lad17:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        jp nz,lad17
        ret
lad18:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        jp nz,lad18
        ret
lad19:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        jp nz,lad19
        ret
lad20:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        jp nz,lad20
        ret
lad21:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        jp nz,lad21
        ret
lad22:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        jp nz,lad22
        ret
lad23:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        jp nz,lad23
        ret
lad24:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        nop
        jp nz,lad24
        ret
lad25:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        nop
        jp nz,lad25
        ret
lad26:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        nop
        jp nz,lad26
        ret
lad27:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
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
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        outi
        nop
        nop
        nop
        nop
        nop
        nop
        jp nz,lad27
        ret
ladderP equ lad0
tl0:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,10
        djnz $
        nop
        jp tl0
tl1:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,10
        djnz $
        nop
        nop
        jp tl1
tl2:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,10
        djnz $
        nop
        nop
        jp tl2
tl3:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,10
        djnz $
        nop
        nop
        jp tl3
tl4:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        jp tl4
tl5:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        jp tl5
tl6:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        jp tl6
tl7:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        jp tl7
tl8:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        nop
        jp tl8
tl9:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        nop
        jp tl9
tl10:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        nop
        jp tl10
tl11:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        nop
        jp tl11
tl12:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        nop
        nop
        jp tl12
tl13:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        nop
        nop
        jp tl13
tl14:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        nop
        nop
        jp tl14
tl15:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,11
        djnz $
        nop
        nop
        jp tl15
tl16:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        jp tl16
tl17:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        jp tl17
tl18:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        jp tl18
tl19:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        nop
        jp tl19
tl20:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        nop
        jp tl20
tl21:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        nop
        jp tl21
tl22:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        nop
        jp tl22
tl23:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        nop
        nop
        jp tl23
tl24:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        nop
        nop
        jp tl24
tl25:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        nop
        nop
        jp tl25
tl26:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,12
        djnz $
        nop
        nop
        jp tl26
tl27:
        ld a,(de)
        inc de
        ld (0x9800),a
        ld (0x9880),a
        in a,(0x99)
        and 0x40
        ret nz
        ld b,13
        djnz $
        jp tl27
tltab:
        dw tl0
        dw tl1
        dw tl2
        dw tl3
        dw tl4
        dw tl5
        dw tl6
        dw tl7
        dw tl8
        dw tl9
        dw tl10
        dw tl11
        dw tl12
        dw tl13
        dw tl14
        dw tl15
        dw tl16
        dw tl17
        dw tl18
        dw tl19
        dw tl20
        dw tl21
        dw tl22
        dw tl23
        dw tl24
        dw tl25
        dw tl26
        dw tl27
ladtab:
        dw lad0
        dw lad1
        dw lad2
        dw lad3
        dw lad4
        dw lad5
        dw lad6
        dw lad7
        dw lad8
        dw lad9
        dw lad10
        dw lad11
        dw lad12
        dw lad13
        dw lad14
        dw lad15
        dw lad16
        dw lad17
        dw lad18
        dw lad19
        dw lad20
        dw lad21
        dw lad22
        dw lad23
        dw lad24
        dw lad25
        dw lad26
        dw lad27
