# Brainstorm — lens: moonshots nobody ships

- **Counterfactual Replay Lab: re-run last week's sessions under a candidate rule** — FEATURE — value 5 — effort M — risk low — category: self-evaluation
  Why: the pack has a ledger, recorded hook stdin (planned "record live hook payloads as fixtures"), and a request to genuinely improve itself. Nothing yet answers "would this new rule have helped or hurt?" before it ships. Assumption: ledger plus transcripts hold enough to rebuild each tool-call sequence.
  Done when: `fm lab replay --rule <file> --days 7` feeds recorded PreToolUse/Stop payloads through old and new rule sets and prints a table of decisions that flipped (blocked→allowed, allowed→blocked) with the session and turn for each.

- **Self-Edit Tournament: Foreman proposes a change to its own prompt or rule, and only a measured win ships** — FEATURE — value 5 — effort L — risk med — category: self-modifying harness
  Why: the user asked "why have you not really improved all that much"; existing ideas score and retire hints but none lets Foreman author candidate edits to its own skills and hooks. Assumption: T-0035's eval-capture cases exist or can be mined from closed tasks.
  Done when: `fm lab evolve <skill>` generates 3 variants, runs each against N captured cases in throwaway worktrees, and writes a report with pass rate and cost per variant; a variant is applied only with `--accept` and only when it beats the baseline by a set margin.

- **Intent Telemetry: infer what the user is trying to do from their edits, interrupts and pauses** — FEATURE — value 4 — effort M — risk med — category: user modelling
  Why: the user's words show repeated "still cluttered" and "why have you not improved" reactions that Foreman only learns about after the fact. Corrections are logged (fmhooks 578-615) but not Esc interrupts, rapid re-prompts or hand-edits. Assumption: those events are visible to hooks (UserPromptSubmit timing, git status deltas between turns).
  Done when: a local `intent.jsonl` records interrupt, re-prompt-within-60s and hand-edit-after-agent-edit events per task, and `fm learn --signals` lists the top three patterns with the turns that produced them.

- **Prediction Draft: pre-do the likely next task in a throwaway lane** — FEATURE — value 4 — effort L — risk med — category: predictive work
  Why: the queue, the deferred backlog and the user's habit of chaining follow-ups ("do everything", "and even more") make the next request fairly predictable. Assumption: a draft costing spare quota is acceptable; the pack's overnight idea (C5) covers queued tasks, not guessed ones.
  Done when: after a close, Foreman predicts one follow-up from history, builds it in a hidden worktree under a spend cap, and on the next prompt either offers `fm draft adopt` (when it matches) or discards it; the hit rate is logged.

- **Tool Forge: generate a skill, hook or MCP server when a repeated tool-call sequence appears** — FEATURE — value 4 — effort M — risk med — category: self-extension
  Why: the pack lists repeated manual recipes and "forge tools from repeated command sequences" as ideas, but none produces a runnable artifact with a test. Assumption: repeated sequences can be mined from the ledger by n-gram over normalised commands.
  Done when: `fm forge` finds a sequence repeated 3 or more times, writes a script plus a fixture-based test under `.foreman/forged/`, and runs the test green before it offers to wire the script in as a verb.

- **Hash-Chained Proof Ledger with offline verifier** — SECURITY — value 3 — effort S — risk low — category: provable trust
  Why: "done" claims are checked against commands actually run, but the ledger itself is plain append-only text; a torn or edited line can't be detected, and a stranger can't audit a close. Assumption: the ledger append path is a single function.
  Done when: each ledger line carries the hash of the previous line, and `fm verify-ledger` exits non-zero on a modified, removed or reordered line, with a test that edits one line and sees the failure.

- **Model-Check the Task State Machine** — FIX — value 3 — effort M — risk low — category: formal verification
  Why: the pack shows repeated state bugs (Stop-hook re-entry, queue stealing focus, env prelude growing 8x, idle-while-queued). A small spec would find illegal transitions earlier than field failures do. Assumption: the states and transitions can be written as a table from the existing code.
  Done when: `fm lab model` explores all reachable (task, lane, stop-hook, session) states up to a bounded depth and fails on any state that is stuck, double-owned or unreachable, and the test suite includes one seeded illegal transition that it catches.

- **Bid Market for Subagents** — FEATURE — value 3 — effort M — risk med — category: orchestration
  Why: delegation today picks by tier; the pack plans a measured routing table but nothing lets agents price their own confidence. Assumption: a cheap call can produce a plan plus an estimate of cost and risk.
  Done when: for an L task, 3 bidders return `{approach, est_tokens, confidence}`, a settle step picks the best value, and after close the actual cost and outcome update each bidder's calibration score shown in `fm lab bids`.

- **Wild: Twin of the User that attacks Foreman before the user does** — FEATURE — value 4 — effort M — risk low — category: simulation
  Why: the user's recurring complaints (clutter, scaling, the harness taking focus, missing claude) are reproducible patterns, and each reached the user before any test caught it. Wild; assumption: the steered/asked list can seed a persona prompt.
  Done when: `fm lab twin` runs a hermetic headless session with a persona built from the user's last 30 steers, drives a scripted scenario through the real hooks, and prints which of the user's known complaint classes it reproduced.

- **Wild: Cross-Repo Transplant — carry a solved fix into a sibling project that has the same problem** — FEATURE — value 4 — effort M — risk med — category: cross-project learning
  Why: the user wants learning across projects and machines, and fixes only travel by git within one repo. Assumption: sibling repos on the same machine share fingerprintable stacks (the card detector already knows languages and dependencies).
  Done when: after a fix closes, `fm transplant` scans local repos whose stack cards overlap, shows each with a match score, and opens a draft task in the chosen repo carrying the diff and the original obstacle as context.

- **Wild: Rule Tribunal — a nightly hearing where each rule must justify its token cost with evidence** — FEATURE — value 3 — effort M — risk low — category: harness diet
  Why: the pack lists many planned rules and hooks and a "retire what doesn't pay" principle, but no recurring forum where rules are weighed. Wild; assumption: per-rule fire counts and prevented-failure evidence are available from the enforcement ledger.
  Done when: `fm tribunal` prints for each rule its fires, the failures it prevented, its injected token cost and a verdict (keep, demote, retire), and applying a retire verdict creates a reversible changelog entry.

- **Wild: Mutation Tests for Foreman's Own Discipline** — SECURITY — value 4 — effort M — risk low — category: provable safety
  Why: the pack's "faked compliance" and canary ideas assume the guard and gates work; nothing verifies that each one actually fails when its logic is broken. Assumption: guard and gate rules are in readable Python modules that can be mutated mechanically.
  Done when: `fm lab mutate` flips one condition at a time in the guard and close-gate code, runs the test suite for each mutant, and reports surviving mutants as a list of untested decisions, with a test that deliberately leaves one surviving mutant.

- **Calibration Ledger: every Foreman forecast gets scored** — FEATURE — value 3 — effort S — risk low — category: self-measurement
  Why: the planned forecast (cost, time, pre-mortem) and size labels (S/M/L) are never checked against what happened, and the user has doubted whether Foreman improves. Assumption: closed tasks record actual wall-clock and token numbers.
  Done when: each size or cost estimate is stored with the later actual, and `fm calibration` shows the error by task type and a trend line over the last 30 closes.
