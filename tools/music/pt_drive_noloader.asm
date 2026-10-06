; PRO-TRACKER V1.0 music driver, (c) Tyfoon Software 1991.
; Included in this repository with the permission of a former Tyfoon team member.
; Changes for the msx2-video-player project: converted from MSX-assembler (&H/&B) to sjasmplus syntax, and the
; BDOS disk loader (entry CA06h) removed - it is a bare RET here, the song is copied from the ROM into RAM page 0 instead.
; Assemble with sjasmplus (tools/build_pt_driver.py does this from the original PT_DRIVE.ASC) -> pt_drive.bin
;
        DEVICE NOSLOT64K
        ORG   0xCA00

; MUSIC-DRIVER for PRO-TRACKER V1.0
;
; TYFOON-SOFTWARE 1991

DMAADR: EQU   0xC900
L00002: EQU   0x24
L00003: EQU   0x0114
L00004: EQU   0x0134
L00005: EQU   0x013A
L00006: EQU   0x013B
L00007: EQU   0x0141
L00008: EQU   0x0142
L00009: EQU   0x0145

        JP    L00010          ; Driver Entry-Points
        JP    L00011          ;
        JP    L00012          ;
;--
L00013: DB    0               ; Timerbyte (External only)
L00014: DB    0               ; (0=MSX-MUSIC 1=MSX-AUDIO)
L00015: DB    0
L00016: DB    0
;--

L00010: CALL  L00017
        LD    A,(L00008)
        LD    HL,L00009
        LD    E,A
        LD    D,0
        ADD   HL,DE
        LD    (L00018),HL

        LD    A,(L00005)
        LD    B,A
        CALL  L00019
        LD    A,1
        LD    (L00020),A
        LD    HL,L00021
        LD    DE,L00021+1
        LD    BC,L00022-L00021-1
        LD    (HL),0
        LDIR
        LD    A,(L00007)
        CALL  L00023
        CALL  L00024
        LD    A,0xFE
        LD    (L00015),A
        CALL  L00025
        CALL  L00026
        CALL  L00027
        DI
        LD    HL,0xFD9F
        LD    DE,L00028
        LD    BC,5
        LDIR
        LD    A,0xC3
        LD    HL,L00029
        LD    (0xFD9F),A
        LD    (0xFDA0),HL
        EI
        RET
;-
L00011: DI
        LD    HL,L00028
        LD    DE,0xFD9F
        LD    BC,5
        LDIR
        CALL  L00030
        EI
        RET
;-
; >>>>>>>>>>> LOADER <<<<<<<<<

; Het beste is om in uw eigen programma een loadroutine te
; verwerken. Want deze is erg simpel en checkt NIET op disk fouten.

L00012: RET

;----------------------------------------------
L00029: DI
        CALL  L00036
        LD    HL,(L00020)
        DEC   HL
        LD    (L00020),HL
        LD    A,H
        OR    L
        JR    NZ,L00037
        LD    A,(L00038)
        LD    (L00020),A
        LD    HL,L00039
        LD    DE,4
        LD    B,6
        XOR   A
L00040: LD    (HL),A
        ADD   HL,DE
        DJNZ  L00040
        CALL  L00017
        LD    A,(L00041)
        OR    A
        CALL  NZ,L00025
        CALL  L00042
        LD    IX,L00043
        LD    A,(IX+6)
        AND   0x0F
        CALL  NZ,L00044
        LD    A,(IX+6)
        RRA
        RRA
        RRA
        RRA
        AND   0x0F
        CALL  NZ,L00045
        CALL  L00046
        LD    HL,L00016
        DEC   (HL)
        CALL  Z,L00025
        CALL  L00027
L00037: CALL  L00026
        EI
L00028: DB    "TFN91"
        RET


L00044: LD    B,(IX+7)
        CP    0x0F
        JR    Z,L00019
        CP    0x0E
        JR    Z,L00047
        CP    0x0D
        JR    Z,L00048
        CP    0x0C
        JR    Z,L00049
        CP    0x0B
        JR    Z,L00050
        CP    0x0A
        JR    Z,L00051
        CP    0x09
        JR    Z,L00052
L00053: DEC   A
        LD    HL,L00054
        ADD   A,L
        LD    L,A
        JR    NC,L00055
        INC   H
L00055: LD    (HL),B
        LD    A,(L00014)
        OR    A
        JP    NZ,L00056
        LD    HL,L00057+1
        LD    B,6
L00058: LD    A,(HL)
        AND   0xF0
        JR    NZ,L00059
        DEC   HL
        LD    (HL),1
        LD    B,1
        INC   HL
L00059: INC   HL
        INC   HL
        DJNZ  L00058
        RET
L00019: LD    A,B
        OR    A
        RET   Z
        LD    A,(0xFFE8)
        AND   2
        LD    A,B
        JR    Z,L00060
        LD    C,255
L00061: INC   C
        SUB   6
        JR    NC,L00061
        XOR   A
        OR    C
        JR    NZ,L00062
        INC   C
L00062: LD    A,B
        SUB   C
L00060: INC   A
        LD    (L00038),A
        LD    (L00020),A
        RET
L00047: LD    A,B
        LD    (L00013),A
        RET
L00048: LD    A,B
        JP    L00023
L00049: LD    A,B
        OR    A
        JR    NZ,L00063
        IN    A,(0xAA)
        OR    0x40
        OUT   (0xAA),A
        XOR   A
        RET
L00063: IN    A,(0xAA)
        AND   0xBF
        OUT   (0xAA),A
        RET
L00050: LD    A,B
        DEC   A
        LD    (L00015),A
L00051: LD    A,1
        LD    (L00041),A
        RET
L00052: LD    A,B
        AND   0xF0
        CP    0x10
        JR    Z,L00064
        RET   NC
        LD    A,B
        AND   0x0F
        LD    (L00065),A
        RET
L00064: LD    A,B
        AND   0x0F
        NEG
        LD    (L00065),A
        RET


L00036: LD    HL,L00039
        LD    DE,L00066
        LD    B,6
L00067: PUSH  BC
        LD    A,(DE)
        LD    C,A
        INC   DE
        LD    A,(DE)
        LD    B,A
        LD    A,(HL)
        INC   HL
        OR    A
        JR    Z,L00068
        CP    1
        JR    Z,L00069
L00070: LD    A,C
        ADD   A,(HL)
        LD    C,A
        JR    NC,L00071
        INC   B
L00071: INC   HL
        LD    A,B
        ADD   A,(HL)
        LD    B,A
        INC   HL
        XOR   A
        CP    (HL)
        JR    Z,L00072
        DEC   (HL)
        INC   BC
        JR    L00072

L00069: LD    A,C
        SUB   A,(HL)
        LD    C,A
        JR    NC,L00073
        DEC   B
L00073: INC   HL
        LD    A,B
        SUB   A,(HL)
        LD    B,A
        INC   HL
        XOR   A
        CP    (HL)
        JR    Z,L00072
        DEC   (HL)
        DEC   BC
L00072: DEC   DE
        LD    A,C
        LD    (DE),A
        INC   DE
        LD    A,B
        LD    (DE),A
        DEC   HL
        DEC   HL
L00068: INC   DE
        INC   DE
        INC   HL
        INC   HL
        INC   HL
        POP   BC
        DJNZ  L00067
        LD    HL,L00066
        LD    B,6
L00074: PUSH  HL
        LD    E,(HL)
        INC   HL
        LD    A,(HL)
        AND   1
        LD    H,A
        LD    L,E
        LD    DE,0xAD
        OR    A
        SBC   HL,DE
        ADD   HL,DE
        JR    C,L00075
        PUSH  HL
        LD    DE,0x015B
        SBC   HL,DE
        POP   DE
        JR    NC,L00076
L00077: POP   HL
        INC   HL
        JR    L00078
L00075: LD    DE,0xAD
        EX    DE,HL
        OR    A
        SBC   HL,DE
        LD    DE,0x015A
        EX    DE,HL
        SBC   HL,DE
        EX    DE,HL
        POP   HL
        PUSH  HL
        INC   HL
        LD    A,(HL)
        RRA
        DEC   A
        AND   0b00000111
        OR    A
        RLA
        ADD   A,D
        LD    D,A
        JR    L00079
L00076: LD    DE,0xAD
        ADD   HL,DE
        EX    DE,HL
        POP   HL
        PUSH  HL
        INC   HL
        LD    A,(HL)
        RRA
        INC   A
        AND   0b00000111
        RLA
        ADD   A,D
        LD    D,A
L00079: LD    A,(HL)
        BIT   4,A
        JR    Z,L00080
        SET   4,D
L00080: POP   HL
        LD    (HL),E
        INC   HL
        LD    (HL),D
L00078: INC   HL
        INC   HL
        DJNZ  L00074
        RET


L00046: LD    DE,L00066+1
        LD    B,6
L00081: PUSH  BC
        LD    A,(IX)
        OR    A
        JR    Z,L00082
        CP    97
        JR    C,L00083
        CP    0b10000000
        JR    Z,L00084
        CP    0b10100000
        JR    Z,L00085
        CALL  L00086
        JR    L00082
L00083: CALL  L00087
        LD    A,(IX)
        DEC   A
        LD    L,A
        LD    A,(L00065)
        ADD   A,L
L00088: SUB   8*12
        JR    NC,L00088
        ADD   8*12
        PUSH  DE
        DEC   DE
        CALL  L00089
        POP   DE
        LD    A,(DE)
        SET   4,A
        LD    (DE),A
L00082: INC   DE
        INC   DE
        INC   DE
        INC   IX
        POP   BC
        DJNZ  L00081
        RET

L00084: LD    A,(DE)
        AND   0x0F
        LD    (DE),A
        JR    L00082
L00085: LD    A,(DE)
        RES   4,A
        SET   5,A
        LD    (DE),A
        JR    L00082

L00087: LD    C,B
        LD    B,0
        SLA   C
        LD    A,(L00014)
        OR    A
        JR    NZ,L00090
L00091: LD    HL,L00092+13
        SBC   HL,BC
        LD    C,(HL)
        LD    A,(DE)
        AND   0x0F
        JP    L00093
L00090: LD    HL,L00094+13
        SBC   HL,BC
        LD    C,(HL)
        LD    A,(DE)
        AND   0x0F
        SLA   A
        JP    L00095


L00089: PUSH  AF
        LD    HL,L00096
        SLA   A
        ADD   A,L
        LD    L,A
        JR    NC,L00097
        INC   H
L00097: LD    BC,2
        LDIR
        POP   AF
        LD    (DE),A
        RET


L00086: BIT   7,A
        JR    Z,L00098
        BIT   6,A
        JP    Z,L00099
        BIT   5,A
        JR    Z,L00100
        BIT   4,A
        JR    Z,L00101
L00102: LD    HL,L00103+6
        LD    C,B
        LD    B,0
        AND   0x0F
        SBC   HL,BC
        LD    (HL),A
        RET

L00101: LD    HL,L00104+13
        LD    C,B
        LD    B,0
        AND   0x0F
        SBC   HL,BC
        SBC   HL,BC
        LD    (HL),A
        RET

L00100: CPL
        AND   0x0F
        LD    HL,L00057+12
        LD    C,B
        SLA   C
        LD    B,0
        SBC   HL,BC
        LD    (HL),1
        INC   HL
        LD    C,A
        LD    A,(HL)
        AND   0xF0
        ADD   A,C
        LD    (HL),A
        RET

L00098: LD    C,A
        LD    A,(DE)
        AND   0x0F
        LD    (DE),A
        LD    A,C
L00105: LD    HL,L00057+12
        LD    C,B
        SLA   C
        LD    B,0
        AND   0b00011111
        SBC   HL,BC
        LD    (HL),1
        INC   HL
        PUSH  AF
        PUSH  HL
        LD    HL,L00003-1
        ADD   A,L
        LD    L,A
        JR    NC,L00106
        INC   H
L00106: LD    A,0x0F
        SUB   (HL)
        LD    B,A
        POP   HL
        POP   AF
        CP    16
        JR    NC,L00107
        RLA
        RLA
        RLA
        RLA
        AND   0xF0
        ADD   A,B
        LD    (HL),A
        RET
L00107: LD    (HL),B
        RLA
        RLA
        RLA
        RLA
        AND   0xF0
        LD    HL,L00002
        ADD   A,L
        LD    L,A
        JR    NC,L00108
        INC   H
L00108: PUSH  DE
        LD    DE,L00054
        LD    BC,8
        LDIR
        LD    A,(L00014)
        OR    A
        CALL  NZ,L00056
        POP   DE
        RET
L00109: POP   HL
        POP   DE
        RET

L00099: PUSH  DE
        DEC   DE
        EX    AF,AF
        LD    HL,L00039+24
        LD    A,B
        ADD   A,A
        ADD   A,A
        LD    C,A
        LD    B,0
        SBC   HL,BC
        EX    AF,AF
        PUSH  HL
        BIT   5,A
        JR    Z,L00110
L00111: LD    (HL),1
        AND   0b00011111
        LD    B,A
        LD    A,(DE)
        LD    L,A
        INC   DE
        LD    A,(DE)
        AND   0x0F
        LD    H,A
        INC   DE
        LD    A,(DE)
        OR    A
        JR    Z,L00109
        SUB   B
        JR    NC,L00112
        LD    A,0
L00112: PUSH  HL
        PUSH  DE
        LD    DE,L00113
        CALL  L00089
        LD    HL,L00113
        LD    E,(HL)
        INC   HL
        LD    D,(HL)
        INC   HL
        LD    A,(HL)
        POP   HL
        LD    (HL),A
        POP   HL
        JR    L00114

L00110: LD    (HL),2
        AND   0b00011111
        LD    B,A
        LD    A,(DE)
        LD    L,A
        INC   DE
        LD    A,(DE)
        AND   0x0F
        LD    H,A
        INC   DE
        LD    A,(DE)
        OR    A
        JR    Z,L00109
        ADD   A,B
        SUB   8*12
        ADD   A,8*12
        JR    C,L00115
        LD    A,8*12-1
L00115: PUSH  HL
        PUSH  DE
        LD    DE,L00113
        CALL  L00089
        LD    HL,L00113
        LD    E,(HL)
        INC   HL
        LD    D,(HL)
        INC   HL
        LD    A,(HL)
        POP   HL
        LD    (HL),A
        POP   HL
        EX    DE,HL
L00114: LD    B,D
        LD    C,H
        OR    A
        SBC   HL,DE
        LD    A,B
        RRA
        AND   0b00000111
        LD    B,A
        LD    A,C
        RRA
        AND   0b00000111
        SUB   B
        JR    Z,L00116
        LD    DE,0x0153
        LD    B,A
L00117: SBC   HL,DE
        DJNZ  L00117
L00116: LD    A,(L00038)
        LD    C,A
        XOR   A
        LD    D,A
        LD    E,A
        ADD   HL,HL
        ADD   HL,HL
        ADD   HL,HL
        ADD   HL,HL
        LD    B,12
L00118: ADD   HL,HL
        RLA
        SLA   E
        RL    D
        CP    C
        JR    C,L00119
        SUB   A,C
        INC   DE
L00119: DJNZ  L00118
L00120: POP   HL
        INC   HL
        LD    (HL),E
        INC   HL
        LD    (HL),D
        INC   HL
        LD    (HL),A
        POP   DE
        XOR   A
        RET


L00026: LD    A,(L00014)
        OR    A
        JP    NZ,L00121
L00122: LD    HL,L00057
        LD    BC,0x0630
L00123: LD    A,(HL)
        LD    (HL),0
        INC   HL
        OR    A
        JR    Z,L00124
        LD    A,(HL)
        AND   0xF0
        JR    NZ,L00125
        PUSH  BC
        PUSH  HL
        LD    HL,L00054
        LD    BC,0x0800
L00126: LD    A,(HL)
        CALL  L00093
        INC   HL
        INC   C
        DJNZ  L00126
        POP   HL
        POP   BC
L00125: LD    A,(HL)
        CALL  L00093
L00124: INC   HL
        INC   C
        DJNZ  L00123
        LD    HL,L00092
        LD    DE,L00066
        LD    IX,L00103
        LD    IY,L00104
        LD    B,6
L00127: PUSH  BC
        PUSH  DE
        PUSH  HL
        LD    A,(DE)
        LD    L,A
        INC   DE
        LD    A,(DE)
        LD    H,A
        INC   DE
        LD    A,(IX)
        AND   0x07
        LD    C,A
        LD    B,0
        BIT   3,(IX)
        JR    Z,L00128
        SBC   HL,BC
        SBC   HL,BC
L00128: ADD   HL,BC
        INC   (IY)
        BIT   2,(IY)
        INC   IY
        JR    Z,L00129
        LD    A,(IY)
        AND   0b00000111
        LD    C,A
        LD    B,0
        ADD   HL,BC
        BIT   3,(IY)
        JR    Z,L00129
        SBC   HL,BC
        SBC   HL,BC
L00129: EX    DE,HL
        POP   HL
        LD    C,(HL)
        LD    A,E
        CALL  L00093
        INC   HL
        LD    C,(HL)
        LD    A,D
        CALL  L00093
        INC   HL
        POP   DE
L00130: INC   DE
        INC   DE
        INC   DE
        INC   IX
        INC   IY
        POP   BC
        DJNZ  L00127
        RET

L00121: LD    HL,L00057
        LD    B,6
L00131: PUSH  BC
        LD    A,(HL)
        LD    (HL),0
        INC   HL
        OR    A
        JR    Z,L00132
        LD    A,(HL)
        RRA
        RRA
        RRA
        RRA
        AND   0x0F
        LD    C,A
        JR    NZ,L00133
        LD    A,(HL)
        CPL
        AND   0x0F
        PUSH  HL
        CALL  L00134
        POP   HL
        JR    L00132
L00133: LD    A,(HL)
        CPL
        AND   0x0F
        PUSH  HL
        CALL  L00135
        POP   HL
L00132: INC   HL
        POP   BC
        DJNZ  L00131
        LD    HL,L00094
        LD    DE,L00066
        LD    IX,L00103
        LD    IY,L00104
        LD    B,6
L00136: PUSH  BC
        PUSH  DE
        PUSH  HL
        LD    A,(DE)
        LD    L,A
        INC   DE
        LD    A,(DE)
        LD    H,A
        INC   DE
        LD    A,(IX)
        AND   0x07
        LD    C,A
        LD    B,0
        BIT   3,(IX)
        JR    Z,L00137
        SBC   HL,BC
        SBC   HL,BC
L00137: ADD   HL,BC
        INC   (IY)
        BIT   2,(IY)
        INC   IY
        JR    Z,L00138
        LD    A,(IY)
        AND   0b00000111
        LD    C,A
        LD    B,0
        ADD   HL,BC
        BIT   3,(IY)
        JR    Z,L00138
        SBC   HL,BC
        SBC   HL,BC
L00138: ADD   HL,HL
        EX    DE,HL
        POP   HL
        LD    C,(HL)
        LD    A,E
        CALL  L00095
        INC   HL
        LD    C,(HL)
        INC   HL
        LD    A,D
        POP   DE
        CALL  L00095
L00139: INC   DE
        INC   DE
        INC   DE
        INC   IX
        INC   IY
        POP   BC
        DJNZ  L00136
        RET


L00045: LD    HL,L00140-1
        ADD   A,L
        LD    L,A
        JR    NC,L00141
        INC   H
L00141: LD    A,(L00014)
        OR    A
        JR    NZ,L00142
L00143: XOR   A
        LD    C,0x0E
        CALL  L00144
        LD    A,(HL)
        JP    L00093
L00142: XOR   A
        LD    C,0xBD
        CALL  L00145
        LD    A,(HL)
        JP    L00095


L00146: LD    HL,L00057
        LD    B,6
        LD    A,0x10
L00147: LD    (HL),A
        INC   HL
        DJNZ  L00147
        LD    DE,L00004
        LD    B,6
L00148: PUSH  BC
        LD    A,(DE)
        CALL  L00105
        POP   BC
        INC   DE
        DJNZ  L00148
        RET


L00024: LD    A,(L00014)
        OR    A
        JR    NZ,L00149
L00150: LD    HL,L00092+12
        LD    DE,L00006
        LD    B,6
L00151: LD    C,(HL)
        LD    A,(DE)
        CALL  L00093
        INC   HL
        INC   DE
        DJNZ  L00151
        RET
L00149: LD    HL,L00094+12
        LD    DE,L00006
        LD    B,3
L00152: LD    C,(HL)
        INC   HL
        PUSH  HL
        LD    A,(DE)
        INC   DE
        LD    L,A
        LD    A,(DE)
        INC   DE
        AND   0x0F
        LD    H,A
        LD    A,B
        CP    3
        JR    Z,L00153
        ADD   HL,HL
L00153: LD    A,L
        CALL  L00095
        LD    A,H
        POP   HL
        LD    C,(HL)
        INC   HL
        CALL  L00095
        DJNZ  L00152
        LD    C,0x18
        LD    A,8
        CALL  L00145
        INC   C
        JP    L00095


L00023: LD    B,A
        LD    A,(L00014)
        OR    A
        LD    A,B
        JR    NZ,L00154
L00155: RLA
        RLA
        RLA
        RLA
        AND   0xF0
        ADD   A,B
        CPL
        LD    C,0x36
        CALL  L00144
        INC   C
        CALL  L00144
        INC   C
        JP    L00093
L00154: LD    C,0xBD
        XOR   A
        CALL  L00095
        LD    HL,L00156
        LD    A,B
        ADD   A,L
        LD    L,A
        JR    NC,L00157
        INC   H
L00157: LD    C,(HL)
        LD    HL,L00158+2
        LD    DE,8
        LD    B,3
        JR    L00159
L00160: LD    A,(HL)
        AND   0b11000000
        ADD   A,C
        LD    (HL),A
L00159: INC   HL
        LD    A,(HL)
        AND   0b11000000
        ADD   A,C
        LD    (HL),A
        ADD   HL,DE
        DJNZ  L00160
L00161: LD    HL,L00162
        LD    DE,L00158
        LD    B,3*9
L00163: LD    C,(HL)
        LD    A,(DE)
        CALL  L00095
        INC   DE
        INC   HL
        DJNZ  L00163
        RET


L00030: LD    A,(L00014)
        OR    A
        JR    NZ,L00164
L00165: LD    BC,0x0630
        LD    A,0xDF
L00166: CALL  L00093
        INC   C
        DJNZ  L00166
        LD    BC,0x0620
        XOR   A
L00167: CALL  L00093
        INC   C
        DJNZ  L00167
        RET
L00164: LD    HL,L00094
        LD    B,18
        XOR   A
L00168: LD    C,(HL)
        CALL  L00145
        INC   HL
        DJNZ  L00168
        RET

L00042: LD    B,8
        LD    IX,L00043
L00169: LD    A,(L00170)
        OR    A
        JR    Z,L00171
        DEC   A
        LD    (L00170),A
        LD    (IX),0
        INC   IX
        DJNZ  L00169
        RET
L00171: LD    HL,(L00172)
L00173: LD    A,(L00174)
        OR    A
        JR    Z,L00175
        DEC   A
        LD    (L00174),A
        LD    A,(HL)
        INC   HL
        LD    (L00172),HL
        LD    (IX),A
        INC   IX
        DJNZ  L00173
        RET
L00175: LD    A,(L00176)
        XOR   0b00000001
        LD    (L00176),A
        JR    NZ,L00177
        LD    A,(HL)
        INC   HL
        LD    (L00170),A
        LD    (L00172),HL
        JR    L00169
L00177: LD    A,(HL)
        INC   HL
        LD    (L00174),A
        LD    (L00172),HL
        JR    L00173


L00025: LD    A,(L00008)
        LD    B,A
        LD    A,(L00015)
        INC   A
        CP    B
        JR    C,L00178
        CALL  L00146
        XOR   A
L00178: LD    (L00015),A
        LD    HL,L00009
        LD    C,A
        LD    B,0
        ADD   HL,BC
        LD    B,(HL)
        LD    A,B
        OR    A
        LD    HL,(L00018)
        JR    Z,L00179
L00180: LD    E,(HL)
        INC   HL
        LD    D,(HL)
        INC   HL
        ADD   HL,DE
        INC   D
        INC   E
        LD    A,D
        OR    E
        JR    Z,L00181
        DJNZ  L00180
L00179: INC   HL
        INC   HL
        LD    (L00172),HL
        LD    A,64
        LD    (L00016),A
        XOR   A
        LD    (L00041),A
        LD    (L00176),A
        LD    (L00170),A
        LD    (L00174),A
        RET
L00181: LD    A,(L00038)
        LD    H,A
        LD    L,0
        SRL   H
        RR    L
        SRL   H
        RR    L
        LD    (L00020),HL
        LD    A,1
        LD    (L00041),A
        RET

L00144: PUSH  AF
        LD    A,C
        OUT   (0x7C),A
        POP   AF
        OUT   (0x7D),A
        EX    (SP),HL
        EX    (SP),HL
        RET
L00093: PUSH  AF
        LD    A,C
        OUT   (0x7C),A
        POP   AF
        OUT   (0x7D),A
        RET
L00145: PUSH  AF
        LD    A,C
        OUT   (0xC0),A
        POP   AF
        OUT   (0xC1),A
        EX    (SP),HL
        EX    (SP),HL
        RET
L00095: PUSH  AF
        LD    A,C
        OUT   (0xC0),A
        POP   AF
        OUT   (0xC1),A
        RET


L00017: LD    A,(0xFFFF)
        CPL
        LD    (L00182),A
        IN    A,(0xA8)
        LD    (L00183),A
        LD    A,(0xF342)
        LD    H,0x40
        CALL  0x24
        DI
        LD    A,(0xF341)
        AND   3
        LD    E,A
        IN    A,(0xA8)
        AND   0xFC
        ADD   A,E
        OUT   (0xA8),A
        LD    A,(0xF341)
        AND   0x0C
        RRA
        RRA
        LD    E,A
        LD    A,(0xFFFF)
        CPL
        AND   0xFC
        ADD   A,E
        LD    (0xFFFF),A
        RET
L00027: LD    A,(L00183)
        OUT   (0xA8),A
        LD    A,(L00182)
        LD    (0xFFFF),A
        EI
        RET


L00056: LD    HL,L00054
        LD    DE,L00184
        LD    BC,8
        LDIR
        LD    A,(L00054+3)
        AND   0b00000111
        SLA   A
        LD    (L00184+8),A
        LD    HL,L00057+1
        LD    B,6
L00185: LD    A,(HL)
        AND   0xF0
        JR    NZ,L00186
        DEC   HL
        LD    (HL),1
        INC   HL
L00186: INC   HL
        INC   HL
        DJNZ  L00185
        RET


L00134: LD    HL,L00156
        ADD   A,L
        LD    L,A
        JR    NC,L00187
        INC   H
L00187: LD    A,(L00184+3)
        AND   0b11000000
        ADD   A,(HL)
        LD    (L00184+3),A
        LD    HL,L00188+54
        LD    DE,9
        OR    A
L00189: SBC   HL,DE
        DJNZ  L00189
        LD    DE,L00184
        LD    B,9
L00190: LD    C,(HL)
        LD    A,(DE)
        CALL  L00095
        INC   HL
        INC   DE
        DJNZ  L00190
        RET


L00135: LD    HL,L00156
        ADD   A,L
        LD    L,A
        JR    NC,L00191
        INC   H
L00191: LD    A,(HL)
        PUSH  AF
        LD    HL,L00188+54
        LD    DE,9
        OR    A
L00192: SBC   HL,DE
        DJNZ  L00192
        PUSH  HL
        LD    L,C
        LD    H,0
        ADD   HL,HL
        ADD   HL,HL
        ADD   HL,HL
        LD    DE,L00193-8
        ADD   HL,DE
        EX    DE,HL
        POP   HL
        LD    B,3
L00194: LD    C,(HL)
        LD    A,(DE)
        CALL  L00095
        INC   DE
        INC   HL
        DJNZ  L00194
        LD    A,(DE)
        LD    B,A
        AND   0b11000000
        LD    C,A
        POP   AF
        ADD   A,C
        LD    C,(HL)
        CALL  L00095
        INC   DE
        INC   HL
        PUSH  BC
        LD    B,4
L00195: LD    A,(DE)
        LD    C,(HL)
        CALL  L00095
        INC   HL
        INC   DE
        DJNZ  L00195
        POP   AF
        AND   0b00000111
        SLA   A
        LD    C,(HL)
        JP    L00095

L00096: DB    0xAD,0,0xB7,0,0xC2,0,0xCD,0,0xD9,0,0xE6,0
        DB    0xF4,0,0x03,1,0x12,1,0x22,1,0x34,1,0x46,1
        DB    0xAD,2,0xB7,2,0xC2,2,0xCD,2,0xD9,2,0xE6,2
        DB    0xF4,2,0x03,3,0x12,3,0x22,3,0x34,3,0x46,3
        DB    0xAD,4,0xB7,4,0xC2,4,0xCD,4,0xD9,4,0xE6,4
        DB    0xF4,4,0x03,5,0x12,5,0x22,5,0x34,5,0x46,5
        DB    0xAD,6,0xB7,6,0xC2,6,0xCD,6,0xD9,6,0xE6,6
        DB    0xF4,6,0x03,7,0x12,7,0x22,7,0x34,7,0x46,7
        DB    0xAD,8,0xB7,8,0xC2,8,0xCD,8,0xD9,8,0xE6,8
        DB    0xF4,8,0x03,9,0x12,9,0x22,9,0x34,9,0x46,9
        DB    0xAD,10,0xB7,10,0xC2,10,0xCD,10,0xD9,10,0xE6,10
        DB    0xF4,10,0x03,11,0x12,11,0x22,11,0x34,11,0x46,11
        DB    0xAD,12,0xB7,12,0xC2,12,0xCD,12,0xD9,12,0xE6,12
        DB    0xF4,12,0x03,13,0x12,13,0x22,13,0x34,13,0x46,13
        DB    0xAD,14,0xB7,14,0xC2,14,0xCD,14,0xD9,14,0xE6,14
        DB    0xF4,14,0x03,15,0x12,15,0x22,15,0x34,15,0x46,15
L00193: DB    0x61,0x61,0x54,0x27,0xF5,0x7C,0x14,0x17
        DB    0x02,0x41,0x1C,0x25,0xB3,0xC3,0xAA,0xAA
        DB    0x01,0x01,0x4F,0x24,0xB3,0xD3,0x7C,0x77
        DB    0x31,0x71,0x20,0x21,0x51,0x51,0x16,0x16
        DB    0x22,0x71,0x56,0x21,0x78,0x63,0x06,0x06
        DB    0x31,0x34,0x18,0x25,0xF2,0x62,0x15,0x15
        DB    0x71,0x31,0x1E,0x27,0xA1,0xD1,0x16,0x06
        DB    0x23,0x21,0x9C,0x23,0xDC,0x70,0x28,0x26
        DB    0x61,0x31,0x18,0x26,0x65,0xD2,0x15,0x05
        DB    0x61,0x61,0x0E,0x24,0x75,0x94,0x36,0x16
        DB    0x13,0x01,0xC0,0xA0,0xB0,0xB3,0xBA,0xCA
        DB    0x49,0xC1,0x67,0x23,0x93,0xD2,0xBB,0xDB
        DB    0x40,0x44,0x4C,0x65,0xB3,0x93,0xA9,0xA9
        DB    0x11,0x01,0x18,0x22,0x62,0x71,0x91,0xA6
        DB    0x51,0x01,0x16,0x26,0xB1,0xB2,0x96,0x96
L00188: DB    0x20,0x23,0x40,0x43,0x60,0x63,0x80,0x83,0xC0
        DB    0x21,0x24,0x41,0x44,0x61,0x64,0x81,0x84,0xC1
        DB    0x22,0x25,0x42,0x45,0x62,0x65,0x82,0x85,0xC2
        DB    0x28,0x2B,0x48,0x4B,0x68,0x6B,0x88,0x8B,0xC3
        DB    0x29,0x2C,0x49,0x4C,0x69,0x6C,0x89,0x8C,0xC4
        DB    0x2A,0x2D,0x4A,0x4D,0x6A,0x6D,0x8A,0x8D,0xC5
L00092: DB    0x10,0x20,0x11,0x21,0x12,0x22
        DB    0x13,0x23,0x14,0x24,0x15,0x25
        DB    0x16,0x26,0x17,0x27,0x18,0x28
L00094: DB    0xA0,0xB0,0xA1,0xB1,0xA2,0xB2
        DB    0xA3,0xB3,0xA4,0xB4,0xA5,0xB5
        DB    0xA6,0xB6,0xA7,0xB7,0xA8,0xB8
L00140: DB    0b00110000,0b00101000,0b00100100,0b00100010,0b00100001
        DB    0b00111000,0b00110100,0b00110010,0b00110001
        DB    0b00101100,0b00101010,0b00101001
        DB    0b00100110,0b00100101,0b00111100
L00162: DB    0x30,0x33,0x50,0x53,0x70,0x73,0x90,0x93,0xC6
        DB    0x31,0x34,0x51,0x54,0x71,0x74,0x91,0x94,0xC7
        DB    0x32,0x35,0x52,0x55,0x72,0x75,0x92,0x95,0xC8
L00158: DB    0x00,0x00,0xC2,0x00,0xA3,0xA3,0x07,0x07,0x00
        DB    0x01,0x00,0x00,0x00,0xF8,0x97,0x88,0x86,0x00
        DB    0x04,0x81,0xC0,0xC7,0xC7,0xF6,0xB7,0x88,0x00
L00156: DB    63,63-16,63-18,63-20,63-22,63-24,63-26,63-28
        DB    63-33,63-37,63-40,63-45,63-50,63-55,63-60,63-63
L00043: DB    0,0,0,0,0,0,0,0
L00054: DB    0,0,0,0,0,0,0,0
L00184: DB    0,0,0,0,0,0,0,0,0
L00021:
L00057: DB    0,0,0,0,0,0
        DB    0,0,0,0,0,0
L00066: DB    0,0,0,0,0,0
        DB    0,0,0,0,0,0
        DB    0,0,0,0,0,0
L00065: DB    0
L00039: DB    0,0,0,0,0,0,0,0
        DB    0,0,0,0,0,0,0,0
        DB    0,0,0,0,0,0,0,0
L00113: DB    0,0,0
L00103: DB    0,0,0,0,0,0
L00104: DB    0,0,0,0
        DB    0,0,0,0
        DB    0,0,0,0
L00196: DB    0
L00022:
L00020: DW    0
L00038: DB    0
L00172: DW    0
L00041: DB    0
L00183: DB    0
L00182: DB    0
L00018: DW    0
L00176: DB    0
L00170: DB    0
L00174: DB    0

        SAVEBIN "pt_drive.bin",0xCA00,$-0xCA00
