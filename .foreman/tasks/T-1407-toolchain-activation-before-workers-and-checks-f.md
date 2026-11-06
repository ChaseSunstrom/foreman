---
id: T-1407
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-23T09:37:02Z
inferred_deps: [T-1382]
inferred_why: T-1382: named in its request
base: 7b7ac5e53b7233131e3554aece993371f28694f7
base_tree: b2904c7e4e7da55a857680699162927cc65e2b00
plan0_at: 2026-10-23T09:33:33Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Toolchain activation: before workers and checks, fm code activates the project's pinned to
## Raw request
> FEATURE: Toolchain activation: before workers and checks, fm code activates the project's pinned toolchain (.tool-versions and the like) through trusted tools only, never running repo code to do it (S20, A30)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a fixture with .tool-versions runs its check on the pinned interpreter; a repo .envrc is never sourced
## Interpretation
Before workers and checks, fm code puts the project's pinned toolchain first on PATH. Pins are read as data (.tool-versions' first version per tool, .python-version, .node-version, .nvmrc; version numbers only). Each pin is looked up by a version manager already on PATH (mise where, asdf where, pyenv prefix), run from / with no stdin so the repo's config files, hooks and .envrc never run; its bin folder goes first on PATH in Run.env. A pin no manager has installed is named in a note and never installed.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fixture with .tool-versions runs its check on the pinned interpreter; a repo .envrc never runs; an uninstalled pin is named — verify with `python3 plugin/tests/run.py test_code.Toolchain`
## Non-goals
## Approach (options → choice → why)
Options: source .envrc or run 'mise env' in the repo (runs repo-defined code: refused by the brief); install missing versions (never silently); read pins as data and ask the managers only where an installed version lives. Choice: the last, one lookup per pin at run start, cached on the Run.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then pins, toolchain and Run.env
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.Toolchain` → ✗ exit 1 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: Toolchain 1s) / FAILED (1 classes) [ran] [tree 2ae887d2314d] (2026-10-23T09:33:39Z)
- (step 1) `python3 plugin/tests/run.py test_code.Toolchain test_code.Repairs` → exit 0 · Ran 10 tests in 7.4s (2 classes, 16 at a time; slowest: Repairs 7s, Toolchain 1s) / OK [ran] [tree 4280330c1d78] (2026-10-23T09:35:30Z)
- (ac 1) `python3 plugin/tests/run.py test_code.Toolchain` → exit 0 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: Toolchain 1s) / OK [ran] [tree 4280330c1d78] (2026-10-23T09:35:32Z)
- (audit intent) `self review; test_code, test_code_worker, test_code_bench green` → a .tool-versions pin found by mise puts its bin first on PATH and the verify runs on it (the shim's marker); an uninstalled pin is named; .envrc never runs (tests) [tree 4280330c1d78] (2026-10-23T09:35:32Z)
- (audit adversary) `self review; test_code, test_code_worker, test_code_bench green` → pins are parsed as data with strict tool and version patterns (no ref:, path:, system or aliases), so nothing from the repo reaches a command line but a matched name and number as separate argv words; managers run from / with no stdin and a 10 s timeout, so a repo mise.toml or .envrc is never read or sourced; only an absolute path with a bin folder is used [tree 4280330c1d78] (2026-10-23T09:35:32Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-23T09:33:28Z set tier=M, scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-23T09:33:32Z focused
- 2026-10-23T09:37:00Z done
- 2026-10-23T09:37:02Z committed 2e2af403 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1393 [SECURITY M, done, 2 steps] fm code's judge also holds shell rc files and agent settings under HOME, and reports an edit step that changed nothing — lesson: Resto…
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmcode.py, plugin/tests/test_code.py; re-ground the plan against them before editing
## Lessons
- Ask a version manager where an installed version lives (mise where, asdf where, pyenv prefix) from outside the repo, rather than letting it activate inside: activation reads repo config that can run code
## Plan gaps
- failed first: step 1 failing tests, then pins, toolchain and Run.env
## Files touched
- plugin/tests/test_code.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcode.py
