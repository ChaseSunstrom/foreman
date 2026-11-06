---
id: T-2313
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T10:45:48Z
updated: 2026-10-31T11:39:27Z
done_in: T-2316
---
# fmhooks._note_key (fmhooks.py:191-195) replaces an apostrophe with a space, so "T-0877's…
## Raw request
> fmhooks._note_key (fmhooks.py:191-195) replaces an apostrophe with a space, so "T-0877's lesson for this file" keys as "s lesson for this file" in the friction digest and can merge unrelated notes: strip 's before the punctuation pass; test _note_key on that note
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
- 2026-10-31T10:45:48Z created
- 2026-10-31T10:46:05Z batched into T-2316
- 2026-10-31T10:57:23Z blocked: member of batch T-2316 (in a builder lane); closes done with it
- 2026-10-31T11:39:27Z done in T-2316 (batch)
## Follow-ups captured
