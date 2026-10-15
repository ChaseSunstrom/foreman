---
name: on-call
title: On-call
area: ops
tags: [on-call, paging, rotation, escalation, handoff, toil]
detect: []
related: [runbooks, slos-alerting, incident-response, postmortems]
---
A sustainable on-call has few, actionable pages, a tested escalation path, clear handoffs, and its load measured.

## Verify
- `amtool alert query --alertmanager.url=http://localhost:9093`: what is firing now (Alertmanager).
- `amtool config routes test --config.file=alertmanager.yml severity=page team=api`: an alert routes to the right receiver.
- `amtool silence query --alertmanager.url=http://localhost:9093`: active silences, so none is hiding a real problem past its purpose.
- `curl -s -X POST "$PAGER_TEST_WEBHOOK" -d '{"test":true}'`: the paging path delivers (use your provider's test endpoint).
- `grep -c . oncall-log.csv`: pages logged per period, as input to load review.

## Test first
Test the path before the first shift: send a test page to the primary, do not acknowledge it, and confirm escalation fires.
- Page the primary at a quiet hour.
- Confirm delivery on phone (push, SMS, call) within one minute.
- Leave it unacknowledged; confirm the secondary is paged at the timeout and then the manager.
- Fail the test if any person lacks a working notification, VPN, or access to production dashboards and runbooks.
Repeat after every rotation change and tooling change.

## Do
- Keep a primary and a secondary, with a documented escalation timeout (for example 5 and then 15 minutes).
- Rotate on a fixed schedule with follow-the-sun if you can; avoid more than one week in four on primary.
- Run a written handoff each shift: open incidents, silenced alerts with reasons, risky changes upcoming.
- Pre-shift checklist: laptop, charger, VPN, pager app, access to logs, runbooks, and the cloud console.
- Track pages per shift, out-of-hours pages, time to acknowledge, and the share that were actionable; review monthly.
- Cap the load: aim for at most a couple of actionable pages per shift, and fix the sources of the rest.
- Compensate the burden, with time off after a night-time incident.
- Let people shadow before they go primary.

## Avoid
- Paging on non-actionable alerts: fatigue and ignored pages. Delete, downgrade to tickets, or fix the cause.
- One person as the only escalation: they burn out and become a bottleneck. Keep a secondary and a rota.
- Silences with no expiry or owner: real problems stay hidden. Require a reason and a short expiry.
- Handoff by memory: context is lost. Write it in a shared log.
- Untested notification paths: the page never wakes anyone. Run the unacknowledged-page drill.
- Treating on-call as a punishment: attrition. Share load, limit hours, compensate, and fix toil.

## Review
- [ ] The rota has primary, secondary, and escalation with timeouts, and covers holidays.
- [ ] A test page was delivered and escalated within the last quarter.
- [ ] Page volume and actionable ratio are reviewed monthly with owners for noisy alerts.
- [ ] Handoff notes exist for each shift.
- [ ] Every on-call has access to the systems and runbooks they need.
