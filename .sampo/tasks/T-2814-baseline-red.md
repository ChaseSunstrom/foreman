---
id: T-2814
type: FIX
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-11-03T16:24:26Z
updated: 2026-11-03T16:30:22Z
trigger: baseline
trigger_key: 8720a22cf18f5642
baseline: true
base: 9ecaf513b1aac7edaf580c857b39994e6f74e514
base_tree: 981c9f062662231c33d517e545e534114ba6efe3
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-03T16:25:31Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# Baseline red:…
## Raw request
> Baseline red: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py` fails test_rename_cli.RenameCli.test_the_usage_names_what_was_typed. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
1. Version-dependent usage (chosen): argparse before 3.14 builds a subparser's prog from the parent's custom usage string, so 'sampo louhi --help' says 'usage: sampo [-p PROJECT] <command> [options] exam' on 3.12; ship's scratch run used 3.12 and caught it.
2. A scratch-tree environment fault (missing file or env): ruled out; a clean worktree under 3.14 prints 'usage: sampo exam', and main under 3.12 reproduces the long form.
## Assumptions (confidence)
## Acceptance criteria
- [x] on Python 3.12 and 3.14 alike, a subcommand's usage line names only what was typed (usage: sampo exam / usage: fm exam), because the subparsers get prog explicitly — verify with `~/.local/bin/python3.12 plugin/tests/run.py test_rename_cli test_help test_cli`
## Non-goals
## Approach (options → choice → why)
1. Pass prog=prog to ap.add_subparsers (chosen). Likely outcome: one line; every subcommand's usage is 'PROG CMD' on every version. Fails if: a test pins the long form; none does.
2. Post-process the help text (strip the root usage). Likely outcome: more code, misses error messages. Fails if: argparse's error usage keeps the long form.
3) use what exists: argparse's own prog argument. 4) do less: pin the test to 3.14. Fails if: users on 3.12 see the wrong usage.
Choice: 1 (95%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: test_rename_cli under python3.12
2. [x] pass prog to add_subparsers; green on 3.12 and 3.14
## Resume here
## Docs impact
none: usage lines are the doc
## Verification evidence
- (step 1) `~/.local/bin/python3.12 plugin/tests/run.py test_rename_cli` → ✗ exit 1 · Ran 7 tests in 3.7s (1 classes, 16 at a time; slowest: RenameCli 3s) / FAILED (1 classes: test_rename_cli.RenameCli) [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:25:57Z)
- (step 2) `~/.local/bin/python3.12 plugin/tests/run.py test_rename_cli test_help test_cli` → exit 0 · Ran 159 tests in 21.8s (48 classes, 16 at a time; slowest: TaskLifecycle 20s, CaptureAndIntake 11s, StateViews 10s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:29:16Z)
- (ac 1) `~/.local/bin/python3.12 plugin/tests/run.py test_rename_cli test_help test_cli` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T16:29:16Z [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:29:48Z)
- (step 1) `~/.local/bin/python3.12 plugin/tests/run.py test_rename_cli` → exit 0 · Ran 7 tests in 1.4s (1 classes, 16 at a time; slowest: RenameCli 1s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:29:48Z)
- (audit intent) `self: read the diff; one argument, prog=prog, on the root's add_subparsers; checked usage lines on 3.12 and 3.14 by hand and via test_rename_cli, test_help, test_cli` → on every Python a subcommand's usage names only what was typed: 'usage: sampo exam' or 'usage: fm exam' [tree 398b4aa61509] (2026-11-03T16:29:48Z)
- (audit edge) `self: read the diff; one argument, prog=prog, on the root's add_subparsers; checked usage lines on 3.12 and 3.14 by hand and via test_rename_cli, test_help, test_cli` → nested subparsers (fm task, fm research) build their prog from their parent's prog, which is now 'PROG CMD', so they read 'fm task ac' too; the root's own help (START_HERE) is unchanged [tree 398b4aa61509] (2026-11-03T16:29:48Z)
- (audit adversary) `self: read the diff; one argument, prog=prog, on the root's add_subparsers; checked usage lines on 3.12 and 3.14 by hand and via test_rename_cli, test_help, test_cli` → help text only; no parsing changes, so no flag or command is accepted or refused differently [tree 398b4aa61509] (2026-11-03T16:29:48Z)
- (audit self) `self: read the diff; one argument, prog=prog, on the root's add_subparsers; checked usage lines on 3.12 and 3.14 by hand and via test_rename_cli, test_help, test_cli` → no findings [tree 398b4aa61509] (2026-11-03T16:29:48Z)
## Log
- 2026-11-03T16:24:26Z created
- 2026-11-03T16:25:29Z set tier=S
- 2026-11-03T16:25:30Z planned: it has criteria and steps
- 2026-11-03T16:25:31Z focused
- 2026-11-03T16:25:31Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-03T16:28:11Z paused: focus moved to T-2768
- 2026-11-03T16:28:51Z focused
- 2026-11-03T16:30:21Z done
- 2026-11-03T16:30:22Z committed feab53ac (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2429 [FIX M, done, 1 steps] Baseline red:… — lesson: A test that appends then shifts an mtime is shifting from the wall clock: read the mtime before the write
- T-2286 [FIX M, dropped, 0 steps] Baseline red:…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- similar past tasks were M: consider --tier M
- similar finished tasks took 1–3 steps
## Lessons
- Run the suite on the oldest supported Python before shipping: argparse's subparser prog changed in 3.14
## Plan gaps
- failed first: step 1 red: test_rename_cli under python3.12
## Files touched
- plugin/lib/sampo/cli.py
