# Capstone Report — OS Resource Manager

**Student:** Anshuman Malik (2401010086), B.Tech CSE 5th Semester
**Title:** Integrated Python-and-Bash application simulating OS resource management

## 1. Objective
One working application (not scattered programs) that simulates four core OS
resource-management functions, compares their algorithms on common datasets,
and reports analytical results with tables and charts.

## 2. System design
- **Modules:** `scheduling` (process control blocks as dataclasses; event-driven
  simulation), `memory` (frame array + victim-selection policies), `deadlock`
  (need-matrix safety check), `disk` (head-movement accounting), `compare`
  (benchmark harness + matplotlib), `validate` (fail-fast input checks),
  `logger` (timestamped activity log).
- **Bash integration:** `scripts/sysinfo.sh` reads the live Linux process table
  (`ps`) and exports PID/arrival/burst/priority CSV; `main.py` invokes it via
  `subprocess` and schedules the real processes — the simulator touches a real OS.
- **Data flow:** sample_input/*.csv|txt|json → validation → algorithm engine →
  console tables + `output/*.png` charts + `output/activity.log`.

## 3. Algorithms implemented (≥3 modules, as required)
CPU: FCFS, SJF (non-preemptive), Round Robin, Priority. Memory: FIFO, LRU,
Optimal. Deadlock: Banker's safety algorithm. Disk: FCFS, SSTF, SCAN.

## 4. Analysis & comparison (common datasets)
| Scheduling (4 procs) | Avg WT | Avg TAT |
|---|---|---|
| FCFS | 8.75 | 15.25 |
| **SJF** | **7.75** | **14.25** |
| Round Robin (q=2) | 12.75 | 19.25 |
| Priority | 7.75 | 14.25 |

| Paging (13 refs, 3 frames) | Faults |
|---|---|
| FIFO | 10 | LRU | 9 | **Optimal** | **7** |

| Disk (head=53) | Movement |
|---|---|
| FCFS | 640 | **SSTF** | **236** | SCAN | 331 |

Charts: `output/scheduling_comparison.png`, `output/paging_comparison.png`,
`output/disk_comparison.png`.

## 5. Testing & reliability
21 unit tests (`python3 -m unittest discover -s tests -v`) — all pass. Valid:
textbook datasets reproduce known answers (e.g. FIFO=10/LRU=9/Optimal=7;
FCFS disk=640). Invalid: empty process list, negative burst, zero
frames/quantum, allocation > max-need → `OSRMError`/`ValueError` with clear
messages. Boundary: burst == quantum, single disk request, empty reference
string. Idle intervals: Gantt charts record `IDLE` segments (tested for FCFS,
SJF, Round Robin) and the UI reports total idle time. Concurrency demos:
process-creation totals match the closed-form sum, the threaded counter is
exact under a Lock, and IPC messages arrive in order. Every execution is
logged with timestamps.

## 6. Conclusion
The integrated app meets all five phases: modular design, four working OS
modules with real Bash/OS integration, quantitative comparison with
visualizations, hardened input handling with tests, and full documentation.
A Lab 1 concurrency demo (process creation, threads + Lock, Queue-based IPC)
and explicit idle-interval reporting in the scheduling Gantt charts cover the
Lab 1 instructions as well. SJF (tied with Priority) minimizes waiting time, Optimal paging and SSTF disk movement are the most
efficient on the tested workloads — matching theoretical expectations.
