---
id: T-3546
type: SECURITY
tier: S
status: done
priority: normal
scope: [.sampo/**, .foreman/**, CHANGELOG.md, scripts/probe-plugin-rename.sh]
depends_on: []
source: user
created: 2026-11-07T00:10:24Z
updated: 2026-11-07T02:17:55Z
base: 781b3e69f72829215b52f1dd37209ffddb2dd840
base_tree: 6f488664b88c42fbb0e67f702e63f5da60e91ec4
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T00:10:25Z
plan0_scope: []
verified: strong
---
# Re-export the public .sampo mirror with the private terms, home paths and private hosts redacted, and commit it
## Raw request
> Re-export the public .sampo mirror with the private terms, home paths and private hosts redacted, and commit it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] no tracked file holds a private term, a home path or the JARVIS address — verify with `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/privcheck.sh`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] export the mirror redacted, check it, commit it
## Resume here
## Docs impact
none: the state mirror only
## Verification evidence
- (step 1) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/privcheck.sh` → ✗ exit 1 · private lines: 13 [ran] [tree 6f488664b88c] [world 2f1906870a] (2026-11-07T00:10:46Z)
- (ac 1) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/privcheck.sh` → ✗ exit 1 · private lines: 13 [ran] [tree 6f488664b88c] [world 2f1906870a] (2026-11-07T00:10:51Z)
- (step 1) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/privcheck.sh` → ✗ exit 1 · private lines: 13 [ran] [tree 6f488664b88c] [world 2f1906870a] (2026-11-07T00:10:51Z)
- (step 1) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/privcheck.sh` → exit 0 · private lines: 0 [ran] [tree 7e5746807b35] [world 2f1906870a] (2026-11-07T02:10:44Z)
- (ac 1) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/privcheck.sh` → exit 0 · reused: the same command passed on this tree and world at 2026-11-07T02:10:44Z [ran] [tree 7e5746807b35] [world 2f1906870a] (2026-11-07T02:10:46Z)
- (audit adversary) `privcheck over every tracked file after the redacted export: 0 lines hold a private term, a home path or the JARVIS address` → the check reads the configured private terms plus the home path and address from state, never from argv; it counts lines, never prints them [tree 7e5746807b35] (2026-11-07T02:10:46Z)
- (audit edge) `privcheck over every tracked file after the redacted export: 0 lines hold a private term, a home path or the JARVIS address` → archived briefs and mirror files the export skips were rescrubbed by T-3547's skip-path scrub [tree 7e5746807b35] (2026-11-07T02:10:46Z)
- (audit self) `privcheck over every tracked file after the redacted export: 0 lines hold a private term, a home path or the JARVIS address` → no findings [tree 7e5746807b35] (2026-11-07T02:10:46Z)
- (step 1) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/privcheck.sh` → exit 0 · private lines: 0 [ran] [tree ed5fbe553395] [world 2f1906870a] (2026-11-07T02:17:11Z)
- (audit adversary) `privcheck over every tracked file after the redacted export: 0 lines hold a private term, a home path or the JARVIS address` → the check reads the configured private terms plus the home path and address from state, never from argv; it counts lines, never prints them [tree ed5fbe553395] (2026-11-07T02:17:15Z)
- (audit edge) `privcheck over every tracked file after the redacted export: 0 lines hold a private term, a home path or the JARVIS address` → archived briefs and mirror files the export skips were rescrubbed by T-3547's skip-path scrub [tree ed5fbe553395] (2026-11-07T02:17:15Z)
- (audit self) `privcheck over every tracked file after the redacted export: 0 lines hold a private term, a home path or the JARVIS address` → no findings [tree ed5fbe553395] (2026-11-07T02:17:15Z)
## Log
- 2026-11-07T00:10:24Z created
- 2026-11-07T00:10:25Z focused
- 2026-11-07T00:10:25Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T00:22:42Z paused: focus moved to T-3549
- 2026-11-07T02:10:21Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-07T02:10:21Z focused
- 2026-11-07T02:10:23Z set scope=['.sampo/**', '.foreman/**']
- 2026-11-07T02:17:03Z focused
- 2026-11-07T02:17:09Z set scope=['.sampo/**', '.foreman/**', 'CHANGELOG.md', 'scripts/probe-plugin-rename.sh']
- 2026-11-07T02:17:52Z done
- 2026-11-07T02:17:55Z committed 72a9138b7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3508 [SECURITY M, done, 2 steps] The public .sampo mirror redacts home paths and private hosts (user@host, 100.x addresses) and its README says sampo sync — lesson: Wh…
- T-3529 [SECURITY M, done, 3 steps] Private terms: the user's private domain names never reach the repo: sampo private add TERM (kept in state, outside git), the mirror e…
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- decision 2026-11-06: Sync is off until its export is cheap: every state write re-exported all ~3,300 briefs under the project lock (sync.export inside regen_views), so c…
## Preflight
Changed in scope since this was planned (2026-11-07): .sampo/README.md, .sampo/archive/2026-09/T-0018-recursive-foreman-self-improvement-after-t-0009.md, .sampo/archive/2026-09/T-0036-plugin-approvals-pinned-to-source-and-content-ha.md, .sampo/archive/2…; re-ground the plan against them before editing
## Lessons
- A redaction is done when a count over everything tracked says 0, not when the writer says it ran.
## Plan gaps
- failed first: step 1 export the mirror redacted, check it, commit it
## Files touched
- CHANGELOG.md
- scripts/probe-plugin-rename.sh
