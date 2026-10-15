---
name: load-balancing
title: Load balancing
area: ops
tags: [load-balancer, health-check, haproxy, nginx, tls, failover]
detect: [file:haproxy.cfg]
related: [blue-green-deploys, canary-releases, dns, uptime-monitoring, cdn-caching]
---
Load balancers spread traffic only across healthy backends; prove it by killing a backend and watching zero failed requests.

## Verify
- `haproxy -c -f /etc/haproxy/haproxy.cfg`: config parses (HAProxy).
- `nginx -t`: config parses (nginx).
- `curl -sS -o /dev/null -w '%{http_code} %{time_total}\n' https://svc.example.com/healthz`: the front door answers, with latency.
- `for i in $(seq 20); do curl -s https://svc.example.com/whoami; done | sort | uniq -c`: traffic spreads across the expected backends.
- `ss -tn state established '( sport = :443 )' | wc -l`: connection count, to compare before and after a drain.

## Test first
The failure drill comes first: stop one backend under load and require no errors.
```sh
( for i in $(seq 200); do
    curl -s -o /dev/null -w '%{http_code}\n' https://svc.example.com/; sleep 0.1
  done ) > codes.txt &
sleep 5; ssh backend2 'systemctl stop app'
wait
grep -vc '^200$' codes.txt   # must stay at or near 0 once health checks eject the node
```
Expect a few errors before the check interval elapses; tune it so the count is within budget.

## Do
- Health-check the app path (`/healthz` verifying its dependencies cheaply), not just TCP connect.
- Set check interval, rise, and fall (`inter 2s fall 3 rise 2` in HAProxy) so ejection is fast but not flappy.
- Drain before maintenance: mark the server `drain` or `disabled`, wait for connections to finish, then stop it.
- Set timeouts explicitly (connect, client, server, idle) and make the LB timeout exceed the app's keep-alive, or lower the app's.
- Retry only idempotent requests, and bound retries.
- Terminate TLS with current protocols, and forward the client address (`X-Forwarded-For`, PROXY protocol) with trust limited to known proxies.
- Make the LB itself redundant (VRRP or keepalived, or a cloud LB across zones).
- Export per-backend metrics: active, 5xx, queue, response time.

## Avoid
- TCP-only health checks: a hung app still accepts connections. Check an HTTP endpoint.
- Sticky sessions as state storage: a node loss drops users. Externalize sessions, and use stickiness only as an optimization.
- Retrying POSTs: duplicates payments or orders. Restrict retries to safe methods or idempotency keys.
- An LB idle timeout shorter than the backend's: random 502s on reused connections. Align them (backend keep-alive longer than the LB's).
- Trusting `X-Forwarded-For` from the internet: clients spoof it. Overwrite it at the edge.
- One LB node, and no test of failover: the LB is the single point of failure. Run two and drill it.

## Review
- [ ] A backend-kill drill ran and error count stayed in budget.
- [ ] Health checks hit an application endpoint with sane thresholds.
- [ ] Drain procedure documented and used for deploys.
- [ ] Timeouts are explicit and consistent through the chain.
- [ ] The LB tier has no single point of failure.
