---
name: rubber-ducking
title: Rubber ducking
area: practice
tags: [debugging, explanation, clarity, reasoning, stuck]
detect: []
related: [scientific-debugging, five-whys, second-opinions, first-principles]
---
When stuck, explain the problem step by step in writing, claim by claim, and check each claim against reality until one breaks.

## Verify
- `fm task log --help`: the explanation is logged on the task, not only thought.
- Each claim in the write-up carries a command or a file line that was checked.
- The step that broke is named, and the next action is a probe, not a guess.

## Test first
Write the explanation as numbered claims, each with its check.
```markdown
Goal: what should happen
1. Request reaches handler  | check: log line at handler.py:42
2. Payload parses to dict   | check: print(type(data))
3. Handler writes the row   | check: SELECT count(*)
Observed vs expected at each step. First mismatch = where to dig.
Pass = every claim has a check that was run; the first false one is identified.
```

## Do
- Describe the expected behaviour end to end, in order, in plain sentences.
- Turn every sentence into a claim you can check: a value, a log, a query, a file line.
- Run the checks in order; stop at the first mismatch, since later ones depend on it.
- Say what you assumed without checking; those are the likeliest suspects.
- Explain to a reader with no context (a fresh subagent, or yourself in a new file); the missing context is often the bug.
- Name what you have ruled out, with evidence, so you do not retrace it.
- When the explanation does not resolve it, hand it on with that write-up (`fm second` or a fresh debugger agent).

## Avoid
- Explaining from memory of the code: open the file and read the real lines.
- Skipping the "obvious" step: the obvious step is where the assumption hides.
- Talking about it without writing it down: written claims can be checked and handed on.
- Stopping at "it should work": that sentence is a claim; run its check.
- Looping on the same explanation three times: change the vantage point (read the logs, diff against a working version).

## Review
- [ ] Explanation is a numbered list of checkable claims.
- [ ] Each claim was checked in order.
- [ ] The first false claim is named.
- [ ] Unchecked assumptions were listed.
- [ ] The next action is a concrete probe.
