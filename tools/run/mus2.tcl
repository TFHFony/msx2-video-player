set throttle off
set out $::env(DUMP_OUT)
set f [open "${out}_w.txt" w]
set last7c 0
debug set_watchpoint write_io 0x7c {} {set ::last7c $::wp_last_value}
debug set_watchpoint write_io 0x7d {} {
  if {$::last7c >= 0x20 && $::last7c <= 0x28} { puts $::f "[format %.3f [machine_info time]] $::last7c $::wp_last_value" }
}
after time 100 { close $::f; exit }
