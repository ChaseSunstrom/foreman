---
id: T-2633
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T19:13:09Z
updated: 2026-11-02T19:22:45Z
base: b9b0f422ab014b065b755f202097dfc7f6f57ad1
base_tree: 789f470560f1405958022de9e20d7b99c22677ce
plan0_at: 2026-11-02T19:22:20Z
plan0_scope: []
verified: strong
---
# RESEARCH: usage is at 0% for this account, feel free to go wild — triage the 552-idea…
## Raw request
> RESEARCH: usage is at 0% for this account, feel free to go wild — triage the 552-idea brainstorm (research/brainstorm-20261102-121128): cluster, ground every cluster in the code, score, mark build or skip with a reason, record the catalogue, publish a checklist page, and turn the slate into briefs
## Interpretation
Reading 1 (chosen): the user's 'go wild' with usage free is the brainstorm skill's super mode: run fm ideas with ten lenses and four rounds, ground every idea, mark each cluster build or skip with a reason, show all of it on a checklist page, and queue every build mark. Reading 2 (ruled out): build ideas straight from the raw list. The brainstormers never saw the code, so ungrounded ideas would duplicate built work (104 of 552 were built already).
## Assumptions (confidence)
## Acceptance criteria
- [x] every idea of the run sits in a grounded cluster with a mark, recorded as research, and the build marks are queued tasks — verify with `sh -c 'set -o pipefail; test -s state/projects/foreman-4a056f/research/brainstorm-20261102.md && grep -c "^- \[" state/projects/foreman-4a056f/research/brainstorm-20261102.md | grep -qx 552'`
## Non-goals
## Approach (options → choice → why)
1) Three read-only recon agents ground the ideas in parallel, one per chunk, each clustering, grounding and scoring. Likely outcome: every idea placed with a file:line or task ground. 2) One agent for the whole run. Fails if: the context overflows and ideas drop silently, as when 400 ideas became seventeen rows in T-0364. 3) Ground only the near-T or wild ideas. Fails if: the skill forbids dropping any idea unseen. 4) Do less: a slate of eight with no page. Likely outcome: the user never sees the rest of the ideas. 5) Use what exists: fm ideas wrote ideas.md and its near-T marks; fm research add records the catalogue; fm intake files the slate. Likely outcome: no new tooling. Choice 1 built on 5 (85%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] ground, record, page, slate
## Resume here
## Docs impact
none: research only (the brainstorm catalogue in Foreman state and the triage page); no Foreman docs change.
## Verification evidence
- (ac 1) `sh -c 'set -o pipefail; test -s state/projects/foreman-4a056f/research/brainstorm-20261102.md && grep -c "^- \[" state/projects/foreman-4a056f/research/brainstorm-20261102.md | grep -qx 552'` → exit 0 · (no output) [ran] [tree 789f470560f1] [world 2f1906870a] (2026-11-02T19:22:36Z)
- (step 1) `sh -c 'set -o pipefail; grep -c "^- \[" state/projects/foreman-4a056f/research/brainstorm-20261102.md | grep -qx 552'` → exit 0 · (no output) [ran] [tree 789f470560f1] [world 2f1906870a] (2026-11-02T19:22:36Z)
- (audit intent) `self: three recon agents grounded every idea (172+254+126 = 552, none dropped), I merged their clusters, spot-checked two grounds (fmprove.py unproven verdicts; T-2611 ship record) and merged the two mutation clusters into one task` → the user's 'go wild' became the brainstorm skill's super mode: every idea grounded and shown, every build mark queued, the user's ticks able to overrule [tree 789f470560f1] (2026-11-02T19:22:36Z)
- (audit edge) `self: three recon agents grounded every idea (172+254+126 = 552, none dropped), I merged their clusters, spot-checked two grounds (fmprove.py unproven verdicts; T-2611 ship record) and merged the two mutation clusters into one task` → chunk B's agent read no foreman-ui code, so its UI clusters are the weakest grounded (all marked skip as polish; the page shows them for the user to overrule) [tree 789f470560f1] (2026-11-02T19:22:36Z)
- `sh -c 'set -o pipefail; grep -c "^- \[" state/projects/foreman-4a056f/research/brainstorm-20261102.md | grep -qx 552'` → exit 0 · (no output) [ran] [tree 789f470560f1] [world 2f1906870a] (2026-11-02T19:22:44Z)
- (audit intent) `self: three recon agents grounded every idea (172+254+126 = 552, none dropped), I merged their clusters, spot-checked two grounds (fmprove.py unproven verdicts; T-2611 ship record) and merged the two mutation clusters into one task` → the user's 'go wild' became the brainstorm skill's super mode: every idea grounded and shown, every build mark queued, the user's ticks able to overrule [tree 789f470560f1] (2026-11-02T19:22:44Z)
- (audit edge) `self: three recon agents grounded every idea (172+254+126 = 552, none dropped), I merged their clusters, spot-checked two grounds (fmprove.py unproven verdicts; T-2611 ship record) and merged the two mutation clusters into one task` → chunk B's agent read no foreman-ui code, so its UI clusters are the weakest grounded (all marked skip as polish; the page shows them for the user to overrule) [tree 789f470560f1] (2026-11-02T19:22:44Z)
## Log
- 2026-11-02T19:13:09Z created
- 2026-11-02T19:21:41Z planned: it has criteria and steps
- 2026-11-02T19:22:19Z focused
- 2026-11-02T19:22:29Z criterion 1 verify: `sh -c 'test -s state/projects/foreman-4a056f/research/brainstorm-20261102.md && grep -c "^- \[" state/projects/foreman-4a056f/research/brainstorm-20261102.md | grep -qx 552'` → `sh -c 'set -o pipefail; test -s state/projects/foreman-4a056f/research/brainstorm-20261102.md && grep -c "^- \[" state/projects/foreman-4a056f/research/brainstorm-20261102.md | grep -qx 552'`
- 2026-11-02T19:22:45Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2076 [FEATURE M, done, 2 steps] Brainstorms learn from what they missed: asks no idea predicted feed a blind-spots lens, and each run leaves questions for the next — l…
- decision 2026-10-21: Round 2 slate: all 25 build marks briefed and built in rounds, security first; 24 clusters skipped with reasons on the checklist page
- research mission-20261102-121118: Request: usage is at 0% for this account, feel free to go wild [stale: site/genesis/index.html changed since it was written]
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- the similar finished task took 2 steps
## Decision
All 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); 24 build marks became 23 queued tasks (T-2635..T-2657); 35 skips with reasons; the Foreman Idea Triage page (https://claude.ai/artifact/DWaxqfvZrbfCZiXiTmUBee) holds every cluster for the user's ticks.
## Lessons
- Ground a big brainstorm in parallel chunks with a fixed JSON shape and extract it straight from the transcript: 552 ideas placed with no idea lost and no file dump in the main context
