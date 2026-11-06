# Brainstorm — lens: machines and projects as one model

- **Keep one estate file of machines, endpoints, models and repos** — FEATURE — value 5 — effort M — risk low — category: model
  Why: the pack has facts about the machines in scattered places: llama-swap has no `/running` and a switch costs about 3 min, Arch lacks libappindicator, the installed foreman-ui is stale, and the uv env lives under `~/.local/share/sampo`. Predicting the next request needs all of these in one place. Assumption: no single file records them today.
  Done when: `sampo estate show --json` lists each machine, endpoint, model and repo with a `verified_at` timestamp and a probe command, and `fm doctor` names any fact older than 7 days.

- **Order queued local-model work by resident model** — PERFORMANCE — value 5 — effort M — risk low — category: scheduling
  Why: the steer says a swap costs about 3 min, so qwen3.8-27b is used for everything and the MoE only late. Mixed-model queues pay that cost repeatedly. Assumption: nothing reorders the queue by model yet.
  Done when: on a replayed queue with 3 models, `fm next` groups tasks by model and the replay shows fewer swaps than FIFO order.

- **Check machine prerequisites before a task is picked** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: T-0325 (needs libappindicator), T-0418 (needs the installed ui updated) and the dropped shellcheck item were all discovered late. A brief with a `needs:` line is checked against the estate file.
  Done when: filing a brief that needs a missing tool prints the exact blocker and the one user action that clears it, and the task never reaches a lane.

- **Predict installed-vs-source drift per machine** — FIX — value 4 — effort S — risk low — category: drift
  Why: T-0418 (installed foreman-ui is behind 0.6.1) and the rename (old and new plugin ids coexist) show installs falling behind. Compare each machine's installed versions with `HEAD` at session start.
  Done when: the session-start card lists "ui 0.6.0 installed, 0.6.1 in repo" and goes silent when they match.

- **Learn which model passes which task kind on this machine** — FEATURE — value 5 — effort M — risk med — category: local models
  Why: the standing steer is local models scaffolded to frontier results, and the Louhi model bench exists. A per-machine table of (task kind × model → pass rate, seconds) predicts the model to start with. Assumption: bench rows carry task kind.
  Done when: `sampo estate pick <task>` returns a model with its measured pass rate, and a held-out week shows the pick beating a fixed default.

- **Move a fix to sibling repos on the same toolchain** — FEATURE — value 4 — effort M — risk med — category: cross-project
  Why: the repo is Python, but the user also has jarvis-style repos. A gate or lesson learned in one repo predicts the same ask in another with the same stack card. This extends the existing ideas about gaps across repos.
  Done when: closing a FIX in one repo drafts a task, flagged as predicted, in each registered repo whose stack card matches and where `fm find` hits the same pattern.

- **Warn when a resource will run out before the night does** — PERFORMANCE — value 4 — effort S — risk low — category: capacity
  Why: children run under `/run/user/1000` (tmpfs) and the ledgers grow. Project disk, tmpfs and VRAM headroom against the queue's expected use and flag a run that would fail at 3am.
  Done when: before an unattended night the card prints "tmpfs 80% full in ~6h at current rate" with a cleanup command, and a test with a faked disk triggers it.

- **Plan the night as a machine-aware schedule** — FEATURE — value 5 — effort L — risk med — category: unattended
  Why: the user sleeps and wants major progress by morning. A plan assigns tasks to lanes, models and machines, avoiding swaps and quota cliffs, and is shown for a one-line veto before the user leaves.
  Done when: `sampo night plan` prints an ordered plan with estimated swaps and cost, and the morning card compares predicted with actual.

- **Probe the endpoint's state without waiting on it** — FIX — value 3 — effort S — risk low — category: observability
  Why: llama-swap's `/running` isn't relayed, so Sampo can't tell which model is loaded and may pay a blind 3-min swap. Infer residency from last-request model and latency, and record it in the estate file.
  Done when: the estate file shows "resident: qwen3.8-27b (inferred, 4 min ago)" and a test shows a wrong inference corrected by the next reply's model field.

- **Wild: Dry-run a placement on a clone of the estate** — FEATURE — value 3 — effort L — risk med — category: twin
  Why: assumption: moving a lane to the server would be cheaper, but nobody can ask that without trying. Replay the ledger against a modified estate (another model resident, another machine) and report the time and cost difference.
  Done when: `sampo estate whatif --model qwen3.6-35b` returns predicted swaps and seconds for the last week's queue.

- **Wild: Give each machine a one-line mood in the pane and status line** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user can't see the server or the GPU from the terminal. Show "jarvis: warm, 27B resident, idle 12 min" next to the work bar, with colour from the estate file.
  Done when: the pane shows each registered machine with a state and age, and an unreachable one reads "can't tell" rather than a stale green.

- **Wild: Grade the user-model against the user, weekly, using only the estate** — FEATURE — value 3 — effort M — risk med — category: prediction
  Why: assumption: predicting the next ask is easiest when the ask follows from a machine fact (a package arrived, a server came up). Seal each Sunday a list of "asks the estate implies" and score it against what the user typed.
  Done when: a weekly line reads "implied 6, user asked 2 of them" and a predictor below the recency baseline for 30 days mutes itself.

- **Wild: Ask the machines what they would like fixed** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: assumption: each machine's own logs (journald failures, OOM kills, swap errors) hold requests the user never typed. A zero-token scan turns repeated machine complaints into draft tasks.
  Done when: a seeded OOM in a test journal yields one drafted task citing the log line, with a never-again key.

Next question: which asks the user typed in the last month were really about a machine fact (a missing package, a model switch, a stale install) rather than a project fact, and can the estate file predict them?
Next question: when the estate file and reality disagree (stale fact, unreachable machine), does the user want a silent re-probe, a warning, or a pause?
