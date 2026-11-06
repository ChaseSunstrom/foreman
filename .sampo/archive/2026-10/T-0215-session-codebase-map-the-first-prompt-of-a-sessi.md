---
id: T-0215
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:21:10Z
updated: 2026-10-04T04:47:11Z
base: ca06b0cd7e1434a21c8ef5cd1c1f02d53a6a7eb2
base_tree: 2fee7db179bbf634f848779667c656accbd9b201
verified: strong
---
# Session codebase map — the first prompt of a session in a repo carries a compact fm map (g
## Raw request
> FEATURE: session codebase map — the first prompt of a session in a repo carries a compact fm map (gates, entry points, hot files, test links) so Claude skips discovery searches (Aider repo map, claudekit codebase-map)
> CONTEXT: PostToolUse is already an async hook (plugin/hooks/hooks.json); fm check --affected and fm impact know a file's tests; pain point #1 in the landscape research is false completion
> CONTEXT: fm map output is ~1.3k chars (plugin/lib/fmmap.py); SessionStart/UserPromptSubmit hooks in fmhooks.py; usage-sensitive user: keep it ≤ ~250 tokens and once per session
> CONTEXT: fm audit prep prints one brief for one pass (plugin/lib/fmcli.py audit prep); token-economy memory says one reviewer pass, so only L
> DONE-WHEN: a test edits a file whose linked test then fails and the next hook output names that test; a passing run says nothing
> DONE-WHEN: a hook test shows the map once in the first prompt's context and not again in that session
> DONE-WHEN: fm audit prep on an L task touching tests and a security-sensitive file prints separate lens briefs for parallel reviewers
## Interpretation
Each new or compacted session rediscovers the repo with greps and reads. Give it the project map up front, compact (gates, entry points, layout, test links; ≤ ~600 chars), once per session start, without slowing the hook.
## Assumptions (confidence)
## Acceptance criteria
- [x] session start context carries a compact map from the cache, at most ~600 chars, and a missing map starts a background build instead of blocking — verify with `python3 plugin/tests/run.py -k test_hooks`
## Non-goals
## Approach (options → choice → why)
A) build the map in SessionStart: 0.02 s here but 1.5 s on a 6.7k-file repo — too slow for a hook. B) use the cached map.json (marked with its HEAD when stale) and refresh it in a detached background fm map when stale or missing. Choice: B.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then compact render + cached read + background refresh in session_context
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_hooks` → exit 0 · Ran 122 tests in 13.7s (20 classes, 16 at a time; slowest: Stop 14s, Approvals 9s, PromptApprovals 7s) / OK [ran] [tree 6f7d9fb88f0c] (2026-10-04T04:45:43Z)
- `python3 plugin/tests/run.py -k test_hooks` → ✗ exit 1 · Ran 122 tests in 17.0s (20 classes, 16 at a time; slowest: SessionStart 17s, Stop 14s, Approvals 9s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6f7d9fb88f0c] (2026-10-04T04:46:14Z)
- `python3 plugin/tests/run.py -k test_hooks` → exit 0 · Ran 122 tests in 13.7s (20 classes, 16 at a time; slowest: Stop 14s, Approvals 9s, PromptApprovals 7s) / OK [ran] [tree 6f7d9fb88f0c] (2026-10-04T04:46:14Z)
- (ac 1) `python3 plugin/tests/run.py -k test_hooks` → exit 0 · Ran 122 tests in 13.7s (20 classes, 16 at a time; slowest: Stop 14s, Approvals 9s, PromptApprovals 7s) / OK [ran] [tree 6f7d9fb88f0c] (2026-10-04T04:47:11Z)
- (audit self) `self checklist: never builds in the hook (cache only, detached refresh), first part dropped over the 2,000-char budget (budget test still passes), failures logged not raised; hook latency gate (bench_hooks) passes` → pass [tree 6f7d9fb88f0c] (2026-10-04T04:47:11Z)
## Log
- 2026-10-04T04:21:10Z created
- 2026-10-04T04:21:16Z set tier=S
- 2026-10-04T04:44:26Z focused
- 2026-10-04T04:47:11Z done
- 2026-10-04T04:47:11Z committed 87da4b6 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research harness-landscape-20261003: Read on 2026-10-03. Quotes are from the fetched summaries, so a few are paraphrases rather than exact page text. Treat them as mediu…
- research brainstorm-20260926-smarter-slate: Secret redaction before evidence/ledger/sync (security): premise false: fmcore.redact runs on typed and --run evidence (add_e…
- research t0063-final-review: MEDIUM — `plugin/lib/fmcore.py:842-845` (FIX red→green requirement) and `plugin/lib/fmcli.py:71-73` (M/L lesson requirement) — the user expl…
- T-0044 [FEATURE M, done, 0 steps] Fm map and fm impact — a per-project map (gates, layout, entry points, hot files, test↔sou
- similar past tasks were M: consider --tier M
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- plugin/lib/fmmap.py
- CHANGELOG.md
- MASTER.md
