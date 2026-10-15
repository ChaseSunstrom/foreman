---
name: grounding-ideas
title: Grounding ideas
area: practice
tags: [ideation, validation, evidence, code-reading, filtering]
detect: []
related: [brainstorming-lenses, capability-mapping, ideation-to-briefs, value-effort-scoring]
---
Check every idea against the real code, data and tools so each survivor cites files or commands and each reject says why.

## Verify
- `fm research list`: the grounded list is saved with its evidence column.
- `grep -n "<symbol from the idea>" -r .`: the cited place exists and does what the idea assumes.
- `fm ideas --help`: `--falsify` asks the idea generator to try to disprove its own items.

## Test first
Give each idea a falsifiable grounding claim before reading code.
```markdown
| idea | grounding claim | check | result |
| cache user lookups | lookup is called > 1x per request | `grep -rn "get_user(" src/ | wc -l` | 7 -> keep |
| add retry to X | X currently fails transiently | `grep -c "timeout" logs/*` | 0 -> reject |
Pass = every row has a command and a result; no row says "seems".
```

## Do
- For each idea, find the exact file and symbol it would change; record path:line.
- Check the premise is real: the problem occurs (logs, tests, a repro), not only plausible.
- Check it is not already done or half-done: search by synonyms and in tests and docs.
- Estimate effort from the files you found; note dependencies and risks.
- Mark each idea keep, reshape or reject with the single deciding fact.
- Drop duplicates and merge near-duplicates, keeping the strongest evidence.
- Pass survivors to scoring and then to briefs.

## Avoid
- Ideas that survive on plausibility: if you cannot cite a line or a number, it stays unverified and does not advance.
- Grounding only the ideas you like: apply the same check to all, and try to falsify the favourite.
- Reading one file and generalising: trace the real flow end to end for the top few.
- Quiet rejection: record why, or the idea returns next round.
- Trusting a model's cited paths: open them; models invent file names.

## Review
- [ ] Every surviving idea cites a path or a command result.
- [ ] Premise was checked against logs, tests or a repro.
- [ ] Existing or partial implementations were searched for.
- [ ] Rejects have a reason recorded.
- [ ] Cited paths were opened, not assumed.
