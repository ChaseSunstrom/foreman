# Brainstorm — lens: sci-fi: the 2030 harness that repairs itself, orchestrates its own lanes on the cheapest capable model, starts work from events and schedules and forecasts the user's next request, worked back to what Python and Foreman can do today

- **Re-watch every self-fix until it holds** — FEATURE — value 5 — effort M — risk low — category: self-repair
  Why: T-2272 turns a recurring signature into a FIX task, but nothing in the pack checks that the signature stopped. Today the fix counts as done at merge.
  Done when: after a signal-to-fix task closes, `fm doctor` lists it as "watching" for N sessions and reopens it, with the new occurrences attached, if the signature returns.

- **Block self-repairs that weaken the guard** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: Mission 12 says every capability keeps the guard intact, and T-2252 shows the guard's command lists are edited by hand. A self-authored patch touching guard, hooks or gates should face the same lists.
  Done when: a self-repair that touches guard or hook files must pass a corpus of forbidden commands that stays blocked. A test patch that deletes one corpus entry is refused.

- **Probe one tier down on a sample of lanes** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: T-2291 escalates from history, so it learns where the cheap model failed but never where it would have sufficed. Assumption: a 1-in-N shadow run is affordable.
  Done when: `fm lane brief` occasionally assigns the next-cheaper model to a low-risk task and records pass or fail. The router's tier table changes on that evidence alone.

- **Classify why a lane stopped, then pick the matching recovery** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: Mission 8 §9 says "recovers stopped ones", and the steers separate usage-limit pauses, killed sessions and compaction. The pack shows lane brief and rm but no stop-cause handling.
  Done when: a killed test lane is labelled with one of {usage-limit, killed, compaction, conflict, red}. Each label runs its own action (wait, respawn from baton, rebrief, message builder, rerun) and the choice is logged.

- **Replay triggers against the last 30 days before the user says yes** — FEATURE — value 3 — effort S — risk low — category: self-triggering
  Why: Installs (timers, units) are queued for "one yes", and T-2276 only measures precision after the fact. The user would approve a timer more easily seeing what it would already have done.
  Done when: each queued install shows "would have fired N times, M of them on work you later dropped". The numbers come from the event log.

- **Give every installed timer an expiry that precision must renew** — SECURITY — value 4 — effort S — risk low — category: self-triggering
  Why: One yes installs something that runs unattended indefinitely. Assumption: unused triggers pile up the way stale deferred tasks have (T-0788 to T-0799).
  Done when: a unit installed through Foreman carries a 30-day expiry. It is renewed only if its trigger's precision stays above a floor, and otherwise `fm doctor` offers a one-command removal.

- **Score the predicted next request against the actual one** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: T-2290 predicts minutes and attempts, but Mission 3 asks for predicting the next request. The user's request log, steers and drops are a ready training set.
  Done when: at each new user request Foreman records its top-3 guesses for the one before it. `fm foresight` prints a hit rate, and drafting in lanes stays off below a threshold.

- **Turn a red CI run on main into a pre-briefed lane** — FEATURE — value 4 — effort M — risk med — category: self-triggering
  Why: The repo has a test workflow, and `fm ship` already files "Baseline red" tasks, filed twice under different command text before the dedupe caught it. An issue or CI watcher is Mission 8 §11.
  Done when: a failing workflow run creates one deduped FIX task with the failing log and last green commit attached, offered as a lane. A test with a simulated run covers it.

- **Charge each self-fix a deletion** — CLEAN — value 4 — effort M — risk low — category: lean
  Why: The lean ratchet only warns on growth, and Ship went red on the 6,400-char rules cap. Self-repair that adds rules will worsen this.
  Done when: a self-authored task that raises always-on chars must also name a removal of equal size, or `fm ship` refuses it.

- **Merge lanes in order and bisect when the result goes red** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: Mission 8 §9 includes merging, and the user steered "merge in mission order". Red-after-merge is already a router signal, so it is common enough to automate.
  Done when: after each lane merge the verify gate runs. On red, Foreman reverts to the last green merge and names the lane that broke it.

- **Wild: Give every failure signature a free antibody check** — FEATURE — value 4 — effort L — risk med — category: self-repair
  Why: wild. The 2030 version doesn't re-learn the same fault. Each fixed signature gets a zero-token regex or hook check, with a test and a 90-day expiry if it never fires.
  Done when: a fixed failure from the signal log is blocked at the earliest hook that sees it, with its test, and the check disappears after 90 quiet days.

- **Wild: `fm replay` reproduces a dead session with a stubbed model** — FEATURE — value 3 — effort L — risk med — category: observability
  Why: wild. Self-repair needs a reproduction, and killed sessions leave only a trail. Replaying recorded tool calls in a throwaway worktree would turn "it died somehow" into a failing test.
  Done when: `fm replay SESSION` re-executes the recorded calls without a model and reports the first divergence from the original outcome.

- **Wild: Push a one-tap yes/no to the phone for queued installs and merges** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild. The "one yes" for installs now waits for the user's next terminal session. Assumption: a local-first push channel such as ntfy self-hosted or a LAN web page can carry the yes safely.
  Done when: a queued install appears on the web UI over LAN with its diff and uninstall line. A tap grants it through a channel the model can't write to, and the grant is logged.

- **Wild: Dry-run tomorrow's predicted request overnight** — FEATURE — value 4 — effort L — risk med — category: anticipation
  Why: wild. Mission 3 asks to "draft it on spec in a lane". The 2030 version leaves a draft branch and a one-line "ready" note, only when the hit rate earns it. It runs under a separate, capped self-initiated budget that pauses when a user session starts.
  Done when: an idle-hours lane drafts the top prediction on a throwaway worktree within its budget. The morning summary says whether the draft matched the real request.

Next question: Which of Foreman's self-made changes (fixes, rules, timers, routing choices) has never been removed, and what would make one expire without the user noticing?
Next question: When the machine is idle at night, what is the one piece of work the user would be happiest to find done, and how would Foreman know without asking?
