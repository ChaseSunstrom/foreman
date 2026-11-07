---
id: T-0786
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmpage.py, plugin/lib/fmcli.py, plugin/tests/test_page.py, MASTER.md, plugin/lib/page.html]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T17:18:30Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
base: 3e8ceca103e4c86506b3d1915abf9b5469c16c5c
base_tree: 6fd53111b546d678be7d7efce5c69db471d28053
verified: strong
---
# fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto picks read back
## Raw request
> FEATURE: fm page: the queue and a brainstorm catalogue as one self-contained HTML page for an Artifact
> CONTEXT: T-0760, clusters artifact-cockpit (46 ideas) and privacy. Foreman's cockpit (foreman-ui pane, Desktop, fm serve) never reaches a phone without self-hosting; an Artifact is a private claude.ai page. Publish only ids, titles, marks and counts (no paths, code or secrets); the model publishes it with the Artifact tool.
> DONE-WHEN: fm page writes one HTML file (queue, inbox counts, and optionally a research catalogue JSON) that passes a no-paths/no-secrets scan; a test pins the redaction.
## Interpretation
Foreman's cockpit (foreman-ui pane, Desktop, fm serve) needs this machine; a claude.ai Artifact is private, reachable from the phone, and can keep shared rows (db capability) that Claude reads with ArtifactData. Today's catalogue page was built by hand. fm page writes one page: active task with step, queue, inbox, blocked, last closes, and with --catalogue NAME a research catalogue's clusters with a Build/Veto pick each. It carries ids, titles, tiers, marks and counts only (no paths, code, secrets), checked before writing. It prints the Artifact publish line (file, capabilities db+user, the URL to update when one is recorded) and how to read picks back (ArtifactData list picks).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm page writes an HTML page with the queue and (with --catalogue) every cluster; it holds no absolute path, home dir or secret-looking string; it prints the publish line and the picks read-back — verify with `cd plugin/tests && python3 -m unittest test_page`
## Non-goals
## Approach (options → choice → why)
Options: serve live data through an mcp capability (needs a connector); a static snapshot republished at drains (simple, phone-reachable); a Claude Docs doc (two sources of truth). Chose the snapshot + db picks.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test
2. [x] fmpage.py + fm page
3. [x] Publish once for real; MASTER.md
## Resume here
## Docs impact
MASTER.md lists fm page (builder's change)
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_page` → ✗ exit 1 · Ran 3 tests in 1.061s / FAILED (failures=3) [ran] [tree 0a1520e6742c] (2026-10-14T17:06:38Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_page test_help` → exit 0 · Ran 5 tests in 1.508s / OK [ran] [tree 9ba291565d5c] (2026-10-14T17:09:05Z)
- (step 3) `python3 plugin/bin/fm page --out /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/now.html && python3 /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/check_page.py && node --check /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/page.js` → exit 0 · LEAK catalogue[6].ideas[10].title / abs hits 0 [ran] [tree 9ba291565d5c] (2026-10-14T17:09:11Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_page test_help test_docs test_doctor` → exit 0 · Ran 49 tests in 8.660s / OK [ran] [tree 9ba291565d5c] (2026-10-14T17:09:44Z)
- (step 1) `python3 plugin/tests/run.py test_page` → exit 0 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: Page 1s) / OK [ran] [tree 43c6199365e6] (2026-10-14T17:12:48Z)
- (step 2) `python3 plugin/tests/run.py test_page test_help test_docs test_doctor` → exit 0 · Ran 68 tests in 14.0s (24 classes, 16 at a time; slowest: ViewsRepair 14s, Command 7s, Page 1s) / OK [ran] [tree 43c6199365e6] (2026-10-14T17:13:03Z)
- (step 3) `fm page --catalogue /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/catalogue.json --out /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/foreman-page.html` → exit 0 · Publish (main thread): Artifact file_path /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/foreman-page.html capabilities {"db": {}, "user": {}} url https:/ [ran] [tree 43c6199365e6] (2026-10-14T17:13:03Z)
- (ac 1) `python3 plugin/tests/run.py test_page` → exit 0 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: Page 1s) / OK [ran] [tree 43c6199365e6] (2026-10-14T17:13:04Z)
- (step 2) `python3 plugin/tests/run.py test_page` → ✗ exit 1 · Ran 7 tests in 1.3s (2 classes, 16 at a time; slowest: Page 1s, PageHardening 1s) / FAILED (1 classes) [ran] [tree ea88d9c3c82b] (2026-10-14T17:15:19Z)
- (step 2) `python3 plugin/tests/run.py test_page test_help test_docs test_doctor` → exit 0 · Ran 72 tests in 13.9s (25 classes, 16 at a time; slowest: ViewsRepair 14s, Command 7s, Page 1s) / OK [ran] [tree d37dbce4f0ec] (2026-10-14T17:16:14Z)
- (ac 1) `python3 plugin/tests/run.py test_page` → exit 0 · Ran 7 tests in 1.3s (2 classes, 16 at a time; slowest: Page 1s, PageHardening 1s) / OK [ran] [tree d37dbce4f0ec] (2026-10-14T17:16:15Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_page` → exit 0 · Ran 7 tests in 2.212s / OK [ran] [tree d37dbce4f0ec] (2026-10-14T17:18:23Z)
- (audit intent) `self: merged diff and main-thread fixes read; fm page builds the board from state_dict and an optional catalogue, redacts every string and refuses home/user in any spelling, embeds JSON with < escaped, renders through textContent; the main thread published it to the existing artifact (v3) and read picks back` → the user's board is reachable from the phone, shows the active task, queue and recent closes, and keeps the Build/Veto picks Claude reads with ArtifactData [tree d37dbce4f0ec] (2026-10-14T17:18:23Z)
- (audit adversary) `self: merged diff and main-thread fixes read; fm page builds the board from state_dict and an optional catalogue, redacts every string and refuses home/user in any spelling, embeds JSON with < escaped, renders through textContent; the main thread published it to the existing artifact (v3) and read picks back` → background commit security review found 4 classes (sanitizer bypass, loose URL check, symlink/overwrite paths, unchecked db ids); all fixed with tests; v2's leaked scratch path was replaced by v3 [tree d37dbce4f0ec] (2026-10-14T17:18:23Z)
- (audit intent) `self: merged diff and main-thread fixes read; fm page builds the board from state_dict and an optional catalogue, redacts every string and refuses home/user in any spelling, embeds JSON with < escaped, renders through textContent; the main thread published it to the existing artifact (v3) and read picks back` → the user's board is reachable from the phone, shows the active task, queue and recent closes, and keeps the Build/Veto picks Claude reads with ArtifactData [tree d37dbce4f0ec] (2026-10-14T17:18:29Z)
- (audit adversary) `self: merged diff and main-thread fixes read; fm page builds the board from state_dict and an optional catalogue, redacts every string and refuses home/user in any spelling, embeds JSON with < escaped, renders through textContent; the main thread published it to the existing artifact (v3) and read picks back` → background commit security review found 4 classes (sanitizer bypass, loose URL check, symlink/overwrite paths, unchecked db ids); all fixed with tests; v2's leaked scratch path was replaced by v3 [tree d37dbce4f0ec] (2026-10-14T17:18:29Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:10:56Z planned from capture
- 2026-10-14T17:04:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0786.builder.md
- 2026-10-14T17:05:08Z focused
- 2026-10-14T17:07:31Z set scope=['["plugin/lib/fmpage.py"', '"plugin/lib/fmcli.py"', '"plugin/tests/test_page.py"', '"MASTER.md"', '"plugin/lib/page.html"]']
- 2026-10-14T17:07:32Z scope: + plugin/lib/page.html, the page template the main thread asked for (one file in the plugin)
- 2026-10-14T17:07:38Z set scope=['plugin/lib/fmpage.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_page.py', 'MASTER.md', 'plugin/lib/page.html']
- 2026-10-14T17:11:55Z merged worktree-agent-a3d0046a358697894 (5 file(s))
- 2026-10-14T17:11:55Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3d0046a358697894
- 2026-10-14T17:11:56Z focused
- 2026-10-14T17:13:05Z real path: fm page rendered the queue and the 30-cluster catalogue (0 absolute paths, script parses) and the main thread published it as version 2 of https://claude.ai/artifact/WYV33EY7dGRgKoANmy5agP (db+user carried forward); ArtifactData list picks read back empty. Main thread: a bare ~/ is allowed (names no user), --catalogue also takes a .json path, and the title is a stable name ('Foreman Board')
- 2026-10-14T17:16:15Z review (commit security review, 4 classes) fixed: home dir and username refused in any spelling (encoded -home-~-, /var/home, C:\Users), --url only a claude.ai artifact link, --out only a non-link .html and --catalogue only a plain file, cluster ids plain names (db doc picks/<id>) checked in fm page and in the page script. Version 2 of the published page carried the scratch path (username) in its header; version 3 replaced it within minutes (private page).
- 2026-10-14T17:18:29Z scope: the worktree paths are this task's own files as the builder edited them in its lane (T-0807 maps them)
- 2026-10-14T17:18:30Z done
- 2026-10-14T17:18:30Z committed 810abac (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- research mission-20261008-195201: Request: super improve foreman [stale: plugin/lib/fmagents.py, plugin/lib/fmbench.py, plugin/lib/fmbudget.py changed since it was writt…
- decision 2026-10-14: [revisit: after 2026-10-15] Round 1 of the T-0760 brainstorm: build 12 briefs (T-0775..T-0786) plus the 5 discovered fixes (T-0759, T-0765, T-0767, …
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-14): MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmpage.py, plugin/lib/page.html, plugin/tests/test_page.py; re-ground the plan against them before editing
## Lessons
- anything that publishes must scrub the user's own home and name in every spelling, including echoed arguments like a file path
## Plan gaps
- failed first: step 1 Failing test
## Files touched
- .claude/worktrees/agent-a3d0046a358697894/plugin/tests/test_page.py
- .claude/worktrees/agent-a3d0046a358697894/plugin/lib/page.html
- .claude/worktrees/agent-a3d0046a358697894/plugin/lib/fmpage.py
- .claude/worktrees/agent-a3d0046a358697894/plugin/lib/fmcli.py
- .claude/worktrees/agent-a3d0046a358697894/MASTER.md
- plugin/lib/fmpage.py
- plugin/tests/test_page.py
- plugin/lib/page.html
