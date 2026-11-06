# Brainstorm — lens: machines and projects as one model

- **Keep one estate file joining machines, models and repos** — FEATURE — value 5 — effort M — risk low — category: user-model
  Why: the pack shows a 27B on a server, a ~3 min llama-swap switch, Ollama models, an Arch box missing libappindicator, and installed-vs-source drift, each rediscovered by hand (T-0325, T-2893). The user-model should be one file: machine → endpoints → resident model → repos built there → known blockers.
  Done when: `sampo estate show --json` lists every registered machine with its endpoints, resident model and last probe time, and `fm next` reads it to name which machine a task needs.

- **Check a brief's machine needs before it is picked** — FEATURE — value 5 — effort S — risk low — category: anticipation
  Why: T-0325 and T-0418 sat blocked on a package or install that was knowable at filing. Assumption: a brief can declare `needs:` (package, endpoint, model, disk) that the estate file can answer.
  Done when: filing a brief with `needs: libappindicator-gtk3` on a machine without it prints "blocked by machine: sudo pacman -S …" at filing, not at pickup.

- **Order queued local-model work by the resident model** — PERFORMANCE — value 4 — effort M — risk low — category: scheduling
  Why: the steer says a llama-swap switch costs ~3 min with no detection. Unordered jobs could pay it repeatedly overnight.
  Done when: a queue with 6 jobs for two models issues exactly one switch, and the drive receipt shows the switch count.

- **Predict installed-vs-source drift per machine** — FIX — value 4 — effort S — risk low — category: drift
  Why: T-0418 (installed foreman-ui is behind), the rename to Sampo with shims, and the plugin-id migration all leave installed copies behind source. Assumption: the install generation is readable per machine.
  Done when: `fm doctor` names, per machine, the plugins whose installed version trails source, with the update command.

- **Learn which model passes which task kind on this machine** — FEATURE — value 5 — effort M — risk med — category: routing
  Why: the steers ask for local models scaffolded to frontier results and a model bench exists (T-2886, T-2887). Pass rates per (machine, model, task kind) from fm outcomes are not yet joined to routing.
  Done when: `sampo estate route <task-kind>` prints a ranked model list with n and pass rate, and returns "no data" when n < 5.

- **Warn when a resource will run out before the night does** — PERFORMANCE — value 3 — effort S — risk low — category: capacity
  Why: the user is asleep and wants major progress by morning; the pack lists growing ledgers and an unattended drive with a cost cap. Assumption: disk, quota and context are readable.
  Done when: before an unattended run, a one-line forecast "disk lasts N h, quota lasts N h" is printed and a shorter-than-planned horizon triggers a warning.

- **Probe an endpoint's state without waiting on it** — FIX — value 4 — effort S — risk low — category: local models
  Why: the llama-swap `/running` isn't relayed, so a switch can't be detected and the drive may block on a cold model. Assumption: a timing probe with a tiny prompt reveals which model is warm.
  Done when: the probe reports warm/cold in under 5 s and the drive skips a cold-model job when a warm-model job is queued.

- **Move a fix to sibling repos on the same toolchain** — FEATURE — value 3 — effort M — risk med — category: cross-project
  Why: the user has several repos (jarvis, sampo, a site); the same bug class (e.g. silent-cut scan, T-2884) likely recurs. Assumption: the estate file lists repos with stack cards.
  Done when: closing a FIX proposes, as dormant briefs, the same detector run on each sibling repo with the same stack card, and each carries its own Exam.

- **Rebuild the estate from probes on a new machine** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: the user's machines are several and the install is opt-in for local runtimes (Ollama, embedders). Assumption: probes (ollama list, /v1/models, nvidia-smi) cover most of it.
  Done when: running `sampo estate probe` on a fresh machine writes a valid estate file with no manual edits.

- **Dry-run a placement on a clone of the estate (wild)** — FEATURE — value 3 — effort L — risk med — category: simulation
  Why: wild. Before the night, replay the planned queue against recorded timings (3 min switches, endpoint outages) to say "this plan finishes at 05:40 with 1 blocked".
  Done when: `sampo estate plan --simulate` outputs a predicted finish time per task, scored against the actual run the next morning.

- **Give each machine a one-line mood in the pane (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The pane could show "server: qwen3.8-27b warm, 41% disk; laptop: idle". It makes the estate model something the user sees.
  Done when: the pane header shows one line per machine from the estate file and it updates within a minute of a model switch.

- **Ask the machines what they would like fixed (wild)** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: wild. Each machine's own logs (journal errors, failed units, SMART warnings, Arch update breakage) are an unmined source of tasks that the user would otherwise discover at the worst moment.
  Done when: a read-only scan files at most 3 dormant briefs per machine per night, each quoting the log line, and the user's drop rate on them is recorded.

- **Forecast Arch updates that break the gates** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: the machine is hardened-kernel Arch with missing packages and rolling updates. Assumption: pending package updates are listable and the gate suite can run in a scratch copy.
  Done when: before `pacman -Syu` is suggested, a dry-run reports which gates changed status in a scratch copy, or "unknown".

- **Grade the user-model against the user, weekly (wild)** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: wild. The estate and habit model make claims (which machine, which model, which repo comes next); settle each against what the user actually touched, and show hit rate in `fm doctor`.
  Done when: the weekly line "estate predictions: N made, M right" is printed, and a predictor below its recency baseline is muted.

Next question: Which facts about the user's machines are stable enough to cache in an estate file, and which must be probed live each time to avoid acting on stale state?
Next question: When the user's other machines are offline overnight, should the plan degrade to local-only work or hold the tasks for the morning?
