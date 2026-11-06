---
id: T-0109
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T03:02:03Z
updated: 2026-10-03T03:17:20Z
base: 5a7a1b1735858bd6a284dae498311ddc40f0149d
verified: ok
---
# Background shells visible; mascot drawn like Claude Code's Clawd; mini colored Claudes per subagent
## Raw request
> also some times claude will have shells running but no subagents, and will wait, and there's nothing in foreman to show that, also the blue dancing claude doesn't look like the claude in claude code does when first opening, and it should have mini randomized colored claudes next to it when sub agents are running, etc
## Interpretation
User: Claude sometimes waits on background shells with no subagents and Foreman shows nothing; the blue mascot should look like the Claude in Claude Code's welcome screen (▐▛███▜▌ / ▝▜█████▛▘ / ▘▘ ▝▝) and dance; mini randomly colored Claudes beside it while subagents run.
## Assumptions (confidence)
## Acceptance criteria
- [x] mod tests cover shell start/done/stop, waiting band row, Clawd frames and mini claudes — verify with `claude plugin test mods/foreman-ui`
- [x] validate + types — verify with `claude plugin validate mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Shell tracking options: (a) the mod tracks live: Bash run_in_background result id on tool.call, done on prompt.submit task-notification and TaskStop/KillShell; (b) fm view from bg events (per project, no session id, 2 s lag). Choice (a): live and per session. Mascot options: (a) redraw the Raster pixel sprite; (b) Text rows of the real block-glyph logo. Choice (b): it is Claude Code's own look, works on every surface, deletes the Raster sprite code. Mini Claudes: 2-row logo per running subagent, color hashed from its id (random-looking, stable), up to 4 then +N.
## Risks and rollback
## Execution prompt
## Steps
1. [x] kit: Clawd frames + mini + agent colors (tests first)
2. [x] register: shell tracking, waiting row in band and pane, mascot rewire
3. [x] verify, release 0.5.0, sync dev copy
## Resume here
## Docs impact
README.md, CHANGELOG.md: shells row and new mascot
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → kit test: Clawd frames 11x3, dance >3 distinct, blink, cheer, minis 7x2, stable agent colors — pass (2026-10-03T03:09:59Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 31 tests across 1 file. [1.34s] [ran] [tree 7120d5248502] (2026-10-03T03:10:01Z)
- (step 2) `claude plugin test mods/foreman-ui` → 31 pass: shells band/pane/notification/TaskStop, minis per subagent (2026-10-03T03:10:01Z)
- (step 3) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 526 tests in 168.357s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (26 pass, 0 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                36.2    41.0     150  [0] / SessionEnd                  32.9    36.5     150  [0] [ran] [tree 15f76583a908] (2026-10-03T03:13:24Z)
- (step 3) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 526 tests in 158.046s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (26 pass, 0 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.6    37.0     150  [0] / SessionEnd                  30.0    33.9     150  [0] [ran] [tree 63210c803676] (2026-10-03T03:17:12Z)
- (step 3) `claude plugin test mods/foreman-ui; validate; tsc; fm check` → 32 pass, validation passed, tsc exit 0, gates exit 0; 0.5.0; dev copy synced (2026-10-03T03:17:13Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 32 tests across 1 file. [1.16s] [ran] [tree 63210c803676] (2026-10-03T03:17:20Z)
- (ac 2) `claude plugin validate mods/foreman-ui` → exit 0 · ❯ ./register.tsx state reads: foreman-ui.agents, foreman-ui.beat, foreman-ui.ctx, foreman-ui.error, foreman-ui.files, foreman-ui.frame, foreman-ui.shells, foreman-ui.sound, foreman-ui.summaries, forem [ran] [tree 63210c803676] (2026-10-03T03:17:20Z)
- (audit intent) `self-review of the diff for reload, lost-notice and killed-agent edges` → user asked for visible shell waits, Claude Code's own Claude, mini colored Claudes per subagent — all three drawn and tested [tree 63210c803676] (2026-10-03T03:17:20Z)
- (audit edge) `self-review of the diff for reload, lost-notice and killed-agent edges` → hot reload re-arms from the atom; notices no longer gated on the module counter; shells age out at 2 h; killed subagents retired from $.agent.list() — tests added [tree 63210c803676] (2026-10-03T03:17:20Z)
## Log
- 2026-10-03T03:02:03Z created
- 2026-10-03T03:05:48Z planned from capture
- 2026-10-03T03:05:48Z focused
- 2026-10-03T03:17:20Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-super: 171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:
- playbook Terminal and mod UI (skills/playbooks/references/ui/terminal-ui.md)
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
## Lessons
- Mods: module variables reset on hot reload while atoms persist; derive counters from atoms, never gate events on module state
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- .claude-plugin/marketplace.json
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
