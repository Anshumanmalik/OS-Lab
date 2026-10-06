"""Deadlock avoidance - Banker's algorithm (safety check)."""


def bankers_safety(allocation, max_need, available):
    """Return (is_safe, safe_sequence). Matrices are lists of lists."""
    n = len(allocation)          # processes
    m = len(available)           # resource types
    if n == 0 or m == 0:
        raise ValueError("empty allocation/available matrix")
    need = [[max_need[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    if any(v < 0 for row in need for v in row):
        raise ValueError("allocation exceeds max need for some process")
    work, finish = list(available), [False] * n
    seq = []
    while True:
        progressed = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                seq.append(f"P{i}")
                progressed = True
        if not progressed:
            break
    return all(finish), (seq if all(finish) else [])
