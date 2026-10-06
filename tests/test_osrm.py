"""Phase 4 - test cases: valid, invalid and boundary inputs."""
import unittest
from osrm.scheduling import Process, fcfs, sjf, round_robin, priority
from osrm.concurrency import demo_process_creation, demo_threads, demo_ipc
from osrm.memory import fifo, lru, optimal
from osrm.deadlock import bankers_safety
from osrm.disk import fcfs_disk, sstf_disk, scan_disk
from osrm.validate import OSRMError

P = [Process("P1", 0, 8, 2), Process("P2", 1, 4, 1),
     Process("P3", 2, 9, 3), Process("P4", 3, 5, 2)]


class TestScheduling(unittest.TestCase):
    def test_fcfs_order(self):
        r = fcfs(P)
        self.assertEqual([p for p, _, _ in r.gantt], ["P1", "P2", "P3", "P4"])
        self.assertAlmostEqual(r.avg_waiting, 8.75)

    def test_sjf_picks_shortest(self):
        r = sjf(P)  # P2(4) before P3(9) once arrived
        order = [p for p, _, _ in r.gantt]
        self.assertLess(order.index("P2"), order.index("P3"))

    def test_rr_quantum_boundary(self):
        r = round_robin([Process("A", 0, 4)], 4)  # burst == quantum
        self.assertEqual(len(r.gantt), 1)
        self.assertEqual(r.completion["A"], 4)

    def test_priority_order(self):
        r = priority(P)  # P2 has highest priority (1)
        self.assertEqual(r.gantt[0][0], "P1")  # P1 arrives first at t=0 alone
        r2 = priority([Process("X", 0, 5, 2), Process("Y", 0, 5, 1)])
        self.assertEqual(r2.gantt[0][0], "Y")

    def test_invalid(self):
        with self.assertRaises(OSRMError):
            fcfs([])
        with self.assertRaises(OSRMError):
            fcfs([Process("B", 0, -3)])
        with self.assertRaises(OSRMError):
            round_robin(P, 0)


class TestIdleIntervals(unittest.TestCase):
    def test_fcfs_idle_gap(self):
        r = fcfs([Process("A", 0, 2), Process("B", 5, 3)])
        self.assertIn(("IDLE", 2, 5), r.gantt)
        self.assertEqual(r.completion["B"], 8)
        self.assertAlmostEqual(r.avg_waiting, 0.0)

    def test_sjf_idle_at_start(self):
        r = sjf([Process("A", 3, 2)])
        self.assertEqual(r.gantt[0], ("IDLE", 0, 3))
        self.assertEqual(r.completion["A"], 5)

    def test_rr_idle_gap(self):
        r = round_robin([Process("A", 0, 2), Process("B", 6, 2)], 2)
        self.assertIn(("IDLE", 2, 6), r.gantt)

    def test_no_idle_when_busy(self):
        r = fcfs(P)  # arrivals 0..3, CPU never idle
        self.assertNotIn("IDLE", [pid for pid, _, _ in r.gantt])


class TestConcurrency(unittest.TestCase):
    def test_process_creation_total(self):
        r = demo_process_creation(chunks=2, n=100)
        self.assertEqual(r["total"], 5050)
        self.assertEqual(r["total"], r["expected"])
        self.assertEqual(len(r["children"]), 2)
        self.assertTrue(all(c["pid"] != r["parent_pid"] for c in r["children"]))

    def test_threads_counter(self):
        r = demo_threads(n_threads=2, increments=5000)
        self.assertEqual(r["counter"], 10000)
        self.assertEqual(r["counter"], r["expected"])

    def test_ipc_order(self):
        r = demo_ipc(n_messages=5)
        self.assertEqual(r["received"], r["expected"])
        self.assertEqual(len(r["received"]), 5)


class TestPaging(unittest.TestCase):
    REF = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]

    def test_textbook_faults(self):
        self.assertEqual(fifo(self.REF, 3)[0], 10)
        self.assertEqual(lru(self.REF, 3)[0], 9)
        self.assertEqual(optimal(self.REF, 3)[0], 7)

    def test_boundary(self):
        self.assertEqual(fifo([], 3)[0], 0)          # empty reference string
        self.assertEqual(fifo([1, 1, 1], 1)[0], 1)   # single frame, repeats

    def test_invalid(self):
        with self.assertRaises(OSRMError):
            fifo(self.REF, 0)
        with self.assertRaises(OSRMError):
            lru([-1, 2], 3)


class TestDeadlock(unittest.TestCase):
    ALLOC = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    MAX = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]

    def test_safe(self):
        safe, seq = bankers_safety(self.ALLOC, self.MAX, [3, 3, 2])
        self.assertTrue(safe)
        self.assertEqual(len(seq), 5)

    def test_unsafe(self):
        safe, seq = bankers_safety(self.ALLOC, self.MAX, [0, 0, 0])
        self.assertFalse(safe)
        self.assertEqual(seq, [])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            bankers_safety([[9, 9, 9]], [[1, 1, 1]], [1, 1, 1])  # alloc > max


class TestDisk(unittest.TestCase):
    REQ = [98, 183, 37, 122, 14, 124, 65, 67]

    def test_textbook(self):
        self.assertEqual(fcfs_disk(self.REQ, 53)[0], 640)
        self.assertEqual(sstf_disk(self.REQ, 53)[0], 236)

    def test_boundary(self):
        total, order = fcfs_disk([100], 53)
        self.assertEqual((total, order), (47, [100]))

    def test_invalid(self):
        with self.assertRaises(OSRMError):
            fcfs_disk([], 53)
        with self.assertRaises(OSRMError):
            sstf_disk([10, -5], 53)


if __name__ == "__main__":
    unittest.main(verbosity=2)
