---
name: psutil
title: psutil
area: python
tags: [python, psutil, processes, cpu, memory, monitoring, system]
detect: [dep:psutil]
related: [pytest, pytest-mock, freezegun, python-packaging]
---
psutil reads process and system metrics (CPU, memory, disks, processes, network) from Python; it reports the host, and only signals processes when you ask it to.

## Verify
- `python -c "import psutil; print(psutil.__version__)"`: the module imports on this platform.
- `pytest -q -k metrics`: the metric readers pass with psutil's values stubbed.
- `python -m pip check`: no installed package conflicts with psutil's requirement.
- `pip show psutil`: one version is installed for the project's environment.

## Test first
Stub the psutil call and assert what your reader returns.
```python
from types import SimpleNamespace
import psutil
from myapp.metrics import memory_percent

def test_memory_percent_reads_virtual_memory(monkeypatch):
    monkeypatch.setattr(psutil, "virtual_memory", lambda: SimpleNamespace(percent=42.0))
    assert memory_percent() == 42.0
```

## Do
- Sample CPU with an interval: `psutil.cpu_percent(interval=1)`. The no-interval call compares against the previous call, so the first one returns a meaningless 0.0.
- Keep one `psutil.Process` object when you need `Process.cpu_percent()` over time; the first call on a new object returns 0.0.
- Fetch several fields in one pass: `psutil.process_iter(["pid", "name"])`.
- Catch `psutil.NoSuchProcess`, `psutil.AccessDenied` and `psutil.ZombieProcess` around each per-process read.
- Read `disk_usage(path)` for a path's total, used, free and percent; read `virtual_memory().available` for memory you can use.
- Use `Process.children(recursive=True)` to find a process tree before acting on it.

## Avoid
- `cpu_percent()` with no interval as a one-shot number: it is 0.0 on the first call.
- Signalling a stored pid later: the pid may belong to another process now. Check `Process.is_running()` and `create_time()` on the `Process` object first.
- A bare `except:` around process reads: it hides `AccessDenied` and real bugs. Catch the three psutil classes.
- Reading `net_connections()` on macOS without root: it raises `AccessDenied`. Document it as root-only there.
- Reporting host memory from inside a container as the container's limit: psutil reads the host view; cgroup limits need a separate read.
- Tests that assert real host numbers: they differ on every machine. Stub the call or assert ranges.

## Review
- [ ] Each per-process read handles `NoSuchProcess`, `AccessDenied` and `ZombieProcess`.
- [ ] CPU values use an interval or a kept `Process` object, not a single first call.
- [ ] A stored pid is checked with `is_running()` before any signal.
- [ ] Tests stub psutil or assert ranges, never exact host numbers.
- [ ] Root-only and container behavior is documented where the code relies on it.
