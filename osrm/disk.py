"""Disk scheduling algorithms: FCFS, SSTF, SCAN.

Each returns (total_head_movement, service_order).
"""
from .validate import check_disk


def fcfs_disk(requests, head):
    check_disk(requests, head)
    order, cur, total = [], head, 0
    for r in requests:
        total += abs(r - cur)
        cur = r
        order.append(r)
    return total, order


def sstf_disk(requests, head):
    check_disk(requests, head)
    pending, cur, total, order = list(requests), head, 0, []
    while pending:
        nxt = min(pending, key=lambda r: (abs(r - cur), r))
        total += abs(nxt - cur)
        cur = nxt
        order.append(nxt)
        pending.remove(nxt)
    return total, order


def scan_disk(requests, head, max_cyl=199, direction="up"):
    """SCAN (elevator): service upward to max_cyl, then reverse down."""
    check_disk(requests, head)
    if direction not in ("up", "down"):
        raise ValueError("direction must be 'up' or 'down'")
    up = sorted(r for r in requests if r >= head)
    down = sorted((r for r in requests if r < head), reverse=True)
    order, cur, total = [], head, 0
    first, second = (up, down) if direction == "up" else (down, up)
    for r in first:
        total += abs(r - cur); cur = r; order.append(r)
    # travel to the end before reversing (classic SCAN)
    end = max_cyl if direction == "up" else 0
    total += abs(end - cur); cur = end
    for r in second:
        total += abs(r - cur); cur = r; order.append(r)
    return total, order
