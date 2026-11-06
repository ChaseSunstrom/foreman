---
id: T-0944
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T20:29:44Z
updated: 2026-10-15T22:05:22Z
base: 0505928b772d84fa78373956e6f677ea1756029b
base_tree: 6cebff53a693363d7690d6327a2378d521e9fab9
verified: strong
---
# Adopt Claude Code 2.1.296–2.1.301: install it, fix subagent turn.start in the pane, re-verify hooks, move Text bold to weight, record the adapted version
## Raw request
> can you update CC to the latest version and update foreman to use the new changes/fixes whatever
## Interpretation
Update Claude Code from 2.1.299 to 2.1.301. The npm copy is root-owned, so its auto-update fails, and the native installer needs no sudo. Then adopt what changed since 2.1.295 (research: recon of the changelog). turn.start now fires for subagents with agentId: the pane's handler resets the main turn's counters, which is a bug. UserPromptSubmit now runs before skill expansion: re-test /foreman: commands. Plan mode respects the PreToolUse allow: re-test the guard. Text weight replaces the deprecated bold. Then record the adapted version.
## Assumptions (confidence)
## Acceptance criteria
- [x] Claude Code 2.1.301+ is installed for the user and first on PATH for new shells — verify with `bash -lc 'claude --version' | grep -E '2\.1\.(30[1-9]|3[1-9][0-9])'`
- [x] A subagent's turn.start no longer resets the main turn's counters in the pane — verify with `claude plugin test mods/foreman-ui`
- [x] Foreman's hooks pass their suite and an e2e round trip on the new version — verify with `python3 plugin/tests/run.py test_hooks test_guard`
- [x] README/MASTER name 2.1.301 as the version Foreman is adapted to, and CHANGELOG lists what changed — verify with `grep -q '2.1.301' README.md`
## Non-goals
## Approach (options → choice → why)
Options: native installer plus a PATH line (chosen: no password, and it updates itself); sudo npm -g (needs the user's password; auto-update stays broken); a user-level npm prefix (works, but drifts from Anthropic's recommended install). Adopt only changes that fix a real behaviour or remove a deprecation. Optional mod hooks (prompt.change, agent.spawn) are captured, not built.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Native install and PATH line; verify in a login shell
2. [x] Mod: skip turn.start when e.agentId is set, with a test; Text bold → weight where supported
3. [x] Re-verify: hook suite, UserPromptSubmit with a /foreman: command, plan mode with the guard
4. [x] Docs: README/MASTER version, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-15T20:52:05Z step 1/4: Native install and PATH line; verify in a login shell
- git: foreman/build; 7 uncommitted: CHANGELOG.md, README.md, plugin/skills/library/cards/practice/eval-driven-development.md, plugin/skills/library/cards/practice/grounding-ideas.md, plugin/skills/library/cards/practice/ideation-to-briefs.md, plugin/skills/library/cards/practice/recursive-improvement.md, plugin/skills/library/cards/practice/second-opinions.md
- touched since last checkpoint: CHANGELOG.md, README.md
## Docs impact
README, MASTER, CHANGELOG (in a113cda)
## Verification evidence
- (step 2) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 84 tests across 1 file. [8.81s] [ran] [tree c7158425cec5] (2026-10-15T20:42:17Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 84 tests across 1 file. [8.71s] [ran] [tree 078d06627118] (2026-10-15T20:42:31Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 84 tests across 1 file. [8.80s] [ran] [tree 7b1d390e5152] (2026-10-15T20:42:57Z)
- (step 3) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 255 tests in 33.2s (63 classes, 16 at a time; slowest: Stop 33s, PreToolUse 18s, SessionStart 15s) / OK [ran] [tree 17f322f4b790] (2026-10-15T20:43:58Z)
- (step 4) `grep -q '2.1.301' README.md && grep -q 'Claude Code 2.1.299' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 2d17f6892c1b] (2026-10-15T20:51:53Z)
- (step 1) `bash -lc 'claude --version' | grep -E '2\.1\.(30[1-9]|3[1-9][0-9])'` → exit 0 · 2.1.301 (Claude Code) [ran] [tree b097b580c1f9] (2026-10-15T22:04:41Z)
- (ac 1) `bash -lc 'claude --version' | grep -E '2\.1\.(30[1-9]|3[1-9][0-9])'` → exit 0 · 2.1.301 (Claude Code) [ran] [tree b097b580c1f9] (2026-10-15T22:05:21Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 86 tests across 1 file. [8.42s] [ran] [tree b097b580c1f9] (2026-10-15T22:05:21Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 255 tests in 29.7s (63 classes, 16 at a time; slowest: Stop 30s, PreToolUse 15s, SessionStart 12s) / OK [ran] [tree b097b580c1f9] (2026-10-15T22:05:21Z)
- (ac 4) `grep -q '2.1.301' README.md` → exit 0 · (no output) [ran] [tree b097b580c1f9] (2026-10-15T22:05:21Z)
- (audit intent) `self-review: the mod and docs changes were reviewed when they landed (a113cda); this close adds only the user's install and PATH lines` → new shells run Claude Code 2.1.301; Foreman's hooks, mod and docs are adapted to it [tree b097b580c1f9] (2026-10-15T22:05:21Z)
- (audit operator) `self-review: the mod and docs changes were reviewed when they landed (a113cda); this close adds only the user's install and PATH lines` → the npm copy stays as a fallback; the running session is still 2.1.299 until restarted; native installs auto-update [tree b097b580c1f9] (2026-10-15T22:05:21Z)
- (audit adversary) `self-review: the mod and docs changes were reviewed when they landed (a113cda); this close adds only the user's install and PATH lines` → only a binary matching both published sha256 sums was installed [tree b097b580c1f9] (2026-10-15T22:05:21Z)
## Log
- 2026-10-15T20:29:44Z created
- 2026-10-15T20:40:58Z planned from capture
- 2026-10-15T20:41:53Z focused
- 2026-10-15T20:46:02Z paused: focus moved to T-0941
- 2026-10-15T20:46:30Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T20:46:30Z focused
- 2026-10-15T20:49:35Z paused: focus moved to T-0939
- 2026-10-15T20:51:28Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-15T20:51:28Z focused
- 2026-10-15T20:52:05Z paused: focus moved to T-0945
- 2026-10-15T22:04:01Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-15T22:04:01Z focused
- 2026-10-15T22:04:02Z guard authorization added: system
- 2026-10-15T22:04:41Z install: claude install 2.1.301 timed out twice (its download has a total deadline this link can't meet); downloaded resumably, verified both sha256 sums from the release manifest, installed the verified binary at ~/.local/share/claude/versions/2.1.301 with ~/.local/bin/claude linked to it; PATH line in ~/.bash_profile (login shells) and ~/.bashrc (interactive), backups in the scratchpad. /usr/bin/claude (npm, 2.1.299) is left: removing it needs sudo.
- 2026-10-15T22:05:22Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- research mission-20261015-154003: Request: have FM enforce some things so we don't rely on agents to do it themselves as they are inconsistent (context: 19 card-writer s…
- research mission-20261015-154003.pack: have FM enforce some things so we don't rely on agents to do it themselves as they are inconsistent (context: 19 card-writer subag…
## Lessons
- When an installer's download has a total deadline, fetch resumably, verify the manifest's checksums yourself, and place the binary in the installer's own layout
## Plan gaps
- failed first: step 2 Mod: skip turn.start when e.agentId is set, with a test; Text bold → weight where supported
## Files touched
- plugin/skills/library/cards/practice/second-opinions.md
- plugin/skills/library/cards/practice/eval-driven-development.md
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/skills/library/cards/practice/recursive-improvement.md
- plugin/skills/library/cards/practice/ideation-to-briefs.md
- mods/foreman-ui/hooks/register.tsx
- plugin/skills/library/cards/claude-code/cc-subagents.md
- plugin/skills/library/cards/practice/grounding-ideas.md
- plugin/skills/library/cards/claude-code/cc-slash-commands.md
- plugin/skills/library/cards/practice/five-whys.md
- plugin/skills/library/cards/practice/retrospectives.md
- plugin/skills/library/cards/claude-code/cc-mcp-config.md
- plugin/skills/library/cards/claude-code/cc-output-styles.md
- plugin/skills/library/cards/claude-code/cc-statusline.md
- mods/foreman-ui/hooks/rows.tsx
- plugin/skills/library/cards/claude-code/cc-mods-ui.md
- plugin/skills/library/cards/claude-code/cc-mod-testing.md
- plugin/skills/library/cards/claude-code/cc-plugin-testing.md
- plugin/tests/test_hooks.py
- plugin/skills/library/cards/claude-code/cc-plugin-evals.md
- plugin/skills/library/cards/claude-code/cc-settings-permissions.md
- plugin/skills/library/cards/claude-code/cc-claude-md-rules.md
- plugin/skills/library/cards/claude-code/cc-headless.md
- plugin/skills/library/cards/claude-code/cc-agent-sdk.md
- plugin/skills/library/cards/claude-code/cc-monitors.md
- plugin/skills/library/cards/claude-code/cc-context-budget.md
- plugin/skills/library/cards/claude-code/cc-plugin-release.md
- plugin/skills/library/cards/claude-code/cc-lsp-plugins.md
- plugin/skills/library/cards/claude-code/cc-plugin-debugging.md
- plugin/lib/fmlib.py
