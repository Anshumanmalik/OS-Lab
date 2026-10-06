#!/bin/bash
# One-command setup + run for the OS Resource Manager capstone.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -c "import matplotlib" 2>/dev/null || pip install -r requirements.txt
chmod +x scripts/sysinfo.sh
python3 main.py
