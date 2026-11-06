---
id: T-0345
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-06T03:29:06Z
updated: 2026-10-06T03:38:57Z
base: 6af61748caee77092ab0b1aba85b0387f14031ff
base_tree: cf553c7421fd74362a6cb709d7d7ce4580332120
verified: strong
---
# Guard: commands python code spawns (subprocess, os.system/exec*/spawn*, pty.spawn) are checked as shell commands
## Raw request
> SECURITY: interpreter code that spawns commands (python subprocess.run(['rm','-rf',HOME]) / os.system / ['cp','x','<core file>']) isn't checked: the coarse rule only looks for file-write APIs; read literal argv lists and command strings in subprocess/os.system/os.exec*/os.spawn* calls as shell commands
## Interpretation
python3 -c "import subprocess; subprocess.run(['rm','-rf',HOME])" and a heredoc copying over a core file through subprocess pass the guard today: the interpreter rule only looks for file-write APIs. Read what python starts as the shell command it is.
## Assumptions (confidence)
## Acceptance criteria
- [x] literal and partly-literal spawn calls (lists, strings, shell=True, from-imports, aliases, cwd=) are judged like the shell command they run (rm -rf HOME, cp onto core, sh -c …), a variable target reads as unknown, and git status stays allowed — verify with `python3 plugin/tests/run.py -k test_guard.SpawnedCommands`
- [x] no unintended verdict changes on real commands — verify with `fm replay`
## Non-goals
## Approach (options → choice → why)
(A) AST: in every heredoc body and python -c code that parses, find spawn calls (aliases and from-imports resolved), turn literal args into shell text (non-literals as an unknown "$_", cwd= as a cd) and run check_bash on it. (B) Regex for subprocess/os.system strings — misses lists, aliases and variables. Choice A: the AST already backs the T-0176 prover.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] _python_sources + _spawned_commands into check_bash
3. [x] replay + review
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guard.SpawnedCommands` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SpawnedCommands 0s) / FAILED (1 classes) [ran] [tree fe435a91e7fd] (2026-10-06T03:35:34Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard.SpawnedCommands` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SpawnedCommands 0s) / OK [ran] [tree e5d46227c353] (2026-10-06T03:38:45Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard.SpawnedCommands` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SpawnedCommands 0s) / OK [ran] [tree e5d46227c353] (2026-10-06T03:38:46Z)
- (step 3) `python3 plugin/tests/run.py -k test_guard.SpawnedCommands` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SpawnedCommands 0s) / OK [ran] [tree e5d46227c353] (2026-10-06T03:38:46Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guard.SpawnedCommands` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: SpawnedCommands 0s) / OK [ran] [tree e5d46227c353] (2026-10-06T03:38:57Z)
- (ac 2) `fm replay` → exit 0 · 0 newly allowed (possible bypasses) / 10 new to the corpus [ran] [tree e5d46227c353] (2026-10-06T03:38:57Z)
- (audit adversary) `self adversary review: the change only adds refusals (spawned commands go through check_bash), so its risk is false blocks — fm replay over the real corpus shows 0 newly blocked and 0 newly allowed; data heredocs written with cat are skipped unless the command also runs an interpreter` → aliases (import subprocess as sp), from-imports, shell=True strings, sh -c inside a list, exec*/spawn* argv positions, pty.spawn, -uc clusters and cwd= are all read; a non-literal argument reads as an unknown target (rm of a variable blocks); limits left: getattr/importlib-built calls and code in files python runs (python3 t.py of a file not written in the same command) [tree e5d46227c353] (2026-10-06T03:38:57Z)
- (audit intent) `self adversary review: the change only adds refusals (spawned commands go through check_bash), so its risk is false blocks — fm replay over the real corpus shows 0 newly blocked and 0 newly allowed; data heredocs written with cat are skipped unless the command also runs an interpreter` → the subprocess/os.system gap found in T-0344's replay is closed; git status and other benign spawns stay allowed [tree e5d46227c353] (2026-10-06T03:38:57Z)
## Log
- 2026-10-06T03:29:06Z created
- 2026-10-06T03:35:25Z planned from capture
- 2026-10-06T03:35:25Z focused
- 2026-10-06T03:38:57Z done
- 2026-10-06T03:38:57Z committed 7028729 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research T-0344-review: Verdict: changes needed.** I had no shell, so these are traced by reading `plugin/lib/fmguard.py` and the tests. I did not run any command. [stal…
- T-0344 [FIX M, done, 3 steps] Guard false positives: str.replace isn't a write; curl | python3 -c with proved-pure code isn't pipe-shell — lesson: A text pattern can't p…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- the similar finished task took 3 steps
## Lessons
- A guard that reads files written but not commands started has a hole the size of subprocess; follow every way the code can act, not just the obvious write API.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
