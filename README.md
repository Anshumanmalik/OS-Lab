# OS Resource Manager

An integrated Python-and-Bash application that simulates major operating-system
resource-management functions and presents analytical results — built for the
Operating Systems lab capstone (zosima.ai).

## Modules (all inside one app, `main.py`)

| # | Module | Algorithms |
|---|--------|-----------|
| 1 | CPU scheduling | FCFS, SJF, Round Robin, Priority — Gantt chart (incl. IDLE intervals), CT/TAT/WT, averages |
| 2 | Page replacement | FIFO, LRU, Optimal — page-fault counts, frame history |
| 3 | Deadlock avoidance | Banker's algorithm — safe/unsafe verdict + safe sequence |
| 4 | Disk scheduling | FCFS, SSTF, SCAN — total head movement, service order |
| 5 | Bash integration | `scripts/sysinfo.sh` harvests **live** Linux processes (`ps`) → scheduled by the Python engine |
| 6 | Comparison lab | every algorithm on common datasets → tables + matplotlib charts in `output/` |
| 7 | Concurrency demo (Lab 1) | process creation (`multiprocessing`), threads (`threading` + Lock), IPC (`Queue` producer/consumer) |

## Run it

```bash
chmod +x scripts/run.sh
./scripts/run.sh
# or directly:
pip install -r requirements.txt
python3 main.py
```

Menu: `1` scheduling · `2` paging · `3` Banker's · `4` disk · `5` live Bash+schedule ·
`6` full comparison (saves charts) · `7` process/threads/IPC demo (Lab 1) · `0` exit.

## Tests (Phase 4)

```bash
python3 -m unittest discover -s tests -v
```

21 test cases cover valid inputs (textbook datasets with known answers),
invalid inputs (empty lists, negative bursts, zero frames/quantum) and
boundary inputs (burst == quantum, single request, empty reference string),
plus idle-interval Gantt segments and the concurrency demos (process-exit
totals, thread-safe counter, ordered IPC delivery).
Every run is append-logged to `output/activity.log`.

## Layout

```
main.py                 integrated menu application
osrm/                   scheduling.py, memory.py, deadlock.py, disk.py,
                        compare.py, validate.py, logger.py
scripts/                run.sh, sysinfo.sh        (Bash integration)
sample_input/           processes.csv, page_refs.txt, bankers.json, disk.txt
tests/                  test_osrm.py              (14 cases)
output/                 charts (*.png), activity.log, traces
REPORT.md               concise capstone report
```

## Sample output trace

```
$ python3 main.py   (option 6)
Algorithm              Avg Waiting   Avg Turnaround
------------------------------------------------------
FCFS                          8.75           15.25
SJF                           7.75           14.25
Round Robin (q=2)             12.75           19.25
Priority                      7.75           14.25
[chart saved] output/scheduling_comparison.png
...
```

*Author: Anshuman Malik (2401010086), B.Tech CSE 5th sem — K.R. Mangalam University.*
