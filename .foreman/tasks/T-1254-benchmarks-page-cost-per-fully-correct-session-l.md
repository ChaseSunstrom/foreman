---
id: T-1254
type: FEATURE
tier: M
status: done
priority: normal
scope: [site/pages.py, plugin/tests/test_docs.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-20T14:01:16Z
updated: 2026-10-20T14:30:49Z
base: 5a3aba4765746558fa358d74cb6941723c7c20f1
base_tree: 1e875571dc47db9028722ee71ef4bbf99c852db2
plan0_at: 2026-10-20T14:28:37Z
plan0_scope: [site/pages.py, plugin/tests/test_docs.py, CHANGELOG.md]
verified: strong
---
# Benchmarks page: cost per fully-correct session (long sessions: Foreman's mean cost over i
## Raw request
> FEATURE: Benchmarks page: cost per fully-correct session (long sessions: Foreman's mean cost over its runs that passed every hidden test, against Claude Code's), so the cost story counts what was delivered
> CONTEXT: brainstorm 2026-10-20 (research brainstorm-20261020), T-1252; Claude Code 2.1.304 re-sends the skill list after each compaction
## Interpretation
Put on the Benchmarks page what one long session that passed every hidden test cost on each side: total cost over the runs divided by the runs that passed, over the long-duel history. Today: Foreman about $0.095, Claude Code about $0.119, so Foreman is cheaper per correct result even though each session costs more.
## Assumptions (confidence)
## Acceptance criteria
- [x] the Benchmarks page says what one fully-correct long session cost on each side (total cost over the runs that passed every hidden test), computed from the duel history, and says so when a side never passed — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
Options: (a) a sentence in _why's long-work paragraph, from the same history; (b) a tile in _long, from the latest duel only; (c) a new chart. Choice: (a), because the history covers all six runs and the sentence sits next to the per-session cost it reframes; a side that never passed says so instead of dividing by zero.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: _why gives the cost per fully-correct session from a history, and handles a side with no full pass
2. [x] Compute it in site/pages.py _why, rebuild the site, update the changelog
## Resume here
## Docs impact
CHANGELOG entry; the page itself is the doc
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs` → ✗ exit 1 · Ran 44 tests in 1.4s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, TaskDocsDrift 0s, DocsDrift 0s) / FAILED (1 classes) [ran] [tree 36c56038bda5] (2026-10-20T14:28:46Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 44 tests in 1.4s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, TaskDocsDrift 0s, DocsDrift 0s) / OK [ran] [tree eb5803f9106d] (2026-10-20T14:28:56Z)
- (step 2) `python3 plugin/tests/run.py test_docs && python3 site/build.py >/dev/null && grep -q 'per fully correct session' _site/benchmarks/index.html` → ✗ exit 2 (never ran: no _site/benchmarks/index.html) · OK / grep: _site/benchmarks/index.html: No such file or directory [ran] [tree 6cf520d187aa] (2026-10-20T14:29:19Z)
- (step 2) `python3 plugin/tests/run.py test_docs && python3 site/build.py >/dev/null && grep -q 'per fully correct session' _site/features/benchmarks.html` → exit 0 · Ran 44 tests in 3.5s (12 classes, 16 at a time; slowest: TaskLifecycle 3s, TaskDocsDrift 1s, DocsDrift 1s) / OK [ran] [tree 6cf520d187aa] (2026-10-20T14:29:32Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 44 tests in 3.4s (12 classes, 16 at a time; slowest: TaskLifecycle 3s, TaskDocsDrift 1s, DocsDrift 1s) / OK [ran] [tree 6cf520d187aa] (2026-10-20T14:29:37Z)
- (audit intent) `self review of the sentence against the six-run history and the zero-pass branches` → the user asked why anyone would use Foreman at equal pass rates and wanted it cheaper; per fully correct long session it is 20% cheaper, now said from the data [tree 6cf520d187aa] (2026-10-20T14:29:37Z)
- (audit edge) `self review of the sentence against the six-run history and the zero-pass branches` → a side with no full pass gets its own sentence instead of a division by zero; Foreman with none says so too; both are tested [tree 6cf520d187aa] (2026-10-20T14:29:37Z)
## Log
- 2026-10-20T14:01:16Z created
- 2026-10-20T14:16:27Z set scope=['site/pages.py', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-20T14:28:36Z focused
- 2026-10-20T14:30:48Z done
- 2026-10-20T14:30:49Z committed a61bcfc3 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1231 [PERFORMANCE L, deferred, 5 steps] Foreman beats Claude Code on the duel: more tasks passed, lower cost, less time
- research T-1242-review: Verdict: changes needed.** The acceptance criterion's published result is missing, and per-request passes aren't reported. [stale: plugin/lib/fmc…
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
## Lessons
- Compare cost per correct result, not per run, wherever pass rates differ: the per-run premium hid that Foreman was the cheaper way to a passing session
## Plan gaps
- failed first: step 1 Failing test: _why gives the cost per fully-correct session from a history, and handles a side with…
- failed first: step 2 Compute it in site/pages.py _why, rebuild the site, update the changelog
## Files touched
- plugin/tests/test_docs.py
- site/pages.py
- CHANGELOG.md
