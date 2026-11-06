---
id: T-1420
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T18:57:48Z
updated: 2026-10-21T22:27:47Z
base: c348823bf67018530004d4df7b78863edb9ae8a4
base_tree: 7382296f42b477605a18f40b1b086b561715f797
plan0_at: 2026-10-21T22:23:23Z
plan0_scope: []
verified: strong
---
# fm lib search matches a description's last word even with its full stop
## Raw request
> fm lib search treats a trailing period as part of a word, so the last word of a description is often unsearchable
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a description ending 'tidewater.' is found by fm lib search tidewater; node.js and c# stay one word — verify with `python3 plugin/tests/run.py test_library`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_library on fmlib._words and a search over a source skill, then strip leading and trailing dots from each word
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_library.LibrarySearch` → ✗ exit 1 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: LibrarySearch 2s) / FAILED (1 classes) [ran] [tree 69abe29a9733] (2026-10-21T22:23:38Z)
- (step 1) `python3 plugin/tests/run.py test_library test_lib_hostile` → exit 0 · Ran 31 tests in 7.2s (9 classes, 16 at a time; slowest: HostileCorpus 7s, LibraryAdmit 6s, LibSources 5s) / OK [ran] [tree fc75fcd72e40] (2026-10-21T22:23:53Z)
- (ac 1) `python3 plugin/tests/run.py test_library` → exit 0 · Ran 22 tests in 5.8s (7 classes, 16 at a time; slowest: LibraryAdmit 6s, LibSources 4s, LibrarySuggest 3s) / OK [ran] [tree a98c38c174af] (2026-10-21T22:24:10Z)
- (audit intent) `self: _words strips leading and trailing dots from each token; inner dots (node.js) and + and # (c++, c#) are kept; queries and texts go through the same function, so '.net' and 'net' match both ways` → a description ending 'tidewater.' is found by tidewater (test_library) [tree a98c38c174af] (2026-10-21T22:24:10Z)
- (audit edge) `self: _words strips leading and trailing dots from each token; inner dots (node.js) and + and # (c++, c#) are kept; queries and texts go through the same function, so '.net' and 'net' match both ways` → an ellipsis ('users...') and a leading dot ('.net') reduce to the word; a lone '.' or '..' drops out under the length rule [tree a98c38c174af] (2026-10-21T22:24:10Z)
- (audit self) `self: _words strips leading and trailing dots from each token; inner dots (node.js) and + and # (c++, c#) are kept; queries and texts go through the same function, so '.net' and 'net' match both ways` → no findings [tree a98c38c174af] (2026-10-21T22:24:10Z)
## Log
- 2026-10-21T18:57:48Z created
- 2026-10-21T22:23:20Z planned from capture
- 2026-10-21T22:23:22Z focused
- 2026-10-21T22:27:44Z done
- 2026-10-21T22:27:47Z committed 22147f53 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0945 [FEATURE M, done, 3 steps] fm lib source: index third-party skill repos read-only (rea, anthropics/skills, wshobson/agents, trailofbits, VoltAgent, K-Dense) for f…
- research t0018-r8-edge-adversary: HIGH — ADVERSARY — `plugin/lib/fmserve.py:304,315`** — The usage-limit check runs `USAGE_LIMIT.search(output)` where `output = r.stdout…
- research T-0262-review-1: LOW** — `plugin/lib/fmcore.py:230-239`: the creation-time check is sound. `realpath` plus the `top + os.sep` prefix rejects `../`, absolute pat…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
## Regression test
test_library.LibrarySearch.test_a_descriptions_last_word_is_found_despite_its_full_stop: red before (step 1 evidence exit 1), green after
## Why not caught
search tests used words from the middle of descriptions
## Lessons
- Tokenizers that keep '.' for names like node.js must strip it at word edges, or sentence-final words never match
## Plan gaps
- failed first: step 1 failing test in test_library on fmlib._words and a search over a source skill, then strip leading a…
## Files touched
- plugin/tests/test_library.py
- plugin/lib/fmlib.py
- CHANGELOG.md
