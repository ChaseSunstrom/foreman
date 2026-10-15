---
name: five-whys
title: Five whys
area: practice
tags: [root-cause, debugging, analysis, incident, process]
detect: []
related: [scientific-debugging, retrospectives, friction-logging, first-principles]
---
Ask why repeatedly, each answer backed by evidence, until you reach a cause you can change, then fix that layer and add a guard.

## Verify
- `git log --oneline -5`: the fix landed at the deepest cause you found, not only at the symptom.
- `pytest -q` (or the project's test command): a test for the root cause exists and passes.
- `fm task finish --help`: shows `--lesson`, which records the root cause and guard with the task.

## Test first
Each why is a claim with proof, so write the chain as checkable lines.
```markdown
Symptom: <what was observed, with command output>
Why 1: <cause> | evidence: <log line, test, diff>
Why 2: <cause of why 1> | evidence: ...
Stop when the cause is something we control and a change would have prevented it.
Pass = every link has evidence and the last link has a concrete change (code, test, check).
```

## Do
- Start from an observed fact, not an interpretation; paste the failing output.
- For each answer, run a probe (grep, log, bisect, minimal repro) before asking the next why.
- Branch when an answer has two causes; follow each branch to its own end.
- Stop at a cause in your control (a missing test, an unchecked input, a wrong default), not at "human error".
- Fix at two levels: the immediate defect and the layer that let it through (test, lint rule, validation, gate).
- Write the chain in the commit or the task log so it is findable.

## Avoid
- Whys without evidence: each link needs a probe or it is a guess; mark guesses and test them.
- Stopping at the first plausible cause: ask one more why and check that fixing it would have prevented the symptom.
- Blame as a root cause ("careless", "forgot"): ask why the system allowed it.
- A single linear chain for a multi-cause failure: branch.
- Fixing only the symptom and calling the rest "follow-up": capture it as a task or do it now.

## Review
- [ ] Symptom is quoted from real output.
- [ ] Every link cites evidence.
- [ ] The final cause is something a code or process change controls.
- [ ] A guard (test, check, validation) was added at the root.
- [ ] The chain is recorded with the change.
