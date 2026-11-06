---
id: T-2124
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T08:06:47Z
updated: 2026-10-30T10:20:06Z
base: b38b99cc4264ebd3f47ca9cf24a2ff5d290adb3c
base_tree: 9943156891576bde225a611b082559233ce05594
plan0_at: 2026-10-30T09:59:22Z
plan0_scope: []
verified: strong
---
# Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the self-inbox (Mission 3 brief 5)
## Raw request
> Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the self-inbox (Mission 3 brief 5)
## Interpretation
fmscout gains probe_find: in a user project (not Foreman's home; its git user.email or the project's registered owner matches the commit author of HEAD, else refused with a reason), fm find --rank runs over p.root with precision(p); only proven leads are captured, at most 3 a day across runs (meta find_day counter), never one whose fingerprint (finder, file, symbol, says normalised) sits in the refutation ledger (a find_key task that was dropped or reverted). Proven today means a kind whose own check is its proof re-run cold (dep, docs, secret: the scan rerun on a fresh read agrees); test-judged kinds (vuln, untested, slow, flaky) stay leads until T-2122's prove gate lands and then pass through it. probe_doctor's FAILs found while scouting a user project go to Foreman's self-inbox (source self), not the user's project.
## Assumptions (confidence)
## Acceptance criteria
- [x] scout files only proven findings in a user project, capped, never a dismissed fingerprint, and doctor faults go to the self-inbox — verify with `python3 plugin/tests/run.py test_scout`
## Non-goals
## Approach (options → choice → why)
A) wait for T-2122 and capture nothing until prove exists: blocks a tier-3 brief on an L approval. B) capture ranked leads unproven: breaks 'proven only' and floods the inbox. C) chosen: a proof hook per kind; self-proving kinds pass now, test-judged kinds queue as leads (fm find --capture is still the manual path) and flip on when fm find prove lands. Refutation ledger = existing briefs' find_key with dropped status or a reverted fate (no new file).
## Risks and rollback
## Execution prompt
## Steps
1. [x] probe_find with cap and ownership
2. [x] refutation ledger + doctor routing
## Resume here
<!-- auto -->
- 2026-10-30T10:09:04Z steps 2/2 done
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmfind.py, plugin/lib/fmscout.py, plugin/tests/test_find.py, plugin/tests/test_scout.py
- touched since last checkpoint: CHANGELOG.md, MASTER.md, README.md, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2127-impl.edit, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2124-fix-tests.edit, plugin/tests/test_find.py, plugin/tests/test_scout.py
## Docs impact
MASTER.md, CHANGELOG.md, README.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 24 tests in 12.9s (5 classes, 16 at a time; slowest: Scout 13s, Mandate 3s, ScoutDrive 1s) / OK [ran] [tree ec4b1ba812a9] (2026-10-30T10:02:15Z)
- (step 2) `python3 plugin/tests/run.py test_scout test_find` → exit 0 · Ran 52 tests in 13.1s (18 classes, 16 at a time; slowest: Scout 13s, FindCli 6s, Mandate 3s) / OK [ran] [tree ec4b1ba812a9] (2026-10-30T10:02:28Z)
- (step 1) `python3 plugin/tests/run.py test_scout test_find` → exit 0 · Ran 54 tests in 13.0s (18 classes, 16 at a time; slowest: Scout 13s, FindCli 6s, Mandate 3s) / OK [ran] [tree 821b75acf6f2] (2026-10-30T10:13:07Z)
- (step 2) `python3 plugin/tests/run.py test_scout test_night` → exit 0 · Ran 46 tests in 13.1s (14 classes, 16 at a time; slowest: Scout 13s, Night 6s, Mandate 3s) / OK [ran] [tree 821b75acf6f2] (2026-10-30T10:13:21Z)
- (audit intent) `reviewer pass vs brief: proven only, capped, never dismissed, doctor to self-inbox` → met; scout now never refiles a key it filed or a settled one, regressions stay fm find's [tree 821b75acf6f2] (2026-10-30T10:16:07Z)
- (audit adversary) `forged commit email, hostile repo git config, symlinked md to outside/dev/zero` → fixed: confirm when others commit; fmdocs git runs fsmonitor/hooks off; links skipped, reads capped 1 MB [tree 821b75acf6f2] (2026-10-30T10:16:08Z)
- (audit edge) `no commits, no git, rolling 24 h, same-second created, home inbox unwritable` → handled: empty authors returns []; explicit None check on age; OSError becomes a probe error [tree 821b75acf6f2] (2026-10-30T10:16:08Z)
- (audit operator) `open find leads vs MAX_OPEN across days` → capped: at most 3 open and 3 per 24 h [tree 821b75acf6f2] (2026-10-30T10:16:08Z)
- (audit maintainer) `settled() and open cap coverage` → tests added: a dropped fm find key never refiled; six leads so the open cap is exercised [tree 821b75acf6f2] (2026-10-30T10:16:08Z)
- (ac 1) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 26 tests in 13.0s (5 classes, 16 at a time; slowest: Scout 13s, Mandate 3s, ScoutDrive 1s) / OK [ran] [tree 821b75acf6f2] (2026-10-30T10:17:20Z)
- (audit intent) `one fm-reviewer pass over five lenses; 6 findings fixed test-first, 3 kept as logged ceilings` → never refiles a filed or settled key [tree 821b75acf6f2] (2026-10-30T10:17:20Z)
- (audit adversary) `one fm-reviewer pass over five lenses; 6 findings fixed test-first, 3 kept as logged ceilings` → confirm where others commit; fmdocs git safe flags, no links, 1 MB cap [tree 821b75acf6f2] (2026-10-30T10:17:20Z)
- (audit edge) `one fm-reviewer pass over five lenses; 6 findings fixed test-first, 3 kept as logged ceilings` → no commits/no git say nothing; home inbox error is a probe error [tree 821b75acf6f2] (2026-10-30T10:17:20Z)
- (audit operator) `one fm-reviewer pass over five lenses; 6 findings fixed test-first, 3 kept as logged ceilings` → 3 open and 3 per 24 h [tree 821b75acf6f2] (2026-10-30T10:17:20Z)
- (audit maintainer) `one fm-reviewer pass over five lenses; 6 findings fixed test-first, 3 kept as logged ceilings` → settled() and open cap tested [tree 821b75acf6f2] (2026-10-30T10:17:20Z)
## Log
- 2026-10-30T08:06:47Z created
- 2026-10-30T09:59:22Z focused
- 2026-10-30T10:13:21Z scope: plugin/lib/fmdocs.py and plugin/tests/test_find.py widened — review found fmdocs ran git on fm find's untrusted trees without fsmonitor/hooks off and read docs uncapped; fixed where fm find calls it
- 2026-10-30T10:17:36Z done
- 2026-10-30T10:17:37Z committed 183de795 (8 files)
- 2026-10-30T10:17:43Z guard authorization added: publish
- 2026-10-30T10:20:06Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2121 [FEATURE L, done, 2 steps] fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (…
- T-2122 [FEATURE L, planned, 2 steps] fm find prove: proof tickets, red 3/3 for an assertion and mutate-to-confirm; unproven candidates become leads (Mission 3 brief 3)
- research T-2125-review: Verdict:** approve with nits. I found no HIGH issues. There are three MEDIUM design gaps worth fixing or capturing, plus some LOW nits. I did not…
- decision 2026-10-30: fm find stays read-only: the failing-gates finder and each candidate's probe move to the prove gate (T-2122), which already runs repo code under a s…
## Lessons
- A test written red-first can still pass vacuously: give it enough fixture (six leads, a backticked dead path) that the guarded branch is the only thing keeping it green
## Files touched
- plugin/tests/test_scout.py
- plugin/lib/fmfind.py
- plugin/lib/fmscout.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/tests/test_find.py
- plugin/lib/fmdocs.py
