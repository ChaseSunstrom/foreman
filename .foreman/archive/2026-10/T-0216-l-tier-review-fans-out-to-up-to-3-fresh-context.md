---
id: T-0216
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:21:10Z
updated: 2026-10-04T04:54:11Z
base: b80023e9b17f35050aa34f3f23835b118b0f94b2
base_tree: 8e86d961dc598b394155e5800bd978563bce69c1
verified: strong
---
# fm audit prep --split: up to three parallel fresh-context reviewer briefs by lens group; suggested for big L diffs
## Raw request
> FEATURE: L-tier review fans out to up to 3 fresh-context fm-reviewer passes chosen by the change's files (security, tests, performance, …), merged and verified by the main thread; S/M keep one pass (claudekit parallel code-review)
> CONTEXT: PostToolUse is already an async hook (plugin/hooks/hooks.json); fm check --affected and fm impact know a file's tests; pain point #1 in the landscape research is false completion
> CONTEXT: fm map output is ~1.3k chars (plugin/lib/fmmap.py); SessionStart/UserPromptSubmit hooks in fmhooks.py; usage-sensitive user: keep it ≤ ~250 tokens and once per session
> CONTEXT: fm audit prep prints one brief for one pass (plugin/lib/fmcli.py audit prep); token-economy memory says one reviewer pass, so only L
> DONE-WHEN: a test edits a file whose linked test then fails and the next hook output names that test; a passing run says nothing
> DONE-WHEN: a hook test shows the map once in the first prompt's context and not again in that session
> DONE-WHEN: fm audit prep on an L task touching tests and a security-sensitive file prints separate lens briefs for parallel reviewers
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm audit prep --split writes one brief per lens group (≤ 3) and says to run them in parallel; without --split one brief as before; an L task with a big diff gets the suggestion — verify with `python3 plugin/tests/run.py -k test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then lens groups in cmd_audit
## Resume here
## Docs impact
CHANGELOG.md, plugin/skills/intake/references/audit.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_cli` → exit 0 · Ran 70 tests in 12.9s (16 classes, 16 at a time; slowest: TaskLifecycle 13s, StateViews 4s, Checks 3s) / OK [ran] [tree 2f3d43629f3e] (2026-10-04T04:53:11Z)
- `python3 plugin/tests/run.py -k AuditPrep` → ✗ exit 1 · Ran 6 tests in 2.0s (1 classes, 16 at a time; slowest: AuditPrep 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2f3d43629f3e] (2026-10-04T04:53:15Z)
- `python3 plugin/tests/run.py -k AuditPrep` → exit 0 · Ran 6 tests in 1.9s (1 classes, 16 at a time; slowest: AuditPrep 2s) / OK [ran] [tree 2f3d43629f3e] (2026-10-04T04:53:15Z)
- (ac 1) `python3 plugin/tests/run.py -k test_cli` → exit 0 · Ran 70 tests in 13.0s (16 classes, 16 at a time; slowest: TaskLifecycle 13s, StateViews 4s, Checks 3s) / OK [ran] [tree 2f3d43629f3e] (2026-10-04T04:54:11Z)
- (audit self) `self checklist: default unchanged (one brief, existing tests pass), --split covers every lens exactly once with no empty group (tested), the self block rides along in each split brief, suggestion only for L diffs over 800 lines` → pass [tree 2f3d43629f3e] (2026-10-04T04:54:11Z)
## Log
- 2026-10-04T04:21:10Z created
- 2026-10-04T04:21:16Z set tier=M
- 2026-10-04T04:52:16Z planned from capture
- 2026-10-04T04:52:16Z focused
- 2026-10-04T04:54:11Z done
- 2026-10-04T04:54:11Z committed fefe3c7 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0215 [FEATURE S, done, 1 steps] Session codebase map — the first prompt of a session in a repo carries a compact fm map (g
- research harness-landscape-20261003: Read on 2026-10-03. Quotes are from the fetched summaries, so a few are paraphrases rather than exact page text. Treat them as mediu…
- research t0063-final-review: MEDIUM — `plugin/lib/fmcore.py:842-845` (FIX red→green requirement) and `plugin/lib/fmcli.py:71-73` (M/L lesson requirement) — the user expl…
- research brainstorm-20260926-r5-slate: Dropped (already true): reviewer diff packet (fm audit prep writes audits/ID.diff); atomic locked state writes; doctor repair (--r…
- the similar finished task took 1 steps
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- plugin/skills/intake/references/audit.md
