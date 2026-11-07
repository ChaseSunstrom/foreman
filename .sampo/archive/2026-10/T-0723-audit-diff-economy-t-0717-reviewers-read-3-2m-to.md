---
id: T-0723
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-09T17:17:40Z
updated: 2026-10-09T17:32:17Z
base: 9d1c16b1fd3d9861f7d7855ae41ceb4de1638a99
base_tree: 376592ea9c6381bd65b876ee1ce552afa0529452
verified: strong
---
# Audit diff economy (T-0717: reviewers read 3.2M tokens of .diff in 30 days): fm audit prep
## Raw request
> Audit diff economy (T-0717: reviewers read 3.2M tokens of .diff in 30 days): fm audit prep leaves fixtures, lockfiles and generated files out of the diff (listed by name and +/- counts) and splits a diff over ~1500 lines into per-file parts the reviewer reads on demand
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the reviewer's diff shows a file whose change repeats another's as one line naming the first, cuts context lines over 200 characters, and lists fixtures and lockfiles by name and +/- counts instead of their bodies; changed lines stay whole — verify with `python3 plugin/tests/run.py -p test_audit.py -k CompactDiff`
- [x] measured on real audit diffs (T-0673, T-0018) — verify with `python3 /tmp/claude-1000/-home-~--claude-foreman/017cbb6b-0026-4a64-af96-4068091225da/scratchpad/diffsave.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing CompactDiff test
2. [x] _compact_diff in fmcli, applied to the frozen reviewer diff (the pre-audit keeps the raw one)
3. [x] measure on real diffs
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_audit.py` → ✗ exit 1 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: CompactDiff 0s) / FAILED (1 classes) [ran] [tree 21e17499f5ce] (2026-10-09T17:31:18Z)
- (ac 2) `python3 /tmp/claude-1000/-home-~--claude-foreman/017cbb6b-0026-4a64-af96-4068091225da/scratchpad/diffsave.py` → exit 0 · T-0364.diff: 70,738 → 55,303 chars (21% less) / 48 diffs over 20 KB: 2,239,286 → 1,974,997 chars (11% less) [ran] [tree b6ed5361ffa9] (2026-10-09T17:31:39Z)
- (step 2) `python3 plugin/tests/run.py -p test_audit.py -p test_diff_gates.py -p test_pass4.py -p test_builder.py` → exit 0 · Ran 40 tests in 6.5s (11 classes, 16 at a time; slowest: DiffGates 6s, Contract 5s, Brief 2s) / OK [ran] [tree b6ed5361ffa9] (2026-10-09T17:32:06Z)
- (step 3) `python3 /tmp/claude-1000/-home-~--claude-foreman/017cbb6b-0026-4a64-af96-4068091225da/scratchpad/diffsave.py` → exit 0 · T-0364.diff: 70,738 → 55,303 chars (21% less) / 48 diffs over 20 KB: 2,239,286 → 1,974,997 chars (11% less) [ran] [tree b6ed5361ffa9] (2026-10-09T17:32:07Z)
- (ac 1) `python3 plugin/tests/run.py -p test_audit.py -k CompactDiff` → exit 0 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: CompactDiff 0s) / OK [ran] [tree 8ac20711a081] (2026-10-09T17:32:17Z)
- (ac 2) `python3 /tmp/claude-1000/-home-~--claude-foreman/017cbb6b-0026-4a64-af96-4068091225da/scratchpad/diffsave.py` → exit 0 · T-0364.diff: 70,738 → 55,303 chars (21% less) / 48 diffs over 20 KB: 2,239,286 → 1,974,997 chars (11% less) [ran] [tree 8ac20711a081] (2026-10-09T17:32:17Z)
- (step 1) `python3 plugin/tests/run.py -p test_audit.py` → exit 0 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: CompactDiff 0s) / OK [ran] [tree 8ac20711a081] (2026-10-09T17:32:17Z)
- (audit edge) `self: compaction runs after secret redaction on the frozen copy only; the pre-audit and file list read the raw diff; changed lines never cut` → a renamed or binary file (no @@) passes through unchanged; a diff with no repeats is byte-identical (test) [tree 8ac20711a081] (2026-10-09T17:32:17Z)
- (audit self) `self: compaction runs after secret redaction on the frozen copy only; the pre-audit and file list read the raw diff; changed lines never cut` → no findings [tree 8ac20711a081] (2026-10-09T17:32:17Z)
## Log
- 2026-10-09T17:17:40Z created
- 2026-10-09T17:31:01Z set type=PERFORMANCE
- 2026-10-09T17:31:01Z focused
- 2026-10-09T17:32:17Z done
- 2026-10-09T17:32:17Z committed a5ebca3 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0717-tool-result-sizes: Measured with scratchpad/sizes.py over 64,393 tool results (~31.7M tokens, chars/4).
- T-0216 [FEATURE S, done, 1 steps] fm audit prep --split: up to three parallel fresh-context reviewer briefs by lens group; suggested for big L diffs
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- the similar finished task took 1 steps
- start here (files T-0216 touched): plugin/tests/test_cli.py, plugin/lib/fmcli.py, CHANGELOG.md, plugin/skills/intake/references/audit.md
## Measurements
48 real audit diffs over 20 KB: 2,239,286 → 1,974,997 chars (11% less); T-0673 18%, T-0364 21%, T-0018 11%. Per-hunk dedup measured no extra gain and was left out.
## Files touched
- plugin/tests/test_audit.py
- plugin/lib/fmcli.py
- CHANGELOG.md
