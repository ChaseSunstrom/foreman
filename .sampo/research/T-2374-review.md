T-2374 review (coordinator, main thread: the pace gate held fm-reviewer subagents).
Security checked: a --later ask never creates a pending approval or a dialog, returns early in every grant path, and fmhooks._grant stays the only writer of approval_granted; forged or queued rows grant nothing (tests).
MEDIUM fixed: an unanswered dialog was recorded as a project-wide grant_refused with no undo verb, so one missed dialog suppressed the request for good: removed; only an explicit no is remembered (test flipped red first).
Open: a queued request on a task that closes stops being listed; the linked miss can be the wrong one when a task has several open misses.
