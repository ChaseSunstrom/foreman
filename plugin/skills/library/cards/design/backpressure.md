---
name: backpressure
title: Backpressure
area: design
tags: [backpressure, queues, load-shedding, flow-control, streams, overload]
detect: []
related: [rate-limiter-algorithms, bulkheads, circuit-breaker, timeouts, background-jobs]
---
When consumers are slower than producers, slow the producer, drop or shed work on purpose, and bound every queue.

## Verify
- `pytest -q -k "backpressure or overload"`: bounded queue and shedding tests.
- `git grep -nE "Queue\(\)|queue\.Queue\(\)|make\(chan [a-zA-Z.]+\)\s*$" -- src`: unbounded queues are findings; each needs a maxsize or capacity.
- `go test -race -count=1 ./...`: channel-based pipelines are race free (Go stacks).

## Test first
Push far more than capacity with a stalled consumer: memory stays bounded and the producer is told.
```python
def test_bounded_queue_pushes_back_instead_of_growing():
    q = BoundedQueue(maxsize=10)
    accepted = 0
    for i in range(1000):
        try: q.put_nowait(i); accepted += 1
        except QueueFull: pass
    assert accepted == 10 and q.qsize() == 10

def test_server_sheds_load_with_retry_after(server):
    server.stall_workers()
    codes = [server.get("/work").status_code for _ in range(200)]
    assert 503 in codes or 429 in codes
    assert server.get("/work").headers.get("Retry-After")
```

## Do
- Bound every queue, channel and buffer; decide the full-queue policy: block the producer, reject (503 or 429 with `Retry-After`), drop oldest, or drop newest.
- Prefer pull-based consumption (consumers request N) or credit-based flow control (Reactive Streams `request(n)`, gRPC flow control, TCP windows).
- Limit in-flight work per consumer (prefetch count in AMQP, `max.poll.records` in Kafka) and tune it down.
- Shed load early at the edge, favouring cheap rejection over slow failure; prioritise critical traffic.
- Make clients cooperate: honour `Retry-After`, backoff with jitter.
- Alert on queue depth and age, not just throughput.
- Test with a deliberately slow consumer.

## Avoid
- Unbounded queues "to absorb spikes": they turn overload into latency and an out-of-memory crash. Bound and shed.
- Infinite retries from clients on rejection: retry storms. Use backoff, jitter and budgets.
- Blocking the producer when the producer is a request thread: threads exhaust. Reject fast instead.
- Dropping silently: invisible data loss. Count and log drops.
- Only scaling consumers up: the bottleneck moves downstream. Find the true constraint.

## Review
- [ ] Every queue has a bound and a full policy.
- [ ] Rejections are explicit and counted.
- [ ] Prefetch or in-flight limits are set.
- [ ] Depth and age are alerted.
