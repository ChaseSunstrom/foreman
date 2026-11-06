# Brainstorm — lens: reliability

- **Probe the browser sandbox before any shot or flow** — FIX — value 4 — effort S — risk low — category: provers
  Why: this host runs a hardened kernel (`7.2.10-hardened1`), which often disables unprivileged user namespaces, and that is what Chromium's sandbox needs. Assumption: `fm shot` and `fm flow` fail there with an opaque error, or silently fall back to `--no-sandbox`.
  Done when: with user namespaces disabled, `fm shot` prints one line naming the missing capability and the labelled fallback, and a test fakes the sysctl value to show this.

- **Attribute every flipped proof with a 2×2 matrix** — FEATURE — value 5 — effort M — risk med — category: attribution
  Why: when a proof goes green→red, nothing says whether the product or the prover changed. Assumption: the prover-version stamps and tree hashes already in the pack's ideas are recorded.
  Done when: a flip re-runs old/new prover against old/new tree in scratch copies and prints "product regressed", "prover regressed" or "environment/flaky", checked on three planted cases.

- **Write evidence first, then the verdict, as two phases** — FIX — value 4 — effort S — risk low — category: ledger
  Why: assumption: a crash between the verdict line and its artifact leaves a "proven" record pointing at nothing. The pack covers torn ledger tails, not this ordering.
  Done when: killing the writer at each step never leaves a verdict without a hash-matching evidence file, and a verdict whose artifact is missing reads as "unproven: evidence missing".

- **Lease ports, displays and browser profiles per concurrent run** — FIX — value 4 — effort M — risk med — category: concurrency
  Why: the pack covers private ports for race lanes only. Assumption: two parallel lanes or sessions running `fm flow` collide on the dev-server port or the Chromium profile lock and produce false reds.
  Done when: two simultaneous `fm flow` runs on one project both finish with correct verdicts, and a stale lease from a killed run is reclaimed.

- **Replace sleeps with a discovered readiness contract** — FEATURE — value 4 — effort M — risk med — category: flakiness
  Why: assumption: flows start before the app is ready, which is the classic flake source. A flow that passes only after a fixed sleep is a latent false green.
  Done when: `fm flow` waits on a health predicate found from the manifest or port scan, and it flags a flow whose pass depends on a sleep, shown by a fixture with a deliberately slow start.

- **Test that proof expiry fires** — FIX — value 4 — effort S — risk low — category: staleness
  Why: the pack proposes expiring proofs when covered files change, but nothing proves the expiry works. Assumption: a path-glob bug would let stale greens live forever.
  Done when: for a sample of closed proofs, touching one covered file in a scratch copy flips the proof to "expired", and an untouched control stays valid.

- **Check cache-key completeness by perturbation** — FIX — value 4 — effort M — risk med — category: caching
  Why: the pack proposes caching proofs by tree hash. Assumption: the key omits some input (prover version, env, locale, flags), so cached greens leak across conditions.
  Done when: changing each declared input in turn forces a cache miss, and a test fails when a new input is added without joining the key.

- **Cap verify attempts per task and escalate** — FEATURE — value 3 — effort S — risk low — category: loops
  Why: assumption: a flaky red makes an agent retry `fm prove` indefinitely, burning tokens and time. The pack has stuck-goal detection but nothing on proof retries.
  Done when: after N proof attempts with unchanged tree and identical verdict, the next one is refused with a classification (flaky, env or real) and the cheapest next step.

- **Label suspend and clock-jump runs "interrupted", not "timeout"** — FIX — value 3 — effort S — risk low — category: timing
  Why: assumption: a laptop suspend mid-proof is read as a prover timeout and recorded as a red or unproven for the wrong reason.
  Done when: SIGSTOP/SIGCONT or a faked wall-clock jump during a prover yields "interrupted, re-run" with a stated reason, and the wall/monotonic gap is the test oracle.

- **Shadow a new prover version beside the old one before promoting it** — FEATURE — value 3 — effort M — risk med — category: upgrades
  Why: the pack shadows hooks, but not provers. A prover upgrade is a silent change of what "proven" means.
  Done when: for N runs both versions emit verdicts, disagreements are listed, and promotion is refused below an agreement threshold.

- **Give provers error budgets and freeze the burnt ones** — FEATURE — value 3 — effort M — risk low — category: SLO
  Why: assumption: a prover that "could not run" a third of the time still looks fine because each failure is labelled unproven individually.
  Done when: `fm doctor` shows per-prover could-run rate, flake rate and p95 time against a budget, and a prover over budget is advisory-only until it recovers.

- **Wild: Prover roulette on another filesystem** — FEATURE — value 2 — effort M — risk low — category: portability
  Why: wild. Once a day, re-run one random closed proof blind, with the repo copied to tmpfs and to disk in turn, to catch proofs that only hold on one filesystem. `/run/user` here is tmpfs, so the assumption is that this class exists.
  Done when: a planted fs-dependent fixture proof (case-sensitivity or mtime based) is caught and named.

- **Wild: Degraded-truth drill** — FEATURE — value 3 — effort M — risk low — category: honesty
  Why: wild. Weekly, Foreman makes its own proof store read-only and its browser unlaunchable, then checks that the finish text says "unproven" rather than "proven".
  Done when: the drill passes on current code and fails when the Unproven footer logic is deliberately broken.

- **Wild: Prover autopsy capsule** — FEATURE — value 3 — effort S — risk low — category: debugging
  Why: wild. When a prover itself crashes (not the product), it auto-bundles argv, scrubbed env, versions and the last 200 output lines into a single file that a bug report can carry.
  Done when: a killed prover leaves a capsule under 100 KB with no secrets, and a stranger can replay it with one command.

Next question: which proofs has the user ever re-run by hand after Foreman said "proven", and what did they check that Foreman's prover didn't?
Next question: for each prover, what is the longest stretch it could have silently returned "could not run" without anyone being told?
