---
id: T-1503
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references, plugin/skills/playbooks/SKILL.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:15Z
updated: 2026-10-22T18:38:41Z
base: c03b8b200ee711eaf675682c591d05c63afb5d3b
base_tree: df261d4acf01b41cc8529aadb39060cc4fba4182
plan0_at: 2026-10-22T18:20:09Z
plan0_scope: [plugin/skills/playbooks/references]
verified: strong
---
# Engineering playbooks: SQL, migrations, text/time/bytes, dependencies, characterisation, deprecation, decision memos
## Raw request
> Engineering playbooks: SQL, migrations, text/time/bytes, dependencies, characterisation, deprecation, decision memos
## Interpretation
Brainstorm T-1479 cluster 10: procedures Claude reaches for that are missing: sql (query review, indexes, explain), migration (expand/contract, backfill, rollback), text-time-bytes (encodings, time zones, money), dependency-admission (what to check before adding one), characterisation-tests (pin behaviour before a refactor), deprecation (announce, shim, remove), decision-memo (options, choice, why, revisit date). Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] the seven playbooks exist with a 'Use when' line and a numbered procedure — verify with `for f in plan/decision-memo clean/characterisation-tests clean/deprecation release/dependency-admission fix/migration fix/sql fix/text-time-bytes; do python3 -c "t=open('plugin/skills/playbooks/references/$f.md').read(); miss=[s for s in ['Use when','1.',] if s not in t]; assert not miss, miss" || exit 1; done`
## Non-goals
## Approach (options → choice → why)
Options: port third-party guides (licence, voice); one omnibus engineering playbook (too long to load); chosen: seven short original playbooks in their natural stages (plan/decision-memo, clean/characterisation-tests, clean/deprecation, release/dependency-admission, fix/migration, fix/sql, fix/text-time-bytes), each a Use-when line and a numbered procedure with checks, linked to library cards; index lines in SKILL.md, or a stage INDEX.md where one exists.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write the seven playbooks
## Resume here
## Docs impact
plugin/skills/playbooks/SKILL.md
## Verification evidence
- (step 1) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ac.py` → exit 0 · ok fix/sql 53 lines / ok fix/text-time-bytes 56 lines [ran] [tree 60b67cc4dc52] (2026-10-22T18:23:41Z)
- (step 1) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/runblocks.py` → exit 0 · ['SEARCH orders USING COVERING INDEX orders_customer_created (customer_id=?)'] / fix/text-time-bytes rc 0 [ran] [tree 8cff37a54a25] (2026-10-22T18:29:10Z)
- (ac 1) `for f in plan/decision-memo clean/characterisation-tests clean/deprecation release/dependency-admission fix/migration fix/sql fix/text-time-bytes; do python3 -c "t=open('plugin/skills/playbooks/references/$f.md').read(); miss=[s for s in ['Use when','1.',] if s not in t]; assert not miss, miss" || exit 1; done` → exit 0 · (no output) [ran] [tree 40b2bc79092a] (2026-10-22T18:38:14Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 106 tests in 2.2s (31 classes, 16 at a time; slowest: Command 2s, TaskLifecycle 2s, ViewsRepair 2s) / OK [ran] [tree 40b2bc79092a] (2026-10-22T18:38:16Z)
- (ac 1) `for f in plan/decision-memo clean/characterisation-tests clean/deprecation release/dependency-admission fix/migration fix/sql fix/text-time-bytes; do python3 -c "t=open('plugin/skills/playbooks/references/$f.md').read(); miss=[s for s in ['Use when','1.',] if s not in t]; assert not miss, miss" || exit 1; done` → exit 0 · (no output) [ran] [tree 40b2bc79092a] (2026-10-22T18:38:26Z)
- (audit intent) `one fm-reviewer pass (technical accuracy): 5 MEDIUM + 5 LOW, all fixed by the builder in f86db135; every Python snippet re-run with python3 -I` → seven playbooks with Use when and numbered procedures, indexed in SKILL.md [tree 40b2bc79092a] (2026-10-22T18:38:26Z)
- (audit adversary) `one fm-reviewer pass (technical accuracy): 5 MEDIUM + 5 LOW, all fixed by the builder in f86db135; every Python snippet re-run with python3 -I` → dependency admission no longer runs install scripts before reading them; pin files scrubbed of secrets before commit [tree 40b2bc79092a] (2026-10-22T18:38:26Z)
- (audit edge) `one fm-reviewer pass (technical accuracy): 5 MEDIUM + 5 LOW, all fixed by the builder in f86db135; every Python snippet re-run with python3 -I` → Postgres 17-and-older NOT NULL, unique via index, INVALID index after a failed CONCURRENTLY build, MySQL lock_wait_timeout [tree 40b2bc79092a] (2026-10-22T18:38:26Z)
- (audit maintainer) `one fm-reviewer pass (technical accuracy): 5 MEDIUM + 5 LOW, all fixed by the builder in f86db135; every Python snippet re-run with python3 -I` → test_docs and test_doctor pass; SKILL.md 9,489 of 10,000 chars [tree 40b2bc79092a] (2026-10-22T18:38:26Z)
- (audit intent) `one fm-reviewer pass (technical accuracy): 5 MEDIUM + 5 LOW, all fixed by the builder in f86db135; every Python snippet re-run with python3 -I` → seven playbooks with Use when and numbered procedures, indexed in SKILL.md [tree 7ebc09218f63] (2026-10-22T18:38:38Z)
- (audit adversary) `one fm-reviewer pass (technical accuracy): 5 MEDIUM + 5 LOW, all fixed by the builder in f86db135; every Python snippet re-run with python3 -I` → dependency admission no longer runs install scripts before reading them; pin files scrubbed of secrets before commit [tree 7ebc09218f63] (2026-10-22T18:38:38Z)
- (audit edge) `one fm-reviewer pass (technical accuracy): 5 MEDIUM + 5 LOW, all fixed by the builder in f86db135; every Python snippet re-run with python3 -I` → Postgres 17-and-older NOT NULL, unique via index, INVALID index after a failed CONCURRENTLY build, MySQL lock_wait_timeout [tree 7ebc09218f63] (2026-10-22T18:38:38Z)
- (audit maintainer) `one fm-reviewer pass (technical accuracy): 5 MEDIUM + 5 LOW, all fixed by the builder in f86db135; every Python snippet re-run with python3 -I` → test_docs and test_doctor pass; SKILL.md 9,489 of 10,000 chars [tree 7ebc09218f63] (2026-10-22T18:38:38Z)
## Log
- 2026-10-22T17:36:15Z created
- 2026-10-22T18:19:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1503.builder.md
- 2026-10-22T18:20:08Z focused
- 2026-10-22T18:38:02Z merged worktree-agent-a2be3c96ddc34eed7 (8 file(s))
- 2026-10-22T18:38:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2be3c96ddc34eed7
- 2026-10-22T18:38:06Z focused
- 2026-10-22T18:38:31Z set scope=['plugin/skills/playbooks/references', 'plugin/skills/playbooks/SKILL.md', 'CHANGELOG.md']
- 2026-10-22T18:38:32Z scope: SKILL.md indexes the seven playbooks (test_docs requires every playbook named); CHANGELOG line for the release
- 2026-10-22T18:38:39Z done
- 2026-10-22T18:38:41Z committed da3f8e19 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1495 [FEATURE M, done, 2 steps] 3D template: a zero-dependency single-file WebGL2 scene — lesson: A probe that can't drive animation frames (dump-dom) passes vacuously…
- T-1491 [FEATURE M, done, 2 steps] UI playbook: interaction, forms, microcopy and mobile — lesson: Probes in playbooks should print text, so fm code (no image input) can …
- T-1490 [FEATURE M, done, 2 steps] UI playbook: composition, depth and states — lesson: Ship a measuring probe with a layout playbook; prose rules about rhythm are unrevi…
- decision 2026-10-22: Slate: round 1 = T-1488..T-1506 (19 tasks over clusters 1-11), round 2 = T-1507..T-1519 (clusters 12-24); skipped: clusters 25-26 (built already, or…
## Preflight
Changed in scope since this was planned (2026-10-22): plugin/skills/playbooks/references/build/INDEX.md, plugin/skills/playbooks/references/build/csharp-build.md, plugin/skills/playbooks/references/build/go-build.md, plugin/skills/playbooks/references/b…; re-ground the plan against them before editing
## Why not caught
nothing runs or version-checks the SQL in playbooks; a reviewer with the docs caught it
## Lessons
- Playbook advice that names database behaviour needs the version it holds for (NOT NULL on Postgres ≤17, NOT VALID for unique): unversioned DDL advice is wrong somewhere
## Files touched
- plugin/skills/playbooks/references/fix/sql.md
- plugin/skills/playbooks/references/fix/migration.md
- plugin/skills/playbooks/references/fix/text-time-bytes.md
- plugin/skills/playbooks/references/clean/characterisation-tests.md
- plugin/skills/playbooks/references/clean/deprecation.md
- plugin/skills/playbooks/references/release/dependency-admission.md
- plugin/skills/playbooks/references/plan/decision-memo.md
- plugin/skills/playbooks/SKILL.md
- CHANGELOG.md
