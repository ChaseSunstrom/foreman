---
id: T-0319
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T00:42:32Z
updated: 2026-10-06T01:00:24Z
base: 953c8a79bbb213cd3bb92724857aab49825fff59
base_tree: 3044e8450032b17894914c8737d0d0235dc23da5
verified: strong
---
# install.sh installs a Python Foreman supports on each platform
## Raw request
> install.sh installs a Python Foreman supports on each platform
## Interpretation
The user wants install.sh to leave every supported platform (Linux distros, macOS, WSL) with a python3 Foreman actually runs on. Foreman says 'Python 3 stdlib' but was only ever tested on 3.14: below 3.13 the suite fails (closed-stdin communicate on <3.13, a backslash f-string on <3.12, tomllib on <3.11, argparse optional-positional handling on older patch releases). Native Windows is out (fmcore needs fcntl): say WSL.
## Assumptions (confidence)
## Acceptance criteria
- [x] install.sh ensures python3 meets Foreman's floor (brew on macOS, uv elsewhere, WSL note on native Windows) — verify with `python3 plugin/tests/run.py -k Install`
- [x] fm doctor reports a python3 below the floor — verify with `python3 plugin/tests/run.py -k Doctor`
- [x] the suite passes on the floor Python — verify with `uv run --no-project --python 3.12 python plugin/tests/run.py`
## Non-goals
## Approach (options → choice → why)
Options: (A) lower the floor to what distros ship (3.9 for macOS/RHEL) by patching every compat break, then only use the OS package manager; (B) pick the lowest floor reachable with small fixes (closed-stdin communicate is a 2-line fix → 3.12 if argparse holds there), and have install.sh install a newer python only when python3 is missing or below it: brew on macOS, uv (python-build-standalone, no sudo, python3 into ~/.local/bin, which the Claude Code installer already puts on PATH) elsewhere. Choice: B. Why: A keeps a 3.9 compat burden in a codebase written on 3.14 with no gate guarding it; B gives one uniform path and stays honest via a doctor check and a floor-version suite run as the criterion.
## Risks and rollback
## Execution prompt
## Steps
1. [x] find the real floor (tests under 3.9–3.13)
2. [x] fix what breaks on the floor version
3. [x] install.sh: ensure python per platform + test
4. [x] fm doctor floor check + README requirement
## Resume here
## Docs impact
README install requirements; CHANGELOG entry
## Verification evidence
- (step 1) `cd /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad && for v in 3.12.3 3.12.7 3.13.0 3.13.1; do uv run -q --no-project --python $v python ap.py 2>&1 | tail -1; done` → exit 0 · ap.py: error: unrecognized arguments: pytest ok / 3.13.1 Namespace(c='ev', id='T-1', cmd='pytest', result='ok', ac='1') [ran] [tree 3044e8450032] (2026-10-06T00:44:07Z)
- (ac 3) `uv run -q --no-project --python 3.12 python plugin/tests/run.py` → ✗ exit 1 · Ran 824 tests in 24.7s (203 classes, 16 at a time; slowest: Stop 16s, Parallel 16s, TaskLifecycle 15s) / FAILED (11 classes) [ran] [tree 3044e8450032] (2026-10-06T00:44:32Z)
- (step 2) `PATH=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/py3127:$PATH python3 plugin/tests/run.py` → ✗ exit 1 · Ran 824 tests in 59.6s (203 classes, 16 at a time; slowest: Stop 44s, TaskLifecycle 34s, Bench 34s) / FAILED (1 classes) [ran] [tree 86045a714c78] (2026-10-06T00:49:22Z)
- (ac 3) `uv run -q --no-project --python 3.12 python plugin/tests/run.py` → exit 0 · Ran 824 tests in 55.7s (203 classes, 16 at a time; slowest: Stop 41s, TaskLifecycle 33s, Bench 31s) / OK [ran] [tree 86045a714c78] (2026-10-06T00:50:19Z)
- (step 3) `python3 plugin/tests/run.py -k InstallScript` → ✗ exit 1 · Ran 6 tests in 0.4s (1 classes, 16 at a time; slowest: InstallScript 0s) / FAILED (1 classes) [ran] [tree 0408eced10b5] (2026-10-06T00:53:42Z)
- (step 3) `python3 plugin/tests/run.py -k InstallScript` → exit 0 · Ran 6 tests in 0.5s (1 classes, 16 at a time; slowest: InstallScript 0s) / OK [ran] [tree aad14156bd32] (2026-10-06T00:53:51Z)
- (step 4) `python3 plugin/tests/run.py -k Doctor` → ✗ exit 1 · Ran 0 tests in 0.1s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree 88df3ca5a2f6] (2026-10-06T00:54:06Z)
- (step 4) `python3 plugin/tests/run.py -k test_doctor` → ✗ exit 1 · Ran 23 tests in 8.1s (7 classes, 16 at a time; slowest: Command 8s, RestoreState 0s, Checks 0s) / FAILED (1 classes) [ran] [tree 88df3ca5a2f6] (2026-10-06T00:54:18Z)
- (step 4) `python3 plugin/tests/run.py -k test_doctor` → exit 0 · Ran 23 tests in 7.9s (7 classes, 16 at a time; slowest: Command 8s, RestoreState 0s, Briefs 0s) / OK [ran] [tree e88682c670c2] (2026-10-06T00:54:36Z)
- (ac 1) `python3 plugin/tests/run.py -k Install` → exit 0 · Ran 21 tests in 1.6s (3 classes, 16 at a time; slowest: Install 2s, Install 1s, InstallScript 0s) / OK [ran] [tree e88682c670c2] (2026-10-06T00:54:38Z)
- (ac 2) `python3 plugin/tests/run.py -k test_doctor` → exit 0 · Ran 23 tests in 8.1s (7 classes, 16 at a time; slowest: Command 8s, RestoreState 0s, Checks 0s) / OK [ran] [tree e88682c670c2] (2026-10-06T00:54:47Z)
- (step 3) `python3 plugin/tests/run.py -k InstallScript` → ✗ exit 1 · Ran 6 tests in 0.3s (1 classes, 16 at a time; slowest: InstallScript 0s) / FAILED (1 classes) [ran] [tree 5171cd821b85] (2026-10-06T00:56:44Z)
- (ac 1) `python3 plugin/tests/run.py -k Install` → exit 0 · Ran 21 tests in 1.1s (3 classes, 16 at a time; slowest: Install 1s, Install 1s, InstallScript 0s) / OK [ran] [tree f23983c779e0] (2026-10-06T00:56:49Z)
- (step 3) `python3 plugin/tests/run.py -k InstallScript` → exit 0 · Ran 6 tests in 0.3s (1 classes, 16 at a time; slowest: InstallScript 0s) / OK [ran] [tree cbbc190a15b9] (2026-10-06T00:56:56Z)
- (step 2) `PATH=/tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/py3127:$PATH python3 plugin/tests/run.py` → exit 0 · Ran 828 tests in 42.2s (203 classes, 16 at a time; slowest: Stop 32s, TaskLifecycle 26s, Bench 25s) / OK [ran] [tree cbbc190a15b9] (2026-10-06T00:58:32Z)
- (ac 3) `uv run -q --no-project --python 3.12 python plugin/tests/run.py` → exit 0 · Ran 828 tests in 35.1s (203 classes, 16 at a time; slowest: Stop 25s, TaskLifecycle 21s, Bench 20s) / OK [ran] [tree cbbc190a15b9] (2026-10-06T00:59:07Z)
- `python3 plugin/tests/run.py -k InstallScript -k test_doctor` → ✗ exit 1 · Ran 29 tests in 6.1s (8 classes, 16 at a time; slowest: Command 6s, InstallScript 0s, RestoreState 0s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree cbbc190a15b9] (2026-10-06T00:59:19Z)
- `python3 plugin/tests/run.py -k InstallScript -k test_doctor` → exit 0 · Ran 29 tests in 5.9s (8 classes, 16 at a time; slowest: Command 6s, InstallScript 0s, RestoreState 0s) / OK [ran] [tree cbbc190a15b9] (2026-10-06T00:59:19Z)
- (ac 1) `python3 plugin/tests/run.py -k Install` → exit 0 · Ran 21 tests in 1.2s (3 classes, 16 at a time; slowest: Install 1s, Install 1s, InstallScript 0s) / OK [ran] [tree cbbc190a15b9] (2026-10-06T01:00:04Z)
- (ac 2) `python3 plugin/tests/run.py -k Doctor` → ✗ exit 1 · Ran 0 tests in 0.0s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree cbbc190a15b9] (2026-10-06T01:00:04Z)
- (ac 3) `uv run --no-project --python 3.12 python plugin/tests/run.py` → exit 0 · Ran 828 tests in 34.7s (203 classes, 16 at a time; slowest: Stop 24s, TaskLifecycle 21s, Bench 20s) / OK [ran] [tree cbbc190a15b9] (2026-10-06T01:00:04Z)
- (ac 2) `python3 plugin/tests/run.py -k test_doctor` → exit 0 · Ran 23 tests in 6.0s (7 classes, 16 at a time; slowest: Command 6s, RestoreState 0s, Checks 0s) / OK [ran] [tree cbbc190a15b9] (2026-10-06T01:00:15Z)
- (audit intent) `main-thread review of the diff (subagent budget cap reached today)` → install.sh leaves python3 >= 3.12.7 on macOS (brew, else uv), Linux and WSL (uv), and refuses native Windows with a WSL pointer; doctor fails below the floor; README and CHANGELOG say so [tree cbbc190a15b9] (2026-10-06T01:00:24Z)
- (audit edge) `main-thread review of the diff (subagent budget cap reached today)` → found and fixed: an already-installed uv's bin dir may not be on later shells' PATH while the in-script export hid it — now uv python update-shell (test updated red→green); BrokenPipe path in statusline skipped the stdin reset (9/12 stressed runs crashed on 3.12.7, now 0/12); brew already-installed or unlinked → final py_ok dies with a clear message [tree cbbc190a15b9] (2026-10-06T01:00:24Z)
- (audit adversary) `main-thread review of the diff (subagent budget cap reached today)` → the only new exec is astral.sh's uv installer over HTTPS, run only when python3 is too old and uv is absent — the same trust model as this curl|bash installer; no new input is interpolated into commands [tree cbbc190a15b9] (2026-10-06T01:00:24Z)
## Log
- 2026-10-06T00:42:32Z created
- 2026-10-06T00:42:40Z focused
- 2026-10-06T00:56:57Z scope: shot.py import order and a test_visibility assert message — both blocked the floor-version suite run (PIL missing in a bare interpreter; stderr hidden in the flaky failure)
- 2026-10-06T01:00:24Z done
- 2026-10-06T01:00:24Z committed 5f6d011 (10 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- research smoke-tomllib: Asked 2026-10-04 · 1 sub-question(s) · 8 claims: 7 quote found, 1 quote not found, 0 unchecked. ✓ means the quoted words are on the cited page, n…
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- research landscape-20261004: Asked 2026-10-04 · 3 sub-question(s) · 21 claims: 12 quote found, 7 quote not found, 2 unchecked. ✓ means the quoted words are on the cited …
## Lessons
- Test the floor, not the dev box: a suite written on 3.14 hid three breaks (closed-stdin communicate <3.13, argparse optional positionals <3.12.7 and 3.13.0, a backslash f-string <3.12); uv run --python X.Y.Z finds them in a minute, and vermin missed two of the three
## Files touched
- plugin/lib/fmideas.py
- plugin/hooks/statusline
- mods/foreman-ui/tools/shot.py
- plugin/tests/test_visibility.py
- plugin/tests/test_setup.py
- install.sh
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- README.md
- CHANGELOG.md
