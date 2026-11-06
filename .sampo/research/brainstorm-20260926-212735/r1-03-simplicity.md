# Brainstorm — lens: simplicity

- **Measure and cap skill and rule size in `fm doctor`** — CLEAN — value 4 — effort S — risk low
  Why: The pack says skills are "long markdown" and rules sit at ~5.2k of a 6k cap, with the user's main complaint being token burn. Nothing enforces a per-skill budget. Mechanism: `doctor` reports chars per skill, and fails past a cap (assumption: ~3k each). Overflow moves into on-demand playbooks.
  Done when: `fm doctor` prints a size table and exits non-zero on an over-cap skill. Every shipped skill passes.

- **Add a trivial-S fast path with no ceremony** — PERFORMANCE — value 5 — effort M — risk med
  Why: One loop (capture → expand → ground → plan → …) runs for every request, and briefs carry frontmatter, steps, criteria and a log. Assumption: typo-sized changes pay the same overhead as real work. Mechanism: for S tasks with one scope file, auto-generate a minimal brief (one criterion, one verify command) and skip expand/ground/recall.
  Done when: a one-line fix completes in ≤ 3 `fm` calls, and the transcript token count from `fm cost` is at least 50% lower than the full-loop baseline.

- **Log command usage and prune what's unused** — CLEAN — value 3 — effort S — risk low
  Why: There are ~20 `fm` commands (`watch`, `serve`, `sync`, `docs`, `tidy`, `plugins`, …) over ~8,000 lines, and the user never runs commands. Retirement exists for playbooks and injections, not commands. Mechanism: a counter per subcommand in state, surfaced by `doctor`. Zero-use commands over N weeks become removal candidates.
  Done when: `fm doctor` lists per-command counts, and one flagged command is removed with the tests still green.

- **Render "Next" from one function for SessionStart and the per-turn note** — CLEAN — value 3 — effort S — risk low
  Why: Both surfaces emit the next action and procedure under different char caps (2,000 vs 400). Assumption: they are built separately and can drift. Mechanism: a single `render_next(cap)` with snapshot tests.
  Done when: one renderer is called from both hooks, and a snapshot test fails if they disagree on the action text.

- **Cap brainstorm pack size and default to 2 rounds** — PERFORMANCE — value 4 — effort S — risk low
  Why: `fm ideas` rounds "build on all ideas so far until dry", so packs grow every round and each `claude -p` re-reads them. Mechanism: dedupe by title before feeding a round and keep only the top-K ideas. Default to `--rounds 2`, and require an explicit flag for more.
  Done when: round-3 input is ≤ 1.5× the round-1 input in chars, and the idea set overlaps ≥ 80% with an uncapped run on a fixture.

- **Drop rule text the code gates already enforce** — CLEAN — value 3 — effort S — risk med
  Why: The rules sit at ~5.2k of 6k, yet `fm focus` and `fm task done` already refuse the same violations. The rules cost tokens every session and repeat what the gates say when they fire. Mechanism: diff each rule against the gate list and delete any covered by a gate's error message.
  Done when: rules shrink by ≥ 800 chars, and the eval suite shows no regressions in gate-related behavior.

- **Add a single-counter thrash nudge** — FEATURE — value 3 — effort S — risk low
  Why: The pack says nothing notices the same file edited 5×. A full detector is heavy, so use a per-file edit counter in PostToolUse state that emits one 1-line note at 5 edits and then stays quiet.
  Done when: a scripted sequence of 5 edits to one file yields exactly one note. The hook stays under 150 ms p95.
