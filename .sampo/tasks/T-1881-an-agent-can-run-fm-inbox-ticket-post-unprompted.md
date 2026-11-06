---
id: T-1881
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md]
depends_on: [T-1898]
source: discovered
created: 2026-10-28T23:41:08Z
updated: 2026-10-29T05:17:16Z
base: 4fc45cd54af39facdd36a088dbf946ad6d11a5bd
base_tree: 420efebfc1e427517c4412f48f51ac7b2a5cbb45
plan0_at: 2026-10-29T04:38:32Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# An agent can run `fm inbox ticket --post` unprompted, because the only barrier is document
## Raw request
> an agent can run `fm inbox ticket --post` unprompted, because the only barrier is documentation. A guard category or an `fm ask` step for outward posts would enforce "only when asked"
> (noticed by an agent; research T-1870-review)
## Interpretation
The guard treats fm inbox ticket --post (in any spelling, and via python3 .../fm) as a publish, so an outward post needs the publish grant like any release.
## Assumptions (confidence)
## Acceptance criteria
- [x] --post is a publish; a plain ticket is not — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
Options: a new outward category; a hook in fminbox; reuse publish in _check_publish. Choice: reuse publish — one rule, existing grant path, replay covers it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Publish table rows red
2. [x] _check_publish rule; green, docs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 292 tests in 10.5s (88 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 8s, Trust 7s) / OK [ran] [tree ded7edcabe94] (2026-10-29T05:16:41Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_replay` → exit 0 · Ran 300 tests in 7.8s (89 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree ded7edcabe94] (2026-10-29T05:16:49Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 292 tests in 7.8s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree ded7edcabe94] (2026-10-29T05:17:05Z)
- (audit adversary) `read the merged lane diff; probed spellings (abbreviated flags, -p/--project ahead, plugin/bin/fm, python3 …/fm); fixed the project-flag gap test-first` → --pos and --po= are refused by fm's parser (allow_abbrev off); -p PROJECT ahead of the subcommand slipped past the positional match: now any position; env/VAR= prefixes reach _check_publish through the shared command walk [tree ded7edcabe94] (2026-10-29T05:17:05Z)
- (audit edge) `read the merged lane diff; probed spellings (abbreviated flags, -p/--project ahead, plugin/bin/fm, python3 …/fm); fixed the project-flag gap test-first` → fm pr --post is left out on purpose: fmcli checks and spends the publish grant itself (T-1167) [tree ded7edcabe94] (2026-10-29T05:17:05Z)
- (audit intent) `read the merged lane diff; probed spellings (abbreviated flags, -p/--project ahead, plugin/bin/fm, python3 …/fm); fixed the project-flag gap test-first` → an agent can't post to someone's issue without the publish grant [tree ded7edcabe94] (2026-10-29T05:17:05Z)
- (audit self) `read the merged lane diff; probed spellings (abbreviated flags, -p/--project ahead, plugin/bin/fm, python3 …/fm); fixed the project-flag gap test-first` → no findings [tree ded7edcabe94] (2026-10-29T05:17:05Z)
## Log
- 2026-10-28T23:41:08Z created
- 2026-10-29T00:38:46Z set tier=S, scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-29T00:53:51Z set status=planned
- 2026-10-29T01:18:56Z plan re-read: fmguard moved (T-1887/T-1888 drafts); T-1881's draft re-applied clean on top of them, test_guard green
- 2026-10-29T02:55:57Z set depends_on=['T-1898']
- 2026-10-29T04:38:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1881.builder.md
- 2026-10-29T04:38:31Z focused
- 2026-10-29T05:15:09Z merged worktree-agent-ada41985ca3f01b81 (3 file(s))
- 2026-10-29T05:15:12Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ada41985ca3f01b81
- 2026-10-29T05:15:13Z focused
- 2026-10-29T05:17:14Z done
- 2026-10-29T05:17:16Z committed 9cc8efbd (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1870-review: Approve with nits. The five focus areas hold up. The findings are one MEDIUM and three LOW, and none block the change. [stale: plugin/lib/fmcli.p…
- T-1870 [FEATURE M, done, 3 steps] Fm inbox ticket --post T-xxxx posts the closing commit back to its source issue — lesson: an outward write needs a claim under the lock…
- T-1167 [FEATURE S, done, 2 steps] Add `fm pr ID --post` that posts the rendered PR body as a comment on the current branch's
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Preflight
Changed in scope since this was planned (2026-10-28): CHANGELOG.md, MASTER.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py; re-ground the plan against them before editing
## Lessons
- A subcommand match on the first positionals misses a global flag's value ahead of it; match the words anywhere
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmguard.py
