---
id: T-0940
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T20:20:44Z
updated: 2026-10-15T20:32:22Z
batch: [T-0934, T-0935, T-0936, T-0937]
base: a5cac9a5412f548d555bca10d59af4392cdfb531
base_tree: c29e92bbe669bce40a99576e970b6e00f19822b9
verified: strong
---
# Guard false blocks from the friction pass: cd; heredoc message, reset --soft, plugin update message, git fetch
## Raw request
> T-0934: Guard: a 'cd DIR; python3 - <<EOF' refusal should say to chain the cd with && (friction: interpreter-code-driving-foreman 2x)
> T-0935: Guard: git reset --soft/--mixed changes no files; only --hard/--merge/--keep count as a tree write over core
> T-0936: Guard: a pinned plugin yes refuses 'claude plugin update' with a misleading 'pinned to installing' message; say an update needs its own fm ask … plugin
> T-0937: Guard: _FETCH_WORD reads 'git fetch' as a download piped into python
## Interpretation
Four guard false blocks from the friction pass (audits/rsi-20261015-195339.md). (1) 'cd DIR; python3 - <<EOF' is read as interpreter code driving Foreman: _python_units (fmguard.py ~1106) only accepts 'cd DIR &&'. Keep the block (the body is opaque), but make the refusal say to chain the cd with && or use Edit/Write, as the git init message does (~2294). (2) git reset --soft/--mixed changes no files, yet 'reset' in _GIT_WORKTREE_WRITES (~2380) makes _write_targets return the repo root (~2623). Only --hard, --merge and --keep write the tree. (3) 'claude plugin update X' after a yes pinned to X is refused with 'pinned to installing or enabling', which is misleading (fmhooks.py ~771). Decided, as a security choice, not to widen pins: keep the refusal and change the message to say an update is never covered by a pin and needs its own fm ask … plugin. (4) _FETCH_WORD (~912) reads 'git fetch … | python3 -c' as downloaded content piped into python. 'fetch' after 'git ' is not a download.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0934: Guard: a 'cd DIR; python3 - <<EOF' refusal should say to chain the cd with && (friction: i works — verify with `python3 plugin/tests/run.py -k GuardFriction`
- [x] T-0935: Guard: git reset --soft/--mixed changes no files; only --hard/--merge/--keep count as a tr works — verify with `python3 plugin/tests/run.py -k GuardFriction`
- [x] T-0936: Guard: a pinned plugin yes refuses 'claude plugin update' with a misleading 'pinned to ins works — verify with `python3 plugin/tests/run.py -k GuardFriction`
- [x] T-0937: Guard: _FETCH_WORD reads 'git fetch' as a download piped into python works — verify with `python3 plugin/tests/run.py -k GuardFriction`
- [x] The four forms behave as decided: 'cd D; python3 - <<EOF' over Foreman is still refused and the refusal names &&; 'git reset -q --soft HEAD~1' in the Foreman repo passes while --hard is refused; a pinned plugin yes refuses 'claude plugin update' with a message saying updates need their own ask; 'git fetch -q origin && git log -1 | python3 -c "import sys;print(sys.stdin.read())"' passes — verify with `python3 plugin/tests/run.py -k GuardFriction`
- [x] The guard corpus replay shows no newly allowed command — verify with `fm replay`
## Non-goals
## Approach (options → choice → why)
Options: one test class pinning all four forms first, then the smallest change at each site (chosen); a general refactor of how the guard reads a cd prefix (too wide for friction fixes); allow-listing the exact commands (brittle). Pins stay narrow, and only the message changes, so no gate is loosened. reset narrows by flag, and fetch narrows by the word before it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0934: Guard: a 'cd DIR; python3 - <<EOF' refusal should say to chain the cd with && (friction: i
2. [x] T-0935: Guard: git reset --soft/--mixed changes no files; only --hard/--merge/--keep count as a tr
3. [x] T-0936: Guard: a pinned plugin yes refuses 'claude plugin update' with a misleading 'pinned to ins
4. [x] T-0937: Guard: _FETCH_WORD reads 'git fetch' as a download piped into python
5. [x] Failing tests: a GuardFriction class in plugin/tests/test_guard.py with the four forms
6. [x] Fix each site in fmguard.py / fmhooks.py; run test_guard*, then fm replay
## Resume here
## Docs impact
none: refusal texts and two guard narrowings; behaviour documented by the GuardFriction tests and the CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree 50b62deeffad] (2026-10-15T20:24:34Z)
- (step 2) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree 50b62deeffad] (2026-10-15T20:24:35Z)
- (step 3) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree 50b62deeffad] (2026-10-15T20:24:36Z)
- (step 4) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree 50b62deeffad] (2026-10-15T20:24:37Z)
- (step 5) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree 50b62deeffad] (2026-10-15T20:24:38Z)
- (step 6) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree 50b62deeffad] (2026-10-15T20:24:39Z)
- (ac 6) `fm replay` → exit 0 · 0 newly allowed (possible bypasses) / 4901 new to the corpus [ran] [tree 50b62deeffad] (2026-10-15T20:24:51Z)
- (ac 1) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:31:05Z)
- (ac 2) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:31:06Z)
- (ac 3) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:31:07Z)
- (ac 4) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:31:08Z)
- (ac 5) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:31:09Z)
- (ac 6) `fm replay` → exit 0 · 0 newly allowed (possible bypasses) / 4992 new to the corpus [ran] [tree a7e936a0632d] (2026-10-15T20:31:19Z)
- `python3 plugin/tests/run.py -k GuardFriction` → ✗ exit 1 · Ran 4 tests in 1.1s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree a7e936a0632d] (2026-10-15T20:31:55Z)
- `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:31:55Z)
- (ac 1) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:32:21Z)
- (ac 2) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:32:21Z)
- (ac 3) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:32:21Z)
- (ac 4) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:32:21Z)
- (ac 5) `python3 plugin/tests/run.py -k GuardFriction` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: PluginPins 1s, GuardFriction 0s) / OK [ran] [tree a7e936a0632d] (2026-10-15T20:32:21Z)
- (ac 6) `fm replay` → exit 0 · 0 newly allowed (possible bypasses) / 4992 new to the corpus [ran] [tree a7e936a0632d] (2026-10-15T20:32:21Z)
- (audit intent) `main-thread review of the 49-line diff (fmguard _FETCH_WORD, reset read-only check, interpreter refusal text; fmhooks _pin_problem text); guard corpus replay 0 newly allowed of 4,992` → ok: all four friction forms behave as decided; pins stay narrow, only the message changed [tree a7e936a0632d] (2026-10-15T20:32:21Z)
- (audit adversary) `main-thread review of the 49-line diff (fmguard _FETCH_WORD, reset read-only check, interpreter refusal text; fmhooks _pin_problem text); guard corpus replay 0 newly allowed of 4,992` → ok: reset counts only --hard/--merge/--keep/--recurse-submodules and their prefixes as tree writes (soft/mixed move HEAD, reflog-recoverable); (?<!git )fetch still flags bare fetch/curl/wget into an interpreter; replay shows no new allows [tree a7e936a0632d] (2026-10-15T20:32:21Z)
- (audit edge) `main-thread review of the 49-line diff (fmguard _FETCH_WORD, reset read-only check, interpreter refusal text; fmhooks _pin_problem text); guard corpus replay 0 newly allowed of 4,992` → ok with a known limit: git -C DIR fetch | python3 is still read as a download (conservative); git reset -- --hard still blocks [tree a7e936a0632d] (2026-10-15T20:32:21Z)
- (audit operator) `main-thread review of the 49-line diff (fmguard _FETCH_WORD, reset read-only check, interpreter refusal text; fmhooks _pin_problem text); guard corpus replay 0 newly allowed of 4,992` → ok: refusal texts now name the fix (&& or a separate fm ask for updates) [tree a7e936a0632d] (2026-10-15T20:32:21Z)
- (audit maintainer) `main-thread review of the 49-line diff (fmguard _FETCH_WORD, reset read-only check, interpreter refusal text; fmhooks _pin_problem text); guard corpus replay 0 newly allowed of 4,992` → ok: each change carries its T-id comment and a GuardFriction test [tree a7e936a0632d] (2026-10-15T20:32:21Z)
## Log
- 2026-10-15T20:20:44Z created
- 2026-10-15T20:21:10Z criterion 1 verify: `` → `python3 plugin/tests/run.py -k GuardFriction`
- 2026-10-15T20:21:10Z criterion 2 verify: `` → `python3 plugin/tests/run.py -k GuardFriction`
- 2026-10-15T20:21:11Z criterion 3 verify: `` → `python3 plugin/tests/run.py -k GuardFriction`
- 2026-10-15T20:21:11Z criterion 4 verify: `` → `python3 plugin/tests/run.py -k GuardFriction`
- 2026-10-15T20:21:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0940.builder.md
- 2026-10-15T20:21:17Z focused
- 2026-10-15T20:30:59Z merged worktree-agent-a4c58d95fcbba6304 (4 file(s))
- 2026-10-15T20:30:59Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4c58d95fcbba6304
- 2026-10-15T20:30:59Z focused
- 2026-10-15T20:32:22Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261004-recon: 1. **Answer.** Four of the five findings are in the guard and the friction digest. The guard blocks most often on a heredoc that only writes…
- T-0761 [FIX S, dropped, 2 steps] Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
## Why not caught
none: false blocks only show in real use; the friction digest (fm friction) is the gate that caught them, and the GuardFriction forms now join the corpus
## Lessons
- Friction digests point at guard false blocks precisely; a refusal that names the fix (&&, a separate ask) removes most of the repeat cost even where the block itself must stay.
## Files touched
- plugin/tests/test_guard.py
- plugin/tests/test_hooks.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
