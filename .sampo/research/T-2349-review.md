**Verdict: approve with nits.** I found no HIGH or CRITICAL defects. The untrusted-text and keying requirements hold. The replay is unbounded and runs in the failure hook, which is the main risk.

I had no shell. I couldn't run `git diff` or the tests, so I read the worktree at `~/.claude/foreman/.claude/worktrees/agent-aa3fa3fe724a4fd21` directly. The changes are in `fmrecall.py`, `fmdoctor.py`, `fmeco.py` and the tests. `fmhooks.py` has no T-2349 marker, so the hook error log is only read from `fm doctor`. I never saw the diff itself.

## lens: adversary
- No finding. Doctor and hook text go through `failure_signature` (which calls `c.redact`) and then `c.defang(c.plain(...))` before it enters a brief. `who` and `named` go through `c.plain`. The key is a hash plus a task id and is regex-escaped.

## lens: edge
- MEDIUM — `fmrecall.py:608-624` — `_replay` has no cap. It files a FIX for every signature with 3+ tasks, all in one PostToolUseFailure hook call. For example, if failures.jsonl holds 15 such signatures from the 494 rows, the inbox gets 15 FIXes at once. Fix: cap a replay at about 5, most tasks first, and leave the rest for the next call, with the marker written only when none remain. Confidence: medium. I don't know how many such signatures there are.
- MEDIUM — `fmdoctor.py:861-865` + `fmrecall.py:560-568` — A hook traceback counts as a new "run" per timestamp. Its `who` can be older than the close of the FIX it follows. A traceback logged after the last doctor run but before the FIX closed is first fed after the close, so it files a false "Fix did not hold". Fix: for `hook-run <ts>`, require the timestamp to be later than the cap brief's close time. Confidence: medium.
- LOW — `fmdoctor.py:861` — Three tracebacks of one bug within one session count as 3 runs. The test at `test_doctor.py:654` confirms a FIX is filed on the first feed. AC2 says "3+ tasks or sessions". Fix: dedupe `hook-run` to the session or the hour, or document the choice.
- LOW — `fmrecall.py:619-624` — The `finally` writes the marker even if `_recurring` raised partway, so the remaining signatures are never replayed. Fix: write the marker only when the loop finishes, or log the failure.
- LOW — `fmdoctor.py:859-866` and `:2458` — One exception inside `feed_self_failures` aborts the remaining feeds, and `cmd_doctor` swallows it silently. Fix: wrap each `note_own` call and log the error.

## lens: operator
- MEDIUM — `fmeco.py:30-33` — `capture_once` holds the `p.dir` lock while it loads about 3,500 briefs including the unindexed archive. The replay triggers this inside the failure hook, once per project. Other sessions' `note_failure` calls use `timeout=2` and silently drop their rows if it runs long. Fix: cap the replay as above, or run it from doctor rather than the hook.
- Cost multiplied out: each `fm doctor` makes at most about 30 `note_own` calls, each reading up to 1 MB under the lock. That is fine.
- `_any_brief` walks the archive on each first hit of a signature that already has a captured FIX. That is a listing plus a regex per file, roughly 10-30 ms per new task and signature.

## lens: maintainer
- LOW — `fmrecall.py:593` — `sig.startswith("fm: refused")` can never match a doctor or hook line, because those start with "fm doctor" or "hook". It only guards direct calls. The test passes only because `note_own` is called with a raw refusal. Fix: drop it or comment it.

## lens: intent
No findings.

## Acceptance criteria
1. Did-not-hold: met, per `test_recall.py:344-367`. It files once per closed fix, bound by `from`, and a dropped FIX is excluded.
2. Own failures: met. A doctor FAIL, a hook traceback and the SLO WARN all capture on the 3rd distinct run (`test_recall.py:378`, `test_doctor.py:649`). Refusals and tallies never capture (`test_recall.py:391`). See the burst-counting finding above.
3. Replay: met, per `test_recall.py:399`. It runs once, behind the marker. It is unbounded and runs in the hook, as flagged.

## Implicit decisions
- Own failures file with source "self" and are fed only from `fm doctor`, only inside Foreman's own repo.
- The unit for own failures is a session id (or the date), or a hook-run timestamp.
- A dropped or missing FIX leaves its signature permanently silent.

## Not checked
The test run, the exact diff, the CHANGELOG and MASTER docs, and the real hooks.log format.

**Noticed:** none
