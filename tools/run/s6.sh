#!/bin/bash
# usage: s6.sh rom prefix [machine]   (player6 timing test)
cd "$(dirname "$0")"
export DUMP_OUT="$(pwd -W)/$2"
rm -f "$2"_*
M=${3:-Philips_NMS_8250}
"/c/Program Files/openMSX/openmsx.exe" -machine $M -cart "$1" -romtype NEO-16 -ext scc -script s6time.tcl >/dev/null 2>&1 &
PID=$!
for i in $(seq 1 120); do sleep 1; [ -f "$2_shot.png" ] && break; done
sleep 1; kill $PID 2>/dev/null; taskkill //F //IM openmsx.exe >/dev/null 2>&1
head -3 "$2_info.txt" 2>/dev/null
