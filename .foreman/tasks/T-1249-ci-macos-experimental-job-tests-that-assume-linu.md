---
id: T-1249
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-16T23:14:12Z
updated: 2026-10-20T17:15:47Z
inferred_deps: [T-0352]
inferred_why: T-0352: macOS CI job depends on the published CI pipelines
base: cd7da43f1fc0c3b23bac5c053f71343e8f6af8b0
base_tree: 218dc1d43dc72de560f6d0e028169b115cab3165
plan0_at: 2026-10-20T17:05:57Z
plan0_scope: []
verified: strong
---
# CI macOS (experimental job): tests that assume Linux fail there: /proc/PID/stat reads, /tm
## Raw request
> CI macOS (experimental job): tests that assume Linux fail there: /proc/PID/stat reads, /tmp being /private/tmp (the guard's scratchpad match blocks fm secrets > /tmp/claude-1000/.../scratchpad), a children/ state path, a recon test needing GNU grep, an import-site count, an 800-char output bound (930). Make them portable or skip them on darwin with a reason
## Interpretation
Make Foreman work on macOS, not just pass there: the macOS CI job's 11 failures are mostly product bugs. (1) /tmp is a link to /private/tmp, so the guard's scratch check compares a resolved path with unresolved scratch folders: writes to Claude Code's scratchpad read as credentials, and a builder's /tmp write as outside its worktree. (2) fm explain and fm deps calls pass \b, \s and \w to git grep -E, GNU extensions BSD regex ignores, so they find nothing. (3) The reaper and the bus read /proc, which macOS lacks. (4) Two tests assume Linux paths (an 800-character bound beside a long macOS temp path; the encoded home '-home-USER-').
## Assumptions (confidence)
## Acceptance criteria
- [x] the guard treats a scratch folder reached through a link (macOS /tmp → /private/tmp) as scratch: a secret-sounding file there isn't a credential and a builder may write there — verify with `python3 plugin/tests/run.py test_guard test_builder`
- [x] fm explain and fm deps calls find definitions and import sites with a git whose regex lacks GNU classes — verify with `python3 plugin/tests/run.py test_knowledge`
- [x] the reaper and the bus work without /proc (ps fallback) — verify with `python3 plugin/tests/run.py test_reaper test_bus`
- [x] the macOS job's other failing tests no longer assume Linux paths — verify with `python3 plugin/tests/run.py test_cli test_page`
## Non-goals
## Approach (options → choice → why)
Options: (a) fix each at its root: scratch folders resolved in fmguard.Ctx; git grep with a fixed string, then Python re on the lines; a ps fallback where /proc is missing; tests built from the real home and path lengths; (b) skip the tests on macOS (hides real bugs); (c) PCRE via git grep -P (not in every git build). Choice: (a). Reproduced on Linux where possible: a symlinked scratch folder, a fake git that ignores GNU regex classes, /proc hidden behind a helper the test can switch off. The guard case 'git reset --hard in /tmp' stays open until a macOS run shows why.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests that reproduce each on Linux
2. [x] Scratch folders resolved in fmguard.Ctx
3. [x] git grep with -F, then Python re (fmrecall, fmoutside)
4. [x] ps fallback for /proc (fmideas reaper, fmbus)
5. [x] Test fixes for Linux-only paths; docs
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.ScratchNames test_knowledge.BsdRegex test_reaper.SweepWithoutProc test_bus test_cli.AuditPrep test_page.PageHardening` → ✗ exit 1 · Ran 39 tests in 19.652s / FAILED (failures=2) [ran] [tree 6b6528ee1f60] (2026-10-20T17:08:06Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_builder test_knowledge test_reaper test_bus test_cli test_page` → exit 0 · Ran 367 tests in 23.1s (115 classes, 16 at a time; slowest: TaskLifecycle 23s, Contract 10s, StateViews 10s) / OK [ran] [tree 9c74fda3a535] (2026-10-20T17:10:07Z)
- (step 3) `python3 plugin/tests/run.py test_guard test_builder test_knowledge test_reaper test_bus test_cli test_page` → exit 0 · Ran 367 tests in 23.0s (115 classes, 16 at a time; slowest: TaskLifecycle 23s, Contract 10s, StateViews 10s) / OK [ran] [tree 5555d40e47d1] (2026-10-20T17:11:09Z)
- (step 4) `python3 plugin/tests/run.py test_guard test_builder test_knowledge test_reaper test_bus test_cli test_page` → exit 0 · Ran 367 tests in 23.1s (115 classes, 16 at a time; slowest: TaskLifecycle 23s, Contract 10s, StateViews 10s) / OK [ran] [tree 5555d40e47d1] (2026-10-20T17:11:32Z)
- (step 5) `python3 plugin/tests/run.py test_guard test_builder test_knowledge test_reaper test_bus test_cli test_page` → exit 0 · Ran 367 tests in 22.9s (115 classes, 16 at a time; slowest: TaskLifecycle 23s, Contract 10s, StateViews 10s) / OK [ran] [tree 5555d40e47d1] (2026-10-20T17:11:56Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_builder` → exit 0 · Ran 214 tests in 7.2s (67 classes, 16 at a time; slowest: Contract 7s, GuardAgainstBash 5s, Brief 4s) / OK [ran] [tree 5555d40e47d1] (2026-10-20T17:13:19Z)
- (ac 2) `python3 plugin/tests/run.py test_knowledge` → exit 0 · Ran 7 tests in 0.6s (7 classes, 16 at a time; slowest: PriorArt 0s, Chesterton 0s, Decision 0s) / OK [ran] [tree 5555d40e47d1] (2026-10-20T17:13:19Z)
- (ac 3) `python3 plugin/tests/run.py test_reaper test_bus` → exit 0 · Ran 31 tests in 8.6s (9 classes, 16 at a time; slowest: Timeout 8s, Watch 5s, Approvals 4s) / OK [ran] [tree 5555d40e47d1] (2026-10-20T17:13:19Z)
- (ac 4) `python3 plugin/tests/run.py test_cli test_page` → exit 0 · Ran 115 tests in 20.7s (32 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 8s, AuditPrep 6s) / OK [ran] [tree 5555d40e47d1] (2026-10-20T17:13:19Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_builder test_knowledge test_reaper test_bus test_cli test_page test_guard_cases` → exit 0 · Ran 367 tests in 23.3s (115 classes, 16 at a time; slowest: TaskLifecycle 23s, Contract 11s, StateViews 10s) / OK [ran] [tree 5555d40e47d1] (2026-10-20T17:13:19Z)
- (audit intent) `self review of each fix against the macOS job's log; reproduced three of the four product bugs on Linux (a linked scratch folder, a git that ignores GNU classes, the reaper with /proc switched off); the fourth (bus) already had a ps path` → macOS is where many Claude Code users are; these were product bugs there (scratchpad writes refused, two search commands finding nothing, crashed helpers never reaped), not just red tests [tree 5555d40e47d1] (2026-10-20T17:13:19Z)
- (audit adversary) `self review of each fix against the macOS job's log; reproduced three of the four product bugs on Linux (a linked scratch folder, a git that ignores GNU classes, the reaper with /proc switched off); the fourth (bus) already had a ps path` → scratch folders now also count by their real path; only folders the environment names (Claude Code's scratchpad, TMPDIR, /tmp, /var/tmp) are added, the main checkout is confined before the scratch exemption and credential folders are matched before it, so a link can't open either; the reaper kills a group only when ps shows the helper's own flag and start time, or the dead leader's pid still names a live group [tree 5555d40e47d1] (2026-10-20T17:13:19Z)
- (audit edge) `self review of each fix against the macOS job's log; reproduced three of the four product bugs on Linux (a linked scratch folder, a git that ignores GNU classes, the reaper with /proc switched off); the fourth (bus) already had a ps path` → a git grep -F candidate line is kept only when Python's regex matches its text after file:line; a ps start time with spaces is closed up for the registry and never compared as a number; tests whose own helpers read /proc skip off Linux, and SweepWithoutProc runs the ps path on Linux [tree 5555d40e47d1] (2026-10-20T17:13:19Z)
- (audit operator) `self review of each fix against the macOS job's log; reproduced three of the four product bugs on Linux (a linked scratch folder, a git that ignores GNU classes, the reaper with /proc switched off); the fourth (bus) already had a ps path` → the guard case 'git reset --hard in /tmp' still differs on macOS for a reason not found without a Mac; the macOS job stays experimental until a run shows it [tree 5555d40e47d1] (2026-10-20T17:13:19Z)
- `cd plugin/tests && python3 -m unittest test_guard.ScratchNames test_knowledge.BsdRegex test_reaper.SweepWithoutProc` → ✗ exit 1 · Ran 9 tests in 0.749s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree 5555d40e47d1] (2026-10-20T17:14:18Z)
- `cd plugin/tests && python3 -m unittest test_guard.ScratchNames test_knowledge.BsdRegex test_reaper.SweepWithoutProc` → exit 0 · Ran 9 tests in 0.696s / OK [ran] [tree 5555d40e47d1] (2026-10-20T17:14:18Z)
- `python3 plugin/tests/run.py test_guard test_builder test_knowledge test_reaper test_bus test_cli test_page test_guard_cases` → exit 0 · Ran 367 tests in 23.5s (115 classes, 16 at a time; slowest: TaskLifecycle 23s, Contract 10s, StateViews 10s) / OK [ran] [tree 5555d40e47d1] (2026-10-20T17:14:50Z)
- (audit intent) `self review of each fix against the macOS job's log; reproduced three of the four product bugs on Linux (a linked scratch folder, a git that ignores GNU classes, the reaper with /proc switched off); the fourth (bus) already had a ps path` → macOS is where many Claude Code users are; these were product bugs there (scratchpad writes refused, two search commands finding nothing, crashed helpers never reaped), not just red tests [tree 5555d40e47d1] (2026-10-20T17:14:50Z)
- (audit adversary) `self review of each fix against the macOS job's log; reproduced three of the four product bugs on Linux (a linked scratch folder, a git that ignores GNU classes, the reaper with /proc switched off); the fourth (bus) already had a ps path` → scratch folders now also count by their real path; only folders the environment names (Claude Code's scratchpad, TMPDIR, /tmp, /var/tmp) are added, the main checkout is confined before the scratch exemption and credential folders are matched before it, so a link can't open either; the reaper kills a group only when ps shows the helper's own flag and start time, or the dead leader's pid still names a live group [tree 5555d40e47d1] (2026-10-20T17:14:50Z)
- (audit edge) `self review of each fix against the macOS job's log; reproduced three of the four product bugs on Linux (a linked scratch folder, a git that ignores GNU classes, the reaper with /proc switched off); the fourth (bus) already had a ps path` → a git grep -F candidate line is kept only when Python's regex matches its text after file:line; a ps start time with spaces is closed up for the registry and never compared as a number; tests whose own helpers read /proc skip off Linux, and SweepWithoutProc runs the ps path on Linux [tree 5555d40e47d1] (2026-10-20T17:14:50Z)
- (audit operator) `self review of each fix against the macOS job's log; reproduced three of the four product bugs on Linux (a linked scratch folder, a git that ignores GNU classes, the reaper with /proc switched off); the fourth (bus) already had a ps path` → the guard case 'git reset --hard in /tmp' still differs on macOS for a reason not found without a Mac; the macOS job stays experimental until a run shows it [tree 5555d40e47d1] (2026-10-20T17:14:50Z)
## Log
- 2026-10-16T23:14:12Z created
- 2026-10-20T16:53:29Z set tier=M
- 2026-10-20T17:05:56Z focused
- 2026-10-20T17:15:46Z done
- 2026-10-20T17:15:47Z committed a14fc15a (11 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research T-1044-review: Verdict: changes needed.** There is one MEDIUM regression, and the pid-reuse guard itself is sound. [stale: plugin/lib/fmideas.py changed since i…
- research rsi-pass-20261008: 1. **Answer.** I could ground one improvement fully (the pipe-shell false block) and one partly (state-direct from guessed variable targets).…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
## Why not caught
CI's macOS job was experimental and its failures were read as test portability, not product bugs; the Linux suite can't see /private/tmp or BSD regex
## Lessons
- A failing portability test is often a product bug on that platform: reproduce the platform's difference on Linux (a link, a fake git, a missing /proc) instead of skipping the test
## Plan gaps
- failed first: step 1 Failing tests that reproduce each on Linux
## Files touched
- plugin/tests/test_bus.py
- plugin/tests/test_cli.py
- plugin/tests/test_guard.py
- plugin/tests/test_knowledge.py
- plugin/tests/test_page.py
- plugin/tests/test_reaper.py
- plugin/lib/fmguard.py
- plugin/lib/fmoutside.py
- plugin/lib/fmrecall.py
- plugin/lib/fmideas.py
- CHANGELOG.md
