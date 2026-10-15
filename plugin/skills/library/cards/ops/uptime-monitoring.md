---
name: uptime-monitoring
title: Uptime monitoring
area: ops
tags: [monitoring, probes, blackbox, synthetic, heartbeat, tls]
detect: [file:blackbox.yml]
related: [slos-alerting, status-pages, certificate-rotation, dns, on-call]
---
Probe from outside the failure domain, check the real user path and its dependencies, and watch the watcher.

## Verify
- `curl -fsS -m 10 -o /dev/null -w '%{http_code} %{time_total}s\n' https://svc.example.com/healthz`: the endpoint answers with latency, within a timeout.
- `curl -fsS https://svc.example.com/ | grep -q 'expected text'`: content check, not just a status.
- `openssl s_client -connect svc.example.com:443 -servername svc.example.com </dev/null 2>/dev/null | openssl x509 -noout -enddate`: certificate expiry the probe should alarm on.
- `promtool check rules probe.rules.yml`: probe alert rules parse.
- `curl -s 'http://localhost:9115/probe?target=https://svc.example.com&module=http_2xx' | grep '^probe_success'`: blackbox exporter result (Prometheus blackbox exporter).

## Test first
Break the thing on purpose and require the alert: stop the service in staging and time the page.
```sh
ssh stage 'systemctl stop app'
start=$(date +%s)
until amtool alert query --alertmanager.url=$AM alertname=ProbeDown | grep -q ProbeDown; do
  sleep 5; [ $(( $(date +%s) - start )) -lt 300 ] || { echo "no alert in 5m"; exit 1; }
done
echo "alerted after $(( $(date +%s) - start ))s"
ssh stage 'systemctl start app'
```
Then also test the monitor itself: block its outbound path and confirm the dead-man's switch fires.

## Do
- Probe from at least two networks or regions, and alert only when several fail, to avoid single-vantage false alarms.
- Check a real transaction (login, search, checkout in a test account) in addition to a static `/healthz`.
- Make `/healthz` verify essentials (database reachable, queue reachable) cheaply, with a separate liveness endpoint that stays dependency-free.
- Alert on TLS expiry (for example under 21 days), DNS answers, and domain expiry.
- Set sensible timeouts, retries, and a `for:` period (for example 2-3 failed probes) before paging.
- Add heartbeat monitoring for cron and batch jobs: the job pings on success, and silence alerts.
- Run an always-firing watchdog alert through the whole paging path, so silence means the pipeline broke.
- Publish probe results to the status page automatically, and keep probe history for SLO calculation.

## Avoid
- Monitoring only from inside the same cluster or provider: an outage that takes both goes unseen. Probe externally.
- A health check that returns 200 unconditionally: the app is broken and the dashboard is green. Test dependencies and content.
- Paging on one failed probe: flapping and fatigue. Require consecutive failures and multiple locations.
- Deep dependency checks in the liveness probe: a database blip restarts every pod. Keep liveness shallow and readiness deeper.
- Letting the monitor share fate with the service (same host, same DNS, same alert channel): fix by isolating it.
- No cron heartbeat: a job that silently stops is never noticed. Alert on missing pings.

## Review
- [ ] Probes run from outside and from multiple locations.
- [ ] At least one probe exercises a real user journey.
- [ ] A kill drill proved the page arrives within target time.
- [ ] TLS, DNS, and job heartbeats are covered.
- [ ] A watchdog alert verifies the monitoring and paging path.
