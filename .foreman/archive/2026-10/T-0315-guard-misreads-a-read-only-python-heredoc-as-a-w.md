---
id: T-0315
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-05T18:04:11Z
updated: 2026-10-06T03:18:38Z
base: 2e4d0eb9abedd14f9c2b75b748fa94405d4e0506
base_tree: 9b55d112e249af490281267553172a6ae04d5700
verified: strong
---
# Guard: a read-only python heredoc with ' | '.join(...) isn't a write
## Raw request
> Guard misreads a read-only python heredoc as a write: "' | '.join((x.get(" taken as a written path (brief category, T-0308); repro: python3 - <<'EOF' with json.loads/open(sys.argv[1]) read-only and a ' | '.join(...) line
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] python3 - <<'EOF' that only reads (json.load(open(sys.argv[1])), print(' | '.join(...))) passes in a project with no task, and an open(p, 'w') in one is still a write — verify with `python3 plugin/tests/run.py -k test_guard.InterpreterReads`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] fix the interpreter write scan
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guard.InterpreterReads` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterReads 0s) / FAILED (1 classes) [ran] [tree 9a5abbd73df9] (2026-10-06T03:16:12Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard.InterpreterReads` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterReads 0s) / OK [ran] [tree e765e0f5aa13] (2026-10-06T03:17:23Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 66 tests in 2.1s (22 classes, 16 at a time; slowest: GuardAgainstBash 2s, InterpreterWrites 0s, GitChannels 0s) / OK [ran] [tree e765e0f5aa13] (2026-10-06T03:17:25Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guard.InterpreterReads` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterReads 0s) / OK [ran] [tree e765e0f5aa13] (2026-10-06T03:18:37Z)
- (audit adversary) `self + adversary review: only the starter line pattern widened; the code is still proved by _open_targets (AST, pure modules, literal write targets); script args reach sys.argv only; a prefix is lowercase name=literal (no PATH/HOME/LD_*/PYTHON*: the PYTHON check stays), anything else falls back to the coarse rule; replay 0 newly allowed` → HOME=/x before the heredoc keeps the coarse rule (python's user site would run usercustomize.py); redirects, pipes, ; inside args still unproved [tree e765e0f5aa13] (2026-10-06T03:18:37Z)
- (audit self) `self + adversary review: only the starter line pattern widened; the code is still proved by _open_targets (AST, pure modules, literal write targets); script args reach sys.argv only; a prefix is lowercase name=literal (no PATH/HOME/LD_*/PYTHON*: the PYTHON check stays), anything else falls back to the coarse rule; replay 0 newly allowed` → no findings [tree e765e0f5aa13] (2026-10-06T03:18:37Z)
## Log
- 2026-10-05T18:04:11Z created
- 2026-10-06T03:15:48Z planned from capture
- 2026-10-06T03:15:49Z focused
- 2026-10-06T03:18:38Z done
- 2026-10-06T03:18:38Z committed 167b4be (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0286-review-1: Changes needed. I found no new hole that the `cd` prefix itself opens. The `cd` chain does make four existing parse mismatches reachable from a…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were L: consider --tier L
- the similar finished task took 3 steps
## Lessons
- A prover that only accepts the textbook form pushes every real-world variant to the coarse rule; widen the form, never the proof.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
