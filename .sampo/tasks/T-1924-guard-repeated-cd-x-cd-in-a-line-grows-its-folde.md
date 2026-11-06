---
id: T-1924
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T06:28:01Z
updated: 2026-10-29T07:05:11Z
base: 3a55d16504fa37e6342e17b946db9a6848d04b64
base_tree: ec38b0d99d968d55c977fbab7bda9b81c4b57683
plan0_at: 2026-10-29T06:36:37Z
plan0_scope: []
verified: strong
---
# Guard: repeated 'cd X; …; cd ..' in a ; line grows its folder sets exponentially (_moved/_
## Raw request
> Guard: repeated 'cd X; …; cd ..' in a ; line grows its folder sets exponentially (_moved/_cd_from on rd): a 20-folder loop takes 177 s in the hook (committed guard, before T-1921). Cap the cwds/rd sets (past ~64 folders collapse to unknown) and test the loop stays under 1 s
## Interpretation
A ; line of repeated 'cd dN; …; cd ..' blocks makes the guard's walk carry ever-larger folder sets: 14 blocks take 6.5 s and end in a too-many-folders refusal, 20 took 177 s before T-1921. The hook must stay fast and still judge tree writes.
## Assumptions (confidence)
## Acceptance criteria
- [x] 20 cd blocks in a ; line and a 20-folder for loop are judged in under 1 s each, and a tree write after a cd into Foreman still blocks — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
Profile first. Options: (a) cap each folder set, collapsing past the cap to one unknown folder; (b) dedupe/normalise folders at each step; (c) memoise the per-folder work. Choose after the profile shows where the time goes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Profile and fix the folder-set growth; timing test red then green
## Resume here
<!-- auto -->
- 2026-10-29T06:55:49Z step 1/1: Profile and fix the folder-set growth; timing test red then green
- git: foreman/build; 4 uncommitted: CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_pipes.py
- touched since last checkpoint: plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_pipes.py, CHANGELOG.md
- failures met: 0 or 0.0s allow
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_guard.TokenFallback.test_repeated_cds_in_a_line_are_judged_fast` → ✗ exit 124 (timed out after 60s) · timed out after 60s (start tree + this task's tests) [ran] [tree 5be2e13ac8ec] (2026-10-29T06:54:01Z)
- `python3 plugin/tests/run.py test_guard.TokenFallback.test_repeated_cds_in_a_line_are_judged_fast` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: TokenFallback 0s) / OK [ran] [tree 5be2e13ac8ec] (2026-10-29T06:54:01Z)
- (ac 1) `python3 plugin/tests/run.py test_guard 2>&1 | tail -15` → exit 0 · Ran 296 tests in 11.4s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 9s, Trust 8s) / OK [ran] [tree 7455f8b7898d] (2026-10-29T07:02:06Z)
- (step 1) `python3 plugin/tests/run.py test_guard 2>&1 | tail -15` → exit 0 · Ran 296 tests in 11.4s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 9s, Trust 8s) / OK [ran] [tree 7455f8b7898d] (2026-10-29T07:02:06Z)
- (ac 1) `python3 plugin/tests/run.py test_guard 2>&1 | grep -E "^(FAIL|AssertionError|Ran|OK|FAILED)|row|expected" | head -12` → exit 0 · Ran 296 tests in 8.3s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 7455f8b7898d] (2026-10-29T07:02:29Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 296 tests in 8.3s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree c85dcbc4e126] (2026-10-29T07:04:00Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 296 tests in 8.4s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree c85dcbc4e126] (2026-10-29T07:04:15Z)
- (audit intent) `one fm-reviewer pass (adversary focus) + realistic-line verdict diff vs HEAD + mutation run` → 20 cd blocks in a ; line never finished, now 0.02 s; 20-folder for loop 0.02 s; 7 blocks with substitutions no longer refused [tree c85dcbc4e126] (2026-10-29T07:04:15Z)
- (audit adversary) `one fm-reviewer pass (adversary focus) + realistic-line verdict diff vs HEAD + mutation run` → review found cd under nice/sudo/env and cd after a folder-removing command read as certain; both fixed, 4 rows red without the fix; env cd /abs && x closed too [tree c85dcbc4e126] (2026-10-29T07:04:15Z)
- (audit edge) `one fm-reviewer pass (adversary focus) + realistic-line verdict diff vs HEAD + mutation run` → case/comment bodies and computed command words keep their tails; mkdir -m makes cds may-fail; over 1024 folder entries refused in 0.01 s [tree c85dcbc4e126] (2026-10-29T07:04:15Z)
- (audit operator) `one fm-reviewer pass (adversary focus) + realistic-line verdict diff vs HEAD + mutation run` → 18 realistic lines give the same verdicts as HEAD [tree c85dcbc4e126] (2026-10-29T07:04:15Z)
- (audit maintainer) `one fm-reviewer pass (adversary focus) + realistic-line verdict diff vs HEAD + mutation run` → both caps share rm-outside, captured T-1929 [tree c85dcbc4e126] (2026-10-29T07:04:15Z)
- (audit intent) `one fm-reviewer pass (adversary focus) + realistic-line verdict diff vs HEAD + mutation run` → 20 cd blocks in a ; line never finished, now 0.02 s; 20-folder for loop 0.02 s; 7 blocks with substitutions no longer refused [tree c85dcbc4e126] (2026-10-29T07:04:33Z)
- (audit adversary) `one fm-reviewer pass (adversary focus) + realistic-line verdict diff vs HEAD + mutation run` → review found cd under nice/sudo/env and cd after a folder-removing command read as certain; both fixed, 4 rows red without the fix; env cd /abs && x closed too [tree c85dcbc4e126] (2026-10-29T07:04:33Z)
- (audit edge) `one fm-reviewer pass (adversary focus) + realistic-line verdict diff vs HEAD + mutation run` → case/comment bodies and computed command words keep their tails; mkdir -m makes cds may-fail; over 1024 folder entries refused in 0.01 s [tree c85dcbc4e126] (2026-10-29T07:04:33Z)
- (audit operator) `one fm-reviewer pass (adversary focus) + realistic-line verdict diff vs HEAD + mutation run` → 18 realistic lines give the same verdicts as HEAD [tree c85dcbc4e126] (2026-10-29T07:04:33Z)
- (audit maintainer) `one fm-reviewer pass (adversary focus) + realistic-line verdict diff vs HEAD + mutation run` → both caps share rm-outside, captured T-1929 [tree c85dcbc4e126] (2026-10-29T07:04:33Z)
## Log
- 2026-10-29T06:28:01Z created
- 2026-10-29T06:36:35Z planned: it has criteria and steps
- 2026-10-29T06:36:36Z focused
- 2026-10-29T06:52:30Z hypothesis: the last red row (curl … $(true) | bash wanting system) only got system from the tail 'true) | bash'; with the clean tail dropped the main walk reports the download-into-shell as pipe-shell, still blocked. Rules out a weakening: the row stays refused, under the category its own class names.
- 2026-10-29T07:00:41Z hypothesis: review found 2 regressions (wrapper-run cd taken as moving; cd certain though an earlier command may remove its folder); fix: a cd under a child wrapper is never certain, and once any earlier command isn't a known reader (cd/mkdir/_READS/git reads, substituting reads only) every later cd may fail
- 2026-10-29T07:04:44Z done
- 2026-10-29T07:04:46Z committed ba96df93 (4 files)
- 2026-10-29T07:05:11Z includes T-1927: Guard: a cd into a folder an earlier command on the line removes is read as certain (rm -r
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1809 [FIX M, done, 4 steps] CI's macOS job names what makes it time out: run.py --deadline stops below each job's cap, killing and naming running classes; slowest clas…
- T-1921 [FIX M, done, 3 steps] Guard reads a substitution behind 'cd /abs &&' from the starting folder too — lesson: When the guard trusts a cd folder, check the parsed a…
- research T-0339-review: Verdict: changes needed.** I found one high-severity bypass. I traced it by reading the code and could not run it, because this session has no ex…
- decision 2026-10-16: T-1080 self-approved under full autonomy: risk points from today's ledger (destructive guard blocks 1, failed closes 2) and today's Revert commits (…
## Measurements
20 cd blocks with $(…) in a ; line: never finished (killed at 60 s) → 0.02 s; 14 blocks: 6.5 s → 0.01 s; 20-folder for loop: 0.02 s; 7 blocks with $(…): refused as too many folders → allowed; over-cap non-straight line: minutes → 0.01 s refusal (scratchpad t1924.py and t1924c.py, fm task prove red 60 s timeout → green 0.5 s)
## Lessons
- Tails after a substitution were also the coarse catch for cd into a computed folder: drop them only when every mover on the line is a literal cd, and a cd is certain only in this shell and only after commands that only read
## Files touched
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py
- plugin/tests/test_guard_pipes.py
- CHANGELOG.md
