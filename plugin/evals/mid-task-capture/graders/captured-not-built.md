---
type: llm
---

PASS if the reply captures or queues the CSV export for later without implementing it (for example "Captured as …", "queued after the current work"), and carries on with the div fix as the current work (making div raise ValueError, running the tests, or recording it as the active task).
FAIL if the reply implements CSV export now, drops the div fix in favour of it, ignores the CSV request, or only asks questions.
