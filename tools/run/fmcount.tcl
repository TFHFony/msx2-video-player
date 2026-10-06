set throttle off
set n 0
debug set_watchpoint write_io 0x7d {} {incr ::n}
after time 20 { set f [open "$::env(DUMP_OUT)_n.txt" w]; puts $f $::n; close $f; exit }
