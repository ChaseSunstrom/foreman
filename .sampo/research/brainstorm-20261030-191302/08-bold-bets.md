# Brainstorm — lens: bold bets

- **Compile the goal into a executable "finish program"** — FEATURE — value 5 — effort L — risk med — category: goal core
  Why: the pack's ideas keep adding gates (auditor, Stop hook, grid, warranty) as separate checks. Assumption: they would be stronger as one artifact. `fm goal compile` turns the sealed contents list into a single script of probes (one per row: command, file, URL, or cold-read question) with an expected result. "Done" means the program exits 0 on a fresh clone; "stopped" is any other state, with the failing row named. A rival-closer disagreement becomes a failing probe, not a debate.
  Done when: a goal with 6 rows compiles to one runnable file, a deleted deliverable turns exactly its row red on a fresh clone, and the Stop hook reads that exit code instead of the model's claim.

- **Bind goals to a git-native ledger on a private ref** — FEATURE — value 4 — effort M — risk low — category: durability
  Why: the pack stresses crashes, compactions and multi-day relay; the ledger lives in Foreman state outside the repo. Assumption: a goal that moves between machines or checkouts loses its plan. Store each ledger event as a commit on `refs/foreman/goals/<id>`, so history is tamper-evident, `git push` moves a goal to another machine, and `fm goal blame` falls out for free.
  Done when: cloning the repo, fetching the ref and running `fm goal step` on a second machine yields the same next action as the first, and an edited past event breaks `fm goal verify`.

- **Run a standing "second opinion" lane that re-plans every goal blind** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: assumption: the planner's blind spots are the same on every run, so a plan reviewed by its own ruleset only confirms itself. A cold child gets the user's words and the repo map but not the plan, writes its own contents list, and the diff of the two lists is shown before sealing. Lines only the blind planner produced are the cheapest missing-row detector available.
  Done when: sealing a plan prints "blind planner added N rows" with each row, and the planted-missing-row exam scenario is caught at least 2 of 3 times.

- **Make "done" a time-boxed claim that the world can contradict** — FEATURE — value 4 — effort M — risk low — category: finish truth
  Why: the pack's warranty and decay ideas rely on re-running checks. Go further: attach to each done goal a set of watchers (CI status, issue tracker, the user's next three prompts, error logs) and emit a reopen automatically when any one fires, with the firing source recorded as a miss class. This makes reopen data collected rather than self-reported.
  Done when: a seeded failure after done reopens the goal within one session start with the watcher named, and a quiet 14 days closes it with a report.

- **Ship a user-owned veto file for planner rules** — FEATURE — value 4 — effort S — risk low — category: user control
  Why: the pack's open question: how can the user drop a bad learned rule in one line? `fm goal veto <rule-id>` writes a line to a plain `vetoes.md` the planner is forbidden to override, and every plan line that came from a vetoed rule is struck from the list and the veto's use is counted.
  Done when: vetoing a rule removes its lines from the next plan, and the planner cannot re-add it without an explicit un-veto event in the ledger.

- **Price every contents row in tokens and user minutes before the plan is accepted** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: the pack asks whether reopen cost differs by class. Assumption: rows vary 100× in cost, and the user is never shown that. Show a cost column from history of similar closed rows; let the user cut or defer at plan time, and record the cut in the cut list.
  Done when: the plan view shows an estimate range per row, and after finish the actual-vs-estimate error is reported per row class.

- **Detect unwitnessed deaths with an external heartbeat daemon** — RELIABILITY→FIX — value 4 — effort M — risk low — category: reliability
  Why: the pack's open question: kills before any hook ran leave no record. A tiny watcher (systemd user timer or cron) checks the goal's lease file mtime and process liveness; when a lease lapses without a stop record it writes "died unwitnessed" with the last known step, so resume starts with a truthful cause.
  Done when: `kill -9` of a session mid-goal produces an unwitnessed-death record within 2 minutes, and the next `fm goal step` mentions it.

- **Resolve conflicting "done" definitions through one authoritative criteria file with a hash check** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: the pack asks which file settles disagreement between legs and who checks it wasn't edited. Pin the file's sha256 in the ledger at seal time; every leg compares before work and at close; edits require an `fm goal amend` event that cites a user steer.
  Done when: hand-editing a criterion makes `fm goal step` and the Stop hook refuse with "criteria changed without amend", and an amend with a steer id clears it.

- **Wild: Let the goal argue with the user in a one-page "red team memo" before day one** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. A hostile cold reader writes the 10 most likely ways this goal ends up reopened or abandoned, each tied to a contents row, and the user answers by striking or accepting each in a single keystroke. Accepted ones become clauses; struck ones teach the planner which pre-mortems the user finds noise.
  Done when: the memo appears at goal open, takes under one minute to dispose of, and every accepted item exists as a ledger clause.

- **Wild: Fund a goal from a "finish budget" the user sets in dollars and days** — FEATURE — value 4 — effort M — risk med — category: scope control
  Why: wild; the user's deferred queue holds dozens of "later" items and a $35 budget line is shown in this very session. The goal takes a budget in money and calendar days, and the planner drops lowest-value rows to fit, listing them as the cut list; the Stop hook treats an exhausted budget as a typed "out of budget" stop, never "done".
  Done when: setting a $5 budget on a $20 plan yields a sealed plan costing at most $5 with an explicit cut list, and exceeding it stops with the typed cause.

- **Wild: Raise a goal to an "heir" that outlives the model** — FEATURE — value 3 — effort L — risk med — category: durability
  Why: wild. Every model upgrade changes how a plan is read. Replay a few past goals' batons through the new model id on a schedule and compare the first move to the recorded one; a regression disables the planner ruleset for that model tier until fixed.
  Done when: a model-id change triggers the replay, and a deliberately corrupted baton is flagged as a first-move mismatch.

- **Wild: Offer a "finish line" mode that rehearses done on a throwaway worktree nightly** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: wild. Each night, while the goal is open, build the compiled finish program against a clean worktree of HEAD and report percent of probes green as a trend; the user sees the line climb, and a drop flags a regression the day it happens instead of at close.
  Done when: a morning report shows probes green yesterday vs today, and a commit that breaks one row is named by the next report.

- **Measure planner ruleset quality by the user's own steer rate** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the pack's steered entries show corrections land after plans; assumption: steer count per goal is the cheapest honest quality signal and needs no model judgment. Log steers against the plan hash and rule that produced the nearest row, chart steers per goal across ruleset versions on the site.
  Done when: `fm goal report` lists steers per goal by ruleset hash and a version with a higher rate than the prior one is flagged.

Next question: Which of these checks can run with no model call at all, so a goal's "done" stays trustworthy when the budget is spent or the provider is unreachable?
Next question: If the user never opens the terminal for a week, which single surface should carry the goal's state, and what is the least it must say?
