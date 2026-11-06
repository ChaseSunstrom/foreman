---
id: T-2008
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmaway.py]
depends_on: []
source: user
created: 2026-10-29T15:58:28Z
updated: 2026-10-29T16:36:52Z
done_in: T-2012
---
# A prompt that ends a silence of 2 h or more gets the away summary in its context, not…
## Raw request
> FEATURE: a prompt that ends a silence of 2 h or more gets the away summary in its context, not only a session start
> @plugin/lib/fmaway.py
> DONE-WHEN: the prompt hook adds "Away: N h since you last spoke" after a 2 h gap and nothing after a short one :: python3 plugin/tests/run.py test_away -k on_a_prompt
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-29T15:58:28Z created
- 2026-10-29T15:58:35Z set tier=S
- 2026-10-29T15:58:38Z batched into T-2012
- 2026-10-29T16:36:52Z done in T-2012 (batch)
## Follow-ups captured
