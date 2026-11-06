---
id: T-2765
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py]
depends_on: []
source: self
created: 2026-11-03T04:14:02Z
updated: 2026-11-03T15:20:50Z
builder_model: sonnet
base: 3bed813e8832bf32bec1b6bd353ce1aa863e1f04
base_tree: e6af4367bb986dd86aac05f55c85cfa5bd35fb34
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-03T04:36:05Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py]
lane_stop: merged 2026-11-03T05:18:16Z
verified: strong
---
# A piped fm check (or sampo check) without pipefail is refused with how to run it instead, rather than a note read after the fact: the exit status of 'fm check | tail' is tail's, so a red gate reads green
## Raw request
> FIX: the gate-pipe note (fm check piped into tail/head) still repeats 3x after T-1889 (fmhooks.py:2381): make it a hard check, e.g. add set -o pipefail or deny once, instead of prose
## Interpretation
Reading 1 (chosen): the note at plugin/lib/sampo/hooks.py:2374 (T-1759, T-1889) is prose that the model still ignores; the friction digest counted it 3x this week. The standing intent says a lesson becomes a rule with a check. So refuse the call, the way the hook already refuses a chained fm ask (hooks.py:2677), and name the two fixes. Also match 'sampo check', the CLI's new name (T-2742). Reading 2 (ruled out): rewrite the command with updatedInput to prepend pipefail. Claude Code pairs updatedInput with a permission decision, and an 'allow' would skip the user's prompt outside bypass mode.
## Assumptions (confidence)
## Acceptance criteria
- [x] PreToolUse denies 'fm check … | tail' and 'sampo check | head' without pipefail, naming 'drop the pipe (its summary is short) or start with set -o pipefail;'; 'set -o pipefail; fm check | tail', 'fm check || true', 'fm checkpoint | x' and quoted text pass — verify with `python3 plugin/tests/run.py test_hooks`
- [x] the hook and guard suites stay green — verify with `python3 plugin/tests/run.py test_hooks test_guard`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the PreToolUse deny path hooks.py already has for fm ask (a ('deny', reason) return), fed by the existing _GATE_PIPE regex widened to sampo. Likely outcome: about 15 lines plus tests. Fails if: a legitimate 'fm check | tee log' gets refused; the message names pipefail, which keeps it.
2. Move the check into the guard. Fails if: the guard is protected core and needs the user's yes; this isn't a safety rule.
3. Do less: make the note louder. Fails if: it is already terse, and it is the third shaping (T-1759, T-1814, T-1889).
Choice 1 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests in test_hooks: the deny, the passes, the sampo spelling
2. [x] _GATE_PIPE takes (fm|sampo); the gate-pipe check returns a deny in PreToolUse in place of the note
## Resume here
## Docs impact
none: the deny text says what to do
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 576 tests in 182.5s (126 classes, 16 at a time; slowest: Stop 181s, PreToolUse 102s, NoTaskGate 99s) / OK [ran] [tree cc40af6152f0] [world 2f1906870a] (2026-11-03T04:45:18Z)
- `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 250 tests in 51.8s (31 classes, 16 at a time; slowest: Stop 50s, NoTaskGate 30s, PreToolUse 28s) / FAILED (6 classes: test_hooks.Stop, test_hooks.PreToolUse, test_hooks.SessionStart, test_hooks.De (start tree + this task's tests) [ran] [tree 928a23295594] [world 2f1906870a] (2026-11-03T15:18:36Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 250 tests in 69.9s (31 classes, 16 at a time; slowest: Stop 69s, NoTaskGate 49s, PreToolUse 43s) / OK [ran] [tree 928a23295594] [world 2f1906870a] (2026-11-03T15:18:36Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T15:18:36Z [ran] [tree 908dcba00dc9] [world 2f1906870a] (2026-11-03T15:19:49Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 577 tests in 71.9s (126 classes, 16 at a time; slowest: Stop 72s, NoTaskGate 48s, PreToolUse 43s) / OK [ran] [tree 908dcba00dc9] [world 2f1906870a] (2026-11-03T15:19:49Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 577 tests in 71.9s (126 classes, 16 at a time; slowest: Stop 72s, NoTaskGate 48s, PreToolUse 43s) / OK [ran] [tree 908dcba00dc9] [world 2f1906870a] (2026-11-03T15:19:49Z)
- (audit intent) `self: read the merged diff; the gate-pipe note is a deny with the fix named; probed plain grep | head pipes (not refused)` → fm check or sampo check piped into tail/head without pipefail is refused, naming the fix [tree 908dcba00dc9] (2026-11-03T15:19:49Z)
- (audit edge) `self: read the merged diff; the gate-pipe note is a deny with the fix named; probed plain grep | head pipes (not refused)` → set -o pipefail; fm check | tail, fm check || true and fm checkpoint pass; plain grep | head passes; the match covers fm and sampo [tree 908dcba00dc9] (2026-11-03T15:19:49Z)
- (audit adversary) `self: read the merged diff; the gate-pipe note is a deny with the fix named; probed plain grep | head pipes (not refused)` → the deny only narrows what runs; a disguised pipe that slips past falls back to the old unrefused run, never a broader allow [tree 908dcba00dc9] (2026-11-03T15:19:49Z)
- (audit self) `self: read the merged diff; the gate-pipe note is a deny with the fix named; probed plain grep | head pipes (not refused)` → no findings [tree 908dcba00dc9] (2026-11-03T15:19:49Z)
## Log
- 2026-11-03T04:14:02Z created
- 2026-11-03T04:20:12Z planned from capture
- 2026-11-03T04:20:14Z set approved=True
- 2026-11-03T04:35:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2765.builder.md
- 2026-11-03T04:36:02Z focused
- 2026-11-03T04:36:05Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-03T05:03:53Z criterion 2 text: the hook suites stay green → the hook and guard suites stay green — verify with `python3 plugin/tests/run.py test_hooks test_guard`
- 2026-11-03T05:03:54Z steer: criterion 2 named test_hooks_more, which doesn't exist (run.py: no test matches); the verify now runs test_hooks and test_guard, 576 tests OK in the lane after merging foreman/build
- 2026-11-03T05:09:05Z criterion 2 verify: `python3 plugin/tests/run.py test_hooks test_guard` — verify with `python3 plugin/tests/run.py test_hooks test_hooks_more test_guard` → `python3 plugin/tests/run.py test_hooks test_guard`
- 2026-11-03T05:18:16Z merged worktree-agent-a865ed3abf9b02fad (2 file(s))
- 2026-11-03T05:20:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a865ed3abf9b02fad
- 2026-11-03T05:48:31Z focused
- 2026-11-03T05:48:35Z scope: files outside the scope since focus came from other lanes' merge commits, not this task's edits
- 2026-11-03T05:48:37Z paused: focus moved to T-2766
- 2026-11-03T14:57:34Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T14:57:34Z focused
- 2026-11-03T14:57:37Z paused: focus moved to T-2766
- 2026-11-03T15:16:33Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T15:16:33Z focused
- 2026-11-03T15:20:50Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, active, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate s…
- T-2563 [FEATURE M, done, 3 steps] Anergy for permission prompts: time each prompt to its PostToolUse and report reflex-approved command classes (spike) — lesson: A spike…
- T-2748 [CLEAN M, planned, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.p…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py; re-ground the plan against them before editing
## Lessons
- A note that is ignored every time should become a deny with its fix
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
