---
id: T-0369
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-08T23:55:43Z
updated: 2026-10-09T00:01:25Z
base: 4767a9bb8e1d079e1a19b9c5859c010866c52b24
base_tree: 87198d7b76de1e6cfa63295a700fdc7ebc7237d3
verified: strong
---
# Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false)
## Raw request
> Guard: pipe-shell blocks curl | python3 -c '<json-only code>' whenever any unrelated command shares the line (pkill, rm -f of a literal, sleep, NAME=…): _reads_pipe_as_data requires every command in the script to write nothing (fmguard.py:1245). Reproduced: 'pkill -f nothing; rm -f /tmp/a.log; curl -s U | python3 -c "import json,sys; json.load(sys.stdin)"' → exit 2, the pipe alone → 0. Check only the pipeline and earlier commands that can set env or plant modules; re-run the T-0344/T-0354 adversarial cases
## Interpretation
Real blocks (events.jsonl): music-fndr 2026-10-08 'pkill -f …; rm -f ../music-fndr-dev.log; L=/tmp/…; curl … | python3 -c …'. _writes_nothing (fmguard.py:1180) accepts only data tools with no redirect, so any inert neighbour, any >/dev/null and any assignment voids the T-0344 proof.
## Assumptions (confidence)
## Acceptance criteria
- [x] the curl | python3 -c proof stays as strict as T-0344/T-0354 left it: the adversarial neighbours (PYTHON*/LD_*/HOME/PATH, substitutions, file redirects, a planted module, an assignment that word-splits into curl flags) are blocked — verify with `python3 plugin/tests/run.py -k test_json_piped_into_proved_python_is_data`
## Non-goals
## Approach (options → choice → why)
(a) leave it: Claude splits the line (3 blocks in 2 days); (b) only look at commands before python — needs separator/background analysis the parser doesn't give reliably; (c) widen _writes_nothing narrowly: redirects only to /dev/null; pkill/kill/rm/which/ls/pwd/date/uname with no $ or backtick in their words (they can't create a file); assignment-only commands with literal values to names that aren't PYTHON*/LD_*/DYLD_*, HOME, PATH or already in the environment (an unexported shell variable never reaches python). Choice (c).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: friction shapes allowed, adversarial neighbours blocked
2. [x] full guard suite + fm replay corpus
## Resume here
## Docs impact
none: no behaviour change
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_json_piped_into_proved_python_is_data` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: FrictionFalseBlocks 0s) / OK [ran] [tree a1d1a0f64ff3] (2026-10-09T00:01:24Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 66 tests in 0.2s (21 classes, 16 at a time; slowest: PluginChanges 0s, Core 0s, InterpreterWrites 0s) / OK [ran] [tree a1d1a0f64ff3] (2026-10-09T00:01:24Z)
- (ac 1) `python3 plugin/tests/run.py -k test_json_piped_into_proved_python_is_data` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: FrictionFalseBlocks 0s) / OK [ran] [tree a1d1a0f64ff3] (2026-10-09T00:01:25Z)
- (audit adversary) `main thread: diff is test-only (fmguard.py identical to HEAD)` → the proposed widening was the risk; reverted, and its hole is now a test [tree a1d1a0f64ff3] (2026-10-09T00:01:25Z)
- (audit intent) `main thread: diff is test-only (fmguard.py identical to HEAD)` → friction source verified from the transcript before changing the guard [tree a1d1a0f64ff3] (2026-10-09T00:01:25Z)
## Log
- 2026-10-08T23:55:43Z created
- 2026-10-08T23:58:32Z planned from capture
- 2026-10-08T23:58:32Z set approved=True
- 2026-10-08T23:58:32Z focused
- 2026-10-09T00:01:23Z set title=Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false)
- 2026-10-09T00:01:23Z criterion 1 text: the friction lines (pkill …; rm -f …; L=…; curl | python3 -c json) pass, and planting, PYTHON*/LD_*/HOME/PATH assignments, substitutions and file redirects beside the pipe still block → the curl | python3 -c proof stays as strict as T-0344/T-0354 left it: the adversarial neighbours (PYTHON*/LD_*/HOME/PATH, substitutions, file redirects, a planted module, an assignment that word-splits into curl flags) are blocked
- 2026-10-09T00:01:24Z reverted the fmguard.py widening: assignments word-split into curl flags; the cited friction line was correctly blocked
- 2026-10-09T00:01:25Z done
- 2026-10-09T00:01:25Z committed e6687b7 (1 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-20261008: 1. **Answer.** I could ground one improvement fully (the pipe-shell false block) and one partly (state-direct from guessed variable targets).…
- research T-0344-review: Verdict: changes needed.** I had no shell, so these are traced by reading `plugin/lib/fmguard.py` and the tests. I did not run any command. [stal…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- decision 2026-10-04: Landscape 2026-10-04 grounded: no new work
- likely tests for the scope: plugin/tests/test_guard.py
## Regression test
none: no behaviour change. The finding's premise was false: the real blocked line (music-fndr 2026-10-08T02:08) started a background server, cd'd, used $(…) and $L, and POSTed with curl, so no sound widening lets it through; the widening I tried (inert tools, bare assignments) opened a hole (U='-o json.py URL'; curl -s $U | python3 -c …). The added cases pin the current, correct blocks.
## Lessons
- Before widening a guard from a friction digest, read the full blocked command: the digest's truncated line looked like a false positive and was a correct block
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
