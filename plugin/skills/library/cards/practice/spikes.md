---
name: spikes
title: Spikes
area: practice
tags: [spike, prototype, research, timebox, uncertainty]
detect: []
related: [assumption-mapping, kill-criteria, approach-comparison, experiment-design]
---
A timeboxed throwaway experiment that answers one specific question, ending in a decision and discarded code.

## Verify
- `git status --short`: spike code is on a scratch branch or outside the tree, not mixed into the change.
- `fm decide --list`: the answer and the resulting choice are recorded.
- `fm research list`: the finding is saved with the command that produced it.

## Test first
Write the question, the timebox and the answer's shape before touching code.
```markdown
Question: Can library X stream 1 GB under 200 MB RSS?
Timebox: 45 min or 8 tool calls, whichever first.
Evidence format: one command and its output (peak RSS).
Decision rule: <= 200 MB -> adopt X; > 200 MB or unfinished -> option B.
```

## Do
- Ask one question per spike, phrased so a number or a yes/no answers it.
- Set the timebox and decision rule up front; when time ends, decide with what you have.
- Work in a scratch directory or branch; cut every corner except the one the question is about.
- Capture the exact command and output that answer the question.
- End with a decision recorded in the brief or `fm decide`, and delete or archive the spike code.
- Re-plan: update steps and estimates using what the spike showed.
- If the answer is "unclear", say what second question remains, and either run one more spike or pick the safer option.

## Avoid
- A spike that grows into the implementation: throw the code away and rebuild test-first with the knowledge.
- No question: "explore X" becomes reading docs for hours; write the question.
- Hidden timebox overrun: when the box ends, stop and decide.
- Answering from the happy path: include the one edge that could kill the option (size, auth, concurrency).
- Findings left in the terminal: save the output, or the next session repeats the spike.

## Review
- [ ] One question, one timebox, one decision rule, written first.
- [ ] Evidence is a command with output.
- [ ] A decision was recorded.
- [ ] Spike code is not in the final diff.
- [ ] The plan was updated from the result.
