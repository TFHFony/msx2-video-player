#!/bin/bash
# usage: go.sh rom seconds prefix [script]
cd "$(dirname "$0")"
export DUMP_T=$2 DUMP_OUT="$(pwd -W)/$3"
SCRIPT=${4:-peek.tcl}
rm -f "$3"_*
"/c/Program Files/openMSX/openmsx.exe" -machine Philips_NMS_8250 -cart "$1" -romtype NEO-8 -script $SCRIPT >/dev/null 2>&1 &
PID=$!
for i in $(seq 1 90); do sleep 1; [ -f "$3_shot.png" ] && break; done
sleep 1; kill $PID 2>/dev/null; taskkill //F //IM openmsx.exe >/dev/null 2>&1
cat "$3_info.txt" 2>/dev/null
