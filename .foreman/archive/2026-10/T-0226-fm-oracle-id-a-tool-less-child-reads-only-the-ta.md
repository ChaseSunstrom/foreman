---
id: T-0226
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T05:18:36Z
updated: 2026-10-04T05:20:28Z
base: d7566639cebd7b319da33772a519f18ebb2552ea
base_tree: 9e87fde42c816f2e93cb52f19803bc6de07aa3f3
verified: strong
---
# Fm oracle ID — a tool-less child reads only the task's request, interpretation and criteri
## Raw request
> FEATURE: fm oracle ID — a tool-less child reads only the task's request, interpretation and criteria (never the code) and returns behaviour examples (given/when/then, edge cases) and the ambiguities that would change them; saved in the brief's Oracle section so tests are written from an independent spec, not from the implementation
> CONTEXT: landscape pain point #1 is circular tests that mirror the code; tool-less children run like fm ideas (fmideas.child_cmd pattern); intake's execute reference says TDD
> DONE-WHEN: with a stub, fm oracle writes the examples and ambiguities into the brief, and the child's prompt holds the request but no file contents
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with a stubbed child, fm oracle writes behaviour examples and ambiguities into the brief's Oracle section; the child gets the request and criteria but no repo file contents and no tools — verify with `python3 plugin/tests/run.py -k test_oracle`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then fm oracle (fmideas-style child) + intake execute reference
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/intake/references/execute.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_oracle` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Oracle 1s) / OK [ran] [tree 2d021157cd55] (2026-10-04T05:19:35Z)
- `python3 plugin/tests/run.py -k test_oracle` → ✗ exit 1 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Oracle 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2d021157cd55] (2026-10-04T05:19:37Z)
- `python3 plugin/tests/run.py -k test_oracle` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Oracle 1s) / OK [ran] [tree 2d021157cd55] (2026-10-04T05:19:37Z)
- (ac 1) `python3 plugin/tests/run.py -k test_oracle` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Oracle 1s) / OK [ran] [tree 2d021157cd55] (2026-10-04T05:20:23Z)
- (audit self) `self checklist: the child has no tools, no MCP, no user settings and runs in a scratch folder (tested: no repo text reaches it); output lines redacted, defanged, one line each; no examples is an error, not an empty section` → pass [tree 2d021157cd55] (2026-10-04T05:20:23Z)
- (audit adversary) `self checklist` → the child runs claude -p with --tools '' , no MCP, no user settings, in a scratch folder, fed only the brief's own sections (no file contents: tested); its output is data — kept only as '- ' lines under two headings, each redacted, defanged and cut to 300 chars, written through mutate under the lock; argv is fixed (spec goes on stdin), so no injection into the command [tree 2d021157cd55] (2026-10-04T05:20:28Z)
- (audit self) `self checklist` → pass [tree 2d021157cd55] (2026-10-04T05:20:28Z)
## Log
- 2026-10-04T05:18:36Z created
- 2026-10-04T05:18:43Z set tier=S
- 2026-10-04T05:18:43Z focused
- 2026-10-04T05:20:28Z done
- 2026-10-04T05:20:28Z committed 53a33c1 (6 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261004-round8: Test oracle (merges "pre-edit test oracle child", "request-to-oracle child", "compile examples in a request into the test", "fork in…
- research T-0207-review: Verdict: changes needed.** Nothing is critical. The guard handling is sound. The brief writes are sanitized much less than `fm task evidence` wri…
- T-0208 [FEATURE S, done, 1 steps] fm ideas marks each new idea with the finished task it most resembles
- T-0207 [FEATURE M, done, 3 steps] Debugging ledger: hypotheses in the brief that fm next drives, and a fresh-eyes fm-debugger agent — lesson: Any new free-text field wri…
- similar finished tasks took 1–3 steps
## Files touched
- plugin/tests/test_oracle.py
- plugin/lib/fmcli.py
- plugin/lib/fmideas.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/intake/references/execute.md
