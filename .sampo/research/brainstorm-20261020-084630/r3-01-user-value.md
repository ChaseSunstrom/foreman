# Brainstorm — lens: user value

- **Reconcile Foreman after /rewind, /clear and forks** — FIX — value 4 — effort M — risk med — category: continuity
  Why: assumption: Claude Code's rewind and fork change the conversation, but ledger state (ticked steps, active task, pending asks) doesn't follow. Long unattended sessions are the user's main use, so a stale "step 3 done" after a rewind would be trusted.
  Done when: a test that ticks 2 steps, simulates a rewind to before step 1, and starts the next session shows `fm state` flagging the 2 ticks as unverified and re-queuing their proofs.

- **Probe the installed Claude Code for facts instead of remembering them** — FEATURE — value 4 — effort S — risk low — category: compatibility
  Why: the pack says Foreman was last adapted to 2.1.301 while 2.1.304 added `decider: "person"`, a Stop rule and a compaction change. Builders know none of this from training. A generated `fm cc` sheet (version, mod API fields, hook limits) read from the installed binary and changelog would replace guessing.
  Done when: `fm cc --json` lists the installed version and the 2.1.304 items by name, and builder briefs cite it.

- **Detect CLAUDE.md rules that contradict Foreman** — FIX — value 3 — effort S — risk low — category: conflicts
  Why: assumption: users' CLAUDE.md files carry commit, test and planning conventions that clash with Foreman's injected notes, which costs turns and tokens. The pack shows one steer where a criterion named a test module that doesn't exist, which is the same kind of unseen mismatch.
  Done when: `fm doctor` on a fixture repo whose CLAUDE.md says "never run tests" prints the conflicting line with a one-line resolution.

- **Keep a measurement-spend ledger with a monthly cap** — FEATURE — value 4 — effort S — risk low — category: usage
  Why: the user's constraints say usage matters. They have asked for several benchmark runs and reruns (`--runs 3`, marathon, long session), each costing dollars.
  Done when: `fm bench` records each run's dollars, `fm bench spend` shows the month's total per claim, and a run that would pass the cap refuses without `--because`.

- **Pick the ceremony profile from repo maturity** — FEATURE — value 4 — effort M — risk med — category: cost
  Why: Foreman costs +10–14% on small tasks where both sides pass everything, and about 60% more in long sessions. A scratch repo with no tests or CI doesn't need the weight a protected-branch repo does.
  Done when: a repo with no tests/CI gets the light profile and one with CI gets the full one, each shown by `fm state`, and the duel records the cost of each.

- **Order the queue by value per dollar when the week's usage is scarce** — FEATURE — value 3 — effort M — risk low — category: queue
  Why: 30+ deferred "Later from…" briefs sit alongside L tasks like T-1231 and T-1207. When usage is short, finishing cheap valuable items first beats age or kind order.
  Done when: `fm next --budget $N` lists tasks that fit the budget, ordered by (user-steer evidence ÷ forecast cost), with the forecast shown.

- **Add a one-key "that was needless ceremony" complaint** — FEATURE — value 4 — effort M — risk med — category: feedback — wild
  Why: the user's steers are about cost and speed ("cheaper/faster"). Guard verdicts can already be marked wrong, but nothing records a turn spent on bookkeeping, and the cost is only seen after the fact on the Benchmarks page.
  Done when: `fm shrug` stores the turn's injected notes and the task shape, and after 3 shrugs for one note on one task shape that note is skipped, with `fm why` listing it.

- **Let leftover plan usage fund the backlog** — FEATURE — value 4 — effort L — risk med — category: usage — wild
  Why: pacing and thermostat ideas only slow work down. Usage that expires unused at the week's reset is wasted. Foreman could spend the slack on Haiku-capped benchmark reruns, deferred S briefs, or marathon-style gardening, behind the existing dollar caps and the guard.
  Done when: with a faked 40%-unused reading 6 hours before reset, the drive starts only capped, read-only-or-worktree tasks, stops at the reset, and leaves a receipt of the dollars used.

- **Audit the user's last ten hand-made commits on day one** — FEATURE — value 3 — effort M — risk low — category: onboarding — wild
  Why: adoption help so far is "what Foreman would do next". A retroactive view ("3 of your last 10 commits changed source with no test run; 1 would have been refused") shows value before the user trusts it with anything. Assumption: the value comes from using their own history.
  Done when: `fm audit --history 10` on a fixture repo prints per-commit findings (unproved writes, risky commands visible in messages) and writes nothing.

- **Show one cross-project "needs you" list** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: the user runs Foreman across several repos (Desktop, the mod, this repo), and each has blocked items, pending asks and user-only steps, such as the Arch libappindicator install for T-0325. Today these are visible only per repo.
  Done when: `fm inbox` run in any directory lists items from every registered project with the exact command to resolve each.

- **Warn before a request bundles unrelated work** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the long-session benchmark shows many sub-requests per prompt cost more after compaction. Grouping them by file area and order lets related ones share context.
  Done when: for an 8-request fixture prompt, the first-turn note proposes an order and groups, and each sub-request still appears as its own tracked item.

- **Ship a `--since-version` digest of what changed for this user** — FEATURE — value 3 — effort S — risk low — category: updates
  Why: releases landed about every few days (1.2.36 to 1.2.40). Users can't tell which changes affect their own habits. The usage log shows which verbs they touch.
  Done when: after an update, the first `fm` call prints at most 5 lines naming only changes that touch verbs the user ran in the last 30 days.

- **Explain the first-hour cost honestly at install** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the measured result is "same pass rate on small tasks, +10–14% cost; better on long sessions and safety". Saying that at install, with the numbers linked to the results files, sets expectations and matches "every claim must be measured".
  Done when: the install output prints those figures read from the results file (not hard-coded), and a test fails if the file is missing a figure.
