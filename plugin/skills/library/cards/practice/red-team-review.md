---
name: red-team-review
title: Red team review
area: practice
tags: [review, adversarial, security, edge-cases, audit]
detect: []
related: [premortem, second-opinions, scientific-debugging, decision-records]
---
Attack your own change as an adversary, a hostile input and a tired operator would, and reproduce each finding before trusting it.

## Verify
- `fm audit prep ID`: prints one brief for a read-only reviewer pass over the diff.
- `fm second debate ID --role prosecutor`: a separate voice argues against the change.
- `fm task evidence ID --step N --run "<cmd>"`: each finding that was real has a failing run, then a passing one after the fix.

## Test first
Turn each attack into a failing test or repro command.
```markdown
Attack: empty input / 10 MB input / unicode / path with ../ / concurrent double submit
Expected: rejected or handled, no crash, no data written
Repro: `printf '' | ./tool --import` -> exit code != 0 and message names the field
Pass = every real finding has a repro that fails before the fix and passes after.
```

## Do
- List the trust boundaries the change touches (input, files, network, permissions, config).
- For each, try the standard hostile cases: empty, huge, malformed, duplicated, out of order, wrong type, wrong user.
- Ask the operator questions: what if it fails halfway, how do I roll back, what is logged.
- Ask the maintainer questions: what will confuse a reader, what is untested.
- Reproduce each suspected issue with a command; classify as real, not real, or unknown.
- Fix real ones test-first; capture the rest with `fm capture --source discovered`.
- Run the review on a fresh context or another model so it is not anchored on your reasoning.

## Avoid
- Findings without a repro: unverified claims waste time, so run it or discard it.
- Reviewing only the diff: also read the callers and the data the diff touches.
- Self-review in the same breath as writing: change the lens or hand it to a reviewer.
- Accepting every finding: check two against the code; reviewers hallucinate.
- Stopping at a clean first pass: ask what class of attack you did not try.

## Review
- [ ] Trust boundaries were listed.
- [ ] Hostile cases were tried, with commands.
- [ ] Each real finding has a test.
- [ ] Non-real findings were checked and dropped with a reason.
- [ ] Remaining work is captured, not lost.
