"""Generates frame_h.inc for player6 variant H: the per-frame housekeeping (table flip, bank switch, level control,
palette, ESC) is split into pieces that each run in their own sample slot, so the SCC sample clock never stops.
Cycle counts include the one MSX wait state per opcode fetch (M1)."""
import re

TP = 240          # nominal period of a housekeeping slot in cycles (a ladder slot is 230..265 depending on the level)
SAMP_C = 43
NL = chr(10)


def cyc(ins):
    i = re.sub(r'\s+', ' ', ins.strip().lower())
    op = i.split(' ')[0]
    if i in ('nop', 'rra', 'or a', 'ex de,hl'):
        return 5
    if i in ('inc hl', 'dec hl'):
        return 7
    if i in ('inc b', 'dec b', 'inc a', 'dec a', 'add a,a', 'add a,b', 'xor a', 'or l', 'or h'):
        return 5
    if i == 'ret':
        return 11
    if re.match(r'ld [abcdehl],[abcdehl]$', i):
        return 5
    if re.match(r'ld [abcdehl],\(hl\)$', i) or i == 'ld (hl),a':
        return 8
    if re.match(r'ld (hl|de|bc),[^(]', i):
        return 11
    if re.match(r'ld [abc],[^(]', i) or i == 'ld h,0':
        return 8
    if re.match(r'ld a,\(.*\)$', i):
        return 14
    if re.match(r'ld \(.*\),a$', i):
        return 14
    if re.match(r'ld hl,\(.*\)$', i) or re.match(r'ld \(.*\),hl$', i):
        return 17
    if re.match(r'ld (de|bc),\(.*\)$', i) or re.match(r'ld \(.*\),(de|bc)$', i):
        return 22
    if re.match(r'out \(.*\),a$', i) or re.match(r'in a,\(.*\)$', i):
        return 12
    if re.match(r'(and|or|cp|sub|xor) ', i):
        return 8
    if re.match(r'add hl,(bc|de)$', i):
        return 12
    if op == 'jr':
        return 13
    if op == 'jp':
        return 11
    if op == 'call':
        return 18
    raise ValueError('no cycle count for ' + ins)


def pad_to(total, work_cycles):
    n = max(0, round((total - work_cycles) / 5))
    return ['        nop'] * n


def block(lines):
    return sum(cyc(x) for x in lines if x.strip() and not x.strip().endswith(':'))


SAMP = ['        ld a,(de)', '        inc de', '        ld (0x9800),a', '        ld (0x9880),a']


def vreg(val, reg):
    return [f'        ld a,{val}', '        out (0x99),a', f'        ld a,{0x80 + reg}', '        out (0x99),a']


def seta(r14, lo, hi):
    return vreg(r14, 14) + [f'        ld a,{lo}', '        out (0x99),a', f'        ld a,{hi | 0x40}', '        out (0x99),a']


def slot(work, wc=None):
    w = block(work) if wc is None else wc
    return list(SAMP) + work + pad_to(TP - SAMP_C, w)


FLIP = {0: (0x07, 0x7F, 0x01), 1: (0x0F, 0x7F, 0x02)}
PATT = {0: (0, 0x00, 0x20), 1: (1, 0x00, 0x20)}      # R#14, VRAM low, high of the pattern table of each set


def post(c, v):
    n = 1 - c
    L = [f'; ------------- after set {c} has been written: flip to it, prepare set {n}']
    L += pad_to(TP, 32)          # completes the slot in which the tail routine saw the retrace edge
    r4, r3, r10 = FLIP[c]
    L += slot(vreg(r4, 4) + vreg(r3, 3) + vreg(r10, 10) + ['        ld (tailend),de'])
    w = ['        ld hl,(tailend)', '        ld bc,-(0x4040+1202)', '        add hl,bc', '        ld a,(lvl)', '        ld b,a',
         '        ld a,h', '        or a', f'        jr nz,.ao{c}', '        ld a,l', '        cp 100', f'        jr nc,.ao{c}',
         '        cp 3', f'        jr c,.al{c}', '        cp 10', f'        jr c,.ak{c}',
         f'.am{c}:', '        ld a,b', '        cp NLEV-1', f'        jr nc,.ak{c}', '        inc b', f'        jr .ak{c}',
         f'.al{c}:', '        ld a,b', '        or a', f'        jr z,.ak{c}', '        dec b', f'        jr .ak{c}',
         f'.ao{c}:', '        ld a,b', '        sub 3', f'        jr nc,.ap{c}', '        xor a', f'.ap{c}:', '        ld b,a',
         f'.ak{c}:', '        ld a,b', '        ld (lvl),a']
    wc = block(w[:15]) + block(['        ld a,b', '        cp 1', '        jr nc,.x', '        inc b', '        jr .x',
                                '        ld a,b', '        ld (lvl),a'])
    L += list(SAMP) + w + pad_to(TP - SAMP_C, wc)
    w = ['        ld a,(lvl)', '        add a,a', '        ld c,a', '        ld b,0', '        ld hl,ladtab', '        add hl,bc',
         '        ld a,(hl)', '        inc hl', '        ld h,(hl)', '        ld l,a'] + \
        [f'        ld (callp{i}+1),hl' for i in range(4)]
    L += slot(w)
    w = ['        ld hl,tltab', '        add hl,bc', '        ld a,(hl)', '        inc hl', '        ld h,(hl)', '        ld l,a',
         '        ld (calltlA+1),hl', '        ld (calltlB+1),hl']
    L += slot(w)
    w = ['        ld a,(rg1)', '        out (0x99),a', '        ld a,0x81', '        out (0x99),a',
         '        ld hl,(bankno)', '        inc hl', '        ld (bankno),hl',
         '        ld hl,(fleft)', '        dec hl', '        ld (fleft),hl', '        ld a,h', '        or l', f'        jp z,restart_{c}']
    L += slot(w)
    L += [f'p6_{c}:'] + list(SAMP)
    L += ['        ld a,(palflag)', '        rra', f'        jr nc,.np{c}'] + vreg(0, 16) + \
         ['        ld hl,0x4001', '        ld bc,0x209A', '        otir', f'.np{c}:']
    sw = ['        ld a,(bankno)', '        ld (0x6000),a', '        ld a,(bankno+1)', '        ld (0x6001),a', '        ld de,0x4040']
    L += sw
    wc = block(['        ld a,(palflag)', '        rra', '        jr nc,.x']) + block(sw)
    L += pad_to(TP - SAMP_C, wc)
    L += slot(['        ld a,(0x4000)', '        ld (palflag),a', '        in a,(0xAA)', '        and 0xF0', '        or 7',
               '        out (0xAA),a', '        in a,(0xA9)', '        and 4', '        jp z,quit'])
    r14, lo, hi = PATT[n]
    L += slot(seta(r14, lo, hi) + ['        ld b,B0', '        ld hl,0x4600', '        ld c,0x98', f'        jp F{n}body'])
    L += [f'restart_{c}:', '        ld hl,1', '        ld (bankno),hl', '        ld hl,(nframes)', '        ld (fleft),hl',
          f'        jp p6_{c}']
    return L


def frame_h(v=None):
    L = ['restart:', '        ld hl,1', '        ld (bankno),hl', '        ld hl,(nframes)', '        ld (fleft),hl',
         'firstframe:', '        call setlad_h',
         '        ld a,(bankno)', '        ld (0x6000),a', '        ld a,(bankno+1)', '        ld (0x6001),a',
         '        ld a,(0x4000)', '        ld (palflag),a', '        ld de,0x4042', '        ld hl,0x4600', '        ld c,0x98']
    L += seta(*PATT[0]) + ['        ld b,B0', '        jp F0body']
    L += ['F0body:', 'callp0: call ladderP'] + seta(1, 0x00, 0x00) + ['        ld b,B0', 'callp1: call ladderP', 'tailA:',
                                                                     'calltlA: call tl0']
    L += post(0, v)
    L += ['F1body:', 'callp2: call ladderP'] + seta(2, 0x00, 0x00) + ['        ld b,B0', 'callp3: call ladderP', 'tailB:',
                                                                     'calltlB: call tl0']
    L += post(1, v)
    L += ['setlad_h: ld a,(lvl)', '        add a,a', '        ld c,a', '        ld b,0', '        ld hl,ladtab', '        add hl,bc',
          '        ld a,(hl)', '        inc hl', '        ld h,(hl)', '        ld l,a'] + \
         [f'        ld (callp{i}+1),hl' for i in range(4)] + \
         ['        ld hl,tltab', '        add hl,bc', '        ld a,(hl)', '        inc hl', '        ld h,(hl)', '        ld l,a',
          '        ld (calltlA+1),hl', '        ld (calltlB+1),hl', '        ret']
    L += ['quit:   xor a', '        ld (0x6000),a', '        ld (0x6001),a', '        ld a,0', '        out (0x99),a',
          '        ld a,0x8F', '        out (0x99),a', '        rst 0']
    return NL.join(L) + NL
