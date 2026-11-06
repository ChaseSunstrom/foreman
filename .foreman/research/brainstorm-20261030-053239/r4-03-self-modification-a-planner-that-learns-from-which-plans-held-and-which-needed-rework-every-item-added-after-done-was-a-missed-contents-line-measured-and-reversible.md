# Brainstorm — lens: self-modification: a planner that learns from which plans held and which needed rework (every item added after done was a missed contents line), measured and reversible

- **Capture every post-done addition as a typed miss record** — FEATURE — value 5 — effort M — risk low — category: planner learning
  Why: the lens's premise is that each item added after done is a missed contents line, but the pack shows no store for them (gap map: "goal ledger" missing; earlier ideas "Log every post-done addition as a missed line" are unbuilt). Record file, task id, goal id, days-since-done, and the user-words noun it should have traced to.
  Done when: closing a goal, then `fm task` adding an item linked to it within the window, writes one `miss` ledger event with those fields; `fm goal misses <id>` lists it.

- **Separate a miss from scope growth with a lag-and-trace test** — FEATURE — value 4 — effort M — risk med — category: planner learning
  Why: assumption: not every later addition was a planning failure; the user may legitimately widen the goal. Count a miss only if the new line traces to words that existed at plan time (the seal snapshot); otherwise label it growth. Without this the planner learns to pad.
  Done when: a fixture goal with one traceable and one new-ask addition yields one `miss` and one `growth` record.

- **Keep planner rules as sealed, hash-named files with a one-command revert** — FEATURE — value 5 — effort M — risk low — category: reversibility
  Why: "measured and reversible" is the lens; the existing charter seal (sha256, 444, ledger event) is a ready pattern. Each rule is a small declarative file (trigger, added line template), never code, so a self-edit cannot execute anything.
  Done when: `fm planner rule revert <hash>` restores the previous ruleset, the ledger records it, and the plan for a fixture goal returns to its earlier text byte for byte.

- **Stamp each plan line with the rule that produced it** — FEATURE — value 4 — effort S — risk low — category: attribution
  Why: credit and blame need a join key; assumption: contents rows currently carry no origin. Add `src:` per row (user-words, repo, rule:<hash>, model).
  Done when: `fm goal show` prints the origin for every row and a lint fails on a row with none.

- **Replay a candidate rule against finished goals before adopting it** — FEATURE — value 5 — effort L — risk med — category: measurement
  Why: the exam principle ("a capability is done only when held-out scenarios pass") applies to the planner too. Backtest: would the rule have produced the missed lines on past goals (recall), and how many extra lines would it add to goals that never needed them (padding)?
  Done when: `fm planner try <rule>` prints recall and padding counts over the last N finished goals and refuses adoption if padding exceeds a settings cap.

- **Allow adoption only after repeats: a rule needs the same miss class on 3 goals** — FEATURE — value 4 — effort S — risk low — category: guardrail
  Why: "precision over volume" was the lesson of the last two Missions; one miss is an anecdote. Assumption: miss classes can be clustered by the trigger noun/verb plus surface (the coverage grid axes).
  Done when: two misses of a class yield no proposal; the third yields exactly one proposed rule file in `proposed/`.

- **Make adoption additive-only and ban loosening** — SECURITY — value 5 — effort S — risk low — category: guardrail
  Why: constraint "NEVER: grant yourself anything or lower your own guard". A learned rule may add or reorder contents lines, never delete a MUST, relax a done-when, or touch the Stop hook.
  Done when: a rule file whose effect removes or weakens any existing row is rejected by `fm planner check` with a named reason; test covers each loosening shape.

- **Auto-revert a rule whose goals reopen more than baseline** — FEATURE — value 4 — effort M — risk med — category: reversibility
  Why: measured and reversible means the loop closes. Compare reopen rate of goals planned with rule X against those without, over a minimum sample; revert and ledger the reason when worse.
  Done when: a synthetic history where rule X goals reopen at twice the baseline triggers one automatic revert event, and a history below the minimum sample triggers none.

- **Plan every goal in shadow under a challenger ruleset and grade both at finish** — FEATURE — value 4 — effort L — risk med — category: measurement
  Why: the only way to get a causal comparison on live work without exposing the user to an untested rule. Challenger plan is never shown or executed, only diffed at close against the final item set.
  Done when: at goal finish, `fm goal grade` reports lines each ruleset covered or missed and which one matched the final list better.

- **Score plan precision as well as recall** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: assumption: a planner rewarded only for recall pads. Track lines that were planned but cut or never touched as a padding penalty, so a rule must earn its place.
  Done when: the planner report shows recall, precision and a net score per ruleset, and a rule adding five never-used lines lowers the net.

- **Wild: Hindsight replay — re-plan the last ten finished goals with today's rules** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: assumption: a time-lapse of "what would we have planned now" is both a regression test and a morale page on the site. Shows which old misses are now caught.
  Done when: `fm planner hindsight` prints, per old goal, lines the current rules add that the original lacked, and the site exports it.

- **Wild: Seal three prophecies at plan time of what the user will add after done** — FEATURE — value 3 — effort M — risk med — category: wild
  Why: forces the planner to commit to predictions that are graded against real reopens, giving a calibration score for the planner itself instead of only counting misses.
  Done when: each new goal stores three sealed prophecies, and at the end of the reopen window each is marked hit or miss with a running hit rate.

- **Wild: Planner tournament across projects with scrubbed rules** — FEATURE — value 3 — effort L — risk high — category: wild
  Why: rules learned on Foreman's repo may not transfer (the pack's own question about priors). Scrub project literals, pool classes locally, and test transfer on a held-out project before any rule is shared; nothing leaves the machine without a setting.
  Done when: a rule learned in project A is applied in project B only after a recorded held-out backtest in B passes, and the scrubber leaves no project-specific string in the pooled file.

- **Wild: Have the planner plan its own next ruleset revision as a goal** — FEATURE — value 3 — effort M — risk med — category: wild
  Why: dogfoods the goal ledger on the planner itself; revisions get a contents list, done-when and exam scenarios like any capability, so self-modification passes the same bar as everything else.
  Done when: opening a ruleset revision creates a goal whose done-when includes the backtest from `fm planner try` and finish is refused without it.

Next question: How long must the reopen window run before a miss rate is trustworthy, given goals finish at a rate of only a few per week on one project?
Next question: Which parts of a plan can the user veto in one line, so a bad learned rule is dropped by their steer rather than only by statistics?
