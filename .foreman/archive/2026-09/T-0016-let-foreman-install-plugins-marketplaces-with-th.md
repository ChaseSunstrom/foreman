---
id: T-0016
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmplugins.py, plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/lib/fmdoctor.py, plugin/lib/fmsetup.py, plugin/tests/**, plugin/rules/foreman.md, plugin/skills/**, MASTER.md, README.md]
depends_on: []
source: user
created: 2026-09-26T12:44:06Z
updated: 2026-09-26T16:28:30Z
---
# Approved plugin/marketplace installs on demand; conflict-free integration of plugins and skills
## Raw request
> Let Foreman install plugins/marketplaces (with the user's approval) when Claude needs a capability that isn't available, and integrate plugins/skills better so they don't conflict (overlap detection, precedence, one owner per behaviour)
## Interpretation
When a task needs a capability that isn't installed (an LSP, a framework skill, an MCP server), Foreman finds candidates in the known marketplaces, checks them for conflicts, asks the user one yes/no, installs, and records it so uninstall reverses it. Separately, every enabled plugin's hooks, skills, agents, commands and MCP servers are checked against Foreman's and each other's so two things never own the same behaviour.
## Assumptions (confidence)
## Acceptance criteria
- [x] claude plugin install/enable/disable/uninstall and marketplace add/remove are blocked by the guard (category plugin) unless the task has the user's approval via fm ask — verify with `python3 -m unittest test_guard`
- [x] fm plugins find <need> lists matching plugins from known marketplaces with source, description and always-on cost — verify with `python3 -m unittest test_plugins`
- [x] fm plugins check [ID] reports ownership conflicts (process-skill overlap, duplicate MCP servers, same-event context/Stop hooks, name clashes) with a recommended action; fm doctor includes it — verify with `python3 -m unittest test_plugins test_doctor`
- [x] fm plugins install ID (after approval) installs, records in the manifest, and uninstall-user removes it — verify with `python3 -m unittest test_plugins test_setup; roundtrip.py`
## Non-goals
## Approach (options → choice → why)
(1) fm plugins find/check/install with a new guard category 'plugin' (claude plugin install|enable|disable|uninstall and marketplace add|remove need fm ask approval) and an ownership map [chosen: approval enforced by the guard, not by memory; one owner per behaviour]. (2) Let Claude run claude plugin install freely [rejected: installs code and always-on context without consent]. (3) Only report conflicts [rejected: user asked for integration].
Ownership map (in fmplugins): Foreman owns planning/intake/brainstorm, task tracking, verification + audit gates, Stop/drive, SessionStart state injection, statusline wrapper; other plugins' process skills that duplicate these (brainstorming, planning, TDD workflow, verification loops) are flagged; domain skills (frontend-design, language references, context7) are used inside Foreman steps. Checks: duplicate MCP servers, same-event hooks that inject context or block Stop, skill/command name clashes, overlapping skill triggers (keyword similarity of descriptions), always-on token cost per plugin.
fm plugins find <need> searches ~/.claude/plugins/marketplaces/*/.claude-plugin/marketplace.json (+ claude plugin list --json); fm plugins install ID runs the check first, then installs after the user's yes and records it in state/install-manifest.json (plugins_installed) so fm uninstall-user removes it.
## Risks and rollback
Risk: blocking plugin commands the user runs themselves → the guard only sees Claude's tool calls; the user's own terminal and ! commands are unaffected. Risk: false conflict flags → report with reasons, never auto-disable. Rollback: git revert; manifest-driven uninstall.
## Execution prompt
## Steps
1. [x] fmplugins: marketplace index + find (TDD)
2. [x] Ownership map + check, wired into doctor (TDD)
3. [x] Guard category plugin + fm ask flow + install/record/uninstall (TDD; core)
4. [x] Rules/skills (need a capability → fm plugins find → ask → install); docs; audits
## Resume here
<!-- auto -->
- 2026-09-26T16:05:04Z steps 4/4 done
- git: foreman/build; 3 uncommitted: plugin/tests/test_docs.py, plugin/tests/test_guard.py, plugin/tests/test_plugins.py
- touched since last checkpoint: plugin/tests/test_plugins.py, plugin/lib/fmplugins.py
## Verification evidence
- (step 1) `python3 -m unittest test_plugins.Find; fm plugins find rust lsp (live)` → RED then OK; live: rust-analyzer-lsp/clangd-lsp etc. with enabled/available and token estimate (2026-09-26T15:55:19Z)
- (step 2) `python3 -m unittest test_plugins.Check test_doctor; fm plugins check; fm doctor (live)` → OK; live: security-guidance@claude-plugins-official Stop hook flagged; doctor WARN 'plugins … (fm plugins check)' (2026-09-26T15:55:19Z)
- (step 2) `python3 -m unittest discover (full); fm doctor` → 319 tests OK; doctor 24 pass, 1 warn (real: security-guidance Stop hook) — supersedes the earlier step 1–2 evidence that was recorded while the suite had a failure (2026-09-26T15:58:02Z)
- (step 3) `python3 -m unittest test_guard.PluginChanges test_plugins.Install test_setup; full suite (exit 0); fm doctor (exit 0); fm docs --strict (exit 0)` → RED (12 failures) then OK: plugin category blocks claude plugin/mcp/config changes and fm plugins install|enable|disable, allowed only with the grant; --allow plugin refused; install records, enable reuses, unknown ids refused; uninstall-user uninstalls recorded plugins (2026-09-26T16:02:11Z)
- (ac 1) `python3 -m unittest test_guard.PluginChanges` → OK: claude plugin/marketplace/mcp/config changes and fm plugins install|enable|disable blocked as plugin (user-only) unless granted (2026-09-26T16:02:55Z)
- (ac 2) `python3 -m unittest test_plugins.Find; fm plugins find rust lsp (live)` → OK; live ranking with source marketplace, state, description and always-on estimate (2026-09-26T16:02:55Z)
- (ac 3) `python3 -m unittest test_plugins.Check test_doctor; fm plugins check; fm doctor (live)` → OK; live security-guidance Stop hook flagged with an action; doctor WARN (2026-09-26T16:02:55Z)
- (ac 4) `python3 -m unittest test_plugins.Install test_setup; python3 plugin/tests/e2e/roundtrip.py` → OK; install records plugins_installed, uninstall-user uninstalls it; roundtrip 17/17 (2026-09-26T16:02:55Z)
- (step 4) `grep 'fm plugins' plugin/rules/foreman.md MASTER.md; fm docs --strict; roundtrip.py` → rules line: missing capability → fm plugins find → fm ask ID plugin → fm plugins install; MASTER/README/CHANGELOG updated; no drift (exit 0); roundtrip 17/17. Audits in progress (2026-09-26T16:03:06Z)
- (step 4) `python3 -m unittest discover -s plugin/tests` → Ran 334 tests OK (exit 0) after intent/adversary/edge fixes (2026-09-26T16:13:56Z)
- (step 4) `python3 -m unittest discover -s plugin/tests; fm doctor; fm plugins check` → 337 tests OK (exit 0); doctor 25 pass 0 warn 0 fail; no conflicts among enabled plugins (2026-09-26T16:22:07Z)
- (step 4) `python3 -m unittest discover -s plugin/tests (after adversary r3 fixes)` → Ran 337 tests OK, exit 0; 8 new guard cases pass (2026-09-26T16:28:18Z)
- (audit intent) `fm-reviewer intent lens over t0016.diff (research t0016-intent): 3 findings (no marketplace path, drifting conflict lists, no keep-through-uninstall) fixed test-first in 6fad281 (add-marketplace, KNOWN_CONFLICTS + drift test, forget)` → ok after fixes; every asked capability (find, check, approved install, marketplaces, conflict-free integration, removable) has a command and a test [tree 1b764a6ded74] (2026-09-26T16:28:18Z)
- (audit adversary) `fm-reviewer adversary lens x3 (research t0016-adversary, -recheck, -r3): 14 bypasses fixed test-first in 6fad281, 8eeb3e1 and the r3 commit; task-scoped grants captured as T-0029` → ok after fixes; remaining gaps are deliberate obfuscation (MASTER §10) and T-0029 [tree 1b764a6ded74] (2026-09-26T16:28:18Z)
- (audit edge) `fm-reviewer edge lens (research t0016-edge): block scalars, multi-scope entries, project enabledPlugins, short words, missing claude, unlanded install, uninstall exit codes, plugin.json hooks/MCP - all fixed test-first in 6fad281` → ok after fixes; stale installPath left as is (claude's own error surfaces) [tree 1b764a6ded74] (2026-09-26T16:28:18Z)
- (audit operator) `fm-reviewer operator lens (research t0016-operator) + live fm plugins check / fm doctor on this machine` → ok after fixes: uninstall keeps failed removals for retry, sync-only Stop-hook conflicts (doctor 25/0/0 live), mutation-only slash matching, MASTER CLI line complete [tree 1b764a6ded74] (2026-09-26T16:28:18Z)
- (audit maintainer) `fm-reviewer maintainer lens (research t0016-maintainer)` → ok after fixes: manifest retry, CLI line, readable name fallback, enable-installs documented in help, 'loop' overlap key removed; KNOWN_CONFLICTS drift test in test_docs [tree 1b764a6ded74] (2026-09-26T16:28:19Z)
- (ac 4) `python3 plugin/tests/e2e/roundtrip.py` → roundtrip: 17/17 checks passed, exit 0 (at 5a67d65) (2026-09-26T16:28:28Z)
## Log
- 2026-09-26T12:44:06Z created
- 2026-09-26T12:51:36Z planned from capture
- 2026-09-26T13:01:15Z user approved core in chat
- 2026-09-26T13:01:42Z set approved=True
- 2026-09-26T13:01:42Z approved by user in chat: 'yes, to all of your things … you have FULL permission for the rest of this session to go full auto'
- 2026-09-26T15:52:22Z focused
- 2026-09-26T15:58:01Z correction: steps 1–2 were recorded and committed (commit before this one) while the full suite had 1 failure (MASTER.md lacked fm plugins; the chain used '| tail -1 &&', which can't fail). Fixed in the next commit; suite 319 OK and doctor 24 pass / 1 warn afterwards
- 2026-09-26T16:28:28Z done
- 2026-09-26T16:28:30Z done
## Follow-ups captured
## Docs impact
MASTER.md (CLI line, section 9 plugins, guard description, section 10 limitations incl. T-0029), CHANGELOG Unreleased, rules line 16 (add-marketplace), evals re-synced, setup-plugins.sh points at KNOWN_CONFLICTS
