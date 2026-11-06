---
id: T-0810
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py]
depends_on: []
source: discovered
created: 2026-10-14T17:11:52Z
updated: 2026-10-14T17:24:15Z
base: 14c5cd872e4c8e013b2579eab775be4438e63b19
base_tree: 6e0aa6fd3f8cd0e17a683eb939d9caa132b21935
verified: strong
---
# fm task set ID scope=[a,b] stores the paths, not the brackets
## Raw request
> fm task set ID scope=[a,b] stores the brackets inside the paths (splits the JSON list on commas): accept a JSON list or repeated scope=
## Interpretation
fm task set splits list fields on commas (fmcli.py:1835), so scope=[a,b] or scope='["a", "b"]' (a builder wrote that) stored '[a' and 'b]' as globs. Strip one surrounding pair of brackets and quotes around each item.
## Assumptions (confidence)
## Acceptance criteria
- [x] scope=[a, b], scope='["a","b"]' and scope=a,b all store [a, b] — verify with `python3 plugin/tests/run.py -k test_list_fields_accept_brackets`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing CLI test
2. [x] Strip brackets and quotes
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_list_fields_accept_brackets` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: SetLists 0s) / FAILED (1 classes) [ran] [tree 5c38a1229af2] (2026-10-14T17:22:01Z)
- (step 2) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 87 tests in 17.9s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 6s, Checks 4s) / OK [ran] [tree b5218cc69e0e] (2026-10-14T17:22:24Z)
- (ac 1) `python3 plugin/tests/run.py -k test_list_fields_accept_brackets` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: SetLists 0s) / OK [ran] [tree b5218cc69e0e] (2026-10-14T17:22:25Z)
- `python3 plugin/tests/run.py -k test_list_fields_accept_brackets` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: SetLists 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b5218cc69e0e] (2026-10-14T17:22:27Z)
- `python3 plugin/tests/run.py -k test_list_fields_accept_brackets` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: SetLists 0s) / OK [ran] [tree b5218cc69e0e] (2026-10-14T17:22:27Z)
- (ac 1) `python3 plugin/tests/run.py -k test_list_fields_accept_brackets` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: SetLists 0s) / OK [ran] [tree b5218cc69e0e] (2026-10-14T17:24:14Z)
- (audit edge) `self: diff read; _list_value strips one pair of surrounding brackets and the quotes around each item before splitting on commas; plain a,b is unchanged` → a glob that really starts with [ (a character class like [ab]*.py alone) loses its bracket only when the whole value is wrapped; a single-item [x] list stores x [tree b5218cc69e0e] (2026-10-14T17:24:14Z)
- (audit self) `self: diff read; _list_value strips one pair of surrounding brackets and the quotes around each item before splitting on commas; plain a,b is unchanged` → no findings [tree b5218cc69e0e] (2026-10-14T17:24:14Z)
## Log
- 2026-10-14T17:11:52Z created
- 2026-10-14T17:21:58Z planned from capture
- 2026-10-14T17:21:58Z focused
- 2026-10-14T17:24:14Z done
- 2026-10-14T17:24:15Z committed 0e12022 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- research T-0212-review: Verdict: changes needed.** There are no CRITICAL or HIGH findings. Two MEDIUM issues are worth fixing before relying on `compare`. I read the cod…
- research T-0207-review: Verdict: changes needed.** Nothing is critical. The guard handling is sound. The brief writes are sanitized much less than `fm task evidence` wri…
- decision 2026-09-26: rounds 4-6 slate: 4 safety items, 4 workflow items, 2 measured perf items (research brainstorm-20260926-slate); run inside T-0018 so one core grant …
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- a CLI value people write as a list should accept the list syntax they reach for
## Plan gaps
- failed first: step 1 Failing CLI test
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
