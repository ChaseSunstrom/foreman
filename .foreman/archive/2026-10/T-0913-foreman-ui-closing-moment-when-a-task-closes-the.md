---
id: T-0913
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:12:39Z
updated: 2026-10-15T19:18:30Z
base: 600426aec35903b9ff7251d6bf7261edac51a685
base_tree: b45d93a284c3afac607437d244b392412c262ded
verified: strong
---
# foreman-ui closing moment: when a task closes the hero shows a done card for 6 s (grade, criteria proven, time against the usual) with one green sweep, then settles
## Raw request
> foreman-ui closing moment: when a task closes the hero shows a done card for 6 s (grade, criteria proven, time against the usual) with one green sweep, then settles
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a close shows the done card with grade and proof count, gone after 6 s — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] record the closed task at refresh; the hero's done card and sweep; test
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 79 tests across 1 file. [6.00s] (start tree + this task's tests) [ran] [tree ffb7c910c18f] (2026-10-15T19:18:21Z)
- `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 79 tests across 1 file. [6.10s] [ran] [tree ffb7c910c18f] (2026-10-15T19:18:21Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 79 tests across 1 file. [6.04s] [ran] [tree ffb7c910c18f] (2026-10-15T19:18:29Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 79 tests across 1 file. [6.04s] [ran] [tree ffb7c910c18f] (2026-10-15T19:18:29Z)
- (audit edge) `self: refresh records the closed task from the last snapshot (title, criteria, time on it, the usual) and next.closed (grade, lenses); the card sits above Needs you, sweeps in 0.9 s (blit in full motion), and goes after 6 s: the frame clock now draws once more as it sleeps, so a faded glow or card is drawn settled` → motion off shows the card filled and still, and it goes at the next redraw (the 2 s poll's refresh or any change) [tree ffb7c910c18f] (2026-10-15T19:18:29Z)
- (audit self) `self: refresh records the closed task from the last snapshot (title, criteria, time on it, the usual) and next.closed (grade, lenses); the card sits above Needs you, sweeps in 0.9 s (blit in full motion), and goes after 6 s: the frame clock now draws once more as it sleeps, so a faded glow or card is drawn settled` → no findings [tree ffb7c910c18f] (2026-10-15T19:18:29Z)
## Log
- 2026-10-15T19:12:39Z created
- 2026-10-15T19:16:56Z focused
- 2026-10-15T19:18:29Z done
- 2026-10-15T19:18:30Z committed 85b58f9 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0116 [FEATURE M, done, 4 steps] Size words with meaning: typical time per type and size, time on task, gate ETA — lesson: Medians need a floor on samples; with fewer t…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- T-0473 [FEATURE M, done, 0 steps] Proof and close-out cards (C071, value 3/5, effort S, risk low)
- decision 2026-10-15: Pane order: Needs you and waiting plans above the hero (T-0909)
- similar past tasks were M: consider --tier M
- similar finished tasks took 0–4 steps
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
