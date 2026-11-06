# Brainstorm — lens: reliability

- **Cap Stop-hook nudges with a circuit breaker**: FIX: value 5, effort S, risk low
  Why: Stop nudges (evidence gate, question nudge) each force an extra model turn, and nothing in the pack limits repeats. Assumption: the counter isn't persisted today. Keep a per-task, per-reason count in `fm` state, allow at most one nudge per reason, then let the stop through with a one-line note in the task log.
  Done when: a test firing 5 consecutive Stop events with an unmet gate emits exactly 1 nudge per reason, then exit 0 with no block.

- **Key evidence to a tree fingerprint and reuse it**: PERFORMANCE: value 5, effort M, risk med
  Why: the full suite (~100 s) runs after every small change, and evidence can go stale after later edits. Record a hash of the changed files with each pass. `fm check` returns "PASS (cached @hash)" if the hash is unchanged, and `done` requires a pass on the final hash.
  Done when: a repeat `fm check` on an unchanged tree finishes in <1 s with no gate execution; after editing a tracked file it reruns; `done` refuses evidence from an older hash.

- **Fail-open hooks with atomic, locked state writes**: FIX: value 4, effort M, risk low
  Why: the constraints say state goes only through `fm`, and subagents and other plugins run concurrently. Assumption: writes aren't atomic today. Write via tmp file plus rename under a lock, and wrap every hook in try/except that logs to a size-capped file and exits 0.
  Done when: with a truncated `state.json`, every hook exits 0 in <100 ms and emits one warning line. Two parallel `fm` writers never lose an update in a 100-iteration stress test.

- **Add `fm doctor` with `--repair`**: FEATURE: value 4, effort M, risk low
  Why: the pack shows growing surfaces (rules budget ≤6k, another plugin injecting 5.7k chars, several hooks) and no way to detect drift. Doctor checks hook registration, state schema, stale active tasks, orphan locks, always-on rules size, and injected-context totals per session.
  Done when: seeded faults (missing hook, 7k rules, stale lock) each give a nonzero exit and a named finding; `--repair` clears the lock and stale task.

- **Lint verify commands when the brief is written**: FIX: value 4, effort S, risk low
  Why: criteria carry verify commands that only run at done. A typo'd or missing command costs a full turn later, and a flaky one is only caught by the rerun. Dry-run at `fm focus` (existence via `shutil.which`, syntax check, timeout declared) and warn immediately.
  Done when: a brief with a nonexistent verify binary produces a warning at focus time, not at done.

- **Skip repeat audits with a review verdict cache**: PERFORMANCE: value 5, effort M, risk med
  Why: reviews cost ~50–100k tokens each. Store the reviewer verdict, keyed by the tree fingerprint. If the tree is unchanged, reuse it. If the reviewer output is malformed, retry once with a shorter prompt instead of rerunning the full audit.
  Done when: a second audit on an unchanged fingerprint spawns 0 subagents; a malformed reviewer response triggers exactly 1 retry, then a recorded "review inconclusive".

- **Test the compaction-resume round trip**: FIX: value 3, effort M, risk low
  Why: resume after compaction is core, and SessionStart is capped at 2k chars, so truncation could drop the active step. Version the payload and put the active step, next action and last evidence hash first, so truncation drops the least important parts.
  Done when: a simulated compaction test restores the same task, step and next action within 2k chars, and an oversized state still keeps those three fields.
