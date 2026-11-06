---
id: T-1553
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmoracle.py, plugin/lib/fmreplay.py, plugin/lib/fmcli.py, plugin/tests/test_guard_hardening.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:52Z
updated: 2026-10-22T21:02:32Z
base: 4265fed419ead88d6848f2e7aa82ce4e50567ce3
base_tree: 453a71aa5c176876e857c2803d001bec0eb97863
plan0_at: 2026-10-22T20:39:41Z
plan0_scope: [plugin/lib/fmoracle.py, plugin/lib/fmreplay.py, plugin/lib/fmcli.py, plugin/tests/test_guard_hardening.py, CHANGELOG.md]
verified: strong
---
# Guard oracle: a stub-exec run agrees with the guard's reading
## Raw request
> Round 3 (T-1520): Guard hardening and trust: a stub-exec oracle of what the shell will really run, mutation-testing the guard, seeded ratcheted evasion generation, catching secrets pasted into the prompt, approval-fatigue breakers, fm doctor --wrong to appeal a false alarm, a renewal for unattended runs, Landlock confinement of workers via ctypes on Linux, and a dangerous-command dojo for people (b020 b084 a070 b083 b087 b089 b090 c027 b118). Every change only tightens or explains the guard. Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Guard hardening and trust: a stub-exec oracle of what the shell will really run, mutation-testing the guard, seeded ratcheted evasion generation, catching secrets pasted into the prompt, approval-fatigue breakers, fm doctor --wrong to appeal a false alarm, a renewal for unattended runs, Landlock confinement of workers via ctypes on Linux, and a dangerous-command dojo for people (b020 b084 a070 b083 b087 b089 b090 c027 b118). Every change only tightens or explains the guard. Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [x] each allow and labelled corpus command run under a recorder PATH in a throwaway folder executes only the programs and files the guard's reading names (stub binaries, no real effects) — verify with `cd plugin/tests && python3 -m unittest test_guard_hardening.Oracle`
## Non-goals
## Approach (options → choice → why)
Options: loosen nothing; chosen (only tightens or explains): a stub-exec oracle that runs a command with every binary replaced by a recorder to see what the shell would really run (in a temp sandbox, compared with the guard's verdicts), mutation-testing the guard (flip a rule, the corpus must fail), seeded ratcheted evasion generation, catching secrets pasted into the prompt (UserPromptSubmit note), approval-fatigue breakers (batch the same ask), fm doctor --wrong to file a false alarm as a guard case, a renewal for unattended runs after N hours, Landlock confinement for workers on Linux through ctypes when the kernel supports it, and a dangerous-command dojo page for people.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] a recorder PATH and a comparison against _split/_tokens
3. [x] review fixes: unable never a pass, both status branches, recorder locked, ancestor binds, limits, tampered records
## Resume here
<!-- auto -->
- 2026-10-22T20:40:48Z step 2/2: a recorder PATH and a comparison against _split/_tokens
- git: foreman/build; 2 uncommitted: plugin/lib/fmoracle.py, plugin/tests/test_guard_hardening.py
- touched since last checkpoint: plugin/lib/fmoracle.py, plugin/tests/test_guard_hardening.py
## Docs impact
~/.claude/foreman/MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_hardening` → red as expected (exit 1) · Ran 4 tests in 0.2s (1 classes, 16 at a time; slowest: Oracle 0s) / FAILED (1 classes) [ran] [tree 5457f5ad65aa] (2026-10-22T20:40:02Z)
- (step 2) `python3 plugin/tests/run.py test_guard_hardening` → red as expected (exit 1) · Ran 6 tests in 2.9s (2 classes, 16 at a time; slowest: Oracle 3s, NoSandbox 0s) / FAILED (2 classes) [ran] [tree d12280e260c0] (2026-10-22T20:44:59Z)
- (step 2) `python3 plugin/tests/run.py test_guard_hardening` → exit 0 · Ran 6 tests in 0.9s (2 classes, 16 at a time; slowest: Oracle 1s, NoSandbox 0s) / OK [ran] [tree 8b7a6ae5546d] (2026-10-22T20:45:40Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Oracle` → exit 0 · Ran 5 tests in 0.620s / OK [ran] [tree 8b7a6ae5546d] (2026-10-22T20:45:41Z)
- (step 3) `python3 plugin/tests/run.py test_guard_hardening` → red as expected (exit 1) · Ran 13 tests in 1.6s (2 classes, 16 at a time; slowest: Oracle 1s, NoSandbox 0s) / FAILED (1 classes) [ran] [tree 777a89505642] (2026-10-22T20:49:19Z)
- (step 3) `python3 plugin/tests/run.py test_guard_hardening` → exit 0 · Ran 14 tests in 8.5s (2 classes, 16 at a time; slowest: Oracle 8s, NoSandbox 0s) / OK [ran] [tree 8945d4c14c9d] (2026-10-22T20:53:49Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Oracle` → exit 0 · Ran 13 tests in 8.848s / OK [ran] [tree 8945d4c14c9d] (2026-10-22T20:54:00Z)
- (step 3) `python3 plugin/tests/run.py test_guard_hardening` → exit 0 · Ran 14 tests in 1.5s (2 classes, 16 at a time; slowest: Oracle 1s, NoSandbox 0s) / OK [ran] [tree 12a0bd659154] (2026-10-22T20:55:16Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Oracle` → exit 0 · Ran 13 tests in 1.365s / OK [ran] [tree 12a0bd659154] (2026-10-22T20:55:18Z)
- (step 2) `python3 plugin/tests/run.py test_guard_hardening test_guard_cases test_replay` → exit 0 · Ran 47 tests in 3.1s (6 classes, 16 at a time; slowest: Replay 3s, GuardCases 3s, Oracle 2s) / OK [ran] [tree 12a0bd659154] (2026-10-22T20:55:21Z)
- (audit adversary) `fm-reviewer adversary pass on the diff` → 7 findings, all fixed with tests: unable never a pass, both status branches, recorder and cd readonly, cwd bound only inside home//tmp//run, ulimit -v/-f, stray records skipped, path vars cleared; absolute-path, PATH=, command -p, exec ceiling documented [tree 12a0bd659154] (2026-10-22T21:00:27Z)
- (audit edge) `tests: pipeline stages recording at once, a bare cd, cd "" no-op, mktemp-steered cd, quoting round trip incl. backslashes and newlines` → fixed two of my own: interleaved records (one file per record) and shlex quote splices (plainest quoting) [tree 12a0bd659154] (2026-10-22T21:00:28Z)
- (audit operator) `fm replay --oracle and --oracle --cmd run by hand; no-bwrap path tested` → 120 labelled cases, 0 misread; without bwrap it says so and runs nothing; unable and misread both exit 1; JSON redacted [tree 12a0bd659154] (2026-10-22T21:00:28Z)
- (audit maintainer) `read fmoracle.py whole (~140 lines) and the replay hook-in` → one module, stdlib only, ponytail note names its ceilings; _guard is a test seam used for both judgments [tree 12a0bd659154] (2026-10-22T21:00:28Z)
- (audit intent) `criterion: each allow and labelled corpus command run under a recorder PATH executes only what the guard's reading names` → met for programs reached by PATH lookup; files a program opens aren't compared (the guard's own file rules cover them), logged as the ceiling [tree 12a0bd659154] (2026-10-22T21:00:29Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Oracle` → exit 0 · Ran 13 tests in 1.227s / OK [ran] [tree 140ba09c34ef] (2026-10-22T21:01:02Z)
- (audit edge) `one fm-reviewer five-lens pass; 7 findings fixed test-first; fm replay --oracle 0 misread on 120 labelled cases` → pipelines, bare/empty cd, mktemp-steered cd and quoting round trips tested [tree 140ba09c34ef] (2026-10-22T21:01:02Z)
- (audit adversary) `one fm-reviewer five-lens pass; 7 findings fixed test-first; fm replay --oracle 0 misread on 120 labelled cases` → sandbox start, recorder lock, ancestor binds, limits, stray records fixed; PATH-less reach documented as the ceiling [tree 140ba09c34ef] (2026-10-22T21:01:02Z)
- (audit intent) `criterion: each allow and labelled corpus command run under a recorder PATH executes only what the guard's reading names; MASTER.md now names fmoracle` → met for programs reached by PATH lookup; files a program opens aren't compared (the guard's own file rules cover them), documented as the ceiling in the module and MASTER.md [tree 140ba09c34ef] (2026-10-22T21:01:44Z)
- (audit adversary) `re-confirmed after the MASTER.md docs line (no code change)` → unchanged: see the earlier adversary audit; docs-only change since [tree 140ba09c34ef] (2026-10-22T21:01:44Z)
- (audit edge) `re-confirmed after the MASTER.md docs line (no code change)` → unchanged: see the earlier edge audit; docs-only change since [tree 140ba09c34ef] (2026-10-22T21:01:45Z)
- (audit operator) `re-confirmed after the MASTER.md docs line (no code change)` → unchanged: see the earlier operator audit; docs-only change since [tree 140ba09c34ef] (2026-10-22T21:01:45Z)
- (audit maintainer) `re-confirmed after the MASTER.md docs line (no code change)` → unchanged: see the earlier maintainer audit; docs-only change since [tree 140ba09c34ef] (2026-10-22T21:01:45Z)
- (audit edge) `one fm-reviewer five-lens pass; 7 findings fixed test-first; fm replay --oracle 0 misread on 120 labelled cases` → pipelines, bare/empty cd, mktemp-steered cd and quoting round trips tested [tree 140ba09c34ef] (2026-10-22T21:01:46Z)
- (audit adversary) `one fm-reviewer five-lens pass; 7 findings fixed test-first; fm replay --oracle 0 misread on 120 labelled cases` → sandbox start, recorder lock, ancestor binds, limits, stray records fixed; PATH-less reach documented as the ceiling [tree 140ba09c34ef] (2026-10-22T21:01:46Z)
## Log
- 2026-10-22T17:43:52Z created
- 2026-10-22T18:06:33Z set scope=['plugin/lib/fmguard.py', 'plugin/lib/fmreplay.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmserve.py', 'plugin/tests/test_guard_hardening.py', 'CHANGELOG.md']
- 2026-10-22T20:38:37Z planned from capture
- 2026-10-22T20:39:40Z set scope=['plugin/lib/fmoracle.py', 'plugin/lib/fmreplay.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_guard_hardening.py', 'CHANGELOG.md']
- 2026-10-22T20:39:41Z focused
- 2026-10-22T21:00:55Z scope: MASTER.md (self docs: the new fmoracle module)
- 2026-10-22T21:02:30Z done
- 2026-10-22T21:02:32Z committed 0298cfcc (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1551 [FEATURE M, active, 4 steps] Round 3 (T-1520): Integrations: export runs as Perfetto/OTLP traces, a glance protocol (on
- T-1543 [FEATURE M, active, 4 steps] Round 3 (T-1520): Settings safety: a last-known-good config that boots if a new one misren
- T-1534 [FEATURE M, active, 4 steps] Round 3 (T-1520): UI replay and determinism: render foreman-ui from recorded fixtures with
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_replay.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmreplay.py; re-ground the plan against them before editing
## Why not caught
the first tests only asked what was recorded, never whether the sandbox ran at all
## Lessons
- A tool that runs things to check them must treat 'didn't run' as its own failing result, never as agreement; mark the start inside the sandbox and check it
## Plan gaps
- added late: review fixes: unable never a pass, both status branches, recorder locked, ancestor binds, limits, tampered records
## Files touched
- plugin/tests/test_guard_hardening.py
- plugin/lib/fmoracle.py
- plugin/lib/fmcli.py
- plugin/lib/fmreplay.py
- CHANGELOG.md
- MASTER.md
