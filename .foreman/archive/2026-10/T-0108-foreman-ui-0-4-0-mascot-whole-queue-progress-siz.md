---
id: T-0108
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T23:11:39Z
updated: 2026-10-03T02:58:33Z
base: 780ce78cfe002bfc6015f1d8c0e8d1b5f65a8b76
verified: ok
---
# foreman-ui 0.4.0: mascot, whole-queue progress, size words, clean permission notes, quieter finished rows
## Raw request
> foreman-ui 0.4.0: mascot, whole-queue progress, size words, clean permission notes, quieter finished rows
## Interpretation
User asks (T-0100 T-0102 T-0103 T-0105 T-0106 T-0107): an animated, configurable blue Claude in the pane's top-right corner; prompts/selects that look better; S/M/L replaced by what they mean; a band that shows the whole queue instead of looking nearly done; every part of the TUI (tool calls, prompts, output, in-progress) in the animated Foreman look without clutter.
## Assumptions (confidence)
## Acceptance criteria
- [x] mod tests: sprite frames and color option, size words, queue progress row, permission note, compact read rows and notifications — verify with `claude plugin test mods/foreman-ui`
- [x] fm ui --json has today's done count; statusline says small/medium/large — verify with `python3 -m unittest discover -s plugin/tests -p 'test_[us][it]*.py' -q`
- [x] full suite green — verify with `python3 -m unittest discover -s plugin/tests -q`
## Non-goals
## Approach (options → choice → why)
Options: (a) extend the mod: a half-block true-color sprite (configurable color/off) animated while work is live and blinking on the 2 s poll, size words in chips with a legend, a band row with today's done/queued/inbox bar and up-next, a plain-words note under every fm ask permission dialog, one-line Foreman-styled rows for finished read-only tools and background notifications; core adds today's done count to fm ui and size words to the statusline; (b) redraw the engine's dialogs and diffs. Choice: (a). Why: the engine's dialogs and diffs keep their interaction and fidelity; the mod styles everything around them.
## Risks and rollback
## Execution prompt
## Steps
1. [x] kit: sprite + size words
2. [x] band: whole-queue row
3. [x] pane: mascot header, size legend
4. [x] permission notes for fm ask
5. [x] compact finished read rows and background notifications
6. [x] core: today's done count, statusline size words
7. [x] tests, validate, tsc, 0.4.0, docs, update installed copy
## Resume here
## Docs impact
README.md (mods paragraph), CHANGELOG.md, MASTER.md unchanged rows still accurate
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → 29 pass (2026-10-02T23:14:01Z)
- (step 2) `claude plugin test mods/foreman-ui` → 29 pass (2026-10-02T23:14:01Z)
- (step 3) `claude plugin test mods/foreman-ui` → 29 pass (2026-10-02T23:14:01Z)
- (step 4) `claude plugin test mods/foreman-ui` → 29 pass (2026-10-02T23:14:01Z)
- (step 5) `claude plugin test mods/foreman-ui` → 29 pass (2026-10-02T23:14:01Z)
- (step 6) `python3 -m unittest discover -s plugin/tests -q` → all green (2026-10-03T00:05:00Z)
- (step 7) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 29 tests across 1 file. [0.89s] [ran] [tree ed0964e6842f] (2026-10-03T00:05:21Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 29 tests across 1 file. [0.96s] [ran] [tree 411261adf095] (2026-10-03T02:58:33Z)
- (ac 2) `python3 -m unittest discover -s plugin/tests -p 'test_[us][it]*.py' -q` → exit 0 · Ran 14 tests in 3.893s / OK [ran] [tree 411261adf095] (2026-10-03T02:58:33Z)
- (ac 3) `python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 526 tests in 147.962s / OK [ran] [tree 411261adf095] (2026-10-03T02:58:33Z)
- (step 7) `claude plugin list` → exit 0 · Path: ~/.claude/plugins/synced/5c6dfa37-93dd-4629-b988-4c203bfcc1c6_1c4f9a98-efaa-4a14-b5b3-7852713bd772/figma~g2 / Status: ✘ disabled [ran] [tree 411261adf095] (2026-10-03T02:58:33Z)
- (audit intent) `fm-reviewer five-lens pass (research T-0108-review), findings verified and fixed test-first` → mascot, size words, whole-queue band, prompt notes, quiet rows — every captured UI ask covered; the queue row hides only when nothing waits (by design) [tree 411261adf095] (2026-10-03T02:58:33Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-0108-review), findings verified and fixed test-first` → permission notes refuse any reason with quotes, $, backticks, backslashes or newlines and any over 160 chars (4 bypass shapes tested), so a note never summarises a chained command as one clean ask; notice timer cancelled when the call ends [tree 411261adf095] (2026-10-03T02:58:33Z)
- (audit edge) `fm-reviewer five-lens pass (research T-0108-review), findings verified and fixed test-first` → today_done counts ledger task_done events today, not briefs saved today (tested); origin read guarded; every sprite frame 12x4 (tested) [tree 411261adf095] (2026-10-03T02:58:33Z)
- (audit operator) `fm-reviewer five-lens pass (research T-0108-review), findings verified and fixed test-first` → 0.4.0 in plugin.json and marketplace, installed copy updated, mascot configurable (blue/orange/purple/green/off) and off by setting [tree 411261adf095] (2026-10-03T02:58:33Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-0108-review), findings verified and fixed test-first` → kit holds sprite and size words, register composes; quiet-row branches kept separate for clarity [tree 411261adf095] (2026-10-03T02:58:33Z)
## Log
- 2026-10-02T23:11:39Z created
- 2026-10-02T23:11:39Z focused
- 2026-10-03T00:01:08Z user approved core in Claude Code's permission prompt
- 2026-10-03T02:55:47Z user approved plugin in Claude Code's permission prompt
- 2026-10-03T02:55:50Z plugin grant used for: claude plugin update changes Claude Code's plugins, MCP servers or config
- 2026-10-03T02:58:33Z done
- 2026-10-03T02:58:33Z includes T-0100: More UI and Claude output improvements
- 2026-10-03T02:58:33Z includes T-0102: Animated blue Claude mascot in the Foreman pane's top-right corner, configurable (on/off,
- 2026-10-03T02:58:33Z includes T-0103: All select/option prompts (questions, choices) look better
- 2026-10-03T02:58:33Z includes T-0105: Tier letters S/M/L mean nothing to the user: show what they mean in the UI and output (siz
- 2026-10-03T02:58:33Z includes T-0106: Band looks nearly finished while a long queue waits: show overall progress across the queu
- 2026-10-03T02:58:33Z includes T-0107: Super-enhance all of Claude Code's TUI to match the animated Foreman look: prompts, output
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0092 [FEATURE L, done, 8 steps] Polished, animated Foreman UI: clean statusline, card band and pane, animated tool/edit/subagent rows, spinner with the Foreman step — …
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- playbook Terminal and mod UI (skills/playbooks/references/ui/terminal-ui.md)
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
- the similar finished task took 8 steps
## Lessons
- When a note summarises what a yes approves, only summarise commands whose whole text the summary shows.
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/hooks/statusline
- plugin/lib/fmwatch.py
- plugin/tests/test_statusline_ui.py
- plugin/tests/test_ui.py
