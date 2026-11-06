---
id: T-1930
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T07:15:22Z
updated: 2026-10-29T07:29:22Z
base: acf3807c0c205e4c536d2d43753dc708c1f084fd
base_tree: 5ef27458d931e645941781a1e66035565da3abb0
plan0_at: 2026-10-29T07:24:50Z
plan0_scope: []
verified: strong
---
# Guard judges repeated unfollowable cds with $(…) bodies in under a second
## Raw request
> Guard: (true); cd dN; cd xN; repeated 4 times then echo with 10 $(ls j) bodies takes 17 s to judge (2 blocks x 40 bodies: 1.9 s); the nested per-folder judging multiplies; the hook can time out
## Interpretation
The guard's guess for a relative write target after an unfollowable cd pairs every word of the line (resolved in every folder the shell may be in) with every lost cd target and stats each pair: 4352 words x 255 lost = 1.1M isdir calls per call, 3.3M per check, 8-17 s. The hook can time out. Verdicts must stay identical: never weaken the guard.
## Assumptions (confidence)
## Acceptance criteria
- [x] lines of 4 (true); cd dN; cd xN; blocks with 2 or 10 $(ls j) bodies are judged in under 2 s with the same verdicts — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
Chosen: test each resolved word with isdir once, and pair only existing folders with lost targets. On Linux w/x is a folder only if w is one (each path part must be a folder), and lost targets are always relative (_moved joins relative parts), so the guesses are identical; the filter is skipped if a lost target were ever absolute. Rejected: a module-level isdir cache (stale across checks in long-lived processes); a cap that refuses (changes verdicts); deduping (w,x) joins (only 6% duplicates).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test-first: timing + verdict assertions for the 4x2 and 4x10 lines; prefilter words by isdir in _target_cats; measure before/after
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_guard.TokenFallback` → ✗ exit 1 · Ran 11 tests in 38.7s (1 classes, 16 at a time; slowest: TokenFallback 38s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ca6eed18020f] (2026-10-29T07:27:30Z)
- `python3 plugin/tests/run.py test_guard.TokenFallback` → exit 0 · Ran 11 tests in 1.6s (1 classes, 16 at a time; slowest: TokenFallback 1s) / OK [ran] [tree ca6eed18020f] (2026-10-29T07:27:30Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 298 tests in 8.2s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 3fefd3eb870e] (2026-10-29T07:28:40Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 298 tests in 8.1s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 20a4d0e0748d] (2026-10-29T07:29:10Z)
- (audit adversary) `one fm-reviewer pass (adversary focus on verdict identity): approve, no way found to change a guess; 1 low finding fixed (per-line 2 s bound); 504 guard and hook tests green; prove red 38.7 s / green 1.6 s` → isdir(w/x) needs w to be a folder for relative x (file, dangling link, .., empty x all checked); lost entries are always relative, and the filter switches off if one is not [tree 20a4d0e0748d] (2026-10-29T07:29:10Z)
- (audit edge) `one fm-reviewer pass (adversary focus on verdict identity): approve, no way found to change a guess; 1 low finding fixed (per-line 2 s bound); 504 guard and hook tests green; prove red 38.7 s / green 1.6 s` → symlinked folders pass both checks; over-long or NUL paths only keep more words [tree 20a4d0e0748d] (2026-10-29T07:29:10Z)
- (audit intent) `one fm-reviewer pass (adversary focus on verdict identity): approve, no way found to change a guess; 1 low finding fixed (per-line 2 s bound); 504 guard and hook tests green; prove red 38.7 s / green 1.6 s` → verdicts identical, check_bash call counts unchanged (50, 606) [tree 20a4d0e0748d] (2026-10-29T07:29:10Z)
- (audit operator) `one fm-reviewer pass (adversary focus on verdict identity): approve, no way found to change a guess; 1 low finding fixed (per-line 2 s bound); 504 guard and hook tests green; prove red 38.7 s / green 1.6 s` → the hook no longer risks a timeout on these lines (7-17 s to under 0.4 s) [tree 20a4d0e0748d] (2026-10-29T07:29:10Z)
- (audit maintainer) `one fm-reviewer pass (adversary focus on verdict identity): approve, no way found to change a guess; 1 low finding fixed (per-line 2 s bound); 504 guard and hook tests green; prove red 38.7 s / green 1.6 s` → two lines with a comment naming why; no cache, no new state [tree 20a4d0e0748d] (2026-10-29T07:29:10Z)
## Log
- 2026-10-29T07:15:22Z created
- 2026-10-29T07:24:39Z planned from capture
- 2026-10-29T07:24:50Z focused
- 2026-10-29T07:27:42Z measured: 6.93s->0.09s (4x2), 10.39s->0.36s (4x10)
- 2026-10-29T07:29:21Z done
- 2026-10-29T07:29:22Z committed e2c9a552 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1924 [PERFORMANCE M, done, 1 steps] Guard: repeated 'cd X; …; cd ..' in a ; line grows its folder sets exponentially (_moved/_ — lesson: Tails after a substitution wer…
- research T-1924-review: Verdict: changes needed.** One adversary finding is real and new. The relative-`cd` change lets a line pass that was refused before. I ran nothin…
- T-1921 [FIX M, done, 3 steps] Guard reads a substitution behind 'cd /abs &&' from the starting folder too — lesson: When the guard trusts a cd folder, check the parsed a…
- decision 2026-10-23: T-1536: leave out the blind multi-runner taste panel
- similar finished tasks took 1–3 steps
## Measurements
Before: 4 unfollowable cd blocks then echo $(ls 0) $(ls 1); tar xf - = 6.9-8.1 s (3.3M stats); with ten $(ls j) = 10.4-17 s. After: 0.09 s and 0.36 s, same verdicts, same check_bash call counts (50, 606). TokenFallback class 37.7 s -> 1.7 s.
## Lessons
- Before a nested product of stats, filter each factor by the cheap check the product implies (a path part must be a folder)
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
