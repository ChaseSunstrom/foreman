---
id: T-3129
type: FIX
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/agents/fm-builder.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/smith.py, plugin/tests/test_hooks.py, plugin/tests/test_builder.py, plugin/tests/test_cli.py, plugin/tests/test_code.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T03:24:37Z
updated: 2026-11-06T03:52:41Z
batch: [T-3109, T-3114, T-3115, T-3124, T-3125]
---
# Batch: The drive offers tasks to plan and clos…; Fm-builder prompt: builders keep hittin…; An unknown verb (fm models, …
## Raw request
> T-3109: the drive offers tasks to plan and close while a merge chain waits for a quiet window, so closes and suites starve the merge for hours (2026-11-05: 3 h); the drive should see a waiting merge (quiet-merge or lane merge pending) and say: let it land, plan only
> T-3114: fm-builder prompt: builders keep hitting the worktree-isolation refusal (7 failed calls since 00:46, 5 of them cat >> FILE <<EOF or reads of /tmp and the scratchpad); add to plugin/agents/fm-builder.md: append to tests with the Edit tool, never read /tmp or the scratchpad from a lane (line 40 covers only .fm-scratch/)
> T-3115: an unknown verb (fm models, fm kalevala seen this window) gets no steer to a real one: print the nearest verbs and the sampo which hint on an unknown verb
> T-3124: Smith on the 27B (T-3108, local lane): the model wrote a correct fix and test by about turn 30, then reran the tests three times and hit --max-steps 40 with step 1 never marked done; Smith should close a step itself when the step's edits are followed by a green run of its verify command, and the step-done protocol should be one plain line in the model's turn prompt
> T-3125: Smith on the 27B (T-3108): two of its 40 turns went to python3 -c 'import sampo…' calls that Ward refuses; Smith's system text should say: use the sampo CLI and the test runner, never import Sampo's modules in a one-liner
## Interpretation
Reading 1: do T-3109, T-3114, T-3115, T-3124, T-3125 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-3129. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670). Reading 2: each one alone; ruled out because one plan read and one gate run serve them all cheaper.
## Assumptions (confidence)
## Acceptance criteria
- [ ] T-3109: while a lane merge or a queued merge waits (a quiet-merge or lane merge process, or a merge marker in meta), the Stop drive offers only planning, never a close or a suite run, and says the merge waits; with no merge waiting it offers as today — verify with `python3 plugin/tests/run.py test_hooks`
- [ ] T-3114: fm-builder.md tells builders to append to tests with the Edit tool and never read /tmp or the scratchpad from a lane — verify with `python3 plugin/tests/run.py test_builder`
- [ ] T-3115: an unknown verb prints the nearest real verbs and the sampo which hint, exit 2 as today — verify with `python3 plugin/tests/run.py test_cli`
- [ ] T-3124: Smith marks a step done itself when the step's edits are followed by a green run of its verify command, and the turn prompt carries one plain line on how a step is done — verify with `python3 plugin/tests/run.py test_code`
- [ ] T-3125: Smith's system text tells the model to use the sampo CLI and the test runner and never import Sampo's modules in a one-liner — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] T-3109: The drive offers tasks to plan and close while a merge chain waits for a quiet window,…  <- CURRENT
2. [ ] T-3114: Fm-builder prompt: builders keep hitting the worktree-isolation refusal (7 failed calls…
3. [ ] T-3115: An unknown verb (fm models, fm kalevala seen this window) gets no steer to a real one:…
4. [ ] T-3124: Smith on the 27B (T-3108, local lane): the model wrote a correct fix and test by about…
5. [ ] T-3125: Smith on the 27B (T-3108): two of its 40 turns went to python3 -c 'import sampo…' calls…
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:24:37Z created
- 2026-11-05T03:24:52Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_hooks`
- 2026-11-05T03:24:52Z criterion 1 text: T-3109: The drive offers tasks to plan and close while a merge chain waits for a quiet window,… works → T-3109: while a lane merge or a queued merge waits (a quiet-merge or lane merge process, or a merge marker in meta), the Stop drive offers only planning, never a close or a suite run, and says the merge waits; with no merge waiting it offers as today
- 2026-11-05T03:24:53Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_builder`
- 2026-11-05T03:24:53Z criterion 2 text: T-3114: Fm-builder prompt: builders keep hitting the worktree-isolation refusal (7 failed calls… works → T-3114: fm-builder.md tells builders to append to tests with the Edit tool and never read /tmp or the scratchpad from a lane
- 2026-11-05T03:24:54Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_cli`
- 2026-11-05T03:24:54Z criterion 3 text: T-3115: An unknown verb (fm models, fm kalevala seen this window) gets no steer to a real one:… works → T-3115: an unknown verb prints the nearest real verbs and the sampo which hint, exit 2 as today
- 2026-11-05T03:24:54Z criterion 4 verify: `` → `python3 plugin/tests/run.py test_code`
- 2026-11-05T03:24:54Z criterion 4 text: T-3124: Smith on the 27B (T-3108, local lane): the model wrote a correct fix and test by about… works → T-3124: Smith marks a step done itself when the step's edits are followed by a green run of its verify command, and the turn prompt carries one plain line on how a step is done
- 2026-11-05T03:24:55Z criterion 5 verify: `` → `python3 plugin/tests/run.py test_code`
- 2026-11-05T03:24:55Z criterion 5 text: T-3125: Smith on the 27B (T-3108): two of its 40 turns went to python3 -c 'import sampo…' calls… works → T-3125: Smith's system text tells the model to use the sampo CLI and the test runner and never import Sampo's modules in a one-liner
- 2026-11-05T03:24:55Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/agents/fm-builder.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/smith.py', 'plugin/tests/test_hooks.py', 'plugin/tests/test_builder.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_code.py', 'CHANGELOG.md']
- 2026-11-05T03:24:55Z set approved=True
- 2026-11-05T03:24:55Z blocked: approved batch; after T-3087's merge (cli.py), then a builder slot
- 2026-11-06T03:52:41Z unblocked
## Follow-ups captured
