# Brainstorm — lens: unspoken needs

- **Explain what each waiting task is waiting on** — FEATURE — value 4 — effort S — risk low — category: queue clarity
  Why: the steers put T-2462, T-2450, T-2444, T-2428 and T-2441 behind round 1 with `--round-first`, and `--pace off`, blocked and deferred states add more holds. Nothing names the active hold, so the user has to read the steers to know why a task didn't start.
  Done when: `fm why-waiting T-2462` prints the chain of holds (rule, condition, current state) and a test with two stacked holds shows both.

- **Give conditional steers a machine-readable release condition** — FEATURE — value 4 — effort M — risk med — category: steers
  Why: several steers are temporal ("until the end-of-run exam", "pause now, run again only at the end", "wait for round 1"). `fm decide --check` stores a check, but nothing says when the steer lifts, so a finished steer keeps constraining work. Assumption: these are stored as free text.
  Done when: a steer with `--until round-1-done` stops applying, and is marked fulfilled in `fm doctor`, once that fact holds in a fixture.

- **Run affected tests first at ship, full suite as the backstop** — PERFORMANCE — value 4 — effort M — risk med — category: ship speed
  Why: every push goes through `fm ship` gated by the full suite, with 404 test files under `plugin/tests/` and the `tests→src` map already in the project map. The user wants frequent pushes. Assumption: the full suite is the slowest step in a ship.
  Done when: `fm ship` reports the affected-test result before the full-suite result, and a deliberately broken module fails in the first phase in under a third of the full-suite time.

- **Cache cold-read verdicts by content hash** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: every tower file gets a Haiku cold read, then a Sonnet read on any non-pass, each time it is written. Rewrites that change only whitespace, or a re-file of the same text after a refusal, re-pay for an identical read. Assumption: such repeats happen.
  Done when: filing the same file twice makes one cold-read call, and any byte change makes a new one.

- **Store steers and criteria verbatim, and flag truncated ones** — FIX — value 3 — effort S — risk low — category: data integrity
  Why: many steers in the pack end in "…" mid-clause. If that is stored text rather than display, the checks derived from them rest on partial rules. Assumption: this may only be pack truncation.
  Done when: a steer longer than the display limit round-trips byte-identical from storage, and `fm doctor` WARNs on any stored steer ending in an ellipsis.

- **Map every MASTER.md clause to a test or exam line** — CLEAN — value 4 — effort M — risk low — category: proof
  Why: MASTER.md holds module clauses with task ids, and T-2546 already reads them to find work that is built. The repo claims proof before presentation, but a clause with no test is a claim with no proof.
  Done when: `fm doctor` lists clauses with no test reference, and adding one reference removes that clause from the list.

- **Predict file overlap before spawning parallel lanes** — FEATURE — value 4 — effort M — risk med — category: agent fleet
  Why: Missions 5-8 run as parallel `fm lanes`, merged in mission order. Briefs that touch the same module will conflict at merge, and the lane's work is thrown away. T-0792 and the blast-radius work show interest in fleet planning. Assumption: conflicts have occurred.
  Done when: two briefs naming the same file are put in one lane in order, two disjoint briefs run in parallel, and the plan prints the overlap that caused the serialization.

- **Ship a status-bar module instead of a tray icon** — FEATURE — value 3 — effort S — risk low — category: desktop surface
  Why: T-0325, the Desktop tray icon, has been blocked on `libappindicator-gtk3`. The host is Arch with a hardened kernel, which suggests a tiling-WM setup. A JSON line for waybar, polybar or i3status needs no extra package. Assumption: the user runs a status bar.
  Done when: `fm status --bar` prints one line of JSON (queue count, blocked-on-you count, red doctor count) in under 200 ms.

- **Budget each verb's cold-start time and import cost** — PERFORMANCE — value 3 — effort M — risk low — category: CLI speed
  Why: `plugin/lib` has 131 modules, and hooks are benchmarked (`bench_hooks.py`) but plain verbs such as `fm next` and `fm doctor` are not. Assumption: they pull in more modules than they need.
  Done when: `fm doctor --perf` prints wall time and imported-module count per top verb, and a test fails if `fm next` grows past its recorded budget.

- **Schedule work to resume when a usage limit lifts** — FEATURE — value 3 — effort S — risk low — category: unattended runs
  Why: the steer says to wait out real usage limits and resume where stopped. The user cannot see when the wait ends or what resumes. Assumption: the reset time is known from the limit error.
  Done when: while paused, `fm drive status` shows the reset time and the next task to resume, and the resume happens without a new command in a fixture with a faked clock.

- **Replay last month's tasks with one steer removed (wild)** — FEATURE — value 4 — effort L — risk med — category: steers
  Why: the user keeps adding steers and the pack never records what any of them cost. Ablation already exists for features (`fm bench duel --ablate`), but not for rules. Wild.
  Done when: `fm steer ablate N` runs a sample of finished-task scenarios with and without steer N and prints pass, cost and time deltas.

- **Keep a graveyard page of removed features and rejected ideas (wild)** — FEATURE — value 3 — effort M — risk low — category: memory, delight
  Why: the Genesis rule says an idea is removed only for proven harm or exact duplication, with the reason recorded, and subtraction tasks are coming. Without a visible record, a removed capability gets re-proposed. Wild.
  Done when: the site and `fm graveyard` list each removed item with its date, reason and the evidence that killed it, and `fm capture` of a near-duplicate links to its entry.

- **Pre-answer every `fm ask` from the user model and score the guess (wild)** — FEATURE — value 4 — effort M — risk low — category: user model
  Why: the user dislikes being blocked, yet Foreman still asks. A tool-less child can write a predicted answer to each ask. Once the user answers, the miss rate per question class is logged, which measures the user model on real decisions with no sealed-prediction ceremony. Wild.
  Done when: each `fm ask` stores a predicted answer, the real answer closes it as hit or miss, and `fm doctor` shows the hit rate by class once 10 are scored.

- **Rehearse a steer's check against the diff that would break it (wild)** — SECURITY — value 3 — effort M — risk low — category: rule checks
  Why: the rule "every steer becomes an automatic check" is only as good as the check. A tool-less child that sees only the rule text writes a minimal violating diff, and the stored check must flag it.
  Done when: for each stored steer check, a generated violating diff trips it, and any check that passes the diff is listed as likely vacuous.

Next question: Which of the user's recurring corrections are about wording and numbers inside Foreman's own task text, and could a lint have caught them before the user did?
Next question: What does the user wait for most per day: ship gates, cold reads, usage windows or review, and does Foreman record those waits anywhere?
