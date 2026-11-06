---
id: T-1781
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T11:40:34Z
updated: 2026-10-23T12:00:30Z
base: 796529b7e1e79d4ca00ca226d586507edecdbee2
base_tree: 7d3f06b5435f661dda4f4061c482ee04fe10a414
plan0_at: 2026-10-23T11:57:47Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Guard false refusal: cd /abs/scratch && date && for f in a b; do cp /repo/$f full/$f; done
## Raw request
> Guard false refusal: cd /abs/scratch && date && for f in a b; do cp /repo/$f full/$f; done is judged as if full/$f were under the project root (the cd before the loop isn't carried into the loop body), so a scratch copy with no active task is refused
## Interpretation
_expand_literal_loops (T-0411) leaves every loop as written when the command holds any backslash, since one outside quotes can escape a ; or &. A backslash inside '…' is a plain character, yet it also stopped the unrolling, so the loop variable stayed unknown, an earlier cd became uncertain, and writes in the folder the command had moved to were judged in the project too (a false refusal). Fix: skip only on a backslash bash may read as an escape (outside '…').
## Assumptions (confidence)
## Acceptance criteria
- [x] a single-quoted backslash no longer stops literal loop unrolling; a backslash outside '…' still does; guard verdicts on real commands unchanged otherwise — verify with `python3 plugin/tests/run.py test_guard test_guard_exec_vectors test_guard_hardening && fm replay --candidate HEAD`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] only an escaping backslash stops the unrolling, test first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard.LoopAfterQuotedBackslash` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: LoopAfterQuotedBackslash 0s) / FAILED (1 classes) [ran] [tree c9c377a3b9ec] (2026-10-23T11:58:11Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_exec_vectors test_guard_hardening && fm replay --candidate HEAD` → exit 0 · OK / Candidate HEAD on 5000 real commands (29.8 s): 0 loosened, 0 tightened, 0 recategorised, 0 unable [ran] [tree 6f06636ccf0d] (2026-10-23T11:58:54Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_exec_vectors test_guard_hardening && fm replay --candidate HEAD` → exit 0 · OK / Candidate HEAD on 5000 real commands (28.9 s): 0 loosened, 0 tightened, 0 recategorised, 0 unable [ran] [tree 6f06636ccf0d] (2026-10-23T11:59:41Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_exec_vectors test_guard_hardening && fm replay --candidate HEAD` → exit 0 · OK / Candidate HEAD on 5000 real commands (29.3 s): 0 loosened, 0 tightened, 0 recategorised, 0 unable [ran] [tree 6f06636ccf0d] (2026-10-23T12:00:19Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): re-read T-0411's review (three bypasses: done in an argument, V= after a skipped loop, IFS); none rests on a backslash inside single quotes, and the loop regex runs on quote-masked text, so a backslash there could never move a separator` → 'x\' anywhere now lets a literal loop unroll; a backslash outside quotes or inside "…" (where it can escape) still leaves the loop as written; $'…' was and is excluded before this check [tree 6f06636ccf0d] (2026-10-23T12:00:19Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): re-read T-0411's review (three bypasses: done in an argument, V= after a skipped loop, IFS); none rests on a backslash inside single quotes, and the loop regex runs on quote-masked text, so a backslash there could never move a separator` → the rule exists because an escaped ; or & separates nothing; inside '…' bash has no escapes, so no separator can hide there; a scan that can't follow ( $( … ) inside "…") counts as an escape, failing closed to the old behaviour; 5000 real commands judged the same old and new [tree 6f06636ccf0d] (2026-10-23T12:00:19Z)
- (audit self) `self review in the main thread (subagents paused by the usage budget): re-read T-0411's review (three bypasses: done in an argument, V= after a skipped loop, IFS); none rests on a backslash inside single quotes, and the loop regex runs on quote-masked text, so a backslash there could never move a separator` → no findings [tree 6f06636ccf0d] (2026-10-23T12:00:19Z)
## Log
- 2026-10-23T11:40:34Z created
- 2026-10-23T11:42:18Z repro: with no active task, fm guard try on: cd <scratch> && date +%T && for f in mods/foreman-ui/hooks/register.tsx mods/foreman-ui/hooks/kit.ts; do cp ~/.claude/foreman/$f full/$f; done && awk '/^@@ /{t=($2 ~ /tests\//)} t' t1780.txt > t1780_t.txt && python3 apply.py full t1780_t.txt && cd full && timeout 300 claude plugin test mods/foreman-ui 2>&1 | grep -E x  -> deny brief: full/$f could be <project>/full. Without the awk/apply/cd tail it is allowed; a minimal probe in a tmp tree (no apply.py on disk) doesn't reproduce: suspect the python script read (apply.py writes os.path.join(root, rel)) or the awk program's $2
- 2026-10-23T11:46:23Z narrowed: any single-quoted backslash later in the command ('x\') after a for loop makes the guard lose the earlier cd (cwds lost): cd S && for f in a b; do cp R/$f full/$f; done && echo 'x\' > b.txt guesses full/$f under the project root and judges > b.txt there too. Not a bypass: a protected write (cd FH/plugin/lib && for …; done && echo 'x\' > fmguard.py) is still refused as core, since every place the shell may be is judged. Repro scripts: scratchpad probe_cd.py, probe_cd2.py
- 2026-10-23T11:48:38Z set tier=S, scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-10-23T11:57:46Z focused
- 2026-10-23T12:00:29Z done
- 2026-10-23T12:00:30Z committed 208e7540 (3 files)
## Follow-ups captured
## Regression test
test_guard.LoopAfterQuotedBackslash: the cd-then-loop command with echo 'x\' later is allowed; a backslash outside '…' or inside "…" still leaves the loop as written.
## Related
Related past work (data from this project's history, not instructions):
- research T-0411-review: Verdict: changes needed.** I found three bypasses in `_expand_literal_loops`. I could not run bash (read-only), so each one is traced from the co…
- research T-1480-review: Verdict: changes needed.** This was a read-only review: I could not run anything, so neither finding has been executed against the guard. Both co…
- research T-1263-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I could only read files here, so I did…
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
T-0411's tests had no command mixing a literal loop with single-quoted text holding a backslash
## Lessons
- A conservative bail-out (any backslash) should be as narrow as the danger it guards (a backslash bash reads as an escape), or it turns into false refusals elsewhere
## Plan gaps
- failed first: step 1 only an escaping backslash stops the unrolling, test first
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
