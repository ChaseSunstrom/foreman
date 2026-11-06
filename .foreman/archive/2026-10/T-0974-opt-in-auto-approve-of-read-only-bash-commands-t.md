---
id: T-0974
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-15T22:08:01Z
updated: 2026-10-16T00:22:47Z
base: 8029cc05c5776cbfc8f894bc1b6063d44f441528
base_tree: 93f939a9df316e3c2d822232a54dd5d95e73c899
verified: strong
---
# Opt-in auto-approve of read-only Bash the guard classifies safe, in the PermissionRequest hook (T-0974)
## Raw request
> Opt-in auto-approve of read-only Bash commands the guard classifies safe, in the PermissionRequest hook, for default-mode users (off by default), from Dippy (research/T-0964-catalogue.md)
## Interpretation
Users in Claude Code's default permission mode get a dialog for every Bash command not on their allow list, including plain reads (ls, cat, git status). Opt-in (the user's to turn on): Foreman's PermissionRequest hook answers allow for a command that only reads, by a conservative allowlist; anything else gets the dialog as before. Bypass users never see dialogs, so nothing changes for them.
## Assumptions (confidence)
## Acceptance criteria
- [x] off by default: a read-only command's PermissionRequest gets no decision — verify with `python3 plugin/tests/run.py -k ApproveReads`
- [x] on: ls/cat/grep/git status… are allowed; a write, a redirect to a file, a substitution, find -delete, sort -o, git branch NAME, an unknown program still get the dialog; turning it on is the user's (self-authorize) — verify with `python3 plugin/tests/run.py -k ApproveReads`
## Non-goals
## Approach (options → choice → why)
Decision shape confirmed in Claude Code's own types: hookSpecificOutput.decision = {behavior: 'allow'} from the classic PermissionRequest hook. Options: (1) a conservative read-only allowlist in fmguard (ls/cat/head/tail/wc/grep/rg/find without -exec/-delete/-fprint, git status/log/diff/show/branch --list, pwd, which, stat, du, df, tree, sort/uniq/cut without -o, fm read verbs), every simple command must pass, no redirect except to /dev/null, no substitution, and check_bash must find nothing — chosen; (2) approve whatever check_bash finds nothing in (far too loose: the guard only stops the dangerous); (3) a model classifier (cost, nondeterminism; Claude Code's auto mode already offers that). Opt-in is the user's: fm approve-reads on is self-authorize (refused from Claude), off is free. Default-mode users only; bypass users never see dialogs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Read the guard classifier and the PermissionRequest hook; write failing tests for the off-by-default case and for both the safe and the unsafe on-case
2. [x] Add the opt-in setting (off by default) and reuse the guard classifier for the decision; never loosen it for unknown commands
3. [x] Document the setting and its limits in the docs; run fm check and the e2e roundtrip
## Resume here
<!-- auto -->
- 2026-10-16T00:08:53Z step 1/3: Read the guard classifier and the PermissionRequest hook; write failing tests for the off-by-default case and for both the safe and the unsafe on-case
- git: foreman/build; 1 uncommitted: plugin/tests/test_approve_reads.py
- touched since last checkpoint: plugin/tests/test_approve_reads.py
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k ApproveReads` → ✗ exit 1 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: ApproveReads 0s) / FAILED (1 classes) [ran] [tree f381b79b2b67] (2026-10-16T00:07:56Z)
- (step 2) `python3 plugin/tests/run.py -k ApproveReads` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ApproveReads 1s) / OK [ran] [tree fd20ee5757ff] (2026-10-16T00:20:13Z)
- (step 3) `python3 plugin/tests/run.py test_approve_reads test_guard test_hooks` → exit 0 · Ran 261 tests in 36.7s (65 classes, 16 at a time; slowest: Stop 37s, PreToolUse 20s, SessionStart 16s) / OK [ran] [tree e4930c1056f8] (2026-10-16T00:21:58Z)
- (step 2) `python3 plugin/tests/run.py -k ApproveReads` → ✗ exit 1 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ApproveReads 1s) / FAILED (1 classes) [ran] [tree ffb15f086a23] (2026-10-16T00:22:24Z)
- (step 2) `python3 plugin/tests/run.py -k ApproveReads` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ApproveReads 1s) / OK [ran] [tree e805a74d47d4] (2026-10-16T00:22:25Z)
- (ac 1) `python3 plugin/tests/run.py -k ApproveReads` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ApproveReads 1s) / OK [ran] [tree c1e05b25eac5] (2026-10-16T00:22:45Z)
- (ac 2) `python3 plugin/tests/run.py -k ApproveReads` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ApproveReads 1s) / OK [ran] [tree c1e05b25eac5] (2026-10-16T00:22:45Z)
- (audit intent) `self + adversarial pass on read_only(): every part must be an allowlisted reader without its writing/exec/never-ending flags; redirects only to /dev/null; no backtick, $, process substitution, newline, background &, env assignment, path-named program, subshell; git only status/log/diff/show/blame/rev-parse/ls-files/describe/shortlog/grep without --output; the PreToolUse guard has already run (credential reads are refused there); on is self-authorize` → default-mode users stop getting dialogs for plain reads; nothing else changes; off by default [tree c1e05b25eac5] (2026-10-16T00:22:45Z)
- (audit adversary) `self + adversarial pass on read_only(): every part must be an allowlisted reader without its writing/exec/never-ending flags; redirects only to /dev/null; no backtick, $, process substitution, newline, background &, env assignment, path-named program, subshell; git only status/log/diff/show/blame/rev-parse/ls-files/describe/shortlog/grep without --output; the PreToolUse guard has already run (credential reads are refused there); on is self-authorize` → found and closed in review: echo $SECRET / printf ${TOKEN} / jq -n env would print environment secrets without a dialog (now no $ at all, jq dropped); remaining accepted risk: git reads in a hostile repo can run configured fsmonitor/textconv commands, which Claude Code's own git status already accepts [tree c1e05b25eac5] (2026-10-16T00:22:45Z)
- (audit edge) `self + adversarial pass on read_only(): every part must be an allowlisted reader without its writing/exec/never-ending flags; redirects only to /dev/null; no backtick, $, process substitution, newline, background &, env assignment, path-named program, subshell; git only status/log/diff/show/blame/rev-parse/ls-files/describe/shortlog/grep without --output; the PreToolUse guard has already run (credential reads are refused there); on is self-authorize` → an empty command, a trailing newline, a subshell (depth) or a heredoc feed is not a read; turning it on from Claude is refused even with a flag before 'on' [tree c1e05b25eac5] (2026-10-16T00:22:45Z)
## Log
- 2026-10-15T22:08:01Z created
- 2026-10-15T23:49:18Z planned from capture
- 2026-10-16T00:07:15Z criterion 1 verify: `fm check` → `python3 plugin/tests/run.py -k ApproveReads`
- 2026-10-16T00:07:15Z criterion 1 text: With the opt-in off (default), a read-only Bash command still prompts exactly as today → off by default: a read-only command's PermissionRequest gets no decision
- 2026-10-16T00:07:15Z criterion 2 verify: `fm check` → `python3 plugin/tests/run.py -k ApproveReads`
- 2026-10-16T00:07:15Z criterion 2 text: With the opt-in on, a command the guard classifies read-only and safe is approved in PermissionRequest; anything unknown, writing or destructive still prompts → on: ls/cat/grep/git status… are allowed; a write, a redirect to a file, a substitution, find -delete, sort -o, git branch NAME, an unknown program still get the dialog; turning it on is the user's (self-authorize)
- 2026-10-16T00:07:16Z focused
- 2026-10-16T00:09:17Z paused: focus moved to T-1000
- 2026-10-16T00:19:44Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T00:19:44Z focused
- 2026-10-16T00:22:46Z done
- 2026-10-16T00:22:47Z committed 59869e1 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- research brainstorm-round4-20261015: 437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run) from new evidence: a clean-HOME newcomer install, a survey…
- T-0961 [FEATURE M, done, 3 steps] Lanes and internals: the merge base saved before the merge, one _git helper — lesson: When a helper turns exceptions into return codes,…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- the similar finished task took 3 steps
## Lessons
- An allowlist for 'reads' must also forbid expansion: printing is reading, and a variable can print a secret.
## Plan gaps
- failed first: step 1 Read the guard classifier and the PermissionRequest hook; write failing tests for the off-by-defaul…
## Files touched
- plugin/tests/test_approve_reads.py
- plugin/lib/fmguard.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- README.md
- MASTER.md
