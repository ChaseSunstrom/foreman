# Brainstorm — lens: capability map

- **Checkpoint builders to a git ref so resume never loses work** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: you asked for easy resume of stopped worktree builders and T-1028 is only planned. Finding the worktree isn't enough if it was deleted or left dirty. Assumption: builders can be hooked on PostToolUse.
  Done when: killing a builder mid-task and deleting its worktree, then running `fm resume T-xxxx`, restores the branch, the uncommitted edits (from `refs/foreman/wip/T-xxxx`) and the brief.

- **Offer resume at SessionStart** — FEATURE — value 4 — effort S — risk low — category: resume
  Why: nobody remembers to ask "what was stopped?". A hook sees dead PIDs with open tasks. Assumption: by-pid records identify dead sessions (T-1001/T-1003 suggest so).
  Done when: a fresh session in a repo with an orphaned builder prints one line, "T-xxxx stopped 2h ago at step 3, `fm resume`", and prints nothing otherwise.

- **Score every learned fix by hit rate and retire the losers** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: you asked "why haven't you improved". T-1032 records and offers hints but nothing shows whether they helped. Assumption: the offer and the outcome are both logged.
  Done when: `fm hints stats` lists each hint with offered/accepted/fixed counts, and a hint that failed 3 times in a row is marked stale and no longer offered.

- **Promote hints project → machine → shared pack with redaction** — FEATURE — value 4 — effort M — risk med — category: transfer
  Why: you steered that fixes must travel with git and also work across projects. Project hints are in the repo, but nothing lifts a repeated fix into the machine-wide store.
  Done when: a fix seen in 3 projects is proposed for machine scope, paths and secrets are stripped, and `fm hints import <git-url>` merges it with provenance.

- **Predict file overlap before dispatching parallel builders** — FEATURE — value 4 — effort M — risk low — category: fleet
  Why: the Agents graph shows parallel worktrees, but merge conflicts are unaddressed. `fm map` knows tests→src and blast radius.
  Done when: two queued tasks touching the same file are serialised or flagged, and a test shows the planner refusing to parallelise them.

- **Add a per-step file rewind** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: Cline and Cursor ship checkpoints, and the pack shows none. Plan-then-edit steps are natural restore points. Assumption: step boundaries are recorded.
  Done when: `fm rewind step 2` restores the tree to the end of step 2 without touching other worktrees, and the dirty tree is saved first.

- **Ship to a PR and keep fixing until CI is green** — FEATURE — value 5 — effort L — risk med — category: CI loop
  Why: the gates run locally, but nothing carries a task through PR and CI. Devin and Sweep do. Assumption: `gh` is available.
  Done when: `fm ship T-xxxx` opens a PR, polls CI, feeds failing logs to a fix attempt (max 3), and reports the final state.

- **Turn GitHub issues into tasks with dedupe** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: T-0317, "there's new bug feedback", sits deferred, so intake is manual.
  Done when: `fm intake gh` creates one task per new issue, linked by number, and a re-run creates no duplicates.

- **Cap tokens and spend per task and show the bill** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: users complain about token burn. Aider and Cline show cost. Foreman has no visible budget per task (the injected-context cap idea covers only context).
  Done when: a task with `--budget 200k` warns at 80% and stops at 100%, and the pane shows a spent/budget meter.

- **Send push alerts when blocked and answer from a phone** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: unattended overnight work is a theme (T-0793), and Foreman's only surface is the web UI. Assumption: ntfy or similar is acceptable and off by default.
  Done when: a blocked task sends one notification, replying "yes" from the phone grants the pending ask, and with the setting off nothing leaves the machine.

- **Scan outputs and commits for secrets before they leave** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard stops dangerous commands, and T-0275/T-0791 are open. Nothing is shown that checks content going into commits or to external brainstorm children.
  Done when: a commit or prompt containing a planted fake key is blocked with the file and line, and a clean diff passes.

- **Quarantine flaky tests automatically** — FIX — value 3 — effort M — risk low — category: reliability
  Why: gate failures in the pack came from environment (PATH, claude lookup). A red-then-green proof gate is hurt by flakes. Assumption: run history is stored.
  Done when: a test that flips on identical trees 2+ times is labelled flaky, retried once, and reported separately instead of blocking.

- **Wild: Idle "dream" mode that replays past failures offline and drafts hints and rule patches** — FEATURE — value 5 — effort L — risk med — category: self-improvement
  Why: wild. You want real self-improvement. Between sessions, a local job mines the failure ledger, proposes a hint with a test, and queues it for approval, never auto-applied.
  Done when: after seeded failures, `fm dream` yields at least one drafted hint whose test fails without the hint and passes with it.

- **Wild: End-of-day shift report** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. The foreman metaphor fits a daily log of closed, blocked, learned and cost, as one markdown page or push note. Assumption: the ledger has the data.
  Done when: `fm shift` writes `shift-YYYY-MM-DD.md` with the counts matching `fm history`.

- **Wild: Cheap live shadow reviewer that watches the diff stream and interrupts** — FEATURE — value 4 — effort L — risk high — category: verification
  Why: wild. A small model reads each edit as it lands and pauses the builder on obvious breakage (ignored requirement, deleted test), instead of reviewing at close.
  Done when: a seeded bad edit (test deleted) triggers an interruption within one turn, and a benign edit triggers none across a 20-edit fixture.

- **Generate an ADR/decision log from closed tasks** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: docs are thin in the pack, and task close already holds the "why" and the plan. Another session or teammate cloning the repo gets context for free.
  Done when: `fm docs adr` writes one file per task that changed a decision, each with a task link, and a re-run is idempotent.
