#!/bin/bash
# Bash integration: harvest live process data from the Linux kernel's
# process table and export it as scheduler input (pid,arrival,burst,priority).
# Usage: ./scripts/sysinfo.sh [output_csv] [count]
set -euo pipefail
OUT="${1:-sample_input/live_processes.csv}"
N="${2:-8}"
mkdir -p "$(dirname "$OUT")"
echo "pid,arrival,burst,priority" > "$OUT"
# etimes = elapsed seconds; burst derived deterministically so runs are stable
ps -eo pid,etimes --sort=-etimes --no-headers | head -n "$N" | \
  awk '{burst=($2 % 12) + 2; printf "LP%s,0,%d,3\n", $1, burst}' >> "$OUT"
echo "[bash] wrote live process snapshot -> $OUT"
