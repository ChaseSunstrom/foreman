# Brainstorm — lens: unspoken needs

- **Seal gen-0 and the standing intent with a hash the tower cannot write** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: steers say "gen-0 never changes" and the standing intent sits above every steer, but nothing outside the tower's own write path detects an edit to either. This is a second-order item: it protects the invariant the other self-checks depend on.
  Done when: editing gen-0 or `templates/standing-intent.md` in a scratch copy turns `fm doctor` and the sweep red, naming the file. The reference hash lives in a place the tower's writers refuse (a git ref or an out-of-repo file).

- **Detect conflicts between standing steers and show which are binding now** — FEATURE — value 5 — effort M — risk med — category: steers
  Why: about 40 steers now overlap and several conflict. The lean-subtraction task (T-2503) files deletions, while gen-2 says "none is ever removed" and "only proven harm or exact duplication removes an idea". "Never block on the user" sits beside "say which once with `fm ask`". Steers like "T-2462 waits with T-2441 until round 1" are time-bound holds. The existing ideas only check a new feature against steers, not steers against each other.
  Done when: `fm decide --check` lists each pair of steers whose checks give opposite verdicts on one recorded action. Each pair carries a precedence line, or it goes red. `fm steers` marks held steers with their end condition.

- **Reopen blocked tasks and not-yet entries when their blocker's probe turns true** — FEATURE — value 4 — effort S — risk low — category: unblocking
  Why: T-0325, T-0336, T-0337 and T-0418 are blocked on facts a command can check (`pacman -Q libappindicator-gtk3`, `command -v codex gemini opencode`, installed foreman-ui version). The "wake predicates" ideas cover deferrals, but blocked tasks and genesis `not-yet.md` entries have no probe.
  Done when: each blocked task and `not-yet.md` row carries a `probe:` line. A tick run with the probe stubbed true moves the item to open and says why.

- **Name the one user action that unblocks the most work** — FEATURE — value 4 — effort S — risk low — category: unblocking
  Why: T-0335, T-0336 and T-0337 share one blocker (no real non-Claude CLI to test against). T-0325 and T-0352 share another (the Desktop build). The user only sees ten separate blocked lines.
  Done when: `fm next` or `fm doctor` prints "install X: frees T-a, T-b, T-c", ranked by items freed, from a blocker field on each item.

- **Schedule heavy rows right after a usage window resets** — PERFORMANCE — value 3 — effort M — risk med — category: pacing
  Why: steers say to wait out limits and not drop work. A multi-day plan has L rows (the long-horizon exam, builds) and S rows (docs, probes). Assumption: the window reset time is readable from `fmbudget`.
  Done when: in a replay with a fake budget clock, L rows start in the first third of a window and S rows fill the last third. The ledger shows fewer L rows interrupted by a limit than FIFO order.

- **Size each plan row to fit one context window** — FEATURE — value 4 — effort M — risk med — category: plan quality
  Why: the request is to carry a plan across compactions. A row whose touched files (from `fm graph`) exceed the budget gets compacted mid-row. Assumption: file-size sums approximate token footprint well enough.
  Done when: `fm goal` splits or flags any row whose estimated footprint exceeds a set fraction of the window. A compaction-count-per-row column shows it falling on a replayed goal.

- **Quiz the resumed session after every real compaction** — FEATURE — value 4 — effort M — risk low — category: resume fidelity
  Why: existing ideas test file-only resume or a cold child. Nothing measures what the live resumed model got wrong. Five questions come from files: current row, last decision, the binding steers, the finish oracle, and a planted arbitrary token.
  Done when: after a compaction, the next turn gets a "recall check" whose answers are graded against the files. The misses are logged per fact class, and the commonly lost facts are put first in the resume brief.

- **Attribute crashes and kills to plan rows and shrink the repeat offender** — FIX — value 3 — effort S — risk low — category: crash recovery
  Why: the request says the plan survives crashes, but the baton records only that a crash happened. A row hit by 2 or more crashes (huge output, OOM, hung command) should change. T-0798 defers crash-loop quarantine without tying it to rows.
  Done when: a kill during row R twice in a row makes the third attempt run with capped output or a split row, and the goal page shows the crash count on R.

- **Group commits into a capability-level changelog for a human reader** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: the log is at T-2611, and recent commits are narrow gauge refinements (the ship-chance record, the calibration windows, the night-tick naming). The user cannot follow that rate commit by commit.
  Done when: `fm changelog --week` groups commits by MASTER.md clause. It puts changes with no observable effect in a one-line "internal" bucket. Every commit lands in exactly one group.

- **Cluster review findings by root cause before they become tasks** — CLEAN — value 3 — effort S — risk low — category: queue hygiene
  Why: gen-2 review findings #12, #16 and #21 were filed as tasks, then dropped as folded into #22 or the same as #1. That is filing churn that a dedupe step before filing would have caught.
  Done when: filing review findings runs a duplicate pass first, and a replay of the gen-2 review files at most one task for the #12/#16/#22 cluster.

- **Keep case law for steers (wild)** — FEATURE — value 3 — effort M — risk low — category: steers
  Why: wild. The steers say to decide instead of asking and record costly decisions. Each such decision is a precedent that today sits only in a report. Cases get stored with the steers they applied and the user's later reaction. The user can overrule a case, and that edits the steer. Assumption: `fm decide` records are structured enough to cite.
  Done when: a new ambiguous decision cites the nearest earlier case by id. Overruling a case in one command creates or edits a steer and its check.

- **Emit a reviewed one-shot unlock script for the user-only installs (wild)** — FEATURE — value 3 — effort S — risk med — category: unblocking
  Why: wild. Some blockers are sudo steps Foreman must never run (`sudo pacman -S ...` for T-0325). Foreman writes one commented script collecting every keystone step. The user reads and runs it, and Foreman never executes it.
  Done when: `fm unlock` prints a script where each line cites the task it frees. A test confirms Foreman's own code never invokes it.

- **Draft the steer the user is about to give (wild)** — FEATURE — value 4 — effort M — risk low — category: steers
  Why: wild. Three "steered" rows are corrections of Foreman's own invented details: the 8+ versus 7 characters, the ambiguity rule, the hash reassignment. The rule is that every steer becomes a standing rule with an automatic check. A pattern of 3 or more similar corrections could arrive as a drafted rule and check, ready for one yes. Assumption: clustering corrections is feasible on the asked stream.
  Done when: on a replay of past corrections, a drafted steer appears before the third repeat. The draft includes its `fm decide --check` command, and a test confirms it fails on the offending example.

Next question: Which of the ~40 standing steers have never had their automatic check fire, and which of those are actually unreachable by any session path?
Next question: When the tower stops (budget, usage window, blocked, crash), what is the first line the user reads, and does it say done, stopped, or waiting?
