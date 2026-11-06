---
id: T-0736
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T18:27:51Z
updated: 2026-10-09T18:36:51Z
base: bbb2da3713c939fa834f82b57a617c5ec9e22262
base_tree: ed9bd32e5ae5276a26044586425022dc727304ef
verified: strong
---
# Not-verified warning at finish fires even when the full suite ran (T-0703: fm check-free r
## Raw request
> not-verified warning at finish fires even when the full suite ran (T-0703: fm check-free run of plugin/tests/run.py covered every file; topic-named tests like test_economics.py aren't linked to fmcost/fmhooks)
## Interpretation
The finish warning 'not verified' counts only tests linked to a file by name, so a passing run of a project gate that covers the file (the full suite, scoped by fm check paths) is ignored: T-0703 and T-0704 both ran python3 plugin/tests/run.py and still got the warning. A passing fm-run of a gate covers the files its paths match (all files when it has none).
## Assumptions (confidence)
## Acceptance criteria
- [x] a passing run of a gate whose paths cover a changed file clears that file from the not-verified warning; files outside the gate's paths still show — verify with `python3 plugin/tests/run.py -p test_verification.py -k NotVerified`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] gate runs count in _not_verified
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_verification.py -k NotVerified` → ✗ exit 1 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: NotVerified 1s) / FAILED (1 classes) [ran] [tree 040150eed9e6] (2026-10-09T18:36:37Z)
- (step 2) `python3 plugin/tests/run.py -p test_verification.py -k NotVerified` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: NotVerified 1s) / OK [ran] [tree 0cf595193dad] (2026-10-09T18:36:44Z)
- (step 1) `python3 plugin/tests/run.py -p test_verification.py -k NotVerified` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: NotVerified 1s) / OK [ran] [tree 0cf595193dad] (2026-10-09T18:36:50Z)
- (ac 1) `python3 plugin/tests/run.py -p test_verification.py -k NotVerified` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: NotVerified 1s) / OK [ran] [tree 0cf595193dad] (2026-10-09T18:36:51Z)
- (audit self) `self: one guard in the shared warning; gates without paths cover every file, gates with paths only their globs; only passing fm-run evidence counts` → no findings [tree 0cf595193dad] (2026-10-09T18:36:51Z)
## Log
- 2026-10-09T18:27:51Z created
- 2026-10-09T18:36:30Z focused
- 2026-10-09T18:36:51Z done
- 2026-10-09T18:36:51Z committed c5d76b3 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- research T-0262-review-1: LOW** — `plugin/lib/fmcore.py:230-239`: the creation-time check is sound. `realpath` plus the `top + os.sep` prefix rejects `../`, absolute pat…
- decision 2026-09-26: User approved (AskUserQuestion, 2026-09-26): once everything is finished and all gates pass, fast-forward main to foreman/build and push both branch…
## Files touched
- plugin/tests/test_verification.py
- plugin/lib/fmcli.py
