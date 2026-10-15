---
name: capacity-planning
title: Capacity planning
area: ops
tags: [capacity, load-testing, saturation, forecasting, headroom, scaling]
detect: []
related: [slos-alerting, cost-monitoring, load-balancing, database-failover]
---
Find the saturation point with load tests, set headroom targets from it, and forecast from measured growth.

## Verify
- `k6 run --vus 50 --duration 5m load.js`: sustained load against a staging environment, with latency and error summaries (k6).
- `vmstat 1 10`: run queue, swap, and CPU split on a host under load.
- `iostat -x 1 5`: disk utilization and await.
- `ss -s`: socket counts, to watch for connection exhaustion.
- `promtool query instant http://localhost:9090 'max_over_time(node_cpu_utilisation:ratio[7d])'`: peak utilization over the window, assuming a recording rule of that name exists.

## Test first
Write the capacity claim as a load test with thresholds, and let it fail at the current size.
```js
import http from 'k6/http';
export const options = {
  stages: [{ duration: '2m', target: 200 }, { duration: '5m', target: 200 }],
  thresholds: {
    http_req_duration: ['p(95)<400'],
    http_req_failed: ['rate<0.01'],
  },
};
export default function () { http.get(`${__ENV.BASE}/api/items`); }
```
Raise the target until a threshold breaks; that rate, divided by your safety factor, is the supported capacity.

## Do
- Use the USE method per resource (utilization, saturation, errors) and the four golden signals per service.
- Load-test a production-like environment with realistic data volume and request mix, and record the results with the build id.
- Find the first bottleneck (CPU, memory, connections, disk IO, a downstream limit), fix it, and repeat.
- Set target peak utilization (for example 60-70%) so you can lose a node or zone and still serve (N+1 or N+2).
- Forecast from trend and from business inputs (launches, seasonality); record the date each limit is expected to be reached.
- Alert on saturation indicators and on time-to-exhaustion (`predict_linear` on disk and quotas).
- Track quotas and limits (cloud service limits, file descriptors, connection pools, database connections) in one list.
- Re-run the test after major releases and before known peaks.

## Avoid
- Load-testing production without guardrails, or staging with a tenth of the data: results mislead. Match data size and use rate caps.
- Watching averages: tail latency breaks first. Judge by p95 and p99 and by queue depth.
- Scaling the app while the database or a downstream API is the bottleneck: no gain. Find the real constraint first.
- Closed-loop load generators only: they slow down with the system and hide overload. Use constant-arrival-rate executors to model real clients.
- Forgetting soft limits (open files, ephemeral ports, connection pool size, cloud quotas): the outage arrives before CPU is high. Inventory and alert on them.
- Planning for the average day: the peak plus a failure is the target.

## Review
- [ ] A load test with pass or fail thresholds exists and its latest result is recorded.
- [ ] Headroom target and failure tolerance (N+1) are stated and met.
- [ ] A forecast with an exhaustion date exists per limiting resource.
- [ ] Quotas, pools, and descriptor limits are listed and monitored.
- [ ] Tests ran against realistic data and request mix.
