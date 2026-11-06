# Brainstorm — lens: performance

- **Collapse the 15 skill listings into one router skill** — PERFORMANCE — value 4 — effort S — risk low — category: context cost
  Why: since 2.1.304 the skill list is re-sent after every compaction. Foreman's 15 skills are ~3,200 of ~9,600 chars, and the long session compacts the most (Foreman ~60% dearer, $0.095 vs $0.059). Assumption: the router can load the old bodies on demand without hurting the held rate.
  Done when: `fm doctor` reports the Foreman share of the skill listing at ≤ 800 chars, and the long-session benchmark's pass rate is unchanged at 6 of 6.

- **Infer bookkeeping from tool results so the model makes none** — FEATURE — value 5 — effort L — risk med — category: context cost
  Why: the pack says the long-session surcharge comes from bookkeeping calls and hook notes growing context faster. Step done, proof ran and file touched are all visible to hooks. Assumption: most `fm task step/ac/prove` calls can be derived from the Bash and Edit results already seen.
  Done when: a recorded 8-request session closes every task with ≥ 50% fewer `fm` Bash calls, and the same hidden tests pass.

- **Compact at task close, not mid-task** — FEATURE — value 4 — effort M — risk med — category: compaction
  Why: the misses were written after a compaction, and Foreman compacts more often. Compacting where the least live state exists, with the capsule already written, costs less and loses less. Assumption: Foreman can trigger or request compaction at that boundary, or lower the auto-compact window just before one.
  Done when: in the forced-compaction benchmark, ≥ 80% of compactions land within one turn of a task close, with cost and pass rate no worse.

- **Gate pull requests on offline token counts replayed from recordings** — PERFORMANCE — value 4 — effort M — risk low — category: cost regression
  Why: measuring cost needs paid model runs (the user cares about usage), and T-1231 cost parity is deferred for lack of a cheap signal. Hook notes, `fm` outputs and skill text can be counted from recorded transcripts with no model call. Assumption: recorded sessions for the long-session cases exist or can be saved.
  Done when: a CI step replays N transcripts, prints Foreman-added tokens per turn by source, and fails when the total grows more than 5% over the committed baseline.

- **Time-box Foreman's context tax per source in the pane and at close** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: nobody can say today where the +14% on Haiku goes. Assumption: sources can be tagged (hook note, `fm` stdout, skill listing, compaction note).
  Done when: `fm cost --tax` prints bytes and estimated tokens per source for the current session, and the numbers sum to the measured Foreman-added total within 5%.

- **Add an import-time budget per hook** — PERFORMANCE — value 3 — effort S — risk low — category: hook latency
  Why: `bench_hooks.py` measures wall time, but a slow import is the usual cause and is invisible there. Assumption: some hooks import modules they only need on rare paths.
  Done when: a test runs each hook with `python -X importtime` and fails if any imports a module outside its allowlist or exceeds its ms budget.

- **Skip the guard subprocess for provably harmless read-only calls** — PERFORMANCE — value 3 — effort M — risk high — category: hook latency
  Why: 2.1.304's `tool.check` hands the mod `e.isReadOnly`. The mod could decide in-process using the same compiled rule table, and fall back to the hook on any sensitive path pattern. The guard must never weaken: credential-read rules stay authoritative.
  Done when: the guard's full refusal corpus gives identical verdicts with the fast path on and off, and read-only calls on ordinary paths spawn zero hook processes.

- **Stop benchmark reruns early with a sequential test** — PERFORMANCE — value 3 — effort M — risk low — category: benchmark cost
  Why: `--runs 3` reruns on Sonnet and Haiku are the main spend. When pass and cost gaps are already clear, or clearly inside noise, more runs waste dollars. Assumption: the per-run variance is small enough on the spec suites for early stopping to trigger.
  Done when: `fm bench duel --sequential` stops at the first run where the decision rule is met, and the published figures state how many runs were used.

- **Decide compaction against fresh-session handoff by measurement** — PERFORMANCE — value 4 — effort M — risk med — category: long sessions
  Why: the compaction summary call plus rebuilt context may cost more than starting a new `claude -p` from the capsule at a task boundary. Foreman already writes capsules and handoff notes. This is a decision the benchmark can settle. Assumption: capsule restart preserves the pass rate.
  Done when: the long-session benchmark runs both modes and the page publishes cost, time and pass rate for each.

- **Wild: Reach hooks over a local HTTP hook to a warm daemon** — PERFORMANCE — value 3 — effort L — risk high — category: hook latency
  Why: assumption: current Claude Code supports HTTP-type hooks. A resident process avoids Python startup per event. Wild.
  Done when: p95 per-event latency in `bench_hooks.py` drops ≥ 3x with the daemon up, and killing the daemon falls back to command hooks with identical verdicts.

- **Wild: Teach the model a two-character note dialect once, in the cached prefix** — PERFORMANCE — value 3 — effort M — risk high — category: context cost
  Why: hook notes are re-read every turn, and a fixed glossary in the stable prefix would make each note a fraction of its size. Assumption: Haiku follows the glossary without a pass-rate loss. Wild.
  Done when: the Haiku long-session run with dialect notes uses ≥ 20% fewer note tokens at an equal hidden-test pass rate.

- **Wild: Run a budget-neutral "Foreman diet" automatically once cost exceeds plain Claude Code's recorded baseline** — FEATURE — value 3 — effort M — risk med — category: cost control
  Why: the user wants Foreman cheaper and faster, not just better. A governor that strips optional notes when spend per request passes the baseline keeps discipline on safety and proof and drops commentary. Assumption: notes can be ranked as required or optional. Wild.
  Done when: with the governor on, the long-session run's cost ratio versus plain Claude Code falls below 1.2x while the guard and proof gates still fire in every case.

- **Wild: Print a per-close "what discipline cost you" line** — FEATURE — value 2 — effort S — risk low — category: observability
  Why: the +10% is the sticking point on the page. Showing it beside the saved rework builds trust or exposes the leak. Assumption: tokens and seconds from the tax ledger are available at close. Wild.
  Done when: every task close prints Foreman's token and dollar overhead and the number of rework loops it prevented, matching `fm cost --tax`.
