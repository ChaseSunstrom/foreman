# Brainstorm — lens: deepen: planning

- **Compile the plan into a "finished contract" file the Stop hook reads** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: the goal is "knows when it's actually done rather than merely stopped"; open questions ask which file settles "done" between legs and who checks it wasn't edited. Combines the poster, the contents rows and the done check into one sealed artifact, like gen-0's charter seal (sha256, 444, ledger event).
  Done when: a goal's plan writes `contract.md` with a hash in the ledger; editing it between legs makes `fm doctor` fail, and Stop refuses to close the goal until every row's check command has passed.

- **Give every plan row a check command and a user-minutes and token price** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: grows "price every row" with the standing rule that every steer is a rule plus an automatic check (`fm decide --check`). A row without a runnable check is rejected as vague.
  Done when: `fm plan add` without `--check` fails; the plan shows a per-row cost and a total before acceptance.

- **Rank the plan by fog: rolling-wave rows with a visible horizon** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: grows "rolling-wave fog of war". Near rows are detailed, far rows are one-line themes, and each leg ends by expanding the next wave. This keeps the baton small enough for a fresh session (open question on baton size).
  Done when: a plan holds at most N detailed rows; completing a wave triggers expansion of the next, and the baton for a fresh session stays under a measured size cap.

- **Tag every spike row with the decision it must produce and what each answer changes** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: grows "spike rows that end in a decision". Each spike names its options and the rows that appear or vanish per answer, so the answer edits the plan mechanically. Matches the T-1331 pattern of research tasks.
  Done when: closing a spike without a decision line fails; the decision adds or removes the rows it declared.

- **Classify reopens as miss, mind-change or environment, and learn only from misses** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: answers the questions on user mind-changes vs missing rows. A reopen records its cause; a user steer cited in the reopen marks it mind-change and is excluded from the miss rate. Assumption: the user's steer text is available at reopen time.
  Done when: the ledger shows reopens split by class, and the planner's learned rules cite only miss-class reopens.

- **Let the user veto a learned planning rule in one line** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: answers the one-line veto question. `fm plan rule drop <id>` plus a steer becomes a standing "never" rule with a check, so statistics can't re-learn it.
  Done when: a dropped rule never reappears in the next three plans, and `fm doctor` flags any plan that violates a steer-backed rule.

- **Retrieve a skeleton from finished-goal shapes with a similarity receipt** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: grows "retrieve a skeleton". The plan shows which past goals it borrowed rows from and which rows those goals later reopened, so borrowed rows carry their known miss history.
  Done when: a new plan lists its source goals, and a row that reopened in a source is marked "watch".

- **Run a blind second planner and diff the two plans into a missing-rows list** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: grows the "second opinion lane". Instead of re-planning wholesale, only the diff is shown, and rows only one plan had are the questions. Uses cheap Haiku fm cold reads, as in the genesis put.
  Done when: each accepted plan has a diff report, and rows from the second plan that later prove needed are counted as the first planner's miss rate.

- **Wild: Pre-mortem lane that writes the postmortem before work starts** — FEATURE — value 4 — effort M — risk low — category: planning — wild
  Why: assumption: failures cluster in a few classes (reopens, killed processes). A child is told "this goal failed in a week, write why" and each cause becomes a row or a check.
  Done when: every plan has a "premortem" section whose causes map to rows or explicit accepted risks.

- **Wild: Refuse any plan longer than one screen, then fold the rest into named sub-goals** — FEATURE — value 3 — effort S — risk med — category: planning — wild
  Why: grows the one-screen refusal into a hierarchy: overflow becomes child goals, each with its own contract, so the baton stays small and ownership of the Stop verdict is clear when two goals are open.
  Done when: a plan of more than one screen is split automatically, and the Stop hook names which goal's ledger owns the verdict.

- **Wild: Plan replay against the repo's own history before accepting it** — FEATURE — value 3 — effort L — risk med — category: planning — wild
  Why: grows the long-horizon exam tier (rolled-back real repos). The planner is scored on its own past goals, so the skeleton's quality is measured before use.
  Done when: `fm plan backtest` reports row recall against a historical multi-task change.

- **Write an external witness that records stops the hooks never saw** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: answers the killed-process question. A tiny heartbeat file per goal plus a startup check marks a gap as "stopped without a verdict", which the plan then shows as an open row.
  Done when: killing the process mid-leg yields a "killed" entry on next start, and the goal is not reported as done.

Next question: What is the smallest plan edit the user makes most often after accepting one, and could that edit be predicted?
Next question: Does the plan's "finished" definition ever need to change mid-goal, and who is allowed to change it?
