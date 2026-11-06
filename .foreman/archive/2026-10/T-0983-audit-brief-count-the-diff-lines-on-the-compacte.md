---
id: T-0983
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T22:26:16Z
updated: 2026-10-15T22:47:49Z
base: 3fe7abd51df68a78794f489a72247d104ce7847f
base_tree: 8478f786db973e88e5a77f95e49605888e8a9789
verified: strong
---
# Audit brief: count the diff lines on the compacted file and, above ~1500 lines, tell the r
## Raw request
> Audit brief: count the diff lines on the compacted file and, above ~1500 lines, tell the reviewer to read it with offset/limit or per file (a 162k-token diff hit Read's cap)
## Interpretation
fm audit prep counted the raw diff's lines, not the compacted file the reviewer reads, and never said a long one won't fit one Read (a 162k-token diff hit the cap).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm audit prep counts the compacted diff's lines and, over 1500, tells the reviewer to read it in parts — verify with `python3 plugin/tests/run.py -k test_long_compacted_diff_tells_the_reviewer_to_read_in_parts`
## Non-goals
## Approach (options → choice → why)
Options: take the fix the recorded demo session made in its clone (count the compacted text; over 1500 lines, tell the reviewer to read it in parts), after review (chosen: real tested work from T-0979's recording); write it again by hand.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Bring in the recorded session's change and its test
## Resume here
## Docs impact
none: the audit brief's own text
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_long_compacted_diff_tells_the_reviewer_to_read_in_parts` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: AuditPrep 1s) / FAILED (1 classes) [ran] [tree 0a5458977613] (2026-10-15T22:47:08Z)
- (step 1) `python3 plugin/tests/run.py -k test_long_compacted_diff_tells_the_reviewer_to_read_in_parts` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: AuditPrep 1s) / OK [ran] [tree 2373481b191e] (2026-10-15T22:47:22Z)
- (ac 1) `python3 plugin/tests/run.py -k test_long_compacted_diff_tells_the_reviewer_to_read_in_parts` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: AuditPrep 1s) / OK [ran] [tree 2373481b191e] (2026-10-15T22:47:47Z)
- (audit self) `self: the recorded demo session's change (T-0979), reviewed and re-applied; red then green` → the brief's line count is the compacted diff's, and past 1500 lines it says to read in parts [tree 2373481b191e] (2026-10-15T22:47:47Z)
## Log
- 2026-10-15T22:26:16Z created
- 2026-10-15T22:46:53Z focused
- 2026-10-15T22:47:48Z done
- 2026-10-15T22:47:49Z committed e061abf (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- T-0723 [PERFORMANCE S, done, 3 steps] Audit diff economy (T-0717: reviewers read 3.2M tokens of .diff in 30 days): fm audit prep
- decision 2026-10-14: [costly] Turned compact output on for the user (fm compact-output on)
- similar finished tasks took 2–3 steps
## Plan gaps
- failed first: step 1 Bring in the recorded session's change and its test
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
