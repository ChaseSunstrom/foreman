---
id: T-0421
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: [T-0414]
source: discovered
created: 2026-10-09T13:57:52Z
updated: 2026-10-09T14:08:35Z
base: d4d8dff8eb7dd3d568ca29a0dc77147558a72c98
base_tree: 2af4f0b169da816597ea73ee5b2858fbc0e7a143
verified: strong
---
# Guard: any download on the line counts when a shell reads a pipe
## Raw request
> SECURITY: pipe-shell misses downloads fed through a substitution or a subshell (T-0414 builder): curl … $(true) | bash, curl … |(bash), diff <((curl … | bash)) — the check that a fetcher feeds the pipe doesn't see them; downloaded code runs unchecked
## Interpretation
pipe-shell asks whether a fetcher is in the piped shell's own chain, built in command order from _split; a $(…) or a ( ) group splits into commands of its own that reset or break the chain, so curl … $(true) | bash, curl … |(bash) and diff <((curl … | bash)) run downloaded code unchecked (T-0414 builder).
## Assumptions (confidence)
## Acceptance criteria
- [x] the three forms and curl -o f URL; cat f | bash refuse as pipe-shell; curl … | jq and the T-0344/T-0414 data-python forms still pass; real bash rows agree — verify with `python3 plugin/tests/run.py -k test_any_download_feeding_a_shell`
## Non-goals
## Approach (options → choice → why)
(A, chosen) the lazy, wider rule: a shell (or source/.) that reads a pipe or a <( ) is pipe-shell when ANY command on the line is a fetcher, unless _reads_pipe_as_data proves the data-only python case; a downloaded file later piped to bash is caught too. (B, rejected) fix chain tracking through substitutions and groups: every new shell form reopens it. Cost of A: 'curl …; echo x | bash' is refused, a rare form that pipes into a shell anyway.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: unit + real-bash rows
2. [x] widen the fetcher test to the whole line
3. [x] replay, gate, ship
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_any_download_feeding_a_shell` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: AnyDownload 0s) / FAILED (1 classes) [ran] [tree cfbbea4b5c2a] (2026-10-09T13:59:10Z)
- (step 2) `python3 plugin/tests/run.py -k test_any_download_feeding_a_shell` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: AnyDownload 0s) / OK [ran] [tree 661006ac7dd9] (2026-10-09T14:04:53Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 14:06 UTC) [ran] [tree 80129685eaba] (2026-10-09T14:08:15Z)
- (ac 1) `python3 plugin/tests/run.py -k test_any_download_feeding_a_shell` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: AnyDownload 0s) / OK [ran] [tree 80129685eaba] (2026-10-09T14:08:30Z)
- (audit adversary) `red→green unit rows + real-bash EXTRA rows; full gate exit 0 with replay 0 newly allowed; committed with T-0414 (4328aa2, shared fmguard.py)` → the reported forms refuse in unit and real-bash rows; the data-python and jq forms still pass [tree 80129685eaba] (2026-10-09T14:08:30Z)
- (audit edge) `red→green unit rows + real-bash EXTRA rows; full gate exit 0 with replay 0 newly allowed; committed with T-0414 (4328aa2, shared fmguard.py)` → conservative by design (a fetcher anywhere / any brace word) — a rare false refusal over a silent pass [tree 80129685eaba] (2026-10-09T14:08:30Z)
- (audit intent) `red→green unit rows + real-bash EXTRA rows; full gate exit 0 with replay 0 newly allowed; committed with T-0414 (4328aa2, shared fmguard.py)` → closes the hole the T-0414 builder reported, nothing wider [tree 80129685eaba] (2026-10-09T14:08:35Z)
- (audit adversary) `red→green unit rows + real-bash EXTRA rows; full gate exit 0 with replay 0 newly allowed; committed with T-0414 (4328aa2, shared fmguard.py)` → the reported forms refuse in unit and real-bash rows; the data-python and jq forms still pass [tree 80129685eaba] (2026-10-09T14:08:35Z)
- (audit edge) `red→green unit rows + real-bash EXTRA rows; full gate exit 0 with replay 0 newly allowed; committed with T-0414 (4328aa2, shared fmguard.py)` → conservative by design (a fetcher anywhere / any brace word): a rare false refusal over a silent pass [tree 80129685eaba] (2026-10-09T14:08:35Z)
## Log
- 2026-10-09T13:57:52Z created
- 2026-10-09T13:58:32Z planned from capture
- 2026-10-09T13:58:52Z focused
- 2026-10-09T13:59:17Z set depends_on=['T-0414']
- 2026-10-09T13:59:17Z waits on T-0414's merge: both change the pipe-shell call site and _reads_pipe_as_data; its builder branch is under adversary review
- 2026-10-09T14:00:59Z paused: focus moved to T-0426
- 2026-10-09T14:04:13Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-09T14:04:13Z focused
- 2026-10-09T14:04:53Z paused: focus moved to T-0422
- 2026-10-09T14:08:29Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-09T14:08:29Z focused
- 2026-10-09T14:08:30Z paused: focus moved to T-0422
- 2026-10-09T14:08:34Z focused
- 2026-10-09T14:08:35Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0384-review: Changes needed.** I found four concrete bypasses by reading the code. I could not run bash or the tests, because I only had read tools. For each …
- research T-0286-review-1: Changes needed. I found no new hole that the `cd` prefix itself opens. The `cd` chain does make four existing parse mismatches reachable from a…
- T-0414 [FIX M, active, 3 steps] Guard: a data-reading python -c is judged by what runs before it
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
## Lessons
- Check the property (a download reaches a shell; a word may expand) rather than the shape of one line.
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/lib/fmguard.py
