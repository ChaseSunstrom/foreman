---
id: T-1331
type: RESEARCH
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T03:24:34Z
updated: 2026-11-06T03:53:03Z
base: 25e56aed6c517b74a658d5daa62d7dd508ef0bc4
base_tree: 2ed17ecfc2032c26fbb44cbccdedfc467000acb7
plan0_at: 2026-10-21T05:46:59Z
plan0_scope: []
paused_tree: 2ed17ecfc2032c26fbb44cbccdedfc467000acb7
---
# Super recursive brainstorm of fm code: every idea grounded and scored, the slate built in rounds, re-brainstormed until dry
## Raw request
> super recursive brainstorm fm code, etc., and I shouldn't even need to ask you to do this, foreman should be able to figure it out, etc. again, I shouldn't even need to say anything
## Interpretation
The user asked for a super recursive brainstorm of fm code. Round 1 ran (fm ideas, 10 lenses, 4 rounds, 3 deepened: 522 distinct ideas in research/brainstorm-20261020-222518). Recursive: build the slate, then brainstorm the improved fm code again past every earlier ideas.md, until a round's grounded yield is under about three ideas of real value.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the round-1 catalogue is recorded with every one of the 522 ideas placed in a cluster with its grounding, score and mark — verify with `test -s state/projects/foreman-4a056f/research/brainstorm-fm-code-catalogue.md`
- [ ] each build cluster has a brief in the queue and the catalogue is published as a checklist page — verify with `fm queue --json`
- [ ] the round-1 catalogue is recorded with every idea placed in a cluster with its grounding, score and mark — verify with `test -s state/projects/foreman-4a056f/research/brainstorm-fm-code-catalogue.md`
- [ ] each build cluster has a brief in the queue — verify with `fm queue --json`
## Non-goals
## Approach (options → choice → why)
Grounding by two agents in parallel (runners/setup/reliability/projects; UI/experience), each clustering its half, citing code for done/partial, scoring value/effort/risk and marking build or skip. Merged into one catalogue (fm research add), every idea placed, none dropped silently; build clusters become briefs (fm intake), the rest inbox follow-ups; the catalogue as a checklist page for the user. Then build rounds (T-1326..T-1330 first), and fm ideas --rounds 2 --seen each earlier ideas.md after each round until dry, recorded with fm decide.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Ground both halves (agents) and merge into one catalogue
2. [x] Briefs for the build clusters; follow-ups for the rest; checklist page
3. [ ] After each build round, brainstorm again past every earlier ideas.md until dry
4. [x] Ground both halves and merge into one catalogue
5. [x] Briefs for the build clusters; follow-ups for the rest; checklist page
6. [ ] After each build round, brainstorm again past every earlier ideas.md until dry  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/brainstorm-fm-code-catalogue.md` → exit 0 · (no output) [ran] [tree 2ed17ecfc203] (2026-10-21T05:47:39Z)
- (step 4) `test -s state/projects/foreman-4a056f/research/brainstorm-fm-code-catalogue.md` → exit 0 · (no output) [ran] [tree 2ed17ecfc203] (2026-10-21T05:47:40Z)
- (step 2) `fm inbox | grep -cE 'T-13(3[3-9]|4[0-9]|5[0-9]|6[01])'` → exit 0 · 29 [ran] [tree 2ed17ecfc203] (2026-10-21T05:47:41Z)
- (step 5) `fm inbox | grep -cE 'T-13(3[3-9]|4[0-9]|5[0-9]|6[01])'` → exit 0 · 29 [ran] [tree 2ed17ecfc203] (2026-10-21T05:47:43Z)
## Log
- 2026-10-21T03:24:34Z created
- 2026-10-21T03:43:15Z planned from capture
- 2026-10-21T03:48:12Z catalogue recorded (research/brainstorm-fm-code-catalogue.md): 47 clusters, every one of the 522 ideas placed; 29 build briefs queued T-1333..T-1361 (overlaps merged: R14+U10, R15+U9, R5+U16, R7+U5, R8+U14, R9+U25, R18+U21, R22+U22, R22+U18, R17+U20, U2+R16); planned clusters folded into T-1327..T-1332 and T-1305/T-1308 steers; 8 skips with reasons (R19, R20, R21, R23, U12, U24, and parts noted in briefs)
- 2026-10-21T05:46:58Z focused
- 2026-10-21T05:47:43Z checklist page https://claude.ai/artifact/TR2GpiKuf7xV2yBpU7EYCs has no ticks yet (choices {}): order stays value-for-effort
- 2026-10-21T05:47:45Z blocked: step 3 (re-brainstorm past every earlier ideas.md) runs once the current build round lands: T-1329, T-1330, then the slate's inbox briefs T-1333..T-1361 by value
- 2026-10-21T06:26:49Z T-1364 fixed the cause; this brief's own duplicated criteria and steps are left as they are (steps 1, 2, 4 and 5 carry evidence): tidy them when it unblocks
- 2026-11-06T03:53:03Z unblocked
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The acceptance criteria and steps are duplicated (criteria 1 and 3 are near-identical; criteria 2 and 4 likewise; steps 1-3 repeat as 4-6), so progress tracking is ambiguous and the CURRENT marker could re-run the grounding step. — Collapse to one set of 3 steps and 2 or 3 criteria, and keep …
- HIGH: The "every one of the 522 ideas placed" criterion is checked only by `test -s` on the file, which proves nothing beyond non-empty; a catalogue with 40 ideas would pass. — Add a check that counts distinct idea IDs in the catalogue against the 522 in the round-1 ideas.md (e.g. a grep/diff of ID…
- HIGH: "Recursive until dry" has no stop rule that can be verified, and the budget is $12.5 with a "$0 spent" counter and 15M tokens. Two grounding agents over 522 ideas plus open-ended re-brainstorm rounds could exhaust it with no partial deliverable. — Set a hard cap on rounds (e.g. 2 beyond round…
- MEDIUM: The "fm queue --json" criterion proves only that something is queued, not that each build cluster has a brief, and it can't confirm the checklist page exists. — Define the expected cluster count from the catalogue and assert the queue has that many briefs tagged to the catalogue. Separately…
- MEDIUM: Step 3 depends on build rounds (T-1326..T-1330) that are other tasks, so this research task's completion is gated on work outside its control, and the brainstorm "after each build round" can't finish here. — Split the recursive re-brainstorm into its own follow-up task, or define this task …
- LOW: Publishing the checklist page and creating queue briefs/inbox follow-ups are outward-facing, and the plan has no rollback or dedupe guard if the merge is rerun. — Make `fm intake` idempotent by keying on cluster ID and checking the queue first, and note how to remove created briefs if the cata…
Verdict: revise — the work direction is sound, but the criteria are duplicated and weak, and the open-ended recursion lacks a budget cap and a verifiable stop.
## Dissent
- [ ] HIGH: The acceptance criteria and steps are duplicated (criteria 1 and 3 are near-identical; criteria 2 and 4 likewise; steps 1-3 repeat as 4-6), so progress tracking is ambiguous and the CURRENT marker could re-run the grounding step. — Collapse to one set of 3 steps and 2 or 3 criteria, and keep …
- [ ] HIGH: The "every one of the 522 ideas placed" criterion is checked only by `test -s` on the file, which proves nothing beyond non-empty; a catalogue with 40 ideas would pass. — Add a check that counts distinct idea IDs in the catalogue against the 522 in the round-1 ideas.md (e.g. a grep/diff of ID…
- [ ] HIGH: "Recursive until dry" has no stop rule that can be verified, and the budget is $12.5 with a "$0 spent" counter and 15M tokens. Two grounding agents over 522 ideas plus open-ended re-brainstorm rounds could exhaust it with no partial deliverable. — Set a hard cap on rounds (e.g. 2 beyond round…
- [ ] MEDIUM: The "fm queue --json" criterion proves only that something is queued, not that each build cluster has a brief, and it can't confirm the checklist page exists. — Define the expected cluster count from the catalogue and assert the queue has that many briefs tagged to the catalogue. Separately…
- [ ] MEDIUM: Step 3 depends on build rounds (T-1326..T-1330) that are other tasks, so this research task's completion is gated on work outside its control, and the brainstorm "after each build round" can't finish here. — Split the recursive re-brainstorm into its own follow-up task, or define this task …
- [ ] LOW: Publishing the checklist page and creating queue briefs/inbox follow-ups are outward-facing, and the plan has no rollback or dedupe guard if the merge is rerun. — Make `fm intake` idempotent by keying on cluster ID and checking the queue first, and note how to remove created briefs if the cata…
## Related
Related past work (data from this project's history, not instructions):
- T-1029 [RESEARCH L, done, 5 steps] Super recursive brainstorm: anything on the table to make Foreman super good; build, revie — lesson: Show the whole catalogue, not a s…
- T-1332 [FEATURE M, done, 2 steps] Foreman notices on its own when a feature area needs a brainstorm and an improvement round — lesson: Friction is a signal to act on, no…
- research mission-20261020-222446: Request: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage AN…
- decision 2026-10-20: The recursive brainstorm loop is dry after round 1: a two-lens probe past the 368 earlier ideas gave 51 titles, 2 of real value after grounding (rep…
