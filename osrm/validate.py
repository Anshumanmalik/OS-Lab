"""Input validation helpers - every public entry point validates first."""


class OSRMError(ValueError):
    """Raised for invalid / out-of-range inputs."""


def check_processes(procs):
    if not procs:
        raise OSRMError("process list is empty")
    for p in procs:
        if p.arrival < 0:
            raise OSRMError(f"{p.pid}: arrival time cannot be negative")
        if p.burst <= 0:
            raise OSRMError(f"{p.pid}: burst time must be positive")
        if p.priority < 0:
            raise OSRMError(f"{p.pid}: priority cannot be negative")


def check_quantum(q):
    if q <= 0:
        raise OSRMError("time quantum must be positive")


def check_frames(frames):
    if not isinstance(frames, int) or frames < 1:
        raise OSRMError("number of frames must be a positive integer")


def check_pages(pages):
    for pg in pages:
        if not isinstance(pg, int) or pg < 0:
            raise OSRMError(f"invalid page reference: {pg!r}")


def check_disk(requests, head):
    if not requests:
        raise OSRMError("request queue is empty")
    if head < 0:
        raise OSRMError("head position cannot be negative")
    for r in requests:
        if r < 0:
            raise OSRMError(f"invalid cylinder request: {r}")
