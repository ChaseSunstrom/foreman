---
id: T-1603
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T20:30:59Z
updated: 2026-10-23T08:43:48Z
---
# Fm design lint` shares `_blank` and `Source`. A string containing `{` skews its block stac
## Raw request
> fm design lint` shares `_blank` and `Source`. A string containing `{` skews its block stack the same way as in `_props`. That is worth a hostile-input test
> (noticed by an agent; research T-1507-review)
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
- 2026-10-22T20:30:59Z created
- 2026-10-23T08:43:48Z dropped: covered since: test_design_lint's test_a_brace_inside_a_string_doesnt_end_the_block feeds content: "}" and content: '{' and checks the lint's findings; _props reads Source.braces, where strings' braces are blanked (T-1507)
## Follow-ups captured
