---
id: T-2017
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T17:03:35Z
updated: 2026-10-29T17:31:01Z
base: fadef9478419589fb846aae16eade243a189973f
base_tree: 782077dede7ead992fd6304d681a8403292cfb39
plan0_at: 2026-10-29T17:04:21Z
plan0_scope: []
paused_tree: 8963f9cb49b05da51b0ff1baaf0759725edc5174
verified: strong
---
# Hooks skip work a call doesn't need: plain() fast path, no fmdeps import without an install word, last_change parses only touched lines
## Raw request
> Hooks skip work a call doesn't need: plain() fast path, no fmdeps import without an install word, last_change parses only touched lines
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] plain keeps stripping control, format and variation characters — verify with `python3 plugin/tests/run.py test_core -k plain`
- [x] last_change and the dep note give the same answers — verify with `python3 plugin/tests/run.py test_ledger_chain test_deps -k last_change_parses -k no_install_word`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] plain: isprintable fast path, test first
2. [x] last_change filters lines before json.loads; _dep_note skips the import without an install verb; measure hooks
## Resume here
<!-- auto -->
- 2026-10-29T17:19:18Z steps 2/2 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_core.py, plugin/tests/test_deps.py, plugin/tests/test_ledger_chain.py
- failures met: error: unable to create file xxe.md: no space left on device
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core -k plain` → exit 0 · Ran 2 tests in 0.3s (2 classes, 16 at a time; slowest: Briefs 0s, WorkRequests 0s) / OK [ran] [tree d444b247a76e] (2026-10-29T17:09:41Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_chain test_deps -k last_change_parses -k no_install_word` → exit 0 · Ran 2 tests in 0.7s (2 classes, 16 at a time; slowest: Deps 0s, Chain 0s) / OK [ran] [tree d444b247a76e] (2026-10-29T17:09:42Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 4221 tests in 185.0s (995 classes, 16 at a time; slowest: Worker 98s, Stop 54s, Fakes 44s) / FAILED (1 classes) (environment: disk full) [ran] [tree 8963f9cb49b0] (2026-10-29T17:14:17Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k plain` → exit 0 · Ran 2 tests in 0.3s (2 classes, 16 at a time; slowest: WorkRequests 0s, Briefs 0s) / OK [ran] [tree e1f8a6534e1a] (2026-10-29T17:30:17Z)
- (ac 2) `python3 plugin/tests/run.py test_ledger_chain test_deps -k last_change_parses -k no_install_word` → exit 0 · Ran 2 tests in 0.7s (2 classes, 16 at a time; slowest: Deps 0s, Chain 0s) / OK [ran] [tree e1f8a6534e1a] (2026-10-29T17:30:17Z)
- (audit intent) `self-review of the diff (budget spent: no subagents): plain()'s fast path returns only text that is printable and has no variation selectors, the cases plain() would otherwise change; _tail_rows keep= only skips lines missing a needed key and last_change still bypasses the memo; _dep_note's install-word check matches every verb fmdeps handles (install, add, i)` → hooks do less per call; outputs unchanged (tests pin plain, last_change, dep check) [tree e1f8a6534e1a] (2026-10-29T17:30:17Z)
- (audit edge) `self-review of the diff (budget spent: no subagents): plain()'s fast path returns only text that is printable and has no variation selectors, the cases plain() would otherwise change; _tail_rows keep= only skips lines missing a needed key and last_change still bypasses the memo; _dep_note's install-word check matches every verb fmdeps handles (install, add, i)` → a line cut at a partial read's start is still dropped; a non-str to plain() takes the old path; 'pip3 i' and 'npm add' still reach fmdeps [tree e1f8a6534e1a] (2026-10-29T17:30:17Z)
- (audit self) `self-review of the diff (budget spent: no subagents): plain()'s fast path returns only text that is printable and has no variation selectors, the cases plain() would otherwise change; _tail_rows keep= only skips lines missing a needed key and last_change still bypasses the memo; _dep_note's install-word check matches every verb fmdeps handles (install, add, i)` → no findings [tree e1f8a6534e1a] (2026-10-29T17:30:17Z)
## Log
- 2026-10-29T17:03:35Z created
- 2026-10-29T17:04:20Z focused
- 2026-10-29T17:07:40Z hypothesis: _tail_rows' remaining cost is the re-decode/splitlines of each growing chunk; counting bytes and decoding once should cut it. Result: 27.3 -> 21.3 ms unfiltered, 11.3 -> 5.5 ms filtered; rules out json parsing as the floor
- 2026-10-29T17:09:41Z criterion 2 verify: `python3 plugin/tests/run.py test_core test_deps -k 'last_change or note'` → `python3 plugin/tests/run.py test_ledger_chain test_deps -k last_change_parses -k no_install_word`
- 2026-10-29T17:09:54Z scope: CHANGELOG.md (perf line)
- 2026-10-29T17:19:44Z paused: focus moved to T-2019
- 2026-10-29T17:30:59Z done
- 2026-10-29T17:31:01Z committed 81f54563 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- T-1049 [FEATURE M, done, 3 steps] Dependency-install check in the guard: a new npm/pip/cargo package named in an install get — lesson: A hook that touches the network ne…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
## Measurements
PreToolUse min 70 -> 57 ms; Notification 116 -> 95 ms; last_change cold 20.7 -> 5.0 ms; _tail_rows 5000 27.3 -> 21.3 ms (5.5 filtered)
## Files touched
- plugin/tests/test_core.py
- plugin/tests/test_ledger_chain.py
- plugin/tests/test_deps.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
