#!/usr/bin/env python3
"""OS Resource Manager - integrated menu-driven capstone application.

One app, four OS resource-management modules (CPU scheduling, paging,
deadlock avoidance, disk scheduling) + Bash integration + comparisons
+ a Lab 1 demo of process creation, threads and IPC.
"""
import csv, json, os, subprocess, sys

from osrm.scheduling import Process, fcfs, sjf, round_robin, priority
from osrm.memory import fifo, lru, optimal
from osrm.deadlock import bankers_safety
from osrm.disk import fcfs_disk, sstf_disk, scan_disk
from osrm.compare import compare_scheduling, compare_paging, compare_disk
from osrm.concurrency import run_all_demos
from osrm.logger import get_logger
from osrm.validate import OSRMError

BASE = os.path.dirname(os.path.abspath(__file__))
log = get_logger()

SCHED = {"1": ("FCFS", fcfs), "2": ("SJF", sjf), "4": ("Priority", priority)}
PAGE = {"1": ("FIFO", fifo), "2": ("LRU", lru), "3": ("Optimal", optimal)}
DISK = {"1": ("FCFS", fcfs_disk), "2": ("SSTF", sstf_disk), "3": ("SCAN", scan_disk)}


def load_processes(path):
    procs = []
    with open(path) as f:
        for row in csv.DictReader(f):
            procs.append(Process(row["pid"].strip(), int(row["arrival"]),
                                 int(row["burst"]), int(row.get("priority", 0))))
    return procs


def show_schedule(res):
    print(f"\n--- {res.algorithm} ---")
    print("Gantt:", " | ".join(f"{pid}[{s}-{e}]" for pid, s, e in res.gantt))
    idle = sum(e - s for pid, s, e in res.gantt if pid == "IDLE")
    if idle:
        print(f"CPU idle intervals total: {idle} time units")
    print(f"{'PID':<8}{'CT':>6}{'TAT':>6}{'WT':>6}")
    for pid in res.completion:
        print(f"{pid:<8}{res.completion[pid]:>6}{res.turnaround[pid]:>6}{res.waiting[pid]:>6}")
    print(f"Avg turnaround = {res.avg_turnaround:.2f}, Avg waiting = {res.avg_waiting:.2f}")


def menu_scheduling():
    path = os.path.join(BASE, "sample_input", "processes.csv")
    procs = load_processes(path)
    print("\n[1] FCFS  [2] SJF  [3] Round Robin  [4] Priority")
    c = input("Choose: ").strip()
    try:
        if c == "3":
            q = int(input("Quantum: "))
            res = round_robin(procs, q)
        else:
            name, fn = SCHED[c]
            res = fn(procs)
        show_schedule(res)
        log.info("scheduling ran: %s", res.algorithm)
    except (KeyError, OSRMError, ValueError) as e:
        print("Input error:", e); log.warning("scheduling input error: %s", e)


def menu_paging():
    path = os.path.join(BASE, "sample_input", "page_refs.txt")
    pages = [int(x) for x in open(path).read().split()]
    frames = int(input("Frames (default 3): ") or 3)
    print("\n[1] FIFO  [2] LRU  [3] Optimal")
    c = input("Choose: ").strip()
    try:
        name, fn = PAGE[c]
        faults, hist = fn(pages, frames)
        print(f"\n--- {name}: {faults} page faults ---")
        for i, state in enumerate(hist[:12]):
            print(f"ref {pages[i]:>3} -> {state}")
        if len(hist) > 12:
            print(f"... ({len(hist) - 12} more references)")
        log.info("paging ran: %s faults=%d", name, faults)
    except (KeyError, OSRMError, ValueError) as e:
        print("Input error:", e); log.warning("paging input error: %s", e)


def menu_deadlock():
    data = json.load(open(os.path.join(BASE, "sample_input", "bankers.json")))
    try:
        safe, seq = bankers_safety(data["allocation"], data["max"], data["available"])
        print("\nSystem is", "SAFE" if safe else "UNSAFE (deadlock possible)")
        if safe:
            print("Safe sequence:", " -> ".join(seq))
        log.info("bankers ran: safe=%s", safe)
    except (ValueError, KeyError) as e:
        print("Input error:", e); log.warning("bankers input error: %s", e)


def menu_disk():
    parts = open(os.path.join(BASE, "sample_input", "disk.txt")).read().split()
    head, reqs = int(parts[0]), [int(x) for x in parts[1:]]
    print("\n[1] FCFS  [2] SSTF  [3] SCAN")
    c = input("Choose: ").strip()
    try:
        name, fn = DISK[c]
        total, order = fn(reqs, head)
        print(f"\n--- {name}: head movement = {total} cylinders ---")
        print("Order:", order)
        log.info("disk ran: %s movement=%d", name, total)
    except (KeyError, OSRMError, ValueError) as e:
        print("Input error:", e); log.warning("disk input error: %s", e)


def menu_live():
    """Bash integration: harvest real processes, then schedule them."""
    out = os.path.join(BASE, "sample_input", "live_processes.csv")
    r = subprocess.run(["bash", os.path.join(BASE, "scripts", "sysinfo.sh"), out],
                       capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    procs = load_processes(out)
    for res in (fcfs(procs), sjf(procs), round_robin(procs, 2)):
        print(f"{res.algorithm:<18} avg WT={res.avg_waiting:.2f}  avg TAT={res.avg_turnaround:.2f}")
    log.info("live bash+schedule ran on %d processes", len(procs))


def menu_compare():
    procs = load_processes(os.path.join(BASE, "sample_input", "processes.csv"))
    pages = [int(x) for x in open(os.path.join(BASE, "sample_input", "page_refs.txt")).read().split()]
    parts = open(os.path.join(BASE, "sample_input", "disk.txt")).read().split()
    compare_scheduling(procs)
    compare_paging(pages, 3)
    compare_disk([int(x) for x in parts[1:]], int(parts[0]))
    log.info("full comparison ran; charts saved")


def menu_concurrency():
    """Lab 1: demonstrate process creation, threads and IPC."""
    try:
        run_all_demos()
        log.info("concurrency demos ran: processes + threads + IPC")
    except (OSRMError, ValueError, OSError) as e:
        print("Demo error:", e); log.warning("concurrency demo error: %s", e)


def main():
    items = [
        ("CPU scheduling simulator", menu_scheduling),
        ("Page replacement simulator", menu_paging),
        ("Banker's algorithm (deadlock avoidance)", menu_deadlock),
        ("Disk scheduling simulator", menu_disk),
        ("Live system processes via Bash + schedule them", menu_live),
        ("Run full comparison (tables + charts)", menu_compare),
        ("Process creation, threads & IPC demo (Lab 1)", menu_concurrency),
    ]
    while True:
        print("\n===== OS Resource Manager =====")
        for i, (name, _) in enumerate(items, 1):
            print(f" {i}. {name}")
        print(" 0. Exit")
        c = input("Choose: ").strip()
        if c == "0":
            print("Bye!"); break
        try:
            items[int(c) - 1][1]()
        except (IndexError, ValueError):
            print("Please choose a valid option.")


if __name__ == "__main__":
    main()
