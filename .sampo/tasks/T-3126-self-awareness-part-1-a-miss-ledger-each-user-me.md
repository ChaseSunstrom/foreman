---
id: T-3126
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T03:20:43Z
updated: 2026-11-05T15:09:53Z
builder_model: haiku
base: ba5d3c9a516c083c9469978c0b161bc676186521
base_tree: 9562e51b003f56176ffae9feebaf063bbdb0523b
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T04:57:37Z
plan0_scope: []
lane_stop: refused 2026-11-05T14:28:56Z
postmerge_red: test_cli.HelpRegistrations
postmerge_sha: d5fe1bb4d682cb844c2682322a3c6d4b65670f69
verified: strong
unproven: [docs]
---
# Self-awareness part 1: a miss ledger: each user message that points something out is logged with its class, and sampo misses shows them by class and per day (T-3123)
## Raw request
> Self-awareness part 1: a miss ledger: each user message that points something out is logged with its class, and sampo misses shows them by class and per day (T-3123)
## Interpretation
Reading 1 (chosen): the UserPromptSubmit hook classifies a message that points something out (why isn't X done, are you also, have you tried, how come, can we improve, you missed) into the miss classes (stalled ask, unfiled workaround, unmeasured wait, invisible output, unreachable goal, unused capability, dead or silent job, other) by plain patterns first and a cheap local model only when no pattern matches, logs it with the turn, and sampo misses lists them by class and day with the trend. Reading 2: count all questions; rejected, most questions aren't misses.
## Assumptions (confidence)
## Acceptance criteria
- [x] tonight's six pointing-out messages (2026-11-05: the stalled charts, unfiled bugs, merge speed, local models on real tasks, viewing cards, self-awareness) are each logged with the right class from their text; a plain request or a thanks is not a miss; sampo misses prints counts by class and per day — verify with `python3 plugin/tests/run.py test_self_aware`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the clause and steer detectors in hooks.py, the ledger, a pattern table seeded from tonight's six messages; likely outcome: a per-day miss count that tells whether the checks work. 2. Do less: log every message; fails if: the count means nothing. 3. A model classifies every message; fails if: a model call per prompt costs latency on every turn. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests from tonight's messages and three non-misses
2. [x] the classifier, the store, sampo misses
## Resume here
## Docs impact
CHANGELOG line; MASTER.md and docs/map/files-lib-3.md list selfaware.py; sampo misses in the Reports help
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_self_aware` → ✗ exit 1 · Ran 4 tests in 2.3s (2 classes, 16 at a time; slowest: Ledger 1s, Classify 0s) / FAILED (2 classes: test_self_aware.Classify, test_self_aware.Ledger) [ran] [tree 0b167f15cc5f] [world 2f1906870a] (2026-11-05T04:58:44Z)
- (step 2) `python3 plugin/tests/run.py test_self_aware` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: Ledger 0s, Classify 0s) / OK [ran] [tree 31e1122bd473] [world 2f1906870a] (2026-11-05T05:04:34Z)
- (step 2) `python3 plugin/tests/run.py test_self_aware` → exit 0 · Ran 4 tests in 4.9s (2 classes, 16 at a time; slowest: Ledger 4s, Classify 0s) / OK [ran] [tree 31e1122bd473] [world 2f1906870a] (2026-11-05T05:04:49Z)
- (step 2) `python3 plugin/tests/run.py test_self_aware` → exit 0 · Ran 4 tests in 3.0s (2 classes, 16 at a time; slowest: Ledger 2s, Classify 0s) / OK [ran] [tree 31e1122bd473] [world 2f1906870a] (2026-11-05T05:09:28Z)
- (step 2) `python3 plugin/tests/run.py test_self_aware test_cli test_hooks test_rename_aliases test_board_verbs` → exit 0 · Ran 431 tests in 79.5s (404 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 41s, StateViews.test_state_md_is_bounded 36s, SessionStart.test_the_whole_note_fits_one_budget_ [ran] [tree 7c81204a949d] [world 2f1906870a] (2026-11-05T15:09:13Z)
- `python3 plugin/tests/run.py test_self_aware test_cli.HelpRegistrations` → ✗ exit 1 · Ran 6 tests in 3.1s (3 jobs, 16 at a time; slowest: Ledger 1s, HelpRegistrations 0s, Classify 0s) / FAILED (2 classes: test_self_aware.Classify, test_self_aware.Ledger) (start tree + this task's tests) [ran] [tree 58813900910e] [world 2f1906870a] (2026-11-05T15:09:31Z)
- `python3 plugin/tests/run.py test_self_aware test_cli.HelpRegistrations` → exit 0 · Ran 6 tests in 1.4s (3 jobs, 16 at a time; slowest: Ledger 1s, HelpRegistrations 0s, Classify 0s) / OK [ran] [tree 58813900910e] [world 2f1906870a] (2026-11-05T15:09:31Z)
- (ac 1) `python3 plugin/tests/run.py test_self_aware` → exit 0 · Ran 4 tests in 1.2s (2 jobs, 16 at a time; slowest: Ledger 1s, Classify 0s) / OK [ran] [tree 58813900910e] [world 2f1906870a] (2026-11-05T15:09:35Z)
- (audit intent) `re-landed after its post-merge revert: the red was real (test_cli.HelpRegistrations: 'misses' reused help position 1031, which 'triggers' holds); re-applied on main from its merged tree (selfaware.py, the shim and the test identical to it; cli.py, hooks.py, MASTER.md, docs map by sampo edit from its own diff), moved to 1032; test_self_aware test_cli test_hooks test_rename_aliases test_board_verbs 431 OK` → a message that points something out is logged as a miss with its class; requests and thanks are not; sampo misses counts by class and day; the hook never asks a model (patterns only), --sweep asks the local model with a fixed class list [tree 58813900910e] (2026-11-05T15:09:35Z)
- (audit edge) `re-landed after its post-merge revert: the red was real (test_cli.HelpRegistrations: 'misses' reused help position 1031, which 'triggers' holds); re-applied on main from its merged tree (selfaware.py, the shim and the test identical to it; cli.py, hooks.py, MASTER.md, docs map by sampo edit from its own diff), moved to 1032; test_self_aware test_cli test_hooks test_rename_aliases test_board_verbs 431 OK` → an unknown class from the model counts as no miss; a thanks never reaches the model; note() never raises, so the prompt hook can't fail on it [tree 58813900910e] (2026-11-05T15:09:35Z)
- (audit adversary) `re-landed after its post-merge revert: the red was real (test_cli.HelpRegistrations: 'misses' reused help position 1031, which 'triggers' holds); re-applied on main from its merged tree (selfaware.py, the shim and the test identical to it; cli.py, hooks.py, MASTER.md, docs map by sampo edit from its own diff), moved to 1032; test_self_aware test_cli test_hooks test_rename_aliases test_board_verbs 431 OK` → a logged miss stores the message redacted and cut to 300 chars; the local model's answer is accepted only when it is one of the fixed class words, so it can't inject a label or text [tree 58813900910e] (2026-11-05T15:09:35Z)
## Log
- 2026-11-05T03:20:43Z created
- 2026-11-05T03:20:50Z set approved=True
- 2026-11-05T03:20:50Z blocked: approved; waits for a builder slot
- 2026-11-05T04:56:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3126.builder.md
- 2026-11-05T04:57:11Z builder slot freed
- 2026-11-05T04:57:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3126.builder.md
- 2026-11-05T04:57:32Z focused
- 2026-11-05T04:57:37Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T13:09:52Z merge held by the self-change gate: verbs 166 -> 167 (+1: misses); waits for the user's yes (sampo ask T-3126 core) in the morning report
- 2026-11-05T13:22:54Z user approved core in Claude Code's permission prompt
- 2026-11-05T14:20:03Z merged worktree-agent-a2ab8805d173f4bee (7 file(s))
- 2026-11-05T14:20:03Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2ab8805d173f4bee
- 2026-11-05T14:28:56Z red after merge: test_cli.HelpRegistrations; d5fe1bb4d reverted
- 2026-11-05T15:05:20Z focused
- 2026-11-05T15:09:36Z affected tests waived: the only names that can't match are T-3160's (test_callcards, test_smith_cards), merged and reverted inside this task's window and not on disk; T-3126's own and the classes its revert named pass (431 
- 2026-11-05T15:09:49Z done
- 2026-11-05T15:09:53Z committed ccd6e3b8 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3123 [FEATURE L, blocked, 3 steps] Self-awareness: Sampo notices what the user would otherwise point out: a miss ledger from the user's pointing-out messages, turn-end…
- decision 2026-11-05: standing (user 2026-11-05): self-checks before every reply: stalled asks, unfiled workarounds, unmeasured waits, invisible outputs, unreachable goal…
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- T-2878 [FEATURE L, blocked, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- similar past tasks were L: consider --tier L
## Lessons
- A new verb's help position must be unique: pick a free slot, and run test_cli.HelpRegistrations in the lane
## Plan gaps
- failed first: step 1 failing tests from tonight's messages and three non-misses
## Files touched
- plugin/tests/test_self_aware.py
- plugin/lib/sampo/selfaware.py
- plugin/lib/fmselfaware.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/hooks.py
- MASTER.md
- docs/map/files-lib-3.md
- CHANGELOG.md
