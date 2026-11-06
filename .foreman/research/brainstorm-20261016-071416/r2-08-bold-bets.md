# Brainstorm — lens: bold bets

- **Run Foreman's drive as a headless daemon that works the queue between sessions** — FEATURE — value 5 — effort L — risk high — category: autonomy
  Why: The user is AFK and wants Foreman to "figure everything out itself"; the review notes the autonomous drive can't use /foreman:review or /foreman:ideas, and `fm contract` (T-1158) already bounds runs by time and spend. A supervised background process that wakes on a schedule, respects the contract, and leaves a return receipt (`fm away`) removes the need for an open Claude session.
  Done when: with a fake clock and fake `claude`, starting the daemon under a contract with one queued task closes it, stops at the bound, and `fm away` lists the close.

- **Make the round itself a verb: `fm round` runs review, brainstorm, triage, build, and release** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: Round 4's mission is a hand-run recipe (review what shipped, brainstorm with `--seen`, build, release by an 8-step ritual); T-0826 (round ledger) is deferred and the brainstorm list repeats "fm release" and "round retro" ideas. One resumable verb with a stop-when-dry rule collapses them.
  Done when: a test with stubbed children runs two rounds on a fixture, stops when the second brainstorm returns zero new ideas, and prints a scorecard with counts built, skipped and reverted.

- **Pre-flight every brief by dry-building it in a throwaway lane** — FEATURE — value 4 — effort M — risk med — category: quality
  Why: Premises were false after the fact (dropped: hook import cost, lane-merge retry, verb auto-capture, guard variable following). Each cost a builder run. A cheap probe lane that runs the brief's DONE-WHEN against the current tree and reports "already true / premise false / buildable" before dispatch removes that waste.
  Done when: a brief whose DONE-WHEN already passes on the fixture is marked "already true" and not dispatched; a brief with a failing check is dispatched.

- **Prove the reviewer loop closes: auto-record findings and show defect-class survival** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: Findings are recorded by hand (`fm task finding`), so the "Defects this project keeps shipping" feed starves; every builder branch still needed 2–6 fixes, and T-1147/T-1164 are "new and unmeasured".
  Done when: a reviewer stop with output containing two findings creates two finding records, and a report prints per-class counts before and after the builder self-review shipped.

- **Run the whole discipline on a small local model as a gating smoke test** — FEATURE — value 4 — effort M — risk med — category: weak-model support
  Why: The standing ask is that Foreman work for weak/small local models; no test shows it does, and guessed verbs like `fm task list` show weak agents derail. Wild-adjacent: a scripted tour against a local OpenAI-compatible endpoint maps where it derails.
  Done when: a scripted tour runs against a stub model that guesses wrong verbs twice, and the report lists each derailment with the verb that rescued it.

- **Alias guessed verbs from the unknown-command log and say so quietly** — FIX — value 3 — effort S — risk low — category: ergonomics
  Why: Review: "common guesses could simply work"; `fm task list` is the named case, and the nearest-match suggestion already exists.
  Done when: `fm task list` runs `fm task ls` and prints one note line "(ran `fm task ls`)"; an unknown, unlogged verb still errors.

- **Give each lane its own `fm` on PATH** — FIX — value 4 — effort S — risk low — category: lanes
  Why: Review: builders can't run their own new flags because bare `fm` resolves to the main checkout; they must call `python3 plugin/bin/fm`.
  Done when: in a lane worktree, `fm <new-flag>` runs the lane's copy, shown by a test that adds a flag only in the worktree.

- **Cut a release with `fm release`, resumable at every step** — FEATURE — value 4 — effort M — risk med — category: release
  Why: The release is a manual 8-step ritual (3 version fields, heading, gates on a quiet tree, release-check, temp worktree merge, push); T-1173 is open now. Push is outward-facing, so it stays behind the existing push grant.
  Done when: on a fixture repo with a fake remote, killing the verb after step 4 and rerunning finishes steps 5–8 without repeating 1–4, and push refuses without the grant.

- **Wild: Fire-drill the discipline with a planted bad brief** — FEATURE — value 3 — effort M — risk low — category: assurance
  Why: assumption: the guard and review gates are only tested on known cases. Plant a brief with a false premise, a secret in a quoted spec, and an out-of-scope edit; a drill passes when Foreman refuses all three. wild
  Done when: `fm drill` on a fixture prints three caught and zero missed, and fails when a gate is disabled.

- **Wild: Make the final report a tickable "only you" page that executes the ticks** — FEATURE — value 4 — effort M — risk med — category: handoff
  Why: Pillar 7 sends user-only work to the final report; `fm todo` exists with commands. A local HTML page with checkboxes that, on tick, runs the approved command through the existing grants closes the loop from a phone or desktop. wild
  Done when: ticking one item in the served page runs its command once and the item drops from `fm todo`; an unticked item runs nothing.

- **Wild: Race two cheap builders on a hard task and keep the one whose proof passes** — FEATURE — value 3 — effort L — risk med — category: lanes
  Why: Reviews found 2–6 defects per branch; a cheap second attempt may cost less than a review round. Spend is governed by `fm contract`. assumption: cost parity holds. wild
  Done when: a test with two stub builders, one failing its DONE-WHEN, merges only the passing lane and logs the loser's cost.

- **Replay mined refusals as a standing premise check before any guard task** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: Twice a premise was false only after hand-mining transcripts; refusals are counted without their commands. Digest should show the command plus the replay verdict via `fm guard try`.
  Done when: the friction digest on a fixture transcript lists each refused command with its replay verdict, and a guard-task capture attaches that list.

- **Drop the guard's "it could be …" guess unless the path exists** — FIX — value 2 — effort S — risk low — category: guard
  Why: Review: the guess shows odd paths such as /repo/cd/w.out, a word glued into the path.
  Done when: a test with `cd w; cat > w.out` yields no guess naming `/repo/cd/w.out`, and an existing path still yields a guess.
