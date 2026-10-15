---
name: postmortems
title: Blameless postmortems
area: ops
tags: [postmortem, retrospective, root-cause, action-items, blameless]
detect: []
related: [incident-response, runbooks, on-call, slos-alerting]
---
Write a blameless postmortem within days of an incident, with a timeline from evidence and actions that have owners, dates, and a verification.

## Verify
- `git log --since='<incident start>' --until='<incident end>' --oneline --all`: changes that landed around the incident.
- `journalctl --since '<start>' --until '<end>' -p warning`: host evidence for the timeline, in UTC.
- `grep -c '^- \[ \]' postmortems/<id>.md`: open action items remaining in the document.
- `grep -L 'Owner:' postmortems/*.md`: postmortems missing owned actions.
- `gh issue list --label postmortem --state open`: action items still open, if tracked on GitHub.

## Test first
The test of a postmortem is whether each action would have prevented or shortened the incident. For each action, write the check that proves it landed.
- Action: add an alert for X. Check: a `promtool test rules` case that fires on the incident's recorded data.
- Action: add a timeout. Check: an automated test that the dependency stalling no longer hangs the request.
- Action: fix the runbook. Check: a cold drill of the corrected steps.
Open actions without a check count as unfinished.

## Do
- Hold the review within a few days, while memory is fresh, with the people involved plus a facilitator who was not.
- Build the timeline from logs, chat, and deploy records, all in UTC: detection, acknowledgment, mitigation, resolution.
- Separate sections: Summary, Impact (users, duration, error budget spent), Timeline, Contributing factors, What went well, What went poorly, Where we got lucky, Action items.
- Ask "how did the system allow this" instead of "who did it", and describe decisions in the context known at the time.
- Name contributing factors in plural; a single root cause is usually a story.
- Give each action an owner, a due date, and a priority; track them in the normal work tracker.
- Measure detection and mitigation time against targets, and note alerts that fired late or never.
- Share widely, and keep a searchable archive of them.

## Avoid
- Naming a person as the cause: people hide mistakes. Describe the missing guardrail instead.
- Action items like "be more careful" or "improve monitoring": nothing changes. Write a specific, verifiable change.
- Actions with no owner or date: they rot. Assign both in the meeting.
- Stopping at the trigger (a bad deploy): ask why tests, canary, and alerts did not catch it.
- Writing it weeks later from memory: the timeline is wrong. Collect evidence during the incident.
- Never revisiting actions: review the open count monthly and escalate overdue items.

## Review
- [ ] Impact is quantified, and the timeline is evidence-based with UTC stamps.
- [ ] Language is blameless and focused on system conditions.
- [ ] Every action has an owner, a due date, a tracker link, and a way to verify.
- [ ] Detection and mitigation gaps are addressed by at least one action each.
- [ ] The postmortem is shared and its overdue actions reviewed.
