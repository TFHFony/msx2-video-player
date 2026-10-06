set throttle off
set out $::env(DUMP_OUT)
set last -1
set rec {}
proc rd16 {a} { return [expr {[debug read memory $a] + 256*[debug read memory [expr {$a+1}]]}] }
proc poll {} {
  global last rec out
  set fn [rd16 0xC004]
  if {$fn != $last && $fn < 60000} {
    set last $fn
    lappend rec "$fn [machine_info time]"
    if {$fn >= 260} {
      set f [open "${out}_info.txt" w]
      foreach r $rec { puts $f $r }
      close $f
      screenshot "${out}_shot.png"
      exit
    }
  }
  after time 0.001 poll
}
after time 3 poll
