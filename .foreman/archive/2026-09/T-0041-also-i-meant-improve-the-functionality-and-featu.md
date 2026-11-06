---
id: T-0041
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-09-27T00:54:59Z
updated: 2026-09-27T01:02:48Z
base: bd86fd6a901ddc6ebe53cdade19ca7c92e6bd58f
---
# Brainstorm how Foreman makes Claude's project work smarter (planning, memory, grounding, verification, decisions, learning) and queue a grounded slate
## Raw request
> Also, I meant improve the functionality and feature set of foreman, so it makes everything wayyy smarter, etc.
## Interpretation
The user clarified that the self-improvement they want is functional: Foreman should make Claude's work on real projects much smarter (how it plans, remembers, grounds claims in the code, verifies, decides and learns across tasks and sessions), not more hardening of Foreman's own guard and state.
## Assumptions (confidence)
## Acceptance criteria
- [x] a grounded, scored slate recorded as research and turned into planned briefs — verify with ls ~/.claude/foreman/state/projects/foreman-4a056f/research | grep -c brainstorm
## Non-goals
## Approach (options → choice → why)
A) brainstorm skill: context pack + fm ideas (six tool-less lenses) + grounding + scoring. B) pick features directly from my own notes. Choice: A: the user asked for breadth ('everything wayyy smarter'), and independent lenses beat one viewpoint; grounding keeps it honest.
## Risks and rollback
## Execution prompt
## Steps
1. [x] context pack (what Foreman does for real project work today, where it's dumb)
2. [x] fm ideas across six lenses, merge, ground against the code, score
3. [x] record research, intake the slate, decide and start the queue
## Resume here
## Docs impact
none: research and planning only (brainstorm records in research/, briefs T-0043..T-0049 and inbox follow-ups); no code or docs changed
## Verification evidence
- (step 1) `wrote the context pack (scratchpad/pack-smarter.md, ~1,150 words)` → pack covers the user's words, what Foreman does, where it's dumb (grounded), constraints, open work [tree df8472520c8c] (2026-09-27T00:58:37Z)
- (step 2) `fm ideas --pack pack-smarter.md (six lenses) + grounding` → 6/6 lenses ok (~44 ideas); merged to 9 slate items; 2 premises false (secret redaction exists; hook bench exists) [tree df8472520c8c] (2026-09-27T00:58:37Z)
- (step 3) `ls state/projects/foreman-4a056f/research | grep -c brainstorm && fm state --json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d["inbox"]), "inbox")'` → exit 0 · 8 / 19 inbox [ran] [tree df8472520c8c] (2026-09-27T00:58:37Z)
- (ac 1) `ls ~/.claude/foreman/state/projects/foreman-4a056f/research | grep -c brainstorm` → exit 0 · 8 [ran] [tree df8472520c8c] (2026-09-27T00:58:37Z)
- (audit self) `self checklist: every slate item grounded against the code (grep/read); premises that were false dropped; recalled-text safety folded into recall; security item kept separate` → no findings [tree df8472520c8c] (2026-09-27T00:58:37Z)
- (audit intent) `fm-reviewer intent lens on the slate (t0041-slate-review)` → changes needed → item 9 (sensitive-path audits) is hardening: moved out of the slate to the normal SECURITY queue; fixes T-0040/42 kept but labelled plumbing [tree df8472520c8c] (2026-09-27T01:02:48Z)
- (audit maintainer) `fm-reviewer maintainer lens on the slate (t0041-slate-review)` → changes needed → map v1 name-based test links only, refreshed by fm commands (focus/done/map), never from a hook [tree df8472520c8c] (2026-09-27T01:02:48Z)
## Log
- 2026-09-27T00:54:59Z created
- 2026-09-27T00:55:07Z planned from capture
- 2026-09-27T00:55:23Z focused
- 2026-09-27T01:02:48Z steer (user): 'and also faster, way more token efficient, this one session has burned 20% of my weekly usage' → slate gains token-efficiency items; one combined review per round; evals only at the end; recursion bounded
- 2026-09-27T01:02:48Z done
## Follow-ups captured
