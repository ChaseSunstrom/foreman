# Brainstorm — lens: machines and projects as one model

- **Join machine and project into one `estate.json` graph** — FEATURE — value 5 — effort M — risk low — category: user-model
  Why: asks name machines, endpoints, models and repos together (llama-swap 3-min switch, jarvis endpoint, Arch missing libappindicator blocking T-0325), yet each fact lives in a different place.
  Done when: `sampo estate show --json` lists every repo, machine, endpoint and resident model with edges (repo→needs→tool, task→runs-on→machine), and a unit test fails if a blocked task's named dependency is absent from the graph.

- **Predict blocked-by-machine before pickup** — FEATURE — value 5 — effort S — risk low — category: anticipation
  Why: T-0325, T-0418, T-0336 are blocked by host facts (packages, CLIs not installed). Briefs get picked and then stall. Assumption: tasks can declare `needs:`.
  Done when: `fm next` marks a task "machine can't" with the missing item when a `needs:` probe fails, and skips it.

- **Order the night by resident model** — PERFORMANCE — value 4 — effort M — risk low — category: scheduling
  Why: the user steer says a llama-swap switch costs about 3 minutes, with no detection. Interleaved 27B and 35B jobs pay that repeatedly.
  Done when: a queue of 6 mixed-model local jobs runs with at most one switch, shown in the drive receipt.

- **Forecast the date each machine resource binds** — FEATURE — value 3 — effort S — risk low — category: capacity
  Why: ledgers and worktrees grow on tmpfs (/run/user/1000), and the quota windows are known. Assumption: disk and quota series are already readable.
  Done when: the estate view prints "tmpfs full in ~N days" from the last 14 days of growth, with a test on a synthetic series.

- **Learn which model passes which task kind on which machine** — FEATURE — value 4 — effort M — risk med — category: routing
  Why: the model bench exists (T-2886, T-2894) but its results are not keyed by task kind and machine for picking.
  Done when: `models.pick(kind)` returns the best-scoring local profile from bench rows, and falls back to the default with a visible reason when fewer than 5 rows exist.

- **Flag installed-vs-source drift per machine at session start** — FIX — value 4 — effort S — risk low — category: drift
  Why: T-0418 (installed foreman-ui is stale) and the rename leave old and new installs coexisting; the user hits these by hand.
  Done when: session start prints one line naming a machine/plugin whose installed hash differs from source, and is silent when they match.

- **Port a fix to sibling repos on the same stack** — FEATURE — value 3 — effort M — risk med — category: cross-project
  Why: the same lane-drive bugs recur (T-0575 → T-2873 → T-2901); the other repos share these toolchains. Assumption: a repo registry exists.
  Done when: closing a FIX proposes, as dormant draft briefs, the sibling repos with the same file pattern, with nothing touched.

- **Draft the predicted ask only if the machine can verify it** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: the carried gap says every brief's Exam must read live state; a draft whose Exam cannot run here is noise.
  Done when: the drafter dry-runs a draft's Exam on the estate and drops any draft that errors, counting the drops.

- **Wild: Give each machine a mood line in the pane** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user asks for fast glance status; assumption: the estate graph exists. A line like "jarvis: 27B loaded, idle 4m; laptop: fine".
  Done when: the pane header shows one line per machine from probes, and it turns hatched when a probe is stale.

- **Wild: Rehearse the top predicted task on a cloned estate** — FEATURE — value 4 — effort L — risk med — category: overnight
  Why: the user sleeps and wants progress by morning; a scratch worktree with the hard-hat fake estate (models stubbed) can catch problems before the real run.
  Done when: at 02:00 the top queue item runs in a scratch worktree, and the morning card says "rehearsal passed/failed: reason" with nothing landed on main.

- **Wild: Ask the machines what they'd like fixed** — FEATURE — value 3 — effort M — risk low — category: observation
  Why: journald, pacman logs and failed units are read-only signals Foreman did not author, matching the steer to use outside signals.
  Done when: `sampo estate hints` lists up to 5 findings (failed units, pending kernel updates, full disks) filed as dormant tasks with their source line.

- **Wild: Seal a night plan across machines, graded in the morning** — FEATURE — value 4 — effort M — risk low — category: forecast
  Why: the user wants major progress by morning; a sealed plan (which task, which model, which machine, expected stop reason) graded against the ledger calibrates anticipation.
  Done when: the plan is hashed before sleep, and the morning card prints planned vs actual with a hit count.

- **Warn when a request names things this machine lacks** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: asks like "port to a repo" or "run on codex" fail late when the CLI, repo or endpoint is absent (T-0335, T-0336).
  Done when: intake maps nouns in a request to the estate graph and prints "not on this machine: X" before filing.

Next question: which estate facts can be probed without waking the user's GPU or paying the 3-minute model switch?
Next question: does the user's trust in a prediction depend on the machine it ran on, such as laptop versus server, and is that recorded anywhere?
