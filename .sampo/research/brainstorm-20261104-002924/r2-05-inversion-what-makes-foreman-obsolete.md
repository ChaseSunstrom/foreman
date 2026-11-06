# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Teach at the block, not at the start** — CLEAN — value 4 — effort S — risk low — category: context
  Why: SessionStart injects 2,733 characters twice. Some of that prose describes rules Ward already enforces by hook. The agent learns nothing from a sentence it can't break, and Ward's block message teaches it just in time. Assumption: block messages already carry a `Next:` line.
  Done when: a lint lists every injected sentence that a Ward rule enforces. After those are moved into the matching block message, SessionStart shrinks by the lint's counted characters and the Ward exam is unchanged.

- **Run the Ward exam through the host's own permission check** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: Ward becomes redundant wherever the host's native deny rules or sandbox already refuse the same command. Nothing in the pack measures that overlap. Assumption: the host can evaluate a command against its permission rules offline.
  Done when: `sampo ward overlap` prints N cases the host also refuses and M that only Ward refuses, and a test pins both counts on the fixture exam.

- **Ablate the 2.4 GB state itself** — PERFORMANCE — value 4 — effort M — risk low — category: state
  Why: the 2.4 GB of project state has no measured benefit. Earlier ideas prune or tier it, but none asks whether any of it changes a result. Assumption: held-out scenarios can run against a fresh state directory.
  Done when: a report runs the same held-out scenarios with full state and with an empty state plus only the keep-set, and it names the state classes whose absence changed an outcome.

- **Enforce the floor from git hooks when host hooks vanish** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: T-0337 shows Gemini's Stop hook can't be wired, and host hook protocols change. A pre-push or pre-commit floor enforces the proof receipt and refuses protected-path edits for any agent, with or without Sampo's hooks. Assumption: git hooks fire in lane worktrees.
  Done when: with all host hooks disabled in a scratch repo, a push with no proof receipt is refused by the git hook, and a test covers it.

- **Defer to the host's native plan mode at runtime** — FEATURE — value 3 — effort S — risk low — category: host-overlap
  Why: if the host ships plan mode or task tracking, Sampo's plan nudges and per-turn lines double up. The per-turn burden of 48–76 characters is then pure duplication. Assumption: the hook payload exposes the permission or plan mode.
  Done when: in a recorded plan-mode payload the plan nudge is empty, and the per-turn characters drop by the nudge's length in a test.

- **Log what happened just before every switch-off** — FEATURE — value 3 — effort S — risk low — category: churn
  Why: a user disables a tool because it was slow, noisy or wrong, and that event never reaches the project. Assumption: `off`, `--vanilla` and uninstall go through code Sampo controls.
  Done when: each off event records the last Ward block and the last hook p95 timing, `sampo doctor` shows the last three, and a test with a planted slow hook sees the link.

- **Lint that every pointer in injected text is readable** — FIX — value 3 — effort S — risk low — category: docs
  Why: MASTER.md is 75,758 tokens, so Read refuses it, yet the README links to it as Docs. The same trap may exist for other files that injected text or skills point to. Assumption: Read's size limit is known or measurable.
  Done when: the ship gate fails on any injected or skill-referenced path whose size exceeds the Read limit, and passes on the fixture after sharding.

- **Shed non-Ward injection when the context window is crowded** — PERFORMANCE — value 3 — effort M — risk med — category: context
  Why: small context is the stated goal, and a full window is when extra injected text costs the most. Assumption: the transcript gives a usable fill percentage.
  Done when: above a threshold the per-turn text is empty except Ward's liveness, and replayed transcripts at 40% and 85% fill show different character counts.

- **Express hook overhead as a share of the host's own turn time** — PERFORMANCE — value 3 — effort S — risk low — category: speed
  Why: the benchmark gate checks absolute milliseconds. Users abandon a tool when its overhead feels large next to the host's own latency. Assumption: transcript timestamps give each turn's duration.
  Done when: `sampo doctor` prints "hooks = X% of p50 tool-call time" from real transcripts, and the bench fails above a set ratio.

- **Chart each capability's delta against model strength** — FEATURE — value 4 — effort L — risk med — category: necessity
  Why: the local models (qwen3.6-35b, qwen3.8-27b) already exist and cost nothing in tokens. Running held-out scenarios with and without each capability across weak, mid and strong models shows which capabilities shrink as models improve. Assumption: the exam harness accepts a local backend.
  Done when: a table lists, per capability, the delta at three or more model tiers and flags those that fall to zero at the strongest tier.

- **Wild: Hold a monthly obsolescence pre-mortem written by a cold child** — FEATURE — value 3 — effort M — risk low — category: necessity
  Why: assumption: the strongest case for dropping Sampo has not been written down. A tool-less child gets the host's changelog and the verb table and writes the five sentences a sceptic would use. Each must be answered by a measured number or becomes a retire task.
  Done when: the report holds five sentences, each linked to a command's output or a filed task.

- **Wild: Draft each capability's retirement as an upstream feature request** — FEATURE — value 3 — effort M — risk med — category: host-overlap
  Why: the host is the only party that can make a capability native. A request carries ledger evidence (held rate, outcomes) and ends in a retire-when predicate that fires when the host ships it. Assumption: the user wants to send these.
  Done when: for one capability, `sampo upstream draft` writes a request body with the ledger numbers and sets a `retire_when` check that a test flips.

- **Wild: Have the user stop paying for a capability by default, and make it re-earn a slot on request** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: assumption: the user would delete more if deletion were free and reversible. A dormant-by-default profile shows each capability as a one-line menu entry. Naming one wakes it for the session and logs the use.
  Done when: a session in dormant profile injects only Ward and the menu, waking a capability adds its text in the next turn, and the wake is logged.

Next question: which Sampo behaviours do unprompted stock sessions on the newest model already show, as seen in the user's own vanilla transcripts?
Next question: when the user last turned a hook off, what did Sampo do in the five minutes before?
