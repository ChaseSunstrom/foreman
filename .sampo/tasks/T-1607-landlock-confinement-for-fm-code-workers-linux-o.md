---
id: T-1607
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlandlock.py, plugin/lib/fmcode.py, plugin/lib/fmdoctor.py, plugin/lib/fmguard.py, plugin/tests/test_guard_hardening.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-22T20:38:51Z
updated: 2026-10-22T22:49:59Z
base: df5e3d158937e173a684249806b1e1921209f893
base_tree: 04c1383ea27468cad5540580db11b775e7a5adbc
plan0_at: 2026-10-22T22:28:20Z
plan0_scope: [plugin/lib/fmlandlock.py, plugin/lib/fmcode.py, plugin/lib/fmdoctor.py, plugin/tests/test_guard_hardening.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Landlock confinement for fm code workers, Linux, optional (from T-1553)
## Raw request
> Landlock confinement for fm code workers, Linux, optional (from T-1553)
## Interpretation
On Linux with Landlock (listed in /sys/kernel/security/lsm, ABI from landlock_create_ruleset's version query), an fm code worker's process tree is confined before exec (fmcode.run_bounded gains confine=[writable paths], applied in the child through ctypes: PR_SET_NO_NEW_PRIVS, a ruleset handling every filesystem write access the ABI knows, path-beneath rules for the writable set, landlock_restrict_self). Writable: the worker's worktree, /tmp and /var/tmp, ~/.claude and ~/.claude.json (Claude Code's own state, Foreman's state under it), ~/.cache, and /dev for /dev/null and the terminal. Everything else stays readable but can't be written: the project's main checkout, other projects, ~/.ssh, dotfiles. Without Landlock (another OS, an older kernel, a disabled LSM) the worker runs as before and the run says once that it is unconfined. fm doctor reports whether confinement is available, so /foreman:doctor shows it from Claude Code.
## Assumptions (confidence)
## Acceptance criteria
- [x] on a Linux kernel with Landlock, an fm code worker's process can't write outside its worktree and scratch; without Landlock it runs as before and says so — verify with `cd plugin/tests && python3 -m unittest test_guard_hardening.Landlock`
## Non-goals
## Approach (options → choice → why)
Options: bwrap around each worker (an extra dependency, and Claude Code's own sandbox may nest badly); seccomp (filters syscalls, not paths); Landlock through ctypes (stdlib, unprivileged, path-based, inherited by every child and impossible to undo from inside). Choice: Landlock, optional: detected and used, never required or installed; unsupported → unchanged behaviour plus a note. Reads are not restricted (a worker must read the repo, tools and libraries). Only tightens: no grant or guard rule changes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: Landlock class (a confined child can't write outside its set; unsupported runs unchanged and says so)
2. [x] fmlandlock.py: probe the ABI, build the ruleset, restrict self
3. [x] fmcode.run_bounded confine= for workers, the once-per-run note, fm doctor's line
4. [x] review fixes: narrow set, parent-built ruleset, confined verify/run, guard refuses FOREMAN_CONFINE
## Resume here
<!-- auto -->
- 2026-10-22T22:41:34Z steps 4/4 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcode.py, plugin/lib/fmdoctor.py, plugin/tests/test_guard_hardening.py, plugin/lib/fmlandlock.py
- touched since last checkpoint: plugin/lib/fmdoctor.py, CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/skills_slate.sh, plugin/lib/fmlandlock.py, plugin/tests/test_guard_hardening.py, plugin/lib/fmcode.py
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_hardening.LandlockOptional` → red as expected (exit 1) · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: LandlockOptional 0s) / FAILED (1 classes) [ran] [tree 7b3d4323d213] (2026-10-22T22:28:57Z)
- (step 2) `python3 plugin/tests/run.py test_guard_hardening.Landlock` → exit 0 · Ran 5 tests in 0.6s (2 classes, 16 at a time; slowest: LandlockOptional 0s, Landlock 0s) / OK [ran] [tree 3c34ae342a26] (2026-10-22T22:32:32Z)
- (step 3) `python3 plugin/tests/run.py test_guard_hardening.LandlockOptional test_doctor test_code` → exit 0 · Ran 386 tests in 104.2s (73 classes, 16 at a time; slowest: Worker 104s, Fakes 57s, Bench 33s) / OK [ran] [tree 3c34ae342a26] (2026-10-22T22:34:17Z)
- (step 1) `python3 plugin/tests/run.py test_guard_hardening` → exit 0 · Ran 32 tests in 41.0s (6 classes, 16 at a time; slowest: Mutation 41s, Trust 9s, Oracle 5s) / OK [ran] [tree 3c34ae342a26] (2026-10-22T22:34:59Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Landlock test_guard_hardening.LandlockOptional` → exit 0 · Ran 5 tests in 0.235s / OK [ran] [tree 3c34ae342a26] (2026-10-22T22:35:03Z)
- (step 4) `python3 plugin/tests/run.py test_guard_hardening.LandlockBounds test_guard_hardening.LandlockOptional` → red as expected (exit 1) · Ran 9 tests in 0.3s (2 classes, 16 at a time; slowest: LandlockBounds 0s, LandlockOptional 0s) / FAILED (2 classes) [ran] [tree 9b5f24b7971b] (2026-10-22T22:39:12Z)
- (step 4) `cd plugin/tests && python3 -m unittest test_guard_hardening.Landlock test_guard_hardening.LandlockBounds test_guard_hardening.LandlockOptional` → exit 0 · Ran 11 tests in 0.074s / OK [ran] [tree bf1b9d8c2870] (2026-10-22T22:47:19Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Landlock` → exit 0 · Ran 2 tests in 0.024s / OK [ran] [tree bf1b9d8c2870] (2026-10-22T22:47:36Z)
- (audit intent) `fm-reviewer full pass; HIGH (all of ~/.claude writable) and the fail-open/unconfined-verify findings fixed test-first; real-kernel smoke: fm runs, tree writable, settings.json and new ~/.claude files refused` → fm code workers, their run commands, plan checks and verify evidence all run under Landlock writes-only-beneath set; optional and said once per run; FOREMAN_CONFINE=0 is the user's off switch [tree bf1b9d8c2870] (2026-10-22T22:47:36Z)
- (audit adversary) `fm-reviewer full pass; HIGH (all of ~/.claude writable) and the fail-open/unconfined-verify findings fixed test-first; real-kernel smoke: fm runs, tree writable, settings.json and new ~/.claude files refused` → ~/.claude narrowed to measured working folders (never settings, hooks, plugins, rules, skills, Foreman code); shared repo hooks/config not writable from a worktree; a ruleset that can't be built raises ConfineError → Blocked, never runs unconfined; the guard refuses a model setting FOREMAN_CONFINE (lead, export/declare, env). Ceiling: reads, network, /tmp sockets and Foreman state stay open (mistake guard, not a sandbox) [tree bf1b9d8c2870] (2026-10-22T22:47:36Z)
- (audit edge) `fm-reviewer full pass; HIGH (all of ~/.claude writable) and the fail-open/unconfined-verify findings fixed test-first; real-kernel smoke: fm runs, tree writable, settings.json and new ~/.claude files refused` → no Landlock (other OS, old kernel, LSM off) → unconfined with the reason; file rules carry only WRITE_FILE|TRUNCATE; REFER/TRUNCATE gated by ABI; missing paths skipped; ruleset fd closed in the parent on every path [tree bf1b9d8c2870] (2026-10-22T22:47:36Z)
## Log
- 2026-10-22T20:38:51Z created
- 2026-10-22T21:36:19Z set scope=['plugin/lib/fmlandlock.py', 'plugin/lib/fmcode.py', 'plugin/lib/fmdoctor.py', 'plugin/tests/test_guard_hardening.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T22:13:37Z grounding: Landlock ABI 10 on this kernel; a ctypes prototype (scratchpad ll_proto.py: create_ruleset 444, add_rule 445 path-beneath packed =Qi, PR_SET_NO_NEW_PRIVS, restrict_self 446; file rules only WRITE_FILE|TRUNCATE) confines writes and leaves reads alone. Snag: Claude Code saves ~/.claude.json via ~/.claude.json.tmp.<pid>.<hex> + rename in the home folder, so confining writes to ~/.claude breaks that save. Options: (a) run workers with CLAUDE_CONFIG_DIR=~/.claude so the config file lives inside it (workers then miss user-scope MCP servers from ~/.claude.json, arguably safer); (b) test whether claude -p tolerates the failed save; (c) allow MAKE_REG/REMOVE_FILE/WRITE_FILE under ~ (defeats most of the point). Test (b) first with one tiny claude -p under the confinement, else (a).
- 2026-10-22T22:14:05Z experiment: claude -p 'Reply with exactly: OK' --max-turns 1 under Landlock with writes allowed only to the worktree, /tmp, /var/tmp, /dev, ~/.claude, ~/.claude.json and ~/.cache: exit 0, output OK, no stray file in home (scratchpad ll_claude.py). Option (b) holds: no CLAUDE_CONFIG_DIR change needed; a failed ~/.claude.json save is tolerated.
- 2026-10-22T22:28:19Z focused
- 2026-10-22T22:32:31Z set scope=['plugin/lib/fmlandlock.py', 'plugin/lib/fmcode.py', 'plugin/lib/fmdoctor.py', 'plugin/tests/test_guard_hardening.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T22:39:07Z set scope=['plugin/lib/fmlandlock.py', 'plugin/lib/fmcode.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmguard.py', 'plugin/tests/test_guard_hardening.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T22:39:08Z scope: fmguard.py: refuse the model setting FOREMAN_CONFINE (self-authorize, tightening only)
- 2026-10-22T22:47:34Z scope: plugin/lib/fmguard.py — the FOREMAN_CONFINE self-authorize rule (review: a model mustn't switch confinement off)
- 2026-10-22T22:49:57Z done
- 2026-10-22T22:49:59Z committed d5354fc7 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- research T-1284-review: Verdict:** approve with nits. I found no way to make the guard treat an outside write as inside a project, or a project or state write as outside…
- decision 2026-10-22: Project playbook overlays live at <project>/.claude/playbooks/<stage>/<name>.md, not under .foreman/
- similar finished tasks took 3–4 steps
- likely tests for the scope: plugin/tests/test_code.py, plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmdoctor.py, plugin/tests/test_guard_hardening.py; re-ground the plan against them before editing
## Why not caught
the first cut allowed all of ~/.claude because a claude -p run writes there; only measuring the exact paths it writes showed the narrow set
## Lessons
- Landlock: build the ruleset in the parent and pass its fd (pass_fds); the child's preexec_fn only does prctl + restrict_self, so nothing is imported after fork and a failure surfaces before the worker starts
## Plan gaps
- added late: review fixes: narrow set, parent-built ruleset, confined verify/run, guard refuses FOREMAN_CONFINE
## Files touched
- plugin/tests/test_guard_hardening.py
- plugin/lib/fmlandlock.py
- plugin/lib/fmcode.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmguard.py
