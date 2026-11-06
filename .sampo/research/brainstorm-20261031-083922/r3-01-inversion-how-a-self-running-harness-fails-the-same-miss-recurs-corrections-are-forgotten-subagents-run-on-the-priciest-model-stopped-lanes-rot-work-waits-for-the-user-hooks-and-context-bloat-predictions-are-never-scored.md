# Brainstorm — lens: inversion: how a self-running harness fails: the same miss recurs, corrections are forgotten, subagents run on the priciest model, stopped lanes rot, work waits for the user, hooks and context bloat, predictions are never scored

- **Prove the router's pick reaches the child's argv** — FIX — value 5 — effort S — risk low — category: orchestration
  Why: T-2291 built the history-based router, but a standing rule says a capability must be called by a real session path. Nothing in the pack shows the chosen model is what `fm lane brief` and `fm run` actually launch, so subagents may still run on the priciest model. Assumption: the launch command is built separately from the router call.
  Done when: a test spawns a lane with the router stubbed to "haiku" and asserts the child process's argv or env names that model. A mismatch fails `fm doctor`.

- **Print a failure-mode board with detector liveness in `fm doctor`** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: the lens lists seven ways a self-running harness decays (recurrence, forgotten corrections, pricey models, rotting lanes, waiting work, bloat, unscored predictions). Each has a partial feature, but no single view shows whether each detector has produced data lately. Assumption: some detectors are silent because nothing feeds them.
  Done when: `fm doctor` prints seven lines, each with a count and a "last fired" age. A detector with no input for 14 days shows red as "blind", not green.

- **Keep a correction ledger with coverage and latency** — FEATURE — value 5 — effort M — risk low — category: self-repair
  Why: the user's "asked" stream is full of corrections, and the missed-asks list shows repeated surprises. Nothing measures how many corrections ever got a check, or how long that took. Assumption: the latency is days for some.
  Done when: `fm corrections` lists each user correction with its linked check (or "none") and hours from correction to check. `fm doctor` warns when coverage falls below the last shipped value.

- **Normalise failure signatures before counting recurrence** — FIX — value 4 — effort S — risk low — category: self-repair
  Why: T-2272 triggers on a signature recurring across 3+ tasks. Signatures that embed paths, task ids, temp dirs or timings split one miss into many and never reach 3. T-2283's "same failure, deduped by command text missed it" is direct evidence.
  Done when: a test feeds the same failure with different task ids, paths and interpreter paths and gets one signature. The loop then files one FIX task.

- **Plant a canary recurrence weekly and time the loop** — FEATURE — value 4 — effort M — risk med — category: self-repair
  Why: nothing proves the signal-to-fix loop still works end to end. A loop that silently stops would look the same as a harness with no misses. Assumption: a scratch repo can host a planted, harmless repeat failure.
  Done when: `fm doctor` shows "canary filed a FIX in N hours" from the last weekly run. It warns if no FIX appeared within the window or the canary didn't run.

- **Measure the injection hit-rate per source** — PERFORMANCE — value 4 — effort M — risk low — category: context
  Why: the lean ratchet only stops growth. It can't tell which injected lines the model never used. Assumption: a quoted token, path or task id from an injected line appearing in later tool calls is a usable "was it read" signal.
  Done when: `fm doctor` ranks injected sources by uses per thousand characters. A source at zero over 20 sessions is flagged as a candidate to drop or load lazily.

- **Let the user approve queued yeses by editing a checkbox sheet** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: installs, merges and grants wait on "one yes", and work stalls while they wait. A plain-text sheet needs no new channel, and a file trigger can watch it. Assumption: editing a file is lower friction than answering a prompt in a stopped session.
  Done when: a queued install appears as `- [ ] ...` in `approvals.md`. Ticking it and saving executes it once and writes the result under the line. A line the model edited is ignored.

- **Drill every steer's check by deleting it in a copy** — CLEAN — value 3 — effort S — risk low — category: reliability
  Why: a standing rule says `fm doctor` names a missing check for each steer. No evidence shows that detection is tested.
  Done when: a test removes each steer's stored check in a temp state dir and asserts `fm doctor` names that steer. All steers pass.

- **Write a lane autopsy when a lane stops** — FEATURE — value 4 — effort M — risk low — category: orchestration
  Why: stopped lanes rot because recovery needs a model to work out what happened. The harness can capture last command, last error, diff stat, tokens spent and open criteria itself, without a model. Assumption: today that is reconstructed ad hoc.
  Done when: every stopped lane has `autopsy.md` written by code. A recovery lane's brief starts from it and cites it.

- **Watch lane progress by state hash, not wall time** — PERFORMANCE — value 3 — effort S — risk low — category: orchestration
  Why: an unattended lane can loop on the same edits and burn budget without ever "stopping". The stuck ladder covers steps in a task, not a lane overall. Assumption: no check compares successive task, diff and evidence hashes.
  Done when: a lane with no change in diff, evidence or task state across N tool calls is paused and filed with its last three actions. A test with a looping stub model hits this.

- **Share fixed signatures across projects as antibodies** — FEATURE — value 3 — effort M — risk med — category: self-repair
  Why: the same class of miss on another machine or project is rediscovered from scratch. The pack mentions machines and many projects. Assumption: failure signatures are stored per project.
  Done when: a signature fixed in project A raises a pre-flight note in project B. The note shows the fix commit and is silent once B has the fix.

- **Wild: Give a capability a tombstone and a resurrection condition** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: wild. Steers forbid killing ideas, yet predictors and triggers that lose to baseline cost hooks and context. A retired capability would keep a tombstone with its score history and the signal that would bring it back.
  Done when: a muted predictor leaves `tombstones/NAME.md` with its precision history and a revival test. Seed reads those files, and the revival test runs on each Seed.

- **Wild: Open each session with a one-line weather report** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: wild. Merge the detectors into a forecast such as "calm; 2 lanes rotting; usage wall near 15:00; 3 yeses waiting (about 11 min)".
  Done when: the first prompt of a session shows one line under 120 characters from the board's counts. It is silent when all are healthy.

- **Wild: Run a stub-model day to see what breaks when the cheap model drives** — FEATURE — value 3 — effort L — risk med — category: orchestration
  Why: wild. The router learns only from tiers it has tried. A scripted day with the cheapest tier driving every S task in a throwaway clone would fill its history with failures and flag tasks that must never go down.
  Done when: a run on 10 recorded S tasks writes per-task pass or fail for the cheap tier into router history. The router then escalates on those task kinds.

Next question: Which of the seven decay detectors has never been fed a real failure, so nobody knows it works?
Next question: When a self-fix or lane merge is wrong, how does the user find out, and how many days pass?
