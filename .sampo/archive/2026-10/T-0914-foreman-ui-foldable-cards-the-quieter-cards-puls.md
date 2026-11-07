---
id: T-0914
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:12:39Z
updated: 2026-10-15T19:21:08Z
base: 85b58f9774e6cbf97ff2780698599afc307b6944
base_tree: ffb7c910c18f2f0dffaa97f45162e2a6e43dfca0
verified: strong
---
# foreman-ui foldable cards: the quieter cards (pulse, files, fleet, gates, brainstorm, spend, bench, research, activity) fold to their head line with a ▾/▸ toggle, remembered across sessions
## Raw request
> foreman-ui foldable cards: the quieter cards (pulse, files, fleet, gates, brainstorm, spend, bench, research, activity) fold to their head line with a ▾/▸ toggle, remembered across sessions
## Interpretation
Let the person fold the quieter pane cards to their one-line head and keep that choice across sessions
## Assumptions (confidence)
## Acceptance criteria
- [x] folding a card hides its body and survives a reload — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
a ▾/▸ toggle per quiet card, the folded set in an atom and $.store (chosen: the person decides what they see, and it lasts) · auto-collapse idle cards by heuristics (guesses wrong, moves things under the eye) · one global compact switch (all or nothing)
## Risks and rollback
## Execution prompt
## Steps
1. [x] a folded set in an atom and $.store; head() gets the toggle; each quiet card folds; tests
## Resume here
## Docs impact
CHANGELOG Unreleased (folding); MASTER.md mods/foreman-ui row
## Verification evidence
- `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 80 tests across 1 file. [6.21s] (start tree + this task's tests) [ran] [tree b83fa5c58bd9] (2026-10-15T19:20:52Z)
- `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 80 tests across 1 file. [6.38s] [ran] [tree b83fa5c58bd9] (2026-10-15T19:20:52Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 80 tests across 1 file. [6.34s] [ran] [tree b83fa5c58bd9] (2026-10-15T19:20:59Z)
- (audit intent) `self` → met: nine quiet cards fold to their head line with ▾/▸; the hero, Plan, Now, Needs you, Queue and Inbox never fold; the set persists via $.store and is read at session start [tree b83fa5c58bd9] (2026-10-15T19:20:59Z)
- (audit edge) `self` → a failing Gates card folded still shows its red head and pass count; a stored value of the wrong shape is filtered to strings; unknown keys in the set are harmless [tree b83fa5c58bd9] (2026-10-15T19:20:59Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 80 tests across 1 file. [6.43s] [ran] [tree b83fa5c58bd9] (2026-10-15T19:21:07Z)
## Log
- 2026-10-15T19:12:39Z created
- 2026-10-15T19:18:50Z set approved=True
- 2026-10-15T19:19:00Z focused
- 2026-10-15T19:21:07Z done
- 2026-10-15T19:21:08Z committed b6e3259 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- T-0228 [FEATURE M, done, 3 steps] foreman-ui catch-up: budget, bench and evolve, research asks, and the task's hypotheses, oracle and batch in the pane — lesson: Look at…
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
- decision 2026-10-09: Added JARVIS (<host>) as a fm conductor remote so the Foreman pane shows its sessions as tiles: the user's own host over their own …
## Lessons
- When wrapping many JSX blocks by script, find each block's end by its exact indent and closing tag, then re-indent the body in a second pass; the tests still pin behaviour, the second pass keeps the file readable
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- CHANGELOG.md
- MASTER.md
