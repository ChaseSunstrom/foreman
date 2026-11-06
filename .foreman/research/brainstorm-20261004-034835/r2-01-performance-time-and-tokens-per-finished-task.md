# Brainstorm — lens: performance: time and tokens per finished task

- **Measure ceremony time per closed task from the ledger** — FEATURE — value 4 — effort S — risk low — category: perf telemetry
  Why: "31+ drive stops on a background reviewer", ~1–2 min idle per batch, and 2.0M of 4M subagent tokens, but no per-step wall/token breakdown. Existing ideas cover showing cost, not attributing it to a step. Timestamps already exist in events.jsonl (bg_done, waits). assumption: step start/end events are recoverable.
  Done when: `fm cost --by-step` on a finished task prints wall seconds and tokens for brief, edit, gate, review, wait, and the sum is within 5% of ledger span.

- **Collapse reviewer idle by splitting review into a fast and a slow lane** — PERFORMANCE — value 5 — effort M — risk med — category: review latency
  Why: Each batch waits 1–2 min on the reviewer. Run cheap deterministic lenses (pre-audit patterns, edge checklist) inline and in seconds, and send only the judgment lenses (intent, adversary) to the subagent, which runs while the next brief's plan is read. Differs from "park" and "overlap" ideas: it shrinks what must wait.
  Done when: on a replayed batch, the blocking time before the next step falls ≥50% and the same findings set is reproduced on the bench.

- **Memoize gate and verify results keyed by the content of the files they read** — PERFORMANCE — value 4 — effort M — risk med — category: gate caching
  Why: 704 tests at ~30 s run repeatedly per step and at close. Prior ideas cache by tree hash (all-or-nothing); this keys per command by a dependency set (files read, via a recorded import or trace), so an unrelated edit does not invalidate. assumption: tests can be traced cheaply with sys.settrace or coverage-lite.
  Done when: editing a file outside a test's recorded reads leaves its cached pass reused (`fm check` reports "reused 612/704"), and editing a read file reruns it.

- **Prefix-stable context packs for every child** — PERFORMANCE — value 4 — effort S — risk low — category: token cost
  Why: Many child runs (brainstorm lenses, audit lenses, research) get packs that differ at the front, defeating prompt caching. Put the large stable part (rules, project map, "built so far" list) first, per-lens text last, byte-identical across siblings. Beyond "order packs for cache reuse": a test asserts the shared prefix length.
  Done when: a test builds packs for five lenses and asserts a common prefix ≥80% of tokens, and child spend for a five-lens ideas run drops measurably in `fm budget`.

- **Cap the pack itself with a measured token diet** — PERFORMANCE — value 3 — effort S — risk low — category: token cost
  Why: This pack carries ~250 lines of prior ideas plus a growing "built" list. Each pass pays for all of it times N children. Keep only titles clustered, drop the verbatim repeats, and track pack tokens per pass.
  Done when: pack size for pass 7 is ≥40% smaller than pass 6 with the dedup check still rejecting a re-proposed idea.

- **Escalate verification by failure risk, not by tier** — FEATURE — value 4 — effort M — risk med — category: adaptive rigor
  Why: S/M/L tier sets ceremony, but the escapes ledger knows which kinds of changes slip past. Spend full lenses only on diffs touching code classes with past escapes (network, parsers, guard); a docs or test-only diff gets one lens. assumption: escape attribution gives usable per-path rates.
  Done when: a docs-only diff runs ≤1 lens, a guard diff runs all five, and bench shows no new escapes on replayed history.

- **Run fm hooks as a resident daemon** — PERFORMANCE — value 3 — effort M — risk high — category: hook latency
  Why: Every PreToolUse spawns Python, imports fmcore, fmguard, and reads state; on a long drive that is thousands of cold starts. A unix-socket server started on session start answers hooks via a tiny client. assumption: hook latency is measurable and noticeable; profile first. Must fail closed to the in-process path.
  Done when: median hook latency drops ≥3× in a benchmark and killing the daemon leaves the guard still enforcing.

- **Wild: Keep a "speed ghost" of the best prior run of each task type** — FEATURE — value 3 — effort M — risk low — category: pace benchmark
  Why: assumption: tasks of similar type have comparable shape. Show on the pane the fastest finished S/M FIX's step timings as a ghost lane, so slow steps stand out as a racer would see them. Wild.
  Done when: the pane shows ghost versus current elapsed per step for a task with ≥3 prior same-type closes.

- **Wild: Decide by token auction between the reviewer and the author** — FEATURE — value 3 — effort L — risk med — category: budget allocation
  Why: A fixed 4M subagent budget is spread evenly. Let each lens bid on expected findings per token from its track record, and fund the best bids first within the day's cap. Wild; ties to "score reviewer severity against escapes".
  Done when: on replayed history, the auction allocation finds ≥ the same confirmed issues using ≥20% fewer reviewer tokens.

- **Wild: Pre-warm the next brief while the current review runs** — PERFORMANCE — value 4 — effort L — risk med — category: pipelining
  Why: Review idle is dead time, yet the queue is known. Draft the next task's plan, map impact, and recall lessons into a read-only scratch brief during the wait, discarded if the review's findings change the tree. Wild but grounded in the 31 stalled drive stops.
  Done when: on a two-task queue, time from review start to the second task's first edit falls ≥60 s, and a review finding touching shared files invalidates the scratch cleanly.

- **Wild: Ship a "fm diet" that proposes which ceremony steps to skip, backed by ablation** — FEATURE — value 4 — effort M — risk med — category: ceremony pruning
  Why: Ceremony per task is unmeasured as to yield. Replay finished tasks on the bench with one step removed (a lens, a second gate run) and report time/tokens saved versus findings lost, so skipping is evidence-based. Combines the per-step telemetry with the bench.
  Done when: `fm diet` outputs a table of steps with seconds saved and bench regressions per step, and flags at least one step as "free to skip" or states none is.
