---
id: T-1914
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: scout
created: 2026-10-29T04:44:31Z
updated: 2026-10-29T04:56:28Z
base: cdf906a1fca232aba6ec7b5a419c00e979f1656e
base_tree: f4e9dcd69b117ba55be02f82ed550c773a801e68
plan0_at: 2026-10-29T04:47:36Z
plan0_scope: []
verified: strong
---
# Write stack cards for androidx.lifecycle:lifecycle-runtime-ktx, androidx.lifecycle:lifecycle-service, androidx.test.esp…
## Raw request
> Found by fm scout: dependencies in your projects with no stack card: androidx.lifecycle:lifecycle-runtime-ktx, androidx.lifecycle:lifecycle-service, androidx.test.espresso:espresso-core, androidx.test.ext:junit, androidx.test.uiautomator:uiautomator, androidx.test:core, androidx.test:core-ktx, androidx.test:rules. Write one card each to the spec in plugin/skills/library/SKILL.md (a writer subagent per batch), then fm lib check
## Interpretation
The gaps scan listed androidx deps the espresso and android cards already cover: a card names the bare Maven id (dep:espresso-core, as the spec says) but the scan only checked the group:artifact form; androidx.test, uiautomator and androidx.lifecycle had no signal.
## Assumptions (confidence)
## Acceptance criteria
- [x] a Gradle dep named by its bare id or a glob is not a gap — verify with `python3 plugin/tests/run.py test_library test_scout`
## Non-goals
## Approach (options → choice → why)
Options: (a) eight new cards; (b) one androidx-test card; (c) fix the scan to accept a card's bare-id signal and add globs to the existing espresso and android cards. Chose (c): root cause plus two signal lines, no duplicated card text.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fix the gap scan and the card signals
## Resume here
<!-- auto -->
- 2026-10-29T04:48:29Z step 1/1: fix the gap scan and the card signals
- git: foreman/build; 0 uncommitted
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_library test_scout` → red as expected (exit 1) · Ran 61 tests in 13.6s (12 classes, 16 at a time; slowest: Scout 13s, LibSources 6s, Mandate 2s) / FAILED (1 classes) [ran] [tree 3c2c14f43d26] (2026-10-29T04:49:49Z)
- (step 1) `python3 plugin/tests/run.py test_library test_scout` → ✗ exit 1 · Ran 61 tests in 13.6s (12 classes, 16 at a time; slowest: Scout 13s, LibSources 6s, Mandate 3s) / FAILED (1 classes) [ran] [tree 86206fabaa2a] (2026-10-29T04:50:06Z)
- (ac 1) `python3 plugin/tests/run.py test_library test_scout 2>&1 | grep -E "FAIL|Error|assert|^ " | head -20` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree 86206fabaa2a] (2026-10-29T04:50:23Z)
- (step 1) `python3 plugin/tests/run.py test_library test_scout` → exit 0 · Ran 61 tests in 13.5s (12 classes, 16 at a time; slowest: Scout 13s, LibSources 7s, Mandate 3s) / OK [ran] [tree 0ee62b57f12d] (2026-10-29T04:50:45Z)
- `python3 plugin/tests/run.py test_library` → ✗ exit 1 · Ran 42 tests in 7.5s (9 classes, 16 at a time; slowest: LibSources 6s, LibraryAdmit 2s, LibrarySearch 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 0ee62b57f12d] (2026-10-29T04:51:04Z)
- `python3 plugin/tests/run.py test_library` → exit 0 · Ran 42 tests in 6.7s (9 classes, 16 at a time; slowest: LibSources 6s, LibraryAdmit 2s, LibrarySearch 1s) / OK [ran] [tree 0ee62b57f12d] (2026-10-29T04:51:04Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmlib.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.5    44.8     150  [0] / SessionEnd                  36.6    39.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree 0ee62b57f12d] (2026-10-29T04:55:32Z)
- (ac 1) `python3 plugin/tests/run.py test_library test_scout` → exit 0 · Ran 61 tests in 13.9s (12 classes, 16 at a time; slowest: Scout 14s, LibSources 7s, Mandate 3s) / OK [ran] [tree 0ee62b57f12d] (2026-10-29T04:56:09Z)
- (audit edge) `self-review: scan rule only widens coverage by a card's bare artifact id (the spec's form); globs are anchored per-group` → a dep with no colon skips the bare check; a group:artifact whose bare id a card names is covered, an unrelated group:artifact stays a gap (test) [tree 0ee62b57f12d] (2026-10-29T04:56:09Z)
- (audit intent) `self-review: scan rule only widens coverage by a card's bare artifact id (the spec's form); globs are anchored per-group` → fm lib gaps no longer asks for cards the library already has [tree 0ee62b57f12d] (2026-10-29T04:56:09Z)
- (audit self) `self-review: scan rule only widens coverage by a card's bare artifact id (the spec's form); globs are anchored per-group` → no findings [tree 0ee62b57f12d] (2026-10-29T04:56:09Z)
## Log
- 2026-10-29T04:44:31Z created
- 2026-10-29T04:47:04Z set type=FIX, tier=S
- 2026-10-29T04:47:05Z planned: it has criteria and steps
- 2026-10-29T04:47:35Z focused
- 2026-10-29T04:56:26Z done
- 2026-10-29T04:56:28Z committed bda2bda0 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1251 [FEATURE S, done, 2 steps] Stack cards cover the 8 androidx dependencies fm scout found: new cards for DataStore, Macrobenchmark and the Car App Library; Compose …
- T-1016 [FEATURE S, done, 2 steps] Stack cards for the deps scout found: scipy, python-audio (librosa, soundfile, demucs), postprocessing; detect lines for playwright-cor…
- T-1020 [FEATURE S, done, 1 steps] Stack cards: SvelteKit adapters, Vite plugins, VS Code extension tooling and xterm.js detected
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
- similar finished tasks took 1–2 steps
## Lessons
- A scan that matches one spelling of a name misses the spec's other spelling: test both forms the spec allows
## Files touched
- plugin/tests/test_library.py
- CHANGELOG.md
- plugin/lib/fmlib.py
- plugin/skills/library/cards/jvm/android.md
- plugin/skills/library/cards/jvm/espresso.md
- plugin/tests/test_scout.py
