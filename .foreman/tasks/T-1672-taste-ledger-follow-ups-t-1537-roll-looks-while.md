---
id: T-1672
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-22T21:07:32Z
updated: 2026-10-28T22:15:06Z
base: 2e553d0497379bc10afdf7fe2333cee22d8b1196
base_tree: cf92d4510bb09fb7b68b456494c7d1ecfe4bd90c
plan0_at: 2026-10-28T21:57:22Z
plan0_scope: []
verified: strong
---
# Taste ledger follow-ups: look of the day, bisect, séance, DESIGN.md history
## Raw request
> Taste ledger follow-ups (T-1537): roll looks while idle, bisect taste across history, a style séance, the foreman-ui pane surface, kept/reverted detected from DESIGN.md history (needs a decision on the named-file rule)
## Interpretation
The four follow-ups T-1537 left: a look of the day drawn with the ledger's lean (shown while idle), where taste turned, the departed looks, and kept/reverted read from DESIGN.md history. The named-file decision: DESIGN.md is read by default as Foreman's own record; other paths only when named.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm looks roll draws the look of the day, stable within a day, leaning on the ledger (kept looks win more), and fm ui / the pane's idle row show it once taste exists — verify with `python3 plugin/tests/run.py test_taste_more`
- [x] fm looks bisect names the signal where the leading look changed, or says the taste held; under four signals it is refused with rc 2 — verify with `python3 plugin/tests/run.py test_taste_more`
- [x] fm looks seance lists departed looks (below 0) with their last words and the nearest look that lives on — verify with `python3 plugin/tests/run.py test_taste_more`
- [x] fm looks history [PATH] reads DESIGN.md's git history into stints, records kept (held ≥7 days) or reverted (replaced sooner) once per stint, and refuses a file with no history — verify with `python3 plugin/tests/run.py test_taste_more test_taste_ledger test_taste`
## Non-goals
## Approach (options → choice → why)
a separate fmlooks module / pane-only roll computed in TS / history parsed from a diff of every commit / everything in fmtaste with stdlib random seeded by date and git log+show, deduped by FILE@sha → the last → one module, deterministic tests, history records each stint once so reruns are no-ops
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first: test_taste_more
2. [x] fmtaste roll/roll_line, bisect, seance, history; cmd_looks verbs
3. [x] fm ui look field and the pane idle row
4. [x] docs, gates, review
## Resume here
<!-- auto -->
- 2026-10-28T22:02:57Z step 4/4: docs, gates, review
- git: foreman/build; 9 uncommitted: CHANGELOG.md, MASTER.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/fmcli.py, plugin/lib/fmtaste.py, plugin/lib/fmwatch.py, plugin/tests/test_taste_more.py
- touched since last checkpoint: plugin/tests/test_taste_more.py, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md, MASTER.md
- failures met: types; assertionerror: 0 != 0 : fm: too few to bisect: 0 signals in the ledger, 0 at least (fm l…; keyerror: 'look'
## Docs impact
MASTER.md, CHANGELOG.md, plugin/commands/looks.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_taste_more` → ✗ exit 1 · Ran 7 tests in 0.6s (4 classes, 16 at a time; slowest: History 0s, Roll 0s, Bisect 0s) / FAILED (4 classes) [ran] [tree 7a591fa02ade] (2026-10-28T21:57:27Z)
- (step 2) `python3 plugin/tests/run.py test_taste_more test_taste_ledger test_taste` → exit 0 · Ran 33 tests in 5.1s (13 classes, 16 at a time; slowest: CorrectionClusters 5s, Taste 2s, Ledger 2s) / OK [ran] [tree 175bc3323768] (2026-10-28T21:59:29Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 150 tests across 4 files. [17.14s] [ran] [tree 175bc3323768] (2026-10-28T21:59:47Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 4062 tests in 195.0s (973 classes, 16 at a time; slowest: Worker 105s, Stop 62s, Bench 51s) / FAILED (1 classes) [ran] [tree 175bc3323768] (2026-10-28T22:04:09Z)
- (step 4) `python3 plugin/tests/run.py test_taste_more test_taste_ledger test_taste test_looks_gallery test_board_surfaces test_ui` → exit 0 · Ran 97 tests in 13.6s (29 classes, 16 at a time; slowest: UiView 13s, Roll 4s, CorrectionClusters 3s) / OK [ran] [tree 2c0fa00d8e69] (2026-10-28T22:10:17Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmtaste.py, plugin/lib/fmwatch.py, plugin/lib/ui-demo.json — commit it through a task, or git ch; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                39.9    41.5     150  [0] / SessionEnd                  34.7    37.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 0822ac03dd04] (2026-10-28T22:14:12Z)
- (ac 1) `python3 plugin/tests/run.py test_taste_more` → exit 0 · Ran 9 tests in 0.8s (4 classes, 16 at a time; slowest: Roll 1s, Seance 0s, History 0s) / OK [ran] [tree 0822ac03dd04] (2026-10-28T22:14:27Z)
- (ac 2) `python3 plugin/tests/run.py test_taste_more` → exit 0 · Ran 9 tests in 0.8s (4 classes, 16 at a time; slowest: Roll 1s, Seance 0s, History 0s) / OK [ran] [tree 0822ac03dd04] (2026-10-28T22:14:27Z)
- (ac 3) `python3 plugin/tests/run.py test_taste_more` → exit 0 · Ran 9 tests in 0.8s (4 classes, 16 at a time; slowest: Roll 1s, Seance 0s, History 0s) / OK [ran] [tree 0822ac03dd04] (2026-10-28T22:14:27Z)
- (ac 4) `python3 plugin/tests/run.py test_taste_more test_taste_ledger test_taste` → exit 0 · Ran 35 tests in 2.8s (13 classes, 16 at a time; slowest: CorrectionClusters 3s, Taste 1s, Ledger 1s) / OK [ran] [tree 0822ac03dd04] (2026-10-28T22:14:27Z)
- (step 1) `python3 plugin/tests/run.py test_taste_more` → exit 0 · Ran 9 tests in 0.8s (4 classes, 16 at a time; slowest: Roll 1s, Seance 0s, History 0s) / OK [ran] [tree 0822ac03dd04] (2026-10-28T22:14:27Z)
- (audit intent) `one fm-reviewer pass over the diff (approve with nits); every nit fixed test-first: git deadline, literal pathspecs, window-cut stint, manual-keep dedup, looks.md verbs` → roll/bisect/seance/history do what the brief asked; history reads DESIGN.md by default and only a typed path otherwise [tree 0822ac03dd04] (2026-10-28T22:14:27Z)
- (audit adversary) `one fm-reviewer pass over the diff (approve with nits); every nit fixed test-first: git deadline, literal pathspecs, window-cut stint, manual-keep dedup, looks.md verbs` → git runs with --literal-pathspecs, no signature checks and a 60 s deadline; a slow or missing git is bad input (exit 1), never a hang [tree 0822ac03dd04] (2026-10-28T22:14:27Z)
- (audit edge) `one fm-reviewer pass over the diff (approve with nits); every nit fixed test-first: git deadline, literal pathspecs, window-cut stint, manual-keep dedup, looks.md verbs` → a history longer than 200 versions drops the stint the window cut; a keep said by hand during a stint is not counted twice; too few signals to bisect exits 1 [tree 0822ac03dd04] (2026-10-28T22:14:27Z)
- (audit operator) `one fm-reviewer pass over the diff (approve with nits); every nit fixed test-first: git deadline, literal pathspecs, window-cut stint, manual-keep dedup, looks.md verbs` → the pane shows the look line only idle and only once the ledger has taste; the demo view carries the new field [tree 0822ac03dd04] (2026-10-28T22:14:27Z)
- (audit maintainer) `one fm-reviewer pass over the diff (approve with nits); every nit fixed test-first: git deadline, literal pathspecs, window-cut stint, manual-keep dedup, looks.md verbs` → the four verbs share one _followups path; HISTORY_SECONDS and HISTORY_MAX are the knobs; dedup sees only EVENTS_KEEP (ponytail note) [tree 0822ac03dd04] (2026-10-28T22:14:27Z)
## Log
- 2026-10-22T21:07:32Z created
- 2026-10-28T21:57:21Z planned from capture
- 2026-10-28T21:57:22Z focused
- 2026-10-28T21:58:22Z bad input exits 1 (UsageError, Foreman's convention), not 2: AC 2's 'rc 2' reads rc 1
- 2026-10-28T22:15:04Z done
- 2026-10-28T22:15:06Z committed 8bfd3dc1 (11 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1537 [FEATURE M, done, 4 steps] Round 3 (T-1520): Taste ledger: learn from what the user keeps and from 'not like that', a — lesson: Any score fed by a bulk input (a g…
- research T-1537-review: Verdict: changes needed.** The acceptance criteria are met. The three named features that were not built are the main gap, and the ledger can be …
- T-1626 [FEATURE M, done, 5 steps] fm code's motion clock reads the project's Motion Score; fm motion compile --to lab: a page to play, scrub and edit each motion — lesso…
- decision 2026-10-23: T-1650: build the trading cards now (fm page looks --cards); the shader sketchbook and the site gallery become their own items
- similar finished tasks took 4–5 steps
## Lessons
- a new fm ui view field also goes in ui-demo.json: test_board_surfaces checks the demo has every real key
## Plan gaps
- failed first: step 1 tests first: test_taste_more
- failed first: step 4 docs, gates, review
## Files touched
- plugin/tests/test_taste_more.py
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
- MASTER.md
- plugin/commands/looks.md
- plugin/lib/fmtaste.py
- plugin/lib/ui-demo.json
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmcli.py
- plugin/lib/fmwatch.py
