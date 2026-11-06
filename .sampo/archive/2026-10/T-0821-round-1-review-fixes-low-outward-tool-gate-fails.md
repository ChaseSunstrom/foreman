---
id: T-0821
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T18:16:02Z
updated: 2026-10-14T18:30:20Z
base: e08db4581842015c188a4aae042295e77c0e74ab
base_tree: 0c7671e8403f4549ee4a9957f158c2a5841d3ee1
verified: strong
---
# Round-1 review fixes (low): outward-tool gate fails closed, fm page warns in sensitive repos and redacts the username instead of refusing, compact output uses Foreman's state dir and passes through on write errors or nothing clipped, clearer one-off note
## Raw request
> Round-1 review fixes (low): outward-tool gate fails closed, fm page warns in sensitive repos and redacts the username instead of refusing, compact output uses Foreman's state dir and passes through on write errors or nothing clipped, clearer one-off note
## Interpretation
Five low-severity defects the round-1 review verified in today's code: a privacy gate that fails open, fm page offering a publish a sensitive repo refuses, compact output writing outside Foreman's configured state and crashing when it can't write (plus a false 'lines cut' footer), fm page refusing harmless titles that contain the username as a word, and a one-off note that contradicts the edit gate.
## Assumptions (confidence)
From the round-1 review (verified file:line at HEAD): (5) plugin/lib/fmhooks.py _outward_denial (~844-853) logs an exception and allows the tool although hooks.json says onFailure: block — deny instead; plugin/lib/fmpage.py never checks the repo's sensitive flag (c.read_meta(p).get('sensitive') or the helper fmhooks uses) and prints 'Publish: Artifact …' — say publishing is refused there. (6) plugin/hooks/compact:58-60 hard-codes $FOREMAN_HOME/state/outputs: honour FOREMAN_STATE the way fmcore.state_dir does (read it, stdlib only, no Foreman import), and wrap makedirs/os.open in try/except OSError returning 0 (output untouched). (10) compact():27-31: few long lines, none longer than WIDE, still returns text with a 'long lines cut' footer — return None when no line was clipped. (7) fmpage.py:31 username pattern refuses any title with the username as a dash/slash-delimited word (e.g. a repo named after the user): replace those words with 'user' instead of raising Leak; keep refusing real home paths. fmpage _clusters: a cluster without an id becomes 'None' — skip it; a non-dict idea must not crash. (8) fmhooks.py ONEOFF_NOTE: add that if the prompt asks for an edit, it creates one S brief first (the guard refuses unbriefed edits). (high confidence)
## Acceptance criteria
- [x] outward gate denies on an internal error; fm page in a sensitive repo says publishing is refused there — verify with `python3 plugin/tests/run.py test_hooks test_page`
- [x] compact writes under FOREMAN_STATE, passes the output through when it can't write, and adds no footer when nothing was cut — verify with `python3 plugin/tests/run.py test_compact`
- [x] a title with the username as a word is redacted, not refused; a cluster without an id is skipped — verify with `python3 plugin/tests/run.py test_page`
## Non-goals
## Approach (options → choice → why)
Options: (a) local fixes where each finding lives (fmhooks _outward_denial except → deny; fmpage checks c.sensitive; compact reads FOREMAN_STATE like c.state_dir and wraps the write; fmpage replaces a bare username word with 'user'); (b) a shared redaction module for page and compact; (c) leave LOW findings captured. Chose (a): smallest diffs, each with a test; (b) has one caller each.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests
2. [x] Outward gate and fm page
3. [x] Compact hook
4. [x] fm page redaction and ids; ONEOFF wording
## Resume here
## Docs impact
none: behaviour wording is self-describing
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks test_page test_compact` → ✗ exit 1 · Ran 160 tests in 34.1s (24 classes, 16 at a time; slowest: Stop 34s, PreToolUse 17s, SessionStart 15s) / FAILED (4 classes) [ran] [tree 1a8d1d2822df] (2026-10-14T18:20:07Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_page` → exit 0 · Ran 154 tests in 73.4s (22 classes, 16 at a time; slowest: Stop 73s, PreToolUse 39s, SessionStart 33s) / OK [ran] [tree 46949a499028] (2026-10-14T18:23:48Z)
- (step 3) `python3 plugin/tests/run.py test_compact` → exit 0 · Ran 7 tests in 1.4s (3 classes, 16 at a time; slowest: Install 1s, Compact 1s, PostToolUse 0s) / OK [ran] [tree 46949a499028] (2026-10-14T18:23:50Z)
- (step 4) `python3 plugin/tests/run.py test_page` → exit 0 · Ran 10 tests in 3.8s (2 classes, 16 at a time; slowest: PageHardening 4s, Page 3s) / OK [ran] [tree 46949a499028] (2026-10-14T18:23:54Z)
- (step 4) `python3 plugin/tests/run.py test_hooks test_page test_compact` → exit 0 · Ran 161 tests in 32.4s (24 classes, 16 at a time; slowest: Stop 32s, PreToolUse 16s, SessionStart 14s) / OK [ran] [tree 374a0776be48] (2026-10-14T18:27:39Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                39.2    42.8     150  [0] / SessionEnd                  36.1    39.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 374a0776be48] (2026-10-14T18:29:35Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_page` → exit 0 · Ran 155 tests in 33.4s (22 classes, 16 at a time; slowest: Stop 33s, PreToolUse 17s, SessionStart 14s) / OK [ran] [tree 374a0776be48] (2026-10-14T18:30:19Z)
- (ac 2) `python3 plugin/tests/run.py test_compact` → exit 0 · Ran 7 tests in 0.6s (3 classes, 16 at a time; slowest: Install 1s, PostToolUse 0s, Compact 0s) / OK [ran] [tree 374a0776be48] (2026-10-14T18:30:19Z)
- (ac 3) `python3 plugin/tests/run.py test_page` → exit 0 · Ran 10 tests in 1.9s (2 classes, 16 at a time; slowest: PageHardening 2s, Page 1s) / OK [ran] [tree 374a0776be48] (2026-10-14T18:30:19Z)
- (audit intent) `main thread read the builder's 99-line branch diff and checked each fix against its review finding; sensitivity read the same way as _outward_denial (read_meta sensitive); full suite 1,315 OK after the merge` → all six low findings fixed: outward gate denies on its own error; fm page names the refusal in a sensitive repo; compact honours FOREMAN_STATE, passes through on write errors, and adds no false 'cut' footer; a bare username word becomes 'user' while real home paths (incl. the -home-<user> encoding) still refuse; id-less clusters skipped; one-off note says an edit needs an S brief [tree 374a0776be48] (2026-10-14T18:30:19Z)
- (audit adversary) `main thread read the builder's 99-line branch diff and checked each fix against its review finding; sensitivity read the same way as _outward_denial (read_meta sensitive); full suite 1,315 OK after the merge` → the username swap only touches /, \\ or - delimited words; absolute paths, C:\\Users and the encoded home still raise Leak before the swap; fail-closed gate can only over-refuse outward tools, never leak [tree 374a0776be48] (2026-10-14T18:30:19Z)
## Log
- 2026-10-14T18:16:02Z created
- 2026-10-14T18:16:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0821.builder.md
- 2026-10-14T18:16:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0821.builder.md
- 2026-10-14T18:16:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0821.builder.md
- 2026-10-14T18:16:50Z focused
- 2026-10-14T18:27:00Z merged worktree-agent-a79b324aa18e21dca (6 file(s))
- 2026-10-14T18:27:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a79b324aa18e21dca
- 2026-10-14T18:27:01Z focused
- 2026-10-14T18:30:20Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- T-0784 [SECURITY S, done, 2 steps] In a sensitive repo, Claude Code's outward tools (Artifact, PushNotification, SendMessage, RemoteTrigger, Claude Docs writes) are refu…
- research T-0263-review-1: Findings come from reading the diff plus `fmcore.py`, `fmmap.py` and `fmrecall.py`. I did not run any tests. Line numbers for new code are diff…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–3 steps
## Why not caught
none: found by the round-1 cross-task review, the check meant to catch them
## Lessons
- A privacy gate whose hook entry says onFailure: block must also deny on its own caught exceptions
## Plan gaps
- failed first: step 1 Failing tests
## Files touched
- plugin/tests/test_compact.py
- plugin/tests/test_hooks.py
- plugin/tests/test_page.py
- plugin/lib/fmhooks.py
- plugin/lib/fmpage.py
- plugin/hooks/compact
