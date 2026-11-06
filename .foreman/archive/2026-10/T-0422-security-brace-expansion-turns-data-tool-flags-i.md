---
id: T-0422
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: [T-0414]
source: discovered
created: 2026-10-09T13:57:52Z
updated: 2026-10-09T14:08:35Z
base: df9d352930915cf2cdde0429368def670e699d6e
base_tree: 661006ac7dd9abff54241e70ffd0d5e50c7cfb7c
verified: strong
---
# Guard: brace expansion can't turn a data tool's flag into a write
## Raw request
> SECURITY: brace expansion turns data-tool flags into writes (T-0414 builder): curl -s {-o,json.py} URL and wget -qO- URL {-O,json.py} pass _writes_nothing, but bash expands them to -o json.py / -O json.py
## Interpretation
_writes_nothing reads curl/wget words as written; bash expands {-o,json.py} to -o json.py, so curl -s {-o,json.py} URL writes a file python then imports (T-0414 builder).
## Assumptions (confidence)
## Acceptance criteria
- [x] curl -s {-o,json.py} URL | python3 -c … and wget -qO- URL {-O,json.py} | python3 -c … refuse; plain curl -s URL | python3 -c 'json.load…' still passes — verify with `python3 plugin/tests/run.py -k test_braces_never_hide_a_write`
## Non-goals
## Approach (options → choice → why)
(A, chosen) _writes_nothing refuses any word with an unquoted brace expansion ({a,b} or {a..b}); (B, rejected) expand braces in the guard: bash's rules (nesting, quoting, sequences) for no gain on a data-tool line.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: unit + real-bash rows
2. [x] refuse brace words in _writes_nothing
3. [x] replay, gate, ship
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_braces_never_hide_a_write` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Braces 0s) / FAILED (1 classes) [ran] [tree cfbbea4b5c2a] (2026-10-09T13:59:11Z)
- (step 2) `python3 plugin/tests/run.py -k test_braces_never_hide_a_write` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Braces 0s) / OK [ran] [tree 8bbef92ceb2a] (2026-10-09T14:05:02Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 14:06 UTC) [ran] [tree 80129685eaba] (2026-10-09T14:08:15Z)
- (ac 1) `python3 plugin/tests/run.py -k test_braces_never_hide_a_write` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Braces 0s) / OK [ran] [tree 80129685eaba] (2026-10-09T14:08:30Z)
- (audit adversary) `red→green unit rows + real-bash EXTRA rows; full gate exit 0 with replay 0 newly allowed; committed with T-0414 (4328aa2, shared fmguard.py)` → the reported forms refuse in unit and real-bash rows; the data-python and jq forms still pass [tree 80129685eaba] (2026-10-09T14:08:30Z)
- (audit edge) `red→green unit rows + real-bash EXTRA rows; full gate exit 0 with replay 0 newly allowed; committed with T-0414 (4328aa2, shared fmguard.py)` → conservative by design (a fetcher anywhere / any brace word) — a rare false refusal over a silent pass [tree 80129685eaba] (2026-10-09T14:08:30Z)
- (audit intent) `red→green unit rows + real-bash EXTRA rows; full gate exit 0 with replay 0 newly allowed; committed with T-0414 (4328aa2, shared fmguard.py)` → closes the hole the T-0414 builder reported, nothing wider [tree 80129685eaba] (2026-10-09T14:08:35Z)
- (audit adversary) `red→green unit rows + real-bash EXTRA rows; full gate exit 0 with replay 0 newly allowed; committed with T-0414 (4328aa2, shared fmguard.py)` → the reported forms refuse in unit and real-bash rows; the data-python and jq forms still pass [tree 80129685eaba] (2026-10-09T14:08:35Z)
- (audit edge) `red→green unit rows + real-bash EXTRA rows; full gate exit 0 with replay 0 newly allowed; committed with T-0414 (4328aa2, shared fmguard.py)` → conservative by design (a fetcher anywhere / any brace word): a rare false refusal over a silent pass [tree 80129685eaba] (2026-10-09T14:08:35Z)
## Log
- 2026-10-09T13:57:52Z created
- 2026-10-09T13:58:32Z planned from capture
- 2026-10-09T13:59:17Z set depends_on=['T-0414']
- 2026-10-09T13:59:17Z waits on T-0414's merge: T-0414 rewrote _writes_nothing
- 2026-10-09T14:04:53Z focused
- 2026-10-09T14:08:15Z paused: focus moved to T-0414
- 2026-10-09T14:08:30Z focused
- 2026-10-09T14:08:34Z paused: focus moved to T-0421
- 2026-10-09T14:08:35Z focused
- 2026-10-09T14:08:35Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0397 [FIX S, done, 1 steps] Guard: curl -m/--max-time and nvidia-smi beside a data-reading python -c count as writing files (JARVIS: curl -s -m 5 127.0.0.1:9000/runnin…
- T-0177 [SECURITY M, done, 3 steps] Guard: glob and brace write targets are checked as bash expands them — lesson: A path check is only as good as the path bash will real…
- research T-0344-review: Verdict: changes needed.** I had no shell, so these are traced by reading `plugin/lib/fmguard.py` and the tests. I did not run any command. [stal…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 1–3 steps
## Lessons
- Check the property (a download reaches a shell; a word may expand) rather than the shape of one line.
## Files touched
- plugin/lib/fmguard.py
- plugin/tests/test_guard_diff.py
- CHANGELOG.md
