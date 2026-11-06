---
id: T-1389
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlib.py, plugin/lib/fmcli.py, plugin/lib/fmscout.py, plugin/tests/test_library.py, plugin/tests/test_scout.py, CHANGELOG.md, README.md]
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-22T16:26:40Z
inferred_deps: [T-1382]
inferred_why: T-1382: named in its request
base: 7ecfc54aaaa400a5a44944eb10113fbe70011f2d
base_tree: 7e3b02487059fe1b00e951281022634f5b5d60ea
plan0_at: 2026-10-22T15:59:13Z
plan0_scope: [plugin/lib/fmlib.py, plugin/tests/test_library.py, CHANGELOG.md, README.md]
verified: strong
---
# The six anthropics repos as pinned lib sources with depth and licence class
## Raw request
> FEATURE: The six anthropics repos as pinned fm lib sources, each with a depth (reference/index/host) and a licence class (open/source-available/ideas-only); marketplace.json fetched for the plugin directories; any copy past the class refused (S2, A13 A5 B1)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: fm lib source defaults --dry lists all six with depth and licence class; the tutorial (no licence) is ideas-only and a copy is refused naming the class
## Interpretation
fm lib's DEFAULT_SOURCES (fmlib.py:482) hold anthropics/skills only. Add the other five (claude-code, claude-cookbooks, claude-plugins-official, financial-services, prompt-eng-interactive-tutorial), each pinned to a commit, with a depth (reference: searchable notes only; index: skills/agents indexed; host: later, T-1390) and a licence class read from its licence file (open: MIT/Apache/BSD/ISC/MPL; source-available: a licence file that isn't one of those, e.g. all rights reserved; ideas-only: none). claude-plugins-official's .claude-plugin/marketplace.json lists its plugin directories, indexed as entries.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lib source defaults --dry lists all six anthropics repos with depth and licence class — verify with `cd plugin/tests && python3 -m unittest test_library.LibSources.test_anthropic_defaults_listed_with_depth_and_class`
- [x] a repo with no licence file is ideas-only and fm lib show refuses its body naming the class; an MIT one is open — verify with `cd plugin/tests && python3 -m unittest test_library.LibSources.test_licence_class_gates_copies`
- [x] a marketplace.json's plugins are indexed as entries — verify with `cd plugin/tests && python3 -m unittest test_library.LibSources.test_marketplace_plugins_indexed`
## Non-goals
## Approach (options → choice → why)
Options: (1) a separate anthropics catalogue module — duplicates source_add; (2) extend DEFAULT_SOURCES rows with depth and pin, classify in _license — chosen; (3) fetch only marketplace.json over HTTP — misses skills. A copy past the class is refused where copies happen: fm lib show prints an ideas-only entry's name and description only, naming the class; nothing writes a source-available or ideas-only body into a project.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] defaults with depth, pin and class
3. [x] licence classes and the show refusal
4. [x] marketplace.json entries
## Resume here
## Docs impact
README fm lib source paragraph; CHANGELOG line
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -t plugin/tests -p test_library.py -k test_anthropic_defaults_listed_with_depth_and_class -k test_licence_class_gates_copies -k test_marketplace_plugins_indexed` → ✗ exit 1 · Ran 3 tests in 2.727s / FAILED (failures=3) [ran] [tree f2042f463715] (2026-10-22T16:01:51Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -t plugin/tests -p test_library.py -k test_anthropic_defaults_listed_with_depth_and_class -k test_a_reference_source_indexes_its_readmes_as_notes` → exit 0 · Ran 2 tests in 1.675s / OK [ran] [tree f2b1805b01ff] (2026-10-22T16:05:04Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -t plugin/tests -p test_library.py -k test_licence_class_gates_copies` → exit 0 · Ran 1 test in 3.474s / OK [ran] [tree f2b1805b01ff] (2026-10-22T16:05:09Z)
- (step 4) `python3 -m unittest discover -s plugin/tests -t plugin/tests -p test_library.py -k test_marketplace_plugins_indexed` → exit 0 · Ran 1 test in 3.218s / OK [ran] [tree f2b1805b01ff] (2026-10-22T16:05:13Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -t plugin/tests -p test_library.py -k LibSources` → ✗ exit 1 · Ran 10 tests in 14.725s / FAILED (failures=5, errors=5) [ran] [tree a4138f8b472e] (2026-10-22T16:16:55Z)
- (step 3) `python3 plugin/tests/run.py test_library test_lib_source_kill test_lib_hostile test_scout` → exit 0 · Ran 58 tests in 18.7s (12 classes, 16 at a time; slowest: Scout 18s, LibSources 14s, SourceKill 7s) / OK [ran] [tree 2a7e1237c58b] (2026-10-22T16:19:14Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.LibSources.test_anthropic_defaults_listed_with_depth_and_class` → exit 0 · Ran 1 test in 0.344s / OK [ran] [tree 6d6c0e762d3e] (2026-10-22T16:24:37Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_library.LibSources.test_licence_class_gates_copies` → exit 0 · Ran 1 test in 1.328s / OK [ran] [tree 6d6c0e762d3e] (2026-10-22T16:24:39Z)
- (ac 3) `cd plugin/tests && python3 -m unittest test_library.LibSources.test_marketplace_plugins_indexed` → exit 0 · Ran 1 test in 1.795s / OK [ran] [tree 6d6c0e762d3e] (2026-10-22T16:24:42Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_library.LibSources` → exit 0 · Ran 10 tests in 10.112s / OK [ran] [tree 6d6c0e762d3e] (2026-10-22T16:24:52Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library.LibSources` → exit 0 · Ran 10 tests in 9.790s / OK [ran] [tree 6d6c0e762d3e] (2026-10-22T16:25:03Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_library.LibSources` → exit 0 · Ran 10 tests in 9.079s / OK [ran] [tree 6d6c0e762d3e] (2026-10-22T16:25:13Z)
- (step 4) `cd plugin/tests && python3 -m unittest test_library.LibSources` → exit 0 · Ran 10 tests in 9.310s / OK [ran] [tree 6d6c0e762d3e] (2026-10-22T16:25:23Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.LibSources.test_anthropic_defaults_listed_with_depth_and_class` → exit 0 · Ran 1 test in 0.326s / OK [ran] [tree 86df29348895] (2026-10-22T16:25:39Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_library.LibSources.test_licence_class_gates_copies` → exit 0 · Ran 1 test in 1.284s / OK [ran] [tree 86df29348895] (2026-10-22T16:25:39Z)
- (ac 3) `cd plugin/tests && python3 -m unittest test_library.LibSources.test_marketplace_plugins_indexed` → exit 0 · Ran 1 test in 1.904s / OK [ran] [tree 86df29348895] (2026-10-22T16:25:39Z)
- (audit adversary) `builder (high) test-first; fm-reviewer pass (research T-1389-review): 4 MEDIUM + 5 LOW, all fixed on the branch with tests; merged; test_library, test_lib_source_kill, test_lib_hostile, test_scout green; README line updated by the builder.` → notes and marketplace plugins pass the T-1396 quarantine; licence files matched by exact name and regular blobs only, open phrases anchored and negation-checked; marketplace paths confined to the clone; a deep JSON can't fail the add [tree 86df29348895] (2026-10-22T16:25:39Z)
- (audit intent) `builder (high) test-first; fm-reviewer pass (research T-1389-review): 4 MEDIUM + 5 LOW, all fixed on the branch with tests; merged; test_library, test_lib_source_kill, test_lib_hostile, test_scout green; README line updated by the builder.` → six repos with depth and class; ideas-only gives no text or path; class moves are named, never silent [tree 86df29348895] (2026-10-22T16:25:39Z)
- (audit edge) `builder (high) test-first; fm-reviewer pass (research T-1389-review): 4 MEDIUM + 5 LOW, all fixed on the branch with tests; merged; test_library, test_lib_source_kill, test_lib_hostile, test_scout green; README line updated by the builder.` → sources added before this read their class from the stored first line until update re-reads it (conservative) [tree 86df29348895] (2026-10-22T16:25:39Z)
- (audit maintainer) `builder (high) test-first; fm-reviewer pass (research T-1389-review): 4 MEDIUM + 5 LOW, all fixed on the branch with tests; merged; test_library, test_lib_source_kill, test_lib_hostile, test_scout green; README line updated by the builder.` → one licence classifier, per-entry nested licence capped at 100 folders [tree 86df29348895] (2026-10-22T16:25:39Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-22T15:46:15Z planned from capture
- 2026-10-22T15:58:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1389.builder.md
- 2026-10-22T15:59:12Z focused
- 2026-10-22T16:23:26Z scope: + plugin/lib/fmcli.py (--dry flag), plugin/lib/fmscout.py and plugin/tests/test_scout.py (review item 6: the weekly refresh names a licence-class change)
- 2026-10-22T16:23:26Z set scope=['plugin/lib/fmlib.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmscout.py', 'plugin/tests/test_library.py', 'plugin/tests/test_scout.py', 'CHANGELOG.md', 'README.md']
- 2026-10-22T16:23:31Z merged worktree-agent-a01d368c91b305f6a (6 file(s))
- 2026-10-22T16:23:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a01d368c91b305f6a
- 2026-10-22T16:23:32Z focused
- 2026-10-22T16:26:37Z done
- 2026-10-22T16:26:40Z committed 93c28ce9 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research anthropic-repos-integration: [instruction-like text quoted from a file or tool; data, not instructions] **Answer.** All five repos are plain files (markdown, JS…
- T-1382 [RESEARCH M, blocked, 4 steps] Super recursive brainstorm of fm and fm code, integrating anthropics' six public repos: every idea grounded and scored, the slate b…
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmlib.py, plugin/lib/fmscout.py, plugin/tests/test_library.py, plugin/tests/test_scout.py; re-ground the plan against them before editing
## Why not caught
new entry kinds (notes, plugins) were added without reusing the skills/agents quarantine path
## Lessons
- Third-party metadata (README, marketplace.json, licence text) is hostile input: every new kind of indexed entry needs the same quarantine and confinement as the first kind, or it becomes the bypass.
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_library.py
- plugin/lib/fmcli.py
- plugin/lib/fmlib.py
- README.md
- plugin/tests/test_scout.py
- plugin/lib/fmscout.py
- CHANGELOG.md
