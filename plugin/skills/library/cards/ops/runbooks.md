---
name: runbooks
title: Runbooks
area: ops
tags: [runbook, operations, documentation, automation, drills]
detect: []
related: [on-call, incident-response, slos-alerting, postmortems]
---
A runbook is a tested, copy-pasteable procedure linked from the alert that needs it, short enough to follow at 3am.

## Verify
- `grep -rL 'runbook_url' alerts/`: alert files with no runbook annotation at all.
- `grep -rn 'runbook' alerts/*.yml | wc -l`: how many alerts link a runbook, to compare with the alert count.
- `lychee --offline runbooks/`: relative links resolve (link checker, if installed).
- `shellcheck runbooks/scripts/*.sh`: embedded scripts are sound.
- `git log -1 --format=%cd -- runbooks/<name>.md`: when the runbook was last touched.

## Test first
The drill is the test: someone who did not write the runbook executes it in staging, following only the text.
- Pick an alert, trigger it in staging, and hand the runbook to a teammate.
- Record every point where they ask a question, guess, or use unwritten knowledge.
- Fix the text until a cold run reaches the end state without help.
- Record the date and the runner in the file header, and repeat on a schedule.
Fail the drill if any step needs a secret or access they lack; fix access, not the drill.

## Do
- Use a fixed shape: Symptom and alert name; Impact; Quick triage (three checks); Mitigation steps; Escalation (who, when); Verification (how you know it worked); Links (dashboards, logs).
- Write steps as exact commands in code blocks with the expected output, and mark which are safe (read-only) and which change state.
- Put the first mitigation at the top; background goes at the bottom.
- Link the runbook in the alert annotation, and the dashboard in the runbook.
- Automate steps that have no judgment (a script or a chat command); the runbook then calls the script.
- State rollback for every state-changing step.
- Review each runbook after every incident that used it, and delete obsolete ones.
- Keep an owner and last-verified date in the header.

## Avoid
- Prose essays and architecture tours: nobody reads them mid-incident. Use numbered steps and commands.
- Commands with placeholders left ambiguous (`<host>`): wrong target. Show how to discover the value (`kubectl get pods -l app=x`).
- Stale procedures: they cause the second incident. Date them, drill them, and expire unverified ones.
- Steps that need tribal knowledge ("ask Dana"): a single point of failure. Write down the answer or the escalation path.
- A runbook only in a wiki that is down when the system is: keep a copy in the repo and an offline export.
- Destructive commands without a confirm step: add a dry-run first and name the blast radius.

## Review
- [ ] Every paging alert links a runbook with a named owner.
- [ ] Each runbook has symptom, triage, mitigation, rollback, and verification sections.
- [ ] A cold drill by a non-author succeeded within the last two quarters.
- [ ] Commands are exact, and destructive steps carry a dry-run and warning.
- [ ] Runbooks are readable during an outage of the main wiki or platform.
