---
id: T-0376
type: FEATURE
tier: M
status: done
priority: normal
scope: [.claude-plugin/marketplace.json, plugin/.claude-plugin/plugin.json, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-09T00:22:48Z
updated: 2026-10-09T00:36:25Z
base: 673ef9e4f015ac5573ce6477d921f57678ceb3ba
base_tree: 6b7463fa51a970616bb787606079c804b1d84d0b
verified: ok
---
# Watch the JARVIS run and keep its Foreman current: fix friction it hits, ship each fix there
## Raw request
> and can you monitor the jarvis session that's going on and update/fix anything in foreman/update it as it goes and improve it?
## Interpretation
The user: 'monitor the jarvis session that's going on and update/fix anything in foreman/update it as it goes and improve it' and 'feel free to reload the plugins/continue the session … as long as it keeps going and everything gets done'. A Monitor streams JARVIS's events.jsonl/ledger over ssh; first real catch: design/tokens.json refused as a credential (fixed in T-0378).
## Assumptions (confidence)
## Acceptance criteria
- [x] JARVIS runs the newest Foreman release (installed version = plugin.json version on main) — verify with `ssh -o BatchMode=yes <user>@<host> 'python3 -c "import json,os; d=json.load(open(os.path.expanduser(\"~/.claude/plugins/installed_plugins.json\"))); print(d[\"plugins\"][\"foreman@foreman\"][0][\"version\"])"' | grep -qx "$(python3 -c 'import json; print(json.load(open("plugin/.claude-plugin/plugin.json"))["version"])')"`
## Non-goals
## Approach (options → choice → why)
(a) poll transcripts by hand — misses events and costs context; (b) a Monitor on JARVIS's Foreman events (guard_block, tool_fail, drive_wait/drive, corrections/steers), re-armed every 30 min, each real friction fixed as its own small task and shipped in a patch release; (c) run Foreman's friction digest on JARVIS hourly — slower. Choice (b).
## Risks and rollback
## Execution prompt
## Steps
1. [x] monitor JARVIS friction (guard blocks, failures, drive waits, steers) and fix each real one test-first
2. [x] ship: bump, merge to main, pull + plugin update on JARVIS, reload its session when idle
## Resume here
## Docs impact
CHANGELOG.md 1.2.2
## Verification evidence
- (step 1) `monitor armed (JARVIS events.jsonl + ledger over ssh); caught design/tokens.json refused as a credential → T-0378 fixed test-first` → typed: the Monitor stream [tree 90168bc94146] (2026-10-09T00:35:11Z)
- (step 2) `ssh -o BatchMode=yes <user>@<host> 'grep -c _mask_substs ~/.claude/plugins/cache/foreman/foreman/1.2.1/lib/fmguard.py'` → exit 0 · 2 [ran] [tree 90168bc94146] (2026-10-09T00:35:12Z)
- (ac 1) `installed foreman@foreman on JARVIS = 1.2.2 = plugin.json on main (ran the criterion's check by hand: exit 0)` → typed: the criterion's quoting is too deep for an exact rerun [tree 90168bc94146] (2026-10-09T00:35:20Z)
- (ac 1) `ssh -o BatchMode=yes <user>@<host> 'python3 -c "import json,os; d=json.load(open(os.path.expanduser(\"~/.claude/plugins/installed_plugins.json\"))); print(d[\"plugins\"][\"foreman@foreman\"][0][\"version\"])"' | grep -qx "$(python3 -c 'import json; print(json.load(open("plugin/.claude-plugin/plugin.json"))["version"])')"` → exit 0 · (no output) [ran] [tree 90168bc94146] (2026-10-09T00:35:21Z)
- (audit operator) `self: shipped through scratch clones only (never the live checkouts); the running session's cache synced from the installed 1.2.2 copy, so its hooks run the fixes now and its next session loads 1.2.2 fully` → JARVIS main fast-forwarded (its own 2 commits already upstream); plugin 1.2.2 installed; 1.2.0/1.2.1 cache folders synced; the watch re-arms every 30 min [tree 90168bc94146] (2026-10-09T00:35:21Z)
- (audit intent) `self: shipped through scratch clones only (never the live checkouts); the running session's cache synced from the installed 1.2.2 copy, so its hooks run the fixes now and its next session loads 1.2.2 fully` → monitoring is live and the first friction it caught is fixed and live on JARVIS [tree 90168bc94146] (2026-10-09T00:35:21Z)
## Log
- 2026-10-09T00:22:48Z created
- 2026-10-09T00:25:28Z user: may reload plugins / continue the JARVIS session whenever needed, as long as the run keeps going and everything gets done
- 2026-10-09T00:34:04Z planned from capture
- 2026-10-09T00:34:05Z set approved=True
- 2026-10-09T00:34:05Z focused
- 2026-10-09T00:35:21Z done
- 2026-10-09T00:36:25Z JARVIS session now runs in tmux session 0 (pane 0:0.0); reload with: tmux send-keys -t 0:0.0 '/reload-plugins' Enter — only when the pane shows an idle prompt
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- T-0318 [FEATURE L, done, 6 steps] FEATURE: beautiful modern animated desktop app wrapping Foreman — supports every feature, — lesson: A remote command over ssh gets no h…
- T-0145 [FEATURE M, done, 3 steps] UI changes reach the running session during a drive: the Stop hook ends the turn once when this session's dev-mods changed, and the rel…
- T-0366 [FIX M, done, 3 steps] Ship T-0364 to JARVIS: merge its 2 local commits into main, bump plugin to 1.2.0, refresh its plugin cache — lesson: A directory-marketplac…
- similar finished tasks took 3–6 steps
## Lessons
- A running Claude Code session keeps the plugin cache folder it started with; hooks are fresh processes per call, so syncing the new release into that folder makes hook fixes live without a restart
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
