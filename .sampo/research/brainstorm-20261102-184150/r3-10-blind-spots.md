# Brainstorm — lens: blind spots

Each blind-spot ask I traced (T-2691/2693, T-2720/2724, T-2722, T-2729, T-2738) is Foreman's own bookkeeping disagreeing with itself. A record keyed too coarsely, a rule that assumes one state, a printed value the next verb refuses, a derived document drifting from its source. The questions and the missing ideas in each class:

- **Which dimension does this summary collapse?** (T-2691, T-2693)
- **Who consumes this printed value, and in what grammar?** (T-2738)
- **In which states does this rule fire, and which states does it never see?** (T-2722)
- **Where does the evidence live, and what was fixed before it ran?** (T-2720, T-2724)
- **Which document is the source and which is the copy?** (T-2729)

- **Define one stage predicate** — CLEAN — value 4 — effort M — risk low — category: state
  Why: T-2722 found `fm next`'s ship rule keyed on "idle" while the tower reported "genesis". Assumption: other rules still hold their own queue-empty tests.
  Done when: a test greps `plugin/` for ad hoc idle or empty-queue checks and finds none outside the `fm stage` predicate. Every printed rule is exercised across the full stage × unshipped-commits matrix.

- **Accept one id-list grammar everywhere** — FIX — value 3 — effort S — risk low — category: CLI
  Why: T-2738 printed an unblock command with space-separated ids, and the verb takes commas. Assumption: sibling verbs differ on lists too.
  Done when: every verb taking ids accepts comma, space and `T-1..T-3` forms. A test feeds each verb every form.

- **Name the grant on the ship line** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: `fm next` now names the ship step more often (T-2722), and a push needs a grant (the steer: "each push goes through fm ship").
  Done when: with no grant set, the ship line prints the grant command and not a bare "run fm ship". With a grant, it prints its remaining uses.

- **Sandbox moonshot kill scripts** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: kill_m02 rebuilds deleted modules from model output and runs their tests. Assumption: it runs in the user's checkout with their full environment.
  Done when: the script runs in a scratch worktree with an allowlisted environment and no network. A planted attempt that writes to `$HOME` leaves no file there.

- **Classify committed experiment outputs** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: T-2720's approach 2 keeps full script output in the repo, and `fm genesis live` publishes to main. Assumption: full output carries absolute paths, usernames or verbatim user words.
  Done when: a pre-commit check scans `bench/moonshot/*` output for home paths, the user's email and quoted-ask text. A planted `~` fails it.

- **Index exam-tail lines by run, agent and generation** — PERFORMANCE — value 3 — effort M — risk low — category: readers
  Why: T-2691/2693 made the tail keep one line per run, agent and generation, which implies a full-ledger scan on each read. Assumption: that scan is the slow path.
  Done when: the tail reader on a ledger 10× today's size stays under a recorded budget, with the number in the test. Output is identical to the full scan.

- **Profile `fm next` by line** — PERFORMANCE — value 3 — effort S — risk low — category: latency
  Why: each recent fix added a line (ship step, blocked-pile unblock, withheld items). Several of them probably call git (T-2722's "first-parent since refs/foreman/shipped").
  Done when: `fm next --profile` prints milliseconds and git calls per line. A ratchet test fails if the total rises more than 20% over its baseline.

- **Table seed rules against gen-0 clauses** — FIX — value 4 — effort M — risk low — category: tower
  Why: T-2729 found the seed's selection rule contradicting gen-0 §3 on #13.
  Done when: every rule sentence in a seed has a `rule → gen-0 clause → agree/extends/contradicts` row, built by a zero-token quoter plus a cold read. One planted contradiction turns a row red.

- **Report kill-verdict agreement** — FEATURE — value 3 — effort S — risk low — category: experiments
  Why: M-02 says "3 of 3 rebuilt, viable" from two blind attempts each, and M-12's verdict was confounded. Nothing says how often the same script gives the same verdict twice.
  Done when: each `bench/moonshot` result file records `agree: k/n` over reruns. The generated table shows it beside each verdict.

- **(wild) Leave-one-out the blind-spot bank** — FEATURE — value 4 — effort M — risk low — category: meta
  Why: the bank exists as a question list, but nothing measures whether it works. Hold out each of the 8 listed asks and see which bank questions would have caught it.
  Done when: `fm genesis` prints "caught k of 8 held-out asks" with the catching question per ask. A bank edit that lowers k is flagged.

- **(wild) Put an unshipped count on the watch** — FEATURE — value 2 — effort M — risk low — category: devices
  Why: five of the 20 listed asks are "Ship N commits", so shipping is the user's most repeated manual nudge. Assumption: a glanceable count would cut those asks.
  Done when: a local-only endpoint serves "N unshipped, grant yes/no" as one line. A phone or watch shortcut reads it with no cloud hop.

- **(wild) Run a pre-mortem on the next ask** — FEATURE — value 3 — effort M — risk med — category: meta
  Why: every miss here was a sentence of the form "X now names/keeps/joins Y". A tool-less child that sees only the last month of asks and the new brief writes the one-line correction the user will send.
  Done when: its guess is stored sealed and scored against the user's real next correction. The hit rate prints in `fm outcomes`.

- **(wild) Fuzz the doc pair with a contradiction court** — CLEAN — value 2 — effort M — risk med — category: docs
  Why: two cold children defend different documents (gen-0 vs a seed, MASTER.md vs the README), and a judge scores them. That catches contradictions text diffs miss.
  Done when: a planted contradiction is found in at least 4 of 5 runs, and no false hit appears on the unmodified pair.

Next question: which of the user's asks were corrections of something Foreman printed that nothing parsed, and which were corrections of something it never printed?
Next question: does each ask that prompted a rule or gauge change also record which surface (pane, web, `fm next`, status line) showed the defect first?
