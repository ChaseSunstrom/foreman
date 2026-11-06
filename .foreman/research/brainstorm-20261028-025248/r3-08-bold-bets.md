# Brainstorm — lens: bold bets

- **Retune the rules file when the model changes** — FEATURE — value 5 — effort M — risk med — category: model drift
  Why: assumption: a changed model reruns the cost math (pack), but nothing re-tests the rules and prompts against it. A model swap can silently change which rules still earn their lines.
  Done when: changing the model id in the test fixture starts a duel run, writes a retune record with pass and fail counts, and leaves the rules file unchanged unless the candidate beats the baseline.

- **A/B two rules-file variants across real queued tasks** — FEATURE — value 4 — effort L — risk med — category: duel
  Why: assumption: the duel and ablation run offline on fixtures (pack: "Ablate each rules-file line", "duel data"). No arm of the live queue gets a different rule set.
  Done when: each queued task is assigned a variant by a hash of its id, both arms are recorded in the journal, and `fm duel` reports per-arm pass rates only once each arm has a set minimum of closed tasks.

- **Run each lane in a microVM with a network allowlist** — FEATURE — value 4 — effort L — risk med — category: isolation
  Why: the guard is an in-process hook, and Landlock limits writes only. Nothing stops a lane from reading `~/.ssh` or opening arbitrary network connections.
  Done when: a probe task run under the VM backend cannot read `~/.ssh` and cannot reach a host outside the allowlist, and the probe is a test that fails the build if either access succeeds.

- **Ship Foreman through its own queue** — FEATURE — value 4 — effort M — risk med — category: release
  Why: the pack shows pushes and site deploys done by hand, and an acceptance check pinned to an old commit (a5b5cf7e, criterion 2). The release path is outside the loop Foreman sells.
  Done when: a green commit on main produces a tag, a site deploy and a receipt naming the commit, with no manual push, and the receipt is re-checked against the live site.

- **Wild: a CI referee for disputed gates** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: pack: the false "CI red on main" alarm came from a cancelled run, and local and CI verdicts can disagree. Nothing arbitrates when they do.
  Done when: when a task's local gate and its CI gate disagree, a referee run re-judges the change in a clean checkout and posts one verdict with the evidence, and the test feeds it a deliberate disagreement and checks that exactly one verdict is posted.

- **Wild: a bounty board for TODOs** — FEATURE — value 3 — effort M — risk low — category: queue
  Why: assumption: the backlog and the code's TODO comments are separate lists, and nothing ties a spend budget to a specific small fix.
  Done when: `fm bounty` lists each TODO with a token cap, a lane claims one and the claim expires on its own, and a closed bounty shows the cap it used.

- **Turn a plain sentence into a guard rule, previewed on real history** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: the pack has replay of guard decisions and a rule-learning idea, but no way for the user to add a rule in their own words and see its effect first.
  Done when: `fm guard add "<sentence>"` compiles a rule, replays the last 500 journaled commands, lists every command the rule would change, and writes the rule only after a yes.

- **Wild: an energy receipt in watt-hours** — FEATURE — value 2 — effort S — risk low — category: cost
  Why: wild. Cost is shown in tokens and dollars only; on Linux, RAPL counters may show the machine's energy use for a run.
  Done when: on a host where the RAPL counter is readable, the close receipt shows watt-hours for the run, and on a host without it the receipt prints "energy: n/a" with no error.

- **Wild: a repro bug filed against any gate that lied** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: wild. A gate that passes a change a later revert undoes is a defect in the gate, but nothing records the gate's own mistake as a bug.
  Done when: when a revert lands within a set window of a closed task's proof, a bug file is written with the gate name, the commit and a minimal repro command, and it is de-duplicated by gate and commit.
