# Brainstorm — lens: bold bets

- **Cut a verb for every verb added, enforced at ship** — FEATURE — value 5 — effort M — risk med — category: lean ratchet
  Why: gen-0 §6 says each generation subtracts as much as it adds, yet 5 of 1219 cards are used and T-0794 "Slim Foreman" sits deferred. T-2503 only lists growth as pending. Assumption: a verb-retirement list can be derived from `fm burden --by-verb`.
  Done when: `fm ship` refuses a diff that adds a verb to the CLI table without removing or merging one, and a test with a planted new verb shows the refusal naming the candidates.

- **Make the SessionStart note a hash plus a delta** — PERFORMANCE — value 4 — effort S — risk low — category: context
  Why: the pack measures ~2k chars × 89 sessions, and context per reply averages 387k.
  Done when: a second session start in an unchanged repo injects under 200 chars, and a test compares the bytes.

- **Attribute every reply's context to its source** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: 387k per reply is reported, but nothing says how much is Foreman's own. "Lean" is unmeasured in the pack.
  Done when: `fm cost --by-source` prints bytes per injected block (note, lessons, steers, skills, MCP schemas) and sums to within 5% of the total.

- **Replay real guard decisions against every candidate rule change** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: core:interpreter-code-driving-foreman blocked 42× in 7 days, and 2 brief-guard false positives read a dict key and `.join(` as paths. Assumption: hook inputs are logged and replayable.
  Done when: `fm guard replay` over the 7-day log reports changed verdicts per rule, and the two false positives become corpus entries that pass.

- **Fix the brief-guard false positives with a real tokenizer** — FIX — value 4 — effort S — risk low — category: guard
  Why: the pack names a dict key and a `.join(` call misread as written paths.
  Done when: both strings, pinned as red-first tests, no longer block, and a corpus of known-bad writes still blocks.

- **Prove the guard fires on every surface with a deny-class matrix** — SECURITY — value 5 — effort L — risk med — category: coverage
  Why: the 61 empty cells mostly sit under Codex, Gemini, opencode, MCP, Desktop and headless. T-0337 shows Gemini's Stop isn't wired. Assumption: a destructive-command fixture can run through each harness adapter.
  Done when: `fm guard matrix` prints deny-class × surface with pass, fail or "unguarded, declared", and no cell is blank.

- **Fill each empty coverage cell from a probe's own output** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: the steer says a cell counts only when it names a concrete capability grounded in a file or a real gap, with no reused phrasing. Hand-writing 61 cells invites templating.
  Done when: each of the 61 cells cites a file path or probe command, and the sweep's duplicate-phrase check passes.

- **Cold-shelve unused stack cards** — PERFORMANCE — value 3 — effort S — risk low — category: lean
  Why: 5 of 1219 cards are used.
  Done when: cards unused for 90 days move to a cold index outside the load path, `fm lib show` still resolves them, and install size drops by a measured amount.

- **Wild: Prove leanness by an eject round trip** — FEATURE — value 4 — effort M — risk med — category: lean proof
  Why: assumption: "leaves no trace" is a claim no command shows (T-0794 mentions eject).
  Done when: install, run a task, eject in a scratch repo leaves a `git status` identical to the start.

- **Wild: Lean twin — same task with hooks off** — PERFORMANCE — value 4 — effort M — risk low — category: measurement
  Why: nothing in the pack shows what the weight earns. A paired run gives the real price.
  Done when: `fm exam lean` reports cost, time and pass rate for hooks on versus off on 9 or fewer scenarios, using the free arms only.

- **Wild: Plant a harmless forbidden command weekly to prove the guard is alive** — SECURITY — value 4 — effort S — risk low — category: guard liveness
  Why: a guard that silently stopped firing looks the same as a quiet week. Assumption: the guard can mark a canary as expected.
  Done when: the nightly tick runs the canary on each installed host, and `fm doctor` goes red if any host fails to block it.

- **Hook latency budget per event, enforced in CI** — PERFORMANCE — value 4 — effort M — risk low — category: hooks
  Why: p95 is 278 ms over 13533 runs, but gen-0 says it may not grow, and only `bench_hooks.py` guards it.
  Done when: CI fails when any event's p95 exceeds its stored budget by more than noise, naming the slowest module.

- **Show the guard's weekly save in plain words** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: 42 blocks in 7 days are a number the user never sees as value.
  Done when: `fm status` shows one line such as "stopped 42 risky commands, 2 were mistakes", and a test checks the false-positive count.

- **Wild: Hostile-week replay** — SECURITY — value 4 — effort L — risk med — category: red team
  Why: assumption: a week of real hook inputs plus child-written evasions finds guard gaps nobody hand-wrote.
  Done when: a tool-less child's evasion set runs through the guard, and each miss becomes a red-first test.

Next question: Which of the 61 empty cells can be honestly n/a by rule, and who is allowed to record that?
Next question: Does the hook-input log keep enough bytes to replay a guard decision, or is it already redacted past use?
