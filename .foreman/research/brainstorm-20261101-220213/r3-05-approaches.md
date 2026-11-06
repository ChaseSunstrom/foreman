# Brainstorm — lens: approaches

- **Fill the 61 cells by probe, not prose** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the rule says a cell counts only if it names a concrete capability grounded in a file or a real gap; "Fill each cell from a probe's own output" is already floated but no single mechanism is chosen. Approach: one `fm lean probe CELL` per (stage × surface) that runs a real measurement (hook ms, injected bytes, guard verdict) and writes the cell from its output, so wording can't be templated.
  Done when: all 61 cells hold text containing a number or file path from a probe run, and `fm genesis sweep` reports zero templated or duplicated cells.

- **Mark n/a by rule with an expiring reason** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: many cells (e.g. "plan × site", "learn × Desktop") are plausibly n/a; the cheapest approach is to do less. Assumption: roughly a third are legitimately n/a. Each n/a carries a reason and a re-check date, and goes red if the surface later gains the capability.
  Done when: `coverage.md` n/a cells each have a reason and expiry, and a test turns one red when its surface gains a matching verb.

- **Reuse the guard corpus as the safety proof for every surface** — FEATURE — value 5 — effort M — risk med — category: safety
  Why: "core:interpreter-code-driving-foreman blocked 42x in 7 days" shows a real corpus exists. Replay logged guard decisions through each surface (MCP, headless, Desktop, fm code, other agents) and print a deny-class matrix; a surface that skips the guard shows as a gap rather than a vague cell.
  Done when: `fm doctor` prints a surface × deny-class matrix from replayed real inputs, and a deliberately unguarded surface shows red.

- **Fix the brief-guard false positives with a real tokenizer** — FIX — value 4 — effort S — risk low — category: guard
  Why: pack names 2 false positives reading a dict key and a `.join(` call as written paths. Approach: tokenize with a shell/Python parser instead of regex, and keep the two cases as a permanent corpus.
  Done when: both false positives pass, and a test with them plus 20 known true blocks passes.

- **Attribute injected context by source, then cap each source** — PERFORMANCE — value 5 — effort M — risk low — category: context
  Why: 387k context per reply and a ~2k-char SessionStart note repeated 89 times, with no breakdown of who contributes. Approach: tag each injected block, report bytes per source in `fm cost`, then give each a ceiling.
  Done when: `fm cost` lists bytes per injection source and a test fails when one exceeds its ceiling.

- **Inject the SessionStart note as hash plus delta** — PERFORMANCE — value 4 — effort S — risk low — category: context
  Why: ~2k chars × 89 sessions is a measured repeat. Do less: send the full note once per project state, then only changes.
  Done when: the second session start in an unchanged repo injects under 300 bytes.

- **Cold-shelve unused stack cards** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: 5 of 1219 cards used. Move cards unused for 90 days to a cold index loaded on demand; this pays for new growth through the subtract-as-you-add rule.
  Done when: the hot library has under 100 cards and `fm lib show NAME` still resolves any shelved card.

- **Budget the hook tail, with a per-event latency check in CI** — PERFORMANCE — value 4 — effort M — risk med — category: hooks
  Why: p95 is 278 ms over 13,533 runs, but only p95 is tracked and `bench_hooks.py` exists as a gate. Approach: extend it to p99 and per-event budgets, run under parallel lane load.
  Done when: CI fails on a synthetic 2× slowdown of one hook and the report names that hook.

- **Make a guard block teach the safe command** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: 42 blocks of one rule in 7 days means agents repeat the mistake. Each deny message includes the sanctioned alternative verb, so repeats drop.
  Done when: the top 5 block reasons each name an alternative, and the 7-day repeat count for the top rule falls versus baseline.

- **Wild: Eject round trip proves "leave no trace"** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: wild; the user wants Foreman lean and removable (T-0794 "eject" is deferred). Install, run a task, eject in a scratch copy, and diff the tree; the diff is the proof of footprint.
  Done when: the post-eject tree equals the pre-install tree except the user's own commits.

- **Wild: Run the exam with every optional hook off** — FEATURE — value 4 — effort M — risk med — category: lean
  Why: wild; the only honest answer to "does this weight earn its bytes" is ablation. Use the zero-token arms so it costs nothing, one hook disabled per run.
  Done when: a table shows each optional hook's exam delta, and any hook with zero delta is listed for removal.

- **Wild: Have a tool-less child invent the 61 cells blind, then diff** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: wild; steers prize signals Foreman didn't author. A child that never sees the code proposes each cell; disagreements with the probe-derived cell mark either an overclaim or a missed capability.
  Done when: a diff report lists each cell's agree/disagree, and each disagreement is filed or dismissed with a reason.

- **Pay for every new verb with a deletion** — CLEAN — value 4 — effort S — risk low — category: lean
  Why: gen-0 §6 says subtract as you add, yet T-2503 only handles growth after measurement. Approach: `fm task finish` refuses a diff that adds a verb without naming a retired or merged one.
  Done when: a test adding a verb with no retirement line fails the finish audit.

Next question: Which of the 61 cells describe surfaces (Desktop, site) where hooks don't run, so that "lean" has to be measured by page weight or idle CPU instead of hook milliseconds?
Next question: Does any guard rule exist only in Claude Code's hook path, so that fm code and other agents are silently unguarded today?
