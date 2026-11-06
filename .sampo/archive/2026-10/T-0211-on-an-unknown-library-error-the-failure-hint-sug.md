---
id: T-0211
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-04T04:10:53Z
updated: 2026-10-04T04:49:26Z
base: 87da4b6240cc8e0a061f1a3a921384768edb241d
base_tree: 6f7d9fb88f0c3262dc1b04f135c1a2936b889ffd
verified: strong
---
# A failure that names a library API that doesn't exist points to its real docs before another guess
## Raw request
> On an unknown-library error, the failure hint suggests context7/recon before guessing
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an unknown-module / no-such-attribute / unexpected-keyword error gets a one-time hint naming context7 and fm research ask; an ordinary assertion failure doesn't — verify with `python3 plugin/tests/run.py -k test_debug`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then an API-misuse pattern in fmrecall.note_failure
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 6 tests in 1.7s (3 classes, 16 at a time; slowest: Hypotheses 2s, ApiMisuse 0s, Debugger 0s) / OK [ran] [tree 85768eb1aaed] (2026-10-04T04:48:36Z)
- `python3 plugin/tests/run.py -k test_debug` → ✗ exit 1 · Ran 6 tests in 1.8s (3 classes, 16 at a time; slowest: Hypotheses 2s, ApiMisuse 0s, Debugger 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 85768eb1aaed] (2026-10-04T04:48:40Z)
- `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 6 tests in 1.7s (3 classes, 16 at a time; slowest: Hypotheses 2s, ApiMisuse 0s, Debugger 0s) / OK [ran] [tree 85768eb1aaed] (2026-10-04T04:48:40Z)
- (ac 1) `python3 plugin/tests/run.py -k test_debug` → exit 0 · Ran 6 tests in 1.7s (3 classes, 16 at a time; slowest: Hypotheses 2s, ApiMisuse 0s, Debugger 0s) / OK [ran] [tree 85768eb1aaed] (2026-10-04T04:49:26Z)
- (audit self) `self checklist: patterns are library-shaped (module attribute, keyword, export, import, method), a None attribute in our own code doesn't match (tested); once per failure signature with or without an active task (tested); hint appended to any seen-before pointer` → pass [tree 85768eb1aaed] (2026-10-04T04:49:26Z)
## Log
- 2026-10-04T04:10:53Z created
- 2026-10-04T04:47:36Z planned from capture
- 2026-10-04T04:47:37Z focused
- 2026-10-04T04:49:26Z done
- 2026-10-04T04:49:26Z committed 8f06b7a (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0183 [FIX M, done, 3 steps] Guard: unknown-target guesses come from the command's own words, pair up across unknown parts, and know a literal set once before any branc…
- research brainstorm-20261003-round6: Runs: brainstorm-20261003-230652 (5 lenses + deepen 3: 78 new titles) and brainstorm-20261003-230844 (4 lenses + deepen 2: 61 new ti…
- research smoke-tomllib: Asked 2026-10-04 · 1 sub-question(s) · 8 claims: 7 quote found, 1 quote not found, 0 unchecked. ✓ means the quoted words are on the cited page, n…
- T-0190 [FIX M, done, 3 steps] Guard: guesses never use a variable's own name; rm targets use literals set once before a branch — lesson: A replay gate turns a guard chan…
## Files touched
- plugin/tests/test_debug.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
