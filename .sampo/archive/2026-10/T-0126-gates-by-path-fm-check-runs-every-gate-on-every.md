---
id: T-0126
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_check_paths.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-10-03T04:44:01Z
updated: 2026-10-03T08:29:40Z
base: 3b20e5baac895a0c30de95f9043334481ef7d94c
base_tree: 29150495fd5bf902b5073da35a3cae0531f3c8a5
verified: strong
---
# Gates by path: a gate can declare the paths it covers and is skipped when none changed since its last pass
## Raw request
> Gates by path: fm check runs every gate on every task (~3 min); a check should declare the paths it covers (mods/** → mod tests, plugin/** → python suite) and run only when they changed
## Interpretation
fm check reruns every gate whenever anything in the tree changed; a gate that only covers mods/** reruns after a docs edit. Let a gate declare its paths; skip it (as a recorded pass) when nothing under them changed since its last passing run; --fresh and gates without paths keep today's behaviour.
## Assumptions (confidence)
## Acceptance criteria
- [x] A gate with paths is skipped (and says so) when only other files changed, runs when a covered file changed, and --fresh runs it; a gate without paths always runs — verify with `python3 plugin/tests/run.py -k test_check_paths`
- [x] All gates pass — verify with `fm check --fresh`
## Non-goals
## Approach (options → choice → why)
Options: (a) declared globs per gate (fm check paths N GLOB…), compared with git diff between the tree of the gate's last pass and now; (b) infer coverage from fm map's test links. Choice: (a): explicit, predictable, and a gate's real inputs (configs, fixtures, docs a test reads) aren't visible to the map; a wrong glob only means a skipped run that --fresh or the next change of a covered file catches.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test
2. [x] fm check paths and the skip in the runner
3. [x] Declare paths for this repo's gates; MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER (Gates by path) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_check_paths` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: CheckPaths 0s) / OK [ran] [tree de6941380793] (2026-10-03T08:24:55Z)
- (step 2) `python3 plugin/tests/run.py -k test_check_paths` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: CheckPaths 0s) / OK [ran] [tree de6941380793] (2026-10-03T08:24:56Z)
- (step 3) `fm check list` → exit 0 · 4. claude plugin test mods/foreman-ui  [paths: mods/foreman-ui/**] / 5. python3 plugin/tests/run.py [ran] [tree de6941380793] (2026-10-03T08:24:56Z)
- (step 1) `python3 plugin/tests/run.py -k test_check_paths` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: CheckPaths 1s) / OK [ran] [tree b8e708994e1a] (2026-10-03T08:28:46Z)
- (step 2) `python3 plugin/tests/run.py -k test_check_paths` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: CheckPaths 1s) / OK [ran] [tree b8e708994e1a] (2026-10-03T08:28:47Z)
- (step 3) `fm check list` → exit 0 · 4. claude plugin test mods/foreman-ui  [paths: mods/foreman-ui/**] / 5. python3 plugin/tests/run.py [ran] [tree b8e708994e1a] (2026-10-03T08:28:47Z)
- (ac 1) `python3 plugin/tests/run.py -k test_check_paths` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: CheckPaths 1s) / OK [ran] [tree b8e708994e1a] (2026-10-03T08:29:39Z)
- (ac 2) `fm check --fresh` → exit 0 · ✓ claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 57 tests across 1 file. [2.42s] (2.5 s) / ✓ python3 plugin/tests/run.py → exit 0 · Ran 573 tests in 21.6s (117 classes, 16 at a time; slowe [ran] [tree b8e708994e1a] (2026-10-03T08:29:39Z)
- (audit intent) `One fm-reviewer pass (intent + edge): changes needed, all fixed with tests: --no-renames (a file moved out counts), a skip carries its real run's time and tree so chained skips expire 12 h after that run and diff against its tree (a write by another gate counts), and this repo's roundtrip/bench paths now include install.sh, plugin/bin, the bench script and fixtures. Kept: a skip in --evidence is recorded as a pass whose text says 'skipped: … since its pass at HH:MM', since it rests on a real pass of unchanged inputs.` → gates declare paths and skip only while their inputs are unchanged since a real pass within 12 h; --fresh and pathless gates behave as before; this repo's docs-only fm check drops from ~40 s to ~27 s [tree b8e708994e1a] (2026-10-03T08:29:39Z)
- (audit edge) `One fm-reviewer pass (intent + edge): changes needed, all fixed with tests: --no-renames (a file moved out counts), a skip carries its real run's time and tree so chained skips expire 12 h after that run and diff against its tree (a write by another gate counts), and this repo's roundtrip/bench paths now include install.sh, plugin/bin, the bench script and fixtures. Kept: a skip in --evidence is recorded as a pass whose text says 'skipped: … since its pass at HH:MM', since it rests on a real pass of unchanged inputs.` → renames, skip chains, writes by other gates, deleted files, pruned trees, edited commands, subdirectory roots and --fail-fast each run the gate when its inputs may have changed (tests for the first three) [tree b8e708994e1a] (2026-10-03T08:29:39Z)
## Log
- 2026-10-03T04:44:01Z created
- 2026-10-03T08:22:38Z planned from capture
- 2026-10-03T08:22:38Z focused
- 2026-10-03T08:28:48Z hypothesis: the seven fmcli edits were the planned feature plus review fixes, not a thrash; each was checked by test_check_paths and fm check
- 2026-10-03T08:29:39Z done
- 2026-10-03T08:29:40Z committed 44f2163 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0087-review: Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW.
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- research t0071-abc-review: MEDIUM** — `plugin/lib/fmcli.py:551-568` (`cmd_focus`/`_moved_since_planned`). `target.set_section("Related", related)` is only called inside …
- research t0063-final-review: MEDIUM — `plugin/lib/fmcore.py:842-845` (FIX red→green requirement) and `plugin/lib/fmcli.py:71-73` (M/L lesson requirement) — the user expl…
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Lessons
- A cache entry derived from another must carry the original's time and base forward; re-stamping a derived entry turns a 12-hour cache into a permanent one.
## Files touched
- plugin/tests/test_check_paths.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
