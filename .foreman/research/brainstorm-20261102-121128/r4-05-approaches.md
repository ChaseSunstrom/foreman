# Brainstorm — lens: approaches

- **Spend the expiring quota first** — FEATURE — value 4 — effort S — risk low — category: scheduling
  Why: assumption: usage is windowed, so capacity that resets in a few hours is free and capacity that resets in six days is not. The pack says only "0%", with no reset time. Rank queued idle work by cost times hours until reset, and run the cheap-to-lose items first.
  Done when: with a fake reset clock 2 hours out, the planner picks a measurement run, and with the clock 6 days out it picks nothing over the cap.

- **Lint the spend plan against the steers** — FEATURE — value 4 — effort S — risk low — category: guardrails
  Why: steers say `fm exam long run` refuses without `--final` or `--regressing`, and "go wild" could tempt a drive into exactly that. Check each planned run against the stored steer checks before it starts, and print which steer blocks it.
  Done when: a plan containing a long-horizon session arm is rejected with the steer's date, and the same plan with `--regressing N` passes.

- **Yield to the user: idle work preempts itself** — FEATURE — value 4 — effort M — risk med — category: unattended
  Why: assumption: idle drives and the user's interactive session draw on one account. Pause or shrink lanes when a session starts, then resume where they stopped. This matches the standing rule to wait out limits, but adds a yield, so the idle spend never takes the user's quota.
  Done when: starting a session event mid-drive stops new child launches within one tick and the drive resumes after the session ends.

- **Run Foreman on thirty foreign repos, zero tokens** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the map shows only six stack cards, and the steers say `fm find` recall must be reported per language. Run `fm init`, `fm map`, `fm find` and `fm doctor` on a fixed corpus of public repos across stacks and record crashes, empty gates and nonsense output. This is the free first pass, before any session arm.
  Done when: a corpus report lists, per repo, the gate Foreman inferred and any verb that crashed, and a failing repo files a task.

- **Fill missing stack cards from the corpus** — FEATURE — value 3 — effort M — risk low — category: stacks
  Why: assumption: a card is only worth having if its gate command passes on a sample repo of that stack. Generate a card per uncovered stack from the corpus run above and keep it only when its commands run there.
  Done when: each new card ships with a recorded passing run on a corpus repo, and `fm lib show NAME` prints it.

- **Print a spend receipt with yield per dollar** — FEATURE — value 3 — effort S — risk low — category: ops
  Why: the budget line shows $0 of $200, and the pack has no way to say whether idle spend bought anything. List dollars and minutes against tasks closed, later reopened, or reversed after "proven".
  Done when: after an idle run, `fm cost` ends with a line of spend, closed tasks, and the count of those reopened within 14 days.

- **Offer three spend plans with a timed default** — FEATURE — value 3 — effort S — risk low — category: decisions
  Why: the steers say never block on the user, but "go wild" leaves open how wild. File one `fm decide --kind costly` with cheap, measured and ambitious plans, and take the measured one after a timeout.
  Done when: the final report lists the chosen plan, the two rejected ones, and who or what chose.

- **Map churn hotspots from task history** — CLEAN — value 3 — effort S — risk low — category: maintenance
  Why: recent commits show T-2606 to T-2616 each patching calibration and readers, and T-0166 shows `register.tsx` as a hotspot. Count tasks per file and per MASTER.md clause over the 2,600 ids, then file a consolidate task for the top three. This needs no tokens.
  Done when: `fm map --churn` prints files ranked by distinct task ids touched, and one CLEAN task cites the top entry.

- **Test answerability of the status verbs** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: a prior idea asked for `fm why`. A child writes 200 questions the user might ask ("why is T-0335 blocked?", "what did the night tick skip?"), and each must be answerable from `fm` output alone and checked against the ledgers.
  Done when: an answerability score is reported per verb and a wrong answer, as opposed to a refusal, fails the check.

- **Make zero spend the default with a named payoff** — CLEAN — value 2 — effort S — risk low — category: doing less
  Why: the lean steers say growth without measurement waits, and the idle budget invites growth. Each idle item must name the metric it moves, otherwise it is logged as "declined, no measure" so that skipping counts as a success.
  Done when: an idle item with no named metric is recorded in a declined list with its reason and never launched.

- **Duel Foreman against its past self — wild** — FEATURE — value 5 — effort L — risk med — category: evidence
  Why: wild: nothing in the pack shows the last 2,000 tasks improved held-out outcomes, and the steers prize signals Foreman didn't author. Check out Foreman at four old commits, run the same held-out scenarios on each with the Haiku arm, and plot passes, cost and time against commit.
  Done when: a table shows each commit's held-out pass rate and cost, and a later commit scoring lower is flagged for the end-of-run exam.

- **Build a rival from the README, then duel it — wild** — FEATURE — value 4 — effort L — risk med — category: Lite mode
  Why: wild: T-0794 (Slim Foreman, Lite mode) is deferred for lack of evidence. A tool-less child writes the smallest tool that meets the README's claims (guard, plan, prove), with no sight of the code. Duel it against Foreman on held-out scenarios to see what the other features buy.
  Done when: the rival and Foreman have scores on the same scenarios, and the gap is recorded per capability.

- **Write the smallest-diff retrospective — wild** — CLEAN — value 3 — effort M — risk low — category: subtraction
  Why: wild: lean and subtraction steers keep growing. For a sample of 30 closed tasks, a cold child proposes the smallest diff that meets each DONE-WHEN. Compare it with the shipped diff, and where the shipped one is more than twice the size, file a trim task.
  Done when: a report lists shipped versus minimal lines per task, with at least one trim task filed from a ratio above 2.

Next question: which standing steers are phrased as "wait for the end-of-run exam" and so quietly cap what idle usage may be spent on, and does the drive know that?
Next question: what would the user say if shown last month's spend receipt, and is there any record of them ever judging whether an unattended run was worth its cost?
