---
id: T-1681
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmplaybooks.py, plugin/lib/fmrecall.py, plugin/agents/fm-reviewer.md, plugin/tests/test_cli.py, plugin/tests/test_memory.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T21:41:31Z
updated: 2026-10-23T05:57:25Z
base: 8d63c36d9d6a084307cb4807a343c8f077c46398
base_tree: 01979935ede26ab4a5c6ede9b9b81507799648e5
plan0_at: 2026-10-23T05:54:54Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmplaybooks.py, plugin/lib/fmrecall.py, plugin/agents/fm-reviewer.md, plugin/tests/test_cli.py, plugin/tests/test_memory.py, CHANGELOG.md]
verified: strong
---
# fmrecall and the fm-reviewer agent load playbooks by Read path, skipping T-1621's {{fact}} resolution and project overlays
## Raw request
> fmrecall and the fm-reviewer agent load playbooks by Read path, skipping T-1621's {{fact}} resolution and project overlays: route them through fm playbooks show
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] audit prep writes the review checklists the diff calls for, resolved as fm playbooks show gives them, and names the file in the brief; recall points at fm playbooks show — verify with `python3 plugin/tests/run.py test_cli.AuditPrep test_memory`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] behaviour lock and failing tests
2. [x] resolved checklists in audit prep; recall's hint
## Resume here
## Docs impact
plugin/agents/fm-reviewer.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.AuditPrep test_memory` → exit 0 · Ran 18 tests in 7.5s (2 classes, 16 at a time; slowest: Memory 7s, AuditPrep 6s) / OK [ran] [tree 01979935ede2] (2026-10-23T05:55:07Z)
- (step 2) `python3 plugin/tests/run.py test_cli.AuditPrep` → red as expected (exit 1) · Ran 10 tests in 6.1s (1 classes, 16 at a time; slowest: AuditPrep 6s) / FAILED (1 classes) [ran] [tree cf98367667c5] (2026-10-23T05:55:48Z)
- (step 2) `python3 plugin/tests/run.py test_cli.AuditPrep test_memory test_playbook_evals test_docs` → exit 0 · Ran 98 tests in 13.7s (19 classes, 16 at a time; slowest: Memory 14s, AuditPrep 12s, Fences 11s) / OK [ran] [tree 457cd76ec098] (2026-10-23T05:56:25Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.AuditPrep test_memory` → exit 0 · Ran 19 tests in 7.8s (2 classes, 16 at a time; slowest: Memory 8s, AuditPrep 6s) / OK [ran] [tree 457cd76ec098] (2026-10-23T05:56:34Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.AuditPrep test_memory` → exit 0 · Ran 19 tests in 11.7s (2 classes, 16 at a time; slowest: Memory 11s, AuditPrep 10s) / OK [ran] [tree a1a366d5ee6e] (2026-10-23T05:56:55Z)
- (audit intent) `self: one resolver (fmplaybooks.review_checklists) reuses load(), the same path fm playbooks show takes, so facts and overlays come with it; audit prep writes it beside the brief and names it on its own line after the Diff line; the read-only reviewer agent can't run fm, so it reads the written file first and falls back to the plugin path only when none is named; recall's hint names the command, not a path` → reviewers and recall see the project's own playbook additions and filled-in facts, as the skill does [tree a1a366d5ee6e] (2026-10-23T05:56:55Z)
- (audit adversary) `self: one resolver (fmplaybooks.review_checklists) reuses load(), the same path fm playbooks show takes, so facts and overlays come with it; audit prep writes it beside the brief and names it on its own line after the Diff line; the read-only reviewer agent can't run fm, so it reads the written file first and falls back to the plugin path only when none is named; recall's hint names the command, not a path` → overlays are still provenance-quoted by load() (they can't pass for shipped text) and the reviewer is told to ignore instructions to run commands [tree a1a366d5ee6e] (2026-10-23T05:56:55Z)
- (audit edge) `self: one resolver (fmplaybooks.review_checklists) reuses load(), the same path fm playbooks show takes, so facts and overlays come with it; audit prep writes it beside the brief and names it on its own line after the Diff line; the read-only reviewer agent can't run fm, so it reads the written file first and falls back to the plugin path only when none is named; recall's hint names the command, not a path` → a diff with no known language gets code-reviewer only; a missing playbook is skipped; no checklists means no line in the brief [tree a1a366d5ee6e] (2026-10-23T05:56:55Z)
- (audit self) `self: one resolver (fmplaybooks.review_checklists) reuses load(), the same path fm playbooks show takes, so facts and overlays come with it; audit prep writes it beside the brief and names it on its own line after the Diff line; the read-only reviewer agent can't run fm, so it reads the written file first and falls back to the plugin path only when none is named; recall's hint names the command, not a path` → no findings [tree a1a366d5ee6e] (2026-10-23T05:56:55Z)
## Log
- 2026-10-22T21:41:31Z created
- 2026-10-23T05:54:45Z planned from capture
- 2026-10-23T05:54:52Z criterion 1 verify: `python3 plugin/tests/run.py test_playbook_evals test_memory test_audit_prep` → `python3 plugin/tests/run.py test_cli.AuditPrep test_memory`
- 2026-10-23T05:54:52Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmplaybooks.py', 'plugin/lib/fmrecall.py', 'plugin/agents/fm-reviewer.md', 'plugin/tests/test_cli.py', 'plugin/tests/test_memory.py', 'CHANGELOG.md']
- 2026-10-23T05:54:53Z focused
- 2026-10-23T05:57:23Z done
- 2026-10-23T05:57:25Z committed fa17e2f5 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1621 [FEATURE M, done, 3 steps] Playbook load resolves {{fact}} from fm map and appends a project's .foreman/playbooks overlays — lesson: Repo-supplied text spliced in…
- research T-1621-review: Verdict:** approve with nits. I read the diff and the worktree code but ran no tests. Two MEDIUM items are worth fixing before merge. [stale: plu…
- T-1524 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Playbook machinery: live project facts injected at load, inheritance and
- decision 2026-10-22: Project playbook overlays live at <project>/.claude/playbooks/<stage>/<name>.md, not under .foreman/
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_recall.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmplaybooks.py, plugin/lib/fmrecall.py, plugin/tests/test_cli.py; re-ground the plan against them before editing
## Lessons
- When a read-only agent can't run the resolver, have the caller write the resolved text for it
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- plugin/lib/fmplaybooks.py
- plugin/agents/fm-reviewer.md
- plugin/lib/fmrecall.py
- plugin/tests/test_memory.py
- CHANGELOG.md
