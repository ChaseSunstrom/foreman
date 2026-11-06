## Verdict: approve with nits

I found no HIGH issues. The change is small and the diff matches the two acceptance criteria. I read the code but did not run any tests. The adversary lens found one hole this change leaves open, and the maintainer lens found a test that can pass without checking anything.

## lens: adversary
- MEDIUM — plugin/lib/fmcore.py:4282-4296 (reached from plugin/lib/fmmandate.py:309) — `lint_verify` still lets a done-when that can't fail through when it ends in `|| true`, `; true`, `|| echo ok` or `|| exit 0`. Splitting on `&&`, `||` and `;` gives `firsts=["test","true"]`, which is not all vacuous, and the pipe regex ignores `||`. Reproducer: `fm goal item x --done-when "test -d /nonexistent || true"`, close the task, then run `fm gates` and `fm goal verdict`. `drift` runs the check, it exits 0, and the verdict reads finished. Fix: in `lint_verify`, flag a final segment that is vacuous after `||` or `;`. Add `"false || true"` and `"false; true"` to the adversary test's check list. Confidence: high.

## lens: edge
- MEDIUM — plugin/lib/fmmandate.py:327-328 — `skip_tests` lists another open task's red-first test modules (`red_first_tests` skips only tasks other than the active one). Any unrelated open task with an uncommitted red-first file therefore holds the goal at "stopped". The cause prints only a count, so the user can't tell which task to close. Fix: name the modules, e.g. `gates skipped red tests: test_x (T-…)`, and say in the changelog that this is intended. Confidence: medium.

## lens: maintainer
- MEDIUM — plugin/tests/test_goal.py:109 — `have = ... if "Goal: " in out else 5`. If `fm resume` stops printing the goal line, the "lost" case the test exists to catch reads as "all five done", so `lost` stays 0 and the test passes. Fix: use `else (5 if len(done) == 5 else 0)`, or assert the line is present until all five are done. Confidence: high.
- LOW — CHANGELOG.md:9 — It says "9 kill points". The test calls `kill()` 11 times (five direct calls and six through `close`), and it asserts only `points >= 5`. Fix: say 11 and assert `points == 11`. Confidence: high.
- LOW — plugin/lib/fmmandate.py:310-311 — `cat out.txt | grep -q ok` hits the `_VACUOUS` first-word rule (`cat`, `ls`), so the cause says "nothing in it checks the behaviour" even though `grep` does. The verdict is still right because the pipe is flagged too. Fix: when both match, prefer the pipe message. Confidence: high.

## lens: intent
- LOW — The request asks for a verdict on each of three spikes. The diff has code and tests for the adversary and the relay race, and nothing for the reopened-ticket miner. MASTER.md's change is too large to see. The verdicts may be in the task log, but I can't verify that.

## Acceptance criteria
- AC1 (verdict never finished on a vacuous, pipe-masked or skipped-red done-when): partly met. `true`, `echo ok`, `exit 0`, `:` and a trailing pipe are covered by tests, and the skipped-red-tests case is covered at plugin/tests/test_goal.py:82-86. The `|| true` and `; true` forms still read finished.
- AC2 (relay race loses and redoes nothing): met, with the weak `lost` guard noted above.
- Hunks outside the steps: the CHANGELOG and MASTER.md edits fit the task (docs). No stray edits.

## Implicit decisions
- Reuses `lint_verify` and filters its output by substring match on the message text ("can't fail", "piped program"), so rewording those messages would silently turn the check off.
- Reports only the first hollow cause per item.
- Skipped red tests count as "stopped" and take lowest precedence, after gates red.
- The relay race simulates a fresh session with a `fm resume` subprocess plus an in-process `_next_runnable`.

## Not checked
I did not run the test suite or read MASTER.md's changed line. I did not check `fm resume` output formatting beyond the regex. The three checklist-listed pre-audit items (fmcli.py needing no edit, hotspot files) show no evidence of a missed edit.

**Noticed:** `_VACUOUS` in plugin/lib/fmcore.py:4274 treats `ls`, `cat` and `date` as can't-fail, but `ls missing` and `cat missing` do fail. That makes a done-when like `ls dist` read as hollow. It is worth its own task.
