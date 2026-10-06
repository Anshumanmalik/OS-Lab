"""CPU scheduling algorithms: FCFS, SJF (non-preemptive), Round Robin, Priority.

Each algorithm returns a ScheduleResult with the Gantt segments and
per-process completion / turnaround / waiting times plus averages.
"""
from dataclasses import dataclass, field
from .validate import check_processes, check_quantum


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int = 0
    remaining: int = field(init=False)

    def __post_init__(self):
        self.remaining = self.burst


@dataclass
class ScheduleResult:
    algorithm: str
    gantt: list          # [(pid, start, end), ...]
    completion: dict     # pid -> completion time
    turnaround: dict     # pid -> turnaround time
    waiting: dict         # pid -> waiting time
    avg_turnaround: float
    avg_waiting: float


def _finish(procs, gantt, completion, name):
    tat = {p.pid: completion[p.pid] - p.arrival for p in procs}
    wt = {p.pid: tat[p.pid] - p.burst for p in procs}
    n = len(procs)
    return ScheduleResult(name, gantt, completion, tat, wt,
                          sum(tat.values()) / n, sum(wt.values()) / n)


def fcfs(procs):
    check_processes(procs)
    ps = sorted(procs, key=lambda p: (p.arrival, p.pid))
    t, gantt, comp = 0, [], {}
    for p in ps:
        if p.arrival > t:
            gantt.append(("IDLE", t, p.arrival))
        t = max(t, p.arrival)
        gantt.append((p.pid, t, t + p.burst))
        t += p.burst
        comp[p.pid] = t
    return _finish(ps, gantt, comp, "FCFS")


def sjf(procs):
    """Shortest Job First, non-preemptive."""
    check_processes(procs)
    ps = sorted(procs, key=lambda p: p.arrival)
    done, t, gantt, comp = set(), 0, [], {}
    while len(done) < len(ps):
        ready = [p for p in ps if p.pid not in done and p.arrival <= t]
        if not ready:
            nxt = min(p.arrival for p in ps if p.pid not in done)
            gantt.append(("IDLE", t, nxt))
            t = nxt
            continue
        p = min(ready, key=lambda p: (p.burst, p.arrival))
        gantt.append((p.pid, t, t + p.burst))
        t += p.burst
        comp[p.pid] = t
        done.add(p.pid)
    return _finish(ps, gantt, comp, "SJF")


def round_robin(procs, quantum):
    check_processes(procs)
    check_quantum(quantum)
    ps = sorted(procs, key=lambda p: (p.arrival, p.pid))
    for p in ps:
        p.remaining = p.burst
    t, gantt, comp, queue, i = 0, [], {}, [], 0
    while len(comp) < len(ps):
        while i < len(ps) and ps[i].arrival <= t:
            queue.append(ps[i]); i += 1
        if not queue:
            gantt.append(("IDLE", t, ps[i].arrival))
            t = ps[i].arrival
            continue
        p = queue.pop(0)
        run = min(quantum, p.remaining)
        gantt.append((p.pid, t, t + run))
        t += run
        p.remaining -= run
        while i < len(ps) and ps[i].arrival <= t:
            queue.append(ps[i]); i += 1
        if p.remaining:
            queue.append(p)
        else:
            comp[p.pid] = t
    return _finish(ps, gantt, comp, f"Round Robin (q={quantum})")


def priority(procs):
    """Non-preemptive priority; lower number = higher priority."""
    check_processes(procs)
    ps = sorted(procs, key=lambda p: p.arrival)
    done, t, gantt, comp = set(), 0, [], {}
    while len(done) < len(ps):
        ready = [p for p in ps if p.pid not in done and p.arrival <= t]
        if not ready:
            nxt = min(p.arrival for p in ps if p.pid not in done)
            gantt.append(("IDLE", t, nxt))
            t = nxt
            continue
        p = min(ready, key=lambda p: (p.priority, p.arrival))
        gantt.append((p.pid, t, t + p.burst))
        t += p.burst
        comp[p.pid] = t
        done.add(p.pid)
    return _finish(ps, gantt, comp, "Priority")
