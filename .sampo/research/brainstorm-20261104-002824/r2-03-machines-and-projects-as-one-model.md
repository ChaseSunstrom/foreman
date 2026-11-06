# Brainstorm — lens: machines and projects as one model

Lens: machines and projects as one model. Assumptions are marked; the pack shows the user's estate (a llama-swap server with ~3 min model switches, Ollama decision models, Arch/hardened kernel laptop, many Sampo lanes, the install vs source drift).

- **Keep one estate file joining machines, endpoints, models and repos** — FEATURE — value 5 — effort M — risk low — category: user model
  Why: the request is a model of "user, projects and machines"; the pack's endpoint (llama-swap, 3-min switch), Ollama profiles, Arch host and repos live in separate places. Assumption: no single file joins them today.
  Done when: `sampo estate --json` lists each machine with its endpoints, resident model, installed toolchain and the repos that use it, and a test fails if a profile in config is missing from it.

- **Order queued local-model work by resident model** — PERFORMANCE — value 5 — effort M — risk low — category: scheduling
  Why: a switch costs ~3 min and /running isn't relayed; the steer says use qwen3.8-27b first and switch late. Interleaved jobs waste minutes.
  Done when: given 10 queued drafts tagged with models, the planner emits at most one switch and a test on a fake endpoint counts it.

- **Check machine prerequisites before a task is picked** — FIX — value 4 — effort S — risk low — category: preflight
  Why: T-0325 (libappindicator), T-0418, blocked tasks, and the dropped shellcheck item all discovered missing host facts late. Assumption: tasks lack a `needs:` line.
  Done when: a task with `needs: libappindicator-gtk3` is shown as "blocked on machine X" by `fm next` without being picked, with the one-line fix.

- **Predict installed-vs-source drift per machine** — FEATURE — value 4 — effort M — risk low — category: drift
  Why: T-0418 (installed foreman-ui is old), rename shims, plugin ids moving; each machine's installed copy lags source differently.
  Done when: at session start a line says "installed 0.6.0, source 0.6.1 on this machine" and clears after update.

- **Learn which model passes which task kind on this machine** — FEATURE — value 5 — effort M — risk med — category: model routing
  Why: the steer is local models scaffolded to frontier results; ledgers already record closes per model. Join that with task kind to pick the rung per pair.
  Done when: `sampo estate fit` prints a pass-rate table by model × kind from the ledger, and the drive uses it to choose the first model on a held-out replay.

- **Plan the night as a machine-aware schedule** — FEATURE — value 5 — effort L — risk med — category: unattended
  Why: the user sleeps and wants progress by morning; resources (quota, endpoint uptime, disk, one GPU) are shared. Assumption: the drive plans by queue order only.
  Done when: at bedtime a plan file lists slots by machine and model, and the morning card shows plan vs actual per slot.

- **Probe the endpoint's state without waiting on it** — FIX — value 4 — effort S — risk low — category: endpoints
  Why: /running isn't relayed, so a switch can't be detected and costs 3 min blind. Infer residency from the last reply's model field and latency.
  Done when: after any call, the estate file records the inferred resident model with a timestamp, and a test using a recorded slow-first-token trace flags a switch.

- **Warn when a resource will run out before the night does** — FEATURE — value 4 — effort M — risk low — category: forecasting
  Why: quota, ledger growth, tmpfs under /run/user (this very working dir), disk. Combine machine and project growth rates.
  Done when: a synthetic ledger growing 10 MB/h on a 100 MB tmpfs produces a "full in ~10h" warning before the plan starts.

- **Move a fix to sibling repos on the same toolchain** — FEATURE — value 3 — effort M — risk med — category: cross-project
  Why: the same drive bug was fixed three times in a row (T-2873, T-2900, T-2901 area), and the user's repos share Python/Arch. Assumption: other repos exist beyond this one.
  Done when: after a FIX closes, a dormant brief is filed for each sibling repo whose search finds the same pattern, with the matching lines cited.

- **Gate drafts on the surface being in use** — FIX — value 4 — effort S — risk low — category: grounding
  Why: the carried gap "grounding checks the surface is in use" plus the dropped "premise already met" items.
  Done when: a draft brief whose named file or verb has no call in the last 14 days is flagged "unused surface" and not auto-filed.

- **Wild: Give each machine a one-line mood in the pane and status line** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the estate file gives enough signal. Mood like "jarvis: warm, 27b resident, 2 queued".
  Done when: the status line shows one mood string per machine that changes when the resident model changes.

- **Wild: Dry-run a placement on a clone of the estate** — FEATURE — value 3 — effort L — risk med — category: simulation
  Why: before the night, replay the plan against recorded latency and failure traces from the ledger.
  Done when: the simulator predicts the night's finished-task count within 30% on a replayed past night.

- **Wild: Ask the machines what they would like fixed** — FEATURE — value 3 — effort M — risk low — category: machine voice
  Why: each machine's own logs (journal, dmesg, ollama logs) hold complaints nobody reads. Assumption: readable without root.
  Done when: a morning list shows at least one filed brief per machine sourced from its own logs, each quoting the log line.

- **Wild: Grade the user-model against the user, weekly, using only the estate** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the model predicts next asks; score it against the week's real typed asks with a recency baseline, mute if it loses.
  Done when: a weekly line gives hit rate vs baseline, and the predictor mutes after a losing 30 days.

Next question: Which of the user's machines and repos actually exist beyond this one, and does any ledger already record the host on each row?
Next question: How often does a ~3 min model switch occur on a real night, and could the ledger answer that today?
