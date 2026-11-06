---
id: T-1037
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlib.py, plugin/lib/fmscout.py, plugin/lib/fmcli.py, plugin/tests/test_library.py, plugin/tests/test_scout.py, plugin/skills/library/SKILL.md]
depends_on: []
source: user
created: 2026-10-16T03:17:26Z
updated: 2026-10-16T09:53:35Z
base: f165e02937d9a07b33aa2f60fcdf46644a9c3327
base_tree: 52d93241538145c3d9412259283da58913564ebe
plan0_at: 2026-10-16T09:37:01Z
plan0_scope: [plugin/lib/fmlib.py, plugin/lib/fmscout.py, plugin/lib/fmcli.py, plugin/tests/test_library.py, plugin/tests/test_scout.py, plugin/skills/library/SKILL.md]
verified: strong
---
# Grow the card library in bulk for uncovered dependencies (fm scout finds them across proje
## Raw request
> Grow the card library in bulk for uncovered dependencies (fm scout finds them across projects): drafts written from real docs (context7, the package's own README), held to the card format and a quality check before they join
## Interpretation
Grow the card library in bulk where projects need it: fm lib gaps lists dependencies no card covers (across registered projects); fm lib draft stages a card; fm lib admit lints a staged card and moves it into the library or rejects it with the problems.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm lib admit` moves a well-formed draft into the library and rejects a malformed one with its problems — verify with `python3 plugin/tests/run.py test_library`
- [x] `fm lib gaps --json` lists uncovered deps — verify with `python3 plugin/tests/run.py test_library test_scout`
## Non-goals
## Approach (options → choice → why)
Refactor the dependency loop out of probe_lib_gaps into uncovered_deps(roots); admit runs the existing card lint. Drafting uses the existing card template; nothing is admitted unlinted. Options considered: auto-admit drafts (quality risk), or one card at a time by hand (doesn't scale).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: a staged good card is admitted (file in cards dir, exit 0); a card with a missing section stays staged (exit 1, the lint message printed); gaps lists an uncovered dep and not a covered one.
2. [x] Refactor the dep loop out of `probe_lib_gaps` into `uncovered_deps(roots)`; add the `draft`, `admit` and `gaps` actions in `cmd_lib`.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md plugin/skills/library/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_library` → ✗ exit 1 · Ran 17 tests in 3.4s (7 classes, 16 at a time; slowest: LibSources 3s, LibrarySuggest 2s, LibrarySearch 2s) / FAILED (1 classes) [ran] [tree 12255abc9890] (2026-10-16T09:37:50Z)
- (step 2) `python3 plugin/tests/run.py test_library test_scout` → exit 0 · Ran 33 tests in 27.3s (9 classes, 16 at a time; slowest: Scout 27s, ScoutDrive 5s, LibSources 3s) / OK [ran] [tree 339c3ab2237b] (2026-10-16T09:39:23Z)
- (step 2) `python3 plugin/tests/run.py test_library test_scout` → exit 0 · Ran 36 tests in 21.8s (9 classes, 16 at a time; slowest: Scout 22s, ScoutDrive 2s, LibraryAdmit 2s) / OK [ran] [tree dcd9c42e8dd4] (2026-10-16T09:47:08Z)
- (step 2) `python3 plugin/tests/run.py test_library test_scout` → exit 0 · Ran 37 tests in 25.1s (9 classes, 16 at a time; slowest: Scout 25s, ScoutDrive 4s, LibraryAdmit 4s) / OK [ran] [tree 5afc470c8ee9] (2026-10-16T09:50:20Z)
- (step 1) `python3 plugin/tests/run.py test_library test_scout test_help` → exit 0 · Ran 41 tests in 17.4s (11 classes, 16 at a time; slowest: Scout 17s, ScoutDrive 2s, LibraryAdmit 2s) / OK [ran] [tree 9717a25a70be] (2026-10-16T09:51:46Z)
- (ac 1) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 21 tests in 3.4s (7 classes, 16 at a time; slowest: LibraryAdmit 3s, LibSources 3s, LibrarySuggest 2s) / OK [ran] [tree 1997dafb1c00] (2026-10-16T09:52:40Z)
- (ac 2) `python3 plugin/tests/run.py test_library test_scout` → exit 0 · Ran 37 tests in 32.9s (9 classes, 16 at a time; slowest: Scout 33s, ScoutDrive 4s, LibraryAdmit 4s) / OK [ran] [tree 1997dafb1c00] (2026-10-16T09:52:40Z)
- (audit intent) `fm-reviewer (intent, adversary, edge) plus the automated commit security review: admit could write anywhere (--into ~/.claude) and follow symlinks → cards folder only, O_NOFOLLOW, one read linted then O_EXCL write, kebab-case names; the untrusted-text check refused existing cards and missed curl|python and bash <(curl) → fixed, all existing cards pass; a negation word anywhere on a line exempted a match → only a governing never/avoid/don't directly before it; a missing --root read as success → error` → grow cards where projects need them, safely [tree 1997dafb1c00] (2026-10-16T09:52:40Z)
- (audit adversary) `fm-reviewer (intent, adversary, edge) plus the automated commit security review: admit could write anywhere (--into ~/.claude) and follow symlinks → cards folder only, O_NOFOLLOW, one read linted then O_EXCL write, kebab-case names; the untrusted-text check refused existing cards and missed curl|python and bash <(curl) → fixed, all existing cards pass; a negation word anywhere on a line exempted a match → only a governing never/avoid/don't directly before it; a missing --root read as success → error` → no write outside the cards folder; untrusted instructions refused; governed-negation only [tree 1997dafb1c00] (2026-10-16T09:52:40Z)
- (audit edge) `fm-reviewer (intent, adversary, edge) plus the automated commit security review: admit could write anywhere (--into ~/.claude) and follow symlinks → cards folder only, O_NOFOLLOW, one read linted then O_EXCL write, kebab-case names; the untrusted-text check refused existing cards and missed curl|python and bash <(curl) → fixed, all existing cards pass; a negation word anywhere on a line exempted a match → only a governing never/avoid/don't directly before it; a missing --root read as success → error` → symlink, ../ area, missing root, existing cards [tree 1997dafb1c00] (2026-10-16T09:52:40Z)
- (audit operator) `fm-reviewer (intent, adversary, edge) plus the automated commit security review: admit could write anywhere (--into ~/.claude) and follow symlinks → cards folder only, O_NOFOLLOW, one read linted then O_EXCL write, kebab-case names; the untrusted-text check refused existing cards and missed curl|python and bash <(curl) → fixed, all existing cards pass; a negation word anywhere on a line exempted a match → only a governing never/avoid/don't directly before it; a missing --root read as success → error` → gaps sorted by use; admit prints problems and keeps the draft staged [tree 1997dafb1c00] (2026-10-16T09:52:40Z)
- (audit maintainer) `fm-reviewer (intent, adversary, edge) plus the automated commit security review: admit could write anywhere (--into ~/.claude) and follow symlinks → cards folder only, O_NOFOLLOW, one read linted then O_EXCL write, kebab-case names; the untrusted-text check refused existing cards and missed curl|python and bash <(curl) → fixed, all existing cards pass; a negation word anywhere on a line exempted a match → only a governing never/avoid/don't directly before it; a missing --root read as success → error` → uncovered_deps shared by fmscout and fmlib [tree 1997dafb1c00] (2026-10-16T09:52:40Z)
## Log
- 2026-10-16T03:17:26Z created
- 2026-10-16T05:01:13Z set scope=['plugin/lib/fmlib.py', 'plugin/lib/fmscout.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_library.py', 'plugin/tests/test_scout.py', 'plugin/skills/library/SKILL.md']
- 2026-10-16T05:01:13Z set tier=L
- 2026-10-16T09:36:52Z set tier=M
- 2026-10-16T09:36:53Z re-tiered L → M: three fm lib actions (gaps, draft, admit) and one refactor (uncovered_deps out of probe_lib_gaps) in fmlib/fmscout and their tests; not cross-cutting, no schema/API/security surface
- 2026-10-16T09:36:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1037.builder.md
- 2026-10-16T09:37:00Z focused
- 2026-10-16T09:51:23Z merged worktree-agent-acbf210dddf5987dd (4 file(s))
- 2026-10-16T09:51:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acbf210dddf5987dd
- 2026-10-16T09:51:27Z focused
- 2026-10-16T09:52:03Z scope: CHANGELOG.md, MASTER.md, plugin/skills/library/SKILL.md — docs point at gaps/draft/admit
- 2026-10-16T09:53:34Z done
- 2026-10-16T09:53:35Z committed 67ec5c8 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py changed since it was written]
- T-1036 [FEATURE L, done, 4 steps] Cards actually used, and many more of them: inject framework and library cards by what the — lesson: Apply a cap after the per-task see…
- research T-1036-review: Verdict** — changes needed. Three correctness gaps in the injection path (displaced cards, wildcard deps, files outside the project). The rest is…
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
- similar past tasks were L: consider --tier L
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scout.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmlib.py, plugin/lib/fmscout.py, plugin/tests/test_library.py; re-ground the plan against them before editing
## Lessons
- A keyword filter for instructions needs the negation to govern the match, not merely share the line
## Plan gaps
- failed first: step 1 Failing tests: a staged good card is admitted (file in cards dir, exit 0); a card with a missing se…
## Files touched
- plugin/tests/test_library.py
- plugin/lib/fmscout.py
- plugin/lib/fmlib.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/library/SKILL.md
