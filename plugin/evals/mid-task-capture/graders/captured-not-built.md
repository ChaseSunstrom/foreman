---
type: llm
---

PASS if the reply treats the CSV export as a new item to capture or queue for later (for example "Captured as …", "queued after the current task") and indicates work on T-0001 continues or will continue; it must not implement CSV export now.
FAIL if the reply starts implementing CSV export, abandons T-0001 for it, or ignores the request entirely.
