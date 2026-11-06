---
id: T-1704
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/tests/test_docs.py, plugin/tests/fixtures/skill_triggers.json, CHANGELOG.md]
depends_on: [T-1698]
source: user
created: 2026-10-22T22:36:42Z
updated: 2026-10-22T23:34:26Z
base: 393b00413a5e52337645bbc0c2182c3b9cf42ffd
base_tree: 22e76c98821593e99a403b35187f158258bfaa57
plan0_at: 2026-10-22T23:20:03Z
plan0_scope: [plugin/tests/test_docs.py, plugin/tests/fixtures/skill_triggers.json, CHANGELOG.md]
verified: ok
---
# Static trigger eval: phrased requests per skill must match that skill's description best, with no tie
## Raw request
> Static trigger eval: phrased requests per skill must match that skill's description best, with no tie
## Interpretation
Descriptions drift and start competing. A small corpus of plain requests per skill, mined from fm recall and the user's own words, held by a word-overlap ranking, catches that without a model call.
## Assumptions (confidence)
## Acceptance criteria
- [x] for every model-invocable skill, three or more real-sounding requests rank it first by word overlap with no tie; a description change that breaks one fails — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
Options: live model evals (cost, flaky); a static overlap check. Choice: static, cheap, in the suite.
## Risks and rollback
## Execution prompt
## Steps
1. [x] corpus
2. [x] ranking test
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_docs 2>&1 | tail -40` → ✗ exit 1 · Ran 64 tests in 17.7s (15 classes, 16 at a time; slowest: Fences 15s, TaskLifecycle 5s, Site 3s) / FAILED (1 classes) [ran] [tree 323722106284] (2026-10-22T23:20:59Z)
- (ac 1) `python3 plugin/tests/run.py test_docs 2>&1 | tail -8` → exit 0 · Ran 64 tests in 21.4s (15 classes, 16 at a time; slowest: Fences 20s, TaskLifecycle 8s, Site 5s) / OK [ran] [tree 820e0215cfa7] (2026-10-22T23:21:26Z)
- (step 1) `python3 plugin/tests/run.py test_docs 2>&1 | tail -8` → exit 0 · Ran 64 tests in 21.4s (15 classes, 16 at a time; slowest: Fences 20s, TaskLifecycle 8s, Site 5s) / OK [ran] [tree 820e0215cfa7] (2026-10-22T23:21:26Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 64 tests in 20.9s (15 classes, 16 at a time; slowest: Fences 20s, TaskLifecycle 6s, Site 2s) / OK [ran] [tree 820e0215cfa7] (2026-10-22T23:21:52Z)
- (step 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 64 tests in 11.9s (15 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 6s, TaskDocsDrift 3s) / OK [ran] [tree 820e0215cfa7] (2026-10-22T23:22:11Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 64 tests in 8.5s (15 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 97977ea2d54d] (2026-10-22T23:33:21Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 64 tests in 9.1s (15 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 3s, Site 1s) / OK [ran] [tree 7a8c275db192] (2026-10-22T23:33:41Z)
- (audit self) `self: read the ranking test and fixture; 10 model-invocable skills × 3 requests rank first with no tie; user-only skills skipped; a missing entry fails with the line to add` → descriptions now have a regression guard; word-overlap margins are small (1–3 words), so a description edit may need fixture upkeep, by design [tree 7a8c275db192] (2026-10-22T23:33:41Z)
- (audit self) `self: read the ranking test and fixture; 10 model-invocable skills × 3 requests rank first with no tie; user-only skills skipped; a missing entry fails with the line to add` → descriptions now have a regression guard; word-overlap margins are small (1–3 words), so a description edit may need fixture upkeep, by design [tree 7a8c275db192] (2026-10-22T23:34:06Z)
## Log
- 2026-10-22T22:36:42Z created
- 2026-10-22T22:36:43Z set scope=['plugin/tests/test_docs.py', 'plugin/tests/fixtures/skill_triggers.json', 'CHANGELOG.md']
- 2026-10-22T22:36:44Z from T-1692 (skills hardly used; brainstorm-skills-20261022)
- 2026-10-22T22:36:44Z set depends_on=['T-1698']
- 2026-10-22T23:19:10Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1704.builder.md
- 2026-10-22T23:20:03Z focused
- 2026-10-22T23:28:55Z merged worktree-agent-ac5c86c74eb219716 (2 file(s))
- 2026-10-22T23:29:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac5c86c74eb219716
- 2026-10-22T23:33:12Z focused
- 2026-10-22T23:34:06Z scope: MASTER.md, fmplaybooks.py, playbooks SKILL.md and test_playbook_evals.py are T-1618's, edited while T-1704's merge was pending; committed under T-1618
- 2026-10-22T23:34:24Z done
- 2026-10-22T23:34:26Z committed 889cef16 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- research T-1396-review: Verdict: changes needed.** I found two crashes on a malformed marketplace, one way the trust ledger can be laundered, and some bypasses and false…
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Lessons
- A static overlap eval catches skill descriptions drifting into each other without a model call
## Files touched
- plugin/tests/test_docs.py
- plugin/tests/fixtures/skill_triggers.json
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmplaybooks.py
- plugin/skills/playbooks/SKILL.md
- plugin/tests/test_playbook_evals.py
