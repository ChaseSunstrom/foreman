# Brainstorm — lens: self-modification: a planner that learns from which plans held and which needed rework (every item added after done was a missed contents line), measured and reversible

- **Compute a plan-miss rate from the goal ledger** — FEATURE — value 5 — effort M — risk low — category: planner metrics
  Why: the pack lists "every item added after done was a missed contents line" and earlier ideas ("Log every post-done addition as a missed line") but no single number exists to learn from. Assumption: the goal ledger stores an item's `added_at` and the goal's `done_at`.
  Done when: `fm goal stats` prints, for a fixture goal with 10 planned and 3 post-done items, `miss_rate=0.23` (3/13) and lists the 3 lines.

- **Define a ruleset as a sealed, hash-named file the planner reads** — FEATURE — value 5 — effort M — risk med — category: self-edit substrate
  Why: the planner is currently prompt text in `fm mission`; nothing is versionable. Self-modification needs a unit that can be diffed, stamped on each goal and reverted. Assumption: a rule is one line plus a trigger (kind of goal, surface, verb).
  Done when: `fm planner rules` lists rules with sha256s, each goal records the ruleset hash, and `fm planner revert <hash>` restores the earlier set byte-for-byte (tested).

- **Propose rules only from repeated misses, never from one** — FEATURE — value 4 — effort M — risk low — category: learning gate
  Why: the lessons say "precision over volume"; one miss is anecdote and padding is a cost. Assumption: miss lines can be clustered by a normalized verb×surface key.
  Done when: with two misses sharing a key a rule is only proposed after a third on a distinct goal; a test with a single miss yields zero proposals.

- **Replay a candidate ruleset against finished goals before adoption** — FEATURE — value 5 — effort L — risk med — category: backtest
  Why: the exam grades capabilities, but nothing grades the planner. Past goals with known post-done additions are free held-out data. Assumption: ≥10 finished goals exist in the ledger (Foreman's own repo has many).
  Done when: `fm planner try <ruleset>` reports recall (how many historical misses the plan would have listed) and padding (lines never later used) on a train/holdout split, and refuses adoption if holdout recall does not rise or padding rises over a set bound.

- **Make adoption additive-only: rules may add or reorder, never delete or loosen** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: constraint "NEVER lower your own guard"; a learned rule that drops a MUST line is a self-grant. Assumption: rules are parsed by a small declarative grammar.
  Done when: a rule file containing a removal/loosening directive is rejected with a ledger event, and a test proves the gen-0 MUST lines still appear in every plan.

- **Auto-revert a rule whose goals reopen more than the baseline** — FEATURE — value 4 — effort M — risk med — category: reversibility
  Why: "measured and reversible" is the lens; rules need a kill criterion. Assumption: reopen rate is measurable per ruleset hash after the 14-day window.
  Done when: in a simulated history, a rule present in 5 goals with a miss rate above the prior ruleset's is reverted by `fm planner audit`, with a ledger event naming the evidence.

- **Credit rules by withholding: skip each learned rule on one goal in five** — FEATURE — value 3 — effort M — risk low — category: causal credit
  Why: without a control group, a rule that coincides with good goals gets credit it did not earn. Assumption: goals are numerous enough (tens) for rough signal.
  Done when: planning records which rules were withheld, and `fm planner stats` shows per-rule miss rates with and without it.

- **Tag every plan line with the rule that produced it** — FEATURE — value 3 — effort S — risk low — category: provenance
  Why: user trust and debugging; the pack already wants line provenance. Assumption: contents rows have a `src` field.
  Done when: the goal card shows `(rule R-07)` beside learned lines, and an unknown-source line fails `fm goal check`.

- **Show a planner report card on the pane and site** — FEATURE — value 3 — effort M — risk low — category: surfaces
  Why: the mission requires every capability on each surface. Assumption: stats export is redacted of project literals before reaching the site.
  Done when: the pane line, MCP read-only tool, `fm code` command and a site page all render the same miss-rate trend from one JSON, and the site build test passes.

- **Wild: Hindsight replay — re-plan the last ten finished goals with today's rules and show the diff** — FEATURE — value 3 — effort M — risk low — category: backtest, wild
  Why: assumption: a vivid diff ("today's planner would have listed 4 of your 6 reopens") makes the learning visible to the user.
  Done when: `fm planner hindsight` prints per-goal added lines versus the actual post-done additions.

- **Wild: Planner tournament — plan each new goal under champion and challenger rulesets, grade both at finish** — FEATURE — value 4 — effort L — risk med — category: shadow evaluation, wild
  Why: assumption: shadow planning costs one extra child call per goal and yields live, not retrospective, evidence. Only the champion's plan is ever shown.
  Done when: at goal finish, the ledger records both plans' recall against actual additions, and a challenger wins promotion only after N wins.

- **Wild: Have the planner plan its next ruleset revision as a goal in its own ledger** — FEATURE — value 3 — effort M — risk high — category: recursion, wild
  Why: assumption: dogfooding makes revisions inherit the done-vs-stopped verdict and exam gate; protected core edits still need `fm ask ID core`.
  Done when: a planner revision exists as a goal whose closing requires passing the backtest, and a test shows it cannot finish with the backtest red.

- **Split misses into knowable and unknowable by the snapshot the planner saw** — FEATURE — value 3 — effort M — risk low — category: attribution
  Why: a miss caused by a later user steer is not a planner fault and would teach padding. Assumption: user steers are journaled with timestamps.
  Done when: a post-done line traced to a steer dated after planning is classed unknowable and excluded from rule proposals (tested).

Next question: What is the minimum number of finished goals before any learned rule is statistically distinguishable from noise, and what does the planner do until then?
Next question: Who owns the sealed ruleset if a rule is learned from a user's private project and then applies on another project?
