---
id: T-0728
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T17:24:07Z
updated: 2026-10-09T17:25:43Z
base: 056b373937dd1a38101c867e4a90771428b1f8a0
base_tree: 6df5259f73c308383fddb9ad88f378c16c74cf8a
verified: strong
---
# recall --ask: redact before indexing (snippet markers can split a secret past the redactor) and cap the bytes indexed
## Raw request
> recall --ask: redact before indexing (snippet markers can split a secret past the redactor) and cap the bytes indexed
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a secret whose middle matches the question never prints, and indexing stops at a total byte cap — verify with `python3 plugin/tests/run.py -p test_trust.py -k AskMemory`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then redact on insert and a total cap
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_trust.py -k AskMemory` → ✗ exit 1 · Ran 6 tests in 9.2s (1 classes, 16 at a time; slowest: AskMemory 9s) / FAILED (1 classes) [ran] [tree fb67bc4576c9] (2026-10-09T17:24:33Z)
- (ac 1) `python3 plugin/tests/run.py -p test_trust.py -k AskMemory` → exit 0 · Ran 6 tests in 11.8s (1 classes, 16 at a time; slowest: AskMemory 12s) / OK [ran] [tree 303c3f375c6c] (2026-10-09T17:25:42Z)
- (step 1) `python3 plugin/tests/run.py -p test_trust.py` → exit 0 · Ran 13 tests in 11.7s (3 classes, 16 at a time; slowest: AskMemory 12s, StoryView 3s, ExplainBlock 3s) / OK [ran] [tree 303c3f375c6c] (2026-10-09T17:25:42Z)
- (audit adversary) `self: the bypass reproduced (a hand-written research note's key printed with [api03] highlighted); redaction now runs on insert so snippets come from redacted text; total index cap and -n clamp` → highlight markers can no longer split an unredacted secret (nothing unredacted is indexed); labels come from fixed strings and file names, already plain()ed; the cap stops a huge research folder or ledger from exhausting memory [tree 303c3f375c6c] (2026-10-09T17:25:42Z)
- (audit self) `self: the bypass reproduced (a hand-written research note's key printed with [api03] highlighted); redaction now runs on insert so snippets come from redacted text; total index cap and -n clamp` → no findings [tree 303c3f375c6c] (2026-10-09T17:25:42Z)
## Log
- 2026-10-09T17:24:07Z created
- 2026-10-09T17:24:07Z focused
- 2026-10-09T17:25:14Z paused: focus moved to T-0727
- 2026-10-09T17:25:18Z focused
- 2026-10-09T17:25:43Z done
- 2026-10-09T17:25:43Z committed 6fe4a37 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20260926-smarter-slate: Secret redaction before evidence/ledger/sync (security): premise false: fmcore.redact runs on typed and --run evidence (add_e…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- research T-0245-review-1: Verdict: approve with nits.** I found no shell, write or path-escape route from `tools/call`. The one real hole is option injection through rec…
- T-0263 [FEATURE M, done, 4 steps] Handoff: diff tour, proof sections in fm pr, AGENTS.md export — lesson: Anything written for other people or tools (AGENTS.md, PR bodie…
## Files touched
- plugin/tests/test_trust.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
