---
id: T-0119
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T04:01:08Z
updated: 2026-10-03T08:18:04Z
base: 0765a28482c9690711f0b1e4fbb70959f3bb279d
base_tree: 0c688adc03ae4e28426be04cd3630fb4ba9d7594
verified: ok
---
# Standing core yes: one approval covers Foreman's own code for every task until turned off
## Raw request
> is there any way you can make it so when you're working on foreman you don't have to ask to edit it? and can you do that now so you can be fully auto
## Interpretation
User: when working on Foreman, don't ask to edit it for every task; do it now so Foreman runs fully auto. A standing grant, given once through Claude Code's permission prompt, revocable.
## Assumptions (confidence)
## Acceptance criteria
- [x] standing yes covers later tasks' core code edits; settings, state and fmguard.py still ask; fm standing off revokes; non-core standing refused — verify with `python3 -m unittest discover -s plugin/tests -q -p test_hooks.py`
- [x] all gates — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) fm ask ID core --standing: the dialog says it covers every later task; the approved prompt records project meta standing.core; the guard lets core edits under Foreman's code dirs through, not Claude Code settings, state, or fmguard.py; fm standing off revokes; (b) a settings flag the agent sets. Choice (a): consent still comes only from the user's answer in the dialog (an agent can't self-grant), scoped to code, revocable, logged. (b) would let the agent grant itself.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests
2. [x] fm ask --standing, dialog text, grant, guard ctx, fm standing
3. [x] docs, rules line, gates, adversary review
## Resume here
## Docs impact
README.md, MASTER.md, CHANGELOG.md, plugin/rules/foreman.md: standing yes
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -q -p test_hooks.py -k standing` → red: 2 tests fail (no --standing yet) (2026-10-03T04:02:44Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -q -p test_hooks.py` → exit 0 · Ran 112 tests in 51.653s / OK [ran] [tree 042cabaff3f0] (2026-10-03T04:04:56Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -q -p test_hooks.py` → all hook tests pass incl. standing (2026-10-03T04:04:56Z)
- (step 3) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → ✗ exit 1 · 2 of 4 failed: python3 -m unittest discover -s plugin/tests -q → ✗ exit 1 · Ran 534 tests in 153.116s / FAILED (failures=6); fm doctor → ✗ exit 1 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: FAILED (24 pass, 1 warn, 1 fail) [ran] [tree 042cabaff3f0] (2026-10-03T04:07:55Z)
- (step 3) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 534 tests in 151.080s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.1    32.4     150  [0] / SessionEnd                  28.1    31.0     150  [0] [ran] [tree 6c173200971d] (2026-10-03T04:17:15Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -q -p test_hooks.py` → exit 0 · Ran 112 tests in 48.453s / OK [ran] [tree 6c173200971d] (2026-10-03T04:18:19Z)
- (ac 2) `fm check` → exit 0 · ✓ all 4 gates passed on this exact tree already (run at 04:17 UTC); cached (fm check --fresh reruns) [ran] [tree 6c173200971d] (2026-10-03T04:18:19Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -q -p test_hooks.py` → exit 0 · Ran 112 tests in 48.453s / OK [ran] [tree 6c173200971d] (2026-10-03T04:18:19Z)
- (audit intent) `self-review of grant path, guard check and dialog` → one yes in the permission prompt covers Foreman's code for every later task; fm standing off revokes; session note shows it [tree 6c173200971d] (2026-10-03T04:18:19Z)
- (audit adversary) `self-review of grant path, guard check and dialog` → only an approved dialog for that tool_use_id grants it (tested without dialog → nothing); fm standing has no on; meta writes stay state-direct; interpreter code driving modules is core with a non-path detail, never covered; fmguard.py and whole-tree writes containing it still ask; --standing with other categories refused in fm and the dialog. Known ceiling, said in the dialog: with Foreman's code writable the agent could change grant code in fmhooks/fmcli; the guard file stays a per-task yes [tree 6c173200971d] (2026-10-03T04:18:19Z)
## Log
- 2026-10-03T04:01:08Z created
- 2026-10-03T04:02:31Z planned from capture
- 2026-10-03T04:02:31Z focused
- 2026-10-03T04:02:52Z user approved core in Claude Code's permission prompt
- 2026-10-03T04:18:19Z done
- 2026-10-03T08:18:04Z includes T-0110: One yes for several queued core tasks (queue preflight of predictable yeses)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- research T-0108-review: [instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok
- playbook Loop Design + Review (skills/playbooks/references/evals/loop-design-check.md)
- research t0018-r2-intent: xt — can be created without ever asking the user, directly contradicting the explicit requirement in T-0023's captured text.\nFix: either route…
## Lessons
- A standing grant is safe only if it comes from the same consent channel as a single one and stays narrower than the category
## Files touched
- plugin/tests/test_hooks.py
- README.md
- MASTER.md
- CHANGELOG.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmcli.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/rules/foreman.md
