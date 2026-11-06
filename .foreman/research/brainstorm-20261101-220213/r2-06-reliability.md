# Brainstorm — lens: reliability

**Answers to earlier questions (reliability lens):**
- *Two proofs disagree (green test, broken `fm shot`):* the red one wins by rule. The task can't finish until the user or a re-run reconciles them, and both verdicts are printed side by side.
- *Proofs that need an unreachable vendor:* label them "unreachable, unproven", and only the user may accept one, with an expiry.

## Ideas

- **Declare the unguarded surface at session start** — FIX — value 5 — effort S — risk low — category: guard parity
  Why: T-0337 says Gemini's Stop isn't wired, and T-0336 (live-verify on codex/gemini/opencode) is blocked. A user on those hosts can't tell which protections are missing.
  Done when: starting a session on a host lacking a hook prints one line naming the missing guard or gate. A test asserts the line for each host fixture.

- **Differential-test the guard's command parser against a real shell parse** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: two brief-guard false positives read a dict key and a `.join(` call as paths. A homemade tokenizer diverges from bash in the same way on quotes, heredocs and substitutions.
  Done when: a generated corpus of 500+ commands is run through both the guard's parser and `bash -n`/`shlex`. Any disagreement fails a test, and both known false positives become fixtures.

- **Keep a flake ledger behind `fm task finish`'s full-check refusal** — FIX — value 4 — effort S — risk low — category: gates
  Why: T-2526 now refuses finish when the newest full `fm check` failed. A flaky test would block every task until someone reruns it.
  Done when: a failing test is rerun 3× in isolation. If it flips, finish proceeds with a "flaky: name" note and the ledger counts it. A deterministic failure still refuses.

- **Run the hook hot path on the oldest supported Python** — FIX — value 3 — effort S — risk low — category: portability
  Why: T-2529 showed interpreter-specific breakage. The suite runs only on python3 3.14.
  Done when: `fm doctor` states the supported floor, and `bench_hooks.py` plus the guard unit tests pass under that interpreter in CI.

- **Run the hostile-environment matrix for headless/server** — FIX — value 4 — effort M — risk low — category: headless
  Why: the pack's own sandbox is tmpfs under `/run/user`, and the headless/server column is among the empty cells. Assumption: no test covers read-only `$HOME`, unset `XDG_*`, a non-UTF8 locale, or repo paths with spaces and unicode.
  Done when: `roundtrip.py` passes in each of those four conditions, and failures print which condition broke.

- **Test hook coexistence with other plugins** — FIX — value 4 — effort M — risk med — category: hooks
  Why: Foreman's p95 is measured alone (278 ms). Users run other plugins' hooks on the same events, and ordering and combined latency are unmeasured. Assumption: no such test exists.
  Done when: a fixture with three third-party hook configs shows Foreman's decisions are unchanged under every ordering, and combined p95 is reported.

- **Swap plugin files atomically and pin running sessions** — FIX — value 4 — effort M — risk med — category: install
  Why: hooks and `fm` read the plugin directory live. An update mid-session can serve a torn or mismatched pair.
  Done when: an update during a looping hook run produces no errors. Each session's hooks and `fm` report the same version for its whole life.

- **Kill hooks at every write boundary** — FIX — value 4 — effort M — risk low — category: crash safety
  Why: the pack covers write ordering and lock reaping, but not a SIGKILL landing between any two writes in one hook.
  Done when: a harness kills the hook at each recorded write point. The next `fm status` reads consistent state and names nothing as lost.

- **Pre-stage a gated revert for every `fm ship`** — FEATURE — value 4 — effort M — risk med — category: ship
  Why: T-2527 and T-2518 make CI on main the settlement point. A red main after a push currently needs a hand-made revert.
  Done when: when `ci-watch` sees main red, `fm ship --revert <commit>` produces a ready, gated revert commit, and the user still presses push.

- **Detect evasion after a guard block** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: `core:interpreter-code-driving-foreman` blocked 42× in 7 days. Nothing records whether the next calls complied or routed around it.
  Done when: a block followed within 3 calls by an equivalent action in another form is logged as "evaded" in `fm friction`. A planted evasion triggers it in a test.

- **Wild: Run an N-version shadow guard** — SECURITY — value 4 — effort L — risk med — category: guard
  Why: wild. A second tiny guard in a different language runs in shadow on every call, and any disagreement is written to a file. It catches bugs that same-author tests share.
  Done when: over a recorded 13k-call week the two guards agree on everything or each disagreement has a filed task.

- **Wild: Run a CPU-starved dogfood day** — PERFORMANCE — value 3 — effort S — risk low — category: gates
  Why: wild. A cgroup caps the user's session at 25% CPU for a day. This shows which gates, hook timeouts and child reads fail falsely, which an idle-machine bench can't.
  Done when: a report lists every timeout-induced false refusal, each with a filed fix or a measured-and-accepted note.

- **Wild: Give each area a reliability error budget** — FEATURE — value 3 — effort M — risk med — category: lean and safe
  Why: wild. Each coverage area gets a weekly allowance of false blocks, crashes and flakes. When it's spent, new features there freeze until the fix tasks close, which ties "lean" to "safe".
  Done when: `fm doctor` shows spent/allowed per area. An overspent area makes `fm next` offer only its fix tasks.

- **Measure hook latency under parallel builder lanes** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: `bench_hooks.py --runs 20` runs on a quiet machine, but the real work runs several lanes at once.
  Done when: the bench has a `--load N` mode, and `fm doctor` reports p95 at the current lane count against the idle p95.

Next question: Which of the guard's protections silently depend on the host calling a hook, and what does Foreman do when the host version changes that contract?
Next question: What is the first thing a headless or server user would hit that this repo has only ever run on a desktop Linux box?
