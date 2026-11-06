# Brainstorm — lens: deepen: autonomy

- **Run review and ideas as headless drive stages** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the pack's round-4 review says /foreman:review and /foreman:ideas only run when the user types them, so the AFK drive can't use them. The five near-duplicate ideas already listed all point here. Make them `fm review --headless` and `fm ideas --headless` verbs that the drive calls at set points: after a lane merge, and when the queue is empty.
  Done when: a test with a fake `claude -p` and an empty queue shows the drive calling `fm ideas`, capturing the results, and writing the call to the ledger without any user input.

- **Auto-record reviewer findings from review output** — FEATURE — value 5 — effort S — risk low — category: autonomy
  Why: `fm task finding` is one manual call per finding, so the defect-class feed that builder briefs read starves. The headless review stage should parse the structured findings itself and record them.
  Done when: a test feeds a fixture review result with three findings and `fm lane brief` lists those defect classes under "Defects this project keeps shipping" without a manual call.

- **Gate the drive on a review-then-fix loop per lane** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: "Every builder branch so far needed a review round (2-6 real defects each)". Merge only after a headless reviewer finds nothing, or after N fix rounds, and then park the lane with a note for the user.
  Done when: a test with a fake reviewer that returns defects on the first pass and none on the second shows two builder passes and then a merge, and a third failing pass shows the lane parked.

- **Preview a contract against the queue** — FEATURE — value 4 — effort S — risk low — category: autonomy
  Why: `fm contract --until --usd` exists (T-1158) but gives no forecast. `fm contract --dry` should estimate from past task cost and duration which queued tasks fit, and which will be cut off.
  Done when: a test with seeded per-task cost history prints the tasks that fit under $5 and the ones left out.

- **Resume the drive after a crash or limit hit** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: assumption: the drive is only as unattended as its restarts are. T-0798 (recovery, deferred) covers crash-loop quarantine and blackstart. Combine it with the contract: a watchdog that restarts the drive with the remaining budget, and quarantines a task that crashed it twice.
  Done when: a test that kills a fake drive mid-task sees it restarted once, and the task parked after the second crash.

- **Make a morning digest the end of every contract** — FEATURE — value 4 — effort S — risk low — category: autonomy
  Why: the user is AFK and `fm away`, `fm todo` and the contract receipt exist as separate pieces. A single `fm morning` view should join them: what closed, what is red, what needs the user (with commands), and the spend.
  Done when: a test ends a contract and finds one file that holds the receipt, the todo list and the away summary.

- **Run the drive as a headless daemon between sessions** — FEATURE — value 4 — effort L — risk high — category: autonomy
  Why: this is already in the category list. Bound it by the contract, a systemd user timer or a lock file, and a kill switch file that the guard checks.
  Done when: with a fake clock the daemon starts at HH:MM, works one task, stops at the bound, and exits cleanly when the kill file appears.

- **Release as a drive-run pipeline** — FEATURE — value 4 — effort M — risk high — category: autonomy
  Why: "Releases are a manual 8-step ritual". Let the drive run it to the point of a prepared release branch, and push only on an explicit grant (the user said "push to main" before, but approval in one context doesn't carry to the next).
  Done when: a test with a fake repo gets the version bumps, heading, gates and release-check run in order and stops before the push with a pending grant.

- **Wild: Run a skeptic child that tries to break the last release overnight** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: wild. Under the contract a read-only child gets the release diff, writes adversarial inputs for the guard, the hooks and the CLI, and captures each real failure as a FIX with its repro.
  Done when: a test plants a known bug in a fixture release and the skeptic captures a FIX brief with a failing repro command.

- **Wild: Run a shadow round on a throwaway clone first** — FEATURE — value 3 — effort L — risk med — category: autonomy
  Why: wild. Before spending real budget, the drive does the round in a temporary worktree clone and keeps only the tasks that pass their gates. It reports what would have shipped, as a dry run for the real run.
  Done when: a test shows a shadow run leaving the main checkout untouched and producing a ranked list with pass or fail per task.

- **Wild: Steer a running contract with a plain phrase** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: wild. The user types "stop by 6" or "no more refactors" and a mechanical parser (no model) edits the contract file. The drive reads it at each task boundary, and the receipt shows the change.
  Done when: a test with the phrase "until 18:00" changes the bound, and an unparseable phrase changes nothing and says so.

- **Let lanes run `fm` from their own worktree** — FIX — value 4 — effort S — risk low — category: autonomy
  Why: "bare `fm` resolves to the main checkout's copy", so builders can't test new flags and have to type `python3 plugin/bin/fm`. The lane's environment should put the worktree's `plugin/bin` first on PATH.
  Done when: a test runs bare `fm` inside a lane worktree with a new flag and sees the worktree's copy answer.

- **Pick the cheapest model per lane with a measured fallback** — PERFORMANCE — value 3 — effort M — risk med — category: autonomy
  Why: pillar 1 says "cheapest model that can". Record per task type whether a lane passed review on a small model, and escalate only after a failure.
  Done when: a test with history where small-model lanes failed review twice for a task type sends the next lane of that type to the larger model.
