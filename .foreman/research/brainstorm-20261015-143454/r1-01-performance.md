# Brainstorm — lens: performance

- **Sample hook latency from real turns, not only bench** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: bench_hooks.py runs synthetic payloads (20 runs); the pack shows "hook latency" ideas but no field-measured p50/p99 per event on the user's machine. assumption: no always-on per-event timing ledger exists beyond bench.
  Done when: after 50 real tool calls, `fm doctor --perf` prints p50/p95/p99 per hook event from recorded wall times, and flags any event over 150 ms p95.

- **Short-circuit every hook on a one-stat "is this a Foreman project" check before importing Python modules** — PERFORMANCE — value 4 — effort S — risk low — category: startup
  Why: plugin/lib has 50 modules and hooks spawn Python per event; "exit hooks in one stat call" appears only for non-managed projects as an idea, not a measured import-time budget. assumption: some hooks still import fmcli-sized trees before deciding.
  Done when: a test asserts `python3 -X importtime` for the PostToolUse hook in a non-Foreman dir loads under 15 modules and runs in under 25 ms.

- **Budget `fm` verb cold-start with a per-verb import-time table in CI** — PERFORMANCE — value 3 — effort M — risk low — category: startup
  Why: 108 verbs behind one entry; bare `fm`, `fm complete` and `fm --help` run on every shell keystroke/tab, so import weight is felt. assumption: `fm` imports many libs eagerly.
  Done when: CI fails if `fm complete` or bare `fm --help` exceeds 80 ms median over 20 runs, and the table is printed on failure.

- **Make the test suite itself fast: affected-first with a content-hash result cache** — PERFORMANCE — value 4 — effort M — risk med — category: gate speed
  Why: 155 test files; the gate `fm doctor`+roundtrip+bench runs on every task and round. `--affected` exists but a hash cache of unchanged-test results across rounds isn't shown as shipped (the tree-hash gate cache is only an idea).
  Done when: re-running `fm check` on an unchanged tree after a one-file docs edit finishes in under 10% of the cold time, with a line saying how many tests were cache hits.

- **Time-box and incrementalise `fm map` on large repos** — PERFORMANCE — value 3 — effort M — risk low — category: scale
  Why: the map covers 350 files here; user repos can be 50k. Round-4 shipped `fm check --affected` but nothing bounds `fm map` cost. assumption: map walks the whole tree each refresh.
  Done when: on a synthetic 30k-file repo, `fm map` completes under 3 s cold and under 300 ms warm via git-object-hash incremental updates, and prints "partial" past the cap.

- **Run recording-only hooks fire-and-forget** — PERFORMANCE — value 4 — effort M — risk med — category: hook latency
  Why: ledger and evidence recording sit in the synchronous PostToolUse path next to gating logic; only gating hooks need to block the turn. assumption: they currently run inline.
  Done when: bench_hooks shows PostToolUse added latency drops by ≥40% with recording moved to a detached writer, and a crash-injection test proves no ledger event is lost on a clean exit.

- **Cap per-turn injected context by token count and print the bill** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: round-1 shipped compact output, but injected preambles/whispers (STATE, Next, lessons) have no enforced byte budget visible to the user. assumption: injections vary with state size.
  Done when: a test fails if SessionStart or per-turn injection exceeds a declared budget, and `fm doctor` shows the measured tokens per event.

- **Speed up git calls with a single porcelain snapshot per hook turn** — PERFORMANCE — value 3 — effort S — risk low — category: git speed
  Why: seven `_git` helper copies imply repeated `git status`/`diff` spawns across hooks and verbs. assumption: multiple spawns happen per turn.
  Done when: tracing a PostToolUse turn on a 5k-file repo shows ≤1 `git status` spawn, and total git time drops measurably in bench.

- **Wild: Warm resident hook server with a thin shell shim, auto-fallback to cold Python** — PERFORMANCE — value 5 — effort L — risk high — category: hook latency (wild)
  Why: every event pays interpreter startup; a unix-socket daemon per project removes it. assumption: startup dominates hook cost.
  Done when: p95 hook latency falls under 20 ms with the daemon up, and killing the daemon leaves hooks working at cold speed with a one-line note.

- **Wild: Predict-and-prefetch the next gate while the model is still typing the edit** — PERFORMANCE — value 4 — effort L — risk med — category: gate speed (wild)
  Why: gates run only after the step ends, so the user waits on tests serially. Speculatively start the affected tests on the first edit to a linked file, discard if the tree changes again.
  Done when: on a seeded task, wall time from last edit to green verify shrinks by ≥50% and a changed-tree test proves stale speculative results are never accepted.

- **Wild: "Seconds Foreman added" line at every close, split into hooks, gates, idle and waiting-on-you** — PERFORMANCE — value 4 — effort M — risk low — category: transparency (wild)
  Why: rivals win on a light first touch; an honest, per-task overhead number turns the perf work into something the user sees and can compare against the "usual time" already shown in the pane.
  Done when: `fm task finish` prints one line like "Foreman added 41 s of 6 min (hooks 3 s, gates 33 s, waiting 5 s)" computed from the ledger, matching an independent sum in a test.

- **Wild: Warm hot-spare headless child for brainstorm and review fan-out** — PERFORMANCE — value 3 — effort M — risk med — category: child latency (wild)
  Why: `fm ideas` and reviewers spawn fresh `claude -p` children each time, paying startup and cold-cache cost before the first token.
  Done when: second and later children in one round start producing output at least 30% sooner than cold spawns in a timed comparison, with the spare reaped on exit.

- **Bound every regex and scan over tool output and big files** — PERFORMANCE — value 3 — effort S — risk low — category: stability
  Why: guard, scaffolding and secret scanners run on arbitrary command output (44 MB/month in Bash alone); one pathological pattern can stall a hook. assumption: not all scans have size or time caps.
  Done when: a fuzz test feeding 20 MB of adversarial text through each scanner finishes under 2 s each, with an over-cap scan degrading to head/tail with a recorded note.
