# per-frame timing + SCC write-time statistics for player6
set throttle off
set out $::env(DUMP_OUT)
set last -1
set rec {}
set ::wt {}
set ::armed 0
proc rd16 {a} { return [expr {[debug read memory $a] + 256*[debug read memory [expr {$a+1}]]}] }
proc arm {} {
  debug set_watchpoint write_mem 0x9880 {} {if {$::armed} {lappend ::wt [machine_info time]}}
}
arm
proc poll {} {
  global last rec out
  set fn [rd16 0xC008]
  if {$fn != $last && $fn < 60000} {
    set last $fn
    lappend rec "$fn [machine_info time]"
    if {$fn == 20} { set ::armed 1 }
    if {$fn == 23} { set ::armed 0 }
    if {$fn >= 40} {
      set f [open "${out}_info.txt" w]
      foreach r $rec { puts $f $r }
      close $f
      set f [open "${out}_wt.txt" w]
      foreach r $::wt { puts $f $r }
      close $f
      screenshot "${out}_shot.png"
      exit
    }
  }
  after time 0.001 poll
}
after time 3 poll
