# Brainstorm — lens: self-modification

- **Gate every self-edit on a goal-path replay** — FEATURE — value 5 — effort M — risk med — category: self-edit safety
  Why: the top gaps are 6 false dones unchanged since gen 2 and resume fixes needed twice; a self-edit that touches done-gate or resume code is today judged only by the suite. Assumption: the long-tier planted-fault scenarios can run on a scratch goal without session arms (the steer defers those).
  Done when: `fm genesis` refuses to land a change under the done-gate or resume paths unless the zero-token replay of the 6 false-done scenarios and the compaction/kill scenarios is recorded for that commit sha.

- **Turn each false done into a self-written regression and a draft patch** — FEATURE — value 5 — effort M — risk med — category: self-repair
  Why: 6 false dones are "unchanged since gen 2": nobody converts a known failure into a permanent check. Assumption: false-done evidence is stored with enough transcript to extract a mechanism.
  Done when: each of the 6 has a `tests/` scenario that fails on the old gate, plus a drafted gate-patch proposal file naming the mechanism; the suite fails if one lacks either.

- **Keep a self-edit ledger with a 14-day prediction** — FEATURE — value 4 — effort S — risk low — category: self-edit accountability
  Why: steers require cold reads and lineage marks "provisional", but no record says what an edit expected. Assumption: `fm outcomes` close-survival can be read per commit.
  Done when: every self-edit commit appends {sha, surface, predicted metric, horizon}; at +14 days a line shows hit/miss; `fm doctor` names any edit with no prediction.

- **Run a probation self for done-gate changes** — FEATURE — value 4 — effort L — risk med — category: staged rollout
  Why: the done-gate is the deciding area and there's no way to try a stricter gate without risking real goals. Assumption: hook config can be switched per goal id.
  Done when: a candidate gate runs in shadow on live goals, logs where it would have blocked versus the live gate, and is promoted only after N goals with no false block the user overrode.

- **Ratchet: a self-edit may tighten the done gate freely, loosening needs the user** — SECURITY — value 4 — effort S — risk low — category: gate integrity
  Why: the standing intent says Sampo must not game its own metrics; the cheapest way to turn false dones green is to weaken the gate. Assumption: gate clauses are enumerable in one file.
  Done when: a diff that removes or relaxes a done-gate clause fails the ship gate unless a user-signed grant is present; tightening passes.

- **Queue self-edits and apply them only at a goal boundary** — FIX — value 4 — effort M — risk low — category: resume stability
  Why: a multi-day goal that survives a crash is hit if hooks/skills change under it mid-run; resume was the worst area. The drive already pins nothing. Assumption: pin by plugin generation is feasible (a related idea exists for re-exec at task boundaries).
  Done when: a self-edit landed during an open goal is not loaded by that goal's session until close, shown as "pending for T-x" in `fm doctor`.

- **Replay the failed resume with the edited text before accepting a skill/hook change** — FEATURE — value 4 — effort M — risk med — category: self-edit verification
  Why: 2 of 6 resume fixes needed a later fix, meaning the first fix was never replayed against the failure. Assumption: the dead session's transcript and ledgers are archived.
  Done when: a fix task for a resume failure cannot close unless a recorded replay of the original failure's inputs shows the new behaviour, and the commit cites that replay id.

- **Migrate in-flight ledgers when a self-edit changes schema** — FIX — value 3 — effort M — risk med — category: compatibility
  Why: goals run for days across edits; a changed ledger shape mid-goal is a silent resume break. Assumption: ledgers have no version stamp now.
  Done when: each ledger row carries a schema version, readers upgrade old rows, and a test resumes a goal written under the previous version.

- **Fence a self-edit to the failure's blast radius** — SECURITY — value 3 — effort S — risk low — category: scoped change
  Why: the self-change reviewer and protected core exist, but a fix for a worktree evidence failure could wander into the guard. Assumption: the failure's touched paths can be derived from its log.
  Done when: a self-edit task declares paths; the ship gate fails if the diff touches files outside them plus their tests.

- **Wild: Fork a probation self nightly on a throwaway clone** — FEATURE — value 4 — effort L — risk med — category: self-surgery rehearsal — wild
  Why: assumption: a clone with candidate edits can run the planted-fault tier on free arms overnight.
  Done when: morning card lists each candidate edit with its replay result against the 6 false dones and the resume faults.

- **Wild: Write tripwire tests against Sampo's own future shortcuts** — FEATURE — value 3 — effort M — risk low — category: anti-gaming — wild
  Why: the user steers against metric-gaming. Assumption: past shortcuts (weakened tests, vacuous measures) can be listed from the record.
  Done when: a suite fails when a diff lowers a test count, deletes a clause, or adds a measure its own artifacts satisfy.

- **Wild: Collect agent confessions about what Sampo made harder** — FEATURE — value 3 — effort S — risk low — category: friction signal — wild
  Why: signals not authored by Sampo are steer-preferred. Assumption: the builder can be asked one question at close.
  Done when: each close stores a one-line "what Sampo made harder" from the agent, and a weekly count seeds self-edit candidates.

- **Roll back an edit automatically when outcomes get worse** — FEATURE — value 4 — effort M — risk med — category: self-edit safety
  Why: lineage marks choices provisional but nothing reverses them on evidence. Assumption: a per-edit before/after on `fm outcomes` is computable.
  Done when: a self-edit whose prediction misses at +14 days files a revert task with the numbers attached.

Next question: which self-edit surfaces (skills, hooks, gate, guard, prompts) have actually failed in the record, so the bar per surface is set from data rather than guessed?
