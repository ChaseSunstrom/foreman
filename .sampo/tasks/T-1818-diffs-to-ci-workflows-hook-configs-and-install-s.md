---
id: T-1818
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T08:05:11Z
updated: 2026-10-28T08:11:35Z
base: 06bd383a4182e63a605c22274abad860c4ee3c01
base_tree: 5724f740e60805b755eba441222cb3194a41ba19
plan0_at: 2026-10-28T08:08:38Z
plan0_scope: []
verified: strong
---
# Diffs to CI workflows, hook configs and install scripts require the adversary lens: fmcore.sensitive counts them (they run with CI's token or the user's authority)
## Raw request
> Diffs to CI workflows, hook configs and install scripts require the adversary lens: fmcore.sensitive counts them (they run with CI's token or the user's authority)
## Interpretation
From the T-1798 brainstorm (supply chain, value 5): grounded, no card or user confirm (full autonomy); the gap is that these paths don't make the adversary lens required
## Assumptions (confidence)
## Acceptance criteria
- [x] sensitive() names .github/workflows/*.yml, .gitlab-ci.yml, hooks/hooks.json, .claude/settings*.json, .pre-commit-config.yaml, .husky/*, install*.sh — verify with `python3 plugin/tests/run.py test_sensitive`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test for the paths, then widen the path rule
## Resume here
## Docs impact
CHANGELOG Unreleased entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_sensitive test_round_f test_map` → exit 0 · Ran 26 tests in 6.1s (10 classes, 16 at a time; slowest: RoundF 6s, Map 5s, PreToolUse 2s) / OK [ran] [tree 1b9d55b3b400] (2026-10-28T08:09:22Z)
- (step 1) `python3 plugin/tests/run.py test_sensitive test_round_f test_map` → exit 0 · Ran 26 tests in 4.8s (10 classes, 16 at a time; slowest: RoundF 4s, Map 4s, PreToolUse 2s) / OK [ran] [tree 8812b422ea83] (2026-10-28T08:09:53Z)
- (ac 1) `python3 plugin/tests/run.py test_sensitive` → exit 0 · Ran 7 tests in 1.5s (7 classes, 16 at a time; slowest: PreToolUse 1s, NightGuards 0s, SessionStart 0s) / OK [ran] [tree 8812b422ea83] (2026-10-28T08:09:55Z)
- (audit adversary) `self: read both regex uses; ran the sensitive, round-f and map tests` → the change widens the adversary requirement; a false positive (docs/Dockerfile-notes.md) only asks one more lens line [tree 8812b422ea83] (2026-10-28T08:09:55Z)
- (audit edge) `self: read both regex uses; ran the sensitive, round-f and map tests` → workflows, hooks.json, settings*.json, install*.sh, pre-commit, husky, gitlab-ci counted; docs named after them are not [tree 8812b422ea83] (2026-10-28T08:09:55Z)
- (audit maintainer) `self: read both regex uses; ran the sensitive, round-f and map tests` → one regex in fmcore shared by sensitive() and fmmap's risk; cost at scale — an extra lens line on the few tasks touching CI or hook config [tree 8812b422ea83] (2026-10-28T08:09:55Z)
- (audit self) `self: read both regex uses; ran the sensitive, round-f and map tests` → no findings [tree 8812b422ea83] (2026-10-28T08:09:55Z)
- (step 1) `python3 plugin/tests/run.py test_sensitive test_round_f test_map test_diff_gates` → exit 0 · Ran 39 tests in 9.0s (12 classes, 16 at a time; slowest: DiffGates 9s, RoundF 3s, Map 2s) / OK [ran] [tree 6ee28de63fac] (2026-10-28T08:11:16Z)
- (audit adversary) `self: read both regex uses; ran the linked tests (219)` → the change widens the adversary requirement; a false positive (docs/Dockerfile-notes.md) only asks one more lens line [tree 6ee28de63fac] (2026-10-28T08:11:17Z)
- (audit edge) `self: read both regex uses; ran the linked tests (219)` → workflows, hooks.json, settings*.json, install*.sh, pre-commit, husky, gitlab-ci counted; docs named after them are not [tree 6ee28de63fac] (2026-10-28T08:11:17Z)
- (audit maintainer) `self: read both regex uses; ran the linked tests (219)` → one regex in fmcore shared by sensitive() and fmmap's risk; cost at scale — an extra lens line on the few tasks touching CI, build or hook config [tree 6ee28de63fac] (2026-10-28T08:11:17Z)
- (audit self) `self: read both regex uses; ran the linked tests (219)` → no findings [tree 6ee28de63fac] (2026-10-28T08:11:17Z)
## Log
- 2026-10-28T08:05:11Z created
- 2026-10-28T08:08:37Z focused
- 2026-10-28T08:11:07Z steer: test_diff_gates used Makefile as a plain out-of-scope file; now tox.ini, since Makefile is sensitive by design
- 2026-10-28T08:11:33Z done
- 2026-10-28T08:11:35Z committed dee26583 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261015-154003: Request: have FM enforce some things so we don't rely on agents to do it themselves as they are inconsistent (context: 19 card-writer s…
- research t0018-final-intent: HIGH — round 6 shipped with no recorded reviewer audit — `research/` (missing `t0018-r6-*` files) vs `tasks/T-0018-...md:81`.
- playbook Intent-Driven Development (fm playbooks show plan/intent-driven-development)
- decision 2026-10-09: [costly] Build all 70 'build' capabilities from the Foreman brainstorm in value-for-effort rounds (security first); the user's ticks on the punch li…
## Why not caught
none: a coverage gap, not a bug; the brainstorm's adversary lens found it
## Files touched
- plugin/tests/test_round_f.py
- plugin/lib/fmcore.py
- plugin/lib/fmmap.py
- CHANGELOG.md
- plugin/tests/test_diff_gates.py
