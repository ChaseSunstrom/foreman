---
id: T-2845
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T21:35:42Z
updated: 2026-11-03T22:15:54Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (592) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-03T22:02:11Z
rival_split: true
builder_model: haiku
base: c76ac61da6ffdc365d36ccd78bd3f3ac4cca4c73
base_tree: bcc1534a45115a7af8af0ca31030b4cdb04f0124
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-03T22:03:58Z
plan0_scope: []
lane_stop: merged 2026-11-03T22:14:17Z
verified: strong
unproven: [meaning, tui-unshot]
---
# Every parser that reads typed commands or goals accepts sampo as well as fm (cost, repeats, friction, bench, long, smithtui, smith, mandate, rune, fixes, cli, BOOKKEEPING), and test_rename_scan's fm-only regex scan covers every sampo module, testing each pattern against both spellings
## Raw request
> FEATURE: the parsers that read the user's own commands and goals count only fm spellings, so sampo runs go uncounted: cost.py ~101 and ~1433, BOOKKEEPING, fixes.py _WRITES, mandate.py ~431, rune.py ~785/~791, cli.py ~4402; and hook, guard and Next-line messages still print fm spellings (follow-up of T-2778)
## Interpretation
Reading 1: T-2778 taught sampo spellings, so users and sessions now type sampo …; every parser that classifies a typed command or goal by matching 'fm' miscounts them (cost analytics, repeats, friction's fm edit detection, bench, long, smithtui, smith's resume hint, mandate, rune's goal parsing, fixes' _WRITES, cli ~4402, BOOKKEEPING). Fix each to accept both, and make the rename scan find any that slip (it scanned only three files and skipped any string containing 'sampo'). Reading 2: switch the printed messages too; split to T-2847 because it rewrites hundreds of pinned strings.
## Assumptions (confidence)
## Acceptance criteria
- [x] the fm-only scan covers plugin/lib/sampo/*.py and checks each command-matching regex against an fm and a sampo spelling; it finds none; each fixed consumer counts a sampo-spelled command as it counts the fm one — verify with `python3 plugin/tests/run.py test_rename_scan test_cost test_friction test_repeats`
## Non-goals
## Approach (options → choice → why)
1) A scan over plugin/lib/sampo/*.py extracts regex literals and startswith/== comparisons naming fm as a command word, compiles each, and asserts it matches a sampo spelling wherever it matches the fm one; then fix every hit with fmguard.FM_NAME_RE or a ('fm', 'sampo') tuple. Likely outcome: the list of hits is the fix list, and the scan keeps it closed. Fails if: the extraction misses non-literal patterns (built strings); the reviewer's list covers those by hand.
2) Fix the reviewer's list only, no scan. Likely outcome: today's sites fixed. Fails if: the next fm-only parser goes unnoticed, as these did.
3) Normalize at entry: rewrite a leading 'sampo' to 'fm' wherever commands are read. Likely outcome: one change per reader. Fails if: readers take commands from many sources (ledger, transcripts, goals) with no shared entry.
4) Use what exists: fmguard.FM_NAME_RE ('(?:fm|sampo)') and test_rename_scan's current fm_only_regexes as the scan's base. Likely outcome: no new pattern helper. Fails if: a module can't import fmguard (hook import budget); then a core constant.
5) Do less: only cost.py, the biggest miscount. Likely outcome: analytics right. Fails if: repeats, friction and mandate stay blind to sampo.

Choice 1 with 4 (75%): the scan turns the reviewer's spot list into a closed check.
## Risks and rollback
## Execution prompt
## Steps
1. [x] scan: every command-matching regex in plugin/lib/sampo/*.py matches sampo where it matches fm (red on today's sites)
2. [x] fix each hit with FM_NAME_RE or a tuple; per-consumer tests for cost, repeats, friction
## Resume here
## Docs impact
none: parsers and tests
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_rename_scan test_cost test_friction test_repeats 2>&1 | tail -30` → exit 0 · Ran 71 tests in 21.9s (16 classes, 16 at a time; slowest: Repeats 22s, Friction 10s, TaskCostCap 10s) / OK [ran] [tree b5f48af57171] [world 2f1906870a] (2026-11-03T22:07:16Z)
- (step 1) `python3 plugin/tests/run.py test_rename_scan test_cost test_friction test_repeats 2>&1 | tail -30` → exit 0 · Ran 71 tests in 21.9s (16 classes, 16 at a time; slowest: Repeats 22s, Friction 10s, TaskCostCap 10s) / OK [ran] [tree b5f48af57171] [world 2f1906870a] (2026-11-03T22:07:16Z)
- (step 1) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 10 tests in 6.1s (1 classes, 16 at a time; slowest: RenameScan 6s) / OK [ran] [tree 6fe1a33514ef] [world 2f1906870a] (2026-11-03T22:07:29Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan test_cost test_friction test_repeats` → exit 0 · Ran 71 tests in 34.1s (16 classes, 16 at a time; slowest: Repeats 34s, Friction 15s, TaskCostCap 15s) / OK [ran] [tree 6fe1a33514ef] [world 2f1906870a] (2026-11-03T22:08:04Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_bench test_cli test_core test_cost test_fixes test_friction test_long test_mandate test_rename_scan test_repeats && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.16s] [ran] [tree 6fe1a33514ef] [world 2f1906870a] (2026-11-03T22:09:52Z)
- `python3 plugin/tests/run.py test_rename_scan` → ✗ exit 1 · Ran 10 tests in 4.0s (1 classes, 16 at a time; slowest: RenameScan 3s) / FAILED (1 classes: test_rename_scan.RenameScan) (start tree + this task's tests) [ran] [tree a153b1588207] [world 2f1906870a] (2026-11-03T22:14:34Z)
- `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 10 tests in 3.0s (1 classes, 16 at a time; slowest: RenameScan 3s) / OK [ran] [tree a153b1588207] [world 2f1906870a] (2026-11-03T22:14:34Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_scan test_cost test_friction test_repeats` → exit 0 · Ran 71 tests in 18.8s (16 classes, 16 at a time; slowest: Repeats 18s, Friction 7s, TaskCostCap 7s) / OK [ran] [tree a153b1588207] [world 2f1906870a] (2026-11-03T22:14:54Z)
- (audit intent) `self: read the cost.py hunks (verb regex, _program, Next-followed now keyed by the words after either spelling, usage, BOOKKEEPING) and the scan: it compiles every regex literal in plugin/lib/sampo/*.py and fmguard.py and flags one that matches an fm command but not the sampo spelling; 33 sites before, none after; allowlist keyed by file and text` → a session typing sampo commands is counted by cost, repeats, friction, bench, long, mandate, rune, fixes, cli, smithtui and louhi as an fm one was [tree a153b1588207] (2026-11-03T22:14:54Z)
- (audit edge) `self: read the cost.py hunks (verb regex, _program, Next-followed now keyed by the words after either spelling, usage, BOOKKEEPING) and the scan: it compiles every regex literal in plugin/lib/sampo/*.py and fmguard.py and flags one that matches an fm command but not the sampo spelling; 33 sites before, none after; allowlist keyed by file and text` → patterns built by concatenation slip the scan (noted); Next-followed labels drop the program word, so either spelling follows either [tree a153b1588207] (2026-11-03T22:14:54Z)
- (audit adversary) `self: read the cost.py hunks (verb regex, _program, Next-followed now keyed by the words after either spelling, usage, BOOKKEEPING) and the scan: it compiles every regex literal in plugin/lib/sampo/*.py and fmguard.py and flags one that matches an fm command but not the sampo spelling; 33 sites before, none after; allowlist keyed by file and text` → parsers only; fmguard's refusal regexes were already both-spelled and stay so [tree a153b1588207] (2026-11-03T22:14:54Z)
## Log
- 2026-11-03T21:35:42Z created
- 2026-11-03T21:38:47Z scope from T-2778's review: widen test_rename_scan's fm_only scan to plugin/lib/sampo/*.py and test each regex against both spellings; fix cost.py 101/261/1433/1445/1454/1504/1570, repeats.py 50, friction.py 78, bench.py 885, long.py 546/565, smithtui.py 2660/2766, smith.py's 'fm code --resume' text
- 2026-11-03T22:01:48Z set title=Every parser that reads typed commands or goals accepts sampo as well as fm (cost, repeats, friction, bench, long, smithtui, smith, mandate, rune, fixes, cli, BOOKKEEPING), and test_rename_scan's fm-only regex scan covers every sampo module, testing each pattern against both spellings
- 2026-11-03T22:02:00Z planned: it has criteria and steps
- 2026-11-03T22:03:48Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2845.builder.md
- 2026-11-03T22:03:57Z focused
- 2026-11-03T22:03:58Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-03T22:14:17Z merged worktree-agent-a6b20bbbec235f8ff (15 file(s))
- 2026-11-03T22:14:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6b20bbbec235f8ff
- 2026-11-03T22:14:26Z focused
- 2026-11-03T22:15:54Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a command-spelling alias gap. The parsers that classify the user's own shell commands and goals (`cost.py` ~101/~1433, `BOOKKEEPING`, `fixes.py` `_WRITES`, `mandate.py` ~431, `rune.py` ~785/~791, `cli.py` ~4402) match only `fm ...` and must also match `sampo ...` (and likely `plugin/bin/…
- Narrower: only the parsers get fixed (counting), and the message spelling is left as a separate follow-up, since the title lists it parenthetically.
- Broader: introduce one shared "program names" definition (for example a regex or tuple in `fmcore.py` or `plugin/lib/sampo/`) that every parser and message imports, replacing per-file literals.
- Alternative: `sampo` is the new canonical name and `fm` the legacy alias, so messages should always print `sampo` regardless of how it was invoked.
Approaches:
- Shared helper: define one `CLI_NAMES = ("fm", "sampo")` plus a compiled pattern in a common module, replace each literal in the listed sites with it, and add a `display_name()` for messages. This gives one place to change, but touches `plugin/lib/fmcore.py`, which is hot and widely imported.
- Per-site patch: edit each listed regex or string to `(?:fm|sampo)` in place. This is the smallest diff, but it leaves duplicated literals that drift again, and there is no guard to catch missed sites.
- Invocation-aware messages: derive the printed name from `argv[0]` or an env var set by `plugin/bin/sampo` and `plugin/bin/fm`, falling back to a default. Messages then match what the user typed, but the hook and guard run as subprocesses of the harness, so `argv[0]` may not reflect the user's spell…
- Grep-driven sweep: grep the whole `plugin/lib` tree for `\bfm\b` command patterns beyond the listed sites to catch ones the ticket missed. Pair it with the shared helper to avoid regressions.
Failure modes:
- Regex boundaries: `sampo` appears as a path (`plugin/lib/sampo/cli.py`, `plugin/bin/sampo`), a package name and a command. A loose pattern in `cost.py` or `BOOKKEEPING` would count file reads or imports as commands, inflating costs. An anchored command-position match is needed.
- Fixtures and snapshots: tests under `plugin/tests/` (and `fm replay`, `roundtrip.py`) likely assert the exact `fm ...` text in hook, guard and Next-line output. Changing messages breaks them, and the old output may be baked into replay data.
- Write detection: `fixes.py` `_WRITES` decides which commands mutate state. If `sampo` is added to counting but the subcommand tables differ (renamed or aliased subcommands), sampo writes could be miscounted as reads, or the reverse.
- Missed sites: the ticket's line numbers (`cost.py` ~101, ~1433, `cli.py` ~4402) are approximate and stale against HEAD 998fdc5a. Editing by line number rather than by symbol will hit the wrong code, and unlisted twins in `fmhooks.py` or `fmguard.py` stay uncovered.
## Dissent
- [x] rival reading: Likeliest: a command-spelling alias gap. The parsers that classify the user's own shell commands and goals (`cost.py` ~101/~1433, `BOOKKEEPING`, `fixes.py` `_WRITES`, `mandate.py` ~431, `rune.py` ~785/~791, `cli.py` ~4402) match only `fm ...` and must also match `sampo ...` (and likely `plugin/bin/… — answered: adopted: the parsers are this task
- [x] rival reading: Narrower: only the parsers get fixed (counting), and the message spelling is left as a separate follow-up, since the title lists it parenthetically. — answered: adopted: messages split to T-2847
- [x] rival reading: Broader: introduce one shared "program names" definition (for example a regex or tuple in `fmcore.py` or `plugin/lib/sampo/`) that every parser and message imports, replacing per-file literals. — answered: adopted for parsers: reuse fmguard.FM_NAME_RE, or a core constant if the hook import budget forbids fmguard
- [x] rival reading: Alternative: `sampo` is the new canonical name and `fm` the legacy alias, so messages should always print `sampo` regardless of how it was invoked. — answered: deferred: printed spellings are T-2847
- [x] rival approach: Shared helper: define one `CLI_NAMES = ("fm", "sampo")` plus a compiled pattern in a common module, replace each literal in the listed sites with it, and add a `display_name()` for messages. This gives one place to change, but touches `plugin/lib/fmcore.py`, which is hot and widely imported. — answered: adopted in part: one shared names constant; display_name belongs to T-2847
- [x] rival approach: Per-site patch: edit each listed regex or string to `(?:fm|sampo)` in place. This is the smallest diff, but it leaves duplicated literals that drift again, and there is no guard to catch missed sites. — answered: rejected: per-site literals drift; the scan plus one constant closes it
- [x] rival approach: Invocation-aware messages: derive the printed name from `argv[0]` or an env var set by `plugin/bin/sampo` and `plugin/bin/fm`, falling back to a default. Messages then match what the user typed, but the hook and guard run as subprocesses of the harness, so `argv[0]` may not reflect the user's spell… — answered: deferred to T-2847 (messages); cli already names what was typed in usage (T-2814)
- [x] rival approach: Grep-driven sweep: grep the whole `plugin/lib` tree for `\bfm\b` command patterns beyond the listed sites to catch ones the ticket missed. Pair it with the shared helper to avoid regressions. — answered: adopted: step 1's scan is that sweep over plugin/lib/sampo
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2778 [FEATURE M, done, 3 steps] Skills and docs teach sampo spellings (sampo task new, sampo check …) once every hook… — lesson: Before a docs rename, list every parse…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Why not caught
the first scan covered three files and skipped any string containing 'sampo'
## Lessons
- A scan for missing aliases judges each pattern by what it matches, never by whether the alias text appears in it
## Files touched
- plugin/tests/test_rename_scan.py
- .fm-scratch/e1.json
- plugin/lib/sampo/cost.py
- .fm-scratch/e2.json
- plugin/lib/sampo/bench.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/fixes.py
- plugin/lib/sampo/friction.py
- plugin/lib/sampo/long.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/mandate.py
- plugin/lib/sampo/repeats.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/smithtui.py
- plugin/tests/test_cost.py
- plugin/tests/test_repeats.py
- plugin/tests/test_friction.py
