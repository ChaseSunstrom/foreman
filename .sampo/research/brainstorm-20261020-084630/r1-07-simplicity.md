# Brainstorm — lens: simplicity

- **Fold the 15 skills into one router skill** — PERFORMANCE — value 4 — effort M — risk med — category: context cost
  Why: Claude Code 2.1.304 re-sends the whole skill list after every compaction. Foreman's skills are about 3,200 of the ~9,600 listing chars, paid again each time. The long-session run shows ~60% extra cost from compaction frequency (T-1231).
  Done when: the session skill listing carries one Foreman entry of 300 chars or less. The existing skill e2e tests still load every sub-skill body on demand, and the long-session benchmark's cost drops against the 1.2.40 baseline.

- **Ablate each component on the duel and ship only what pays** — PERFORMANCE — value 5 — effort M — risk low — category: measurement
  Why: Foreman costs +10–14% on small tasks and ~60% on the long session. The pack shows no per-component cost, so which hook, note or skill causes the growth is unknown. Haiku runs under dollar caps make this affordable.
  Done when: `fm bench duel --without <component>` runs on the spec suite. A table of Δpass, Δcost and Δtime per component is committed, and at least one component with no measurable benefit is removed or defaulted off.

- **Infer step and acceptance-criterion bookkeeping from the verify command** — FEATURE — value 4 — effort M — risk med — category: fewer turns
  Why: the long session shows bookkeeping calls inflate context, and the "fewer turns" work already shortened the verbs. The remaining step is zero model calls: a hook sees the criterion's verify command exit 0 and marks the criterion.
  Done when: a task with 3 criteria closes in a recorded session with no `fm task ac`/`step` call from the model. The ledger shows the same proofs, and a failing verify marks nothing.

- **Replace home-grown ask binding with the native `decider: "person"`** — CLEAN — value 4 — effort M — risk high — category: delete code
  Why: 2.1.304 lets a mod's `tool.check` require the permission dialog or a host callback, and refuses where nobody can be asked. That is the behaviour the process-identity and self-grant defences in recent commits (approvals answer only in the asking process) re-implement. Assumption: foreman-ui's mod API exposes it on the installed version.
  Done when: the name- and process-based approval code is removed or reduced to a fallback for older Claude Code. A test shows `claude --resume SID -p yes` still cannot resolve a pending ask, and the guard test suite is unchanged.

- **Report what each Claude Code release made redundant** — CLEAN — value 3 — effort S — risk low — category: obsolescence
  Why: Foreman was adapted to 2.1.301 while 2.1.304 shipped native changes (fork subagents default, subagent-after-Stop block, `decider`). Nothing flags Foreman code that now duplicates the host. Assumption: the release notes can be fetched or pasted.
  Done when: `fm doctor` compares the installed Claude Code version with the last adapted version and prints a short list of Foreman features whose behaviour the new release changes, each linked to a deletion brief.

- **Ratchet always-on context bytes per release** — PERFORMANCE — value 4 — effort S — risk low — category: budget
  Why: cost comes from what Foreman injects (preamble, hook notes, skill listing), and the evidence shows it growing. Only verb count is capped, not the characters injected.
  Done when: a gate measures the skill listing, preamble and median hook note characters on a fixture session. The release check fails if the total rises over the previous release without a `--because` that cites a benchmark.

- **Generate the Benchmarks page prose from the results file** — FIX — value 3 — effort S — risk low — category: single source
  Why: T-1246 says the site prose figures are hard-coded. The user's rule is that every claim must be measured, and the figures have already shifted between 1.2.38 and 1.2.40.
  Done when: changing a value in the results JSON changes every number in the page text on rebuild, and a test fails if a hard-coded figure is found in `site/` prose.

- **Make the core a five-hook install and everything else an `fm add` pack** — CLEAN — value 4 — effort L — risk med — category: footprint
  Why: the plugin has 1,560 files, 1,158 of them under skills. T-0794 (Lite mode) sits deferred. Packs make Lite the default rather than a mode.
  Done when: a fresh install writes only guard, plan-gate, proof, queue and stop hooks. `fm add audit` (or similar) enables the rest, and the duel passes with the core alone.

- **Merge all hooks for one event into a single dispatcher process** — PERFORMANCE — value 3 — effort M — risk med — category: hooks
  Why: `bench_hooks.py` is already a gate, and 2.1.304 limits prompt/agent hooks to 12 concurrent per event, so fewer entries per event is safer. Assumption: some events register several separate commands today.
  Done when: each event in the hooks manifest has at most one command. `bench_hooks.py` shows lower p95 per event, and the hook e2e roundtrip passes.

- **Wild: Ship the whole discipline as a 40-line CLAUDE.md for people who won't install** — FEATURE — value 3 — effort S — risk low — category: reach — wild
  Why: assumption: many users would try the plan, prove and one-task rules before accepting hooks. The duel shows what the rules alone are worth against the full plugin.
  Done when: `fm eject --snippet` writes a file of 40 lines or fewer, and the spec-suite duel reports its pass rate and cost next to plain and full Foreman.

- **Wild: Make "Foreman off" a measured baseline row on every page** — FEATURE — value 3 — effort S — risk low — category: honesty — wild
  Why: the pack shows both sides pass small tasks, so the page has to be honest about when Foreman doesn't matter. A permanent control row, with a rule that a Foreman feature must beat it to stay, would keep the product simple.
  Done when: every benchmark table includes a plain-Claude row from the same run, and a CI check fails if a published claim lacks one.

- **Wild: Self-deleting features — every flag and hook note expires unless its hit counter justifies it** — CLEAN — value 3 — effort M — risk med — category: sunset — wild
  Why: assumption: usage ledgers already count verb runs (`fm usage --prune`). Extending that to hook notes and flags lets the product shrink without manual triage.
  Done when: each hook note records fires and acted-on counts. After 30 days a note with zero acted-on hits is listed by `fm doctor` as an auto-captured deletion brief, and nothing is removed without a task.
