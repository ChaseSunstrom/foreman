---
id: T-0882
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T15:17:11Z
updated: 2026-10-15T15:28:54Z
base: e33690283325c26965ec721b781de6a221bb7abb
base_tree: 74f586d261012793a1bb5539cd42beae1b964f61
verified: strong
---
# CI runs the test suite on push and pull requests (Linux and macOS, Python 3.12 and 3.14)
## Raw request
> CI runs the test suite on push and pull requests (Linux and macOS, Python 3.12 and 3.14)
## Interpretation
Round-4 deferred item T-0865: tests run only on this machine today; a push or PR should run the suite on Linux and macOS so a contributor sees breakage. The suite must not need claude installed (CI has none), and the e2e roundtrip that calls claude stays out of CI.
## Assumptions (confidence)
## Acceptance criteria
- [x] the suite passes with no claude on PATH — verify with `bash -c 'S=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/noclaude; test -d $S && PATH=$S python3 plugin/tests/run.py'`
## Non-goals
## Approach (options → choice → why)
1) GitHub Actions workflow running plugin/tests/run.py on ubuntu and macOS (chosen: zero deps, PRs show it). 2) Makefile target plus workflow (extra file, nothing gained). 3) Local pre-push hook (one machine only; Foreman already gates commits). Complete version: OS x Python matrix (3.12 minimum, 3.14 newest), suite with no claude on PATH, fm doctor smoke skipped (needs an install), e2e roundtrip skipped (needs claude).
## Risks and rollback
## Execution prompt
## Steps
1. [x] dry-run the suite with claude off PATH; fix what assumes it
2. [x] write .github/workflows/test.yml
## Resume here
## Docs impact
README badge
## Verification evidence
- (step 1) `env -i PATH=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/noclaude HOME=~ USER=chase LOGNAME=chase LANG=C.UTF-8 python3 plugin/tests/run.py` → exit 0 · Ran 1348 tests in 71.5s (446 classes, 16 at a time; slowest: Stop 46s, TaskLifecycle 25s, Recall 24s) / OK [ran] [tree fcbfbc88ad26] (2026-10-15T15:27:27Z)
- (step 2) `uv run --no-project --with pyyaml python -c "import yaml; d=yaml.safe_load(open('.github/workflows/test.yml')); j=d['jobs']['test']; assert 'plugin/tests/run.py' in j['steps'][-1]['run'] and d['permissions']=={'contents':'read'}; print('workflow ok')"` → exit 0 · workflow ok [ran] [tree fcbfbc88ad26] (2026-10-15T15:27:27Z)
- (ac 1) `bash -c 'S=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/noclaude; test -d $S && PATH=$S python3 plugin/tests/run.py'` → exit 0 · Ran 1348 tests in 73.8s (446 classes, 16 at a time; slowest: Stop 49s, TaskLifecycle 29s, Bench 26s) / OK [ran] [tree fcbfbc88ad26] (2026-10-15T15:28:53Z)
- (audit intent) `self review: workflow uses no untrusted event input, contents:read only, pinned major action versions; suite verified with no claude on PATH under Python 3.12.14 (uv, 1348 OK) and 3.14 (1348 OK, minimal env); a HOME that isn't the passwd home fails 16 guard tests (captured T-0883; GitHub runners match)` → a push or PR runs the whole suite on Linux (3.12, 3.14) and reports macOS; it needs no claude, matching the deferred T-0865's precondition (dry-run without claude: passed) [tree fcbfbc88ad26] (2026-10-15T15:28:53Z)
- (audit operator) `self review: workflow uses no untrusted event input, contents:read only, pinned major action versions; suite verified with no claude on PATH under Python 3.12.14 (uv, 1348 OK) and 3.14 (1348 OK, minimal env); a HOME that isn't the passwd home fails 16 guard tests (captured T-0883; GitHub runners match)` → macOS leg is continue-on-error until it has run green once; git identity set in the workflow for the tests' commits; e2e roundtrip and hook bench stay local (need claude / a quiet machine) [tree fcbfbc88ad26] (2026-10-15T15:28:53Z)
## Log
- 2026-10-15T15:17:11Z created
- 2026-10-15T15:17:18Z focused
- 2026-10-15T15:28:53Z done
- 2026-10-15T15:28:54Z committed b078702 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261015-083935.pack: can you keep going? super super improve? recursively? genuinely, make it THE plugin, everything, etc. [stale: plugin/tests/e2e/rou…
- research mission-20261014-103352.pack: super improve foreman, integrate better with new CC features, super improve, smarter, faster, better, more capable, etc. etc. etc.…
- T-0319 [FIX M, done, 4 steps] install.sh installs a Python Foreman supports on each platform — lesson: Test the floor, not the dev box: a suite written on 3.14 hid three…
- decision 2026-10-06: [revisit: when install.sh changes @5949c14dbec6] Foreman Desktop releases build Linux and macOS only, no Windows
- the similar finished task took 4 steps
## Lessons
- Simulating CI with a fake HOME breaks tests that compare $HOME to the passwd home; simulate with env -i and the real user, then vary one thing at a time
## Files touched
- .github/workflows/test.yml
- README.md
