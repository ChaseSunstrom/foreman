---
name: brainstorming-lenses
title: Brainstorming lenses
area: practice
tags: [ideation, brainstorm, lenses, breadth, divergence]
detect: []
related: [grounding-ideas, ideation-to-briefs, capability-mapping, value-effort-scoring]
---
Generate ideas by forcing different viewpoints (user, operator, attacker, maintainer, cost), then cluster, so the list is broad instead of ten variants of one thought.

## Verify
- `fm research list`: the ideas note was saved, not left in chat.
- `grep -c '^- ' .foreman/ideas.md`: replace the path with the saved note; at least 3 lenses each produced distinct items.
- `fm ideas --help`: shows `--lens`, `--rounds`, `--dry`, `--seen` for fanning the lenses out to tool-less children.

## Test first
Write the success claim before generating anything.
```markdown
Goal: <one sentence, measurable>
Lenses (pick 4+): new user | operator at 3am | attacker | maintainer in a year | cheapest possible | remove-something
Pass = >= 3 lenses yield an idea no other lens produced, and >= 1 idea is a deletion.
Fail = after clustering, fewer than 3 distinct clusters remain.
```

## Do
- State the goal and constraints in two lines first. A lens without a goal produces slogans.
- Run each lens separately with a fixed quota (5 ideas) and write ideas as "who does what, so that what changes".
- Include at least one subtractive lens (what could we delete) and one adversarial lens (how does this fail).
- Keep rejected and duplicate ideas in the note with a one-word reason, so the next round does not regenerate them.
- Cluster by mechanism, not by wording; name each cluster by the problem it addresses.
- Stop when a full round adds no new cluster (a dry round), not after a fixed count.
- Hand the clusters to grounding next; an ungrounded list is not output.

## Avoid
- One lens re-labelled five times: check that ideas differ in mechanism; drop the repeats.
- Evaluating while generating: write first, score later, or the list shrinks to the safe idea.
- Lists of features with no user or trigger: attach a who and a when to each or discard it.
- Stopping at the first plausible idea: demand the quota per lens before reading any of them.
- Leaving the list in chat: save it (`fm research list` should show it) so later sessions can recall it.

## Review
- [ ] At least four lenses were used and each is named in the note.
- [ ] Duplicates were merged and the rejected ones recorded with a reason.
- [ ] One idea removes work instead of adding it.
- [ ] Each surviving cluster states the problem it solves.
- [ ] The note says what happens next (grounding, scoring), with a path.
