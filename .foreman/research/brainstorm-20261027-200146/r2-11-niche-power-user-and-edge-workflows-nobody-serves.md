# Brainstorm — lens: niche: power-user and edge workflows nobody serves

- **Re-anchor pinned done-checks when their commit moves** — FIX — value 4 — effort S — risk low — category: task contracts
  Why: a finished task's criterion was pinned to 235932b8, which predated the test fix that moved build to e021641f, so the task had to be redone. Assumption: other tasks pin commits that go stale the same way.
  Done when: a task whose pinned commit is behind its branch's current head is re-pinned by a test, and its check reports "re-anchored" rather than failing.

- **Make local-time deferrals survive the DST fall-back** — FIX — value 4 — effort S — risk low — category: scheduling
  Why: `defer --until` now reads local time (T-1802), but a wall-clock 02:00 happens twice on fall-back and doesn't exist on spring-forward. Today's date is 2026-10-27, just after the European change, so this is live for some users.
  Done when: a fake-clock test across the 2026 fall-back resolves a deferral to exactly one instant, and a spring-forward test never lands in the missing hour.

- **Scope rules and budgets to subdirectories in a monorepo** — FEATURE — value 3 — effort M — risk med — category: monorepo scoping
  Why: the rules file is one global file, and it already went over its 6,400-char budget once (6,416). Assumption: a package's guidance spends the shared budget even when nobody is editing that package.
  Done when: a nested rules file loads only when an edit lands inside its directory, and the budget check counts only the files a given edit loads.

- **Make the gate lock hold on NFS, sshfs and WSL mounts** — FIX — value 3 — effort M — risk med — category: locking
  Why: the gate lock is machine-wide, and the state directory may sit on a network or Windows-mounted path. Assumption: `flock` can silently fail to exclude on those filesystems, so two full checks overlap without anyone seeing it.
  Done when: with the state directory on an NFS or sshfs mount, two concurrent full checks serialize, and the second one reports the wait.

- **Give tmux and shell prompts a one-line run status** — FEATURE — value 3 — effort S — risk low — category: terminal integration
  Why: assumption: power users put run state in `status-right` or their prompt, and the current output is too wide and colored for that.
  Done when: `fm status --line` prints at most 60 characters with no escape bytes when stdout is piped.

- **Stop escape codes leaking into dumb terminals and CI logs** — FIX — value 2 — effort S — risk low — category: terminal output
  Why: assumption: listings and the TUI assume a capable terminal, so `NO_COLOR` and `TERM=dumb` output carries escape noise into logs.
  Done when: `NO_COLOR=1 TERM=dumb fm status | cat` prints zero ESC bytes, and the same holds in CI.

- **Run a pre-push hook that gates only the pushed range** — FEATURE — value 3 — effort S — risk low — category: git hooks
  Why: `fm check --affected` exists, but nothing wires it to the commits actually being pushed. Assumption: a push touching one plugin subtree should not queue the full gate.
  Done when: pushing a branch that changes only `plugin/lib/` runs only the gates that cover that subtree, and the hook's log lists them.

- **Merge fm's state files with a git merge driver** — FEATURE — value 3 — effort M — risk med — category: branch merges
  Why: the backlog and journal are shared text files, and a merge of two branches that each close a different task needs hand resolution. Assumption: this recurs whenever parallel lanes land on main.
  Done when: two branches that each close a different task merge with zero conflict markers in the backlog file.

- **Replay any closed task in a throwaway worktree** — FEATURE — value 3 — effort M — risk low — category: reproduction
  Why: wild — `fm task prove` already shows a test failing without the change, but only at close time. Extending that to any closed task means a regression can be re-checked later without touching the working tree.
  Done when: `fm task replay <id>` creates a worktree at the task's base commit, runs its proof, and removes the worktree on exit, leaving the main tree unchanged.

- **Rebuild a lost run journal from git reflog and commits** — FEATURE — value 2 — effort L — risk med — category: recovery
  Why: wild — a run's work lives in commits and the reflog even if its journal is deleted. Assumption: a lost journal is rare but leaves the user with no way to see what happened.
  Done when: deleting a run's journal and running `fm code recover <id>` rebuilds a status with the same commits and gate results as before.

- **Drive a remote box's Foreman over SSH from a laptop** — FEATURE — value 2 — effort L — risk med — category: remote work
  Why: wild — assumption: some users run long queues on a home server and want to watch and steer them from elsewhere, without a local clone or the runs leaving that box.
  Done when: `fm remote status <host>` prints the remote queue and the active run's gate state, and no project files are copied to the laptop.
