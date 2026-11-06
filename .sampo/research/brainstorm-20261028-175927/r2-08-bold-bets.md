# Brainstorm — lens: bold bets

- **Replace the gate with a content-addressed proof cache shared across machines** — PERFORMANCE — value 5 — effort L — risk med — category: gates
  Why: assumption: repeated full gates, the hook bench flaking under load, and the 15-minute gate-lock waits all come from re-running checks whose inputs haven't changed. Keying each gate by tree hash and tool versions lets a second lane or laptop reuse a verdict.
  Done when: running `fm check` twice on an unchanged tree, the second run returns in under 2 s with "cached: tree <hash>", and changing one tracked file forces a real run.

- **Make every guard refusal self-healing** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: the round 5 review says the risk budget tripped (6 destructive blocks) mostly from the agent's own `$VAR` paths and `rm` on `/tmp` globs. The guard knows why it refused, so it can name the literal-path rewrite that would pass.
  Done when: a refused `rm -rf $DIR/x` prints a second line with the resolved literal command, and a replay of the 24-command corpus shows the suggested rewrite is allowed in every case where one exists.

- **Run the whole queue as one slash command with zero child processes** — FEATURE — value 4 — effort L — risk high — category: architecture
  Why: the usage-burn complaints, the capped `claude -p` children and the watchdog code all exist because headless children are costly and fragile. assumption: a native in-session loop with subagents avoids a separate process tree and its leases.
  Done when: `/foreman:queue` closes two tiny fixture tasks end to end in one session, and `ps` shows no spawned `claude -p`.

- **Quote and enforce a queue's cost before it starts** — FEATURE — value 5 — effort M — risk med — category: budget
  Why: the user said "I shouldn't have even had to tell you about the usage things". Today the defer-to-reset logic and `fm cost` exist but nothing predicts a queue's burn against the remaining weekly window.
  Done when: `fm run` prints the estimated tokens and dollars per task and the time to the reset, and refuses with a clear message if the sum exceeds the remaining headroom without `--force`.

- **Unify ticket sync: GitHub issues, in-place refresh, post-back on close** — FEATURE — value 4 — effort M — risk low — category: inbox
  Why: round 5 review says `fm inbox ticket` covers only Jira and Linear, makes a second brief on edit, and cannot link the commit back.
  Done when: `fm inbox ticket gh:owner/repo#12` creates a brief, re-running after an issue edit updates the same brief, and closing the task posts the commit link as a comment on the issue (against a recorded fake `gh`).

- **Ship `fm triage` as the single backlog entry with undo and a count** — FEATURE — value 4 — effort M — risk low — category: triage
  Why: four triage surfaces exist (first, swipe TTY, swipe --serve, app view I) with no router; swipe --serve has no undo or cards-left count.
  Done when: `fm triage` opens the right surface for TTY or browser, shows "n left", and pressing undo restores the previous card and reverses its verdict in the journal.

- **Serve every page from one `fm serve` hub with shared style** — CLEAN — value 3 — effort M — risk low — category: web UI
  Why: settings serve and swipe serve each use a one-shot token, Ctrl-C to stop, and duplicate style blocks; there are many scene, design and desk pages with no index.
  Done when: `fm serve` lists every servable page on one index at one loopback port with one token, and a test confirms no page embeds its own copy of the base stylesheet.

- **Report known-fix and playbook hit rates, and demote bad matches** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: T-1865 made matching safer, but nothing reports how often a known fix was offered, accepted or wrong, so a bad signature can persist unseen.
  Done when: `fm doctor` shows offered, accepted and wrong counts per signature, and a signature wrong twice stops being offered.

- **Wild: Replay the user's own words as a nightly "new user, old repo" rehearsal** — FEATURE — value 4 — effort L — risk med — category: self-test
  Why: wild; the user keeps finding failures (stdin-less `fm quiet`, midnight defer, CI-only crashes) that tests missed. A scripted persona driven by the last 30 real requests, run in a scratch clone, would find them first and file tasks itself.
  Done when: the nightly job runs in a scratch copy, and a planted regression (e.g. `fm quiet` ignoring stdin) is filed as a task by the next morning.

- **Wild: Reap a dead run's leases, gate lock and children as one unit** — FIX — value 4 — effort M — risk med — category: reliability
  Why: the open pain is edit leases that live 20 minutes after a run ends and a gate lock that blocks other windows. Tying all three to the run's process liveness with a heartbeat fixes the class, not the instances.
  Done when: killing a run with SIGKILL frees its leases and lock within 5 s, shown by a test, and `fm status` names no holder.

- **Wild: Keep a last-known-good Foreman install that takes over when the new one fails its first gates** — SECURITY — value 3 — effort L — risk med — category: recovery
  Why: wild; the plugin and CLI have drifted before (installed foreman-ui behind, parity gaps), and a broken update halts the whole queue. A pinned prior copy with automatic rollback means an update can't strand the user.
  Done when: a deliberately broken plugin update is rolled back automatically on the first failed self-check, and `fm doctor` reports "rolled back to X, reason Y".

- **Wild: Make the queue a git ref so any machine can pick up lanes** — FEATURE — value 3 — effort L — risk high — category: fleet
  Why: wild; lanes, worktrees and overnight work all run on one box, while the backlog already lives as files. Storing it on an orphan ref that syncs by push lets a second machine claim tasks by atomic compare-and-swap.
  Done when: two clones claim different tasks from the same queue with no double-claim in a race test of 50 attempts, and a push merges cleanly.

- **Serve a scene gallery with captions and a render-under-1s test** — CLEAN — value 2 — effort S — risk low — category: scenes
  Why: T-1846..1855 shipped many showpiece scenes with no index, no caption, and no render-time check.
  Done when: `fm scene gallery` lists each scene with a one-line caption, and the test suite fails if any scene takes over 1 s to render.

- **Report DESIGN.md tokens that no CSS uses** — FEATURE — value 2 — effort S — risk low — category: design
  Why: the round 5 review notes Figma/DTCG import is one-way and nothing checks that tokens are actually used.
  Done when: `fm design unused` lists tokens with zero references in the project's CSS, and a fixture with one dead token reports exactly that one.
