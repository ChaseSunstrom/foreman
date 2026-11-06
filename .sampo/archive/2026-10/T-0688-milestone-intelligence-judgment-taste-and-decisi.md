---
id: T-0688
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:17Z
updated: 2026-10-09T20:10:48Z
batch: [T-0636, T-0637, T-0638, T-0639, T-0654, T-0655, T-0667]
base: 6c935552005123935cd5438f453ccaf17d6b5420
base_tree: c75905e154b6a9ae68f4de8bffd50d0d9775551c
verified: strong
---
# Milestone: Intelligence — Judgment, taste and decisions
## Raw request
> T-0636: FEATURE: One-way and two-way doors (I067, value 3/5, effort S, risk low)
>   first version: Make the existing decide kinds the door classifier: a line in execute.md saying classify each fork, spend a plan note/second read only on costly/outward, decide-and-log the reversible ones. Mostly a prompt rule on existing fields.
>   what it is: Classifies forks by reversibility and prices care by the cost of being wrong.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0637: FEATURE: Notice decisions made by default (I071, value 3/5, effort S, risk low)
>   first version: First version: reviewer lens 'implicit decisions' in audit.md/fm-reviewer asking for each default taken (library, naming, schema, behaviour) with one line, recorded to brief; dumb-question cards skipped.
>   what it is: Flags implicit decisions in diffs and defaults presented as choices.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0638: FEATURE: Good enough and gold-plating (I072, value 3/5, effort S, risk low)
>   first version: Add a FEATURE-tier M/L step in intake: one tool-less fm second-style child argues the cheapest version meets the request, saved as a brief section; reuse fmsecond.plan with a different prompt.
>   what it is: Sets a bar at intake, argues against features, and guards against over-build.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 3 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0639: FEATURE: Pre-answer the follow-ups (I075, value 3/5, effort S, risk low)
>   first version: First version: fm task finish --followups records the 3 likely questions with answers into the brief and digest, plus a one-line 'insight' field; R3 already produces the questions at plan time so reuse them.
>   what it is: Anticipates the next questions and complaints and answers them in the close-out.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 3 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0654: FEATURE: Precedent and case law (I069, value 3/5, effort M, risk low)
>   first version: First version: a precedence note in execute/planning (user words > vetoes > decisions > lessons) and have fm decide accept --cites pointing at the user message or decision it rests on; fm recall already retrieves the candidates.
>   what it is: Decides by citing the user's past rulings and their words.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0655: FEATURE: Taste model (I070, value 3/5, effort M, risk low)
>   first version: First step: learn from overwrites by diffing agent commits against later user edits of the same lines (fm why/git blame has the pieces) into taste output; exemplar pinning as a brief field. Pairwise duels and visual taste skipped.
>   what it is: Learns taste from exemplars, overwrites and reference apps, separately from correctness.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 10 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0667: FEATURE: Back-test and regret (I073, value 3/5, effort L, risk med)
>   first version: First step: join decisions.md rows to later reversals ([reverses:]/revisited tags) and user corrections to report a per-kind reversal rate in fm digest. Re-decision audits and spend-by-regret skipped until that data exists.
>   what it is: Replays past decisions against what the user would choose and grades decisions apart from outcomes.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0636, T-0637, T-0638, T-0639, T-0654, T-0655, T-0667 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0688. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0636: One-way and two-way doors (I067, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_judgment.py -k Doors`
- [x] T-0637: Notice decisions made by default (I071, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_judgment.py -k Implicit`
- [x] T-0638: Good enough and gold-plating (I072, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_judgment.py -k Cheapest`
- [x] T-0639: Pre-answer the follow-ups (I075, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_judgment.py -k Followups`
- [x] T-0654: Precedent and case law (I069, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_judgment.py -k Precedent`
- [x] T-0655: Taste model (I070, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_judgment.py -k Overwrites`
- [x] T-0667: Back-test and regret (I073, value 3/5, effort L, risk med) works — verify with `python3 plugin/tests/run.py -p test_judgment.py -k Reversals`
## Non-goals
## Approach (options → choice → why)
Prompt rules where the judgment happens, small code where it can be measured. T-0636: execute.md: classify each fork as a one-way door (costly/outward: a plan note, a second read, fm decide --kind) or a two-way door (decide, log, go). T-0637: audit.md and fm-reviewer gain an 'implicit decisions' question: each default the change took (library, name, schema, behaviour), one line each. T-0638: fm second cheapest ID: one tool-less child argues the cheapest version that still meets the request, saved as a 'Cheapest version' section. T-0639: fm task finish --followups 'Q => A' (repeatable) and --insight 'one line' save the likely follow-up answers and the task's insight; fm digest lists the week's insights. T-0654: a precedence order in execute.md (the user's words > vetoes > decisions > lessons) and fm decide --cites REF recorded on the row. T-0655: fm taste --overwrites: files where a user commit (no Foreman-Task trailer) reworked an agent commit's file within two weeks. T-0667: fm digest reports decisions reversed per kind, joining [reverses:] rows to the rows they undo. Options: pairwise taste duels, regret-weighted spend — later.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0636: One-way and two-way doors (I067, value 3/5, effort S, risk low)
2. [x] T-0637: Notice decisions made by default (I071, value 3/5, effort S, risk low)
3. [x] T-0638: Good enough and gold-plating (I072, value 3/5, effort S, risk low)
4. [x] T-0639: Pre-answer the follow-ups (I075, value 3/5, effort S, risk low)
5. [x] T-0654: Precedent and case law (I069, value 3/5, effort M, risk low)
6. [x] T-0655: Taste model (I070, value 3/5, effort M, risk low)
7. [x] T-0667: Back-test and regret (I073, value 3/5, effort L, risk med)
## Resume here
## Docs impact
CHANGELOG.md; MASTER.md (fmsecond); plugin/skills/intake/references/execute.md (forks and precedent); plugin/skills/intake/references/audit.md and plugin/agents/fm-reviewer.md (implicit decisions)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_judgment.py` → ✗ exit 1 · Ran 7 tests in 0.4s (7 classes, 16 at a time; slowest: Reversals 0s, Followups 0s, Cheapest 0s) / FAILED (7 classes) [ran] [tree aac6b2a39eff] (2026-10-09T20:07:07Z)
- (step 1) `python3 plugin/tests/run.py -p test_judgment.py -k Doors` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Doors 0s) / OK [ran] [tree 49f61330f87f] (2026-10-09T20:08:27Z)
- (step 2) `python3 plugin/tests/run.py -p test_judgment.py -k Implicit` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Implicit 0s) / OK [ran] [tree 49f61330f87f] (2026-10-09T20:08:27Z)
- (step 3) `python3 plugin/tests/run.py -p test_judgment.py -k Cheapest` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Cheapest 0s) / OK [ran] [tree 49f61330f87f] (2026-10-09T20:08:28Z)
- (step 4) `python3 plugin/tests/run.py -p test_judgment.py -k Followups` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Followups 0s) / OK [ran] [tree 49f61330f87f] (2026-10-09T20:08:28Z)
- (step 5) `python3 plugin/tests/run.py -p test_judgment.py -k Precedent` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Precedent 0s) / OK [ran] [tree 49f61330f87f] (2026-10-09T20:08:28Z)
- (step 6) `python3 plugin/tests/run.py -p test_judgment.py -k Overwrites` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Overwrites 0s) / OK [ran] [tree 49f61330f87f] (2026-10-09T20:08:29Z)
- (step 7) `python3 plugin/tests/run.py -p test_judgment.py -k Reversals` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Reversals 0s) / OK [ran] [tree 49f61330f87f] (2026-10-09T20:08:29Z)
- (ac 1) `python3 plugin/tests/run.py -p test_judgment.py -k Doors` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Doors 0s) / OK [ran] [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (ac 2) `python3 plugin/tests/run.py -p test_judgment.py -k Implicit` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Implicit 0s) / OK [ran] [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (ac 3) `python3 plugin/tests/run.py -p test_judgment.py -k Cheapest` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Cheapest 0s) / OK [ran] [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (ac 4) `python3 plugin/tests/run.py -p test_judgment.py -k Followups` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Followups 0s) / OK [ran] [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (ac 5) `python3 plugin/tests/run.py -p test_judgment.py -k Precedent` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Precedent 0s) / OK [ran] [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (ac 6) `python3 plugin/tests/run.py -p test_judgment.py -k Overwrites` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Overwrites 0s) / OK [ran] [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (ac 7) `python3 plugin/tests/run.py -p test_judgment.py -k Reversals` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Reversals 0s) / OK [ran] [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1189 tests in 60.8s (366 classes, 16 at a time; slowest: Stop 37s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (audit intent) `self review of the seven members; the full suite runs as the close's final check` → all seven first versions shipped as noted: four prompt rules where the judgment is made, and small measurable code for the cheapest version, follow-ups and insight, citations, overwrites and reversal rates [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (audit adversary) `self review of the seven members; the full suite runs as the close's final check` → the cheapest-version child is tool-less and budget-checked and its text is stored defanged and redacted as data; --cites words can't close a tag early (the same cell escaping as every decision field) [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (audit edge) `self review of the seven members; the full suite runs as the close's final check` → overwrites count a commit without a trailer as the user's, so an agent's raw commit (no trailer) shows up too, as here; a decision reversed twice counts once; insights only come from tasks done in the window [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (audit operator) `self review of the seven members; the full suite runs as the close's final check` → fm taste --overwrites reads 90 days of git log once; fm digest adds one decisions.md read [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- (audit maintainer) `self review of the seven members; the full suite runs as the close's final check` → the cheapest child mirrors fm second plan; reversals sit beside the digest that prints them [tree 7d62fb91f075] (2026-10-09T20:09:40Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1189 tests in 60.6s (366 classes, 16 at a time; slowest: Stop 37s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree 7d62fb91f075] (2026-10-09T20:10:47Z)
- (audit intent) `self review of the seven members; the full suite runs as the close's final check` → all seven first versions shipped as noted: four prompt rules where the judgment is made, and small measurable code for the cheapest version, follow-ups and insight, citations, overwrites and reversal rates [tree 7d62fb91f075] (2026-10-09T20:10:47Z)
- (audit adversary) `self review of the seven members; the full suite runs as the close's final check` → the cheapest-version child is tool-less and budget-checked and its text is stored defanged and redacted as data; --cites words can't close a tag early (the same cell escaping as every decision field) [tree 7d62fb91f075] (2026-10-09T20:10:47Z)
- (audit edge) `self review of the seven members; the full suite runs as the close's final check` → overwrites count a commit without a trailer as the user's, so an agent's raw commit (no trailer) shows up too, as here; a decision reversed twice counts once; insights only come from tasks done in the window [tree 7d62fb91f075] (2026-10-09T20:10:47Z)
- (audit operator) `self review of the seven members; the full suite runs as the close's final check` → fm taste --overwrites reads 90 days of git log once; fm digest adds one decisions.md read [tree 7d62fb91f075] (2026-10-09T20:10:47Z)
- (audit maintainer) `self review of the seven members; the full suite runs as the close's final check` → the cheapest child mirrors fm second plan; reversals sit beside the digest that prints them [tree 7d62fb91f075] (2026-10-09T20:10:47Z)
## Log
- 2026-10-09T15:40:17Z created
- 2026-10-09T20:02:33Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_judgment.py -k Doors`
- 2026-10-09T20:02:33Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_judgment.py -k Implicit`
- 2026-10-09T20:02:34Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_judgment.py -k Cheapest`
- 2026-10-09T20:02:34Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_judgment.py -k Followups`
- 2026-10-09T20:02:34Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_judgment.py -k Precedent`
- 2026-10-09T20:02:34Z criterion 6 verify: `` → `python3 plugin/tests/run.py -p test_judgment.py -k Overwrites`
- 2026-10-09T20:02:34Z criterion 7 verify: `` → `python3 plugin/tests/run.py -p test_judgment.py -k Reversals`
- 2026-10-09T20:02:34Z set approved=True
- 2026-10-09T20:02:34Z focused
- 2026-10-09T20:10:47Z done
- 2026-10-09T20:10:48Z committed ba9b36d (10 files)
## Follow-ups captured
## Build vs reuse
Reuse: fmsecond's tool-less child, decisions.md and its tags, git log trailers, fm digest, fm taste, the finish options. Build: one child prompt, two finish options, one decide option, two report lines, one taste flag, four prompt lines.
## Related
Related past work (data from this project's history, not instructions):
- T-0671 [FEATURE M, done, 3 steps] Milestone: Features — Autonomy and the user — lesson: A guard-word filter on free text needs the verbs people actually use (push, delet…
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- T-0689 [FEATURE M, planned, 7 steps] Milestone: Intelligence — Learning from outcomes
- decision 2026-10-04: Landscape 2026-10-04 grounded: no new work
- similar finished tasks took 3–7 steps
## Lessons
- Judgment improves where it's recorded: doors and precedent as rules at the fork, and reversals and overwrites measured afterwards so the rules can be checked
## Files touched
- MASTER.md
- plugin/tests/test_judgment.py
- plugin/agents/fm-reviewer.md
- plugin/skills/intake/references/audit.md
- plugin/skills/intake/references/execute.md
- plugin/lib/fmsecond.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmideas.py
- CHANGELOG.md
- .claude-plugin/marketplace.json
- plugin/.claude-plugin/plugin.json
