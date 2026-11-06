---
id: T-0932
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:52:06Z
updated: 2026-10-15T21:13:13Z
---
# Feel free to do the entire board, and more if possible
## Raw request
> feel free to do the entire board, and more if possible
## Interpretation
Build every open cluster on the board (later and skip marks alike, 69 clusters, rounds 1-8 and the UI): for each, the smallest slice that makes its capability real, test-first, then go past the board with whatever the work turns up. Clusters that need something this machine can't give (an account, another OS, a paid service, a human) are reported, not faked.
## Assumptions (confidence)
## Acceptance criteria
- [ ] every open cluster on the board has an outcome: built (task id), already done (where), or blocked (why) — verify with `fm research show board-outcomes`
## Non-goals
## Approach (options → choice → why)
A one brief per idea (~1000 ideas: most are duplicates inside a cluster; churn) · B one grounded slice per cluster, built in waves by value-for-effort, two fm-builder lanes in parallel with the main thread, a reviewer pass per wave, gates and a release at the end (chosen: covers every cluster with real code, keeps each change reviewable) · C a workflow fan-out (needs the user's explicit opt-in to multi-agent orchestration). Grab-bag clusters (misc, round N later/skip) get up to four slices each.
## Risks and rollback
Hot files (fmcli.py, fmhooks.py, register.tsx) conflict between lanes: lanes take slices in other modules; each slice is its own commit and reverts alone. Security-relevant slices (guard, sensitive, injection) get the adversary lens.
## Execution prompt
## Steps
1. [ ] ground all 69 clusters (six recon passes), merge into one slate with marks: build / blocked (why) / already done  <- CURRENT
2. [ ] turn the slate into briefs (fm intake), ordered by value for effort
3. [ ] build in waves: main thread + up to two fm-builder lanes; review each wave; fix findings test-first
4. [ ] gates, CHANGELOG, board refresh with every cluster's outcome, release
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-15T19:52:06Z created
- 2026-10-15T19:54:07Z set approved=True
- 2026-10-15T21:13:13Z dropped: split into ten batch briefs T-0954..T-0963 (one builder lane each); every cluster's outcome in research board-slate-20261015
## Follow-ups captured
## Build vs reuse
Reuses the board's own catalogue (research brainstorm-*), fm-recon for grounding, fm lane + foreman:fm-builder for parallel slices, fm intake for briefs, fm check/release.py for gates and release; each slice extends the module it names (fmcli, fmhooks, fmguard, the mod) rather than adding parallel machinery.
