---
id: T-1049
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdeps.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/tests/test_deps.py]
depends_on: []
source: followup
created: 2026-10-16T03:42:10Z
updated: 2026-10-16T07:40:20Z
base: 4584fb01da32901ab93cf56d1a2f90d597b8eef0
base_tree: 428f31cf0ee6960f65b2636c34b007d28f1e571b
plan0_at: 2026-10-16T07:37:52Z
plan0_scope: [plugin/lib/fmdeps.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/tests/test_deps.py]
verified: strong
---
# Dependency-install check in the guard: a new npm/pip/cargo package named in an install get
## Raw request
> Dependency-install check in the guard: a new npm/pip/cargo package named in an install gets an age, typosquat and registry check before it runs (T-1029 C10)
## Interpretation
When a Bash command installs packages (npm/pnpm/yarn/bun add or install, pip/pip3/`python -m pip`/`uv pip install`, cargo add/install), the guard names each package that is new to the project. It then checks age, typosquat and registry before the command runs. Nothing like it exists: fmguard.py only has `_PUBLISH` (fmguard.py:3123), which covers publishing, not installing. The result is a PreToolUse note, so a wrong guess never blocks work.
## Assumptions (confidence)
## Acceptance criteria
- [x] `npm i lodahs` gets a typosquat note and `npm i lodash` stays silent; a package under 14 days old (fake fetcher) is flagged; a custom `--registry` is flagged — verify with `python3 plugin/tests/run.py test_deps`
- [x] the hook emits the note as PreToolUse additionalContext and never blocks, even when the fetcher raises — verify with `python3 plugin/tests/run.py test_deps`
## Non-goals
## Approach (options → choice → why)
(a) block in fmguard.check_bash. (b) A new fmdeps.py called from the PreToolUse note chain beside `_fix_note` (fmhooks.py:1142, 1153). (c) A CLI-only `fm deps check`. Choose (b), plus an `fm deps check "<cmd>"` entry point for tests and manual use. A note matches how a false positive costs nothing, and a hook note is the existing pattern. The checks are: - Typosquat: edit distance 1 from a built-in top-names list or from the project's own manifest deps. - Registry: `--registry`, `--index-url`, `--extra-index-url`, `git+` or URL specs. - Age: a registry JSON fetch with a 2 s timeout and an injectable fetcher. It fails open as "age unknown", and is skipped in sensitive projects and under FOREMAN_NO_NET=1. Add `parse_install(cmd)`, `check(p, cmd, fetch=None)` and `cmd_deps` in a new plugin/lib/fmdeps.py. Add `_dep_note(pl, p)` in fmhooks.py and a lazy `deps` subparser in fmcli.py.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: `fm deps check "npm i lodahs" --json` lists a typosquat of lodash. The age case uses a monkeypatched fetch. `self.hook("PreToolUse", Bash pip install --index-url http://x requests)` returns additionalContext containing "registry". A package already in package.json or requirements.txt is not "new".
2. [x] Write fmdeps.py (parser, manifest reader, Levenshtein ≤1, checks).
3. [x] Wire `_dep_note` into the note chain and the `deps` subcommand.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_deps` → exit 0 · Ran 6 tests in 10.6s (1 classes, 16 at a time; slowest: Deps 10s) / OK [ran] [tree f0719695da65] (2026-10-16T07:14:32Z)
- (step 2) `python3 plugin/tests/run.py test_deps` → exit 0 · Ran 6 tests in 9.6s (1 classes, 16 at a time; slowest: Deps 9s) / OK [ran] [tree f0719695da65] (2026-10-16T07:14:43Z)
- (step 3) `python3 plugin/tests/run.py test_deps` → exit 0 · Ran 6 tests in 3.3s (1 classes, 16 at a time; slowest: Deps 3s) / OK [ran] [tree f0719695da65] (2026-10-16T07:14:46Z)
- (step 3) `python3 plugin/tests/run.py test_deps` → exit 0 · Ran 10 tests in 24.7s (1 classes, 16 at a time; slowest: Deps 24s) / OK [ran] [tree 1db2109eaaed] (2026-10-16T07:23:24Z)
- (step 1) `python3 plugin/tests/run.py test_deps test_tool_taint test_tool_injection test_hooks` → exit 0 · Ran 178 tests in 39.6s (23 classes, 16 at a time; slowest: Stop 39s, PreToolUse 19s, SessionStart 15s) / OK [ran] [tree 783e2a20867d] (2026-10-16T07:38:32Z)
- (ac 1) `python3 plugin/tests/run.py test_deps` → exit 0 · Ran 10 tests in 7.0s (1 classes, 16 at a time; slowest: Deps 7s) / OK [ran] [tree a075774d3979] (2026-10-16T07:39:04Z)
- (ac 2) `python3 plugin/tests/run.py test_deps` → exit 0 · Ran 10 tests in 7.0s (1 classes, 16 at a time; slowest: Deps 7s) / OK [ran] [tree a075774d3979] (2026-10-16T07:39:04Z)
- (audit intent) `fm-reviewer (security + edge + performance): unbounded per-lookup time → one shared 1.2 s budget in abandoned worker threads; popular/scoped/private-registry names were looked up → skipped; -f and other value flags misread as names → per-tool flag sets; cargo label mismatch → crates; more installers parsed; all fixed test-first. Hand check: fm deps check 'npm i lodahs' names lodash` → a note, never a block, on typosquat-shaped or brand-new package names [tree a075774d3979] (2026-10-16T07:39:04Z)
- (audit adversary) `fm-reviewer (security + edge + performance): unbounded per-lookup time → one shared 1.2 s budget in abandoned worker threads; popular/scoped/private-registry names were looked up → skipped; -f and other value flags misread as names → per-tool flag sets; cargo label mismatch → crates; more installers parsed; all fixed test-first. Hand check: fm deps check 'npm i lodahs' names lodash` → redirects re-checked as public https via fmresearch._Redirect; no lookup for private registries or sensitive repos so names don't leak [tree a075774d3979] (2026-10-16T07:39:04Z)
- (audit edge) `fm-reviewer (security + edge + performance): unbounded per-lookup time → one shared 1.2 s budget in abandoned worker threads; popular/scoped/private-registry names were looked up → skipped; -f and other value flags misread as names → per-tool flag sets; cargo label mismatch → crates; more installers parsed; all fixed test-first. Hand check: fm deps check 'npm i lodahs' names lodash` → bash -c, python3.X -m pip, scoped names, value flags, whitelisted near-names (boto, pyaml) [tree a075774d3979] (2026-10-16T07:39:04Z)
- (audit operator) `fm-reviewer (security + edge + performance): unbounded per-lookup time → one shared 1.2 s budget in abandoned worker threads; popular/scoped/private-registry names were looked up → skipped; -f and other value flags misread as names → per-tool flag sets; cargo label mismatch → crates; more installers parsed; all fixed test-first. Hand check: fm deps check 'npm i lodahs' names lodash` → FOREMAN_NO_NET documented; fm deps check by hand [tree a075774d3979] (2026-10-16T07:39:04Z)
- (audit maintainer) `fm-reviewer (security + edge + performance): unbounded per-lookup time → one shared 1.2 s budget in abandoned worker threads; popular/scoped/private-registry names were looked up → skipped; -f and other value flags misread as names → per-tool flag sets; cargo label mismatch → crates; more installers parsed; all fixed test-first. Hand check: fm deps check 'npm i lodahs' names lodash` → one module, per-ecosystem tables, fetcher injectable for tests [tree a075774d3979] (2026-10-16T07:39:04Z)
## Log
- 2026-10-16T03:42:10Z created
- 2026-10-16T04:22:58Z set scope=['plugin/lib/fmdeps.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_deps.py']
- 2026-10-16T04:22:58Z set tier=M
- 2026-10-16T07:12:49Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1049.builder.md
- 2026-10-16T07:12:58Z focused
- 2026-10-16T07:37:35Z merged worktree-agent-a5b0b09db7d858028 (5 file(s))
- 2026-10-16T07:37:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5b0b09db7d858028
- 2026-10-16T07:37:52Z focused
- 2026-10-16T07:38:41Z scope: CHANGELOG.md — release note
- 2026-10-16T07:38:49Z scope: MASTER.md — fmdeps module named; CHANGELOG.md — release note
- 2026-10-16T07:40:19Z done
- 2026-10-16T07:40:20Z committed 280046f (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmhooks.py changed since it was written]
- playbook Test-Driven Development Workflow (skills/playbooks/references/verify/tdd-workflow.md)
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- the similar finished task took 2 steps
- start here (files T-0369 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmdeps.py, plugin/lib/fmhooks.py, plugin/tests/test_deps.py; re-ground the plan against them before editing
## Lessons
- A hook that touches the network needs one total deadline, not a timeout per call
## Files touched
- plugin/tests/test_deps.py
- plugin/lib/fmdeps.py
- plugin/lib/fmoutside.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_tool_taint.py
