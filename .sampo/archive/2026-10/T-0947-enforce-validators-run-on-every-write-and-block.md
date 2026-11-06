---
id: T-0947
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T20:44:23Z
updated: 2026-10-15T21:03:00Z
base: f6d9ea1a5257a3f5b4a89340060500a0aff50571
base_tree: b193a8555d3c4f2b4cbf690f6a29d75672ef34d1
verified: strong
---
# Enforce: validators run on every write and block until fixed (cards, JSON, skill frontmatter, Python, project globs via fm check onwrite)
## Raw request
> Enforce: validators run on every write and block until fixed (cards, JSON, skill frontmatter, Python, project globs via fm check onwrite)
## Interpretation
Part of T-0942 (the user: have FM enforce things instead of relying on inconsistent agents). post_tool_use (fmhooks.py ~1527) gains a validator step for Write/Edit/MultiEdit/NotebookEdit. It looks up validators for the written path: built-ins (plugin/skills/library/cards/**/*.md → fmlib.lint on that one card; *.json → json.loads; */SKILL.md and agents/*.md → name and description in the frontmatter; *.py → compile()), plus the project's own from meta 'onwrite' ({glob: cmd with {file}}) set by fm check onwrite. On failure it answers {decision: block, reason} so Claude, or the subagent, must fix it first. A timeout of 5 s each; the failure is logged as an enforce event.
## Assumptions (confidence)
## Acceptance criteria
- [x] Writing a stack card that fails the lint, invalid JSON, or a SKILL.md without name/description makes the PostToolUse hook answer decision block with the problem, in subagents too; a clean write passes silently — verify with `python3 plugin/tests/run.py -k OnWrite`
- [x] fm check onwrite GLOB 'CMD {file}' registers a project validator that runs on matching writes, at most 5 s, and a failing one blocks with its last lines — verify with `python3 plugin/tests/run.py -k OnWrite`
- [x] Hook latency stays inside budget: a non-matching write adds under 5 ms — verify with `python3 plugin/tests/bench_hooks.py --runs 20`
## Non-goals
## Approach (options → choice → why)
Options: (A) the hook or the fm verb does the step itself, so no agent has to remember it (chosen; T-0942 brainstorm research/brainstorm-20261015-154016); (B) stronger instructions in rules and skills (what failed: 19 card writers were told to lint and didn't); (C) a supervising reviewer agent per task (costly, and still an agent); (D) a per-repo enforce.toml policy file (later, if the meta registry outgrows itself). Built-ins are in-process (no subprocess) to stay inside the hook budget; project commands run via subprocess with a timeout. The PostToolUse entry must be sync for Write/Edit (an async hook cannot block): check hooks.json and split the matcher if needed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing OnWrite tests
2. [x] Built-in validators and the fm check onwrite registry, called from post_tool_use
3. [x] Docs and the bench
## Resume here
## Docs impact
MASTER.md and README (the builder's lines on fm check onwrite and write validation); CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k OnWrite` → ✗ exit 1 · Ran 9 tests in 1.5s (1 classes, 16 at a time; slowest: OnWrite 1s) / FAILED (1 classes) [ran] [tree 90b1352e65ce] (2026-10-15T20:49:08Z)
- (step 2) `python3 plugin/tests/run.py -k OnWrite` → exit 0 · Ran 9 tests in 6.6s (1 classes, 16 at a time; slowest: OnWrite 7s) / OK [ran] [tree 226085909434] (2026-10-15T20:51:09Z)
- (step 3) `python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · Notification                34.9    41.7     150  [0] / SessionEnd                  32.1    36.3     150  [0] [ran] [tree 828011883480] (2026-10-15T20:52:08Z)
- (ac 1) `python3 plugin/tests/run.py -k OnWrite` → ✗ exit 1 · Ran 10 tests in 6.8s (1 classes, 16 at a time; slowest: OnWrite 7s) / FAILED (1 classes) [ran] [tree 60ca57710859] (2026-10-15T20:58:38Z)
- (ac 2) `python3 plugin/tests/run.py -k OnWrite` → ✗ exit 1 · Ran 10 tests in 6.7s (1 classes, 16 at a time; slowest: OnWrite 7s) / FAILED (1 classes) [ran] [tree 60ca57710859] (2026-10-15T20:58:45Z)
- (ac 3) `python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · Notification                33.5    37.4     150  [0] / SessionEnd                  30.8    32.3     150  [0] [ran] [tree 60ca57710859] (2026-10-15T20:58:58Z)
- `python3 plugin/tests/run.py -k OnWrite` → ✗ exit 1 · Ran 10 tests in 1.5s (1 classes, 16 at a time; slowest: OnWrite 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 60ca57710859] (2026-10-15T20:59:07Z)
- `python3 plugin/tests/run.py -k OnWrite` → ✗ exit 1 · Ran 10 tests in 6.7s (1 classes, 16 at a time; slowest: OnWrite 7s) / FAILED (1 classes) [ran] [tree 60ca57710859] (2026-10-15T20:59:07Z)
- (ac 1) `python3 plugin/tests/run.py -k OnWrite` → exit 0 · Ran 10 tests in 6.7s (1 classes, 16 at a time; slowest: OnWrite 7s) / OK [ran] [tree 5d38048cb5b1] (2026-10-15T21:00:05Z)
- (ac 2) `python3 plugin/tests/run.py -k OnWrite` → exit 0 · Ran 10 tests in 6.7s (1 classes, 16 at a time; slowest: OnWrite 7s) / OK [ran] [tree 5d38048cb5b1] (2026-10-15T21:00:12Z)
- `python3 plugin/tests/run.py -k OnWrite` → ✗ exit 1 · Ran 10 tests in 1.5s (1 classes, 16 at a time; slowest: OnWrite 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 5d38048cb5b1] (2026-10-15T21:00:20Z)
- `python3 plugin/tests/run.py -k OnWrite` → exit 0 · Ran 10 tests in 6.7s (1 classes, 16 at a time; slowest: OnWrite 7s) / OK [ran] [tree 5d38048cb5b1] (2026-10-15T21:00:20Z)
- (ac 1) `python3 plugin/tests/run.py -k OnWrite` → exit 0 · Ran 10 tests in 6.7s (1 classes, 16 at a time; slowest: OnWrite 7s) / OK [ran] [tree 5979ebdd4f3b] (2026-10-15T21:01:51Z)
- (ac 2) `python3 plugin/tests/run.py -k OnWrite` → exit 0 · Ran 10 tests in 6.7s (1 classes, 16 at a time; slowest: OnWrite 7s) / OK [ran] [tree 5979ebdd4f3b] (2026-10-15T21:01:57Z)
- (ac 3) `python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · Notification                33.6    37.3     150  [0] / SessionEnd                  30.8    32.6     150  [0] [ran] [tree 5979ebdd4f3b] (2026-10-15T21:02:10Z)
- (ac 1) `python3 plugin/tests/run.py -k OnWrite` → exit 0 · Ran 10 tests in 6.7s (1 classes, 16 at a time; slowest: OnWrite 7s) / OK [ran] [tree 5979ebdd4f3b] (2026-10-15T21:02:59Z)
- (ac 2) `python3 plugin/tests/run.py -k OnWrite` → exit 0 · Ran 10 tests in 6.7s (1 classes, 16 at a time; slowest: OnWrite 7s) / OK [ran] [tree 5979ebdd4f3b] (2026-10-15T21:02:59Z)
- (ac 3) `python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · Notification                34.6    40.2     150  [0] / SessionEnd                  31.2    32.6     150  [0] [ran] [tree 5979ebdd4f3b] (2026-10-15T21:02:59Z)
- (audit intent) `main-thread review of the branch; replaced its lookahead matcher split with a plain catch-all plus a validate-only sync entry (a rejected regex would have dropped every tool's recording); fixed its self-check test to read tracked JSON only` → ok: cards, JSON, Python, SKILL.md and agent frontmatter and fm check onwrite globs validate on every write and block until fixed, in subagents too [tree 5979ebdd4f3b] (2026-10-15T21:02:59Z)
- (audit adversary) `main-thread review of the branch; replaced its lookahead matcher split with a plain catch-all plus a validate-only sync entry (a rejected regex would have dropped every tool's recording); fixed its self-check test to read tracked JSON only` → ok: onwrite commands are guard-checked when stored and run argv-quoted with {file} shlex-quoted and a 5 s cap [tree 5979ebdd4f3b] (2026-10-15T21:02:59Z)
- (audit edge) `main-thread review of the branch; replaced its lookahead matcher split with a plain catch-all plus a validate-only sync entry (a rejected regex would have dropped every tool's recording); fixed its self-check test to read tracked JSON only` → ok: a timeout notes and doesn't block; docs/agents prose isn't an agent definition; only tracked JSON in the self-check [tree 5979ebdd4f3b] (2026-10-15T21:02:59Z)
- (audit operator) `main-thread review of the branch; replaced its lookahead matcher split with a plain catch-all plus a validate-only sync entry (a rejected regex would have dropped every tool's recording); fixed its self-check test to read tracked JSON only` → ok: PostToolUse catch-all unchanged (async); the write entry is sync with a 30 s timeout and adds ~0 ms when nothing matches (bench p95 38 ms) [tree 5979ebdd4f3b] (2026-10-15T21:02:59Z)
- (audit maintainer) `main-thread review of the branch; replaced its lookahead matcher split with a plain catch-all plus a validate-only sync entry (a rejected regex would have dropped every tool's recording); fixed its self-check test to read tracked JSON only` → ok: post_tool_validate is one small function with its own handler name [tree 5979ebdd4f3b] (2026-10-15T21:02:59Z)
## Log
- 2026-10-15T20:44:23Z created
- 2026-10-15T20:44:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0947.builder.md
- 2026-10-15T20:44:53Z focused
- 2026-10-15T20:52:08Z latency: in-process _onwrite on a non-matching write costs 0.011 ms (200 runs, scratch timing of fmhooks._onwrite); bench PostToolUse p95 38 ms of 150
- 2026-10-15T20:58:23Z merged worktree-agent-a4d6fe0d1f8c73488 (7 file(s))
- 2026-10-15T20:58:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4d6fe0d1f8c73488
- 2026-10-15T20:58:31Z focused
- 2026-10-15T21:03:00Z done
- 2026-10-15T21:03:00Z committed 87c9f48 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0933 [FEATURE L, done, 5 steps] Stack library: 400+ on-demand implementation cards (fm lib) plus federated search over installed plugins' skills — lesson: Subagent-wri…
- research T-0933-review: Changes needed. The code works and the 22 cards I sampled are accurate. Detect signals produce false-positive suggestions, and one manifest regex…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
## Why not caught
none: new capability
## Lessons
- Split hook behaviour by a separate entry with a plain matcher and its own handler name, not by a lookahead regex: a matcher a surface rejects silently drops every tool it was meant to cover.
## Plan gaps
- failed first: step 1 Failing OnWrite tests
## Files touched
- plugin/tests/test_onwrite.py
- plugin/lib/fmlib.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcli.py
- plugin/hooks/hooks.json
- plugin/tests/test_docs.py
- MASTER.md
