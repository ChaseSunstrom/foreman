---
id: T-2866
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T01:45:24Z
updated: 2026-11-04T01:49:44Z
base: 5ca8ac7335e1c66cccd5da6575b8dfea66503d63
base_tree: 971d90a71e9b8a01760b2bd8a5b1a9a98c4e79df
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T01:48:59Z
plan0_scope: []
verified: strong
---
# A criterion's verify check refuses the Sampo alias verbs that run fine (sampo moons…
## Raw request
> FIX: a criterion's verify check refuses the Sampo alias verbs that run fine (sampo moons check: 'unknown moons'); the validator must resolve the same aliases the CLI does (moons, rune, louhi, ward, underworld, smith)
## Interpretation
Reading 1 (chosen): core.unrunnable() parses an fm/sampo verify command with the bare parser, so Sampo's own verb names (moons, rune, louhi, ward, smith, underworld), which cli.main turns into the real verbs through _alias, read as unknown commands, and a criterion that runs fine is refused. It must normalise argv the way main does. Reading 2 (ruled out): add the aliases as real subparsers; RENAMES is the single table main reads, and a second registration would drift.
## Assumptions (confidence)
## Acceptance criteria
- [x] a criterion verified by a Sampo alias verb (sampo moons check, sampo rune status) is accepted, and a real unknown verb is still refused — verify with `python3 plugin/tests/run.py test_verify_alias`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test on core.unrunnable, then normalise argv through cli._alias
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_verify_alias` → ✗ exit 1 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: VerifyAlias 0s) / FAILED (1 classes: test_verify_alias.VerifyAlias) (start tree + this task's tests) [ran] [tree 9e69f8732801] [world 2f1906870a] (2026-11-04T01:49:08Z)
- `python3 plugin/tests/run.py test_verify_alias` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: VerifyAlias 0s) / FAILED (1 classes: test_verify_alias.VerifyAlias) [ran] [tree 9e69f8732801] [world 2f1906870a] (2026-11-04T01:49:08Z)
- (step 1) `python3 plugin/tests/run.py test_verify_alias` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: VerifyAlias 0s) / OK [ran] [tree d3e7d6940c86] [world 2f1906870a] (2026-11-04T01:49:17Z)
- `python3 plugin/tests/run.py test_verify_alias` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: VerifyAlias 0s) / FAILED (1 classes: test_verify_alias.VerifyAlias) (start tree + this task's tests) [ran] [tree d3e7d6940c86] [world 2f1906870a] (2026-11-04T01:49:20Z)
- `python3 plugin/tests/run.py test_verify_alias` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: VerifyAlias 0s) / OK [ran] [tree d3e7d6940c86] [world 2f1906870a] (2026-11-04T01:49:20Z)
- (ac 1) `python3 plugin/tests/run.py test_verify_alias` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T01:49:20Z [ran] [tree d3e7d6940c86] [world 2f1906870a] (2026-11-04T01:49:21Z)
- (audit edge) `self-review: unrunnable now parses through cli._alias, the same normalisation main applies first, so Sampo's verb names validate as they run; an unknown verb still fails parse` → 'sampo louhi --help' exits 0 at parse (SystemExit 0 is not an error); a misspelt alias is still refused [tree d3e7d6940c86] (2026-11-04T01:49:21Z)
- (audit self) `self-review: unrunnable now parses through cli._alias, the same normalisation main applies first, so Sampo's verb names validate as they run; an unknown verb still fails parse` → no findings [tree d3e7d6940c86] (2026-11-04T01:49:21Z)
## Log
- 2026-11-04T01:45:24Z created
- 2026-11-04T01:48:58Z set tier=S
- 2026-11-04T01:48:58Z planned: it has criteria and steps
- 2026-11-04T01:48:59Z focused
- 2026-11-04T01:48:59Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T01:49:43Z done
- 2026-11-04T01:49:44Z committed cf8cbdc1 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
## Why not caught
T-2766 added RENAMES to main's argv path, and the verify validator kept parsing the raw words
## Files touched
- plugin/tests/test_verify_alias.py
- plugin/lib/sampo/core.py
