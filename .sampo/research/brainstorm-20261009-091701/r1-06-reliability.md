# Brainstorm — lens: reliability

- **Fuzz the guard against real shells** — FEATURE — value 5 — effort L — risk med — category: guard
  Why: the guard keeps missing shell forms found by accident (`bash -lc`/`zsh -ic`, T-0414/0421/0422, open T-0275) and over-blocking others (symlink `rm`, `fm focus; sed`). Differential tests exist but are hand-written.
  Done when: `fm check` runs a grammar fuzzer for 60 s over bash, zsh and dash, comparing what each really executes with the guard's verdict, and fails on any write/exec the guard allowed. The corpus keeps every past miss.

- **Reject gates that can't fail** — FIX — value 5 — effort M — risk low — category: verification
  Why: a criterion's verify used `-k a or b`, which run.py ignores, so it ran no tests and passed. A checked criterion can't be edited, so it had to be recreated.
  Done when: `fm task done` refuses a verify that collected zero tests, or that also passes on the pre-change tree (no red→green), and names which. A test covers the `-k` case.

- **Chaos-test resume** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: "resumes at the exact step after /compact" is the headline promise, with no pack evidence of it being stress-tested. Band-stuck-on-step-1 (T-0406) shows state can drift.
  Done when: a harness kills or compacts a scripted session at every step boundary, resumes, and asserts the same step, brief and STATE; it runs in the e2e gate.

- **Prove a merge before it lands** — FEATURE — value 4 — effort M — risk med — category: lanes
  Why: `fm lane merge` refused a dirty main (T-0403), then was loosened to allow non-overlapping dirty files. Gates still run only on the lane, not on the merged result.
  Done when: merge first builds a throwaway worktree of main plus branch, runs the gates there, and lands only on green. A test shows two individually green lanes with a semantic conflict being refused.

- **Model-check the drive for idleness** — FEATURE — value 4 — effort M — risk low — category: drive
  Why: JARVIS idled with 20+ queued tasks (T-0401), then "long-lived jobs and an empty queue never leave a session idle". Each was patched case by case.
  Done when: a state-machine test enumerates queue, job, budget and blocked combinations and asserts every Stop-hook outcome is a concrete action or a stated wait reason (never silence). It fails on any state that yields neither.

- **Canary new Claude Code versions** — FEATURE — value 4 — effort M — risk low — category: compatibility
  Why: T-0316 (re-run a builder lane after a Claude Code update) and T-0336/T-0337 (adapters unverified live) are all blocked on "does it still work upstream".
  Done when: a scheduled `fm night` job installs the newest `claude` in a sandbox, runs a synthetic task round trip (hook schemas, guard, lane, resume) and writes pass/fail with the version to the ledger. A failure raises a blocker.

- **Check that a closed task did what it said** — FEATURE — value 5 — effort M — risk med — category: honesty
  Why: the user's steer is that cleanup requests (dead code, docs, replaced functionality) never got done. Done-gates check tests, not the brief's claims.
  Done when: for cleanup-type briefs, `fm task done` extracts the named targets and verifies by diff and grep that they were removed or updated (references to the old thing are gone). It refuses with the remaining hits.

- **Make state crash-safe, with a repair command** — FIX — value 3 — effort M — risk med — category: state
  Why: assumption: the ledger, briefs and STATE are plain files written by concurrent hooks, lanes and `fm run` sessions, so torn writes or lost updates are plausible. Nothing in the pack shows an fsck.
  Done when: writes are atomic with a lock, and `fm doctor --repair` rebuilds STATE from briefs plus the ledger. A test that kills a writer mid-write ends with a consistent state.

- **Fail-safe hooks with a watchdog** — FEATURE — value 3 — effort S — risk med — category: hooks
  Why: assumption: a crashed or slow hook can silently drop the guard. `bench_hooks.py` measures speed only.
  Done when: a guard hook that errors or times out fails closed (blocks, naming why), while drive and statusline hooks fail open. `fm doctor` shows hook error counts, and a test injects a crash in each hook.

- **Wild: self-healing guard patches** — FEATURE — value 4 — effort L — risk high — category: guard — wild
  Why: JARVIS hit the same false refusal twice before a human noticed. `fm friction` and `fm replay` already see these events.
  Done when: after two repeated false refusals, Foreman drafts a guard fix on a branch with a failing test for the false positive. It attaches a 5000-command replay showing no previously blocked command is now allowed, and queues it for approval.

- **Wild: canary ring across the user's own projects** — FEATURE — value 4 — effort M — risk med — category: release
  Why: each release (1.2.8 to 1.2.16) goes straight to GitHub main and JARVIS, where regressions then show up as complaints.
  Done when: a release first installs to one low-stakes project for N tasks, and auto-rolls back to the prior tag if friction, guard-block or replay metrics regress against baseline. Promotion is logged.

- **Wild: tamper-evident evidence ledger** — SECURITY — value 3 — effort M — risk low — category: evidence
  Why: "verifies with recorded evidence" is only as good as the record. The model could write evidence the commands never produced.
  Done when: evidence entries are hash-chained and store the command, exit code and output digest as captured by the PostToolUse hook, not by the model. `fm sentinel` flags any entry whose chain or command wasn't hook-captured.

- **Wild: blind twin run for risky tasks** — FEATURE — value 3 — effort L — risk med — category: verification — wild
  Why: `fm second` and `fm oracle` already give independent reads, but only of plans and reviews, not of outcomes.
  Done when: for an L-effort task, a second lane builds from the oracle's spec alone. The two diffs are compared by running the same behaviour examples, and any divergence is listed in the brief before commit.

- **Gate releases on clean-install and upgrade tests** — FEATURE — value 3 — effort M — risk low — category: release
  Why: 16 patch releases, and the installer handles Python 3.12.7+, Homebrew/uv and the manifest-based uninstall across Linux, macOS and WSL.
  Done when: a release check runs install, upgrade from the previous tag, and `uninstall-user` in a clean container, asserting `~/.claude` is byte-identical to before.
