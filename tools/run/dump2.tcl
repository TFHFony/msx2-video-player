set throttle off
set out $::env(DUMP_OUT)
set target $::env(TARGET)
proc rd16 {a} { return [expr {[debug read memory $a] + 256*[debug read memory [expr {$a+1}]]}] }
proc finish {} {
  global out
  set f [open "${out}_info.txt" w]
  puts $f "frameno [rd16 0xC004]"
  close $f
  set f [open "${out}_vram.bin" wb]
  puts -nonewline $f [debug read_block VRAM 0 65536]
  close $f
  screenshot "${out}_shot.png"
  exit
}
proc waitack {} { if {[debug read memory 0xC021] == 1} { after time 0.02 finish } else { after time 0.02 waitack } }
proc poll {} {
  global target
  set fn [rd16 0xC004]
  if {$fn >= $target - 1 && $fn < 60000} { debug write memory 0xC020 1; waitack } else { after time 0.003 poll }
}
after time 4 poll
