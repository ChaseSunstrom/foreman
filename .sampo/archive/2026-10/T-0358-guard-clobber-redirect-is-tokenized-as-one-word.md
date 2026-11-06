---
id: T-0358
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-06T05:09:22Z
updated: 2026-10-06T05:13:32Z
base: e4ce90e48d15e18741b171461742aea92a4db45b
base_tree: b81f54c7851207b32dad9b6bd9fe234ca8d8ce2e
verified: strong
---
# Guard: a clobber redirect (>|) is a redirect: its target is checked
## Raw request
> Guard: '>|' (clobber redirect) is tokenized as one word, so its target is never checked: echo x >| ~/.claude/foreman/x passes (T-0355 review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] echo x >| / >|X / 2>| / &>| into Foreman core are refused as core; a plain >| into scratch passes — verify with `python3 plugin/tests/run.py -k test_clobber_redirect`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red) + fix in _split
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -k test_clobber_redirect` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree d0231d16f774] (2026-10-06T05:13:31Z)
- (step 1) `python3 plugin/tests/run.py -k test_clobber_redirect` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree d0231d16f774] (2026-10-06T05:13:31Z)
- (audit adversary) `self (adversary): tokens newly matched by [<>&]+\|? (&| still a separator, <| and >|& bash syntax errors); raw-text parsers checked: _straight_line treats >| as a pipe (conservative), _top/mixed with >| stays correct, _track_vars now skips a >| target too; differential cases vs real bash incl. set -C` → no new allow; replay 0 newly allowed [tree d0231d16f774] (2026-10-06T05:13:31Z)
- (audit edge) `self (adversary): tokens newly matched by [<>&]+\|? (&| still a separator, <| and >|& bash syntax errors); raw-text parsers checked: _straight_line treats >| as a pipe (conservative), _top/mixed with >| stays correct, _track_vars now skips a >| target too; differential cases vs real bash incl. set -C` → >|, >|X, 2>|, &>|, under set -C: tested [tree d0231d16f774] (2026-10-06T05:13:31Z)
- (audit self) `self (adversary): tokens newly matched by [<>&]+\|? (&| still a separator, <| and >|& bash syntax errors); raw-text parsers checked: _straight_line treats >| as a pipe (conservative), _top/mixed with >| stays correct, _track_vars now skips a >| target too; differential cases vs real bash incl. set -C` → no findings [tree d0231d16f774] (2026-10-06T05:13:31Z)
## Log
- 2026-10-06T05:09:22Z created
- 2026-10-06T05:09:51Z planned from capture
- 2026-10-06T05:09:53Z focused
- 2026-10-06T05:13:31Z done
- 2026-10-06T05:13:32Z committed 90604f8 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0161-review: Verdict: changes needed.** `_track_vars` still has bypasses, and one of them is the same class T-0161 set out to close. I traced each through `_s…
- T-0177 [SECURITY M, done, 3 steps] Guard: glob and brace write targets are checked as bash expands them — lesson: A path check is only as good as the path bash will real…
- research T-0120-review: Verdict [stale: mods/foreman-ui/hooks/register.tsx, plugin/lib/fmguard.py changed since it was written]
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- plugin/tests/test_guard_diff.py
