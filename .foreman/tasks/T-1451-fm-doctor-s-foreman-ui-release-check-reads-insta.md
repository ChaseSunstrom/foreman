---
id: T-1451
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T05:50:56Z
updated: 2026-10-22T13:41:34Z
base: 1aefd59155ef89113050c973c3712443ff11dead
base_tree: 6df4c201946115c955a39d8cda071bbc3182ac92
plan0_at: 2026-10-22T13:39:57Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
verified: strong
---
# Doctor: a directory marketplace's foreman-ui is read in place
## Raw request
> fm doctor's foreman-ui release check reads installed_plugins.json (0.7.0) but a directory marketplace is read in place (claude plugin list: Read from mods/foreman-ui, 0.18.3): PASS when the foreman marketplace source is this checkout's directory; false WARN today (rest of dropped T-1445)
## Interpretation
check_mod_release compares installed_plugins.json's cache copy to the repo, but Claude Code reads a directory marketplace in place (claude plugin list: Read from mods/foreman-ui 0.18.3), so today's WARN is false.
## Assumptions (confidence)
## Acceptance criteria
- [x] a directory marketplace at this checkout passes; a github one still warns — verify with `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_mod_release`
## Non-goals
## Approach (options → choice → why)
Read known_marketplaces.json beside the listing; foreman's source a directory resolving to this home → PASS 'read in place'. Other sources keep the hash compare.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] read known_marketplaces in check_mod_release
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_mod_release` → ✗ exit 1 · Ran 1 test in 0.003s / FAILED (failures=1) [ran] [tree dcdf69b1a300] (2026-10-22T13:39:58Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_mod_release` → exit 0 · Ran 1 test in 0.003s / OK [ran] [tree e2d52d7c9134] (2026-10-22T13:40:38Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_mod_release` → exit 0 · Ran 1 test in 0.002s / OK [ran] [tree 1c029f9bfb1c] (2026-10-22T13:40:39Z)
- (audit edge) `self: check_mod_release reads known_marketplaces.json beside the listing; PASS only when foreman's source is a directory whose realpath is this home; any other source keeps the hooks hash compare. Verified live: doctor now PASSes 'read in place'; claude plugin list confirms 'Read from' the checkout at 0.18.3.` → a malformed known_marketplaces (non-dict source, missing path) falls through to the old compare [tree 1c029f9bfb1c] (2026-10-22T13:40:39Z)
- (audit intent) `self: check_mod_release reads known_marketplaces.json beside the listing; PASS only when foreman's source is a directory whose realpath is this home; any other source keeps the hooks hash compare. Verified live: doctor now PASSes 'read in place'; claude plugin list confirms 'Read from' the checkout at 0.18.3.` → the warning existed so other sessions don't draw an old UI; with in-place reads they draw the checkout, so the check's purpose holds [tree 1c029f9bfb1c] (2026-10-22T13:40:39Z)
- (audit self) `self: check_mod_release reads known_marketplaces.json beside the listing; PASS only when foreman's source is a directory whose realpath is this home; any other source keeps the hooks hash compare. Verified live: doctor now PASSes 'read in place'; claude plugin list confirms 'Read from' the checkout at 0.18.3.` → no findings [tree 1c029f9bfb1c] (2026-10-22T13:40:39Z)
## Log
- 2026-10-22T05:50:56Z created
- 2026-10-22T05:56:03Z planned from capture
- 2026-10-22T13:39:57Z focused
- 2026-10-22T13:41:33Z done
- 2026-10-22T13:41:34Z committed 46935c5f (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1441-review: Verdict: changes needed.** The main hole is that the "gitignored and identical to the checkout" rule reads attacker-writable ignore rules. I read…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar finished tasks took 2–2 steps
- likely tests for the scope: plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md; re-ground the plan against them before editing
## Why not caught
the check was written when the marketplace was installed from a cache copy; the directory source arrived later
## Lessons
- Before trusting installed_plugins.json, ask claude plugin list what is actually read; directory marketplaces load in place.
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
