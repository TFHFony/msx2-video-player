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
