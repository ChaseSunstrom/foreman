---
id: T-0724
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-09T17:17:40Z
updated: 2026-10-09T17:36:22Z
base: a5ebca31841d3329aaff509b81c3a1b677b6f7bb
base_tree: 8ac20711a0811437c4cf0bcabdfcd6e57ff9540e
verified: strong
---
# Outline-first reads (T-0717: 925 Read results over 5k tokens = 8.6M tokens/30 days): a ful
## Raw request
> Outline-first reads (T-0717: 925 Read results over 5k tokens = 8.6M tokens/30 days): a full Read of a source file over ~600 lines gets its outline (fm outline) and a range pointer first, with offset 1 or a limit reading it whole; measure hook latency on Read before shipping
## Interpretation
Cut the 8.6M tokens a month spent on full Reads of big files (T-0717) by showing the outline first, so the model reads only the range it needs. Never block a read Foreman can't judge, and never hide a file the model insists on.
## Assumptions (confidence)
## Acceptance criteria
- [x] a first full Read of a file over 600 lines is refused with its outline (code defs, Markdown headings, a diff's files with line ranges) and how to read a range; the same Read again, a range, a small file, or another agent's first read goes through; a compaction resets it — verify with `python3 plugin/tests/run.py -p test_firewall.py -k OutlineFirst`
- [x] the Read hook never blocks a read on failure and stays fast — verify with `python3 plugin/tests/run.py -p test_firewall.py -k ReadHookSafety`
## Non-goals
## Approach (options → choice → why)
Options: (a) deny a full Read of a big file once, with its outline in the reason (the model then reads ranges, or repeats the Read to get it whole); (b) rewrite the Read via updatedInput to add a limit (bypass mode only; silently truncates); (c) PostToolUse summary (can't replace a tool result); (d) a cheap-model reader (costs a call per read). Choice: (a) — no truncation surprise, works in every permission mode, and the outline is useful context on its own. Its own PreToolUse entry for Read that never blocks on failure (the guard's entry fails closed), a stat-first fast path (~30 ms per Read), once per file per agent between compactions; outline for code (fmmap), Markdown headings and diff files (fm outline gains those too).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing OutlineFirst and ReadHookSafety tests
2. [x] fmmap.outline for Markdown and diffs; fmhooks _outline_first; hooks.json Read entry without onFailure block
3. [x] measure on real transcripts: how many big full reads it would have caught
## Resume here
## Docs impact
CHANGELOG entry; MASTER.md hook paragraph
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_firewall.py` → ✗ exit 1 · Ran 5 tests in 0.6s (2 classes, 16 at a time; slowest: OutlineFirst 1s, ReadHookSafety 0s) / FAILED (2 classes) [ran] [tree 37105cee2dab] (2026-10-09T17:33:23Z)
- (step 3) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/017cbb6b-0026-4a64-af96-4068091225da/scratchpad/outline_measure.py` → exit 0 · first full reads of 600+ line files: 367, ~4,130,177 tokens; as outlines (~800 each): ~293,600 tokens; saved if each then reads a 200-line range (~2,000 tokens): ~3,102,577 tokens [ran] [tree 606a4dd62b60] (2026-10-09T17:36:12Z)
- (ac 1) `python3 plugin/tests/run.py -p test_firewall.py -k OutlineFirst` → exit 0 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: OutlineFirst 1s) / OK [ran] [tree 606a4dd62b60] (2026-10-09T17:36:22Z)
- (ac 2) `python3 plugin/tests/run.py -p test_firewall.py -k ReadHookSafety` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: ReadHookSafety 0s) / OK [ran] [tree 606a4dd62b60] (2026-10-09T17:36:22Z)
- (step 1) `python3 plugin/tests/run.py -p test_firewall.py -p test_docs.py -p test_map.py` → exit 0 · Ran 28 tests in 1.1s (9 classes, 16 at a time; slowest: Map 1s, OutlineFirst 1s, ReadHookSafety 0s) / OK [ran] [tree 606a4dd62b60] (2026-10-09T17:36:22Z)
- (step 2) `python3 plugin/tests/run.py -p test_firewall.py -p test_docs.py -p test_map.py` → exit 0 · Ran 28 tests in 1.1s (9 classes, 16 at a time; slowest: Map 1s, OutlineFirst 1s, ReadHookSafety 0s) / OK [ran] [tree 606a4dd62b60] (2026-10-09T17:36:22Z)
- (audit intent) `self over the diff: Read handled before the guard path in _pre_tool_use, wrapped so any error lets the read through; its own hooks.json entry without onFailure; the seen-list lives in state/sessions/<sid>.* so SessionStart clears it` → cuts the measured 8.6M big-read tokens where the model needed a part; never hides a file (the same Read again reads whole; a range always reads) [tree 606a4dd62b60] (2026-10-09T17:36:22Z)
- (audit adversary) `self over the diff: Read handled before the guard path in _pre_tool_use, wrapped so any error lets the read through; its own hooks.json entry without onFailure; the seen-list lives in state/sessions/<sid>.* so SessionStart clears it` → the hook only ever denies a Read with an outline; a crafted file can't make it allow anything the Read wouldn't, and outline text goes through plain_lines; session and agent ids are validated before they name a file [tree 606a4dd62b60] (2026-10-09T17:36:22Z)
- (audit edge) `self over the diff: Read handled before the guard path in _pre_tool_use, wrapped so any error lets the read through; its own hooks.json entry without onFailure; the seen-list lives in state/sessions/<sid>.* so SessionStart clears it` → unreadable, missing, small, ranged or paged reads pass; a file with nothing to outline passes; 80-row cap falls back to top-level rows [tree 606a4dd62b60] (2026-10-09T17:36:22Z)
- (audit operator) `self over the diff: Read handled before the guard path in _pre_tool_use, wrapped so any error lets the read through; its own hooks.json entry without onFailure; the seen-list lives in state/sessions/<sid>.* so SessionStart clears it` → ~31 ms per Read; a hook failure never blocks a read (test pins the entry has no onFailure block) [tree 606a4dd62b60] (2026-10-09T17:36:22Z)
## Log
- 2026-10-09T17:17:40Z created
- 2026-10-09T17:33:08Z focused
- 2026-10-09T17:36:22Z done
- 2026-10-09T17:36:22Z committed 4eaf81c (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0717-tool-result-sizes: Measured with scratchpad/sizes.py over 64,393 tool results (~31.7M tokens, chars/4).
- research brainstorm-20261004-round7: Run: brainstorm-20261003-235742 (bold bets, measured self-evolution with fm bench, state-of-the-art harness gaps, unspoken needs; de…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- decision 2026-10-04: Friction pass deferred to the next day
- the similar finished task took 3 steps
## Measurements
30 days of transcripts: 367 first full reads of 600+ line files, ~4.13M tokens; as outlines ~0.29M; with a 200-line range read after each, ~3.1M tokens saved (upper bound: a re-read whole costs ~800 extra). Hook cost: ~31 ms per Read (unguarded path, measured).
## Lessons
- Measure where tokens go before building a token saver: delta reads and noisy-runner wrapping measured ~0, while the first full read of big files held 4.1M tokens a month.
## Files touched
- plugin/tests/test_firewall.py
- plugin/lib/fmmap.py
- plugin/lib/fmhooks.py
- plugin/hooks/hooks.json
- plugin/tests/test_docs.py
- CHANGELOG.md
- MASTER.md
