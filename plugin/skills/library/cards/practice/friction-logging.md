---
name: friction-logging
title: Friction logging
area: practice
tags: [friction, observation, process, improvement, tooling]
detect: []
related: [self-improvement-loops, retrospectives, recursive-improvement, decision-records]
---
Note each moment of drag as it happens (blocked command, repeated step, confusing output), with the exact trigger, so improvements target real pain.

## Verify
- `fm friction --brief`: shows the friction evidence collected so far and what a pass should look at.
- `fm repeats`: lists repeated manual work worth automating.
- `fm capture --help`: friction that needs work becomes a captured task, not a note.

## Test first
Each entry must be specific enough that a fix can be tested.
```markdown
- trigger: `git commit -m "$(cat <<EOF ...` blocked by guard
  cost: 2 retries, ~3 min
  expected: commit allowed
  repro: the exact command
  fix-test: guard fixture for this command returns allow
Pass = entry has trigger, cost, and a repro command; no entry says only "slow" or "annoying".
```

## Do
- Log at the moment of friction: command, output line, what you wanted, what it cost.
- Record the cost in retries or minutes, so entries can be ranked.
- Include the repro command verbatim; paraphrase loses the detail that matters.
- Tag type: guard block, missing tool, unclear message, repeated step, slow check, stale doc.
- Group at pass time; frequency times cost orders the work.
- Turn the top entries into tasks with a failing test or a check that proves the friction is gone.
- Delete or mark entries once fixed, so the log stays a live list.

## Avoid
- Vague entries ("tooling is clunky"): add the trigger and a repro or drop it.
- Logging without acting: after a pass, at least the top item becomes a task or is rejected with a reason (`fm friction --reject`).
- Treating a one-off as a pattern: wait for two occurrences, or note it as a single.
- Fixing friction by weakening a safety guard: fix the false positive with a fixture, never by lowering the guard.
- Dumping raw transcripts: summarise to the line that matters.

## Review
- [ ] Each entry has trigger, cost and repro.
- [ ] Entries are grouped and ranked by frequency times cost.
- [ ] The top item is a task or has a recorded rejection.
- [ ] Fixed entries were marked.
- [ ] No fix reduced a safety check.
