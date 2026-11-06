---
id: T-1393
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T19:42:54Z
base: 385a7abb4076c66d157e0ab565438ba1bd7cadb3
base_tree: b8d61ef77572c4794c35be853f65b829266872e6
plan0_at: 2026-10-21T18:33:05Z
plan0_scope: []
verified: strong
---
# fm code's judge also holds shell rc files and agent settings under HOME, and reports an edit step that changed nothing
## Raw request
> SECURITY: fm code's judge also holds shell rc files (~/.bashrc, ~/.profile, ~/.zshrc) and agent settings (~/.codex, ~/.gemini, ~/.claude) a worker can reach outside the tree, and an edit step that changed nothing is reported (S6, A8)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a fake worker appending to $HOME/.bashrc is reverted and named in a revert event; an edit step with an empty diff is reported as no-effect
## Interpretation
A worker CLI runs as the user, so it can write outside the repo: a line appended to ~/.bashrc or ~/.zshrc runs in the user's next shell, and ~/.codex/config.toml or ~/.gemini/settings.json can turn off another CLI's sandbox. fm code's judge already holds Git's global config the same way (fmcode._snapshot 'own'); extend it to these, with their own reason in the revert event. Separately, an edit step whose turn changed nothing at all should say so instead of looking like progress.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fake worker appending to $HOME/.bashrc (and writing ~/.codex/config.toml) is reverted and named in a revert event; an edit step whose turn changed nothing is reported as no effect — verify with `python3 plugin/tests/run.py test_judge_home`
## Non-goals
## Approach (options → choice → why)
Options: (A) add the rc files and agent settings files to _snapshot's held 'own' set, each put back by Run.judge with its own reason (chosen: the mechanism exists, judged every turn, no new walk); (B) run the worker with a temp HOME (breaks its login and the user's own CLI config); (C) a guard hook rule (codex/gemini shells don't pass Foreman's guard). Held: ~/.bashrc .bash_profile .bash_login .profile .zshrc .zshenv .zprofile .config/fish/config.fish, ~/.codex/config.toml, ~/.gemini/settings.json, ~/.claude/settings.json and settings.local.json (files only; a missing one that appears is removed). The judge's reason for these: 'a worker never changes your shell startup or another agent's settings'. No-effect: when a step's turn leaves the tree, HEAD and held files exactly as before, emit a note event 'step N: the worker's turn changed nothing'. Tests use a temp HOME.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_judge_home.py: a fake worker (HOME a temp dir) appends to HOME/.bashrc and writes HOME/.codex/config.toml; both are put back and each named in a revert event; a turn that changes nothing gets an event saying the step had no effect
2. [x] extend Run.judge's held set in fmcode.py to the shell rc files (.bashrc .bash_profile .profile .zshrc .zprofile .config/fish/config.fish) and agent settings (.codex/ .gemini/ config files, .claude/settings*.json) under HOME, held before the turn like Git's global config; report a no-effect step
## Resume here
## Docs impact
README fm code paragraph names the held HOME files; CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_judge_home` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (17.8 s; last 34 of 34 lines) [ran] [tree 64b20abaaa07] (2026-10-21T18:35:12Z)
- (step 1) `python3 plugin/tests/run.py test_judge_home` → ✗ exit 1 · Ran 3 tests in 15.0s (1 classes, 16 at a time; slowest: JudgeHome 15s) / FAILED (1 classes) [ran] [tree 64b20abaaa07] (2026-10-21T18:35:31Z)
- (step 2) `python3 plugin/tests/run.py test_judge_home test_code_worker` → exit 0 · (no output) [ran] [tree a78095dc75d4] (2026-10-21T18:38:44Z)
- (step 2) `python3 plugin/tests/run.py test_judge_home` → exit 0 · Ran 3 tests in 18.7s (1 classes, 16 at a time; slowest: JudgeHome 18s) / OK [ran] [tree a22fe8dcf2be] (2026-10-21T18:46:54Z)
- (ac 1) `python3 plugin/tests/run.py test_judge_home` → exit 0 · ✓ exit 0 (20.4 s) · OK [ran] [tree b5786799d6ce] (2026-10-21T18:48:26Z)
- (ac 1) `python3 plugin/tests/run.py test_judge_home` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (19.9 s; last 37 of 37 lines) [ran] [tree 9db6f337c36e] (2026-10-21T19:13:05Z)
- (step 1) `python3 plugin/tests/run.py test_judge_home` → ✗ exit 1 · Ran 6 tests in 21.7s (1 classes, 16 at a time; slowest: JudgeHome 21s) / FAILED (1 classes) [ran] [tree 9db6f337c36e] (2026-10-21T19:13:30Z)
- (ac 1) `python3 plugin/tests/run.py test_judge_home` → exit 0 · ✓ exit 0 (21.1 s) · OK [ran] [tree 26988861d221] (2026-10-21T19:14:22Z)
- (step 2) `python3 plugin/tests/run.py test_judge_home` → exit 0 · Ran 6 tests in 19.9s (1 classes, 16 at a time; slowest: JudgeHome 19s) / OK [ran] [tree bb639aa4c9fa] (2026-10-21T19:16:13Z)
- (step 1) `python3 plugin/tests/run.py test_judge_home test_code_worker` → exit 0 · Ran 67 tests in 133.8s (2 classes, 16 at a time; slowest: Worker 133s, JudgeHome 18s) / OK [ran] [tree cb4ab27e7769] (2026-10-21T19:37:03Z)
- (step 2) `python3 plugin/tests/run.py test_judge_home test_code_worker` → exit 0 · Ran 67 tests in 130.9s (2 classes, 16 at a time; slowest: Worker 131s, JudgeHome 19s) / OK [ran] [tree cb4ab27e7769] (2026-10-21T19:39:14Z)
- (audit adversary) `fm-reviewer` → a worker turning a parent folder into a link made the restore delete ~/.claude/settings.json through it; fixed failing-first (parents recorded, a new link removed unfollowed, a still-redirected path blocks the run); coverage widened to bash_aliases, zlogout, ZDOTDIR, XDG fish conf.d, CODEX_HOME, ~/.claude.json mcpServers [tree cb4ab27e7769] (2026-10-21T19:39:15Z)
- (ac 1) `python3 plugin/tests/run.py test_judge_home` → exit 0 · Ran 6 tests in 18.4s (1 classes, 16 at a time; slowest: JudgeHome 18s) / OK [ran] [tree cb4ab27e7769] (2026-10-21T19:39:41Z)
- (audit intent) `fm-reviewer: 2 findings (planted parent link, missing startup files) fixed failing-first; ~/.claude.json holds only mcpServers (decision recorded)` → a fake worker appending to ~/.bashrc and writing ~/.codex/config.toml and ~/.claude/settings.json is reverted and named; a do-nothing turn gets 'the worker's turn changed nothing' (test_judge_home, 6 tests) [tree cb4ab27e7769] (2026-10-21T19:39:41Z)
- (audit edge) `fm-reviewer: 2 findings (planted parent link, missing startup files) fixed failing-first; ~/.claude.json holds only mcpServers (decision recorded)` → a .zshrc that links into a dotfiles folder is restored in place, link kept; a turn that only leaves __pycache__ isn't 'no effect'; the user's own edit to a held file during a turn is reverted too (named in the event; T-1417 tracks a backup) [tree cb4ab27e7769] (2026-10-21T19:39:41Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T18:31:54Z planned from capture
- 2026-10-21T18:32:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1393.builder.md
- 2026-10-21T18:32:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1393.builder.md
- 2026-10-21T18:33:04Z focused
- 2026-10-21T19:34:33Z merged worktree-agent-a4ac4c545770fbe6b (2 file(s))
- 2026-10-21T19:34:34Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4ac4c545770fbe6b
- 2026-10-21T19:34:35Z focused
- 2026-10-21T19:42:52Z done
- 2026-10-21T19:42:54Z committed 63b5f2c9 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-half-a: Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).
- research T-1328-review: Verdict: changes needed.** One crash, one silent fallback that sends code to a cloud CLI, one unguarded command-bearing config file, and a gap ag…
- T-1388 [SECURITY M, planned, 2 steps] A coding CLI that fm code runs only reads Foreman's state: fm refuses every state-changing command under FOREMAN_WORKER_OF, and a l…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Why not caught
none: new coverage; the reviewer's adversary lens found the parent-link case
## Lessons
- Restoring files outside the repo must check every parent folder is still what it was, or a planted link turns the restore into a delete elsewhere
## Plan gaps
- failed first: step 1 failing tests in plugin/tests/test_judge_home.py: a fake worker (HOME a temp dir) appends to HOME/.…
## Files touched
- plugin/tests/test_judge_home.py
- plugin/lib/fmcode.py
- CHANGELOG.md
- README.md
- plugin/lib/fmcodetui.py
- plugin/lib/fmlib.py
- plugin/lib/fmmodels.py
- plugin/lib/fmplugins.py
- plugin/tests/fixtures/hostile/corpus.json
- plugin/tests/fixtures/hostile/marketplace.json
- plugin/tests/test_code.py
- plugin/tests/test_code_envelope.py
- plugin/tests/test_doctor.py
- plugin/tests/test_lib_hostile.py
- plugin/tests/test_runner_lint.py
