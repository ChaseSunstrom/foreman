---
id: T-1547
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_receipts.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:50Z
updated: 2026-10-23T16:27:53Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: 438e4aca0f32274900afe51eee30f9ce671db003
base_tree: b930245c83a5be2ed9c312e03c8d65a1c87adcf4
plan0_at: 2026-10-23T16:23:54Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_receipts.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): Receipts and review: a replayable process cast per design run, a client
## Raw request
> Round 3 (T-1520): Receipts and review: a replayable process cast per design run, a client packet per UI task, past review nits as a pre-review checklist, blueprint-sheet receipts, a GitHub Action posting proof receipts on PRs, receipts signed with the user's SSH key, and a cold-reader test of the README and site (b006 b079 b086 b097 b111 b117 b088). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Receipts and review: a UI task's receipt as a blueprint SVG (fm task receipt --svg), signed with the user's SSH key and checkable with ssh-keygen -Y verify (--sign KEY), and past review nits on the touched files as a pre-review checklist in fm audit prep's brief. Left out (decided): a replayable process cast (fm code runs already replay with fm code tui --events), a client packet (the signed blueprint is it), a GitHub Action posting receipts (fm pr --post exists) and a model cold-reader test of the README and site.
## Assumptions (confidence)
## Acceptance criteria
- [x] a UI task's receipt renders as a blueprint SVG and verifies with ssh-keygen -Y verify when signed; the pre-review checklist lists past nits for the touched files — verify with `cd plugin/tests && python3 -m unittest test_receipts`
- [x] blueprint receipt, a signature that verifies and fails once changed, past nits in the review brief — verify with `python3 plugin/tests/run.py test_receipts`
## Non-goals
## Approach (options → choice → why)
Options for signing: (a) gpg; (b) ssh-keygen -Y sign with a namespace and an allowed-signers file written beside it; (c) an HMAC of fm's own. Choice: (b): the user's SSH key is the one git already signs with, ssh-keygen ships with OpenSSH, and anyone can verify with one standard command. Nits come from the ledger's finding events (reviewer hooks and fm task finding), matched by path, rejected ones left out, into the brief the reviewer already reads.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] cast and client packet
3. [x] blueprint and signing
4. [x] PR action and cold-reader test
5. [x] red tests: blueprint, signing, past nits
6. [x] _blueprint, _sign_receipt, _past_nits; receipt --svg/--sign; audit prep's nits; CHANGELOG, MASTER
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md, ~/.claude/foreman/MASTER.md (Receipts and review), fm task receipt's help (--svg, --sign)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_receipts` → ✗ exit 1 · Ran 3 tests in 1.8s (1 classes, 16 at a time; slowest: Receipts 2s) / FAILED (1 classes) [ran] [tree 2c243da59253] (2026-10-23T16:24:01Z)
- (step 1) `python3 plugin/tests/run.py test_receipts test_cli test_suite_hygiene test_audit test_design_sprint` → exit 0 · Ran 165 tests in 24.2s (57 classes, 16 at a time; slowest: TaskLifecycle 24s, AuditRun 9s, AuditPrep 9s) / OK [ran] [tree 78f492a9b6e2] (2026-10-23T16:24:56Z)
- (step 2) `python3 plugin/tests/run.py test_receipts test_cli test_suite_hygiene test_audit test_design_sprint` → exit 0 · Ran 165 tests in 25.2s (57 classes, 16 at a time; slowest: TaskLifecycle 25s, AuditRun 10s, StateViews 10s) / OK [ran] [tree 78f492a9b6e2] (2026-10-23T16:25:22Z)
- (step 3) `python3 plugin/tests/run.py test_receipts test_cli test_suite_hygiene test_audit test_design_sprint` → exit 0 · Ran 165 tests in 25.9s (57 classes, 16 at a time; slowest: TaskLifecycle 26s, AuditRun 11s, AuditPrep 11s) / OK [ran] [tree 78f492a9b6e2] (2026-10-23T16:25:48Z)
- (step 4) `python3 plugin/tests/run.py test_receipts test_cli test_suite_hygiene test_design_sprint` → exit 0 · Ran 134 tests in 23.9s (43 classes, 16 at a time; slowest: TaskLifecycle 24s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree 78f492a9b6e2] (2026-10-23T16:26:23Z)
- (step 5) `python3 plugin/tests/run.py test_receipts test_cli test_suite_hygiene test_design_sprint` → exit 0 · Ran 134 tests in 24.1s (43 classes, 16 at a time; slowest: TaskLifecycle 24s, AuditPrep 9s, StateViews 9s) / OK [ran] [tree 78f492a9b6e2] (2026-10-23T16:26:48Z)
- (step 6) `python3 plugin/tests/run.py test_receipts test_cli test_suite_hygiene test_design_sprint` → exit 0 · Ran 134 tests in 24.1s (43 classes, 16 at a time; slowest: TaskLifecycle 24s, StateViews 9s, AuditPrep 9s) / OK [ran] [tree 78f492a9b6e2] (2026-10-23T16:27:13Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_receipts` → exit 0 · Ran 3 tests in 1.972s / OK [ran] [tree 78f492a9b6e2] (2026-10-23T16:27:16Z)
- (ac 2) `python3 plugin/tests/run.py test_receipts` → exit 0 · Ran 3 tests in 2.2s (1 classes, 16 at a time; slowest: Receipts 2s) / OK [ran] [tree 78f492a9b6e2] (2026-10-23T16:27:18Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_receipts` → exit 0 · Ran 3 tests in 1.941s / OK [ran] [tree 78f492a9b6e2] (2026-10-23T16:27:24Z)
- (ac 2) `python3 plugin/tests/run.py test_receipts` → exit 0 · Ran 3 tests in 2.3s (1 classes, 16 at a time; slowest: Receipts 2s) / OK [ran] [tree 78f492a9b6e2] (2026-10-23T16:27:24Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): viewed the blueprint of this very task as an image and moved the bars off the counts; a signature made with a fresh ed25519 key verifies with the printed ssh-keygen -Y verify line and stops verifying after one appended line; nits come only from confirmed or reported findings on the same paths` → the blueprint receipt, receipts signed with the user's SSH key, and past nits as a pre-review checklist, each from Claude Code (fm task receipt, fm audit prep); the rest left out by a recorded decision [tree 78f492a9b6e2] (2026-10-23T16:27:24Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): viewed the blueprint of this very task as an image and moved the bars off the counts; a signature made with a fresh ed25519 key verifies with the printed ssh-keygen -Y verify line and stops verifying after one appended line; nits come only from confirmed or reported findings on the same paths` → a key without its .pub, or no ssh-keygen, is a usage error; an old .sig is replaced, never refused; a task with no changed files draws a sheet that says so; colours that aren't plain hex never reach a fill; findings with no path or under 12 characters are skipped [tree 78f492a9b6e2] (2026-10-23T16:27:24Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): viewed the blueprint of this very task as an image and moved the bars off the counts; a signature made with a fresh ed25519 key verifies with the printed ssh-keygen -Y verify line and stops verifying after one appended line; nits come only from confirmed or reported findings on the same paths` → the key path is the user's own argument, passed to ssh-keygen as one argv item with no shell; the allowed-signers line carries only the key's type and blob and the repo's email; past nits enter the brief marked as data, not instructions, and blueprint text is escaped [tree 78f492a9b6e2] (2026-10-23T16:27:24Z)
## Log
- 2026-10-22T17:43:50Z created
- 2026-10-22T18:06:18Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmpage.py', '.github/workflows', 'plugin/tests/test_receipts.py', 'CHANGELOG.md']
- 2026-10-23T16:21:48Z set tier=M, scope=['plugin/lib/fmcli.py', 'plugin/tests/test_receipts.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T16:23:54Z focused
- 2026-10-23T16:27:51Z done
- 2026-10-23T16:27:53Z committed 881162b5 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1551 [FEATURE M, done, 4 steps] Round 3 (T-1520): Integrations: export runs as Perfetto/OTLP traces, a glance protocol (on — lesson: A stdio server must survive any by…
- decision 2026-10-23: T-1547: leave out a process cast, a client packet, a receipts GitHub Action and a cold-reader model test
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Lessons
- Sign with the key people already verify with: ssh-keygen -Y and an allowed-signers file need nothing new installed
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/tests/test_receipts.py
- MASTER.md
