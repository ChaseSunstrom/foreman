---
id: T-0112
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmideas.py, plugin/lib/fmcli.py, plugin/tests/test_taste.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-03T03:05:24Z
updated: 2026-10-03T08:51:49Z
base: bb843a703d308bc324d33b8f7efd1f3f2eca6b84
base_tree: 6c0afb8d7018a2b9627ac8656a343d9ee2964a75
verified: ok
---
# Taste profile: fm taste shows what the user kept, dropped (with reasons), steered and corrected; brainstorm packs carry it
## Raw request
> Taste profile from what the user accepts and corrects
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm taste lists kept work, dropped work with its reason, steers and corrections, with --json, and the brainstorm pack's user voice includes the drops and steers — verify with `python3 plugin/tests/run.py -k test_taste`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test
2. [x] taste() and fm taste; drops and steers in user_voice
3. [x] MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER (Taste profile) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_taste` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Taste 1s) / OK [ran] [tree da27683ff17d] (2026-10-03T08:51:48Z)
- (step 2) `python3 plugin/tests/run.py -k test_taste` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Taste 1s) / OK [ran] [tree da27683ff17d] (2026-10-03T08:51:48Z)
- (step 3) `grep -q T-0112 MASTER.md && grep -q T-0112 CHANGELOG.md` → exit 0 · (no output) [ran] [tree da27683ff17d] (2026-10-03T08:51:48Z)
- (ac 1) `python3 plugin/tests/run.py -k test_taste` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Taste 0s) / OK [ran] [tree da27683ff17d] (2026-10-03T08:51:49Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:51 UTC); cached (fm check --fresh reruns) [ran] [tree da27683ff17d] (2026-10-03T08:51:49Z)
- (audit self) `self: the test covers a kept request, a drop with its reason, a steer, the --json shape and the pack lines; on this project's real history housekeeping drops are filtered (folded into, done in, fixed inline in) so the profile shows choices, e.g. the denied removal of the dev-mods copy; all text passes c.plain and c.fit` → no findings [tree da27683ff17d] (2026-10-03T08:51:49Z)
## Log
- 2026-10-03T03:05:24Z created
- 2026-10-03T08:50:09Z planned from capture
- 2026-10-03T08:50:09Z focused
- 2026-10-03T08:51:49Z done
- 2026-10-03T08:51:49Z committed 06fe3af (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-super: 171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:
- research t0063-final-review: MEDIUM — `plugin/lib/fmcore.py:842-845` (FIX red→green requirement) and `plugin/lib/fmcli.py:71-73` (M/L lesson requirement) — the user expl…
- T-0114 [FEATURE S, done, 3 steps] fm queue --preview: usual time per item and what will need the user, gathered to answer at once — lesson: The brainstorm's 'overnight d…
- research t0041-slate-review: HIGH — INTENT — slate item 9 (`brainstorm-20260926-smarter-slate.md:16`)** "Sensitive-path audits: a diff touching auth/crypto/secrets/exec/…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_ideas.py
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmideas.py; re-ground the plan against them before editing
## Lessons
- Preference signal hides among bookkeeping: filter the records that say where work went before reading them as what the user wants.
## Files touched
- plugin/tests/test_taste.py
- plugin/lib/fmideas.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
