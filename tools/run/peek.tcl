set throttle off
set t $::env(DUMP_T)
set out $::env(DUMP_OUT)
proc rd16 {a} { return [expr {[debug read memory $a] + 256*[debug read memory [expr {$a+1}]]}] }
after time $t {
  set f [open "${out}_info.txt" w]
  puts $f "frameno [rd16 0xC004] late [rd16 0xC002] framesleft [rd16 0xC010] strp [rd16 0xC00C] segcur [rd16 0xC00E] ncleft [debug read memory 0xC006] tcount [debug read memory 0xC001] fticks [debug read memory 0xC015] pc [reg pc] dbg [debug read memory 0xC021]"
  close $f
  screenshot "${out}_shot.png"
  exit
}
