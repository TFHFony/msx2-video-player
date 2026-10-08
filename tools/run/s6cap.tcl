set throttle off
set out $::env(DUMP_OUT)
set ::wt {}
set ::armed 0
debug set_watchpoint write_mem 0x9800 {} {if {$::armed} {lappend ::wt "[machine_info time] $::wp_last_value"}}
proc rd16 {a} { return [expr {[debug read memory $a] + 256*[debug read memory [expr {$a+1}]]}] }
set last -1
proc poll {} {
  global last out
  set fn [rd16 0xC008]
  if {$fn != $last && $fn < 60000} {
    set last $fn
    if {$fn == 20} { set ::armed 1 }
    if {$fn == 70} { set ::armed 0; set f [open "${out}_cap.txt" w]; foreach r $::wt {puts $f $r}; close $f; exit }
  }
  after time 0.001 poll
}
after time 3 poll
