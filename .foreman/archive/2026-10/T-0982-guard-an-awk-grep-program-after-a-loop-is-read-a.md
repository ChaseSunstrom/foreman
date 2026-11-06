---
id: T-0982
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T22:26:16Z
updated: 2026-10-15T22:30:46Z
base: d585092d322ce00d4468ad191a7248ce89ebb896
base_tree: 889d47aabefeb5fc64f0a2ee60467a52022f20cd
verified: strong
---
# Guard: an awk/grep program after a "$(…)" loop is read as 'a program read from a pipe' (4
## Raw request
> Guard: an awk/grep program after a "$(…)" loop is read as 'a program read from a pipe' (4 blocks): the quote-blind fallback split (fmguard _tokens ~799) makes $1<1200' a command; skip the pipe-program finding for fallback-split names, keeping curl | python3 blocked
## Interpretation
An awk or grep program after a "$(…)" loop (for f in …; do echo "$(wc -c <$f) $f"; done | awk '$1>4000') was refused as 'a program read from a pipe' 4 times this week: the read-to-the-end tail of the substitution has an odd quote, the quote-blind fallback split makes $1<1200' a command name, and that name is piped.
## Assumptions (confidence)
## Acceptance criteria
- [x] The two loop forms the friction digest quotes pass the guard, while curl … | python3, echo 'rm -rf ~' | bash and | $SH still block — verify with `python3 plugin/tests/run.py -k PipeProgramDebris`
## Non-goals
## Approach (options → choice → why)
Options: skip the pipe-program finding for a 'name' holding a quote or redirect character, which no real program name has (chosen: the smallest change, real | python3 and | $SH still refused); return a fallback flag from _tokens (touches every caller); drop the tails reading (loses fail-closed coverage).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing PipeProgramDebris test
2. [x] Skip debris names in the pipe-program check
## Resume here
## Docs impact
none: guard internals
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k PipeProgramDebris` → ✗ exit 1 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: PipeProgramDebris 0s) / FAILED (1 classes) [ran] [tree 855bb744f891] (2026-10-15T22:29:39Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_git test_guard_pipes test_guard_debris` → exit 0 · Ran 106 tests in 7.9s (45 classes, 16 at a time; slowest: GuardAgainstBash 8s, Hook 3s, RuleIds 1s) / OK [ran] [tree 22993d0ca23e] (2026-10-15T22:30:44Z)
- (ac 1) `python3 plugin/tests/run.py -k PipeProgramDebris` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: PipeProgramDebris 0s) / OK [ran] [tree 22993d0ca23e] (2026-10-15T22:30:45Z)
- (step 1) `python3 plugin/tests/run.py -k PipeProgramDebris` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: PipeProgramDebris 0s) / OK [ran] [tree 22993d0ca23e] (2026-10-15T22:30:45Z)
- (audit self) `self: red then green; every guard suite passes` → loop output piped to awk/grep passes; real pipe programs still refused [tree 22993d0ca23e] (2026-10-15T22:30:45Z)
- (audit adversary) `self: red then green; every guard suite passes` → the skip applies only inside substitution readings (depth > 0), never to the top-level command, which shlex reads whole; | python3, echo 'rm -rf ~' | bash, | $SH and a $( ) loop piped to python3 still block [tree 22993d0ca23e] (2026-10-15T22:30:45Z)
## Log
- 2026-10-15T22:26:16Z created
- 2026-10-15T22:29:31Z focused
- 2026-10-15T22:30:45Z done
- 2026-10-15T22:30:46Z committed 111e539 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0414 [FIX M, done, 3 steps] Guard: a data-reading python -c is judged by what runs before it — lesson: A parser that drops quoting can't be trusted about structure the…
- T-0940 [FIX M, done, 6 steps] Guard false blocks from the friction pass: cd; heredoc message, reset --soft, plugin update message, git fetch — lesson: Friction digests p…
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- decision 2026-10-15: Round 5 slate: 7 builds from 54 grounded ideas (snapshot before discarding commands, risk-ranked review, claims audit, keep-going stall count, night…
## Plan gaps
- failed first: step 1 Failing PipeProgramDebris test
## Files touched
- plugin/tests/test_guard_debris.py
- plugin/lib/fmguard.py
