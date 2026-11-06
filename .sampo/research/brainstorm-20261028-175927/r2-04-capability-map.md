# Brainstorm — lens: capability map

- **Keep a living capability map with evidence per cell** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: Pillar 2 demands a have/half/lack map every round, but the pack shows it rebuilt by hand each time (this review is prose). Related ideas bind README claims to checks, but nothing stores the rows.
  Done when: `fm capmap` prints rows (tool, capability, have/half/lacks), each "have" cell links to a passing check or test, each "lacks" cell to an open task, and a "have" with no passing check is shown as "half".

- **Snapshot the public surface and gate breaking changes** — FEATURE — value 4 — effort M — risk low — category: compatibility
  Why: Assumption: with roughly 1,900 files and dozens of verbs, flags, env vars, config keys and JSON fields shipping each round, nothing stops a silent removal. Best-in-class release tools (api-extractor, cargo-semver-checks, oasdiff) all do this.
  Done when: `fm check surface` diffs a generated manifest against the last tag. Removing a verb or flag in a test fixture fails the gate, and an intended removal passes once recorded with a reason.

- **Refuse unparseable edits before they land** — FIX — value 4 — effort S — risk low — category: edit safety
  Why: `fm edit` block-form bugs (T-1213) and the review's "TypeError tracebacks" show edits reaching disk in bad shape. SWE-agent and Aider both lint at edit time. Assumption: the existing edit chokepoint can call stdlib parsers (`ast`, `json`, `tomllib`).
  Done when: an edit that leaves a .py, .json or .toml file invalid is rejected with file:line, and the file is byte-identical afterwards.

- **Add a boot-smoke evidence kind** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: Evidence kinds cover tests, screenshots and journeys, but "does the service start, answer and log no ERROR" is not shown. Assumption: no such kind exists today.
  Done when: `fm task prove --boot CMD --url URL` starts the command in its own process group, waits for the URL, scans the log for ERROR, then kills the group. It fails on a deliberately broken fixture app and passes on a good one.

- **Harden loopback servers against rebinding and CSRF** — SECURITY — value 4 — effort S — risk low — category: served pages
  Why: Swipe serve, settings serve, app view and about 11 new pages all bind localhost with a one-shot token, and the review notes each duplicates its own setup. A Host/Origin check is not mentioned anywhere.
  Done when: one conformance test requests every served route with a foreign Host header and a foreign Origin, and each is refused. A state-changing POST without the token is refused.

- **Infer import-layer rules and ratchet them** — FEATURE — value 4 — effort M — risk med — category: architecture
  Why: The deferred register.tsx split (T-0166) and the 300-line ratchet idea show structure drifting, but no layer check exists. ArchUnit and import-linter do this.
  Done when: `fm arch init` writes allowed-dependency rules from today's import graph, and a new forbidden import in a test repo fails `fm check`. Existing violations are grandfathered and can only shrink.

- **Mint a pattern rule from each fixed bug class** — FEATURE — value 3 — effort M — risk med — category: regression
  Why: Known-fixes (T-1865) match failures, not code shapes. Semgrep and ast-grep rules catch the second instance of the same mistake. Assumption: Python-first with stdlib `ast` is enough to start.
  Done when: closing a FIX with `--pattern` stores an AST rule, and `fm check` flags a planted second instance in a fixture.

- **Show failing-test locals as a digest** — FEATURE — value 3 — effort S — risk low — category: debugging
  Why: Assumption: failures reach the model as bare tracebacks. The crash-hygiene and test_help tasks suggest slow root-causing. pytest's showlocals and rr-style replay are the best-in-class reference.
  Done when: a failing gate prints only project-code frames with their local variable values, truncated to a byte budget, and a fixture failure shows the offending value.

- **Draft a Claude Code upstream bug report from a local repro** — FEATURE — value 3 — effort S — risk low — category: upstream
  Why: T-1217 (Claude Code paints the pane background #262626) and T-0337 (Gemini AfterAgent discards the answer) are blocked on upstream behaviour with no path to reporting it.
  Done when: `fm report claude-code T-1217` writes a redacted file with version, hook payload and minimal repro steps, and sends nothing.

- **Draft a postmortem when main goes red or a run is abandoned** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: Session start already sweeps for CI-on-main problems, but the knowledge dies with the task. Assumption: journal, git log and CI status are enough for a timeline.
  Done when: on a red main, `fm postmortem` writes timeline, cause, fix commit and a "catch it earlier" check to docs/, with each claim linked to a journal line or commit.

- **Import other agents' rule files at init** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: Assumption: repos adopting Foreman often carry .cursorrules, .clinerules, copilot-instructions or AGENTS.md. Export to other CLIs exists but import does not appear.
  Done when: `fm init` lists those files, merges non-contradicting lines into one budgeted ruleset, flags conflicts, and writes nothing without a yes.

- **Let ADRs carry a check that rejects violating diffs** — FEATURE — value 3 — effort M — risk med — category: docs, architecture — wild
  Why: Assumption: close-time decisions are logged but unenforced. A decision record with an attached command turns prose into a fitness function.
  Done when: closing a task with `--adr` writes docs/adr/NNNN.md with a check command, and a later diff violating it is refused with the ADR's title in the message.

- **Reimplement from the criteria alone to find ambiguity** — FEATURE — value 3 — effort L — risk med — category: requirements — wild
  Why: Acceptance criteria are written once by the same model that builds against them. Two independent builds disagreeing on an input is a cheap signal that a criterion is ambiguous.
  Done when: for a flagged task a second lane builds from the criteria only, and `fm task diverge` lists the inputs where the two outputs differ, each turned into one question.

- **Turn the user's manual poke at the app into a smoke script** — FEATURE — value 3 — effort M — risk med — category: proof — wild
  Why: Assumption: the user already curls or clicks the running app by hand, and that knowledge is never captured.
  Done when: a HAR or curl history, kept local, becomes a replayable script with status and body-shape assertions, with secrets redacted, that runs as a verify command.

- **Capture a rival CLI's output as the target for a "lacks" row** — FEATURE — value 2 — effort L — risk high — category: capability map — wild
  Why: Codex, Gemini and opencode are already detected as runners (T-0335/36), so a rival can be run on a fixture and stored as a golden transcript. Assumption: licence and ToS allow local comparison.
  Done when: a "lacks" capmap row can attach a rival transcript on a fixture, and the build task cites it as its done-check.
