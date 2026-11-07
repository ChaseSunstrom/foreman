---
id: T-2600
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T10:46:31Z
updated: 2026-11-02T11:58:21Z
base: d2f4f18accea5e3ad571d717d9a598af9926eda1
base_tree: 60d780bee972f6cf23c285c67e3b65202b3ac607
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T10:48:05Z
plan0_scope: []
verified: strong
---
# fm lib's dependency reader skips path dependencies (Cargo, Poetry): a workspace crate is the project's own code, not a stack needing a card
## Raw request
> FIX: fm scout --slow lists a Cargo path dependency (jarvis-desktop-logic, a workspace crate of jarvis-code: logic = { path = ... }) as a dependency without a stack card; a path or workspace dependency is the project's own code and never needs a card
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] _toml_deps leaves out a Cargo or Poetry dependency whose table has a path key, keeps version, git and workspace=true ones — verify with `python3 plugin/tests/run.py test_lib`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_lib
2. [x] filter path entries in _toml_deps
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_library.LibraryCards` → ✗ exit 1 · Ran 7 tests in 1.0s (1 classes, 16 at a time; slowest: LibraryCards 1s) / FAILED (1 classes: test_library.LibraryCards) [ran] [tree e2ba05acdb6b] [world 2f1906870a] (2026-11-02T10:55:46Z)
- (step 2) `python3 plugin/tests/run.py test_library test_scout` → exit 0 · Ran 83 tests in 14.7s (14 classes, 16 at a time; slowest: Scout 14s, LibSources 5s, Mandate 3s) / OK [ran] [tree 8155d11e201a] [world 2f1906870a] (2026-11-02T10:56:32Z)
- `python3 plugin/tests/run.py test_library.LibraryCards` → ✗ exit 1 · Ran 7 tests in 2.0s (1 classes, 16 at a time; slowest: LibraryCards 1s) / FAILED (1 classes: test_library.LibraryCards) (start tree + this task's tests) [ran] [tree a3445cec02d7] [world 2f1906870a] (2026-11-02T11:02:16Z)
- `python3 plugin/tests/run.py test_library.LibraryCards` → exit 0 · Ran 7 tests in 1.0s (1 classes, 16 at a time; slowest: LibraryCards 1s) / OK [ran] [tree a3445cec02d7] [world 2f1906870a] (2026-11-02T11:02:16Z)
- (ac 1) `python3 plugin/tests/run.py test_lib` → exit 0 · Ran 59 tests in 5.2s (13 classes, 16 at a time; slowest: LibSources 5s, SourceKill 2s, HostileCorpus 2s) / OK [ran] [tree a3445cec02d7] [world 2f1906870a] (2026-11-02T11:02:22Z)
- (audit intent) `self-review: _named skips table entries whose value carries a path key; applied to Cargo/Pipfile tables, Poetry groups and workspace dependencies; version, git and workspace=true entries stay` → a Cargo path crate and a Poetry path package are left out; version, git and workspace=true deps stay (test) [tree a3445cec02d7] (2026-11-02T11:02:22Z)
- (audit edge) `self-review: _named skips table entries whose value carries a path key; applied to Cargo/Pipfile tables, Poetry groups and workspace dependencies; version, git and workspace=true entries stay` → a Pipfile entry with a path is the project's own too; a string value can't carry a path, so it stays [tree a3445cec02d7] (2026-11-02T11:02:22Z)
- (audit self) `self-review: _named skips table entries whose value carries a path key; applied to Cargo/Pipfile tables, Poetry groups and workspace dependencies; version, git and workspace=true entries stay` → no findings [tree a3445cec02d7] (2026-11-02T11:02:22Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 8c1c32ee7d8b] [world 2f1906870a] (2026-11-02T11:58:21Z)
## Log
- 2026-11-02T10:46:31Z created
- 2026-11-02T10:46:49Z planned from capture
- 2026-11-02T10:48:05Z set approved=True
- 2026-11-02T10:48:05Z focused
- 2026-11-02T10:48:05Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T11:02:43Z done
- 2026-11-02T11:02:45Z committed 6176c50b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- T-2599 [FEATURE S, deferred, 0 steps] Write stack cards for hmac, hmmlearn, http-body-util, import-linter, io.github.takahirom.roborazzi:roborazzi
- playbook Rust Build Error Resolver (fm playbooks show build/rust-build)
- decision 2026-10-31: Deferred scout captures T-2301 (stack cards for other projects' deps) and T-2302 (upstream voltagent source moved) under gen-0's MUST (tokens into F…
- similar past tasks were M: consider --tier M
- the similar finished task took 1 steps
## Lessons
- A dependency reader must tell the project's own code (path and workspace members) from outside stacks, or every monorepo floods its findings
## Plan gaps
- failed first: step 1 red test in test_lib
## Files touched
- plugin/tests/test_library.py
- plugin/lib/fmlib.py
- CHANGELOG.md
