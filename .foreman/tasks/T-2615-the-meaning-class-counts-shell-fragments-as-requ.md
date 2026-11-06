---
id: T-2615
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T14:16:47Z
updated: 2026-11-02T14:17:14Z
---
# The meaning class counts shell fragments as request clauses: fmrecall.clauses splits a…
## Raw request
> FIX: the meaning class counts shell fragments as request clauses: fmrecall.clauses splits a request on ';' inside quoted commands, so T-0859's 'mkdir -p $S/toy' reads as unproven intent; 50 of the 872 meaning clauses fm prove --rollup shows look like shell code. A clause that is a command fragment (a $ or backtick, or a leading shell command with flags) is dropped from bind(), so meaning counts only asks
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
- 2026-11-02T14:16:47Z created
- 2026-11-02T14:17:14Z dropped: measured: only 10 of 872 meaning clauses hold a shell expansion, and several are real asks (guard tasks quote shell syntax: 'resolve a bare $(mktemp -d) assignment to a scratch path'); a code filter would drop requirements to remove ~1% noise
## Follow-ups captured
