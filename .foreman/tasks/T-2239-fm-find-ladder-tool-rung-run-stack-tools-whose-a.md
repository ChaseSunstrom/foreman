---
id: T-2239
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T00:06:09Z
updated: 2026-10-31T06:31:30Z
inferred_deps: [T-2185]
inferred_why: T-2185: named in its request
base: 285730e7a747c66ae3022f244cbbf06160df8ebe
base_tree: b45a57ddc438d8c463c0e062743b020bbf8bebfb
plan0_at: 2026-10-31T05:53:57Z
plan0_scope: []
verified: strong
---
# fm find --ladder tool rung: run stack tools whose argv comes only from Foreman's…
## Raw request
> fm find --ladder tool rung: run stack tools whose argv comes only from Foreman's registry (stack cards); repo manifests only select entries, never supply argv; only in a trusted tree or exam sandbox; SARIF/text normalized to findings with learned precision (T-2185 rung c)
## Interpretation
Steer 4's detection ladder, rung c (T-2185): fm find's own finders are language-agnostic heuristics; each stack's standard analyzers (ruff, shellcheck, go vet, eslint …) find what they can't. Running them means running tools in a repo, and some (eslint configs, go vet's build) execute repo code, so the rung must never run where the user hasn't said yes, and the repo must never choose the command line.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm find --ladder in a trusted tree runs each registry tool its manifests select (shell=False, timeout, stripped env) and reports normalized findings as tool:NAME finders; in an untrusted tree it runs nothing and says why; argv never comes from the repo; a selected tool missing from PATH is captured once as a missing tool — verify with `python3 plugin/tests/run.py test_find`
## Non-goals
## Approach (options → choice → why)
1) fm find --ladder: a registry in Foreman (data: tool name, fixed argv, the manifest files that select it, the output parser: SARIF or JSON or a line regex, kind) — a repo's manifests only select entries, never supply argv or flags; it runs only when fmprove.trusted(root) (the user's own fm prove --yes-run) or inside an exam sandbox, else it prints 'tool rung skipped: not a trusted tree'; each run shell=False, a timeout, credentials and FOREMAN_/CLAUDE env stripped, cwd the tree, output capped; findings become named finders (tool:NAME) so T-2125's per-finder precision learns them; a selected tool not on PATH is filed once through the capability-miss capture (T-2270). 2) read argv from stack cards' Verify lines — rejected: free text a card source could steer. 3) run in a throwaway copy always — later: trusted-only is the gate fmprove already uses. Choice 1.
## Risks and rollback
Repo code execution through a tool's config (eslint.config.js, conftest) is why the trust gate is mandatory; tests prove an untrusted tree runs nothing (a stub tool on PATH records any call). Rollback: the rung is opt-in behind --ladder.
## Execution prompt
## Steps
1. [x] red tests with stub tools on PATH: trusted runs and parses; untrusted runs nothing (call log empty); repo can't inject argv; missing tool captured once
2. [x] registry data + runner + parsers (SARIF, JSON, line regex) in fmfind
3. [x] docs: MASTER fm find line, README, CHANGELOG
## Resume here
## Docs impact
MASTER.md, README.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_find 2>&1 | tail -30` → ✗ exit 1 · Ran 108 tests in 18.0s (22 classes, 16 at a time; slowest: FindBlindSpots 15s, FindProve 8s, FindCli 7s) / FAILED (1 classes) [ran] [tree 60bf125299f3] (2026-10-31T05:56:22Z)
- (ac 1) `python3 plugin/tests/run.py test_find 2>&1 | grep -v "^$" | tail -30` → ✗ exit 1 · Ran 108 tests in 32.0s (22 classes, 16 at a time; slowest: FindBlindSpots 31s, FindProve 16s, FindRenders 14s) / FAILED (1 classes) [ran] [tree d2cdf2772ef9] (2026-10-31T05:56:59Z)
- (step 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 108 tests in 23.6s (22 classes, 16 at a time; slowest: FindBlindSpots 23s, FindProve 15s, FindRenders 14s) / OK [ran] [tree 6b0f57e85ac2] (2026-10-31T05:59:01Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_statusline_ui && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 369 tests in 45.8s (86 classes, 16 at a time; slowest: TaskLifecycle 45s, FindBlindSpots 31s, BoardVerbs 31s) / FAILED (1 classes) [ran] [tree 6b0f57e85ac2] (2026-10-31T05:59:48Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_statusline_ui && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 369 tests in 29.8s (86 classes, 16 at a time; slowest: TaskLifecycle 29s, BoardVerbs 19s, FindBlindSpots 19s) / FAILED (1 classes) [ran] [tree b86f434e54ab] (2026-10-31T06:01:00Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_statusline_ui && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 369 tests in 37.5s (86 classes, 16 at a time; slowest: TaskLifecycle 37s, BoardVerbs 27s, FindBlindSpots 27s) / FAILED (1 classes) [ran] [tree fe46dfd38bf1] (2026-10-31T06:02:05Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_statusline_ui && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.77s] [ran] [tree 48ad7b9a9888] (2026-10-31T06:02:58Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_statusline_ui && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [14.98s] [ran] [tree 95307b2e70e9] (2026-10-31T06:14:52Z)
- `python3 plugin/tests/run.py test_find test_prove` → ✗ exit 1 · Ran 121 tests in 8.8s (24 classes, 16 at a time; slowest: FindBlindSpots 8s, FindCli 6s, FindProve 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 3d0c935f970f] (2026-10-31T06:27:10Z)
- `python3 plugin/tests/run.py test_find test_prove` → exit 0 · Ran 121 tests in 12.5s (24 classes, 16 at a time; slowest: FindBlindSpots 12s, FindRenders 8s, FindProve 7s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:27:10Z)
- (step 1) `python3 plugin/tests/run.py test_find test_prove` → exit 0 · Ran 121 tests in 12.3s (24 classes, 16 at a time; slowest: FindBlindSpots 12s, FindRenders 8s, FindProve 7s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:27:23Z)
- (step 2) `python3 plugin/tests/run.py test_find test_prove` → exit 0 · Ran 121 tests in 12.1s (24 classes, 16 at a time; slowest: FindBlindSpots 12s, FindRenders 7s, FindProve 7s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:27:35Z)
- (step 3) `python3 plugin/tests/run.py test_find test_prove` → exit 0 · Ran 121 tests in 12.2s (24 classes, 16 at a time; slowest: FindBlindSpots 12s, FindRenders 8s, FindProve 7s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:27:47Z)
- (ac 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 117 tests in 13.1s (22 classes, 16 at a time; slowest: FindBlindSpots 13s, FindRenders 8s, FindProve 8s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:30:09Z)
- (audit intent) `self + one adversary fm-reviewer pass (1 medium: RLIMIT_FSIZE silently killing go's compiler; 6 low; all fixed with tests); every subprocess start listed and checked` → steer 4's tool rung: each stack's own analyzer feeds fm find as tool:NAME finders with learned precision (test_find red-to-green) [tree 3d0c935f970f] (2026-10-31T06:30:09Z)
- (audit adversary) `self + one adversary fm-reviewer pass (1 medium: RLIMIT_FSIZE silently killing go's compiler; 6 low; all fixed with tests); every subprocess start listed and checked` → runs only in a tree the user trusted by its realpath or an exam sandbox; argv only from Foreman's registry; PATH cut to absolute dirs outside the tree and an exe resolving into the tree refused; ruff --isolated, GOPROXY=off, GOTOOLCHAIN=local, CGO_ENABLED=0; findings only for tracked non-symlink files; env stripped [tree 3d0c935f970f] (2026-10-31T06:30:09Z)
- (audit edge) `self + one adversary fm-reviewer pass (1 medium: RLIMIT_FSIZE silently killing go's compiler; 6 low; all fixed with tests); every subprocess start listed and checked` → timeout and output caps kill the process group (finally); a signal death or an unparsed failure leaves a note; vendored go modules use -mod=vendor; a subfolder of a trusted tree stays untrusted [tree 3d0c935f970f] (2026-10-31T06:30:09Z)
- (audit operator) `self + one adversary fm-reviewer pass (1 medium: RLIMIT_FSIZE silently killing go's compiler; 6 low; all fixed with tests); every subprocess start listed and checked` → opt-in behind --ladder; a missing tool is captured once as capability-miss [tree 3d0c935f970f] (2026-10-31T06:30:09Z)
- (audit maintainer) `self + one adversary fm-reviewer pass (1 medium: RLIMIT_FSIZE silently killing go's compiler; 6 low; all fixed with tests); every subprocess start listed and checked` → the registry is data in one place; the real tools' output formats are unverified here (stubs), noted [tree 3d0c935f970f] (2026-10-31T06:30:09Z)
## Log
- 2026-10-31T00:06:09Z created
- 2026-10-31T05:53:40Z set tier=M
- 2026-10-31T05:53:41Z planned: it has criteria and steps
- 2026-10-31T05:53:42Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2239.builder.md
- 2026-10-31T05:53:56Z focused
- 2026-10-31T06:17:51Z merged worktree-agent-ae0bc111f132cfd37 (5 file(s))
- 2026-10-31T06:17:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae0bc111f132cfd37
- 2026-10-31T06:26:47Z focused
- 2026-10-31T06:27:57Z paused: focus moved to T-2276
- 2026-10-31T06:29:54Z focused
- 2026-10-31T06:29:55Z scope: plugin/lib/fmfind.py (TOOLS, ladder, _run_tool, scan extra), plugin/lib/fmcli.py (--ladder), plugin/tests/test_find.py, MASTER.md, README.md, CHANGELOG.md
- 2026-10-31T06:31:05Z done
- 2026-10-31T06:31:30Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2185 [FEATURE L, planned, 7 steps] Initiative detection ladder (steer 2026-10-30 #4, capability #1): fm find stays the free…
- T-2121 [FEATURE L, done, 2 steps] fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule for #1 Initiative: fm find stays…
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- similar past tasks were L: consider --tier L
- the similar finished task took 2 steps
## Lessons
- An rlimit on a tool is inherited by everything it starts: cap the output you read, not the files its children write
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmfind.py
- plugin/lib/fmcli.py
- README.md
- MASTER.md
- .gitignore
- CHANGELOG.md
- plugin/agents/fm-builder.md
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmlong.py
- plugin/tests/genesis_page.js
- plugin/tests/test_docs.py
- plugin/tests/test_genesis.py
- plugin/tests/test_long.py
- plugin/tests/test_proof.py
- plugin/tests/test_site_build.py
- site/genesis/genesis.js
- site/genesis/index.html
