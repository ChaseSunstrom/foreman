# Brainstorm — lens: bold bets

- **Run a pre-edit "test oracle" child that writes the failing test from the request alone** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: fm bench hides a commit's tests from the replay and scores fail-to-pass; Foreman's red→green check exists, but the executor writes its own tests and can fit them to its fix. Assumption: a tool-less `claude -p` child given only the raw request plus `fm map` signatures can produce a useful failing test for FIX/FEATURE tasks.
  Done when: `fm bench run` on 8 cases shows oracle-first tasks pass the hidden commit tests at a rate no lower than live, and the brief records the oracle test's path before any source edit.

- **Mine other harnesses' open issues into bench cases with a "which Foreman gate would have caught it" tag** — FEATURE — value 4 — effort M — risk low — category: benchmark
  Why: `fm bench build --commits` already builds cases from any repo's history, and the user asked to research what people want harnesses to do. Assumption: public fixed-issue commits with tests exist for several popular repos; fetching is limited to public https.
  Done when: `fm bench build --from-issues REPO` yields ≥5 validated fail-to-pass cases, each with a stage tag, and `fm bench show` lists them.

- **Add a skill-adoption trial: run an unrouted foreign skill on 3 bench cases before `fm next` names it** — FEATURE — value 4 — effort M — risk low — category: plugin compat
  Why: `fm next` routes installed skills by a cached index, but nothing shows a routed skill helps; routing is by keyword fit. Bench A/B with `--runs` and `fm bench gate` can supply the evidence.
  Done when: `fm plugins trial SKILL` writes pass/cost deltas to the capability index, and a skill failing `fm bench gate` is no longer named by `fm next`.

- **Make `fm evolve` target the routing table and stage hints, not only instruction files** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: the live evolve run rejected a sensible revision for +20% cost, so cost is the binding constraint. Assumption: STAGE_REFERENCE and hint wording are mutable in the same branch/gate flow.
  Done when: an `fm evolve --target stage-hints` run produces a branch with a bench comparison and either merges on a yes or records the rejection reason.

- **Compile a "preference judge" from the user's pushback and run it on every bench replay** — FEATURE — value 4 — effort M — risk med — category: evaluation
  Why: the user's words repeatedly push for fewer turns, quiet output and no commands handed to them; pass/fail on tests ignores all of that. The bench already records turns and cost per replay.
  Done when: `fm bench show` prints a per-case preference score (turns, handed-over commands, output length) derived from a file of checks, and `fm bench gate` can fail on it.

- **Add a planning "fork race": two cheap plan drafts, pick by recall-nearest past success** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: the idea list has pre-mortems and nearest-brief plans separately, but never a comparison of drafts. Assumption: the extra Haiku draft costs less than one failed step.
  Done when: for L tasks, the brief holds two plan drafts and a chosen one with a one-line reason, and bench cost on L cases is no worse.

- **Wild: Run a shadow-user soak where a child plays the user from their verbatim steers against a candidate build for a whole queue** — FEATURE — value 5 — effort L — risk med — category: self-test
  Why: the user's steers are consistent ("keep recursively improving", "don't stop"). Replaying the pack's verbatim requests as sequential prompts tests drive mode over a long run, where the friction (21 drive waits) appears. Wild.
  Done when: `fm soak` runs 5 queued prompts headless in a temp worktree and reports drive stops, stalls and cost per prompt.

- **Wild: Let Foreman export its gates as a standalone MCP server so a bare Claude Code gets "done needs evidence" without the plugin** — FEATURE — value 3 — effort L — risk med — category: interop
  Why: the user wants compat with "whatever"; an MCP surface lets other harnesses call `fm task done`. Assumption: stdlib JSON-RPC over stdio is enough. Wild.
  Done when: a bare `claude -p` with only this MCP server configured is refused when it calls `done` without evidence.

- **Wild: Evolve the user's request into a spec game: a child proposes three divergent interpretations, and the main thread picks by recall of past accepts** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: the latest asks are vague ("groundbreaking", "whatever it takes") and the last brainstorm went dry because ideas were small or already done. Wild.
  Done when: for a vague inbox item, `fm capture` stores three interpretations, with the chosen one justified by a named past accepted idea.

- **Wild: Keep a nightly "counterfactual ledger" that replays each day's finished tasks with the previous plugin version and reports who would have won** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: `fm bench` compares A vs B and cases build from history, but nothing runs this continuously to show the self-improvement loop is actually improving. Wild.
  Done when: `fm bench trend` prints per-version pass rate and cost over the last N releases, built from stored `fm bench run` results.
