# Brainstorm — lens: research frontier

- **Measure how much of the diff the evidence ran** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: Gates record pass/fail, but nothing shows whether the changed lines ran at all. The `-k a or b` verify that "ran no tests" (T-0342 area) is one case of this. Assumption: coverage tooling can be reached through `fm map` test links.
  Done when: `fm task done` lists changed lines that no recorded gate or evidence run executed, and refuses (or flags, per tier) a task where over a set share of them are uncovered.

- **Verify intermittent bugs statistically** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: The README's own example is "login times out on slow wifi", which is nondeterministic. One green run proves little, and the pack only shows flaky-gate quarantine as an idea. Assumption: FIX briefs can declare a repro command.
  Done when: for a task marked intermittent, Foreman runs the repro until a sequential test (e.g. SPRT) decides at a stated confidence, red before and green after, and records the run counts and bound as evidence.

- **Seed FIX plans with ranked suspect lines** — FEATURE — value 4 — effort M — risk med — category: debugging
  Why: `fm impact` and `fm why` find dependents and history, but nothing localizes a failure. Assumption: per-test coverage can be collected cheaply for Python and JS projects.
  Done when: a FIX task with a failing gate gets a "suspects" section ranking lines by spectrum-based scores. On a fixture of 5 seeded bugs, the real line ranks in the top 5 for at least 4.

- **Mine invariants from gate runs and check each diff** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: `fm oracle` works from the spec alone. Nothing learns what the code has always satisfied, such as return ranges, ordering, and never-null fields. Assumption: gate runs can be traced with light instrumentation.
  Done when: on a fixture project, a diff that breaks a mined invariant gets flagged before `done`, and the false-positive rate on 20 benign recorded diffs is under 10%.

- **Attribute outcomes to injected context by ablation** — FEATURE — value 5 — effort L — risk med — category: learning
  Why: T-0217 and the idea list score lessons by "recall preceded a pass", which is correlation. `fm bench` and `fm evolve` already replay tasks and ablate whole instruction files. Doing it per injected item (lesson, veto, rule) would give causal credit.
  Done when: `fm bench --attribute` replays N finished tasks with each injected item removed in turn, and writes a table of items whose removal changed the outcome. Lessons with no measurable effect are listed as prune candidates.

- **Fuzz Foreman's instructions and classifier with paraphrases** — FEATURE — value 3 — effort M — risk low — category: robustness
  Why: `fm evolve` ablates instruction files, but nothing tests whether classification and plans survive meaning-preserving rewording. Terse input like "fix the login timeout" and the `FIX:` form should give the same result. Assumption: classification can be replayed headlessly.
  Done when: a metamorphic suite rewrites 30 briefs (reorder, rephrase, typo) and reports the share whose type, tier or plan skeleton changes. The release gate fails above a set threshold.

- **Draft cheap, then verify strong** — FEATURE — value 4 — effort L — risk med — category: orchestration
  Why: The list has per-step model routing and racing, but not draft-then-verify at task level. A cheap lane's diff becomes the plan for a strong model, which accepts, patches or discards it, like speculative decoding. Assumption: the draft diff is cheaper to review than to write.
  Done when: on a bench set, draft-then-verify matches the gate pass rate of strong-only runs at lower measured cost (`fm cost`), and the accept/patch/discard split is reported.

- **Ask questions by information gain** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: The user keeps steering after the fact (budget limits only past 75%, cleanup never done). The listed ideas predict approvals and ask when sampled plans disagree, but none choose which question to ask or batch them. Assumption: `fm oracle` ambiguities can be turned into binary choices.
  Done when: for a queue of 5 ambiguous tasks, Foreman produces one batched card of at most 3 binary questions. Their answers are saved as spec and resolve at least 80% of the ambiguities in a fixture.

- **Perturb the environment inside smoke** — FEATURE — value 4 — effort M — risk med — category: product checking
  Why: `fm smoke` checks the product in a headless browser at two viewports, but only in a perfect environment. Faults like "slow wifi" are the kind that get reported. Assumption: a browser harness can throttle the network and skew the clock.
  Done when: `fm smoke --chaos` replays a journey under a seeded schedule of latency, offline and clock-skew faults. It reports which faults broke the journey and prints the seed to rerun it.

- **Detect stuck trajectories mid-run from ledger signatures** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: Past tasks mostly show the same retry loops. The "foreground wait loop" refusal and the idle-session fixes were each patched after the fact, one at a time. Assumption: the ledger has enough per-step events to train on.
  Done when: a detector trained on past ledgers flags a replayed looping run within N steps, at under 5% false alarms on healthy runs, and nudges the session once.

- **Wild: Regenerate a module clean-room and diff it** — FEATURE — value 4 — effort L — risk med — category: spec drift — wild
  Why: Foreman holds the briefs, decisions and tests for each area. Give an agent only those and have it rebuild a module in an empty directory. Every behavior the rebuild lacks, or adds, is something the specs failed to capture.
  Done when: `fm audit regen <path>` rebuilds the module, runs the existing tests against it, and lists behavior differences as proposed brief or test additions.

- **Wild: Auction the budget among lanes** — FEATURE — value 3 — effort L — risk high — category: scheduling — wild
  Why: The list has pace-based brokering. A market goes further: each lane bids its predicted value-per-token from past cost shapes, and spend flows to the best bidders. Assumption: bids can be calibrated against actual cost data.
  Done when: in a replayed week of tasks, the auction schedule finishes more high-value tasks than first-come scheduling at the same total spend.

- **Wild: Hold a "reviewer's duel" with hidden ground truth** — FEATURE — value 3 — effort M — risk low — category: review quality — wild
  Why: Canary bugs and reviewer weighting are listed separately. Combined, two reviewer configurations compete on diffs where a held-out bug was planted, and the winner's prompt is promoted through `fm bench`.
  Done when: a duel run reports each reviewer's catch rate and false alarms on 20 planted-bug diffs, and promotes the winner only if it beats the incumbent.
