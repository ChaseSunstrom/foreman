---
id: T-2133
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T10:15:51Z
updated: 2026-10-30T11:36:46Z
---
# fm find on Foreman flags fmgraph.py:135 (SQL from param where) and fmdeps.py:125…
## Raw request
> fm find on Foreman flags fmgraph.py:135 (SQL from param where) and fmdeps.py:125 (password in a URL): prove or refute each, file as dropped if false
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
- 2026-10-30T10:15:51Z created
- 2026-10-30T11:36:46Z refuted fmgraph.py:135: _edges' where is only ever ' AND dst/src IN (?,?,..)' built from len(paths) (callers :142, :143) or empty (:163); values go through ? args. Refuted fmdeps.py:125: the hit is the regex literal r'(git\+|https?://|file:[REDACTED]@|...)', where '://|file:[REDACTED]@' fits URL_CRED's '://user:[REDACTED]@' shape; no credential. Narrowing URL_CRED would weaken c.redact, so left as is.
- 2026-10-30T11:36:46Z dropped: both flags refuted: constant SQL fragments with ? args; a regex literal, not a credential
## Follow-ups captured
