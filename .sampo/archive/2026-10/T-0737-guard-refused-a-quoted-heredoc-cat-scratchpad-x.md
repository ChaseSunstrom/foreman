---
id: T-0737
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T18:40:08Z
updated: 2026-10-09T18:44:40Z
---
# Guard refused a quoted heredoc (cat > scratchpad/x.py <<'EOF' … EOF) as a core tree write
## Raw request
> guard refused a quoted heredoc (cat > scratchpad/x.py <<'EOF' … EOF) as a core tree write './$_': a quoted heredoc body is data, not commands (T-0705 measurement script)
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
- 2026-10-09T18:40:08Z created
- 2026-10-09T18:44:40Z dropped: not a false positive: the heredoc's Python wrote to runtime-computed paths and the command cd'd into core, so the guard couldn't prove the target was outside; conservative by design (its message names the fix: literal paths or another cwd)
## Follow-ups captured
