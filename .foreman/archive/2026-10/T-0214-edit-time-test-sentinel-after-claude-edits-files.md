---
id: T-0214
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:21:10Z
updated: 2026-10-16T11:47:16Z
---
# Edit-time test sentinel — after Claude edits files, the tests linked to them (fm map test
## Raw request
> FEATURE: edit-time test sentinel — after Claude edits files, the tests linked to them (fm map test links / fm impact) run in the background and a newly failing test is reported to Claude right away, not at fm check (claudekit test-changed, research/harness-landscape-20261003)
> CONTEXT: PostToolUse is already an async hook (plugin/hooks/hooks.json); fm check --affected and fm impact know a file's tests; pain point #1 in the landscape research is false completion
> CONTEXT: fm map output is ~1.3k chars (plugin/lib/fmmap.py); SessionStart/UserPromptSubmit hooks in fmhooks.py; usage-sensitive user: keep it ≤ ~250 tokens and once per session
> CONTEXT: fm audit prep prints one brief for one pass (plugin/lib/fmcli.py audit prep); token-economy memory says one reviewer pass, so only L
> DONE-WHEN: a test edits a file whose linked test then fails and the next hook output names that test; a passing run says nothing
> DONE-WHEN: a hook test shows the map once in the first prompt's context and not again in that session
> DONE-WHEN: fm audit prep on an L task touching tests and a security-sensitive file prints separate lens briefs for parallel reviewers
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
- 2026-10-04T04:21:10Z created
- 2026-10-04T05:18:43Z deferred: low grounded value now: needs a per-project affected-tests template (unset here), fm check --affected and the done gate already catch regressions; revisit if friction shows late-caught test breaks
- 2026-10-16T11:47:16Z dropped: built: ambient affected tests after edits (T-0705) and onwrite validators (T-0947)
## Follow-ups captured
