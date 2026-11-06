---
id: T-2132
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T09:54:46Z
updated: 2026-10-31T01:28:30Z
base: e973d8bee9ad48914a0a64db4557366a670339da
base_tree: a7e70d742a237123ab1e10fe836e7e8e5fb25893
plan0_at: 2026-10-31T01:14:52Z
plan0_scope: []
verified: strong
---
# fm find rank: feed proof (a failing test from T-2122) and effort (hunk estimate) into…
## Raw request
> fm find rank: feed proof (a failing test from T-2122) and effort (hunk estimate) into the score; both fixed at 1 today (T-2125 ceiling)
## Interpretation
fm find --rank scores severity x reach x finder precision; proof and effort are fixed at 1 (T-2125's ponytail). fm prove (T-2122, T-2199) now proves leads on a throwaway copy, and each lead's function has a known size, so both can feed the score: a proven lead outranks an unproven one of the same kind, and a small fix outranks a large one of equal value.
## Assumptions (confidence)
## Acceptance criteria
- [x] end to end: after fm prove proves a lead on a trusted tree, fm find --rank scores it 1.25x until its function changes (an edit elsewhere in the file keeps it); a small function's lead ranks above an equal one in a 200-line function; a proven lead never passes an unproven lead of a higher-severity kind — verify with `cd plugin/tests && python3 -m unittest -q test_find.FindRankValue`
## Non-goals
## Approach (options → choice → why)
Revised after fm second plan (verdict revise). (1) fm prove records each proven lead in the project's state dir (p.dir/find-proofs.json, written only by fm prove through write_atomic; the guard treats the state dir as fm-only), keyed by fm find's find_key, with the hash of the lead's enclosing function's text (the whole line for a lead with no function), so an edit elsewhere in the file keeps the proof and a change to that function drops it. (2) rank multiplies a still-matching proof by PROOF = 1.25 and every lead by an effort factor max(0.5, 1 - span/320) from its enclosing function's line span (1.0 at 0 lines, 0.75 at 80, 0.5 at 160+; 1.0 with no enclosing function, as for docs, dep and secret leads). With SEVERITY's spacing, a proven lead never passes an unproven lead of a higher-severity kind (asserted). (3) No state file: scores change only by the effort factor; T-2125's 'proof and effort are 1' note is replaced. Rejected: running fm prove inside rank (runs repo code), a whole-file hash (drops proofs on any edit), a model's effort estimate (a call per lead, untestable).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests (FindRankValue): proven key lifts until the file's hash changes; effort factor by function span
2. [x] fm prove writes the proven-keys state; rank reads it and the def spans
3. [x] docs (MASTER fmfind, CHANGELOG)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindRankValue 2>&1 | tail -4` → ✗ exit 1 · Ran 4 tests in 0.545s / FAILED (failures=2, errors=2) [ran] [tree 16af1986bf07] (2026-10-31T01:16:16Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindRankValue 2>&1 | tail -15` → ✗ exit 1 · Ran 4 tests in 0.391s / FAILED (failures=1) [ran] [tree a317612c5539] (2026-10-31T01:16:44Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindRankValue` → ✗ exit 1 · Ran 7 tests in 0.883s / FAILED (failures=2, errors=4) (start tree + this task's tests) [ran] [tree f2d8948b52f3] (2026-10-31T01:26:20Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindRankValue` → exit 0 · Ran 7 tests in 0.778s / OK [ran] [tree f2d8948b52f3] (2026-10-31T01:26:20Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 52 tests in 27.746s / OK [ran] [tree f2d8948b52f3] (2026-10-31T01:26:56Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 52 tests in 29.047s / OK [ran] [tree f2d8948b52f3] (2026-10-31T01:27:26Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 52 tests in 19.174s / OK [ran] [tree f2d8948b52f3] (2026-10-31T01:27:45Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindRankValue` → exit 0 · Ran 7 tests in 0.471s / OK [ran] [tree 6418fef4289b] (2026-10-31T01:27:58Z)
- (audit intent) `fm-reviewer intent+adversary+edge+maintainer on the branch; fixed in 7cce27a8: span hashes cached per def (5000 leads in one function rank under 2 s), the cap now holds with unequal reach/precision/effort (0.98x the lowest unproven score of each more severe kind), no lift for a file with no text, twin keys in scan order in prove, realpath keys, record under c.lock in its own try, trailing blank rows ignored; test_find 52 green, red-to-green proven` → a proven lead lifts until its own function changes and a small function's lead outranks an equal one in a long function [tree 6418fef4289b] (2026-10-31T01:27:58Z)
- (audit adversary) `fm-reviewer intent+adversary+edge+maintainer on the branch; fixed in 7cce27a8: span hashes cached per def (5000 leads in one function rank under 2 s), the cap now holds with unequal reach/precision/effort (0.98x the lowest unproven score of each more severe kind), no lift for a file with no text, twin keys in scan order in prove, realpath keys, record under c.lock in its own try, trailing blank rows ignored; test_find 52 green, red-to-green proven` → find-proofs.json lives in the state dir, written atomically under a lock by fm prove only; repo text is parsed, never run; a hostile file with thousands of leads in one def stays linear [tree 6418fef4289b] (2026-10-31T01:27:58Z)
- (audit edge) `fm-reviewer intent+adversary+edge+maintainer on the branch; fixed in 7cce27a8: span hashes cached per def (5000 leads in one function rank under 2 s), the cap now holds with unequal reach/precision/effort (0.98x the lowest unproven score of each more severe kind), no lift for a file with no text, twin keys in scan order in prove, realpath keys, record under c.lock in its own try, trailing blank rows ignored; test_find 52 green, red-to-green proven` → unequal reach can't carry a proven lead past a more severe unproven one; a generated file's lead gets no lift; blank lines between functions keep a proof [tree 6418fef4289b] (2026-10-31T01:27:58Z)
- (audit maintainer) `fm-reviewer intent+adversary+edge+maintainer on the branch; fixed in 7cce27a8: span hashes cached per def (5000 leads in one function rank under 2 s), the cap now holds with unequal reach/precision/effort (0.98x the lowest unproven score of each more severe kind), no lift for a file with no text, twin keys in scan order in prove, realpath keys, record under c.lock in its own try, trailing blank rows ignored; test_find 52 green, red-to-green proven` → one cap rule replaces the per-kind table; the twin-key mismatch with fm find --capture is captured as T-2250 [tree 6418fef4289b] (2026-10-31T01:27:58Z)
## Log
- 2026-10-30T09:54:46Z created
- 2026-10-31T00:57:00Z planned: it has criteria and steps
- 2026-10-31T00:57:00Z set approved=True
- 2026-10-31T01:02:21Z criterion 1 text: a lead fm prove proved ranks above the same kind of unproven lead until its file changes, and a small function's lead ranks above an equal one in a 200-line function → end to end: after fm prove proves a lead on a trusted tree, fm find --rank scores it 1.25x until its function changes (an edit elsewhere in the file keeps it); a small function's lead ranks above an equal one in a 200-line function; a proven lead never passes an unproven lead of a higher-severity kind
- 2026-10-31T01:02:21Z fm second plan: revise; plan revised (state in p.dir written only by fm prove, per-function hash, PROOF 1.25, effort curve max(0.5, 1 - span/320), severity order asserted, end-to-end criterion)
- 2026-10-31T01:14:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2132.builder.md
- 2026-10-31T01:14:51Z focused
- 2026-10-31T01:26:08Z merged worktree-agent-a29837c7d0b816446 (4 file(s))
- 2026-10-31T01:26:08Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a29837c7d0b816446
- 2026-10-31T01:26:16Z focused
- 2026-10-31T01:27:58Z scope: fmfind (rank, proofs state, spans), fmprove (record after a proof), test_find, docs
- 2026-10-31T01:28:21Z done
- 2026-10-31T01:28:30Z guard authorization added: publish
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The acceptance criterion only proves the unit-level behavior in `FindRankValue`. It doesn't show that `fm prove` actually writes the state that rank later reads. Step 2 can be wired wrong (key format mismatch between writer and reader, wrong path, wrong hash input) and the tests still pass if…
- HIGH: Staleness is keyed to the file's content hash, but a proof is about a specific lead in a specific function. Any unrelated edit anywhere in the file (a comment, an import) drops the proof, and a fix that makes the test pass also changes the hash, which is fine. The opposite failure is worse: t…
- MEDIUM: The state file is "written only by fm verbs", but rank trusts it. If it lives in the repo working tree or is user-writable, a stale, hand-edited or merged file can silently inflate scores. A repo-controlled file can also be committed by someone else. — Say where it lives (outside the tracke…
- MEDIUM: The effort factor is described only at its endpoints ("1 for small, down to 0.5 for 160+ lines"). The curve between them, the thresholds, and how the span is computed for languages or leads with no enclosing function (module-level code, config, non-code files) are unspecified. The test "200…
- MEDIUM: The proof of 1.5 and the 0.5 floor are magic numbers, and combined with the existing severity x reach x precision they could reorder existing results in ways the user doesn't expect, for example a proven low-severity lead beating an unproven high-severity one. The criterion says "same kind"…
- LOW: Step 1 is a red test with no mention of how the old fixed-at-1 behavior is regression-tested, and the docs step doesn't mention removing the T-2125 "ceiling" note. — Add a check that with no state file, scores equal the pre-change values, and update or remove the T-2125 ceiling wording in the …
Verdict: revise — the approach is sound, but the criterion doesn't prove the writer and reader agree, and the staleness, failure, and effort-curve semantics need pinning down before the red tests are written.
## Dissent
- [ ] HIGH: The acceptance criterion only proves the unit-level behavior in `FindRankValue`. It doesn't show that `fm prove` actually writes the state that rank later reads. Step 2 can be wired wrong (key format mismatch between writer and reader, wrong path, wrong hash input) and the tests still pass if…
- [ ] HIGH: Staleness is keyed to the file's content hash, but a proof is about a specific lead in a specific function. Any unrelated edit anywhere in the file (a comment, an import) drops the proof, and a fix that makes the test pass also changes the hash, which is fine. The opposite failure is worse: t…
- [ ] MEDIUM: The state file is "written only by fm verbs", but rank trusts it. If it lives in the repo working tree or is user-writable, a stale, hand-edited or merged file can silently inflate scores. A repo-controlled file can also be committed by someone else. — Say where it lives (outside the tracke…
- [ ] MEDIUM: The effort factor is described only at its endpoints ("1 for small, down to 0.5 for 160+ lines"). The curve between them, the thresholds, and how the span is computed for languages or leads with no enclosing function (module-level code, config, non-code files) are unspecified. The test "200…
- [ ] MEDIUM: The proof of 1.5 and the 0.5 floor are magic numbers, and combined with the existing severity x reach x precision they could reorder existing results in ways the user doesn't expect, for example a proven low-severity lead beating an unproven high-severity one. The criterion says "same kind"…
- [ ] LOW: Step 1 is a red test with no mention of how the old fixed-at-1 behavior is regression-tested, and the docs step doesn't mention removing the T-2125 "ceiling" note. — Add a check that with no state file, scores equal the pre-change values, and update or remove the T-2125 ceiling wording in the …
## Related
Related past work (data from this project's history, not instructions):
- T-2125 [FEATURE M, done, 3 steps] Value ranking: severity x proof x reach / effort, per-finder precision from outcomes, a mute floor, abstain below a threshold (Mission …
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-30: Proven kinds (dep, docs, secret) file without a cold re-run; scout never refiles a regression
- similar finished tasks took 2–3 steps
## Lessons
- An invariant stated over one factor (severity) breaks once other factors multiply in; test it with the other factors unequal
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmfind.py
- plugin/lib/fmprove.py
- MASTER.md
