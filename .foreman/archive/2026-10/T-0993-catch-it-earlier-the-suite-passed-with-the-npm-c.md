---
id: T-0993
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-15T23:37:02Z
updated: 2026-10-16T00:01:54Z
base: 0f00ccfd9fae8650929cfeca3ed1cdcbb3cbb511
base_tree: 4f6c47b55908e0fd0ba21d8b6c113a8e26777c0e
verified: strong
---
# Catch the claude lockout gap before it ships (T-0993)
## Raw request
> T-0992 (T-0990's ~/.local/bin fallback bypasses the tests' claude lockout when a test replaces PATH: test runs reached the paid binary) wasn't caught before it shipped: the suite passed with the npm claude on PATH; the gap only showed once it was gone and a test replaced PATH
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A test fails when a test replaces PATH and claude_path could reach a claude outside the lockout stub — verify with `python3 plugin/tests/run.py -k test_a_test_that_replaces_path_still_cant_reach_the_paid_claude`
- [x] claude_path resolves only to the lockout stub while a test replaces PATH — verify with `python3 plugin/tests/run.py -k test_a_test_that_replaces_path_still_cant_reach_the_paid_claude`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Write a failing test in plugin/tests that replaces PATH and asserts claude_path resolves only to the lockout stub; run it with FOREMAN_NATIVE_BIN unset and confirm it fails
2. [x] Make it pass by keeping the lockout in place (product change only if the test shows one); run fm check
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_test_that_replaces_path_still_cant_reach_the_paid_claude` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: SuiteHygiene 0s) / FAILED (1 classes) [ran] [tree 1049024a373f] (2026-10-16T00:01:41Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_test_that_replaces_path_still_cant_reach_the_paid_claude` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: SuiteHygiene 0s) / OK [ran] [tree 003fdf576e72] (2026-10-16T00:01:42Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_test_that_replaces_path_still_cant_reach_the_paid_claude` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: SuiteHygiene 0s) / OK [ran] [tree 003fdf576e72] (2026-10-16T00:01:51Z)
- (ac 2) `python3 plugin/tests/run.py -k test_a_test_that_replaces_path_still_cant_reach_the_paid_claude` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: SuiteHygiene 0s) / OK [ran] [tree 003fdf576e72] (2026-10-16T00:01:51Z)
- `python3 plugin/tests/run.py test_suite_hygiene` → exit 0 · Ran 5 tests in 1.5s (2 classes, 16 at a time; slowest: UndefinedNames 1s, SuiteHygiene 1s) / OK [ran] [tree 003fdf576e72] (2026-10-16T00:01:51Z)
- (audit edge) `self: a suite-hygiene test checks the environment every test's fm inherits: with PATH replaced, claude_path adds nothing; red with the helpers' FOREMAN_NATIVE_BIN line commented out, green with it` → on a machine with no ~/.local/bin/claude the test passes trivially, which is right (nothing to reach) [tree 003fdf576e72] (2026-10-16T00:01:51Z)
- (audit self) `self: a suite-hygiene test checks the environment every test's fm inherits: with PATH replaced, claude_path adds nothing; red with the helpers' FOREMAN_NATIVE_BIN line commented out, green with it` → no findings [tree 003fdf576e72] (2026-10-16T00:01:51Z)
## Log
- 2026-10-15T23:37:02Z created
- 2026-10-15T23:48:55Z planned from capture
- 2026-10-15T23:48:55Z focused
- 2026-10-15T23:50:21Z paused: focus moved to T-0989
- 2026-10-16T00:01:22Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T00:01:22Z focused
- 2026-10-16T00:01:48Z criterion 1 verify: `fm check` → `python3 plugin/tests/run.py -k test_a_test_that_replaces_path_still_cant_reach_the_paid_claude`
- 2026-10-16T00:01:48Z criterion 2 verify: `python3 plugin/tests/run.py -k claude` → `python3 plugin/tests/run.py -k test_a_test_that_replaces_path_still_cant_reach_the_paid_claude`
- 2026-10-16T00:01:52Z done
- 2026-10-16T00:01:54Z committed 02907e4 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0992 [FIX S, done, 2 steps] T-0990's ~/.local/bin fallback bypasses the tests' claude lockout when a test replaces PATH: test runs reached the paid binary
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- T-0891 [FEATURE S, done, 0 steps] Catch it earlier: local runs always had ~/.cache or XDG_RUNTIME_DIR; CI's fresh HOME is th
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
- similar finished tasks took 0–5 steps
## Plan gaps
- failed first: step 1 Write a failing test in plugin/tests that replaces PATH and asserts claude_path resolves only to th…
## Files touched
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/tests/test_suite_hygiene.py
- plugin/tests/helpers.py
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/tools/shot.py
- plugin/lib/fmambient.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/tests/test_ambient.py
- plugin/tests/test_hooks.py
