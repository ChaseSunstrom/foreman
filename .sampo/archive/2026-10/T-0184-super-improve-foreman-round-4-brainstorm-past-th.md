---
id: T-0184
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T19:09:46Z
updated: 2026-10-03T19:12:24Z
verified: strong
---
# Super-improve Foreman: round 4 brainstorm past the 152 earlier ideas, grounded slate
## Raw request
> Super-improve Foreman: round 4 brainstorm past the 152 earlier ideas, grounded slate
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a grounded slate of new ideas is recorded — verify with `test -n "$(ls -d state/projects/foreman-4a056f/research/brainstorm-2026100[3-9]-* 2>/dev/null)"`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ideas super round past earlier ideas
2. [x] ground, score, slate into briefs
## Resume here
## Docs impact
none: research only; the slate's tasks will document what they change
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/brainstorm-20261003-140947/ideas.md` → exit 0 · (no output) [ran] [tree aa2faea47d3b] (2026-10-03T19:12:12Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/brainstorm-20261003-round4.md || ls state/projects/foreman-4a056f/research/ | grep -q round4` → exit 0 · (no output) [ran] [tree aa2faea47d3b] (2026-10-03T19:12:12Z)
- (ac 1) `test -n "$(ls -d state/projects/foreman-4a056f/research/brainstorm-2026100[3-9]-* 2>/dev/null)"` → exit 0 · (no output) [ran] [tree aa2faea47d3b] (2026-10-03T19:12:19Z)
- (audit intent) `self: every idea checked against the code and this session (grounding notes in research/brainstorm-20261003-round4)` → the user's 'keep super improving foreman, make it smarter, better' gets a grounded slate past the 152 earlier ideas, the top two as briefs [tree aa2faea47d3b] (2026-10-03T19:12:19Z)
- (audit edge) `self: every idea checked against the code and this session (grounding notes in research/brainstorm-20261003-round4)` → ideas already built this session (band duplicate, secrets audits, resume checks) dropped rather than rebuilt; costly wild ideas recorded but not started [tree aa2faea47d3b] (2026-10-03T19:12:19Z)
- (audit intent) `self: every idea checked against the code and this session (grounding notes in research/brainstorm-20261003-round4)` → the user's 'keep super improving foreman, make it smarter, better' gets a grounded slate past the 152 earlier ideas, the top two as briefs [tree aa2faea47d3b] (2026-10-03T19:12:24Z)
- (audit edge) `self: every idea checked against the code and this session (grounding notes in research/brainstorm-20261003-round4)` → ideas already built this session (band duplicate, secrets audits, resume checks) dropped rather than rebuilt; costly wild ideas recorded but not started [tree aa2faea47d3b] (2026-10-03T19:12:24Z)
## Log
- 2026-10-03T19:09:46Z created
- 2026-10-03T19:12:24Z done
## Follow-ups captured
## Lessons
- Count lenses per idea: the one four lenses reached independently (replay the real command corpus) was also the one the session's evidence most supported.
