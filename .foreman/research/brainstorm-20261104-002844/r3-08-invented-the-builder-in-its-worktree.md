# Brainstorm — lens: invented: the builder in its worktree

- **Copy the untracked files a fresh worktree needs** — FIX — value 5 — effort S — risk low — category: worktree
  Why: assumption: the harness creates the worktree from tracked files only, so gitignored local config, hook settings and state pointers aren't there, which would explain evidence and lease verbs failing only inside it.
  Done when: a lane spawned in a fresh harness worktree has every file on a `.sampo/worktree-include` list, and `fm doctor --lane` reports none missing.

- **Fence edits to the assigned worktree** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: assumption: a builder that `cd`s or uses absolute paths into the main checkout edits the user's tree, and the lane's diff comes back empty or the main tree dirty. The guard already sees tool paths.
  Done when: an Edit or Write under the main root from a lane session is blocked with a line naming the worktree path, and a test proves it.

- **Say which Sampo code is running** — FIX — value 4 — effort S — risk low — category: self-hosting
  Why: when the repo is Sampo itself, the worktree holds `plugin/lib/sampo` while hooks and gates run the installed copy. A builder who edits a verb and then runs it can be testing the old code (assumption: this has already bitten).
  Done when: `fm which-code` prints worktree or installed for the hook path, the verbs and the test run, and the finish gate warns when they differ for a file the diff touched.

- **Keep a shadow ref of the worktree's work** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: the log has "WIP: T-2851 builder stopped; work kept by fm lane resume". If the harness deletes a worktree on exit, uncommitted work is lost. A snapshot pushed to the common git dir would survive.
  Done when: killing a builder and deleting its worktree still leaves `refs/sampo/wip/<lane>` with the last tool-boundary tree, and `fm lane resume` rebuilds from it.

- **Show base drift before the builder finishes** — FEATURE — value 3 — effort S — risk low — category: done-gate
  Why: assumption: a long-lived worktree branches from an old HEAD, so evidence proves the change on a base that no longer exists. That is a false-done route nobody has listed.
  Done when: `fm task finish` prints commits behind main and refuses "proven" if a touched file changed upstream since the base, with a test.

- **Detect which harness made the worktree** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: the project is not Claude-only, but worktree layouts differ by harness (assumption). One adapter table of path patterns, with a fixture per harness, would keep state resolution honest across them.
  Done when: fixtures for Claude Code, Codex, Gemini and plain `git worktree` each resolve the same state root, and an unknown layout prints "worktree flavour unknown" instead of failing.

- **Tile each builder in the pane** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: the pane has an Agents graph, but nothing there says where a builder is working. A tile showing worktree, base drift, last evidence age and lease heartbeat would make a stuck builder visible.
  Done when: each running lane shows those four fields in the pane and the web UI. A lane with a dead lease greys out within one tick.

- **Heal a failed verb through the parent, then log it** — FIX — value 4 — effort L — risk med — category: resilience
  Why: if a lane's state write is denied, retrying the call as the parent's relay lets the builder continue, and the failure goes into friction instead of the builder's context. (Assumption: the parent holds a socket or inbox.)
  Done when: with the write path chmod-denied, `fm evidence add` in a lane still lands the record via the relay, and a friction row names the denial and the route used.

- **Re-run a builder's closing call as the parent** — FEATURE — value 4 — effort M — risk low — category: done-gate
  Why: the evidence the builder claims is only worth something if the parent can reproduce it from the landed commit. This ties into the six false dones that nothing has caught.
  Done when: the merge step re-runs each cited evidence command on the merged tree in the main checkout, and any mismatch reopens the task with the diff of outputs.

- **Run a ghost builder through a harness worktree each night** (wild) — FEATURE — value 4 — effort M — risk low — category: drill
  Why: a scripted fake builder that starts a lane in a real harness worktree, writes evidence, takes and drops a lease, and finishes. Failures that only show in the worktree would be caught before a real task hits them.
  Done when: a nightly job exercises start, evidence, lease and finish in a real worktree, and a planted denial turns `fm doctor` red.

- **Overlay main's state read-only under the worktree** (wild) — FEATURE — value 3 — effort L — risk high — category: state
  Why: a union view, with reads from main's `.sampo` and writes to the worktree's upper layer, would let every verb work with no path logic. (Assumption: the sandbox allows it. The hardened kernel may not, so this needs a spike with 2 or more approaches.)
  Done when: in a lane, `ls .sampo` shows main's tasks plus lane-local writes, and the landing step folds the upper layer back.

- **Have a cold child read the builder's last 20 verb calls** (wild) — FEATURE — value 3 — effort M — risk low — category: black box
  Why: a per-worktree log of every `fm` call (resolved paths, exit code, cwd) that a tool-less child reads at close to decide whether the builder worked around a failure instead of reporting it.
  Done when: a planted worked-around verb failure is named by the child in the finish card, and a clean run reports none.

- **Warn when a worktree outlives its task** — CLEAN — value 2 — effort S — risk low — category: janitor
  Why: assumption: abandoned worktrees keep branches, locks and disk, and leases pointing at them confuse later resumes.
  Done when: `fm doctor` lists worktrees with no open task or live lease and offers a trash move, never a delete.

Next question: which `fm` verbs have a worktree-specific failure that happens silently (returns 0 but writes nowhere), rather than one that errors?
Next question: when the harness removes a worktree on exit, what does it keep, and is anything Sampo relies on in the part it discards?
