---
id: T-0095
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T19:52:58Z
updated: 2026-10-02T20:19:37Z
base: 40123ab409532734d7827b705dd3552eb05d46c9
verified: strong
---
# foreman-ui 0.3.0: animated cards everywhere, quick capture, live subagents and files, context meter, ghost-text next, footer, gates card, chime
## Raw request
> foreman-ui 0.3.0: animated cards everywhere, quick capture, live subagents and files, context meter, ghost-text next, footer, gates card, chime
## Interpretation
User: keep adding features and improving the UI; queue/inbox/activity and everything else must match the animated true-color look. Build the round-2 slate (research brainstorm-20261002-round2).
## Assumptions (confidence)
## Acceptance criteria
- [x] mod tests cover animated cards, capture input, subagents/files cards, context checkpoint, ghost-text, footer, gates card, chime toggle — verify with `claude plugin test mods/foreman-ui`
- [x] fm ui --json carries queue progress, latency series and last checks — verify with `python3 -m unittest discover -s plugin/tests -p test_ui.py -q`
- [x] mod validates — verify with `claude plugin validate mods/foreman-ui`
- [x] full suite green — verify with `python3 -m unittest discover -s plugin/tests -q`
## Non-goals
## Approach (options → choice → why)
Options: (a) one shared animated card kit in kit.ts used by every card, new cards fed by the mod's own live data (subagents, files, context) plus three small view-model fields from fm (queue progress, latency series, last checks); (b) per-card ad-hoc styling. Choice: (a). Why: one look everywhere, one place to tune; fm stays the source of record.
## Risks and rollback
## Execution prompt
## Steps
1. [x] kit: animated card system (titled cards, live border pulse, recency fade, mini bars, sparkline)
2. [x] restyle queue, inbox, activity, health, plans as animated cards
3. [x] quick capture input
4. [x] live subagents card and files card
5. [x] context meter and one-time checkpoint at 85%
6. [x] ghost-text next and footer hint/mode
7. [x] view model: queue progress, latency series, last checks (core) + gates card
8. [x] chime with a toggle
9. [x] tests, validate, tsc, 0.3.0, docs, update installed copy
10. [x] declutter: one-line rows for successful fm bookkeeping commands (failures stay full)
11. [x] declutter: reply format drops the header and per-command check lines; no reply badge while the band is on (core)
## Resume here
## Docs impact
README.md (mods paragraph: cards, capture, context checkpoint, ghost text, footer, quiet fm rows, no badge), MASTER.md (mod row), CHANGELOG.md; output style rewritten (quiet while working)
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 19 tests across 1 file. [0.61s] [ran] [tree 76849c3fe8f4] (2026-10-02T19:58:25Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 19 tests across 1 file. [0.62s] [ran] [tree 76849c3fe8f4] (2026-10-02T19:58:26Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 19 tests across 1 file. [0.60s] [ran] [tree 76849c3fe8f4] (2026-10-02T19:58:27Z)
- (step 4) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 19 tests across 1 file. [0.62s] [ran] [tree 76849c3fe8f4] (2026-10-02T19:58:28Z)
- (step 5) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 19 tests across 1 file. [0.60s] [ran] [tree 76849c3fe8f4] (2026-10-02T19:58:29Z)
- (step 6) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 19 tests across 1 file. [0.62s] [ran] [tree 76849c3fe8f4] (2026-10-02T19:58:30Z)
- (step 8) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 19 tests across 1 file. [0.60s] [ran] [tree 76849c3fe8f4] (2026-10-02T19:58:31Z)
- (step 10) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 19 tests across 1 file. [0.64s] [ran] [tree 76849c3fe8f4] (2026-10-02T19:58:31Z)
- (step 7) `python3 -m unittest discover -s plugin/tests -p test_ui.py -q` → exit 0 · Ran 6 tests in 2.315s / OK [ran] [tree 82b65189ef90] (2026-10-02T20:02:01Z)
- (step 11) `python3 -m unittest discover -s plugin/tests -p test_hooks.py -q` → exit 0 · Ran 106 tests in 45.374s / OK [ran] [tree 82b65189ef90] (2026-10-02T20:02:46Z)
- (step 9) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 19 tests across 1 file. [0.61s] [ran] [tree 0a7dec62e50c] (2026-10-02T20:08:10Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-0095-review), findings verified against the code; HIGH: folding fm rows could hide chained/multi-line shell — fold now only plain single-line fm commands (no ; & | ' $ < > newline), 5 bypass shapes tested` → fixed: HIGH closed [tree d14c809dabad] (2026-10-02T20:15:13Z)
- (audit edge) `fm-reviewer five-lens pass (research T-0095-review), findings verified against the code; checkpoint flag never re-armed and a failing run escaped the poller — re-arms under 60%, retries on failure, caught (tested); subagents now marked done by their own turn.complete; refused writes stay out of the files card (tested)` → fixed: MEDIUM + 2 LOW closed [tree d14c809dabad] (2026-10-02T20:15:14Z)
- (audit operator) `fm-reviewer five-lens pass (research T-0095-review), findings verified against the code; badge hidden on a settings flag that doesn't prove the band draws — moot: per the user's steer the badge is gone for everyone (statusline/band show the task); output style quiet for everyone by request` → fixed: MEDIUM closed by removal [tree d14c809dabad] (2026-10-02T20:15:14Z)
- (audit intent) `fm-reviewer five-lens pass (research T-0095-review), findings verified against the code; user asks: animated look on every card, more features, less clutter (badge, repeated text, same-looking rows)` → pass [tree d14c809dabad] (2026-10-02T20:15:14Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-0095-review), findings verified against the code; ghost text skips aborted turns and stale views (refresh reports whether it ran); unused ctx.usd dropped; one card kit` → pass [tree d14c809dabad] (2026-10-02T20:15:14Z)
- (step 9) `claude plugin list` → exit 0 · Path: ~/.claude/plugins/synced/5c6dfa37-93dd-4629-b988-4c203bfcc1c6_1c4f9a98-efaa-4a14-b5b3-7852713bd772/figma~g2 / Status: ✘ disabled [ran] [tree d14c809dabad] (2026-10-02T20:17:07Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 20 tests across 1 file. [0.67s] [ran] [tree d14c809dabad] (2026-10-02T20:17:08Z)
- (ac 2) `python3 -m unittest discover -s plugin/tests -p test_ui.py -q` → exit 0 · Ran 6 tests in 2.368s / OK [ran] [tree d14c809dabad] (2026-10-02T20:17:10Z)
- (ac 3) `claude plugin validate mods/foreman-ui` → exit 0 · ❯ ./register.tsx state reads: foreman-ui.agents, foreman-ui.ctx, foreman-ui.error, foreman-ui.files, foreman-ui.frame, foreman-ui.sound, foreman-ui.summaries, foreman-ui.view / ✔ Validation passed [ran] [tree d14c809dabad] (2026-10-02T20:17:11Z)
- (ac 4) `python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 515 tests in 145.211s / OK [ran] [tree d14c809dabad] (2026-10-02T20:19:37Z)
## Log
- 2026-10-02T19:52:58Z created
- 2026-10-02T19:52:58Z focused
- 2026-10-02T19:54:45Z steer: user finds the transcript cluttered (repeated text/badges, many same-looking rows) — added two declutter steps
- 2026-10-02T19:59:08Z user approved core in Claude Code's permission prompt
- 2026-10-02T20:08:10Z step 9 partial: 19/19 mod tests, validate + tsc clean, 516 Python tests, 0.3.0, docs, live preview synced; the installed-copy update waits for review fixes and the user's plugin yes
- 2026-10-02T20:09:43Z steer: user calls the per-reply [T-xxxx …] badge clutter (stale too: 'executing 3/3' after done) — remove the badge entirely, keep on-screen secret masking
- 2026-10-02T20:17:00Z user approved plugin in Claude Code's permission prompt
- 2026-10-02T20:17:01Z plugin grant used for: claude plugin update changes Claude Code's plugins, MCP servers or config
- 2026-10-02T20:19:37Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
- T-0092 [FEATURE L, done, 8 steps] Polished, animated Foreman UI: clean statusline, card band and pane, animated tool/edit/subagent rows, spinner with the Foreman step — …
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- T-0071 [FEATURE L, done, 5 steps] Super-brainstorm (recursive multi-round fm ideas) + implement every grounded idea and the inbox, recursing until dry; candidate improve…
- similar finished tasks took 5–8 steps
## Lessons
- Fold transcript rows only for commands whose whole text is shown (no chaining); remove clutter outright when the user calls it clutter instead of hiding it conditionally.
## Files touched
- plugin/output-styles/foreman.md
- mods/foreman-ui/hooks/register.tsx
- .claude-plugin/marketplace.json
- CHANGELOG.md
- MASTER.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/sounds/done.wav
- mods/foreman-ui/sounds/needs.wav
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmhooks.py
- plugin/lib/fmwatch.py
- plugin/tests/test_docs.py
- plugin/tests/test_hooks.py
- plugin/tests/test_ui.py
