# Brainstorm — lens: approaches

- **Replace the 15 skill entries with one router skill** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: Claude Code 2.1.304 re-sends the whole skill list after every compaction, and Foreman's 15 skills are about 3,200 of ~9,600 listing chars. Foreman already compacts more than plain Claude Code (~60% dearer in the long session).
  Done when: the Foreman entries in the listing total under 800 chars, `fm doctor` fails above that budget, and the long-session benchmark still passes every hidden test.

- **Record proofs from the PostToolUse hook, not from model calls** — PERFORMANCE — value 5 — effort M — risk med — category: turns
  Why: the pack says bookkeeping calls make context grow faster. The README promises "commands it actually ran", and the hook already sees command and exit code. Assumption: the hook can match a command to a criterion's verify string.
  Done when: running a criterion's verify command attaches the proof with no `fm task prove` call, and the turn count on the spec suite drops against 1.2.40.

- **Use `decider: "person"` for guard asks** — SECURITY — value 4 — effort M — risk med — category: approvals
  Why: 2.1.304 lets a mod's `tool.check` require the permission dialog or a host callback, and refuses where nobody can be asked. That fits the steer that chat approvals can't be self-granted. Assumption: foreman-ui's `tool.check` is where `fm ask` is wired today.
  Done when: a risky-but-allowed command in a non-interactive `claude -p` run is refused, in a TUI it opens the dialog, and a test covers both.

- **Compact at task close, not at the limit** — PERFORMANCE — value 4 — effort M — risk med — category: long sessions
  Why: the long-session misses cluster after compactions and the marathon hit 7 of them. A close is when the least live state exists. Assumption: a hook can nudge or request `/compact`, and the new idle-compaction setting can be recommended in `fm doctor`.
  Done when: in the 8-request long session, compactions land on task-close boundaries in at least 80% of runs and cost drops with pass rate held.

- **Fit the compaction window to a measured cost curve** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: `CLAUDE_CODE_AUTO_COMPACT_WINDOW` now takes k/M suffixes and validates its range. The benchmark forces compaction at 40k, but nothing shows what the best window is for Foreman.
  Done when: a sweep over three windows on the Haiku long session is published, and the best one is the default written by `fm doctor`.

- **Run brainstorm lenses as forked subagents of one cached pack** — PERFORMANCE — value 3 — effort M — risk med — category: ideas
  Why: fork subagents are on by default in `claude -p` and share the parent's prompt cache. Today each lens is a separate child that pays for the pack again. Assumption: forks inherit the pack but not the tools.
  Done when: `fm ideas` with 8 lenses shows lower input-token cost than the separate-child path and returns the same number of lens outputs.

- **Show Foreman's own token tax live** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the user wants Foreman cheaper, and the 60% long-session gap is unexplained per source. Hook notes, bookkeeping calls and skill listings need separate numbers.
  Done when: `fm tax` and the pane print tokens by source (notes, `fm` calls, skills) for the current session, and the numbers sum to within 5% of the transcript's measured overhead.

- **Generate site prose figures from the results files** — FIX — value 3 — effort S — risk low — category: docs
  Why: T-1246 says site prose figures are hard-coded, and "every claim on the site must be measured". The 1.2.40 rerun already shifted several numbers.
  Done when: editing a results JSON changes the prose figures on rebuild, and the site build fails if a figure in the prose has no source.

- **Prove the headless drive under the 2.1.304 Stop rule** — FIX — value 3 — effort S — risk med — category: compat
  Why: a plugin can no longer keep a headless run going past Stop or `--max-turns` by spawning subagents. Foreman's unattended drive and the marathon must not rely on that. The pack doesn't say whether they do (assumption).
  Done when: an e2e test runs the drive under `claude -p --max-turns` and shows it ends cleanly or resumes via the queue, never through subagent keepalive.

- **Make the macOS CI job portable** — FIX — value 2 — effort S — risk low — category: CI
  Why: T-1249 says the macOS job is red, and the badge sits at the top of the README. Assumption: the cause is GNU-only tools or paths, not logic.
  Done when: the macOS job is green on two consecutive pushes, and a lint step flags GNU-only flags in `plugin/`.

- **Wild: Move bookkeeping into a Haiku sidecar** — PERFORMANCE — value 5 — effort L — risk high — category: cost
  Why: the main context grows because task steps, proofs and notes all pass through it. A sidecar process owns the task state, takes one-line messages and returns a single status line. Assumption: the main model only needs the status line plus the verdicts.
  Done when: the long-session benchmark shows context growth per request at or below plain Claude Code's, with hidden tests still 6 of 6.

- **Wild: Hold a duel at an equal dollar cap** — FEATURE — value 4 — effort M — risk low — category: benchmarks
  Why: the user wants "better and cheaper", but equal-task duels only show that Foreman costs 10-14% more. Cap both sides at the same spend and score hidden tests passed per dollar.
  Done when: `fm bench duel --cap 0.10` runs both sides to the cap and the Benchmarks page lists passed-per-dollar with all runs shown.

- **Wild: Deliver notes on demand instead of pushing them** — PERFORMANCE — value 4 — effort L — risk high — category: context
  Why: hook notes add to every turn. If the model sees only a one-line pointer and fetches the note with `fm note N` when it matters, the per-turn cost falls. This tests whether the discipline survives without pushed text. Assumption: Sonnet and Haiku will fetch reliably, which the benchmark must show.
  Done when: in the Haiku spec suite, pass rate matches the pushed-notes baseline while injected bytes per session drop by at least 40%.

- **Wild: Add a no-Foreman control lane to every release check** — FEATURE — value 3 — effort M — risk low — category: honesty
  Why: the site stakes claims on measured results, and a single plain-Claude-Code run per release on the same tasks would catch drift in both Foreman and the baseline when Claude Code changes (2.1.301 to 2.1.304).
  Done when: `fm release-check` runs one plain-CC pass beside Foreman on the spec suite and writes both results to the bench log, with a warning if the baseline moved by more than the run-to-run spread.
