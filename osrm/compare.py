"""Phase 3 - run every algorithm on common datasets, print comparison
tables and save charts under output/."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .scheduling import fcfs, sjf, round_robin, priority
from .memory import fifo, lru, optimal
from .disk import fcfs_disk, sstf_disk, scan_disk

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")


def compare_scheduling(procs, quantum=2):
    results = [fcfs(procs), sjf(procs), round_robin(procs, quantum), priority(procs)]
    print(f"\n{'Algorithm':<22}{'Avg Waiting':>14}{'Avg Turnaround':>16}")
    print("-" * 54)
    for r in results:
        print(f"{r.algorithm:<22}{r.avg_waiting:>14.2f}{r.avg_turnaround:>16.2f}")
    labels = [r.algorithm for r in results]
    x = range(len(labels))
    w = 0.35
    plt.figure(figsize=(9, 5))
    plt.bar([i - w / 2 for i in x], [r.avg_waiting for r in results], w, label="Avg waiting time")
    plt.bar([i + w / 2 for i in x], [r.avg_turnaround for r in results], w, label="Avg turnaround time")
    plt.xticks(list(x), labels, rotation=12)
    plt.ylabel("Time units")
    plt.title("CPU Scheduling - algorithm comparison")
    plt.legend(); plt.tight_layout()
    path = os.path.join(OUT, "scheduling_comparison.png")
    plt.savefig(path); plt.close()
    print(f"[chart saved] {path}")
    return results


def compare_paging(pages, frames):
    data = [("FIFO", fifo(pages, frames)[0]),
            ("LRU", lru(pages, frames)[0]),
            ("Optimal", optimal(pages, frames)[0])]
    print(f"\n{'Algorithm':<12}{'Page faults':>12}")
    print("-" * 26)
    for name, faults in data:
        print(f"{name:<12}{faults:>12}")
    plt.figure(figsize=(7, 4.5))
    plt.bar([n for n, _ in data], [f for _, f in data])
    plt.ylabel("Page faults")
    plt.title(f"Page replacement - {len(pages)} references, {frames} frames")
    plt.tight_layout()
    path = os.path.join(OUT, "paging_comparison.png")
    plt.savefig(path); plt.close()
    print(f"[chart saved] {path}")
    return data


def compare_disk(requests, head):
    data = [("FCFS", fcfs_disk(requests, head)[0]),
            ("SSTF", sstf_disk(requests, head)[0]),
            ("SCAN", scan_disk(requests, head)[0])]
    print(f"\n{'Algorithm':<12}{'Head movement':>15}")
    print("-" * 29)
    for name, mv in data:
        print(f"{name:<12}{mv:>15}")
    plt.figure(figsize=(7, 4.5))
    plt.bar([n for n, _ in data], [m for _, m in data])
    plt.ylabel("Total head movement (cylinders)")
    plt.title(f"Disk scheduling - head starts at {head}")
    plt.tight_layout()
    path = os.path.join(OUT, "disk_comparison.png")
    plt.savefig(path); plt.close()
    print(f"[chart saved] {path}")
    return data
