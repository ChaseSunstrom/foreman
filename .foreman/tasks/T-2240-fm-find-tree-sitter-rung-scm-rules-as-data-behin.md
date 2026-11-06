---
id: T-2240
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T00:06:09Z
updated: 2026-10-31T06:54:45Z
inferred_deps: [T-2185]
inferred_why: T-2185: named in its request
base: b8c75aa994103a5b2d485a6fe85a5f1d36658f00
base_tree: 8fa4ad7e0131312035ec7ce54f55dce15eb8e3c1
plan0_at: 2026-10-31T06:36:14Z
plan0_scope: []
verified: strong
---
# fm find tree-sitter rung: .scm rules as data behind an optional import, queued as a…
## Raw request
> fm find tree-sitter rung: .scm rules as data behind an optional import, queued as a plugin when the binding is missing (T-2185 rung d)
## Interpretation
Steer 4's ladder, rung d (T-2185): structural rules (tree-sitter queries) catch bug shapes regexes miss, per language, as data. The Python binding (tree_sitter + a language pack) isn't installed here; installing it is the user's grant, so the rung must work when present and file a capability-miss when absent.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a (stub) binding present, fm find --ladder runs each .scm rule over tracked files of its language and reports ts:RULE findings; with the binding absent it skips with a note and files one capability-miss: tree-sitter; files over the size cap and symlinks are skipped; rules come only from Foreman's ladder_rules — verify with `python3 plugin/tests/run.py test_find`
## Non-goals
## Approach (options → choice → why)
1) rules as data: plugin/lib/ladder_rules/<lang>/*.scm, each with a header (kind, message, severity); fm find --ladder imports tree_sitter and a language pack lazily, parses tracked non-symlink files of that language (size-capped), runs each query, and reports matches as ts:<rule> finders with learned precision; an ImportError files one 'capability-miss: tree-sitter' through the T-2270 key and the rung says it was skipped. Tests inject a stub tree_sitter module (sys.modules) that returns canned captures. 2) vendor a parser — rejected: a native dependency in the plugin. 3) shell out to the tree-sitter CLI — rejected: argv and grammar loading from the environment. Choice 1. Parsing doesn't execute repo code, so no trust gate is needed beyond fm find's own rules.
## Risks and rollback
A hostile file can make a parser slow: per-file size cap and a total time budget. Rules are Foreman's data only; a repo can't add rules.
## Execution prompt
## Steps
1. [x] red tests with a stub tree_sitter module: matches reported, absent binding captured once, caps and symlinks skipped
2. [x] ladder_rules data (a few starter rules for python and js) and the rung in fmfind
3. [x] docs: give MASTER and CHANGELOG lines in the report
## Resume here
<!-- auto -->
- 2026-10-31T06:46:03Z steps 3/3 done
- git: foreman/build; 2 uncommitted: CHANGELOG.md, MASTER.md
- touched since last checkpoint: .claude/worktrees/agent-aa7a8744f3722bb04/plugin/lib/ladder_rules/python/bare-except.scm, .claude/worktrees/agent-aa7a8744f3722bb04/plugin/lib/ladder_rules/python/mutable-default.scm, .claude/worktrees/agent-aa7a8744f3722bb04/plugin/lib/ladder_rules/javascript/eval-call.scm, .claude/worktrees/agent-aa7a8744f3722bb04/plugin/lib/ladder_rules/javascript/loose-null-compare.scm, .claude/worktrees/agent-aa7a8744f3722bb04/plugin/lib/fmfind.py, .claude/worktrees/agent-aa7a8744f3722bb04/plugin/tests/test_find.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_find` → ✗ exit 1 · Ran 125 tests in 7.5s (23 classes, 16 at a time; slowest: FindBlindSpots 7s, FindCli 6s, FindProve 5s) / FAILED (1 classes) [ran] [tree 68c4cb1605a5] (2026-10-31T06:37:20Z)
- (ac 1) `python3 plugin/tests/run.py test_find 2>&1 | tail -30` → ✗ exit 1 · Ran 125 tests in 7.7s (23 classes, 16 at a time; slowest: FindBlindSpots 7s, FindCli 6s, FindProve 5s) / FAILED (1 classes) [ran] [tree bcba0b12e48e] (2026-10-31T06:37:50Z)
- (step 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 7.4s (23 classes, 16 at a time; slowest: FindBlindSpots 7s, FindCli 6s, FindProve 5s) / OK [ran] [tree 6f3b548db285] (2026-10-31T06:38:12Z)
- (step 2) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 7.3s (23 classes, 16 at a time; slowest: FindBlindSpots 7s, FindCli 6s, FindProve 5s) / OK [ran] [tree 6f3b548db285] (2026-10-31T06:38:19Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_find && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.36s] [ran] [tree 6f3b548db285] (2026-10-31T06:38:38Z)
- `python3 plugin/tests/run.py test_find` → ✗ exit 1 · Ran 125 tests in 8.1s (23 classes, 16 at a time; slowest: FindBlindSpots 7s, FindCli 6s, FindProve 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree fd93500f670f] (2026-10-31T06:45:01Z)
- `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 7.2s (23 classes, 16 at a time; slowest: FindBlindSpots 7s, FindCli 6s, FindProve 4s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:45:01Z)
- (step 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 7.2s (23 classes, 16 at a time; slowest: FindBlindSpots 7s, FindCli 6s, FindProve 4s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:45:08Z)
- (step 2) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 7.2s (23 classes, 16 at a time; slowest: FindBlindSpots 7s, FindCli 6s, FindProve 4s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:45:15Z)
- (step 3) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 7.2s (23 classes, 16 at a time; slowest: FindBlindSpots 7s, FindCli 6s, FindProve 4s) / OK [ran] [tree fd93500f670f] (2026-10-31T06:45:23Z)
- (ac 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 12.5s (23 classes, 16 at a time; slowest: FindBlindSpots 12s, FindRenders 8s, FindProve 7s) / OK [ran] [tree e721d00cc394] (2026-10-31T06:48:47Z)
- (audit intent) `self-review of the diff: parses only (no repo code runs), regular non-symlink files from _files, 512 KB per file and a 30 s rung budget, 50 findings per rule per file, rules only from Foreman's ladder_rules (a repo's ladder_rules or .fm-ladder is ignored); the real binding's API is unverified here (stub)` → steer 4's tree-sitter rung: structural rules as data, ts:RULE finders with learned precision; an absent binding is a capability miss, queued once (test_find red-to-green) [tree e721d00cc394] (2026-10-31T06:48:47Z)
- (audit adversary) `self-review of the diff: parses only (no repo code runs), regular non-symlink files from _files, 512 KB per file and a 30 s rung budget, 50 findings per rule per file, rules only from Foreman's ladder_rules (a repo's ladder_rules or .fm-ladder is ignored); the real binding's API is unverified here (stub)` → a hostile file is only parsed, size- and time-capped; a binding error is a note, not a crash [tree e721d00cc394] (2026-10-31T06:48:47Z)
- (audit edge) `self-review of the diff: parses only (no repo code runs), regular non-symlink files from _files, 512 KB per file and a 30 s rung budget, 50 findings per rule per file, rules only from Foreman's ladder_rules (a repo's ladder_rules or .fm-ladder is ignored); the real binding's API is unverified here (stub)` → no files of a rule language means no miss filed; a missing language pack is the same miss [tree e721d00cc394] (2026-10-31T06:48:47Z)
## Log
- 2026-10-31T00:06:09Z created
- 2026-10-31T06:35:53Z set tier=M
- 2026-10-31T06:35:55Z planned: it has criteria and steps
- 2026-10-31T06:35:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2240.builder.md
- 2026-10-31T06:36:13Z focused
- 2026-10-31T06:41:20Z merged worktree-agent-aa7a8744f3722bb04 (6 file(s))
- 2026-10-31T06:41:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa7a8744f3722bb04
- 2026-10-31T06:44:44Z focused
- 2026-10-31T06:46:03Z paused: focus moved to T-2281
- 2026-10-31T06:48:33Z scope: plugin/lib/fmfind.py (_ts_rules, _ts_rung, ladder), plugin/lib/ladder_rules/ (new), plugin/tests/test_find.py, MASTER.md, CHANGELOG.md
- 2026-10-31T06:48:33Z focused
- 2026-10-31T06:49:24Z done
- 2026-10-31T06:49:35Z guard authorization added: publish
- 2026-10-31T06:54:45Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2185 [FEATURE L, planned, 7 steps] Initiative detection ladder (steer 2026-10-30 #4, capability #1): fm find stays the free…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule for #1 Initiative: fm find stays…
- T-2241 [FEATURE M, done, 3 steps] fm find blind spots: a closed FIX whose lines no finder flagged becomes a record and, at most once a day, a rule/tool/check task — less…
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- similar finished tasks took 3–4 steps
## Lessons
- An optional native dependency is a rung that files its own capability miss: the code ships, the install waits for the user's grant
## Plan gaps
- failed first: step 1 red tests with a stub tree_sitter module: matches reported, absent binding captured once, caps and …
## Files touched
- plugin/tests/test_find.py
- plugin/lib/ladder_rules/python/bare-except.scm
- plugin/lib/ladder_rules/python/mutable-default.scm
- plugin/lib/ladder_rules/javascript/eval-call.scm
- plugin/lib/ladder_rules/javascript/loose-null-compare.scm
- plugin/lib/fmfind.py
- CHANGELOG.md
- MASTER.md
