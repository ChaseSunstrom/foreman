---
id: T-1778
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard*.py, plugin/tests/bench_guard_scripts.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T10:51:51Z
updated: 2026-10-23T11:18:55Z
base: 9059fe26126c4a630355c3d67736c39d009795e3
base_tree: 30c7f6984bf56f2fa1308fa0c305d30fe5e40f28
plan0_at: 2026-10-23T11:07:01Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard*.py, plugin/tests/bench_guard_scripts.py, CHANGELOG.md]
verified: strong
---
# Guard script read: a 37 KB real-shaped script takes ~124 s CPU to parse fully (8427 check_
## Raw request
> Guard script read: a 37 KB real-shaped script takes ~124 s CPU to parse fully (8427 check_bash calls), so any script past a few KB falls to the literal scan. Hot: _mask_fm's per-segment flush tokenizes every segment and realpaths fm per call (35 s), _strip_comments 419k calls (35 s), _heredoc_starts 493k calls (20 s), realpath 669k calls (14 s). Prefilters (no 'fm' in the segment) and memoizing the pure helpers would let more real scripts be fully read inside the 0.2 s box
## Interpretation
The guard reads a script a command runs (bash x.sh, source, ./x) inside a 0.2 s CPU box; past it only a literal scan runs and the script is noted unread. The read costs ~0.16 s per 570-char piece (a 37 KB script: 124 s), so most real scripts over a few KB are never fully read. Make the read faster with every verdict unchanged, so more real scripts are fully read inside the same box.
## Assumptions (confidence)
## Acceptance criteria
- [x] on the public script corpus every script's findings match the old guard's at a large box, and more scripts are fully read inside 0.2 s — verify with `python3 plugin/tests/run.py test_guard test_guard_exec_vectors test_guard_hardening && fm replay`
## Non-goals
## Approach (options → choice → why)
Measure on public system shell scripts (/usr/share, /usr/lib, /usr/bin sh scripts): share fully read inside 0.2 s, total CPU, and each script's findings at a large box (old vs new must match). Options: (1) skip target guessing inside a script read: _check_script drops every guessed finding (they name a $ or 'not known'), so making them is waste (prototype: 2.3x); (2) prefilter _mask_fm's per-segment tokenizing when the segment can't name fm; (3) cache pure text helpers (_strip_comments, _shlex_words) by text; (4) cut the carried 40 state lines (rejected: changes what a piece sees); (5) a bigger box (rejected: a slower hook). Choice: 1-3, each kept only if the corpus findings match exactly.
## Risks and rollback
## Execution prompt
## Steps
1. [x] corpus and harness: share read in the box, findings at a large box
2. [x] no guessing inside a script read, test first
3. [x] the text-helper speedups, each kept only on matching findings
## Resume here
## Docs impact
CHANGELOG line. MASTER's fmguard bullet names no read speed; the box itself is unchanged.
## Verification evidence
- (step 1) `python3 /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/compare_cpu.py /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/base_5.json /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/v2_5.json` → exit 0 · inside 0.5s: 162 -> 183 of 200 / fully read at the large box: 187 -> 194; same findings: 187/187; cpu new/old median 0.74, p90 1.26; total 44.5s -> 15.5s [ran] [tree 30c7f6984bf5] (2026-10-23T11:12:42Z)
- (step 2) `python3 plugin/tests/run.py test_guard_exec_vectors.ScriptReadSpeed` → ✗ exit 1 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: ScriptReadSpeed 0s) / FAILED (1 classes) [ran] [tree cbca13d6bb78] (2026-10-23T11:13:42Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_exec_vectors test_guard_hardening && fm replay` → exit 0 · 4994 new to the corpus / guard cases: 124 labelled, 0 drifted [ran] [tree 587c5094e16b] (2026-10-23T11:14:21Z)
- (step 3) `fm replay --candidate HEAD` → exit 0 · Candidate HEAD on 5000 real commands (32.0 s): 0 loosened, 0 tightened, 0 recategorised, 0 unable [ran] [tree 587c5094e16b] (2026-10-23T11:15:45Z)
- (step 3) `python3 /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/compare_cpu.py /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/base_5.json /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/v3_5.json` → exit 0 · inside 0.5s: 162 -> 190 of 200 / fully read at the large box: 187 -> 198; same findings: 187/187; cpu new/old median 0.37, p90 0.64; total 44.5s -> 7.7s [ran] [tree 587c5094e16b] (2026-10-23T11:16:24Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_exec_vectors test_guard_hardening && fm replay` → exit 0 · 4994 new to the corpus / guard cases: 124 labelled, 0 drifted [ran] [tree 587c5094e16b] (2026-10-23T11:16:48Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_exec_vectors test_guard_hardening && fm replay --candidate HEAD` → exit 0 · OK / Candidate HEAD on 5000 real commands (32.3 s): 0 loosened, 0 tightened, 0 recategorised, 0 unable [ran] [tree a6249dc1bc5f] (2026-10-23T11:18:05Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_exec_vectors test_guard_hardening && fm replay` → exit 0 · 4994 new to the corpus / guard cases: 124 labelled, 0 drifted [ran] [tree 4557f6bfa73e] (2026-10-23T11:18:42Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): each change is an equivalence, checked three ways: helper outputs identical on edge inputs (quotes, $'…', comments after \), findings identical on 187 public scripts read whole by both, verdicts identical on 5000 real commands (fm replay --candidate HEAD) and the 124 labelled cases` → more real scripts are read whole inside the unchanged 0.2 s box (145 -> 182 of 200), with no verdict changed, so fewer scripts fall back to the literal scan [tree 4557f6bfa73e] (2026-10-23T11:18:42Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): each change is an equivalence, checked three ways: helper outputs identical on edge inputs (quotes, $'…', comments after \), findings identical on 187 public scripts read whole by both, verdicts identical on 5000 real commands (fm replay --candidate HEAD) and the 124 labelled cases` → a line ending in \ inside '…' still doesn't join, in "…" and after $'…' it does (as before); a comment never begins right after a \, so a line not ending in \ can't continue; a line without << starts no heredoc (the marker regex needs it); cached tokens come back as a fresh list (a caller's append never reaches the next call); caches hold 256 texts each [tree 4557f6bfa73e] (2026-10-23T11:18:42Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): each change is an equivalence, checked three ways: helper outputs identical on edge inputs (quotes, $'…', comments after \), findings identical on 187 public scripts read whole by both, verdicts identical on 5000 real commands (fm replay --candidate HEAD) and the 124 labelled cases` → the skipped guesses only ever made findings the script reader drops (each names a $ or 'not known'); a python script read at top level still guesses (its findings are kept unfiltered), and one read inside a shell script answers to that script's filter as before; the caches key on the exact text of pure functions, so nothing can seed a wrong answer; the script-verdict cache keys on the guard file's hash, so every cached verdict is read again [tree 4557f6bfa73e] (2026-10-23T11:18:42Z)
## Log
- 2026-10-23T10:51:51Z created
- 2026-10-23T11:06:56Z set tier=M, scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard*.py', 'plugin/tests/bench_guard_scripts.py', 'CHANGELOG.md']
- 2026-10-23T11:07:01Z focused
- 2026-10-23T11:18:53Z done
- 2026-10-23T11:18:55Z committed 843a67f9 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1777 [PERFORMANCE M, done, 2 steps] PreToolUse:Bash:script hook runs at about 90% of its 300 ms budget (p50 271 ms, p95 277 ms — lesson: A latency budget for a time-bo…
- research T-1585-rereview: Changes needed.** I had no shell tool, so I ran nothing and traced the code instead. Each finding below is a trace, not a measured result.
- research T-1473-review: Verdict: changes needed.** I found one regression: a command the old code refused and the new code lets through. I read the code and did not run …
- decision 2026-10-16: T-0275: a script over the guard's parse budget stays allowed after the literal scan, not refused
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Measurements
200 public system shell scripts (/usr/share, /usr/lib, /usr/bin), each read as bash PATH from its folder. Fully read inside the 0.2 s box: 145 -> 182 (inside 0.1 s: 134 -> 169; 0.5 s: 162 -> 190). Full-read CPU over the 187 both versions finish within 5 s: 44.5 s -> 7.7 s (per-script median 0.37x). Same findings on all 187 (and 194/194 between the two prototypes). 5000 real commands, fm replay --candidate HEAD: 0 loosened, 0 tightened, 0 recategorised; 124 labelled cases, 0 drifted. Bench script (12 functions): 2.2 s -> 1.5 s; the 37 KB bench script still exceeds the box (the hook bench budget covers that, T-1777).
## Lessons
- Profile a quadratic parse on a size ladder (2, 4, 8, 12 units): the growth rate tells you whether to hunt a per-item cost or a re-read of everything before it
## Plan gaps
- failed first: step 2 no guessing inside a script read, test first
## Files touched
- plugin/tests/test_guard_exec_vectors.py
- plugin/lib/fmguard.py
- CHANGELOG.md
