# Brainstorm — lens: research frontier

- **Inject lessons at the action, not the session** — FEATURE — value 5 — effort M — risk med — category: learning
  Why: assumption: lessons and `fm recall` are mostly loaded at session start or on request, and the idea pile has rule-retention probes and half-lives but no action-time retrieval. A PreToolUse hook could match the pending Edit or command to linked lessons, vetoes and decisions (via `fm why` and `fm map` links) and add only those, once.
  Done when: editing a file with a linked lesson surfaces that lesson exactly once in the hook output, and a 5000-command replay shows no added hook latency beyond the `bench_hooks.py` budget.

- **Mine contrastive lessons from paired attempts** — FEATURE — value 5 — effort L — risk med — category: learning
  Why: assumption: the ledger holds first-time passes and rework on similar tasks (T-0217 scores lessons, but only from single outcomes). Pair a failed and a successful attempt on similar briefs, diff their action sequences, and propose the differing step as a lesson. Keep it only if bench replay improves.
  Done when: on a fixture ledger with one planted fail/pass pair, `fm friction` emits a lesson naming the differing action, and `fm bench` accepts or rejects it.

- **Cross-examine the builder before done** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: reviewers and debate exist, but reviewers read the diff passively. A reviewer asks the builder pointed questions ("what happens when X is empty?"). Each answer must cite a command output or line range, and unanswered or uncited answers become findings.
  Done when: a seeded diff with an unhandled edge case yields a finding from an uncited answer, while a clean diff passes with every answer anchored.

- **Turn landscape findings into bench-gated experiments** — FEATURE — value 5 — effort L — risk med — category: self-improvement
  Why: `fm landscape` finds what people want and `fm evolve` tests instruction revisions, but nothing connects them. A finding such as "plan-then-verify prompts help" would become a candidate evolve branch, run on `fm bench`, with the result written back to the landscape.
  Done when: `fm landscape --experiment N` creates an evolve branch from finding N and records its bench delta against the baseline in research/.

- **Run sequential randomized trials of instruction variants** — FEATURE — value 4 — effort M — risk low — category: experimentation
  Why: the pile covers shadow runs and pre-registered experiments, but small live samples are noisy. Randomly assign a variant per task and stop with an anytime-valid sequential test, so a change ships, or is dropped, as soon as the evidence is enough.
  Done when: a simulated stream of 200 tasks with a planted 15% effect stops early and ships the variant, and a null stream does not ship it at the 5% error rate.

- **Distil the minimal sufficient trajectory into a playbook** — FEATURE — value 4 — effort L — risk med — category: learning
  Why: assumption: finished tasks carry many exploratory steps. Replay a task with each step ablated (the bench replay machinery exists), keep the smallest sequence that still passes the gates, and offer it as a playbook skill for that task class.
  Done when: for a recorded 30-step fixture task, the tool outputs a shorter sequence that passes the same gates, and `fm usage` shows the playbook registered.

- **Compile decisions into executable constraints** — FEATURE — value 4 — effort M — risk med — category: governance
  Why: `decisions.md` is prose, and the pile has revisit triggers and an import-graph gate but no general bridge. A decision such as "no new top-level commands" would carry a small checkable predicate (Datalog-style over the repo facts from `fm map`) that is run on every diff.
  Done when: `fm decide --check "<predicate>"` stores a rule, a diff violating it blocks done with the decision id, and one satisfying it passes.

- **Measure Foreman's time horizon** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: the pile has an outside-score idea and a model-upgrade exam, but no horizon curve. Group bench cases by wall-clock or step length and report the longest length with 50% first-time pass, per model and plugin version, so the user can see whether discipline extends the reach of the model.
  Done when: `fm bench --horizon` prints a pass-rate-by-length table for two plugin versions from the same case set.

- **Share lessons with differential privacy** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: `fm share` and outbound scanning exist, but a lesson that survives redaction may still identify a project. Share only lesson clusters that appear in at least k projects, with generalized text, so single-project details never leave.
  Done when: a lesson seen in one project is withheld from the shared pool, and the same lesson seen in k=3 projects appears with paths and names stripped.

- **Wild: Keep a quality-diversity archive of Foreman variants** — FEATURE — value 3 — effort L — risk med — category: evolution
  Why: wild; assumption: `fm evolve` keeps one winner. A MAP-Elites style archive instead keeps the best variant per behavioural niche (terse vs thorough, cautious vs fast, per language), and picks from it per project.
  Done when: the archive holds at least 3 variants in different niches, and `fm evolve --niche cautious` selects a different variant than `--niche fast` for the same project.

- **Wild: Learn a repo digital twin that predicts blast radius** — FEATURE — value 4 — effort L — risk high — category: prediction
  Why: wild; `fm impact` is static. Train a small local model on co-change, surprise logs and test failures to predict which tests and files a plan will actually disturb, then compare to the real outcome and keep learning.
  Done when: on held-out finished tasks the twin's predicted test set recalls at least 80% of the tests that failed or were touched, beating `fm impact` alone.

- **Wild: Schedule night work by grid carbon intensity** — FEATURE — value 2 — effort S — risk low — category: scheduling
  Why: wild; `fm night` already budgets background work. Delay heavy, non-urgent jobs (landscape, bench, evolve) into low-carbon hours using a public intensity forecast, and report the estimate in `fm digest`.
  Done when: with a stubbed forecast, `fm night` starts a heavy job in the low window and the digest shows the shift.

- **Wild: Publish an open discipline benchmark from redacted ledgers** — FEATURE — value 3 — effort L — risk high — category: research
  Why: wild; `fm bench` replays private tasks, and no public set measures whether harness discipline improves agent outcomes. A redacted, held-out case set with scoring scripts would let others test their own harness against it.
  Done when: an exporter produces a redacted case bundle that passes the secrets scan, and the scoring script reproduces Foreman's own bench score from the bundle.
