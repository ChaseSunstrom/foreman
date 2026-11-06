---
id: T-0355
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-06T04:57:15Z
updated: 2026-10-06T05:09:27Z
base: 4bb88bdd2cc8b4ea114b56687e1fb330db2b6ae4
base_tree: 822250fc36aab3c8cd3e24b4b6769b0e13984e63
verified: strong
---
# Guard: a cd heading an && chain stays certain when later elements have pipes (a piped cd never is)
## Raw request
> Guard: in _prefix_vars' non-skippable branch a prefix mixing ; and && (S=/p; curl -o $S/x && A … | cat) fails _straight_line, so S stays unknown; test _straight_line(prefix.replace('&&',';')) or use the sure-elements loop there too (recon rsi-20261006b)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] cd <dir> && … && a | b && tar xf - (then ; more) judges the tar in <dir>; a cd inside a pipeline (cd /x | true && tar xf -) leaves the old folder possible — verify with `python3 plugin/tests/run.py -k test_guard.KnownVars`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red) + fix
## Resume here
<!-- auto -->
- 2026-10-06T05:04:08Z step 1/1: test (red) + fix
- git: foreman/build; 4 uncommitted: CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py
- touched since last checkpoint: plugin/tests/test_guard_diff.py, CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guard.KnownVars` → exit 0 · Ran 4 tests in 0.2s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree 52faa8b20d5e] (2026-10-06T04:58:54Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard.KnownVars` → ✗ exit 1 · Ran 4 tests in 0.2s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) [ran] [tree 17a70628d2f4] (2026-10-06T04:59:45Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard.KnownVars` → ✗ exit 1 · Ran 4 tests in 0.2s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) [ran] [tree 1485a5c917e8] (2026-10-06T04:59:54Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard.KnownVars` → exit 0 · Ran 4 tests in 0.2s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree 2307fe8ba6bb] (2026-10-06T05:02:47Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guard.KnownVars` → exit 0 · Ran 4 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree b81f54c78512] (2026-10-06T05:09:26Z)
- (audit adversary) `adversary pass (fm-reviewer): newline-continued pipe hid a piped cd, fixed test-first in _split; an automated review's wget -O override fixed with it; differential tests vs real bash extended` → 1 HIGH (newline after | dropped the pipe) fixed + tested; clobber >| pre-existing, captured T-0358 [tree b81f54c78512] (2026-10-06T05:09:26Z)
- (audit edge) `adversary pass (fm-reviewer): newline-continued pipe hid a piped cd, fixed test-first in _split; an automated review's wget -O override fixed with it; differential tests vs real bash extended` → pipes in && segments, piped cd, |& and ||, newline after | && ||, wget -O last-wins: all tested [tree b81f54c78512] (2026-10-06T05:09:26Z)
- (audit self) `adversary pass (fm-reviewer): newline-continued pipe hid a piped cd, fixed test-first in _split; an automated review's wget -O override fixed with it; differential tests vs real bash extended` → no findings [tree b81f54c78512] (2026-10-06T05:09:26Z)
## Log
- 2026-10-06T04:57:15Z created
- 2026-10-06T04:58:50Z planned from capture
- 2026-10-06T04:58:51Z focused
- 2026-10-06T04:59:36Z set title=Guard: a cd heading an && chain stays certain when later elements have pipes (a piped cd never is)
- 2026-10-06T04:59:36Z criterion 1 text: S=/tmp/x; true && curl -so $S/a URL && ls | head resolves S (no brief block), while false && S=/x; rm $S/a still blocks → cd <dir> && … && a | b && tar xf - (then ; more) judges the tar in <dir>; a cd inside a pipeline (cd /x | true && tar xf -) leaves the old folder possible
- 2026-10-06T05:04:08Z scope: wget -O hole from the automated review of T-0354 fixed here (same file, test-first)
- 2026-10-06T05:09:27Z done
- 2026-10-06T05:09:27Z committed e4ce90e (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261006b: 1. **Answer.** I found three grounded findings, one for each of your frictions. For friction (1) I traced the code path but did not run a reprodu…
- research T-0339-review: Verdict: changes needed.** I found one high-severity bypass. I traced it by reading the code and could not run it, because this session has no ex…
- T-0190 [FIX M, done, 3 steps] Guard: guesses never use a variable's own name; rm targets use literals set once before a branch — lesson: A replay gate turns a guard chan…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/test_guard_diff.py
- CHANGELOG.md
