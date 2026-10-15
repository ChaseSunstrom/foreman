---
name: incident-response
title: Incident response
area: ops
tags: [incident, response, severity, communication, mitigation, timeline]
detect: []
related: [runbooks, on-call, postmortems, slos-alerting, status-pages]
---
Run incidents with named roles, stop the bleeding before finding the cause, and keep a timestamped log.

## Verify
- `date -u +%FT%TZ`: stamp every action in UTC so the timeline merges across people.
- `git log --since='6 hours ago' --oneline --all`: what changed recently in the suspect repo.
- `kubectl rollout history deploy/<name>`: recent deploys, as a rollback candidate (Kubernetes).
- `journalctl -u <unit> --since '30 min ago' -p err`: recent errors on a host service.
- `curl -s -o /dev/null -w '%{http_code} %{time_total}\n' https://svc.example.com/healthz`: the user-visible symptom, before and after each action.

## Test first
The drill fails first: run a game day with an unannounced fault and score it.
- Inject a fault in staging (kill a dependency, fill a disk, expire a cert).
- Page the on-call using the real path.
- Time: to acknowledge, to name an incident commander, to first status update, to mitigation.
- Fail the drill if any target slips (for example ack under 5 min, update every 30 min), then fix the process, not the person.
Record results beside the runbooks and repeat each quarter.

## Do
- Declare early and declare high: open the incident channel, set a severity (by user impact), and name roles: incident commander, ops lead, communications lead, scribe.
- The commander coordinates and decides; they do not debug.
- Mitigate first: roll back, fail over, flip a feature flag, shed load. Root cause comes after.
- Post status updates on a fixed cadence even when nothing changed ("no change, next update at 14:30").
- Keep one written timeline in a shared doc: time, actor, action, result.
- Change one thing at a time and state the expectation before doing it.
- Hand off explicitly (name, state, open actions) when shifts change or people tire.
- Close with a clear all-clear message, and schedule the postmortem within a few days.

## Avoid
- Everyone debugging in parallel with nobody coordinating: conflicting changes. Appoint a commander and assign tasks.
- Hunting the root cause while users are down: extend the outage. Mitigate through rollback or failover first.
- Silent war rooms: stakeholders interrupt for updates. Give the communications lead a cadence and a template.
- Verbal-only actions: the timeline is lost and the postmortem guesses. Have the scribe log in the channel.
- Rolling forward a fix under pressure with no test: a second incident. Prefer the proven rollback.
- Hero culture: one expert holds all the knowledge. Rotate the commander role and write runbooks.

## Review
- [ ] Severity levels, role definitions, and escalation paths are written and current.
- [ ] A drill ran in the last quarter with measured ack and mitigation times.
- [ ] Status updates follow a cadence and a template.
- [ ] A timeline exists for each incident, with UTC stamps.
- [ ] Every incident above the threshold got a postmortem with owned actions.
