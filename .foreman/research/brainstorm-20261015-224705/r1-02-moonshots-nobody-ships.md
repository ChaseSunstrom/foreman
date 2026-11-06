# Brainstorm — lens: moonshots nobody ships

- **Mint a per-repo benchmark from git history** — FEATURE — value 5 — effort M — risk low — category: self-evaluation
  Why: assumption: the queue already lists T-0035 eval capture, "Bench vs plain Claude (needs cases)" and "Replay old failures", and all of them are blocked on a case corpus. Any repo's own history can supply one. For each past commit that touched a test, `fm bench mint` records the parent sha, the commit message as the task, and the test command that fails at the parent and passes at the commit. Minting needs no model calls, so the cost is only the later runs. Once the corpus exists, rule A/B tests, Lite-vs-full comparisons and a check of old rules whenever a new model ID ships all run on it.
  Done when: `fm bench mint --n 5` on a fixture repo writes 5 cases, each verified red at the parent and green at the child.

- **Forge project tools from repeated command pipelines** — FEATURE — value 4 — effort M — risk med — category: self-extension — wild
  Why: assumption: the ledger can see the same Bash sequence run 3 or more times. `plugin/templates/mcp-server/` already exists, so Foreman can emit a script into `.foreman/tools/` with a test and register it as a stdio MCP tool, behind a yes/no prompt. The same mechanism covers a card or skill drafted from fetched docs when a dependency has no card. No coding harness writes its own tools from observed habit.
  Done when: running the same 3-command pipeline three times in a fixture session produces a proposed tool whose test passes and which appears in the project's MCP list after the user accepts.

- **Keep a refuted-hypotheses ledger for FIX tasks** — FEATURE — value 4 — effort S — risk low — category: debugging memory
  Why: assumption: the resume capsule in C1 carries the plan and the failing proof but not what was already ruled out, so a resumed or new session re-tests dead theories. `fm task hyp add|refute|confirm` stores each with its evidence in git-carried state. It is re-injected on resume and when a file tied to a refuted theory is edited, and it can seed known-fix lookups when a hypothesis is later confirmed.
  Done when: after a hypothesis is refuted, a fresh session on the same task shows it in its start brief, and editing the linked file prints "refuted: <theory>".

- **Run an interrupt autopsy on every Esc** — FEATURE — value 4 — effort S — risk low — category: intent telemetry
  Why: the user's drops and steers show friction that is currently inferred after the fact. The transcript marks "[Request interrupted by user]", and today nothing captures why. On the next prompt, Foreman snapshots the last 5 tool calls and classifies the interrupt (wrong direction, too slow, out of scope, stop-and-ask) from the next message's wording or a one-key prompt. Repeats feed the correction-to-rule path in C3.
  Done when: a recorded interrupt followed by "no, not that file" writes an autopsy entry with a category and the 5-call snapshot, visible in `fm learn`.

- **Run dependents' tests against my change** — FEATURE — value 4 — effort M — risk med — category: cross-repo
  Why: assumption: Foreman knows the machine's other projects, since it ranks "what next" across them. When a task changes a public module, it finds sibling repos that import the package or install it editable, then runs their gate in a temp worktree with an override path. Failures go on the task as evidence, and a "same bug shape" grep of siblings runs when a fix closes.
  Done when: changing a function signature in fixture repo A turns red the gate summary for dependent repo B, with B's failing test named.

- **Build a ghost reviewer from the repo's own review history** — FEATURE — value 4 — effort M — risk low — category: review
  Why: assumption: `gh` is available, since issues→tasks already uses it. `fm adopt` pulls the last ~200 merged-PR review comments, clusters the recurring complaints into at most 10 concrete checks, and runs them as a lens on each diff. This is the maintainers' own taste rather than generic lint.
  Done when: on a fixture PR history with a repeated "missing test for error path" comment, the lens flags a diff that lacks one.

- **Let a decision twin answer asks overnight, with earned autonomy** — FEATURE — value 4 — effort M — risk med — category: autonomy — wild
  Why: the user keeps steering with "don't ask me, just do it". Past `fm ask` answers, approvals and denials train a per-category predictor. Above a confidence threshold the twin answers and tags the decision "twin-decided". Next morning the user confirms or reverses these with one key, and each category earns or loses permission from its measured accuracy.
  Done when: a night run records at least one twin-decided answer, and a reversal drops that category's autonomy in `fm digest`.

- **Use prediction error as the slow-down signal** — FEATURE — value 3 — effort M — risk med — category: agent control — wild
  Why: assumption: current controls react to failures, not to surprise. Before a gate or test run the agent states one line, `fm expect "fails on X"`, and the hook compares it with the actual outcome. Two surprises in a row inject "stop, recon first", and surprise rates feed the scoreboard in C12.
  Done when: a run that violates its stated expectation twice produces the recon injection, visible in the ledger.

- **Settle delegation by calibrated bids** — FEATURE — value 3 — effort M — risk med — category: orchestration — wild
  Why: the idea list has price-and-pass-rate routing but nothing that scores the model's own estimate. A cheap probe returns "can do, ~N tokens, p=0.8" for each candidate. After the task closes, the bid is settled against the real outcome and a Brier score per model and task class is kept. The router weighs bids by that calibration, so overconfident models lose work.
  Done when: `fm bid report` shows a Brier score per model computed from at least 10 settled fixture tasks.

- **Fingerprint the environment at every green and diff it on red** — FIX — value 3 — effort S — risk low — category: reliability
  Why: recent gate failures came from the environment, not the code: claude only at `~/.local/bin`, PATH changes, tests reaching the paid binary. Store a compact toolchain fingerprint (binary paths, versions, key env, lockfile hash) with each green gate. A red gate with unchanged code prints the fingerprint diff first.
  Done when: removing `~/.local/bin` from PATH between two gate runs makes the red output start with "env changed: claude path".

- **Write a hash-chained effects manifest per task** — SECURITY — value 3 — effort M — risk low — category: provable safety
  Why: assumption: the ledger records tool calls but is not tamper-evident. At close, emit the exact files written, commands run and hosts contacted, chained by hash to the previous task's manifest and compared with the plan's declared scope. Any effect outside the declared scope is flagged. Commits get the manifest hash as a trailer.
  Done when: editing a past ledger line makes `fm verify chain` fail, and an out-of-scope write shows in the close receipt.

- **Consolidate lessons into principles during idle time** — CLEAN — value 3 — effort S — risk low — category: learning
  Why: assumption: lessons, fixes and corrections only accumulate, and the planned ladder only promotes upward. A periodic pass merges 5 or more near-duplicate lessons into one principle with its examples, retires the originals reversibly, and re-checks the result against replayed cases.
  Done when: 6 similar fixture lessons collapse to one principle, and `fm learn --undo` restores all 6.
