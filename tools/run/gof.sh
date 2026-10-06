#!/bin/bash
cd "$(dirname "$0")"
export DUMP_T=0 DUMP_OUT="$(pwd -W)/$2"
rm -f "$2"_*
"/c/Program Files/openMSX/openmsx.exe" -machine Philips_NMS_8250 -cart "$1" -romtype NEO-8 -script ftime.tcl >/dev/null 2>&1 &
PID=$!
for i in $(seq 1 120); do sleep 1; [ -f "$2_shot.png" ] && break; done
sleep 1; kill $PID 2>/dev/null; taskkill //F //IM openmsx.exe >/dev/null 2>&1
python - "$2_info.txt" <<'PY'
import sys,numpy as np
rows=[l.split() for l in open(sys.argv[1])]
fn=np.array([int(r[0]) for r in rows]); t=np.array([float(r[1]) for r in rows])
m=fn>=100
d=np.diff(t[m])*1000
print('frames',len(d),'mean %.1f ms  median %.1f  p90 %.1f  max %.1f'%(d.mean(),np.median(d),np.percentile(d,90),d.max()))
PY
