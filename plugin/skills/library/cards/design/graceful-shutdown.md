---
name: graceful-shutdown
title: Graceful shutdown
area: design
tags: [shutdown, signals, draining, deploys, kubernetes, workers]
detect: []
related: [health-checks, background-jobs, timeouts, zero-downtime-migrations, idempotency]
---
On SIGTERM stop taking new work, finish or hand back in-flight work within a deadline, flush, and exit 0.

## Verify
- `kill -TERM PID; echo $?`: send SIGTERM to a local run, then confirm the process exits promptly (check its exit status with `wait` from the launching shell).
- `pytest -q -k shutdown`: in-flight and deadline tests.
- `kubectl rollout status deploy/NAME`: a rolling deploy completes with no 5xx spike (Kubernetes).

## Test first
An in-flight request completes after SIGTERM, new ones are refused, and a stuck one is cut at the deadline.
```python
def test_sigterm_drains_inflight_and_refuses_new(server_proc):
    slow = server_proc.request_async("/slow")          # takes 1s
    server_proc.send_signal(signal.SIGTERM)
    time.sleep(0.1)
    assert server_proc.request("/fast", timeout=1).status in (503, None)  # refused
    assert slow.result(timeout=3).status == 200            # finished
    assert server_proc.wait(timeout=5) == 0

def test_stuck_work_is_abandoned_at_deadline(server_proc):
    server_proc.request_async("/hang"); server_proc.send_signal(signal.SIGTERM)
    assert server_proc.wait(timeout=server_proc.grace + 2) is not None
```

## Do
- Handle SIGTERM (and SIGINT locally) by setting a shutdown flag; do the real work in the main loop or a coroutine, not inside the signal handler.
- Order: fail readiness, wait briefly for load balancers to deregister, stop accepting, drain in-flight, close pools and flush buffers (logs, metrics, producers), exit.
- Use the framework's drain: `server.shutdown(ctx)` in Go, uvicorn and gunicorn graceful timeouts, Node `server.close()` plus tracked connections.
- Give workers a stop deadline; unfinished jobs are released or nacked so another worker retries them, with idempotent handlers.
- Make the grace period (Kubernetes `terminationGracePeriodSeconds`) larger than the drain deadline plus the pre-stop wait.
- Run the app as PID 1 with a signal-forwarding init, or use `exec` in entrypoint scripts so the signal reaches it.
- Release leases, locks and leadership explicitly on the way out.

## Avoid
- Shell entrypoint without `exec`: SIGTERM goes to the shell, the app is killed after the grace period. Use `exec`.
- Closing the listener before readiness fails: requests still routed get errors. Fail readiness first, then drain.
- Heavy work in the signal handler: deadlocks and reentrancy. Set a flag.
- Infinite drain: the orchestrator sends SIGKILL anyway. Enforce a deadline.
- Acking queue messages before processing finishes: they vanish on kill. Ack after completion.

## Review
- [ ] SIGTERM handled; exit code 0 on clean drain.
- [ ] Readiness fails before listener closes.
- [ ] Drain deadline is shorter than the platform grace period.
- [ ] In-flight jobs are finished, released or retried safely.
