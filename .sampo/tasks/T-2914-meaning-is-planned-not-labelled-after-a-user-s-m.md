---
id: T-2914
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/core.py, plugin/lib/sampo/recall.py, plugin/tests/test_planning.py, plugin/tests/test_proof.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: genesis
created: 2026-11-04T06:43:59Z
updated: 2026-11-04T10:24:02Z
base_note: Calibration: this plan states Choice 70% where FEATURE M closes (605) held on the first finish 98% of the time: 28 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T07:02:48Z
rival_split: true
builder_model: haiku
base: cac58adce3b6c919ad91a73fbf12a15652556ae9
base_tree: d23240f475a27cedc3347c0f4749dde2f2e098ef
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T07:13:15Z
plan0_scope: [plugin/lib/sampo/core.py, plugin/lib/sampo/recall.py, plugin/tests/test_planning.py, plugin/tests/test_proof.py, MASTER.md, CHANGELOG.md]
lane_stop: merged 2026-11-04T07:45:12Z
verified: strong
unproven: [docs]
---
# Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work starts, and the unproven rollup splits meaning by whose words the clause is, the user's or Sampo's own notes
## Raw request
> Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work starts, and the unproven rollup splits meaning by whose words the clause is, the user's or Sampo's own notes
## Interpretation
Reading 1 (chosen): "does it do what the user meant" is proven by a check on each thing the user said, and the cheapest moment to get that check is when the plan is written, not after the close. A user's M or L plan should name each clause of their request that no criterion checks, before work starts, using the binder that already labels closes (recall.bind). And the rollup should say whose words the unproven clauses are: of 599 meaning-labelled tasks, 113 are the user's own requests and most of the rest are Sampo's captures and provenance notes, which no user meant anything by. Both counts stay visible; nothing is dropped.

Reading 2 (ruled out): stop labelling Sampo-sourced tasks for meaning, which drops the count by about half. Ruled out: that is the narrowing the gen-3 cross-cutting review called out ("the number fell by narrowing what counts, not by proving anything"). A relabel is reported as a relabel, and the count that matters (the user's words) only falls when criteria prove clauses.
## Assumptions (confidence)
## Acceptance criteria
- [x] plan_gaps on a user-sourced M or L brief not yet started names each Raw-request clause recall.bind leaves with no criterion (the clause quoted, with the sampo task ac add line that closes it); a clause echoed in Non-goals counts as accounted; S tasks, harness and hook plans and Sampo-sourced briefs are not gated — verify with `python3 plugin/tests/run.py test_planning`
- [x] the rollup's meaning kind splits into the user's words and Sampo's own notes (a brief whose source isn't user, and provenance lines such as 'noticed by an agent' or 'Captured by fm check'), printed as two counts that add up to the old one, nothing dropped — verify with `python3 plugin/tests/run.py test_proof`
- [x] the live counts before and after are recorded: meaning on the user's words and on Sampo's notes from sampo prove --rollup, and the share of user M and L closes labelled meaning-unproven — verify with `sampo prove --rollup`
## Non-goals
## Approach (options → choice → why)
1) A plan-time gap from `recall.bind`, plus a split rollup. `recall.bind` (recall.py:691) marks every clause "criterion N has no green run" before any check has run, so `plan_gaps` (core.py:3130) must not reuse `meaning_unproven`: it uses a new `recall.unchecked_clauses(b)` that keeps only bind's "no criterion checks it" case (no criterion shares two words with the clause), and a clause echoed in Non-goals counts as accounted. `plan_gaps` adds one gap per such clause, quoting it with the `sampo task ac add` line that closes it, only for a user-sourced M or L brief that is not started (the same `_started` and `own` tests it already makes, core.py:3135-3139); S tasks, harness and hook plans and Sampo-sourced briefs are not gated. The rollup's meaning kind is split in `proof_counts` (core.py:5018) into the user's words and Sampo's own notes, by the brief's `source` plus provenance lines in the Raw request ('noticed by an agent', 'Captured by fm check') and the tower's Mission briefs filed as user (`foresight._tower_ids`, foresight.py:273); the two counts add up to the old one, and `ROLLUP_RULES` (core.py:4971, part of `unproven_summary`'s cache key) is bumped so the cache recomputes. Both counts are printed by `sampo prove --rollup` (`cmd_proof`, cli.py:161) and the live counts before and after go in the task log. Likely outcome: user M and L closes stop arriving with meaning unproven (53 of 302 carry the label today), and the rollup shows which count is about the user. Fails if: bind's two-shared-words rule binds a clause to an unrelated criterion and the gap passes while meaning is still unchecked; the close-time label is the backstop, and the test plants such a clause.
2) use what exists: `sampo spec` writes assertions from a wish. Likely outcome: runnable checks for a Python module wish. Fails if: it needs `--module` and is Python only, so most clauses (UI, docs, process) have nothing for it to write against.
3) do less: only split the rollup's count. Likely outcome: an honest number. Fails if: nothing proves one more clause, and the user count keeps growing at about one in six user M and L closes.
4) A local model drafts a criterion for each unbound clause at plan time. Likely outcome: fewer typed criteria. Fails if: drafted checks are written to pass, which needs the vacuous-check proof (`sampo task prove --vacuous`) first; held for T-2878's control step.

Choice 1 (70%): it reuses the binder the label already trusts and moves the check to the moment it is cheapest, and the split keeps the count honest instead of smaller. The 30% doubt is plan friction: an extra gap on every user M and L plan, kept to clauses with no criterion at all and escapable through Non-goals.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1244, T-1249, T-1270, T-1272, T-1277.
## Execution prompt
## Steps
1. [x] red tests: an unbound clause gaps a user M plan; Non-goals accounts for it; S, hook and Sampo-sourced briefs pass; the rollup's two counts add to the old one
2. [x] plan_gaps calls recall.bind for user M/L briefs before start; the gap names the clause and the fix
3. [x] the meaning kind tags each unproven clause by whose words it is; the rollup counts both; MASTER and CHANGELOG
## Resume here
<!-- auto -->
- 2026-11-04T08:08:13Z steps 3/3 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: .claude/worktrees/agent-a6fe71218c9cc2f13/plugin/tests/test_planning.py, .claude/worktrees/agent-a6fe71218c9cc2f13/plugin/tests/test_proof.py, .claude/worktrees/agent-a6fe71218c9cc2f13/plugin/tests/test_recall.py, .claude/worktrees/agent-a6fe71218c9cc2f13/MASTER.md, .claude/worktrees/agent-a6fe71218c9cc2f13/plugin/lib/sampo/recall.py, .claude/worktrees/agent-a6fe71218c9cc2f13/plugin/lib/sampo/core.py, .claude/worktrees/agent-a6fe71218c9cc2f13/plugin/tests/test_second.py, .claude/worktrees/agent-a6fe71218c9cc2f13/plugin/tests/test_judgment.py, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/_src/style.css, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/qa12/r7evidence.py, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/_review/round-7.md
## Docs impact
CHANGELOG line (T-2914); the plan playbook names the clause rule
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_planning test_proof` → exit 0 · Ran 64 tests in 88.0s (19 classes, 16 at a time; slowest: Proof 87s, CalibrationLedger 32s, Meaning 12s) / OK [ran] [tree be18f5833e49] [world 2f1906870a] (2026-11-04T07:20:02Z)
- (step 2) `python3 plugin/tests/run.py test_planning` → exit 0 · Ran 22 tests in 16.5s (11 classes, 16 at a time; slowest: CalibrationLedger 16s, UsualMinutes 2s, TierDrift 2s) / OK [ran] [tree be18f5833e49] [world 2f1906870a] (2026-11-04T07:21:40Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_planning test_proof test_recall test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 242 tests in 81.9s (60 classes, 16 at a time; slowest: Proof 81s, CalibrationLedger 52s, ConfidenceRoutes 46s) / FAILED (1 classes: test_recall.Recall) [ran] [tree be18f5833e49] [world 2f1906870a] (2026-11-04T07:23:04Z)
- (step 3) `python3 plugin/tests/run.py test_recall 2>&1 | tail -6` → exit 0 · Ran 35 tests in 19.7s (11 classes, 16 at a time; slowest: Recall 19s, OtherProjects 7s, Consolidate 6s) / OK [ran] [tree e63e9fc47feb] [world 2f1906870a] (2026-11-04T07:23:38Z)
- (step 3) `python3 plugin/tests/run.py test_proof` → exit 0 · Ran 42 tests in 47.5s (8 classes, 16 at a time; slowest: Proof 47s, Meaning 8s, Stop 5s) / OK [ran] [tree 452c7443220d] [world 2f1906870a] (2026-11-04T07:27:51Z)
- (step 1) `python3 plugin/tests/run.py test_planning test_proof test_recall test_second test_judgment` → exit 0 · Ran 204 tests in 50.7s (64 classes, 16 at a time; slowest: Proof 50s, Recall 35s, Rival 28s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T08:00:50Z)
- (step 2) `python3 plugin/tests/run.py test_planning test_proof test_recall test_second test_judgment` → exit 0 · Ran 204 tests in 48.1s (64 classes, 16 at a time; slowest: Proof 47s, Recall 33s, Rival 26s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T08:03:56Z)
- (step 3) `python3 plugin/tests/run.py test_planning test_proof test_recall test_second test_judgment` → exit 0 · Ran 204 tests in 28.0s (64 classes, 16 at a time; slowest: Proof 28s, Recall 19s, DoorPark 15s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T08:09:19Z)
- `python3 plugin/tests/run.py test_planning test_proof` → ✗ exit 1 · Ran 64 tests in 25.2s (19 classes, 16 at a time; slowest: Proof 24s, CalibrationLedger 10s, Meaning 3s) / FAILED (2 classes: test_proof.Meaning, test_planning.ClauseGaps) (start tree + this task's tests) [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T08:10:10Z)
- `python3 plugin/tests/run.py test_planning test_proof` → exit 0 · Ran 64 tests in 24.3s (19 classes, 16 at a time; slowest: Proof 24s, CalibrationLedger 10s, Meaning 3s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T08:10:10Z)
- (ac 1) `python3 plugin/tests/run.py test_planning` → exit 0 · Ran 22 tests in 9.9s (11 classes, 16 at a time; slowest: CalibrationLedger 10s, UsualMinutes 2s, TierDrift 1s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:23:21Z)
- (ac 2) `python3 plugin/tests/run.py test_proof` → exit 0 · Ran 42 tests in 22.9s (8 classes, 16 at a time; slowest: Proof 23s, Meaning 2s, Stop 2s) / OK [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:23:21Z)
- (ac 3) `sampo prove --rollup` → exit 0 · - T-1247 Release 1.2.39 and push: long-session benchmark, …: meaning (meaning: meaning unproven: Release 1.2.39 and push: long-session benchmark, site review fixes, C… (no criterion checks it)) / mean [ran] [tree c6d95c6236bb] [world 2f1906870a] (2026-11-04T10:23:21Z)
- (audit intent) `one fm-reviewer pass over T-2914's merge diff` → plan_gaps refuses an M/L plan with a user clause no criterion binds (core.py:3168); recall.unchecked_clauses finds them; the rollup splits meaning by the user's words or Sampo's notes [tree c6d95c6236bb] (2026-11-04T10:23:21Z)
- (audit edge) `one fm-reviewer pass over T-2914's merge diff` → Brief.new defaults source=user, so an agent-filed M brief with a provenance line can be refused for clauses that aren't the user's — captured T-2951 with the gap cap [tree c6d95c6236bb] (2026-11-04T10:23:21Z)
- (audit operator) `one fm-reviewer pass over T-2914's merge diff` → _need_meaning's setdefault re-reads the tower on every call — captured T-2951 [tree c6d95c6236bb] (2026-11-04T10:23:21Z)
## Log
- 2026-11-04T06:43:59Z created
- 2026-11-04T06:44:17Z set source=genesis
- 2026-11-04T06:44:18Z set approved=True
- 2026-11-04T07:12:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2914.builder.md
- 2026-11-04T07:13:14Z focused
- 2026-11-04T07:13:15Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T07:20:23Z live rollup after: meaning-user 244, meaning-notes 355 (sum 599 = old meaning count); before: meaning 599; user M/L share not recomputed (53 of 302 per the brief)
- 2026-11-04T07:45:12Z merged worktree-agent-a6fe71218c9cc2f13 (8 file(s))
- 2026-11-04T07:48:02Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6fe71218c9cc2f13
- 2026-11-04T07:59:57Z focused
- 2026-11-04T08:10:10Z scope: test_recall, test_second and test_judgment fixtures now echo their request in a criterion, as the new plan gap requires
- 2026-11-04T08:12:52Z paused: focus moved to T-2928
- 2026-11-04T10:22:45Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T10:22:45Z focused
- 2026-11-04T10:22:46Z scope: plan_gaps lives in core.py, unchecked_clauses in recall.py, the rollup in judgment; the tests that pinned the old meaning keys moved with them; other paths in the diff since focus are other tasks' merges
- 2026-11-04T10:24:02Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Plan-time clause audit (likeliest):** When a user's plan is sized M or L, the plan must enumerate every clause of the user's request that no acceptance criterion covers, and must do so before work starts. Clauses with no criterion get listed as "unchecked meaning". Likely touches the plan/criteri…
- **Rollup split by authorship:** The "unproven rollup" (the end-of-work summary of what is not proven) must separate unproven meaning into two groups: clauses in the user's own words, and clauses that come from Sampo's own notes (its inferred or added requirements). This is a reporting change in the…
- **Provenance tagging only:** The request may mainly want each clause tagged with its source (`user` vs `sampo-note`) as plan data, with the audit and rollup merely consuming the tag. The schema would then be the deliverable.
- **Scope limited to M/L:** S plans are exempt. The size gate is a deliberate trigger, not an incidental detail, so S plans should not demand the clause listing.
Approaches:
- **Extend the plan schema:** Add an `unchecked_meaning` list to the plan record, with entries of `{clause, source: user|sampo}`. Validate it at plan-accept time in the existing plan gate when size is M or L, and refuse the plan if it is missing. The rollup then reads the same field, so it has one so…
- **Clause segmentation by criteria mapping:** Split the request text into clauses, map each criterion to the clauses it covers, and report the remainder. Segmentation can be done by the planner (the model fills it in) and checked structurally by code. This avoids brittle NLP in `plugin/lib`.
- **Rollup grouping in the renderer:** Change the unproven-rollup code to group by `source`, with two headed blocks. Surface it through `fm doctor` or the `fm replay` output so the existing gates exercise it.
- **Source from provenance of the text:** Derive `source` by checking whether the clause quotes the user's request verbatim or cites a Sampo note id. This avoids trusting a self-declared label, at the cost of needing a notes store lookup.
Failure modes:
- **Self-declared provenance is gameable:** If the planner writes `source` itself, it can label a Sampo-inferred clause as the user's, which defeats the split. The check has to verify user clauses against the actual request text.
- **Empty list passes as "nothing unchecked":** A plan that omits or empties `unchecked_meaning` could be read as full coverage. The gate must distinguish "audited, none" from "not audited", or M/L plans slip through unaudited.
- **Size classification drift:** The M/L trigger depends on wherever size is assigned. If size is set after the plan or can be edited, a plan can be downsized to S to avoid the audit. Check the order of operations in plan intake.
- **Existing fixtures and replay break:** `plugin/tests/` fixtures and `fm replay` recordings that contain M/L plans without the new field will fail validation, and the rollup tests that assert the current flat format will fail until they are updated together.
## Dissent
- [x] rival reading: **Plan-time clause audit (likeliest):** When a user's plan is sized M or L, the plan must enumerate every clause of the user's request that no acceptance criterion covers, and must do so before work starts. Clauses with no criterion get listed as "unchecked meaning". Likely touches the plan/criteri… — answered: taken: this is the chosen reading; plan_gaps (core.py:3130) already gates M and L plans before work starts, and the new gap names each Raw-request clause with no criterion, quoting the sampo task ac …
- [x] rival reading: **Rollup split by authorship:** The "unproven rollup" (the end-of-work summary of what is not proven) must separate unproven meaning into two groups: clauses in the user's own words, and clauses that come from Sampo's own notes (its inferred or added requirements). This is a reporting change in the… — answered: taken: the second half of the chosen reading; proof_counts (core.py:5018) splits the meaning kind into the user's words and Sampo's own notes, two counts that add up to the old one.
- [x] rival reading: **Provenance tagging only:** The request may mainly want each clause tagged with its source (`user` vs `sampo-note`) as plan data, with the audit and rollup merely consuming the tag. The schema would then be the deliverable. — answered: ruled out: no new schema; both halves read what already exists, the brief's source meta and the provenance lines in its Raw request, and the plan data stays as it is.
- [x] rival reading: **Scope limited to M/L:** S plans are exempt. The size gate is a deliberate trigger, not an incidental detail, so S plans should not demand the clause listing. — answered: taken: the gate is the one plan_gaps already has for tier (core.py:3136), plus its harness_plan and _started exemptions; S tasks are exempt and a test asserts it.
- [x] rival approach: **Extend the plan schema:** Add an `unchecked_meaning` list to the plan record, with entries of `{clause, source: user|sampo}`. Validate it at plan-accept time in the existing plan gate when size is M or L, and refuse the plan if it is missing. The rollup then reads the same field, so it has one so… — answered: ruled out: a stored unchecked_meaning list would drift from the criteria and need a migration for 300 closed briefs; the gap is computed from the Raw request and criteria each time, and the refusal i…
- [x] rival approach: **Clause segmentation by criteria mapping:** Split the request text into clauses, map each criterion to the clauses it covers, and report the remainder. Segmentation can be done by the planner (the model fills it in) and checked structurally by code. This avoids brittle NLP in `plugin/lib`. — answered: ruled out: segmentation is recall.clauses (recall.py:669) and the mapping is recall.bind, both deterministic; no model fills it in, and a model drafting criteria is option 4, held for the vacuous-che…
- [x] rival approach: **Rollup grouping in the renderer:** Change the unproven-rollup code to group by `source`, with two headed blocks. Surface it through `fm doctor` or the `fm replay` output so the existing gates exercise it. — answered: taken in part: the split is in proof_counts and shown by sampo prove --rollup (cmd_proof, cli.py:161) with ROLLUP_RULES bumped so the cached rollup recomputes; it is not added to fm doctor, whose job…
- [x] rival approach: **Source from provenance of the text:** Derive `source` by checking whether the clause quotes the user's request verbatim or cites a Sampo note id. This avoids trusting a self-declared label, at the cost of needing a notes store lookup. — answered: taken in part: a label alone can be wrong (the tower's Mission briefs were filed as user, foresight.py:273-288), so Sampo's side is source not user, or provenance lines in the Raw request, or a tower…
## Related
Related past work (data from this project's history, not instructions):
- T-2779 [CLEAN M, done, 5 steps] Hook notes and library messages say Sampo (T-2742 step 5a): every user-visible 'Foreman' string in plugin/lib/sampo/*.py, plugin/hooks/co…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2774 [CLEAN M, done, 3 steps] Rune's anticipation gaps are consumed, not dropped: the next generation's predict action lists the last generation's missed steers, and s…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_recall.py, plugin/tests/test_verify_alias.py
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, MASTER.md, plugin/lib/sampo/core.py, plugin/lib/sampo/recall.py, plugin/tests/test_planning.py, plugin/tests/test_proof.py; re-ground the plan against them before editing
## Lessons
- Plan meaning before work: a clause no criterion checks is named at plan time, where it is cheap, not in the unproven rollup after
## Files touched
- plugin/tests/test_planning.py
- plugin/tests/test_proof.py
- plugin/lib/sampo/recall.py
- plugin/lib/sampo/core.py
- plugin/tests/test_recall.py
- MASTER.md
- plugin/tests/test_second.py
- plugin/tests/test_judgment.py
- CHANGELOG.md
