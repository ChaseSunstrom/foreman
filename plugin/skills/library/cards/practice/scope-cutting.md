---
name: scope-cutting
title: Scope cutting
area: practice
tags: [scope, planning, mvp, prioritisation, delivery]
detect: []
related: [value-effort-scoring, kill-criteria, ideation-to-briefs, approach-comparison]
---
Cut the plan to the smallest version that meets the acceptance criteria, and record what was cut so it is a decision rather than a loss.

## Verify
- `fm queue`: remaining steps all trace to a criterion.
- `git diff --stat`: the diff touches only files the criteria need.
- `fm capture --help`: shows how cut items are parked as captured tasks instead of forgotten.

## Test first
Write the criteria as the cut line; anything that cannot be tied to one is out.
```markdown
Must (criteria): 1. <behaviour> :: <command>   2. ...
Should: ... (only if Must is done and cheap)
Cut to later: ... -> fm capture
Pass = every step in the plan names the criterion it serves; zero steps are orphans.
```

## Do
- Start from the done-when criteria, not from the idea list.
- Mark each step or feature: needed for a criterion, helps a criterion, or neither.
- Delete "neither" first, then defer "helps" behind the criteria that must ship.
- Prefer cutting breadth (fewer cases) over depth (a half-working core).
- Keep the cut list: capture each deferred item with one line on why and when to revisit.
- Check that the cut version still passes the criteria commands before adding anything back.
- Cut the edges of the work (config, flags, polish) before the middle (core path and tests).

## Avoid
- Cutting the tests or the verification step to hit scope: cut features, never evidence.
- Cutting silently: tell the user in the record what is not done.
- "Phase 2" lists with no owner: capture them as tasks or drop them.
- Gold-plating a step already past its criterion: stop when the check passes.
- Cutting so far the criteria no longer meet the original need: re-read the request after cutting.

## Review
- [ ] Every remaining step maps to a criterion.
- [ ] Cut items are captured or explicitly dropped with a reason.
- [ ] Tests and verification were not cut.
- [ ] The original request is still met.
- [ ] The final diff has no change outside the criteria.
