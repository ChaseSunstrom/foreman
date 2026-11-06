---
id: T-1395
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T19:20:59Z
base: b74c8320c75c356aaae71f19cbab4c3999c13d30
base_tree: 429184b6c61d31481c129d5bb32b3ea2ef0a6850
plan0_at: 2026-10-21T18:33:06Z
plan0_scope: []
verified: strong
---
# Runner flag lint and grade: a dangerous runner template waits for an acknowledgement of its exact hash; runners show a guard grade; link-local model endpoints are refused
## Raw request
> SECURITY: Runner flag lint and grade: a code.toml runner with --yolo, --dangerously-skip-permissions or danger-full-access is refused until acknowledged for that template's hash; fm code runners shows a guard-coverage grade and says which runners' shell commands the guard doesn't confine; model endpoints on link-local addresses are refused (S8, A10)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a --yolo runner is refused until acknowledged and a changed template voids the acknowledgement; fm code runners --json carries a grade per runner; a 169.254.169.254 base_url is refused
## Interpretation
Users can add their own runner templates in $FOREMAN_HOME/code.toml. A template carrying --yolo, --dangerously-skip-permissions or codex's danger-full-access turns off that CLI's own approvals, and fm code would run it unattended. Make that a deliberate act tied to the exact template, show per runner whether Foreman's guard confines its shell, and refuse model endpoints on link-local addresses (cloud metadata).
## Assumptions (confidence)
## Acceptance criteria
- [x] a code.toml runner whose template has --yolo, --dangerously-skip-permissions or danger-full-access is refused until acknowledged for that template's hash, and a changed template voids it; fm code runners --json carries a grade per runner; a model base_url on 169.254.0.0/16 is refused — verify with `python3 plugin/tests/run.py test_runner_lint`
## Non-goals
## Approach (options → choice → why)
Options: (A) lint at load in fmcode.all_runners: a user template (work or plan) matching a dangerous flag is refused unless code.toml's [ack] table maps the runner name to the sha256 of that exact template string; the CodeError prints the exact line to add; a changed template no longer matches (chosen: one place every launch passes through; the ack lives in a core-protected file the guard keeps Claude from writing); (B) warn only (unattended runs never see it); (C) strip the flag (silently changes what the user asked). Grade: fm code runners --json adds 'guard': 'confined' for claude (its shell goes through Foreman's PreToolUse hook) and 'not confined' for the rest, shown in the text list too. Link-local: where fmmodels reads a model base_url, refuse a host in 169.254.0.0/16 or fe80::/10 (ipaddress module; hostnames resolved are out of scope, a ponytail note).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_runner_lint.py for the three behaviours
2. [x] lint user runner templates where fmcode merges code.toml (refusal names the sha256 line to add to code.toml's ack table); a grade per runner in fm code runners (claude: guard confines its shell; others: not confined); refuse a link-local base_url where fmmodels reads model endpoints
## Resume here
## Docs impact
README fm code runners paragraph names [ack] and the guard grade; CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_runner_lint` → ✗ exit 1 · Ran 7 tests in 5.8s (2 classes, 16 at a time; slowest: LinkLocal 5s, RunnerLint 1s) / FAILED (2 classes) [ran] [tree 82efbcaa6194] (2026-10-21T18:35:02Z)
- (step 2) `python3 plugin/tests/run.py test_runner_lint` → exit 0 · Ran 7 tests in 2.4s (2 classes, 16 at a time; slowest: RunnerLint 2s, LinkLocal 0s) / OK [ran] [tree 0d1be00eda66] (2026-10-21T18:36:26Z)
- (ac 1) `python3 plugin/tests/run.py test_runner_lint 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED|OK" | head -30` → ✗ exit 1 · Ran 11 tests in 1.5s (2 classes, 16 at a time; slowest: RunnerLint 1s, LinkLocal 0s) / FAILED (2 classes) [ran] [tree 80cfcf050cf6] (2026-10-21T19:12:19Z)
- (step 1) `python3 plugin/tests/run.py test_runner_lint` → ✗ exit 1 · Ran 11 tests in 1.5s (2 classes, 16 at a time; slowest: RunnerLint 1s, LinkLocal 0s) / FAILED (2 classes) [ran] [tree 80cfcf050cf6] (2026-10-21T19:12:30Z)
- (step 2) `python3 plugin/tests/run.py test_runner_lint` → exit 0 · Ran 11 tests in 2.2s (2 classes, 16 at a time; slowest: RunnerLint 2s, LinkLocal 0s) / OK [ran] [tree 961afd0bb9b5] (2026-10-21T19:13:18Z)
- (step 1) `python3 plugin/tests/run.py test_runner_lint test_code_tui test_models` → exit 0 · Ran 162 tests in 18.4s (22 classes, 16 at a time; slowest: Fuzz 18s, Command 17s, Events 7s) / OK [ran] [tree d6ee5b1b116d] (2026-10-21T19:17:12Z)
- (step 2) `python3 plugin/tests/run.py test_runner_lint test_code_tui test_models` → exit 0 · Ran 162 tests in 19.6s (22 classes, 16 at a time; slowest: Fuzz 19s, Command 17s, Bench 7s) / OK [ran] [tree d6ee5b1b116d] (2026-10-21T19:17:33Z)
- (audit adversary) `fm-reviewer` → quoting split a dangerous flag past the raw-string lint; yolo spellings (--approval-mode yolo, gemini -y, codex -a never, -c sandbox_mode) missing; fullwidth host digits passed the link-local check; fd00:ec2::254 not refused — all fixed test-first (test_runner_lint 11 tests); the ack lives in core-protected code.toml so a worker can't forge it [tree d6ee5b1b116d] (2026-10-21T19:17:42Z)
- (ac 1) `python3 plugin/tests/run.py test_runner_lint` → exit 0 · Ran 11 tests in 1.8s (2 classes, 16 at a time; slowest: RunnerLint 2s, LinkLocal 0s) / OK [ran] [tree d6ee5b1b116d] (2026-10-21T19:17:45Z)
- (audit intent) `fm-reviewer: 5 findings (grade from basename, quoting bypass, missing yolo spellings, fullwidth host, AWS IPv6) all fixed failing-first; the TUI picker now survives a bad code.toml` → a --yolo runner refused until acked, a changed template voids the ack, fm code runners --json grades each runner, a 169.254.169.254 base_url refused (test_runner_lint) [tree d6ee5b1b116d] (2026-10-21T19:17:45Z)
- (audit edge) `fm-reviewer: 5 findings (grade from basename, quoting bypass, missing yolo spellings, fullwidth host, AWS IPv6) all fixed failing-first; the TUI picker now survives a bad code.toml` → look-alikes still pass (mycli -y, -a on-request, --yolo-not, --sandbox workspace-write); combined short flags like -yp aren't caught; a hostname resolving to metadata isn't (ponytail note, T-1421) [tree d6ee5b1b116d] (2026-10-21T19:17:45Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T18:31:56Z planned from capture
- 2026-10-21T18:32:38Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1395.builder.md
- 2026-10-21T18:33:06Z focused
- 2026-10-21T19:16:33Z merged worktree-agent-ad265653fb914b56c (4 file(s))
- 2026-10-21T19:16:38Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad265653fb914b56c
- 2026-10-21T19:16:39Z focused
- 2026-10-21T19:20:56Z done
- 2026-10-21T19:20:59Z committed 94fdf7b8 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-half-a: Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1410 [FEATURE S, active, 2 steps] fm vetoes prints the command that retracts each veto, and that command removes exactly it
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Why not caught
none: new lint
## Lessons
- Lint a command template the way it will run: on its shell-split words, not the raw string
## Plan gaps
- failed first: step 1 failing tests in plugin/tests/test_runner_lint.py for the three behaviours
## Files touched
- plugin/tests/test_runner_lint.py
- plugin/lib/fmmodels.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- README.md
- CHANGELOG.md
