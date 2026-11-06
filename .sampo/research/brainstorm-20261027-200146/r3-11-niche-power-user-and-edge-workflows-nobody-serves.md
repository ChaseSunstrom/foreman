# Brainstorm — lens: niche: power-user and edge workflows nobody serves

- **Turn a pasted CI failure into a task** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: assumption: many failures reach the user as log text rather than a typed request, and the fm quiet heredoc bug shows people pipe text into fm.
  Done when: `cat ci.log | fm task from-log` opens one task that names the failing test command and quotes its first error line.

- **Open a task's changed hunks in the editor's quickfix list** — FEATURE — value 4 — effort S — risk low — category: editor
  Why: assumption: the pane shows diffs, but Vim and Emacs users can't jump from them to the matching lines.
  Done when: `fm task diff --quickfix` writes `file:line:col` entries that `vim -q` or Emacs `compile` open at each hunk.

- **Review someone else's checkout without writing to it** — FEATURE — value 3 — effort M — risk low — category: review mode
  Why: assumption: users sometimes run gates on repos they don't own, and nothing in the pack covers a read-only run.
  Done when: `fm review <path>` runs the gates and writes only inside a scratch worktree, and a write outside it is refused by the guard.

- **Merge the user's hand-edits into a live run instead of conflicting** — FEATURE — value 4 — effort M — risk med — category: concurrency
  Why: assumption: users edit a file while the model is changing it, and today that ends in an edit lease fight.
  Done when: a user edit to a file the run is changing pauses the run and shows a three-way merge with both sides, and the run continues only after the user accepts.

- **Translate Windows paths when fm runs from a WSL repo** — FIX — value 3 — effort S — risk low — category: platform
  Why: assumption: WSL users run fm from Windows terminals, and the path mapping from `C:\` to `/mnt/c/` is untested.
  Done when: `fm status` run with a `C:\…` path resolves to the same task as the `/mnt/c/…` path.

- **Dry-run the guard over your shell history** — FEATURE — value 4 — effort S — risk low — category: guard tuning
  Why: assumption: guard refusals are a pain point, and shell history is free evidence of which commands get refused.
  Done when: `fm guard replay ~/.bash_history` lists each command the guard would refuse with the rule that fired, and leaves the history and the guard unchanged.

- **Let users define verbs that chain fm steps** — FEATURE — value 3 — effort S — risk low — category: power ergonomics
  Why: assumption: power users repeat the same check, then finish, then push, and want one word for it.
  Done when: `[verbs] ship = ["check --affected", "task finish"]` in config makes `fm ship` run both in order and stop at the first failure.

- **Inherit settings from a `.foreman.toml` up the directory tree** — FEATURE — value 3 — effort S — risk low — category: config
  Why: assumption: monorepos repeat the same settings in every project, and the scopes (run, project, everywhere) don't cover a parent directory.
  Done when: a `.foreman.toml` in a parent directory applies to a child project, a child value overrides it, and `fm config show` reports which file each value came from.

- **Run on a 2 GB box with a shrunk context pack** — PERFORMANCE — value 3 — effort M — risk low — category: edge hardware
  Why: assumption: some users run Foreman on small VMs or a Raspberry Pi, and the full pack is sized for a desktop.
  Done when: with `FM_LOW_MEM=1` on a 2 GB machine, a full `fm check` and a task close both finish with peak RSS under 300 MB, measured by `/usr/bin/time -v`.

- **Pause a run at low battery and resume on charge** — FEATURE — value 3 — effort M — risk med — category: power
  Why: assumption: laptop users lose a run's place when the battery dies mid-step.
  Done when: below 10% battery off mains, the run stops at the next step boundary, writes its journal, and resumes after charging with no step repeated.

- **Wild: answer a blocked prompt with one word from your phone** — FEATURE — value 2 — effort L — risk high — category: remote approval
  Why: wild: blocked-on-you items already exist, and a user away from the desk could clear them by text, but this sends outward traffic and needs strong pairing.
  Done when: a reply of `y` from a paired phone number resolves the top blocked item, the reply is logged, and an unpaired number is refused.

- **Wild: a run re-plans when a teammate's push lands on its branch** — FEATURE — value 3 — effort M — risk med — category: collaboration
  Why: wild: the run assumes a still repo, and a fetch can change the files under it.
  Done when: a pull that changes a file the run has open pauses the run, shows which steps the change touches, and re-plans only those steps.

- **Wild: report run state on the terminal bell as a short pattern** — FEATURE — value 2 — effort S — risk low — category: accessibility
  Why: wild: one bell pattern per state gives a screen-reader-free cue for someone who has looked away from the terminal.
  Done when: each of the four states (working, blocked, failed, done) rings a distinct pattern, and the same pattern is shown in the status line.
