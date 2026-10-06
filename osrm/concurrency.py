"""Lab 1 demo - process creation, threads and IPC using safe Python mechanisms.

Uses only the standard library (multiprocessing / threading). Every demo is
short-lived, deterministic and cleans up after itself: child processes are
joined, queues are closed, no daemons or files are left behind. Each demo
returns its results as a dict so it can be unit-tested.
"""
import multiprocessing as mp
import os
import threading


def _partial_sum(nums, out):
    """Child-process worker: sums its slice and reports back through the queue."""
    out.put({"pid": os.getpid(), "count": len(nums), "total": sum(nums)})


def demo_process_creation(chunks=4, n=1000):
    """Create `chunks` child processes; each sums a slice of 1..n.

    Demonstrates process creation (spawn context works on every platform),
    parent/child PIDs and collecting per-process results.
    """
    data = list(range(1, n + 1))
    size = (len(data) + chunks - 1) // chunks
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    procs = []
    for i in range(chunks):
        sl = data[i * size:(i + 1) * size]
        p = ctx.Process(target=_partial_sum, args=(sl, q), name=f"worker-{i}")
        procs.append(p)
        p.start()
    results = [q.get() for _ in procs]          # one reply per child
    for p in procs:
        p.join()
    q.close()
    q.join_thread()
    total = sum(r["total"] for r in results)
    print(f"\n--- Process creation: {chunks} child processes ---")
    print(f"parent PID: {os.getpid()}")
    for r in sorted(results, key=lambda r: r["pid"]):
        print(f"  child PID {r['pid']}: summed {r['count']} numbers -> {r['total']}")
    print(f"combined total 1..{n} = {total} (expected {n * (n + 1) // 2})")
    return {"parent_pid": os.getpid(), "children": results, "total": total,
            "expected": n * (n + 1) // 2}


def demo_threads(n_threads=4, increments=20000):
    """`n_threads` threads increment one shared counter; a Lock keeps it correct.

    Demonstrates thread creation and synchronisation - without the lock the
    final count would be wrong (race condition).
    """
    counter = [0]
    lock = threading.Lock()

    def work():
        for _ in range(increments):
            with lock:
                counter[0] += 1

    threads = [threading.Thread(target=work, name=f"counter-{i}")
               for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    expected = n_threads * increments
    print(f"\n--- Threads: {n_threads} threads x {increments} increments (with Lock) ---")
    print(f"  final counter = {counter[0]} (expected {expected})")
    print("  synchronised: all increments accounted for, no lost updates")
    return {"threads": n_threads, "counter": counter[0], "expected": expected}


def _producer(q, n):
    """Child-process producer: sends n messages then a None sentinel."""
    for i in range(n):
        q.put(f"msg-{i}")
    q.put(None)


def demo_ipc(n_messages=8):
    """Producer/consumer IPC: a child process sends messages through a Queue.

    Demonstrates inter-process communication - the parent receives every
    message in order until the sentinel arrives.
    """
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    p = ctx.Process(target=_producer, args=(q, n_messages), name="producer")
    p.start()
    received = []
    while True:
        item = q.get()
        if item is None:                        # sentinel: producer is done
            break
        received.append(item)
    p.join()
    q.close()
    q.join_thread()
    print(f"\n--- IPC: producer -> consumer via Queue ({n_messages} messages) ---")
    print(f"  producer PID: {p.pid}, consumer PID: {os.getpid()}")
    print("  received:", ", ".join(received))
    return {"producer_pid": p.pid, "received": received,
            "expected": [f"msg-{i}" for i in range(n_messages)]}


def run_all_demos():
    """Run the three Lab 1 demos back to back."""
    print("\n===== Process creation, threads & IPC (Lab 1) =====")
    r1 = demo_process_creation()
    r2 = demo_threads()
    r3 = demo_ipc()
    print("\nAll three mechanisms demonstrated with safe, short-lived workers.")
    return {"process_creation": r1, "threads": r2, "ipc": r3}
