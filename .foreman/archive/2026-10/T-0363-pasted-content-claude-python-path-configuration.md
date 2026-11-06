---
id: T-0363
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-08T22:44:45Z
updated: 2026-10-08T23:50:48Z
explore: true
confirm: true
done_in: T-0361
---
# "<pasted_content> claude: Python path configuration: PYTHONHOME = '/tmp/.mount_ForemaJcPmd
## Raw request
> "<pasted_content> claude: Python path configuration: PYTHONHOME = '/tmp/.mount_ForemaJcPmdB/usr/' ..."
> (fm second session: "<pasted_content> claude: Python path configuration: PYTHONHOME = '/tmp/.mount_ForemaJcPmdB/usr/' ..." — the AppImage Python config dump was pasted without a clear question, and no open item covers fixing the bundled Python path issue (the one tracker item on Desktop concerns the tray icon only).)
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
- 2026-10-08T22:44:45Z created
- 2026-10-08T23:50:48Z done in T-0361: T-0361 strips the AppImage's PYTHONHOME/PYTHONPATH/LD_* entries from every program the app starts, which is what broke claude's Python here (verified by its host_env tests)
## Follow-ups captured
