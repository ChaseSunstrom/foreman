---
id: T-0085
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/rules/foreman.md, plugin/lib/fmcore.py, plugin/tests/test_recall.py, plugin/tests/e2e/**, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-02T18:35:16Z
updated: 2026-10-03T08:03:06Z
base: b4f4bcca7daf08a590f150b2a469fc0854f19187
base_tree: a387e849175af7b6190c1c719af35079e9f1feb0
verified: strong
---
# Rules diet: drop always-on lines a gate already enforces with the fix in its message
## Raw request
> Rules diet: drop always-on rule lines a gate already enforces
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] The rules lose the lines whose gate already says the fix (focus planning, fm gates/prove, per-tier audits, grant categories repeated), the red→green refusal names fm task prove, and the rules budget check passes — verify with `python3 plugin/tests/run.py -k test_recall -k test_doctor`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red: the refusal names fm task prove
2. [x] Message, rules edit, eval sync
3. [x] CHANGELOG with the before/after size
## Resume here
## Docs impact
CHANGELOG; the rules themselves; evals re-synced.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_recall -k test_doctor` → exit 0 · Ran 31 tests in 6.2s (10 classes, 16 at a time; slowest: Recall 6s, Command 5s, RedGreen 1s) / OK [ran] [tree 662c6e47003e] (2026-10-03T08:02:42Z)
- (step 2) `python3 plugin/tests/run.py -k test_recall -k test_doctor` → exit 0 · Ran 31 tests in 6.3s (10 classes, 16 at a time; slowest: Recall 6s, Command 5s, RedGreen 1s) / OK [ran] [tree 662c6e47003e] (2026-10-03T08:02:48Z)
- (step 3) `grep -q T-0085 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 662c6e47003e] (2026-10-03T08:02:48Z)
- (ac 1) `python3 plugin/tests/run.py -k test_recall -k test_doctor` → exit 0 · Ran 31 tests in 6.3s (10 classes, 16 at a time; slowest: Recall 6s, Command 5s, RedGreen 1s) / OK [ran] [tree 662c6e47003e] (2026-10-03T08:03:00Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:02 UTC); cached (fm check --fresh reruns) [ran] [tree 662c6e47003e] (2026-10-03T08:03:00Z)
- (audit self) `self: each dropped line was checked against the refusal that enforces it: focus names the missing plan parts; focus prints 'Done needs … (fm gates)' and fm gates names each tier's audits; the red→green refusal now names fm task prove (test added); guard blocks give the grant command per category; state writes are core-guarded. Budget check passes; evals re-synced.` → no findings [tree 662c6e47003e] (2026-10-03T08:03:00Z)
- (audit adversary) `self: each dropped line was checked against the refusal that enforces it: focus names the missing plan parts; focus prints 'Done needs … (fm gates)' and fm gates names each tier's audits; the red→green refusal now names fm task prove (test added); guard blocks give the grant command per category; state writes are core-guarded. Budget check passes; evals re-synced.` → no guard code changed; the guard eval prompts only re-embed the shorter rules, and the removed grant line is still enforced (core, remote and plugin only through fm ask, which the guard requires and the model can't answer) [tree 662c6e47003e] (2026-10-03T08:03:06Z)
- (audit self) `self: each dropped line was checked against the refusal that enforces it: focus names the missing plan parts; focus prints 'Done needs … (fm gates)' and fm gates names each tier's audits; the red→green refusal now names fm task prove (test added); guard blocks give the grant command per category; state writes are core-guarded. Budget check passes; evals re-synced.` → no findings [tree 662c6e47003e] (2026-10-03T08:03:06Z)
## Log
- 2026-10-02T18:35:16Z created
- 2026-10-03T08:01:10Z planned from capture
- 2026-10-03T08:01:10Z focused
- 2026-10-03T08:02:53Z scope: evals re-synced (plugin/tests/e2e) since they embed the rules
- 2026-10-03T08:03:06Z done
- 2026-10-03T08:03:06Z committed 494308d (9 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- research t0018-r3-operator: 3","isSidechain":true,"agentId":"a8c97e63300d81c73","message":{"model":"claude-sonnet-5","id":"msg_011CfSRu7Xczh871gZj2Mqhv","type":"message"…
- T-0132 [SECURITY M, done, 5 steps] Credential audit (fm secrets) and task-tagged commits — lesson: A scanner that gates a commit must read exactly what the commit will t…
- research brainstorm-20260926-r7-slate: whole-hook-path fallback (T-0037, e205da2) · rules/eval copy generation (sync_evals + test) · import-time/latency regression (test…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-02): CHANGELOG.md, plugin/lib/fmcore.py, plugin/rules/foreman.md; re-ground the plan against them before editing
## Lessons
- A rule line that restates a gate costs tokens every session; let the refusal carry the fix and keep the rules for what no gate can see.
## Files touched
- plugin/tests/test_recall.py
- plugin/lib/fmcore.py
- plugin/rules/foreman.md
- CHANGELOG.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
