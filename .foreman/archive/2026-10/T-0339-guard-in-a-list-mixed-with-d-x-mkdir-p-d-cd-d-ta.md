---
id: T-0339
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-06T02:48:59Z
updated: 2026-10-06T03:10:04Z
base: 06726bb71de3d18a4a5b50c0df8966ab9b597a58
base_tree: 65893c4f794699dc69f1e1297797f8162794acd9
verified: strong
---
# Guard: a cd inside an && segment of a ; list is certain for the rest of that segment
## Raw request
> Guard: in a ; list mixed with && (D=~/x; mkdir -p $D && cd $D && tar xf -) a cd inside an && segment isn't taken as certain, so the tar is guessed onto the old cwd (core block); treat each && segment of a ; list as its own and-chain
## Interpretation
False core block from friction: the guard can't see that in 'A; B && cd D && T' the T runs only in D. Make the && segment's cd certain within it, without trusting anything an && may have skipped.
## Assumptions (confidence)
## Acceptance criteria
- [x] D=~/x; mkdir -p $D && cd $D && tar xf - run from the Foreman checkout isn't a core block, while a cd an && may skip (false && cd /x; rm -rf y) leaves later commands judged in the old folder too — verify with `python3 plugin/tests/run.py -k test_guard`
- [x] no new verdicts on 5000 real commands but intended ones — verify with `fm replay`
## Non-goals
## Approach (options → choice → why)
(A) In check_bash's loop, know each command's separator (Cmd.op): in a ; list mixed with &&, a cd joined by && to what follows is certain for the rest of its segment; at the segment's end the folders before it are merged back (the chain may have stopped early), and mkdir -p targets made inside it are forgotten. (B) Check each ;-segment as its own command — loses variables and folders flowing across segments. Choice A: smallest change, keeps cross-segment state.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] per-segment chain in check_bash
3. [x] replay + review
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guard.KnownVars` → ✗ exit 1 · Ran 4 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) [ran] [tree cd734a3e8216] (2026-10-06T03:02:59Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 64 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree 78418471c854] (2026-10-06T03:04:36Z)
- (step 3) `python3 plugin/tests/run.py -k test_guard.KnownVars` → ✗ exit 1 · Ran 4 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) [ran] [tree 936f33c3a694] (2026-10-06T03:06:46Z)
- (step 3) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 64 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree aa9d7026692c] (2026-10-06T03:09:41Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 64 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree aa9d7026692c] (2026-10-06T03:09:47Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 64 tests in 1.3s (20 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree aa9d7026692c] (2026-10-06T03:09:58Z)
- (ac 2) `fm replay` → exit 0 · 0 newly allowed (possible bypasses) / 52 new to the corpus [ran] [tree aa9d7026692c] (2026-10-06T03:09:58Z)
- (audit intent) `one fm-reviewer pass (intent + adversary, research T-0339-review): 1 HIGH regression (a chain stopping mid-way left the shell in a dropped middle folder) fixed test-first; replay 0 new verdicts; bash differential test with 4 new forms green` → the friction command (D=~/x; mkdir -p $D && cd $D && tar xf -) passes; skipped cds and mkdirs still leave the old folder possible [tree aa9d7026692c] (2026-10-06T03:09:58Z)
- (audit adversary) `one fm-reviewer pass (intent + adversary, research T-0339-review): 1 HIGH regression (a chain stopping mid-way left the shell in a dropped middle folder) fixed test-first; replay 0 new verdicts; bash differential test with 4 new forms green` → every folder an && segment reaches stays possible after it (cd FH && cd /nonexistent; tar → core); ||, !, pipes, subshells keep mixed off; dropped Cmds only make it more conservative [tree aa9d7026692c] (2026-10-06T03:09:58Z)
- (step 3) `python3 plugin/tests/run.py -k test_guard.KnownVars` → exit 0 · Ran 4 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree aa9d7026692c] (2026-10-06T03:10:03Z)
- (audit intent) `one fm-reviewer pass (intent + adversary, research T-0339-review): 1 HIGH regression (a chain stopping mid-way left the shell in a dropped middle folder) fixed test-first; replay 0 new verdicts; bash differential test with 4 new forms green` → the friction command (D=~/x; mkdir -p $D && cd $D && tar xf -) passes; skipped cds and mkdirs still leave the old folder possible [tree aa9d7026692c] (2026-10-06T03:10:03Z)
- (audit adversary) `one fm-reviewer pass (intent + adversary, research T-0339-review): 1 HIGH regression (a chain stopping mid-way left the shell in a dropped middle folder) fixed test-first; replay 0 new verdicts; bash differential test with 4 new forms green` → every folder an && segment reaches stays possible after it (cd FH && cd /nonexistent; tar → core); ||, !, pipes, subshells keep mixed off; dropped Cmds only make it more conservative [tree aa9d7026692c] (2026-10-06T03:10:03Z)
## Log
- 2026-10-06T02:48:59Z created
- 2026-10-06T03:02:51Z planned from capture
- 2026-10-06T03:02:54Z focused
- 2026-10-06T03:10:03Z done
- 2026-10-06T03:10:04Z committed dcba63a (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261006: 1. **Answer.** Four of the five friction points trace to small, local causes. The guard leaves a variable unknown when its value starts with `~`. …
- T-0338 [FIX M, done, 7 steps] Batch: Guard: D=~/x; mkdir -p $D && cd $D leav…; Guard: _prefix_vars counts every bare w…; Fm session/claude send: opti… — lesson: Making a…
- research T-0338-review: Changes needed. I could not run anything (no execution tool), so each finding comes from tracing the code by hand. The two HIGH findings are bypa…
- T-0190 [FIX M, done, 3 steps] Guard: guesses never use a variable's own name; rm targets use literals set once before a branch — lesson: A replay gate turns a guard chan…
## Lessons
- When a model replaces a set with its newest value inside a chain, a chain that can stop at any link must keep the union of every value it passed through, not just its start and end.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/test_guard_diff.py
- CHANGELOG.md
