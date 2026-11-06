# Brainstorm — lens: user value

- **Offer a one-yes commit at task done** — FEATURE — value 4 — effort S — risk low
  Why: assumption: the user never runs commands, and nothing in the pack commits or packages finished work. Files touched, the outcome report and the grade already exist, so `fm task done` can stage exactly those files and draft the message from the brief. It sends one yes/no prompt, and `fm decide --kind outward` covers any push.
  Done when: after `done` and a yes, `git log -1` shows a commit containing exactly the Files-touched list, and a no leaves the tree untouched.

- **Ship a bounded "read pack" at focus** — PERFORMANCE — value 5 — effort M — risk med
  Why: start-here files, `fm outline` and the symbol index exist separately, and Claude still spends turns exploring. Focus can inject a ≤1,500-char pack of the symbol signatures and bodies the similar past task edited, skipping files it already read.
  Done when: on a replayed recorded task, exploratory Read/Grep calls before the first edit drop by at least 30%, with the pack within its cap.

- **Detect edits made outside Claude mid-task** — SECURITY — value 4 — effort M — risk low
  Why: assumption: the user edits files or switches branches while a task is active. Focus preflight only checks scope drift at focus time. PostToolUse would compare the tree hash against the last post-Claude hash and emit one note ("X changed outside this session; re-read before editing").
  Done when: a test that touches a scoped file between two tool calls yields exactly one note, and Claude's own edits yield none.

- **Cache code-question answers by file fingerprint** — PERFORMANCE — value 4 — effort M — risk med
  Why: recall covers past research, but nothing says whether a stored answer is still true. Store each RESEARCH answer with the hashes of the files it cited. A hit whose fingerprints still match is offered as "answered before, still valid". A mismatch demotes it to a hint.
  Done when: a repeated question with unchanged files is answered from the cache with zero file reads, and editing a cited file invalidates the entry.

- **Brief and cap read-only subagents** — PERFORMANCE — value 4 — effort M — risk med
  Why: assumption: subagent and reviewer passes burn tokens re-exploring, and `fm cost` shows token totals but nothing shapes them. A PreToolUse hook on the subagent tool would append the task's scope, start-here files and a "report ≤N words, cite file:line" contract.
  Done when: the median subagent transcript tokens per audit drop measurably in `fm cost`, with no failed audits attributable to the cap.

- **File audit findings as queued follow-ups automatically** — FEATURE — value 3 — effort S — risk low
  Why: assumption: "deferred" or "out of scope" review findings currently live only in the brief log and get lost. At `done`, tag those findings, dedupe them against the queue by BM25, and add them as unrefined items with a link to the source task.
  Done when: a finished task with two deferred findings adds two deduped queue entries, and running `done` again adds none.

- **Record a demo transcript of the new behaviour in the outcome report** — FEATURE — value 3 — effort S — risk low
  Why: the plain-language report says what changed but not what it looks like. Reuse the auto-captured evidence of the exact verify command, with exit status, and include the trimmed output for FEATURE and FIX.
  Done when: the report for a FEATURE task contains ≥1 real captured command output (≤600 chars), and a task without a demonstrable output omits the section.
