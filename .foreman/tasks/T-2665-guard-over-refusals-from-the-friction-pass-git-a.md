---
id: T-2665
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-02T20:23:36Z
updated: 2026-11-02T20:30:30Z
batch: [T-2661, T-2662, T-2663]
base: 204871387eecdd4fa913a8ac5c6710860adec31e
base_tree: b4e37733ad36c17ba628f4019563bbadb58c8cb7
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-02T20:24:15Z
plan0_scope: []
builder_model: sonnet
lane_stop: merged 2026-11-02T20:27:13Z
verified: strong
---
# Guard over-refusals from the friction pass: git apply's read-only flags, sys.path literals, a bare .ssh string
## Raw request
> T-2661: Guard: git apply --check/--stat/--numstat/--summary is refused as a core tree write; read-only flags exempt like stash list (fmguard.py:3801, 4823-4831); keep plain git apply blocked; FORMS in test_guard_diff
> T-2662: Guard: a sys.path.insert/append path literal in interpreter code counts as a write target (_quoted_paths, fmguard.py:2256); skip constants that are arguments of sys.path calls; replay the full blocked command from the guard ledger first
> T-2663: Guard: a bare '.ssh' string in an edit script reads as a credential read (fmguard.py:2309-2311) when home is named; require a read API for the bare-name branch. Unverified trigger: replay the guard-ledger command first
## Interpretation
1. (chosen) Three narrow exemptions, each pinned by a FORM that is allowed and a sibling that stays blocked: git apply with only read-only flags (--check, --stat, --numstat, --summary) reads; a path literal passed to sys.path.insert/append is an import path, not a write target; a bare credential name ('.ssh') in code with no read API (open, read_text, read_bytes, os.path.join, Path(...), shutil, subprocess) names no read.
2. Loosen the interpreter-code path scan as a whole. Rejected: the scan is the guard's net for writes it can't prove; widening it trades three over-refusals for unknown under-refusals.
## Assumptions (confidence)
## Acceptance criteria
- [x] git apply with only --check, --stat, --numstat or --summary is allowed in Foreman's tree; plain git apply stays blocked — verify with `python3 plugin/tests/run.py test_guard_overrefusal.GitApply`
- [x] a path literal passed to sys.path.insert/append is not a write target; the same literal passed to open(..., 'w') still is — verify with `python3 plugin/tests/run.py test_guard_overrefusal.SysPath`
- [x] a credential name beside the home folder in interpreter code stays refused (fail-closed); the read-API exemption was reverted because io.FileIO, linecache and fileinput read a file without any listed API — verify with `python3 plugin/tests/run.py test_guard_overrefusal.BareCredName`
## Non-goals
## Approach (options → choice → why)
1. Three exemptions in fmguard at the exact branch that fires (git apply in the read-only table near fmguard.py:4823-4831; sys.path call arguments skipped in _quoted_paths' AST walk near 2256; the bare-name credential branch near 2309 requires a read API in the code). Likely outcome: the 7 + 3 + 2 recorded blocks of these shapes stop, nothing else moves. Fails if: a sys.path literal is also opened for writing in the same script (the exemption must skip only the call's own argument node).
2. use what exists: tell sessions to use fm edit and scratch scripts. Fails if: the guard ledger already shows sessions doing that and still hitting these refusals (12 blocks).
3. do less: fix only git apply --check, the clearest one. Fails if: the plugin/lib directory refusal stays the most common of the three (7 of 12).
Choice 1 (80%): each fix is a few lines at the branch that fires, and each keeps a blocked sibling form as its check.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-2661: Guard: git apply --check/--stat/--numstat/--summary is refused as a core tree write;…
2. [x] T-2662: Guard: a sys.path.insert/append path literal in interpreter code counts as a write…
3. [x] T-2663: Guard: a bare '.ssh' string in an edit script reads as a credential read…
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_overrefusal.GitApply` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GitApply 0s) / OK [ran] [tree 0eb8101e17e8] [world 2f1906870a] (2026-11-02T20:25:32Z)
- (step 2) `python3 plugin/tests/run.py test_guard_overrefusal.SysPath` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: SysPath 0s) / OK [ran] [tree 0eb8101e17e8] [world 2f1906870a] (2026-11-02T20:25:34Z)
- (step 3) `python3 plugin/tests/run.py test_guard_overrefusal.BareCredName` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: BareCredName 0s) / OK [ran] [tree 0eb8101e17e8] [world 2f1906870a] (2026-11-02T20:25:34Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_approve_reads test_guard test_guard_diff test_guard_evasions test_guard_exec_vectors test_guard_git test_guard_overrefusal test_guard_pipes test_settings_scopes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.34s] [ran] [tree 0eb8101e17e8] [world 2f1906870a] (2026-11-02T20:25:56Z)
- `python3 plugin/tests/run.py test_guard_overrefusal.GitApply test_guard_overrefusal.SysPath` → ✗ exit 1 · Ran 3 tests in 1.5s (2 classes, 16 at a time; slowest: GitApply 0s, SysPath 0s) / FAILED (1 classes: test_guard_overrefusal.GitApply) (start tree + this task's tests) [ran] [tree 522a4bcc01f6] [world 2f1906870a] (2026-11-02T20:28:59Z)
- `python3 plugin/tests/run.py test_guard_overrefusal.GitApply test_guard_overrefusal.SysPath` → exit 0 · Ran 3 tests in 0.4s (2 classes, 16 at a time; slowest: SysPath 0s, GitApply 0s) / OK [ran] [tree 522a4bcc01f6] [world 2f1906870a] (2026-11-02T20:28:59Z)
- `python3 plugin/tests/run.py test_guard_overrefusal.GitApply test_guard_overrefusal.SysPath` → ✗ exit 1 · Ran 4 tests in 1.4s (2 classes, 16 at a time; slowest: SysPath 0s, GitApply 0s) / FAILED (2 classes: test_guard_overrefusal.SysPath, test_guard_overrefusal.GitApply) (start tree + this task's tests) [ran] [tree bbb76dcf2a64] [world 2f1906870a] (2026-11-02T20:29:17Z)
- `python3 plugin/tests/run.py test_guard_overrefusal.GitApply test_guard_overrefusal.SysPath` → exit 0 · Ran 4 tests in 0.4s (2 classes, 16 at a time; slowest: SysPath 0s, GitApply 0s) / OK [ran] [tree bbb76dcf2a64] [world 2f1906870a] (2026-11-02T20:29:17Z)
- (step 1) `python3 plugin/tests/run.py test_guard_overrefusal test_guard test_guard_diff` → exit 0 · Ran 317 tests in 9.9s (94 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree aefaccfae7a1] [world 2f1906870a] (2026-11-02T20:29:36Z)
- (step 2) `python3 plugin/tests/run.py test_guard_overrefusal test_guard test_guard_diff` → exit 0 · Ran 317 tests in 9.6s (94 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree aefaccfae7a1] [world 2f1906870a] (2026-11-02T20:29:46Z)
- (step 3) `python3 plugin/tests/run.py test_guard_overrefusal test_guard test_guard_diff` → exit 0 · Ran 317 tests in 9.0s (94 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree aefaccfae7a1] [world 2f1906870a] (2026-11-02T20:29:55Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_overrefusal.GitApply` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: GitApply 0s) / OK [ran] [tree aefaccfae7a1] [world 2f1906870a] (2026-11-02T20:30:04Z)
- (ac 2) `python3 plugin/tests/run.py test_guard_overrefusal.SysPath` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: SysPath 0s) / OK [ran] [tree aefaccfae7a1] [world 2f1906870a] (2026-11-02T20:30:04Z)
- (ac 3) `python3 plugin/tests/run.py test_guard_overrefusal.BareCredName` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: BareCredName 0s) / OK [ran] [tree aefaccfae7a1] [world 2f1906870a] (2026-11-02T20:30:04Z)
- (audit intent) `self: reviewed the builder diff; git apply is read-only only when every flag is in the read-only set and one is present; the sys.path skip covers only the call's own argument nodes; the .ssh exemption failed open on review (io.FileIO, linecache, fileinput) and was reverted, with those forms pinned as blocked` → the friction pass asked for three over-refusals gone; two are, the third stays on purpose with its reason recorded (fm decide) [tree aefaccfae7a1] (2026-11-02T20:30:04Z)
- (audit adversary) `self: reviewed the builder diff; git apply is read-only only when every flag is in the read-only set and one is present; the sys.path skip covers only the call's own argument nodes; the .ssh exemption failed open on review (io.FileIO, linecache, fileinput) and was reverted, with those forms pinned as blocked` → git apply --stat --apply, --check --index and --check --reverse stay blocked (tested); open() of the same plugin/lib path stays blocked (tested); FileIO, linecache and listdir-plus-name credential forms stay blocked (tested) [tree aefaccfae7a1] (2026-11-02T20:30:04Z)
- (audit edge) `self: reviewed the builder diff; git apply is read-only only when every flag is in the read-only set and one is present; the sys.path skip covers only the call's own argument nodes; the .ssh exemption failed open on review (io.FileIO, linecache, fileinput) and was reverted, with those forms pinned as blocked` → sys.path aliases (p = sys.path; p.insert) still count as writes, erring toward blocking [tree aefaccfae7a1] (2026-11-02T20:30:04Z)
## Log
- 2026-11-02T20:23:36Z created
- 2026-11-02T20:24:13Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_guard_overrefusal.GitApply`
- 2026-11-02T20:24:13Z criterion 1 text: T-2661: Guard: git apply --check/--stat/--numstat/--summary is refused as a core tree write;… works → git apply with only --check, --stat, --numstat or --summary is allowed in Foreman's tree; plain git apply stays blocked
- 2026-11-02T20:24:14Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_guard_overrefusal.SysPath`
- 2026-11-02T20:24:14Z criterion 2 text: T-2662: Guard: a sys.path.insert/append path literal in interpreter code counts as a write… works → a path literal passed to sys.path.insert/append is not a write target; the same literal passed to open(..., 'w') still is
- 2026-11-02T20:24:14Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_guard_overrefusal.BareCredName`
- 2026-11-02T20:24:14Z criterion 3 text: T-2663: Guard: a bare '.ssh' string in an edit script reads as a credential read… works → a bare '.ssh' string in interpreter code with no read API is allowed; the same with open() of a home path still blocks
- 2026-11-02T20:24:14Z focused
- 2026-11-02T20:24:15Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-02T20:24:22Z set status=planned
- 2026-11-02T20:24:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2665.builder.md
- 2026-11-02T20:24:41Z focused
- 2026-11-02T20:27:13Z merged worktree-agent-a22f73a90956a4791 (2 file(s))
- 2026-11-02T20:27:13Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a22f73a90956a4791
- 2026-11-02T20:27:14Z focused
- 2026-11-02T20:28:56Z criterion 3 text: a bare '.ssh' string in interpreter code with no read API is allowed; the same with open() of a home path still blocks → a credential name beside the home folder in interpreter code stays refused (fail-closed); the read-API exemption was reverted because io.FileIO, linecache and fileinput read a file without any listed API
- 2026-11-02T20:30:27Z done
- 2026-11-02T20:30:30Z committed 12db206c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1585-review: Verdict: changes needed.** I could not run anything, so every finding is traced by reading `~/.claude/foreman/plugin/lib/fmguard.py`. T…
- research T-1585-rereview: Changes needed.** I had no shell tool, so I ran nothing and traced the code instead. Each finding below is a trace, not a measured result.
- research rsi-pass-20261008: 1. **Answer.** I could ground one improvement fully (the pipe-shell false block) and one partly (state-direct from guessed variable targets).…
- decision 2026-10-16: T-0275: a script over the guard's parse budget stays allowed after the literal scan, not refused
## Why not caught
the guard's forms covered refusals that should block, not the read-only flags and import-path literals that shouldn't; the friction digest is where over-refusals surface, and this pass read it
## Lessons
- Never exempt a security check by listing the APIs that would do the dangerous thing: the list is never complete; exempt only what is proven harmless, or keep the refusal
## Files touched
- plugin/lib/fmguard.py
- plugin/tests/test_guard_overrefusal.py
- CHANGELOG.md
