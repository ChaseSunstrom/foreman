# Brainstorm — lens: reliability

- **Quarantine flaky exam scenarios before they decide a selection** — FIX — value 5 — effort M — risk low — category: exam reliability
  Why: selection says a rewrite wins if it closes more scenarios, and scenarios run model-written code in 6 languages. One flaky scenario flips a winner. Assumption: no flake tracking exists today.
  Done when: running the oracle arm 5× on a fixture exam marks any scenario with mixed results as `quarantined`, and selection ignores it and prints the count.

- **Preflight the toolchains before a generation spends anything** — FIX — value 4 — effort S — risk low — category: hermeticity
  Why: the exam spans 6 languages. A missing `go` or `node` would read as a failed scenario, not an environment fault. Assumption: failures are not currently split into "env" and "behaviour".
  Done when: with `cargo` removed from PATH, `fm genesis` stops at preflight naming the missing tool and writes zero scored results.

- **Validate every child's output against a schema, and retry once on repair** — FIX — value 5 — effort M — risk low — category: child output
  Why: the tower depends on tool-less children writing a Seed, Missions and critiques. T-0831 notes capped `claude -p` children lose partial results. Malformed output entering tower storage poisons later generations.
  Done when: a child returning truncated or off-format Seed text is rejected, retried once with the parse error, and `put` never stores an unparsed doc. A test feeds three corrupted outputs.

- **Keep the tower off volatile storage and verify it on open** — FIX — value 4 — effort S — risk med — category: durability
  Why: the working directory is under `/run/user/1000`, a tmpfs that vanishes on reboot or logout. The steer already says tower files live only in genesis storage. Assumption: genesis storage is persistent but nothing checks that.
  Done when: `fm genesis init` refuses or warns if its storage path is on tmpfs, and `status` shows the storage's filesystem type.

- **Stamp tower files with a schema version and migrate on open** — FEATURE — value 4 — effort M — risk low — category: upgrade safety
  Why: Foreman changes weekly (2006 files, many commits a day). A tower that is three generations old and written by an older fm may not parse under newer code. Assumption: no version field exists.
  Done when: a fixture tower written by a frozen old version opens, migrates with a logged diff, and resumes. An unknown future version refuses cleanly.

- **Detect a queue that is dry because it is blocked, not finished** — FIX — value 5 — effort S — risk med — category: auto-start
  Why: the open work has many `blocked` and `deferred` tasks (T-0325, T-0335, T-1207). Auto-start on "queue empty" would fire on a project that is only waiting on the user.
  Done when: a fixture queue with only blocked/deferred items does not trigger auto-start, and one with nothing open does. The proposal states which case it saw.

- **Stop the tower racing with the loop, scouts and lanes on the same repo** — FIX — value 5 — effort M — risk high — category: concurrency
  Why: Genesis ships to main on every tower change (T-2090). Loops, lanes and `fm ship` also write main, and T-2073 shows rounds are already running. Two publishers can produce conflicting pushes or a half-exported site.
  Done when: a test runs a lane ship and a Genesis publish concurrently, and both end with a consistent `site/genesis` and a linear main, with no lost commit.

- **Make publish fail soft, with a retry queue and a visible lag** — FIX — value 4 — effort S — risk low — category: publish
  Why: the detached trailing publish can fail silently on a network or push conflict. Then the site page shows a stale tower while `status` says it is live.
  Done when: with the remote unreachable, the tower step still succeeds and `status` shows "publish pending: N changes". Reconnecting drains the queue in one push.

- **Pin an exam to its toolchain versions and re-validate on drift** — FIX — value 3 — effort M — risk low — category: exam stability
  Why: hidden keys and oracle results depend on compiler and interpreter behaviour. A system update (Arch rolling, kernel 7.2) can break old scenarios without any Genesis change.
  Done when: each exam records tool versions. A version change triggers an oracle re-run before any score from that exam is trusted.

- **Wild: Run a mutation-tested exam, so each scenario proves it can fail** — FEATURE — value 4 — effort L — risk med — category: exam validity
  Why: the empty and oracle arms prove only the two extremes. Assumption: scenarios can pass for the wrong reason. Planted off-by-one breaks in the solution should each flip at least one scenario.
  Done when: for a fixture project, a mutation run reports the share of mutants killed, and scenarios that kill none are flagged.

- **Wild: Keep a black-box flight recorder, so any crash replays in a sandbox** — FEATURE — value 3 — effort L — risk low — category: debuggability
  Why: unattended towers fail at 3am with no chat context. Recording child prompts, outputs, exit codes, timings and env facts would let a failed step be reproduced exactly.
  Done when: `fm genesis replay <step>` re-runs a recorded step against stored child outputs with no model calls and reaches the same decision.

- **Wild: Give the tower a canary project that runs nightly and pages on regression** — FEATURE — value 4 — effort M — risk low — category: self-test
  Why: Genesis is a feature of a harness that changes constantly. A tiny fixture project with a known gap set, run end to end, would show when a Foreman change breaks Genesis before a real project does.
  Done when: a scheduled run on the fixture closes its planted gaps, and a deliberately broken template makes the canary fail and report which stage.

- **Wild: Add a "same answer twice" check on the gen-0 writer** — FEATURE — value 3 — effort S — risk low — category: determinism
  Why: gen-0 is written from one line or nothing, and everything downstream inherits it. If two independent runs on the same project disagree on MUSTs, the draft is unstable.
  Done when: the writer runs twice, the MUST/NEVER sets are diffed, and any item not in both is marked unconfirmed in the output.

- **Classify every failed step as retryable, user-needed or fatal** — CLEAN — value 4 — effort S — risk low — category: error handling
  Why: the not-yet ledger and auto-start both need to know why something failed. A rate limit, a bad parse and a missing toolchain currently look alike.
  Done when: each tower step failure records one of three classes with a reason, and only retryable ones are retried automatically. A test covers one case per class.

Next question: What happens to a tower when the project's own tests, language or layout change underneath it between generations: which stored scenarios and claims go stale, and who notices?
Next question: Which Genesis failures would the user never see because they happen detached (publish, auto-start, overnight), and what is the one place they are guaranteed to look?
