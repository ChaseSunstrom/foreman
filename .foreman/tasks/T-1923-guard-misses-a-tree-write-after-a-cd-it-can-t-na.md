---
id: T-1923
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T06:13:43Z
updated: 2026-10-29T07:50:08Z
base: e2c9a55240be0b40478cee8beaf2b747a97479c1
base_tree: 20a4d0e0748df269da3f4b6be4f2ce187e3b7b4e
plan0_at: 2026-10-29T07:30:38Z
plan0_scope: []
verified: strong
---
# Guard judges tree writes after a cd to a folder it can't name
## Raw request
> SECURITY: guard misses a tree write after a cd it can't name: from scratch, cd $X && git reset --hard, $C <foreman> && git reset --hard, and export CDPATH=<foreman>; cd plugin && sh -c 'rm -rf lib' all pass (unknown-folder guesses use only the read text's words; a computed command word is never taken as a cd)
## Interpretation
A cd whose target the guard can't name (an unset or computed name, a substitution) is treated as landing only below folders the line names, so a following tree write (git reset --hard, rm -rf, tar xf) is judged nowhere. But bash may stay put (cd "" and a substitution printing nothing), go home (an unquoted empty word), or run a computed command word that is cd; and a nested sh -c inherits the CDPATH place. Each such place must be judged; never weaken the guard.
## Assumptions (confidence)
## Acceptance criteria
- [x] cd "$X"/cd $(…) staying put, cd $X going home, a computed command word that may be cd, and a nested sh -c after a CDPATH cd are judged in every place the shell may be; common safe lines still pass — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
Options: (1) refuse every tree write after an unnamed cd (broad, blocks cd $(git rev-parse --show-toplevel) && git checkout); (2) add the places bash can provably reach: the folders it was in (stay put) and home (unquoted empty), plus treat a computed command word as a possible cd of its first argument; (3) re-read the line once per possible place. Chosen: (2), narrow and principled; captures the rest. Probe first: the exact shapes decide where the fix lives.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Probe each shape; test-first table of refused and allowed lines; fix in _moved / the cd handling / nested checks; adversarial cases
## Resume here
<!-- auto -->
- 2026-10-29T07:40:11Z step 1/1: Probe each shape; test-first table of refused and allowed lines; fix in _moved / the cd handling / nested checks; adversarial cases
- git: foreman/build; 2 uncommitted: plugin/lib/fmguard.py, plugin/tests/test_guard.py
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1923c.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1923d.py, plugin/lib/fmguard.py, plugin/tests/test_guard.py
- failures met: python0: can't open file 't0b.py': [errno 0] no such file or directory
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_guard 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK|FAILED)|arg=" | head -30` → ✗ exit 1 · Ran 299 tests in 10.6s (88 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 8s, Trust 7s) / FAILED (1 classes) [ran] [tree 26cd998f5f66] (2026-10-29T07:36:06Z)
- (ac 1) `python3 plugin/tests/run.py test_guard 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|Ran|OK|FAILED)|arg=" | head -30` → ✗ exit 1 · Ran 299 tests in 11.4s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 10s, Trust 7s) / FAILED (1 classes) [ran] [tree f4808ca3388a] (2026-10-29T07:37:02Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 299 tests in 8.7s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 5d462d2c2267] (2026-10-29T07:42:09Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 299 tests in 11.9s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 9s, Trust 7s) / FAILED (1 classes) [ran] [tree 5672f564f40a] (2026-10-29T07:48:07Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 299 tests in 8.7s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 5672f564f40a] (2026-10-29T07:49:40Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 299 tests in 8.7s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 5672f564f40a] (2026-10-29T07:49:56Z)
- (audit intent) `one fm-reviewer pass (T-1923-review): 2 confirmed (colon CDPATH list, dead computed-word branches) and 2 more fixed, 3 probed as already refused; guard+hook set 506 OK; fm replay --candidate HEAD on 5000 real commands: 0 tightened, 0 loosened; 124 labelled cases, 0 drifted` → cd "$X" stays put, cd $X goes home, computed cd words and CDPATH nested text judged in each landing folder [tree 5672f564f40a] (2026-10-29T07:49:56Z)
- (audit adversary) `one fm-reviewer pass (T-1923-review): 2 confirmed (colon CDPATH list, dead computed-word branches) and 2 more fixed, 3 probed as already refused; guard+hook set 506 OK; fm replay --candidate HEAD on 5000 real commands: 0 tightened, 0 loosened; 124 labelled cases, 0 drifted` → colon CDPATH, $C -P, C=; $C cd, $(echo cd), C="cd D"; $C all refused over Foreman [tree 5672f564f40a] (2026-10-29T07:49:56Z)
- (audit edge) `one fm-reviewer pass (T-1923-review): 2 confirmed (colon CDPATH list, dead computed-word branches) and 2 more fixed, 3 probed as already refused; guard+hook set 506 OK; fm replay --candidate HEAD on 5000 real commands: 0 tightened, 0 loosened; 124 labelled cases, 0 drifted` → raw/cmds misalignment drops quoting info; unset names in a bare cd [tree 5672f564f40a] (2026-10-29T07:49:56Z)
- (audit operator) `one fm-reviewer pass (T-1923-review): 2 confirmed (colon CDPATH list, dead computed-word branches) and 2 more fixed, 3 probed as already refused; guard+hook set 506 OK; fm replay --candidate HEAD on 5000 real commands: 0 tightened, 0 loosened; 124 labelled cases, 0 drifted` → no timing change; 5000 real commands same verdicts [tree 5672f564f40a] (2026-10-29T07:49:56Z)
- (audit maintainer) `one fm-reviewer pass (T-1923-review): 2 confirmed (colon CDPATH list, dead computed-word branches) and 2 more fixed, 3 probed as already refused; guard+hook set 506 OK; fm replay --candidate HEAD on 5000 real commands: 0 tightened, 0 loosened; 124 labelled cases, 0 drifted` → dead bare arms removed; one maybe rule for computed words [tree 5672f564f40a] (2026-10-29T07:49:56Z)
## Log
- 2026-10-29T06:13:43Z created
- 2026-10-29T07:30:37Z planned from capture
- 2026-10-29T07:30:38Z focused
- 2026-10-29T07:37:14Z hypothesis: the T-1930 line now refuses over home because a computed command word with no args (a substitution tail reading) adds an unsure cd home; and cd $X; rm -rf build passes because rm judges the single cwd, not cwds
- 2026-10-29T07:47:12Z hypothesis: review — CDPATH words keep ':' so a colon list never resolves (probe: None, confirmed); bare is None for computed command words so the _only_unset arms in the computed-word path are dead and $X cd /tmp from scratch is refused anywhere; cd $(true), $C -P, cd "$(echo D)" && rm already refused (probe)
- 2026-10-29T07:50:07Z done
- 2026-10-29T07:50:08Z committed 7f915dd4 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1921 [FIX M, done, 3 steps] Guard reads a substitution behind 'cd /abs &&' from the starting folder too — lesson: When the guard trusts a cd folder, check the parsed a…
- T-1924 [PERFORMANCE M, done, 1 steps] Guard: repeated 'cd X; …; cd ..' in a ; line grows its folder sets exponentially (_moved/_ — lesson: Tails after a substitution wer…
- research T-0411-review: Verdict: changes needed.** I found three bypasses in `_expand_literal_loops`. I could not run bash (read-only), so each one is traced from the co…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
## Lessons
- bare is None whenever a command word is computed: branches gated on _only_unset there never run; probe each arm before trusting a passing table
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
