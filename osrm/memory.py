"""Page replacement algorithms: FIFO, LRU, Optimal.

Each returns (page_faults, history) where history is the list of frame
contents after every reference (None = empty slot).
"""
from .validate import check_frames, check_pages


def _run(pages, frames, pick_victim):
    check_frames(frames)
    check_pages(pages)
    mem, faults, history = [], 0, []
    for pg in pages:
        if pg not in mem:
            faults += 1
            if len(mem) < frames:
                mem.append(pg)
            else:
                mem[pick_victim(mem, pg)] = pg
        history.append(mem + [None] * (frames - len(mem)))
    return faults, history


def fifo(pages, frames):
    order = []          # insertion order of pages currently resident
    def victim(mem, pg):
        v = order.pop(0)
        order.append(pg)
        return mem.index(v)
    faults, history, mem = 0, [], []
    check_frames(frames); check_pages(pages)
    for pg in pages:
        if pg not in mem:
            faults += 1
            if len(mem) < frames:
                mem.append(pg); order.append(pg)
            else:
                mem[victim(mem, pg)] = pg
        history.append(mem + [None] * (frames - len(mem)))
    return faults, history


def lru(pages, frames):
    check_frames(frames); check_pages(pages)
    mem, faults, history, recent = [], 0, [], []
    for pg in pages:
        if pg in mem:
            recent.remove(pg); recent.append(pg)
        else:
            faults += 1
            if len(mem) < frames:
                mem.append(pg)
            else:
                victim = recent.pop(0)
                mem[mem.index(victim)] = pg
            recent.append(pg)
        history.append(mem + [None] * (frames - len(mem)))
    return faults, history


def optimal(pages, frames):
    check_frames(frames); check_pages(pages)
    mem, faults, history = [], 0, []
    for i, pg in enumerate(pages):
        if pg not in mem:
            faults += 1
            if len(mem) < frames:
                mem.append(pg)
            else:
                future = pages[i + 1:]
                # evict page used farthest in future (or never again)
                idx = max(range(len(mem)),
                          key=lambda k: future.index(mem[k]) if mem[k] in future else float('inf'))
                mem[idx] = pg
        history.append(mem + [None] * (frames - len(mem)))
    return faults, history
