# Brainstorm — lens: guard intact

- **Alarm when the Ward goes quiet** — FEATURE — value 4 — effort S — risk low — category: guard health
  Why: assumption: lean cuts and the plugin-id rename could leave the Ward silently deaf. Nothing in the pack watches for "sessions ran, zero blocks".
  Done when: a test feeds a ledger with 50 sessions and 0 Ward decisions, and `sampo doctor` names the Ward as unproven. A ledger with at least one decision per harness stays green.

- **Record a per-harness block rate** — FEATURE — value 4 — effort S — risk low — category: parity
  Why: the user's standing rule says Sampo must work beyond Claude Code, and T-0337 shows Gemini's Stop hook isn't wired. A harness that never blocks looks the same as one that never fires.
  Done when: `sampo doctor --json` prints decisions, blocks and canary results per harness. A harness with canary results but no decisions is flagged.

- **Pin the Ward's read-set** — SECURITY — value 5 — effort M — risk low — category: Ward speed
  Why: state is 2.4 GB, and the Ward must not slow down or fail open as it grows. Assumption: the hook currently reads only a small file set, but nothing enforces that.
  Done when: a test runs the Ward hook under an audit hook or strace against a synthetic 10× state tree. It fails if the hook opens any path outside a declared manifest, or exceeds its time bar.

- **Resolve protected paths from the install-time repo root** — SECURITY — value 4 — effort S — risk low — category: Ward correctness
  Why: children run from a tmpfs cwd that isn't a git repo (`/run/user/1000/fm-children-1000`). If protected-path matching is relative to cwd, a session from there protects nothing.
  Done when: the Ward exam passes the same cases from a non-git tmpfs cwd, a symlinked cwd and a cwd outside the repo.

- **Give every guard sentence a home** — CLEAN — value 4 — effort M — risk med — category: lean safety
  Why: SessionStart injects 2,733 characters twice, and cutting prose can orphan a rule. Assumption: some sentences exist only in the injection.
  Done when: each guard sentence maps to one of a Ward rule id, a block-message string or a readable doc anchor. A test fails on any sentence with none, and the dedupe change passes it.

- **Pass the Ward its own recovery test, with a local agent** — SECURITY — value 4 — effort M — risk med — category: lean safety
  Why: shorter injection means the agent learns the Ward mostly from blocks, so each block message must be enough to recover from. This costs no cloud tokens if run on the local qwen3.8-27b, which is in the pack.
  Done when: for 30 canned blocked commands, a local model given only the shortened injection plus the block text reaches a safe alternative within 2 turns in at least 90% of runs, and the rate is printed.

- **Spend a guard-adjacency budget on lean cuts** — FEATURE — value 3 — effort M — risk med — category: lean safety
  Why: the pack's lean ideas treat all cuts alike, but cutting a hook comment differs from cutting text near the Ward's vocabulary. Assumption: a word-overlap score against Ward rule words is good enough to rank cuts.
  Done when: a lean diff scoring above a threshold requires the Ward verdict corpus to be re-run and shown at ship. A diff scoring below it does not.

- **Publish guard changes as verdict flips** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: the user reads outcomes, not diffs. "Ward still refuses N of N; changed: none" is the line they can trust without opening the diff.
  Done when: the ship digest includes one line of verdict flips against the previous release's corpus, and a planted flip makes the line name the command.

- **Mark time-to-armed at session start** — PERFORMANCE — value 3 — effort S — risk low — category: Ward timing
  Why: assumption: once SessionStart is deduped or made lazy, the Ward might arm after the first tool call. The bench measures hook time but not arm order.
  Done when: `bench_hooks.py` records the first-tool-call-versus-armed ordering. It fails if any tool call can precede arming across 20 runs.

- **Run the Ward canary from outside the plugin (wild)** — SECURITY — value 4 — effort M — risk med — category: independent check
  Why: wild. The rename left thin shim plugins that depend on the real one; a host update could drop the dependency and leave no hooks. An in-plugin canary dies with the plugin, so a separate user timer should run a harmless blocked command through the real hook path and flag silence.
  Done when: disabling the sampo plugin in a scratch home makes the external check report "Ward absent" within one timer tick. Enabling it clears the report.

- **Have a cold child try to dodge the Ward from the injection alone (wild)** — SECURITY — value 4 — effort M — risk low — category: red team
  Why: wild. After the injection shrinks, a tool-less child that sees only the shrunk text and a scratch sandbox proposes 20 ways to cause a refused effect. The Ward is scored on how many get through.
  Done when: the exam prints the count that got through for the old and new injection. A count that rises with the new text fails the gate.

- **Keep a frozen strictness floor outside the tree (wild)** — SECURITY — value 3 — effort L — risk high — category: tamper resistance
  Why: wild. The Ward is edited by the same lean loop that cuts text. A tiny read-only twin, installed once, that can only add refusals would catch a self-edit that loosens one.
  Done when: a planted loosening in the working Ward is caught by the twin on a corpus run, and the twin never allows what the Ward refuses.

- **Show a weigh-in before any bypass session (wild)** — FEATURE — value 3 — effort S — risk low — category: user trust
  Why: wild. The user said "don't ask me for stuff", so the answer is one non-blocking line at session start: "Ward armed, N rules, exam last green on DATE, injection X chars". It is silent when degraded, which then prints its own line.
  Done when: the line appears once per session from a single copy, and a broken Ward replaces it with the degraded line.

Next question: which Ward rules have never fired in the real hook ledger, and is that because they're safe or because nobody has tried to trigger them?
Next question: when the pruner and the Ward both touch state at once (a lane running during `prune --apply`), who wins, and has anyone ever tested it?
