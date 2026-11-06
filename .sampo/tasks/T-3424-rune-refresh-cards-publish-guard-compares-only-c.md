---
id: T-3424
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T10:23:40Z
updated: 2026-11-06T10:43:28Z
lane: ~/.claude/foreman/.claude/worktrees/agent-aa84c72e440b55592
lane_branch: worktree-agent-aa84c72e440b55592
base: 177fdfc5a8e5cb46c67896101e880f3b96caa9c3
base_tree: d5305a9a01fce005ed7d8914ad0390e51f6ddf69
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-06T10:25:05Z
plan0_scope: []
builder_returned: 2026-11-06T10:43:28Z
---
# rune._refresh_cards' publish guard compares only card counts, so a degraded export…
## Raw request
> FIX: rune._refresh_cards' publish guard compares only card counts, so a degraded export (all-default kit heights, empty demos, missing images) with an equal count is committed to the public site; add a content check (heights present and varied, every demo non-empty) that fails the refresh
## Interpretation
Reading 1: add a pure content check on the built export, fail the refresh before commit. Reading 2: fix the export itself so it never degrades (T-3228's job, ruled out: the guard must hold for any cause).
## Assumptions (confidence)
## Acceptance criteria
- [ ] degraded export is refused, good one passes — verify with `python3 plugin/tests/run.py test_genesis.CardsDegraded`
## Non-goals
## Approach (options → choice → why)
1) one pure helper reading index.json and kit.json; likely outcome: fast, catches the named cases. 2) also parse every shard's per-card demos; fails if too slow (5000 cards). 3) use what exists: compare with the previous export's heights; fails on a legit re-measure. 4) do less: keep the count guard only; fails on the equal-count degraded export (the bug). Choice 1 (80%): fast, pure, covers the named failures.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then implement _cards_degraded
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded 2>&1 | tail -5` → ✗ exit 1 · Ran 1 tests in 55.8s (1 jobs, 16 at a time; slowest: CardsDegraded 0s) / FAILED (1 classes: test_genesis.CardsDegraded) [ran] [tree 90bc1b218589] [world 2f1906870a] (2026-11-06T10:26:21Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded test_genesis.GenesisLive` → ✗ exit 1 · Ran 9 tests in 74.2s (2 jobs, 16 at a time; slowest: GenesisLive 6s, CardsDegraded 0s) / FAILED (1 classes: test_genesis.CardsDegraded) [ran] [tree ae37161f3448] [world 2f1906870a] (2026-11-06T10:27:44Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded 2>&1 | grep -B3 -A12 "^FAIL"` → ✗ exit 1 · Ran 1 tests in 29.4s (1 jobs, 16 at a time; slowest: CardsDegraded 0s) / FAILED (1 classes: test_genesis.CardsDegraded) [ran] [tree ae37161f3448] [world 2f1906870a] (2026-11-06T10:28:15Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded test_genesis.GenesisLive` → exit 0 · Ran 9 tests in 19.8s (2 jobs, 16 at a time; slowest: GenesisLive 9s, CardsDegraded 0s) / OK [ran] [tree 04a4ae6774c9] [world 2f1906870a] (2026-11-06T10:28:41Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_genesis test_left_out test_models test_moons_scale test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [21.91s] [ran] [tree 04a4ae6774c9] [world 2f1906870a] (2026-11-06T10:30:37Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded test_genesis.GenesisLive` → exit 0 · Ran 11 tests in 4.5s (2 jobs, 16 at a time; slowest: GenesisLive 4s, CardsDegraded 0s) / OK [ran] [tree c7c44f783c59] [world 2f1906870a] (2026-11-06T10:43:21Z)
## Log
- 2026-11-06T10:23:40Z created
- 2026-11-06T10:24:52Z planned: it has criteria and steps
- 2026-11-06T10:25:04Z focused
- 2026-11-06T10:25:05Z predicted from its closes: 6 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research readme-site-audit: Seven read-only auditors, one per slice; each claim checked against code and live data. Findings below are verified
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-3266 [FEATURE M, active, 3 steps] Remake the Rune page (site/genesis) in the Sampo look with Kalevala: every tower, the meta-generations and Väinämöinen's acts
- decision 2026-10-23: T-1615: the desk card is a file, never a listener
- similar past tasks were L: consider --tier L
- the similar finished task took 9 steps
