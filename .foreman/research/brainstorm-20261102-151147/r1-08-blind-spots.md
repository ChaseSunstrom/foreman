# Brainstorm — lens: blind spots

- **Census every context channel against the gauges that read it** — FIX — value 4 — effort M — risk low — category: observability
  Why: T-2667 found that `fm burden` missed SessionStart context delivered as `hook_success` stdout. The user had to ask for it. The question that would have caught it: "which channels can carry text into the model, and which gauge reads each?" Existing ideas cover write-only ledger fields, but not unread channels.
  Done when: a test lists the event types and fields in a recent real transcript, and fails on any that are neither read by a gauge nor on a named ignore list with a reason.

- **Print the armed stops at the start of every `fm run`** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: T-2669 added `--stall-usd`, T-2476-style pace and round-first are steers, and the budget cap exists. A user can't see which stops are live without knowing each flag. Class: protections that exist only if you know to ask.
  Done when: `fm run` prints one line naming each stop (budget, stall, pace, risk) as armed with its value or as off, and the receipt repeats the line.

- **Default the stall limit from the user's own median task cost** — FEATURE — value 3 — effort S — risk med — category: safety
  Why: `--stall-usd` is opt-in, so an unattended run on a fresh install has no progress-free spend stop. Assumption: the ledger has enough closed-task costs to take a median (fall back to off below a minimum count).
  Done when: with no flag, a fixture ledger with a known median stops a run at 3× the median since the last close and names the derived value in the receipt.

- **Add a no-yield spend stop to model-spawning fan-out verbs** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: T-2669 covers only the drive. `fm ideas`, cold-read retries and exam arms also spend with no closing event. Assumption: they have no equivalent stop today.
  Done when: a fake child that returns empty output makes each verb stop after N dollars with a message naming the knob, and a verb that returns useful output isn't stopped.

- **Run a pathological-input latency suite over every hook-path parser** — PERFORMANCE — value 4 — effort M — risk low — category: reliability
  Why: T-2668 found the guard hung at about n^4 on nested `$(` and was only found after a hang. The same class applies to the steer expander, `fm find`, `fm map` and the transcript and ledger line readers. Assertions count steps, not seconds, so slow CI doesn't flake.
  Done when: each parser has a table of 10 or more pathological inputs and a step-count bar, and a planted quadratic in each makes its test fail.

- **Route all dedupe through one similarity index** — CLEAN — value 3 — effort M — risk med — category: simplicity
  Why: T-2656 wakes a deferred task on near-duplicate capture, and several dropped ideas ("mostly built") were duplicates found late. Separate dedupe paths for captures, ideas, lessons and decisions will drift apart. Assumption: they currently use different matching code.
  Done when: capture, idea intake and lesson store call one module, and one fixture of near-duplicate pairs passes through all three callers with the same verdicts.

- **Backtest the grounding step on past drops** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: T-2659 says 3 of 4 slate items were already built, and five recent drops record "mostly built" or "exists". The grounding step is never scored against those known misses.
  Done when: a command replays the last 20 "already built" drops through the grounding step and prints how many it would have caught. A ratchet fails the ship gate if that falls below the stored rate.

- **Census protective flags that default off** — SECURITY — value 3 — effort S — risk low — category: safety
  Why: `--stall-usd`, `--pace off`, round-first and similar stops are opt-in or steer-driven. Nothing lists which protections are off right now.
  Done when: an `fm doctor` row names each protective setting that is off or unset, with the command that arms it, and stays quiet when all are armed.

- **Stamp the host CLI version on every hook ledger row** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: T-2667 shows the host's output shape changed what the gauges see. Without the host version on each row, a change in a gauge can't be tied to an upgrade. Assumption: the version is available in the hook payload or environment.
  Done when: new rows carry the host version, and `fm burden --by-version` splits injected characters by it.

- **(wild) Inject a canary through every context channel** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the empirical twin of the channel census. A fixture session sends a unique marker through stdout, `additionalContext`, `systemMessage` and a file read, then checks which gauges counted it.
  Done when: a fixture run prints a channel-by-gauge matrix, and an uncounted channel fails the test.

- **(wild) Run a timing-fuzzer child that is rewarded only for slowness** — SECURITY — value 3 — effort L — risk med — category: agents
  Why: T-2668's hang was found by hand. A tool-less child proposes inputs for a named function, the harness times them and keeps the worst, and each run seeds the pathological table.
  Done when: against a planted quadratic function, the loop finds an input at least 10× slower than the median within a fixed run budget, and files a task.

- **(wild) Show dollars since the last close as a live meter** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: the stall stop is invisible until it trips. A pane or status-line bar that fills toward `--stall-usd` and resets on each close makes progress-free spend visible.
  Done when: the status line shows the meter during `fm run`, resets on a task close, and turns amber at 80% of the limit.

Next question: for each gauge written in the last 30 days, which of the eight missed-ask classes would a cold child say it cannot detect, and is any of them cheap to close?
Next question: which Foreman-run unattended paths have a spend or time bound that exists only as a flag the user must have asked for?
