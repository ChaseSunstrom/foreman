---
id: T-3608
type: SECURITY
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-07T04:28:03Z
updated: 2026-11-07T04:28:03Z
---
# SECURITY: sampo-fast installer for slice 2 of T-3571: scrubbed env (no…
## Raw request
> SECURITY: sampo-fast installer for slice 2 of T-3571: scrubbed env (no RUSTC_WRAPPER/RUSTFLAGS/CARGO_* overrides, no .cargo/config above the tree), cargo build --release --locked --offline from the committed plugin/native, verify the built file, install it 0755 owned by the user into plugin/native/sampo-fast and write sampo-fast.sha256 beside it (the sum hooks/fast checks); doctor --repair reruns it after a merge leaves the binary stale
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
- 2026-11-07T04:28:03Z created
## Follow-ups captured
