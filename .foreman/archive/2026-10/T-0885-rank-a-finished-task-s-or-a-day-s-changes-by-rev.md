---
id: T-0885
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T15:29:55Z
updated: 2026-10-15T15:59:59Z
base: ae4299963fd60d16b7f1d980ff53557acfd51151
base_tree: d65208253f9640fc364e69bcbb37807da3dc7a50
verified: strong
---
# Rank a finished task's or a day's changes by review risk, with a safe-to-skim verdict for
## Raw request
> FEATURE: Rank a finished task's or a day's changes by review risk, with a safe-to-skim verdict for the rest
> CONTEXT: round 5 #48 (value 5). fm tour already gives a reading order; risk signals exist: c.sensitive, churn hot spots, untested changed files, size
## Interpretation
fm tour gains a review-risk verdict per changed file (review / glance / skim, each with its reasons: security-sensitive path or added code, runs in CI or on install, size, no test changed with it, deleted code, a hot file; tests, docs and generated files are skim) and a header naming what to review first; and fm tour --since REF tours a range (the branch since main, a day via HEAD@{yesterday}) including uncommitted work, so a morning review of a long unattended run starts with the few files that matter
## Assumptions (confidence)
## Acceptance criteria
- [x] fm tour --since REF ranks a sensitive code change review, docs/tests skim, with reasons and a header — verify with `python3 plugin/tests/run.py test_handoff`
## Non-goals
## Approach (options → choice → why)
1) Extend fm tour (chosen: it already orders a task's files and shows sizes; one more column and a range mode, no new verb — the over-engineering audit counted too many). 2) A new fm review verb (another verb to learn). 3) A model-scored review (costs tokens, slower, non-deterministic; the mechanical signals already exist: c.sensitive, fmmap hot files and test links, is_generated). Complete version: per-file verdict + reasons in text and JSON, header summary, range mode with merge-base and working tree, scored deterministically.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_handoff, then risk scoring and --since in fmmap.tour
2. [x] docs (MASTER, CHANGELOG) and a live run over this branch
## Resume here
## Docs impact
MASTER review risk; CHANGELOG round 5
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_handoff test_help test_map` → exit 0 · Ran 20 tests in 2.0s (8 classes, 16 at a time; slowest: Tour 2s, Map 1s, Export 1s) / OK [ran] [tree 450d82436105] (2026-10-15T15:57:57Z)
- (step 2) `fm tour --since main | head -1` → exit 0 · since main: Review first: plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmbench.py, plugin/lib/fmsession.py, plugin/lib/fmorders.py, install.sh, plugin/lib/fmsmoke.py, plugin/hooks/compact [ran] [tree 450d82436105] (2026-10-15T15:57:59Z)
- `python3 plugin/tests/run.py test_handoff` → ✗ exit 1 · Ran 9 tests in 2.0s (3 classes, 16 at a time; slowest: Tour 2s, Export 1s, Proof 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 450d82436105] (2026-10-15T15:58:05Z)
- `python3 plugin/tests/run.py test_handoff` → exit 0 · Ran 9 tests in 1.9s (3 classes, 16 at a time; slowest: Tour 2s, Export 1s, Proof 1s) / OK [ran] [tree 450d82436105] (2026-10-15T15:58:05Z)
- (ac 1) `python3 plugin/tests/run.py test_handoff` → exit 0 · Ran 9 tests in 1.9s (3 classes, 16 at a time; slowest: Tour 2s, Export 1s, Proof 1s) / OK [ran] [tree 450d82436105] (2026-10-15T15:59:58Z)
- (audit intent) `self review plus a live run over this branch (217 files → 15 review, 38 glance, 164 skim); the run found two false signals (a React hooks/ folder read as install hooks; docs and data 'used' by name) — both fixed before close` → a range or a task gets a deterministic verdict per file with reasons and a header of what to review first, highest score first; fm tour ID keeps its reading order and sizes (old tests pass) [tree 450d82436105] (2026-10-15T15:59:58Z)
- (audit edge) `self review plus a live run over this branch (217 files → 15 review, 38 glance, 164 skim); the run found two false signals (a React hooks/ folder read as install hooks; docs and data 'used' by name) — both fixed before close` → an unknown REF or no shared history is a usage error; a deleted file scores as deleted code; a test file that mostly lost lines is review, not skim; a branch with 200+ files names 8 and counts the rest [tree 450d82436105] (2026-10-15T15:59:58Z)
## Log
- 2026-10-15T15:29:55Z created
- 2026-10-15T15:56:22Z focused
- 2026-10-15T15:59:58Z done
- 2026-10-15T15:59:59Z committed d9ff6a9 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round5-20261015: Probe: `fm ideas` with capability map + unspoken needs, 2 rounds, past every earlier ideas.md (brainstorm-20261015-101633): 54 new t…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- decision 2026-10-09: [costly] Build all 70 'build' capabilities from the Foreman brainstorm in value-for-effort rounds (security first); the user's ticks on the punch li…
## Lessons
- Run a new report on the biggest real input before trusting it: the unit test passed while the live branch run showed two signals firing on the wrong files
## Files touched
- plugin/tests/test_handoff.py
- plugin/lib/fmcli.py
- plugin/lib/fmmap.py
- CHANGELOG.md
- MASTER.md
