# Brainstorm — lens: capability map

- **Back up and restore all Foreman state in one archive** — FEATURE — value 4 — effort S — risk low — category: data safety
  Why: state is spread over backlog, journals, leases and receipts, and nothing takes them as one unit. Assumption: a single `fm backup` / `fm restore` pair closes that gap.
  Done when: `fm restore` on a fresh checkout reproduces `fm status` and the backlog byte-for-byte.

- **Roll a plugin upgrade back to the last working copy** — FEATURE — value 4 — effort S — risk low — category: upgrades
  Why: T-0418 shows the installed foreman-ui drifting behind the repo, and version skew is already a known failure. Assumption: `fm update` should keep the previous plugin copy so one command can restore it.
  Done when: after a failed `/plugin update`, one command restores the prior version and `fm doctor` passes.

- **Encrypt journals and receipts at rest with a machine-local key** — SECURITY — value 4 — effort M — risk med — category: privacy at rest
  Why: journals hold prompts, command output and receipts in plaintext on disk. Assumption: a key kept in the OS keyring, never synced, covers the threat of a copied or backed-up state directory.
  Done when: a journal file opened without the key shows no readable prompt text, and the same `fm status` output appears with the key present.

- **Expire journals and receipts after a set age, per project** — CLEAN — value 3 — effort S — risk low — category: retention
  Why: journals and receipts grow with every run and are never pruned, which adds to the privacy exposure above. Assumption: a default retention window with a per-project override is enough.
  Done when: a journal entry older than the window is removed by `fm doctor --fix` and a newer one is kept.

- **Pin the toolchain in a devcontainer that CI also runs in** — FEATURE — value 4 — effort M — risk low — category: reproducible CI
  Why: CI broke on Ubuntu 26 (uutils `sleep`), Python 3.12 and a snap chromium that crashed under load (T-1799, T-1806, T-1807). Assumption: running CI and local work from one image removes the "works on my box" class.
  Done when: CI and a local `devcontainer up` both report the same toolchain versions and the full suite passes in both.

- **Give each gate a timeout learned from its own history** — PERFORMANCE — value 4 — effort S — risk med — category: gate timing
  Why: a fixed 480 s kill (T-1808) and a 40-minute hang in another project held the gate lock. Assumption: each check's timeout set from its measured p95 plus a margin catches hangs sooner and stops false kills.
  Done when: a check that runs 3× its p95 is killed and reported with its name, and a normal run is never killed.

- **Answer "how do I" from the shipped docs, offline** — FEATURE — value 3 — effort S — risk low — category: docs search
  Why: the dojo's help position collided with another command (test_help failed), which shows that help and docs are maintained by hand. Assumption: a local index over shipped docs answers common questions without a model call.
  Done when: `fm help "how do I defer to the reset"` returns the matching doc section with zero network calls.

- **Print a one-page field manual per release, built from the verb table** — DOCS — value 3 — effort S — risk low — category: docs output
  Why: docs are spread across skills, the site and the help text. Assumption: one generated page per release, sourced from the command table, is the thing a user would print and keep.
  Done when: the release build produces one page that lists every verb once, and a test fails when a verb is missing from it.

- **Show gate failures as diagnostics at the failing line in the editor** — FEATURE — value 3 — effort M — risk med — category: editor surfaces
  Why: the user works in Claude Code and IDE extensions, but a failing check only reports to the terminal or the pane. Assumption: a diagnostics feed on the editor side puts the failure where the cursor already is.
  Done when: a failing `fm check` on a file puts a diagnostic at the failing line in VS Code, and clearing the failure removes it.

- **Wild: ghost-type the next likely fm command in the prompt** — FEATURE — value 3 — effort M — risk low — category: prompt UX
  Why: assumption: after a run closes, the next step is usually predictable from the queue, and showing it in grey text lets the user accept it with Tab. It never runs without a keypress.
  Done when: after a closed task with a queued next task, the prompt shows that task's command in grey, and pressing Tab fills it in without executing it.

- **Wild: pair mode that watches a terminal and suggests, never acts** — AGENT — value 3 — effort L — risk med — category: pair programming
  Why: assumption: a user who types commands by hand loses the proof and guard steps that Foreman adds. A silent observer that suggests the missing proof step would bring them back without taking over.
  Done when: in a watched session, a `git commit` with no proof run prompts a suggested `fm task prove` line, and no command runs without the user's Enter.

- **Wild: a field manual test by a cold reader** — DOCS — value 3 — effort M — risk low — category: docs testing
  Why: the docs are written by someone who already knows Foreman, so they are hard to check for clarity. Assumption: a fresh model that has only the docs and a goal, run in a sandbox, shows the steps where it gets stuck.
  Done when: a cold-reader run on three goals from the docs lists each stuck step, and each one is fixed or filed as a task.

- **Wild: a weekly plain-language health note for people outside the repo** — DOCS — value 2 — effort S — risk low — category: status reporting
  Why: assumption: a non-engineer stakeholder can read a one-page note in plain words (what shipped, what's blocked, what it cost) without opening the terminal.
  Done when: `fm status --note` writes a note under 200 words with no task ids or command names, and the note passes a jargon check.
