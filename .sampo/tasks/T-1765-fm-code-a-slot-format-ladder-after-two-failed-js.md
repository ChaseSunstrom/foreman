---
id: T-1765
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-23T08:27:33Z
updated: 2026-10-23T08:54:15Z
base: f880675496c73315f7759d93a6655aae71a999c4
base_tree: 2034543ce1c38e75419780d3945f69b064b6626d
plan0_at: 2026-10-23T08:49:39Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md]
verified: strong
---
# Fm code: a slot-format ladder — after two failed JSON repairs, ask one field per question
## Raw request
> fm code: a slot-format ladder — after two failed JSON repairs, ask one field per question before escalating (rest of T-1398)
## Interpretation
When a model's plan or close notes fail JSON repair twice, fm code stops asking for JSON and asks one plain-text question per field (type, tier, title, criteria as 'text :: command' lines, steps; each close note), builds the slot from the answers and checks it as before. Only after that fails does the run stop. Weak local models that can't hold a JSON shape still plan.
## Assumptions (confidence)
## Acceptance criteria
- [x] after two failed JSON repairs a plan or close notes slot asks one plain-text question a field and uses the assembled slot when it checks out; a run whose field answers still fail stops naming both — verify with `python3 plugin/tests/run.py test_code.Repairs`
## Non-goals
## Approach (options → choice → why)
Options: (a) a grammar or JSON-mode flag per server (not every server has one; Ollama/llama.cpp differ); (b) one field per question after the repairs, parsed from plain text; (c) escalate straight to a stronger model (needs one configured). Choice: (b) in slot(), with per-slot field tables (PLAN_FIELDS, CLOSE_FIELDS) and small text parsers; the model call is split out as _ask so both paths share the spend cap, the CLI tree check and the truncation check. Escalation stays as it is after the ladder.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: field-by-field plan, never-repaired message
2. [x] _ask split out; PLAN_FIELDS, CLOSE_FIELDS and parsers; slot ladder; callers pass fields
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.Repairs` → ✗ exit 1 · Ran 8 tests in 7.5s (1 classes, 16 at a time; slowest: Repairs 7s) / FAILED (1 classes) [ran] [tree 779ce12b5926] (2026-10-23T08:50:07Z)
- (step 2) `python3 plugin/tests/run.py test_code.Repairs` → exit 0 · Ran 8 tests in 7.1s (1 classes, 16 at a time; slowest: Repairs 7s) / OK [ran] [tree f19db8d6b125] (2026-10-23T08:52:33Z)
- (audit self) `read the diff; probed _word, _items, _criteria, _unlabel on empty, bold, bulleted, fenced, double '::' and None inputs; ran test_code, test_code_worker, test_code_bench` → ok: answers pass the same check_plan/check_close and _plan_problem as JSON; each field call goes through the spend cap, the CLI tree check and the truncation check; the repair ask is popped so turns alternate [tree f19db8d6b125] (2026-10-23T08:52:34Z)
- (ac 1) `python3 plugin/tests/run.py test_code.Repairs` → exit 0 · Ran 8 tests in 7.1s (1 classes, 16 at a time; slowest: Repairs 7s) / OK [ran] [tree f19db8d6b125] (2026-10-23T08:52:51Z)
- (audit intent) `self review of the diff, parser probes, test_code + test_code_worker + test_code_bench green` → plan and close slots fall back to one plain-text question a field after two failed JSON repairs; the assembled slot passes the same checks (Repairs tests) [tree f19db8d6b125] (2026-10-23T08:52:51Z)
- (audit edge) `self review of the diff, parser probes, test_code + test_code_worker + test_code_bench green` → empty, bulleted, fenced, labelled and double-'::' answers parse or fail the check; a field ladder that fails names both errors and Next: fm code models [tree f19db8d6b125] (2026-10-23T08:52:51Z)
## Log
- 2026-10-23T08:27:33Z created
- 2026-10-23T08:49:18Z set tier=M
- 2026-10-23T08:49:19Z set scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code.py', 'CHANGELOG.md']
- 2026-10-23T08:49:38Z focused
- 2026-10-23T08:52:26Z set scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T08:52:44Z scope: MASTER.md documents fm code's slot path; added to scope
- 2026-10-23T08:54:14Z done
- 2026-10-23T08:54:15Z committed b9c60a4c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1398 [FEATURE M, done, 3 steps] fm code slot integrity: elided code in an edit or write is refused and re-asked, a unique near-miss edit anchor (whitespace only) is ap…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- research brainstorm-fm-anthropic-half-b: Reading used.** I took all 250 bullets of rounds 1 to 4 in lenses 01, 02, 03, 08 and 09. Four titles occur twice (themes, ETA, g…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- likely tests for the scope: plugin/tests/test_code.py
## Lessons
- A weak model that can't hold a JSON shape often answers one plain question well: degrade the format before escalating the model
## Plan gaps
- failed first: step 1 failing tests: field-by-field plan, never-repaired message
## Files touched
- plugin/lib/fmcode.py
- plugin/tests/test_code.py
- MASTER.md
