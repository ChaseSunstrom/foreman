---
id: T-1575
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T18:12:02Z
updated: 2026-10-22T19:35:21Z
done_in: T-1585
---
# Guard gaps (noticed in T-1561): awk '{print | "sh"}' FILE (awk running a shell from its pr
## Raw request
> Guard gaps (noticed in T-1561): awk '{print | "sh"}' FILE (awk running a shell from its program) and a redirect write to a system file (echo hi > /etc/passwd, > /etc/hosts) are allowed; classify awk's print-to-command and system() like a shell, and system-path writes like other system writes
## Interpretation
Found in T-1561: awk running a shell from its program (print | "sh", system("…")) and a redirect into a system file (echo x > /etc/hosts) are allowed. Classify the awk forms by the command they run, and system-path redirect targets as system writes.
## Assumptions (confidence)
## Acceptance criteria
- [ ] awk with print-to-command (print | "sh") or system() is classified like a shell; a redirect write to /etc/* is refused like other system writes; awk '{print $1}' f and > ./out still pass — verify with `cd plugin/tests && python3 -m unittest test_guard.AwkAndSystemWrites`
## Non-goals
## Approach (options → choice → why)
Options: block awk entirely (over-broad); chosen: read awk's program text for print/printf to a pipe, system() and getline from a command, and judge the string as a command when literal (refuse when computed); add /etc, /usr, /boot, /sys and the like to redirect-target classification.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] awk program classification
3. [ ] system-path redirect writes
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T18:12:02Z created
- 2026-10-22T18:13:48Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-10-22T18:46:54Z batched into T-1585
- 2026-10-22T19:35:21Z done in T-1585 (batch)
## Follow-ups captured
