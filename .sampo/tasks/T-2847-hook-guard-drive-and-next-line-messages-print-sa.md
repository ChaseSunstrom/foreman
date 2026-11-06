---
id: T-2847
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T22:01:48Z
updated: 2026-11-04T01:43:43Z
base_note: Calibration: this plan states Choice 70% where FEATURE M closes (594) held on the first finish 98% of the time: 28 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-03T23:00:12Z
rival_split: true
inferred_deps: [T-2742]
inferred_why: T-2742: sampo spellings need the rename first
builder_model: haiku
base: 3e621c938fcb4912768844484f16aae0d08268e1
base_tree: 7668d90bd4352efeabe10800118dcaf2565d6ccb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T00:09:28Z
plan0_scope: []
lane_stop: merged 2026-11-04T01:31:06Z
verified: strong
unproven: [meaning]
---
# Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask…
## Raw request
> FEATURE: hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask …) instead of fm, with the tests that pin those strings updated; split from T-2845, after its parsers accept both
## Interpretation
Reading 1 (chosen): what Sampo says to the model and the user teaches the new name. The Next: line, the drive's Stop reasons, guard refusals, hook notes (SessionStart, PreToolUse, PostToolUse, UserPromptSubmit) and the CLI's own errors and hints print 'sampo <verb>', not 'fm <verb>'. Everything that reads commands keeps accepting both (T-2845). Matchers, regexes, argv comparisons and stored keys stay as they are. Argparse usage still echoes the typed name (T-2766). Text Sampo only passes through (fm quiet output, diffs, brief bodies, the user's quoted words) is never rewritten. Reading 2 (ruled out): rename every fm literal in the code, matchers included. That breaks every old command a user or a stored brief has, against the rule that every old name keeps working.
## Assumptions (confidence)
## Acceptance criteria
- [x] hook notes, drive reasons, guard refusals, the Next: line and CLI hints print sampo spellings; matchers still accept fm; the suite passes — verify with `python3 plugin/tests/run.py test_hooks test_guard test_rename_scan test_claims test_unattended test_sampo_spelling`
## Non-goals
## Approach (options → choice → why)
1. Boundary translation: rewrite 'fm <verb>' to 'sampo <verb>' where hooks print their JSON and in a stdout wrapper for the CLI. Likely outcome: a 30-line diff. Fails if it rewrites passed-through text: fm quiet -- git diff would show altered code, brief bodies would misquote the user, and --json consumers would see changed values.
2. Use what exists, at the source: edit the message literals in fmguard.py, hooks.py, core.py's next-action text and cli.py's errors and hints, judging each one: a message changes, a matcher (re.compile, startswith, in-tuple, argv lists, CHECK_FM) is left alone. One output test drives representative hooks and fm next and asserts no 'fm <verb>' in what they print. Likely outcome: a large but honest diff, with the pinned tests updated. Fails if a matcher literal is changed by mistake; T-2845's both-spellings tests and the guard corpus catch that.
3. Do less: the Next: line and the drive's reasons only. Likely outcome: small. Fails if the guard and hook notes still teach fm, the strings the model reads most.
Choice 2 (70%): it is the only option that changes what is said without altering what is passed through.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: an output test drives SessionStart, a guard refusal, a drive Stop and fm next, asserting no 'fm <verb>' in their text
2. [x] edit message literals in fmguard.py, hooks.py, core.py, cli.py; leave every matcher
3. [x] update the tests that pin the old strings; full check
## Resume here
<!-- auto -->
- 2026-11-04T00:55:59Z steps 3/3 done
- git: worktree-agent-a24d85b6d54c78696; 64 uncommitted: plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/dataproof.py, plugin/lib/sampo/eco.py, plugin/lib/sampo/graph.py, plugin/lib/sampo/home.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/mandate.py, plugin/lib/sampo/new.py, plugin/lib/sampo/prove.py
- touched since last checkpoint: plugin/tests/test_guard.py, plugin/tests/test_hooks.py, plugin/tests/test_core.py, plugin/lib/sampo/graph.py, plugin/lib/sampo/louhi.py, plugin/tests/test_graph.py, .fm-scratch/byline2.py, plugin/lib/sampo/dataproof.py, plugin/lib/sampo/eco.py, plugin/lib/sampo/home.py, plugin/lib/sampo/mandate.py, plugin/lib/sampo/new.py, plugin/lib/sampo/prove.py, plugin/lib/sampo/recall.py, plugin/lib/sampo/release.py
- failures met: assertionerror: 'fm ask t-0 confirm' not found in "acceptance criterion step the user's y…; fail rules symlink foreman.md → foreman.md
## Docs impact
none: message text only; the docs already teach sampo (T-2778)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_sampo_spelling` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: Spelling 1s) / OK [ran] [tree 1f26f027659a] [world 2f1906870a] (2026-11-04T00:27:12Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_guard test_rename_scan test_claims test_unattended test_sampo_spelling` → exit 0 · Ran 621 tests in 53.4s (133 classes, 16 at a time; slowest: Stop 53s, NoTaskGate 34s, PreToolUse 28s) / OK [ran] [tree 1f26f027659a] [world 2f1906870a] (2026-11-04T00:28:06Z)
- (step 3) `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_approve_reads test_cli test_cli_ergonomics test_compact test_core test_genesis test_guard test_guard_diff test_guard_exec_vectors test_guard_git test_guard_pipes test_guard_sampo test_hooks test_rename_scan test_sampo_spelling test_settings_scopes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.44s] [ran] [tree 1f26f027659a] [world 2f1906870a] (2026-11-04T00:29:20Z)
- `sampo check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: fm doctor → ✗ exit 1 · FAIL  rules symlink        ~/.claude/rules/foreman.md → ~/.claude/foreman/plugin/rules/foreman.md / fm doctor: FAILED (56 pass, 10 warn, 2 fail); python3 plugin/tests/run.py → ✗ exit 1 · Ran 6013 tests in 404.5s (1284 classes, 16 at a time; slowest: Worker 143s, LeanKind 122s, Stop 114s) / FAILED (53 classes: test_lanes.Lanes, test_proof.Proof, test_execution.BoardClose, test_lanes.De [ran] [tree 856b18630be7] [world 2f1906870a] (2026-11-04T00:41:29Z)
- `sampo check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: fm doctor → ✗ exit 1 · FAIL  rules symlink        ~/.claude/rules/foreman.md → ~/.claude/foreman/plugin/rules/foreman.md / fm doctor: FAILED (57 pass, 9 warn, 2 fail) [ran] [tree 22b173c2cdb9] [world 2f1906870a] (2026-11-04T01:22:24Z)
- `python3 plugin/tests/run.py test_sampo_spelling test_graph` → ✗ exit 1 · Ran 23 tests in 5.6s (8 classes, 16 at a time; slowest: BlastReach 4s, BlastInPlan 4s, BlastBuild 2s) / FAILED (3 classes: test_graph.BlastReach, test_graph.BlastInPlan, test_sampo_spelling.Spelling) (start tree + this task's tests) [ran] [tree 5a91b55a21d6] [world 2f1906870a] (2026-11-04T01:31:53Z)
- `python3 plugin/tests/run.py test_sampo_spelling test_graph` → exit 0 · Ran 23 tests in 4.7s (8 classes, 16 at a time; slowest: BlastReach 4s, BlastInPlan 4s, BlastBuild 2s) / OK [ran] [tree 5a91b55a21d6] [world 2f1906870a] (2026-11-04T01:31:53Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_guard test_rename_scan test_claims test_unattended test_sampo_spelling` → exit 0 · Ran 621 tests in 51.9s (133 classes, 16 at a time; slowest: Stop 52s, NoTaskGate 32s, PreToolUse 26s) / OK [ran] [tree 5a91b55a21d6] [world 2f1906870a] (2026-11-04T01:32:52Z)
- (audit edge) `builder self-review, then my review: a mechanical scan of all 636 respelled fragments for surviving fm twins found 2 real producer/reader splits (the blast-radius line, louhi's posture anchor) plus 14 leftover messages; all fixed and tested; the self-change gate held the +9 always-on chars until a 12-char cut paid for them; guard rule ids kept stable across the respelling; full suite 6013 OK in the lane` → briefs and ledgers holding the old fm forms still read (blast radius, AFFECTED_LABEL); old rule ids unchanged [tree 5a91b55a21d6] (2026-11-04T01:32:52Z)
- (audit adversary) `builder self-review, then my review: a mechanical scan of all 636 respelled fragments for surviving fm twins found 2 real producer/reader splits (the blast-radius line, louhi's posture anchor) plus 14 leftover messages; all fixed and tested; the self-change gate held the +9 always-on chars until a 12-char cut paid for them; guard rule ids kept stable across the respelling; full suite 6013 OK in the lane` → matchers untouched (T-2845's both-spellings tests and guard replay: 124 labelled, 0 drifted) [tree 5a91b55a21d6] (2026-11-04T01:32:52Z)
- (audit intent) `builder self-review, then my review: a mechanical scan of all 636 respelled fragments for surviving fm twins found 2 real producer/reader splits (the blast-radius line, louhi's posture anchor) plus 14 leftover messages; all fixed and tested; the self-change gate held the +9 always-on chars until a 12-char cut paid for them; guard rule ids kept stable across the respelling; full suite 6013 OK in the lane` → printed hints say sampo; passed-through text (quiet output, diffs, briefs, the user's words) untouched [tree 5a91b55a21d6] (2026-11-04T01:32:52Z)
- `python3 plugin/tests/run.py test_hooks test_guard test_rename_scan test_claims test_unattended test_sampo_spelling` → exit 0 · Ran 622 tests in 60.5s (133 classes, 16 at a time; slowest: Stop 60s, NoTaskGate 38s, PreToolUse 31s) / OK [ran] [tree 971d90a71e9b] [world 2f1906870a] (2026-11-04T01:40:40Z)
- (audit edge) `builder self-review, then my review: a mechanical scan of all 636 respelled fragments for surviving fm twins found 2 real producer/reader splits (the blast-radius line, louhi's posture anchor) plus 14 leftover messages; all fixed and tested; the self-change gate held the +9 always-on chars until a 12-char cut paid for them; guard rule ids kept stable across the respelling; full suite 6013 OK in the lane` → briefs and ledgers holding the old fm forms still read (blast radius, AFFECTED_LABEL); old rule ids unchanged [tree 971d90a71e9b] (2026-11-04T01:40:40Z)
- (audit adversary) `builder self-review, then my review: a mechanical scan of all 636 respelled fragments for surviving fm twins found 2 real producer/reader splits (the blast-radius line, louhi's posture anchor) plus 14 leftover messages; all fixed and tested; the self-change gate held the +9 always-on chars until a 12-char cut paid for them; guard rule ids kept stable across the respelling; full suite 6013 OK in the lane` → matchers untouched (T-2845's both-spellings tests and guard replay: 124 labelled, 0 drifted); the later T-2859 guard edit is message-only [tree 971d90a71e9b] (2026-11-04T01:40:40Z)
- (audit intent) `builder self-review, then my review: a mechanical scan of all 636 respelled fragments for surviving fm twins found 2 real producer/reader splits (the blast-radius line, louhi's posture anchor) plus 14 leftover messages; all fixed and tested; the self-change gate held the +9 always-on chars until a 12-char cut paid for them; guard rule ids kept stable across the respelling; full suite 6013 OK in the lane` → printed hints say sampo; passed-through text (quiet output, diffs, briefs, the user's words) untouched [tree 971d90a71e9b] (2026-11-04T01:40:40Z)
- (audit intent) `re-read against the current tree after T-2859's message-only guard edit` → holds: printed hints say sampo; passed-through text untouched; T-2859 changed only one message branch [tree 971d90a71e9b] (2026-11-04T01:43:43Z)
- (audit adversary) `guard replay and both-spellings tests on the current tree` → holds: matchers untouched; T-2859's branch is message text, check() unchanged; 608 guard/hook/safety tests OK [tree 971d90a71e9b] (2026-11-04T01:43:43Z)
- (audit edge) `stored fm forms in briefs and ledgers` → holds: blast radius and AFFECTED_LABEL read both spellings; rule ids stable [tree 971d90a71e9b] (2026-11-04T01:43:43Z)
## Log
- 2026-11-03T22:01:48Z created
- 2026-11-03T22:59:53Z set tier=M
- 2026-11-03T22:59:55Z planned: it has criteria and steps
- 2026-11-03T22:59:59Z criterion 1 verify: `python3 plugin/tests/run.py test_hooks test_guard test_rename_scan test_claims test_unattended test_next` → `python3 plugin/tests/run.py test_hooks test_guard test_rename_scan test_claims test_unattended test_sampo_spelling`
- 2026-11-04T00:01:02Z user approved core in Claude Code's permission prompt
- 2026-11-04T00:09:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2847.builder.md
- 2026-11-04T00:09:28Z focused
- 2026-11-04T00:09:28Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T01:31:06Z merged worktree-agent-a24d85b6d54c78696 (74 file(s))
- 2026-11-04T01:31:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a24d85b6d54c78696
- 2026-11-04T01:31:20Z focused
- 2026-11-04T01:33:50Z paused: focus moved to T-2859
- 2026-11-04T01:39:38Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T01:39:38Z focused
- 2026-11-04T01:43:28Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: user-facing strings emitted by hooks (`plugin/lib/fmhooks.py`), guard (`plugin/lib/fmguard.py`), drive, and the "Next:" line rendering switch from `fm <cmd>` spellings to `sampo <cmd>` (e.g. `sampo focus`, `sampo ask`). The pinning tests in `plugin/tests/` are updated to match. Parsers a…
- The reverse reading: the request text says "print sampo spellings instead of fm", but could be read as a rename of the command shown in messages only where the message is a suggested command, leaving prose mentions of "fm" (product name, `fm doctor` docs) untouched.
- A wider reading: also change the mirrored `plugin/lib/sampo/*.py` modules and the `plugin/bin/sampo` entry point so the new spelling is the canonical one, not just in the four message surfaces (hook, guard, drive, Next-line).
- Narrow reading: only the Next-line helper (probably in `plugin/lib/fmcli.py` or `fmcore.py`) changes, and hook/guard/drive messages are fed by it, so one edit covers all four.
Approaches:
- Centralize: find the single place that formats the command hint (Next-line builder, likely `fmcore.py`/`fmcli.py`) and add a `cmd_name()` helper returning `sampo`; route hook/guard/drive message strings through it, then update tests that assert on literal `fm focus`/`fm ask` strings.
- Grep-and-replace per surface: enumerate string literals containing `fm <verb>` in `fmhooks.py`, `fmguard.py`, the drive module and Next-line code, change them to `sampo <verb>` only where the verb is a real subcommand, then fix failing assertions in `plugin/tests/test_*.py` guided by `python3 plugi…
- Golden-first: run `python3 plugin/tests/run.py` and `plugin/tests/bench_hooks.py` to capture current output, change the strings, and diff outputs so only the intended message lines move; check `fm replay` fixtures for recorded output.
- Edit the `sampo/` mirror modules and have the `fm*` modules re-export, if the repo is mid-migration toward `plugin/lib/sampo/` as canonical, avoiding editing both copies.
Failure modes:
- Duplicate implementations (`plugin/lib/fmhooks.py` vs `plugin/lib/sampo/*.py`): editing one copy leaves the other printing `fm`, so tests pass under one entry point (`plugin/bin/fm`) and fail under the other (`plugin/bin/sampo`).
- Blind replace hits non-command text: `fm doctor` in docs, `fm` as a product name, file paths like `fmcore`, or strings that tests/parsers match on (e.g. hook output parsed by agents or `skills/` prompts), breaking consumers that still expect `fm`.
- Missed pins: strings recorded in `fm replay` fixtures, `plugin/tests/e2e/roundtrip.py`, `plugin/evals/`, or `mods/foreman-ui` tests and `skills/` markdown that quote the old hint, so the full gate list fails even though `plugin/tests/run.py` passes.
- Ordering dependency: if T-2845's both-spellings parser isn't actually in HEAD for every verb printed (e.g. `drive` or `guard` subcommands), the new hints suggest `sampo <verb>` commands that don't run.
## Dissent
- [x] rival reading: Likeliest: user-facing strings emitted by hooks (`plugin/lib/fmhooks.py`), guard (`plugin/lib/fmguard.py`), drive, and the "Next:" line rendering switch from `fm <cmd>` spellings to `sampo <cmd>` (e.g. `sampo focus`, `sampo ask`). The pinning tests in `plugin/tests/` are updated to match. Parsers a… — answered: adopted: that is the plan's reading; the modules are plugin/lib/sampo/hooks.py, core.py, cli.py and plugin/lib/fmguard.py (there is no fmhooks.py)
- [x] rival reading: The reverse reading: the request text says "print sampo spellings instead of fm", but could be read as a rename of the command shown in messages only where the message is a suggested command, leaving prose mentions of "fm" (product name, `fm doctor` docs) untouched. — answered: adopted in part: suggested commands change; prose naming the product already says Sampo; a bare 'fm' with no verb (`fm` still works) stays
- [x] rival reading: A wider reading: also change the mirrored `plugin/lib/sampo/*.py` modules and the `plugin/bin/sampo` entry point so the new spelling is the canonical one, not just in the four message surfaces (hook, guard, drive, Next-line). — answered: rejected: plugin/bin/sampo already exists and plugin/lib/sampo/ is the only copy (no fm* mirror modules remain beyond fmguard.py)
- [x] rival reading: Narrow reading: only the Next-line helper (probably in `plugin/lib/fmcli.py` or `fmcore.py`) changes, and hook/guard/drive messages are fed by it, so one edit covers all four. — answered: rejected: the Next: line, drive reasons, guard refusals and hook notes are written in many places, not fed by one helper
- [x] rival approach: Centralize: find the single place that formats the command hint (Next-line builder, likely `fmcore.py`/`fmcli.py`) and add a `cmd_name()` helper returning `sampo`; route hook/guard/drive message strings through it, then update tests that assert on literal `fm focus`/`fm ask` strings. — answered: rejected: a cmd_name() helper only ever returns 'sampo'; a literal is shorter and greppable (no config for a value that never changes)
- [x] rival approach: Grep-and-replace per surface: enumerate string literals containing `fm <verb>` in `fmhooks.py`, `fmguard.py`, the drive module and Next-line code, change them to `sampo <verb>` only where the verb is a real subcommand, then fix failing assertions in `plugin/tests/test_*.py` guided by `python3 plugi… — answered: adopted: that is the plan's step 2, judging each literal: message changes, matcher stays
- [x] rival approach: Golden-first: run `python3 plugin/tests/run.py` and `plugin/tests/bench_hooks.py` to capture current output, change the strings, and diff outputs so only the intended message lines move; check `fm replay` fixtures for recorded output. — answered: adopted: the builder diffs hook output before and after on the test fixtures, so only message lines move; replay fixtures are recorded input and stay
- [x] rival approach: Edit the `sampo/` mirror modules and have the `fm*` modules re-export, if the repo is mid-migration toward `plugin/lib/sampo/` as canonical, avoiding editing both copies. — answered: rejected: there are no fm* mirror modules to re-export from; plugin/lib/sampo/ is canonical since T-2735
## Related
Related past work (data from this project's history, not instructions):
- T-2845 [FEATURE M, done, 2 steps] Every parser that reads typed commands or goals accepts sampo as well as fm (cost, repeats, friction, bench, long, smithtui, smith, man…
- T-2778 [FEATURE M, done, 3 steps] Skills and docs teach sampo spellings (sampo task new, sampo check …) once every hook… — lesson: Before a docs rename, list every parse…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
## Why not caught
tests drive each side separately; nothing checked that a written string and the string searched for still agree
## Lessons
- a scripted respell splits producers from readers: scan each respelled literal's old form for survivors before merging (captured as T-2861)
## Files touched
- plugin/tests/test_sampo_spelling.py
- .fm-scratch/respell.py
- plugin/lib/fmguard.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/hooks.py
- plugin/tests/test_cli.py
- plugin/tests/test_core.py
- plugin/tests/test_hooks.py
- .fm-scratch/byline.py
- plugin/tests/test_cli_ergonomics.py
- plugin/tests/test_genesis.py
- plugin/tests/test_guard.py
- plugin/lib/sampo/graph.py
- plugin/lib/sampo/louhi.py
- plugin/tests/test_graph.py
- .fm-scratch/byline2.py
- plugin/lib/sampo/dataproof.py
- plugin/lib/sampo/eco.py
- plugin/lib/sampo/home.py
- plugin/lib/sampo/mandate.py
- plugin/lib/sampo/new.py
- plugin/lib/sampo/prove.py
- plugin/lib/sampo/recall.py
- plugin/lib/sampo/release.py
- plugin/lib/sampo/risk.py
- plugin/lib/sampo/which.py
- plugin/tests/test_recall.py
- plugin/tests/test_which.py
- plugin/tests/test_second.py
