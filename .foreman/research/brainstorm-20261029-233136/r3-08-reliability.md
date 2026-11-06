# Brainstorm — lens: reliability

- **Grade infra failures as "ungradable", never as a loss** — FIX — value 5 — effort M — risk low — category: selection
  Why: the exam runs 6 languages across arms, and a rate-limit, timeout or missing toolchain currently looks the same as a failed scenario. A rewrite could lose or win on noise. Assumption: `fm exam grade` has only pass/fail today.
  Done when: a scenario whose runner is killed or whose toolchain is absent is recorded as `ungradable` with a reason. Selection excludes it from both sides, and a generation with more than 20% ungradable halts instead of choosing.

- **Run an oracle-and-empty health check before every grading pass** — FIX — value 4 — effort S — risk low — category: exam integrity
  Why: the oracle, empty and finders arms exist, but the canary is only listed for exam edits. A toolchain upgrade or a full disk can break the exam between generations without anyone editing it. Assumption: the arms can be run cheaply with no model calls.
  Done when: grading aborts with "exam unhealthy" if the oracle arm fails any scenario or the empty arm passes any. Tests inject each fault and see the abort.

- **Ratchet selection: a rewrite cannot reopen what its parent closed** — FIX — value 5 — effort S — risk low — category: selection
  Why: the rule "closes more scenarios than its parent" lets a child trade one closed scenario for two new ones and silently regress. This is the same shape as the dropped-steer problem.
  Done when: selection requires closed(child) ⊇ closed(parent) plus at least one new scenario. Otherwise the parent stays, and lineage records the reopened scenario ids. A test covers a child that wins on count but reopens one.

- **Run every child in its own process group, with a lease file and a reaper** — FIX — value 4 — effort M — risk low — category: process hygiene
  Why: the tower spawns tool-less `claude -p` children, lanes and exam runners, and a crash or timeout can leave orphans that keep spending quota. Assumption: children are not currently group-killed on timeout.
  Done when: killing the orchestrator with `kill -9` mid-stage leaves no child alive after the next `fm genesis` call, and the reaper logs what it killed.

- **Make the exam runner hermetic: pinned clock, locale, seed, no network, per-scenario timeout** — FIX — value 4 — effort M — risk med — category: exam integrity
  Why: scenarios run generated multi-language code from strangers, and any dependence on date, network or hash order makes pass/fail depend on when you ran it.
  Done when: running the same generation twice on a machine with the network disabled and the clock offset by a day gives identical verdicts. A planted time-dependent scenario is flagged as flaky.

- **Replay the tower end to end from recorded model outputs in the gates** — FEATURE — value 5 — effort L — risk med — category: testing
  Why: the e2e gates (`roundtrip.py`) can't cover Seed → missions → critique → selection → sweep without paying for model calls, so the orchestrator's glue goes untested. Assumption: all child output goes through one call seam.
  Done when: `python3 plugin/tests/e2e/genesis_tower.py` runs a full two-generation tower from a cassette with no network in under 60s. Altering a cassette step changes the lineage, and a missing cassette fails loudly.

- **Inject a fake clock into the orchestrator to test cooldowns and usage-reset waits** — CLEAN — value 4 — effort M — risk low — category: testing
  Why: auto-start cooldown, publish debounce, the stop-at-limit pause and the dead-man's switch are all time logic that only fails in production, days later. Assumption: they currently read the wall clock directly.
  Done when: tests advance a fake clock across a 5-hour reset and a 7-day cooldown in milliseconds, and each time rule has a boundary test.

- **Trip an auto-start breaker on Genesis's own failure rate** — SECURITY — value 4 — effort S — risk low — category: auto-start
  Why: a cooldown and a ceiling bound how often it starts, but not how often it fails. A project whose towers abort three times in a row keeps getting new ones. Assumption: aborts are recorded per tower.
  Done when: after N consecutive aborted or no-gain towers, auto-start stays off and proposes nothing. `fm genesis status` says why and what re-arms it.

- **Pin the Foreman code version for the length of a generation** — FIX — value 3 — effort M — risk med — category: version skew
  Why: Foreman ships changes constantly (about 20 commits in the pack alone, some touching `fm genesis`). A plugin update mid-tower could change templates or exam logic between the parent's score and the child's.
  Done when: each generation records the plugin commit and refuses to compare scores across commits. It either re-grades the parent or marks the comparison "cross-version" and does not select on it.

- **Never land over the user's live edits** — FIX — value 4 — effort M — risk med — category: concurrency
  Why: auto-start runs in the same repo the user works in, and `fm ship` replays lane commits onto main. Assumption: only a clean-tree check exists today.
  Done when: if a lane touches a file the user modified within the last N minutes or has uncommitted, the landing parks with a one-line reason. Nothing is overwritten, and a test covers the overlap.

- **Fuzz the one-line request until gen-0's MUST set holds still** — FEATURE — value 3 — effort M — risk low — category: gen-0 writer *(wild)*
  Why: "make this great", a typo version, a non-English version and an empty string should converge on the same core MUSTs. If they don't, the writer is following wording rather than the project.
  Done when: five paraphrases per fixture project give MUST sets with at least 80% overlap, and the diff is shown to the user when they don't.

- **Pick winners by quorum across two model families** — FEATURE — value 3 — effort L — risk med — category: selection *(wild)*
  Why: a single model both writes the rewrite and judges the critique, so one blind spot decides the outcome. Assumption: another CLI is available locally (the pack mentions blocked work on codex, gemini and opencode).
  Done when: a rewrite that wins on the exam but is rejected by an independent critic from another family is held as "contested". The user sees both sides before it becomes the parent.

- **Shuffle and parallelise scenario order to expose shared state** — PERFORMANCE — value 3 — effort S — risk low — category: exam integrity *(wild)*
  Why: if two scenarios share a temp dir, port or cache, results depend on order, and the held-out third is the likeliest place for that to hide.
  Done when: the grader runs each generation once in random order with parallel workers, and any scenario whose verdict differs from the serial run is quarantined.

Next question: What does the user see when a tower stops half-way and no session is open, and who notices, since nothing in the pack shows a notification path outside Claude Code?
Next question: Which of Genesis's steps write outside the repo (publish, ship, git push, `~/.claude`), and does each have an idempotency key and a way to undo it?
