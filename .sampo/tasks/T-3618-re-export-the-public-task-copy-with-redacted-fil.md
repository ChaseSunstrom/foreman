---
id: T-3618
type: SECURITY
tier: S
status: active
priority: normal
scope: [.sampo/**, .foreman/**, CHANGELOG.md, scripts/probe-plugin-rename.sh]
depends_on: []
source: user
created: 2026-11-07T04:55:10Z
updated: 2026-11-07T05:39:24Z
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T04:55:11Z
plan0_scope: []
---
# Re-export the public task copy with redacted file names and commit it
## Raw request
> Re-export the public task copy with redacted file names and commit it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] no tracked line or path holds a private term, a home path or the JARVIS address — verify with `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/privcheck.sh`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] export the mirror, check lines and paths, commit
## Resume here
<!-- auto -->
- 2026-11-07T04:55:14Z step 1/1: export the mirror, check lines and paths, commit
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/privcheck.sh` → exit 0 · private lines: 0 · private paths: 0 [ran] [tree 5540b1d068a0] [world 2f1906870a] (2026-11-07T04:58:57Z)
## Log
- 2026-11-07T04:55:10Z created
- 2026-11-07T04:55:11Z focused
- 2026-11-07T04:55:11Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T04:55:13Z set scope=['.sampo/**', '.foreman/**', 'CHANGELOG.md', 'scripts/probe-plugin-rename.sh']
- 2026-11-07T05:39:20Z focused
- 2026-11-07T05:39:24Z set scope=['.sampo/**', '.foreman/**', 'CHANGELOG.md', 'scripts/probe-plugin-rename.sh']
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3508 [SECURITY M, done, 2 steps] The public .sampo mirror redacts home paths and private hosts (user@host, 100.x addresses) and its README says sampo sync — lesson: Wh…
- T-3546 [SECURITY S, done, 1 steps] Re-export the public .sampo mirror with the private terms, home paths and private hosts redacted, and commit it — lesson: A redaction …
- T-3574 [SECURITY S, active, 3 steps] SECURITY (user's privacy request): the .sampo mirror keeps each brief's state file name,…
- decision 2026-11-06: Sync is off until its export is cheap: every state write re-exported all ~3,300 briefs under the project lock (sync.export inside regen_views), so c…
- similar finished tasks took 1–2 steps
