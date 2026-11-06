---
id: T-1021
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-16T01:40:39Z
updated: 2026-10-16T01:41:16Z
base: 1900549fb4336478341dfdca62968065768b0ccb
base_tree: d18ae441409047953fe1ff8e0b1c0720a5b11aa1
verified: strong
---
# fm lib: a go.mod's // indirect requires aren't the project's dependencies
## Raw request
> fm lib: a go.mod's // indirect requires aren't the project's dependencies
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fmlib's go.mod reading keeps direct requires and drops // indirect ones (single-line and block form) — verify with `python3 plugin/tests/run.py test_library`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a go.mod with direct and indirect requires
2. [x] skip // indirect in the go.mod parser
3. [x] docs: CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_library` → ✗ exit 1 · Ran 14 tests in 1.3s (6 classes, 16 at a time; slowest: LibSources 1s, LibrarySuggest 1s, LibrarySearch 1s) / FAILED (1 classes) [ran] [tree 19c45530b0a5] (2026-10-16T01:40:51Z)
- (step 2) `python3 plugin/tests/run.py test_library test_map` → exit 0 · Ran 21 tests in 1.9s (9 classes, 16 at a time; slowest: Map 2s, LibSources 1s, LibrarySuggest 1s) / OK [ran] [tree 8b0aa618b0ee] (2026-10-16T01:40:58Z)
- (step 3) `grep -q 'T-1021' CHANGELOG.md` → exit 0 · (no output) [ran] [tree e51485e1e720] (2026-10-16T01:41:08Z)
- (ac 1) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 14 tests in 1.3s (6 classes, 16 at a time; slowest: LibSources 1s, LibrarySuggest 1s, LibrarySearch 1s) / OK [ran] [tree e51485e1e720] (2026-10-16T01:41:09Z)
- `python3 plugin/tests/run.py test_library` → ✗ exit 1 · Ran 14 tests in 1.6s (6 classes, 16 at a time; slowest: LibSources 1s, LibrarySuggest 1s, LibrarySearch 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree e51485e1e720] (2026-10-16T01:41:13Z)
- `python3 plugin/tests/run.py test_library` → exit 0 · Ran 14 tests in 1.3s (6 classes, 16 at a time; slowest: LibSources 1s, LibrarySuggest 1s, LibrarySearch 1s) / OK [ran] [tree e51485e1e720] (2026-10-16T01:41:13Z)
- (audit edge) `self` → single-line and block requires both covered; a hostile one-line go.mod still can't hang (existing test); uncovered deps across projects 98 → 54 [tree e51485e1e720] (2026-10-16T01:41:13Z)
- (ac 1) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 14 tests in 1.4s (6 classes, 16 at a time; slowest: LibSources 1s, LibrarySuggest 1s, LibrarySearch 1s) / OK [ran] [tree e51485e1e720] (2026-10-16T01:41:15Z)
- (audit edge) `red→green; tail measured before and after` → block and single-line forms [tree e51485e1e720] (2026-10-16T01:41:15Z)
- (audit self) `red→green; tail measured before and after` → no findings [tree e51485e1e720] (2026-10-16T01:41:15Z)
## Log
- 2026-10-16T01:40:39Z created
- 2026-10-16T01:40:40Z focused
- 2026-10-16T01:40:43Z criterion 1 verify: `python3 plugin/tests/run.py test_lib` → `python3 plugin/tests/run.py test_library`
- 2026-10-16T01:41:15Z done
- 2026-10-16T01:41:16Z committed 09414b9 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0588 [RESEARCH L, done, 3 steps] And maybe a knowledge graph if we dont have it already, and also, better intuition/reasoni — lesson: grounding brainstormers in today'…
- T-0012 [FEATURE L, done, 5 steps] Harness-enforced procedure: stage machine, next-action injection, no edits without a planned task
- T-1020 [FEATURE S, done, 1 steps] Stack cards: SvelteKit adapters, Vite plugins, VS Code extension tooling and xterm.js detected
- T-1016 [FEATURE S, done, 2 steps] Stack cards for the deps scout found: scipy, python-audio (librosa, soundfile, demucs), postprocessing; detect lines for playwright-cor…
- similar finished tasks took 1–5 steps
## Why not caught
the go.mod fixture had no indirect requires
## Plan gaps
- failed first: step 1 red test: a go.mod with direct and indirect requires
## Files touched
- plugin/tests/test_library.py
- plugin/lib/fmlib.py
- CHANGELOG.md
