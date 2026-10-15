---
name: assumption-mapping
title: Assumption mapping
area: practice
tags: [assumptions, risk, planning, validation, uncertainty]
detect: []
related: [premortem, spikes, first-principles, experiment-design, kill-criteria]
---
List what the plan assumes, rank by risk and uncertainty, and test the riskiest ones first with the cheapest check.

## Verify
- `fm queue`: the brief carries an assumptions list and the top ones have a step to test them.
- `grep -n "assum" <brief or note>`: each assumption has a status (verified, refuted, open) and evidence.
- `git log --oneline -5`: the refuting or confirming check ran before the build commits.

## Test first
Turn each top assumption into a falsifiable check before building on it.
```markdown
| assumption | if false, what breaks | confidence | cheapest check | status |
| API returns <=100 rows | pagination needed, +2 days | M | curl one page, count rows | open |
Order: high impact x low confidence first.
Pass = the top 3 are verified or refuted with evidence before step 2 of the plan.
```

## Do
- Extract assumptions from the request and plan: about users, data shape, APIs, versions, performance, permissions, time.
- Phrase each as a statement that could be false.
- Score impact-if-false and confidence as high/med/low; test the high-impact low-confidence cell first.
- Pick a check that takes minutes: a query, a curl, a read of the code, a tiny script.
- Update the status with the evidence; a refuted assumption changes the plan immediately.
- Re-scan after each refuted assumption; they cluster.

## Avoid
- Burying assumptions inside prose: pull them out as a list or you will not test them.
- Testing the easy ones first: rank by risk, not convenience.
- "Verified" by recollection: show the command output or the file line.
- Treating the user's stated facts as verified: check anything that is cheap to check.
- Unchecked assumptions at the finish: close each as verified, refuted or accepted-with-risk in the record.

## Review
- [ ] Assumptions are statements that can be false.
- [ ] Ranked by impact and confidence.
- [ ] The riskiest ones were tested before building on them.
- [ ] Each has a status and evidence.
- [ ] Refuted ones changed the plan or the brief.
