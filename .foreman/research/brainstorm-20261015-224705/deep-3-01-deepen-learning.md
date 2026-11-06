# Brainstorm — lens: deepen: learning

- **Replay-test every proposed rule against past sessions** — FEATURE — value 5 — effort M — risk low — category: learning
  Why: C3 promotes corrections to rules and C12 wants measurement, but nothing checks a rule before it ships. Ledger and hook logs already exist (fmhooks 578-615). Assumption: the ledger keeps enough tool-call history to re-run hook decisions offline.
  Done when: `fm rule test <rule>` replays the last N ledger sessions through the guard/hook path and prints "would have fired X times, on these turns, N of them on turns the user later accepted"; a rule over a set false-positive threshold is not promoted.

- **Classify every interrupt and steer into a typed mistake** — FEATURE — value 5 — effort S — risk low — category: mistakes
  Why: "Treat every interrupt as a labelled mistake" is listed but unspecified. Corrections are logged but only read by friction/taste. The user's steers ("cluttered", "the user shouldn't need to ask") are the same mistake types recurring. Assumption: a Haiku-or-heuristic label (scope creep, skipped proof, wrong file, too verbose, UI clutter) is accurate enough.
  Done when: each logged correction carries a `kind`, and `fm learned` shows a count by kind with the top kind linked to its newest instance.

- **Add a regret ledger that settles itself** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: builds on the listed regret ledger. Store rejected plan alternatives with the one observable that would prove the rejection wrong (later rework, revert, same file re-edited). Assumption: plans record alternatives in a parseable place.
  Done when: when a closed task's plan alternative was rejected and a later task reverts or reworks the chosen path, `fm learned` lists it as a "regret" and the next plan for a similar task shows it as a warning.

- **Keep a per-library competence map and route on it** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: combines the competence idea with C8's cards-by-import. Per dependency, track first-pass success, retries and corrections on tasks that touched it. Weak spots get the card injected up front, a stronger model, or a forced plan step. Evidence: only 6 of 1,084 cards ever fired, so there is no signal today about which ones matter.
  Done when: `fm competence` ranks the top 10 weakest libraries from the ledger, and a task touching the weakest one gets its card injected, with the receipt saying so.

- **Merge principles from lessons, fixes and corrections in idle time** — FEATURE — value 4 — effort M — risk med — category: consolidation
  Why: a Stop hook already knows when the queue is empty. It can cluster near-duplicate lessons, fixes and corrections into one principle with citations, and retire the originals only on explicit accept. Assumption: lessons are stored as text that can be clustered cheaply (an LLM call or embedding-free keyword overlap).
  Done when: after an idle consolidation run, the lesson count falls, every principle links to its source ids, and `fm learned --undo` restores the originals.

- **Search neighbouring local repos for a prior fix on a new error** — FEATURE — value 4 — effort M — risk med — category: cross-project
  Why: fixes travel via git (the user's steer), but the same machine's other repos are the nearest source. Needs a local-first, opt-in scan of the other repos' fix stores and git logs, read-only. Assumption: other repos are known from the machine-wide Foreman state.
  Done when: an obstacle with no local fix prints "repo X solved this with commit/fix F" with the path, and nothing leaves the machine.

- **Promote a golden session into a replayable playbook** — FEATURE — value 4 — effort M — risk med — category: playbooks
  Why: builds on "mark a session golden". One key marks it, and the first version extracts the ordered tool-call skeleton (read → test → edit → verify) and the cards used, then offers it as a plan template when a similar task appears. It stores a skeleton, not the transcript. Assumption: the ledger can reconstruct the call sequence.
  Done when: `fm golden T-XXXX` writes a template, and `fm task plan` on a similar task shows "similar to golden T-XXXX" with its steps prefilled.

- **Run a shadow A/B on every rule and keep only the ones that help** — FEATURE — value 5 — effort M — risk med — category: self-evaluation
  Why: C12 lists an A/B holdout and the scoreboard but not the loop. Each new rule or fix gets randomly withheld on a fraction of matching tasks. Compare interventions per task, with and without it, then auto-retire rules that show no effect after N samples. Assumption: sample sizes are small, so report intervals rather than verdicts.
  Done when: `fm learned` shows "rule R: with 0.4 interventions per task vs without 1.1 over n=12/11" and a rule with no effect is flagged for retirement.

- **Wild: Let the harness write and revise its own hook, with a bench gate** — FEATURE — value 4 — effort L — risk high — category: self-modifying
  Why: wild. When a repeated correction cannot be a text rule, the agent drafts a small hook check (a Python function in a sandbox directory), runs `bench_hooks.py` and the replay corpus, and proposes it as a diff only if the latency budget and zero false positives on the corpus hold. Never auto-installed.
  Done when: a proposal is created containing the hook diff, the replay result and the bench result, and a failing bench blocks the proposal.

- **Wild: Hold a nightly dream session that rehearses old failures** — FEATURE — value 4 — effort M — risk med — category: overnight
  Why: wild. It merges the C5 overnight work with the replay idea. For each recent failed or corrected task, a headless child re-attempts it in a scratch worktree using the current rules, cards and fixes. A score of "would it now pass first time" goes in the morning receipt and shows which lessons truly stuck. Costs money, so it needs the spend cap.
  Done when: the morning receipt lists N rehearsed failures, how many now pass unaided, and which rule or fix made the difference.

- **Wild: Hold a lesson auction between subagents** — FEATURE — value 3 — effort M — risk med — category: markets
  Why: wild. Before a task, each stored lesson and fix "bids" for prompt space with its trust score, cost in tokens and relevance. Winners are injected under a token budget. The payoff of a win (first-time pass, no correction) updates the bid, so useless lessons stop getting space on their own. This answers the "least token use" steer and the 6 of 1,084 problem.
  Done when: the injected context has a hard token cap, `fm why` shows which lessons won and lost, and a lesson that loses repeatedly drops in trust.

- **Learn the user's taste from accept/reject on diffs** — FEATURE — value 3 — effort M — risk low — category: preferences
  Why: UI steers repeat ("cluttered", "no gaps", "bigger graph"). Track which diff styles were accepted or reverted and which words appear in follow-ups, then derive a per-project design rubric. Assumption: UI-related tasks are identifiable by file type.
  Done when: before a pane or chat UI task closes, a rubric check lists the project's learned preferences, and a change violating one gets flagged with the past steer cited.

- **Wild: Share an anonymised fix commons across opted-in machines** — FEATURE — value 3 — effort L — risk high — category: federation
  Why: wild. This goes beyond the git-travelling brain: a signed, redacted fix feed, opt-in only, with each fix carrying its own A/B stats. The first version is a plain directory or git remote of exported fixes with the secret scan applied, and nothing is sent without an explicit setting. Assumption: only the tested local format is needed.
  Done when: `fm fixes publish` writes a redacted bundle that passes the secret scan, and `fm fixes import` on a second machine marks the entries as unproven until they pass locally.

- **Predict the next task and pre-brief it** — FEATURE — value 3 — effort M — risk med — category: predictive
  Why: the queue and "Later from" deferrals show clear follow-on patterns (feature, then test fix, then release). Mine task-type sequences from the ledger; when a task closes, pre-build the next probable brief (cards, files, past fixes) in the background without running anything.
  Done when: after a close, `fm next` shows a pre-assembled brief whose predicted next task was right at a measured hit rate, with the hit rate shown in the report.
