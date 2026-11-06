# Brainstorm — lens: reliability

- **Fail finish on a silently crashed hook** — FIX — value 4 — effort S — risk low — category: hooks
  Why: p95 278 ms over 13533 runs is measured, but nothing in the pack says a hook that crashed (not slow, crashed) is visible. A crashed guard hook that fails open is the worst reliability bug in a "stay safe" capability. assumption: hook crashes aren't yet counted per task.
  Done when: a test kills the guard hook mid-task (nonzero exit, no verdict) and `fm task finish` refuses, naming the hook and the exit code.

- **Table every hook's failure mode, tested by crashing it** — FEATURE — value 5 — effort M — risk med — category: guard
  Why: the guard's "intact" claim only holds if each hook has a declared fail-open or fail-closed behaviour. Core guard block of `interpreter-code-driving-foreman` fired 42x, so the guard is load-bearing. assumption: no table exists.
  Done when: `fm doctor` prints one row per hook (event, mode, crash-tested date) and a test injects an exception into each hook and asserts the stated mode.

- **Run a guard liveness canary at session start** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: a guard that loaded but is silently inert (bad settings, host update, typo'd key) looks identical to a working one. Standing rule says every steer gets an automatic check; the guard itself has none per session. assumption.
  Done when: SessionStart runs a harmless forbidden-command probe through the guard's decision function, and a deliberately disabled guard makes `fm doctor` and the first note report "guard inert".

- **Fix the two brief-guard false positives with a real tokenizer** — FIX — value 4 — effort M — risk med — category: guard
  Why: the pack measures 2 false positives (a dict key and a `.join(` read as written paths). False positives teach users to bypass the guard, which erodes safety.
  Done when: a corpus holding both cases plus the previously blocked true positives passes with zero false positives and zero lost blocks.

- **Make state writes crash-safe, proved by kill-at-every-boundary** — FEATURE — value 5 — effort L — risk med — category: state
  Why: T-2334 (start point missing after git timeouts), the baton/ledger/repo disagreement after a kill, and T-2525 all stem from partial writes or timeouts. Long-horizon exam plants killed sessions. assumption: writes aren't yet fuzzed at each boundary.
  Done when: a harness kills a `fm task` verb after each file write in turn, and every resulting state loads and `fm doctor` reports consistent.

- **Quarantine flaky tests behind the full-check refusal** — FIX — value 4 — effort M — risk low — category: gates
  Why: T-2526 makes `fm task finish` refuse on a failed newest full check; one flaky test now blocks every task with no way to tell flake from regression. assumption: no flake ledger exists.
  Done when: a test failing then passing on identical tree hash is recorded as flaky, the refusal names it as "flaky, rerun" and a rerun clears it, while a stable failure still refuses.

- **Budget the hook tail in CI per event** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: only p95 is tracked; the rule says hook p95 may not grow, but a p99 spike during parallel builder lanes goes unseen. assumption.
  Done when: `bench_hooks.py` also asserts p99 and a max per event, and fails on a regression beyond a recorded threshold.

- **Test hook latency under parallel lanes** — PERFORMANCE — value 3 — effort M — risk low — category: hooks
  Why: Mission 3's pillar runs independent tasks in parallel builder lanes, yet the 278 ms figure is probably session-typical. assumption.
  Done when: a bench spawns N concurrent lane-style hook loads and reports p95 per event beside the single-run figure.

- **Differential-test the guard parser against real bash** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the tokenizer bugs already shown suggest parser mismatches; evasions live in disagreement between guard parse and shell parse. assumption: only hand-written cases exist.
  Done when: a generator emits N shell commands, and the test fails if the guard's verdict differs from a verdict derived from `bash -n` plus the resolved argv.

- **Wild: Run an N-version shadow guard** — SECURITY — value 4 — effort L — risk med — category: guard
  Why: wild. A second, independently written guard (by a different model, from the rules text only) runs in shadow; any disagreement files a task. Catches bugs neither the author nor tests see.
  Done when: the shadow runs on a week of recorded hook inputs and its disagreements with the main guard are listed, each triaged as a bug or an intended difference.

- **Wild: Run a CPU-starved dogfood day** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: wild. A developer machine is never slow in testing; a CI runner or a stranger's VPS is. Throttle to one core at 10% and see which hooks time out and fail open.
  Done when: a throttled run finishes and records, per hook, whether it hit a timeout and what its failure mode did.

- **Wild: Corrupt a settings copy nightly and check the guard stays closed** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: wild. Typo'd keys and truncated JSON are the realistic way a guard goes inert, and a host update can rewrite settings.
  Done when: the night tick mutates a scratch copy of settings in several ways and each mutation yields either a refusal or a loud "guard inert" report, never silent allow.

- **Give each area a reliability error budget** — FEATURE — value 3 — effort M — risk low — category: gates
  Why: lean measures substance now (T-2503), but nothing says how many crashes, false blocks or timeouts per area are tolerable before work stops. assumption.
  Done when: `fm doctor` shows per-area crashes, false positives and timeouts over 7 days against a stored budget, and a breach files one task.

Next question: Which Foreman failures does the user never see because a hook fails open, and what would counting them reveal?
Next question: Does any reliability check run on a surface other than Claude Code (fm code, Codex, headless/server), or does the guard's "intact" claim only hold on one host?
