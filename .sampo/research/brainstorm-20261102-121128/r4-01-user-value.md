# Brainstorm — lens: user value

- **Earn autonomy per task kind** — FEATURE — value 5 — effort M — risk med — category: trust
  Why: assumption: the user's steers and the "never block on the user" rule show they want fewer interruptions, but today every task gets the same ceremony. Held-rate and Brier data by bet kind already exist (T-2610, T-2624).
  Done when: `fm autonomy` prints a level for each task kind (ask first, land with receipt, auto-land) from its settled record, and a kind drops a level after one reversed "proven" label in a test fixture.

- **Keep test fixtures out of the live ledger** — FIX — value 4 — effort S — risk low — category: ledger hygiene
  Why: the user's recent asks include "FEATURE: the first brief" and "FIX: the second brief", which look like test fixtures that reached the real intake. Pasted keys got a similar skip in T-2624.
  Done when: a test that runs the intake suite leaves zero new tasks in the real ledger, and `fm doctor` flags asks that match known fixture phrases.

- **Learn from hand edits after landing** — FEATURE — value 5 — effort M — risk med — category: learning
  Why: every steer in the pack was stated by the user. Edits they make by hand to lines Foreman just landed are corrections they never voice. assumption: the user commits to the same repo.
  Done when: given a fixture where a user commit rewrites Foreman-written lines within 24 hours, `fm lessons` proposes one candidate steer that cites the commit and the task id.

- **Mine closed FIX tasks into finder rules** — FEATURE — value 4 — effort M — risk med — category: initiative
  Why: T-2554, T-2566 and the "readers count the wrong population" fixes share one root-cause class, and each was found only after the user asked. `fm find` is the free first pass.
  Done when: `fm find --learned` flags the T-2566 pattern (a decider that ignores one split) in a seeded copy of the pre-fix code.

- **Triage the deferred pile in five minutes** — FEATURE — value 4 — effort S — risk low — category: queue
  Why: 30+ "Later from T-07xx/08xx" tasks sit deferred. The user decides in bulk but the queue gives them no bulk tool.
  Done when: `fm triage` shows each deferred task with its evidence, accepts one key (keep, drop, merge, snooze) per task, and applies all choices at the end with a count.

- **Show the three hunks you'd reject** — FEATURE — value 4 — effort M — risk med — category: review
  Why: the user reviews large generated diffs (the 1,388 skill files, Genesis towers). The user model (fmforesight) already predicts their steers. wild
  Done when: before review, `fm review` ranks hunks by predicted rejection. Over the last 20 closed tasks, the user's actual reverts fall in the top 3 more often than a random pick would.

- **Audit your plain sessions for what Foreman would have caught** — FEATURE — value 4 — effort M — risk low — category: adoption
  Why: assumption: the user can't tell whether the discipline pays off outside their own repo. Existing transcripts and the guard rules are enough for a read-only report. wild
  Done when: `fm retro --path <transcripts>` prints per-session counts of guard blocks and unproven "done" claims, and names no session it couldn't parse.

- **Define-on-first-use lint plus `fm glossary`** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: the README and steers use Genesis, tower, Seed, Mission, cell, steer and Brier without a shared definition. The user returns after gaps, and a newcomer can't follow.
  Done when: `fm check` fails a doc that uses a glossary term before defining it, and `fm glossary` lists every term with the file where it is defined.

- **Offer a plan menu on L tasks** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: ten or more L and M tasks (T-0034, T-1207, T-1231) sit deferred or blocked, and the user can't pick without a cost comparison. Planning already runs before edits.
  Done when: for a seeded L task, `fm plan --menu` prints 3 sketches, each with a proof command, a size and a risk, and the chosen one is recorded in the task.

- **Emit the user's way of working for other harnesses** — FEATURE — value 3 — effort S — risk low — category: portability
  Why: the steers say Foreman isn't Claude-specific, but the rules live only in Foreman's store. T-0365 covers just a generated map section.
  Done when: `fm export --harness codex|gemini|opencode` writes an AGENTS.md-style file with the active steers, and a test shows each of them appears in the file.

- **Add a one-key regret button on landed work** — FEATURE — value 4 — effort S — risk low — category: feedback
  Why: assumption: the user will say "wish I hadn't" faster than they will write a steer. The rule that every steer needs an automatic check shows they want a corrections loop.
  Done when: `fm regret T-####` records the regret, names the earliest stage whose check could have caught it, and files one task to tighten that stage.

- **Verify host changes with commands, not hope** — FEATURE — value 3 — effort M — risk med — category: ops
  Why: the user runs a hardened Arch host, and T-0325 is blocked on a pacman package. Package upgrades and unit changes are exactly the work the discipline layer should prove. wild
  Done when: an OPS task kind records a snapshot, runs a systemd or journal check before and after, and finishes only when the after-check passes.

- **Print a "while you were away" card** — FEATURE — value 4 — effort S — risk low — category: reentry
  Why: Foreman works unattended (nights, ticks, drives) for hours, and the user comes back to a pack this size. T-1344's changed-since line covers only the `fm code` home.
  Done when: the first session after 4+ idle hours opens with at most 8 lines: what landed, what failed, and the single decision that blocks the most queue items.

Next question: Which of the user's recurring corrections are never written as steers, and where would Foreman find them (hand edits, reverts, rejected diffs)?
Next question: When two of the 30+ standing steers conflict on a real task, who notices first, and what does Foreman do?
