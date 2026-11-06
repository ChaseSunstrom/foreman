---
id: T-2055
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T21:18:39Z
updated: 2026-10-30T00:55:58Z
base: 9e76255750b22bfe067f702614507ab7d361988f
base_tree: 8024f5d2fd14c9ea2a39afc16552a2685c033e88
plan0_at: 2026-10-30T00:28:14Z
plan0_scope: []
lane_branch: worktree-agent-ab0871aab86f489a0
verified: ok
---
# Demo recorder: the session runs with every non-Foreman plugin turned off; re-record live.mp4
## Raw request
> demo/live.mp4 shows another plugin's (ecc) hooks.json warning at the top of the session: record_live.py should record with only Foreman's plugins enabled
## Interpretation
The live demo recording (demo/live.mp4) shows other plugins' output (ecc's hooks.json warning; claude-hud's status line could appear too) because shot.start launches plain claude with the user's settings. Recordings should show Foreman alone: the session turns off every user-enabled plugin outside the foreman marketplace, keeping the user's login, permissions and env.
## Assumptions (confidence)
## Acceptance criteria
- [x] record_live turns off every enabled plugin outside the foreman marketplace via --settings — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_shot`
- [x] the new live recording shows no other plugin's banner or startup notice (frames at 2s/16s/31s viewed) — verify with `! grep -lE "hooks\.json|login expires|api-credits|focus-events|plan includes" demo/live.cast demo/live.svg`
## Non-goals
## Approach (options → choice → why)
Options: (1) --setting-sources project,local: drops user enabledPlugins but also the user's permissions and env, so the session could stall on prompts it never showed before. (2) a fresh CLAUDE_CONFIG_DIR: loses the login, and copying credentials is worse. (3) --settings with enabledPlugins {name: false} for every user-enabled plugin outside the foreman marketplace: flag settings win over user settings key by key, and everything else stays as it was. Chosen: (3). ecc is already off today, but claude-hud (a status line), ponytail and others would still appear in a recording.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: shot.start passes a.settings as one quoted --settings arg; record_live's settings turn off ponytail/claude-hud-style plugins and keep foreman@foreman, foreman-ui@foreman
2. [x] record_live.only_foreman() + shot.start settings attr
3. [x] re-record demo/live.* and view first, middle and last frames
## Resume here
<!-- auto -->
- 2026-10-30T00:45:48Z step 3/3: re-record demo/live.* and view first, middle and last frames
- git: foreman/build; 6 uncommitted: CHANGELOG.md, demo/live.cast, demo/live.mp4, demo/live.svg, demo/record_live.py, plugin/tests/test_shot.py
- touched since last checkpoint: .claude/worktrees/agent-ab0871aab86f489a0/plugin/tests/test_shot.py, .claude/worktrees/agent-ab0871aab86f489a0/mods/foreman-ui/tools/shot.py, .claude/worktrees/agent-ab0871aab86f489a0/demo/record_live.py, CHANGELOG.md, demo/live.cast, demo/live.mp4, demo/live.svg, demo/record_live.py, plugin/tests/test_shot.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_shot 2>&1 | tail -8` → exit 0 · Ran 8 tests in 2.0s (3 classes, 16 at a time; slowest: Harness 0s, OneOff 0s, Trust 0s) / OK [ran] [tree a155c0252d31] (2026-10-30T00:29:00Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_shot 2>&1 | tail -8` → exit 0 · Ran 8 tests in 2.0s (3 classes, 16 at a time; slowest: Harness 0s, OneOff 0s, Trust 0s) / OK [ran] [tree a155c0252d31] (2026-10-30T00:29:00Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_shot` → exit 0 · Ran 8 tests in 0.5s (3 classes, 16 at a time; slowest: Harness 0s, OneOff 0s, Trust 0s) / OK [ran] [tree a155c0252d31] (2026-10-30T00:29:03Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_shot` → exit 0 · Ran 8 tests in 0.5s (3 classes, 16 at a time; slowest: Harness 0s, OneOff 0s, Trust 0s) / OK [ran] [tree a155c0252d31] (2026-10-30T00:29:03Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_shot` → exit 0 · Ran 8 tests in 2.2s (3 classes, 16 at a time; slowest: Harness 0s, Trust 0s, OneOff 0s) / OK [ran] [tree a155c0252d31] (2026-10-30T00:29:06Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_shot` → exit 0 · Ran 8 tests in 0.9s (3 classes, 16 at a time; slowest: Harness 0s, Trust 0s, OneOff 0s) / OK [ran] [tree 9dec2c4fc6fd] (2026-10-30T00:39:05Z)
- (step 3) `grep -cE 'hooks\.json|login expires|api-credits|focus-events|plan includes' demo/live.cast demo/live.svg | grep -v ':0$' | wc -l | grep -qx 0 && ls demo/live.mp4` → exit 0 · demo/live.mp4 [ran] [tree 257ed9f13011] (2026-10-30T00:47:27Z)
- (ac 2) `ffmpeg frames at 2s, 16s and 31s of demo/live.mp4 viewed: no ecc hooks.json, login, promo or tmux notice; Foreman panel rows intact` → pass [tree 257ed9f13011] (2026-10-30T00:47:30Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_shot` → exit 0 · Ran 8 tests in 0.9s (3 classes, 16 at a time; slowest: Harness 0s, Trust 0s, OneOff 0s) / OK [ran] [tree 430fcac1f7f2] (2026-10-30T00:49:16Z)
- (ac 2) `ffmpeg frames of demo/live.mp4 viewed` → ✗ exit 234 · Error opening output file frames. / Error opening output files: Invalid argument [ran] [tree 430fcac1f7f2] (2026-10-30T00:49:16Z)
- (ac 2) `! grep -lE "hooks\.json|login expires|api-credits|focus-events|plan includes" demo/live.cast demo/live.svg` → exit 0 · (no output) [ran] [tree 430fcac1f7f2] (2026-10-30T00:49:36Z)
- (ac 2) `! grep -lE "hooks\.json|login expires|api-credits|focus-events|plan includes" demo/live.cast demo/live.svg` → exit 0 · (no output) [ran] [tree 430fcac1f7f2] (2026-10-30T00:49:45Z)
- (audit intent) `one fm-reviewer pass over the diff (approve with nits); frames at 2s/16s/31s viewed; cast/svg grep for notices = 0` → changelog reworded to credit the blanking, and names the login/plan/tmux notices too [tree 430fcac1f7f2] (2026-10-30T00:49:45Z)
- (audit adversary) `one fm-reviewer pass over the diff (approve with nits); frames at 2s/16s/31s viewed; cast/svg grep for notices = 0` → quiet() only blanks text, runs before the home scrub; --settings passed through shlex.quote; only_foreman reads ~/.claude/settings.json only [tree 430fcac1f7f2] (2026-10-30T00:49:45Z)
- (audit edge) `one fm-reviewer pass over the diff (approve with nits); frames at 2s/16s/31s viewed; cast/svg grep for notices = 0` → bare hooks.X[n] alternative now needs the warning's '" in' prefix so code rows survive; wide chars noted with a ponytail comment [tree 430fcac1f7f2] (2026-10-30T00:49:45Z)
- (audit operator) `one fm-reviewer pass over the diff (approve with nits); frames at 2s/16s/31s viewed; cast/svg grep for notices = 0` → dev-only recorder, one regex pass per frame, no hook cost [tree 430fcac1f7f2] (2026-10-30T00:49:45Z)
- (audit maintainer) `one fm-reviewer pass over the diff (approve with nits); frames at 2s/16s/31s viewed; cast/svg grep for notices = 0` → ANSI comment says why it isn't shot._SGR; test covers both separators and row lengths [tree 430fcac1f7f2] (2026-10-30T00:49:45Z)
## Log
- 2026-10-29T21:18:39Z created
- 2026-10-30T00:26:29Z planned from capture
- 2026-10-30T00:28:14Z focused
- 2026-10-30T00:28:23Z set status=planned
- 2026-10-30T00:28:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2055.builder.md
- 2026-10-30T00:28:38Z focused
- 2026-10-30T00:38:34Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab0871aab86f489a0 (branch worktree-agent-ab0871aab86f489a0 kept: not merged)
- 2026-10-30T00:38:35Z focused
- 2026-10-30T00:38:55Z merged worktree-agent-ab0871aab86f489a0 (3 file(s))
- 2026-10-30T00:39:00Z focused
- 2026-10-30T00:50:27Z done
- 2026-10-30T00:50:32Z committed 2be9fd04 (6 files)
- 2026-10-30T00:50:57Z guard authorization added: publish
- 2026-10-30T00:55:58Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- T-1035 [FEATURE M, done, 2 steps] Re-record the README demo video and refresh the README's pictures with the new UI (chat se — lesson: Record the demo after the UI work …
- research mission-20261021-115148.pack: and integrate all of these too, automatically, super enhanced harness, etc. fully featured/implemented, super recursive wild brain…
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
## Regression test
plugin/tests/test_shot.py: test_only_foreman_turns_off_every_other_plugin and test_settings_reach_claude_as_one_quoted_argument; both fail on main before the merge (no only_foreman, no --settings in the command).
## Why not caught
none: a visual check; a disabled plugin still warns at startup
## Lessons
- Claude Code validates a disabled plugin's hooks.json at startup, so --settings can't hide its warning; blank captured notices only up to the panel separator
## Files touched
- plugin/tests/test_shot.py
- mods/foreman-ui/tools/shot.py
- demo/record_live.py
- CHANGELOG.md
- demo/live.cast
- demo/live.mp4
- demo/live.svg
- plugin/lib/fmcli.py
- plugin/tests/test_audit.py
