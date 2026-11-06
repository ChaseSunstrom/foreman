# Brainstorm — lens: simplicity

- **Fast-forward single-commit tasks, drop the Merge commits** — CLEAN — value 2 — effort S — risk low — category: history
  Why: the recent log shows every task twice (`T-2651:` then `Merge T-2651:`), so the log is twice as long to read and bisect.
  Done when: closing a one-commit task adds exactly one commit to main, and `git log --merges` stays empty for it.

- **Batch Genesis site publishes into one daily commit** — SECURITY — value 3 — effort S — risk low — category: outward actions
  Why: the standing rule publishes `site/genesis` on every tower change. Each publish is an outward push through `fm ship`.
  Done when: ten tower changes in a day produce one push, and `fm genesis live --now` still forces an immediate publish.

- **Drop Foreman Desktop and open the web UI in browser app-mode** — CLEAN — value 4 — effort M — risk med — category: surfaces
  Why: T-0325, T-0352 and T-0418 have been blocked on libappindicator, a publish pipeline and a mod update. Assumption: the web UI already covers what Desktop shows.
  Done when: `fm ui --app` opens a chromeless window, the three tasks close with a reopen condition, and the Desktop tree is gone from the install.

- **Make the unattended drive allowlist-shaped** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: a denylist only grows. The drive already knows the repo's gates (`fm map`), so unattended runs could be limited to those gate commands, with git and file edits inside the worktree. Anything else would queue for the user.
  Done when: an unattended lane running an off-list command (say `curl`) is held and shown in `fm next`, while the repo's own gate commands run unchanged.

- **Drop the Haiku first-pass cold read if it never changes an outcome** — PERFORMANCE — value 3 — effort S — risk low — category: cold reads
  Why: Sonnet's verdict stands on any Haiku non-pass. If Haiku only shortcuts passes, replaying past filings shows whether it saves anything.
  Done when: a replay of the stored cold reads reports how often Haiku's pass was overturned. If it was overturned at least once, the stage stays. Otherwise it is removed and the rule text is updated.

- **Close T-0034 and T-0035 as covered by `fm exam` and `fm outcomes`** — CLEAN — value 3 — effort S — risk low — category: backlog
  Why: both are deferred L features (`fm audit run`, `fm eval capture`). Assumption: the exam scenarios and outcome survival already give signals Foreman didn't author.
  Done when: each task is closed with the existing verb that covers it, or a concrete gap is named and carried into a new S task.

- **Turn verbs under 40 lines into rows of a recipe table** — CLEAN — value 3 — effort L — risk med — category: structure
  Why: `fm help` lists a long tail of small verbs, each with its own parser, help string and tests. Assumption: many are thin wrappers around a ledger read and a print.
  Done when: at least ten verbs run from one table, their tests become one parametrized test, and the line count of `plugin/lib` drops.

- **Start each Mission by trying to delete the previous Mission's largest addition** — CLEAN — value 4 — effort M — risk med — category: lean process (wild)
  Why: the lean-substance rule makes unmeasured growth wait but never forces a delete attempt. This extends it into a habit.
  Done when: each Mission's first task is the deletion attempt. The addition stays only if an exam or outcome line defends it, and the result is recorded.

- **Draw a simplicity constraint card at the start of each Mission** — FEATURE — value 2 — effort S — risk low — category: lean process (wild)
  Why: gen-0 sets lean as a goal but gives no constraint to design against. Cards such as "no new file", "no new flag" or "net-negative lines" turn it into one.
  Done when: the Mission spec names its card, and the cold read fails a diff that breaks it.

- **Run a dry-run `fm ship` that prints the push and its blast radius first** — SECURITY — value 3 — effort S — risk low — category: ship
  Why: the push grant allows pushing to main at any time. A one-screen summary of files touched, new verbs and new network paths costs one command and makes the grant legible.
  Done when: `fm ship --plan` prints that summary without pushing, and the real ship prints the same summary before it pushes.

- **Hide every verb that has no session path from default `fm help`** — CLEAN — value 3 — effort S — risk low — category: help
  Why: the standing rule says every capability needs a session path (session start, `fm next`, the drive, a skill or a hook). A verb with none is by that rule a manual curiosity, so help can hide it.
  Done when: `fm help` lists only verbs a session path reaches, and `fm help --all` shows the rest.

- **Wild: Run a "one-file Foreman" week where main must pass the ship gate from a single directory listing under 100 files** — CLEAN — value 2 — effort L — risk high — category: structure (wild)
  Why: the repo has 2129 files, 1388 of them skills. A hard cap forces the real argument about what the core is.
  Done when: a scratch branch boots `fm doctor` and the roundtrip e2e with the capped tree, and the report lists what was dropped and what broke.

Next question: which part of Foreman's weight does the user actually feel (start-up time, help length, review burden, context tokens), so "lean" can be measured by that one thing?
Next question: of everything Foreman writes unattended (commits, pushes, site data, filed tasks), what is the smallest set the user would still miss if it stopped?
