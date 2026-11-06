---
id: T-0036
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmplugins.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/lib/fmsync.py, plugin/tests/**, plugin/rules/foreman.md, MASTER.md, CHANGELOG.md, README.md]
depends_on: []
source: followup
created: 2026-09-26T17:28:40Z
updated: 2026-09-26T21:46:26Z
base: 194adbbe6ceca0c010c94c5222f5a2475dc34588
---
# Pin plugin approvals to the plugin and its content: fm ask ID plugin --pin PID; install/enable re-asks when the id differs, the content changed or the yes is over 24 h old
## Raw request
> Plugin approvals pinned to source and content hash, re-ask when upstream content changed (brainstorm security, M)
## Interpretation
Today a plugin yes (fm ask ID plugin) is one-shot but unbound: it lets any one plugin change through, whatever the why text said, and the plugin's content can change between the yes and the install. Bind the yes for installing or enabling a plugin to that plugin id and to a hash of its content at approval time; spending it on anything else, on changed content or after 24 h is refused with a re-ask.
## Assumptions (confidence)
- Claude Code installs from the local marketplace clone (~/.claude/plugins/marketplaces/<mk>), so hashing that copy right before the install covers what gets installed (medium: a marketplace refresh between the check and the copy is a residual window; documented)
- Remote-source entries (source is an object: github/url with ref/sha) have no local copy before install: the pin hashes the marketplace entry, which pins the source only as far as the entry names a sha (high; documented)
- Other plugin-category changes (marketplace add, MCP servers, new skill/agent/command files, claude --settings sessions) keep the unbound one-shot yes; only install/enable carry a content to pin (high)
## Acceptance criteria
- [x] fm ask ID plugin --pin PID records the pin with the grant (dialog and chat paths); the dialog text names PID; an unknown PID is refused — verify with `cd plugin/tests && python3 -m unittest -k pin test_hooks test_cli`
- [x] fm plugins install|enable and claude plugin install|enable spend a plugin yes only for the pinned id, with unchanged content, within 24 h; otherwise blocked with a re-ask message, and the grant stays unspent — verify with `cd plugin/tests && python3 -m unittest -k pin test_hooks`
- [x] pins never travel through fm sync (stripped like allow/approved) — verify with `cd plugin/tests && python3 -m unittest test_sync`
- [x] all gates green: suite, doctor, roundtrip, bench; rules and docs updated — verify with `fm check`
## Non-goals
- Pinning marketplace adds, MCP servers or new skill files
- Verifying the installed copy after the install (Claude Code's cache layout may differ from the source tree)
- Pins for plugin changes made from interpreter code or a prompt's slash command (they still spend the one-shot yes; documented)
## Approach (options → choice → why)
A) The pin rides on the user's yes: fm ask ID plugin --pin PID (the permission dialog shows the command, so the user sees the id); the grant hook stores plugin_pin: [PID, hash, epoch] on the brief; the PreToolUse hook, where the one-shot plugin grant is spent, checks that an install/enable names PID, that the content hash still matches and that the pin is under 24 h old, and clears it with the grant.
B) fm plugins install checks a hash recorded earlier by fm plugins find. Agent-controlled: nothing ties it to what the user approved, and claude plugin install bypasses it.
Choice: A. The check sits in the hook that already spends the grant (one place, covers both fm plugins and claude plugin commands), and the only input is the user-approved command text.
## Risks and rollback
Risk: a hash walk on a large plugin in the hook (rare: only on a grant and on spending it; bounded by the plugin size). Risk: a stricter rule blocks a legitimate install → the message names the exact fm ask to run. Rollback: revert the commit; pins are extra brief meta that older code ignores.
## Execution prompt
Goal: bind a plugin yes for install/enable to the plugin id and its content hash. Repo ~/.claude/foreman, branch foreman/build, core granted for T-0036.
Files: plugin/lib/fmplugins.py (content_hash(pid): installed copy, else the marketplace's local copy, else a hash of the marketplace entry; tree hash skips .git, records symlinks as links), plugin/lib/fmguard.py (install/enable findings end with ' [plugin PID]' for fm plugins install|enable PID and claude plugin install|i|enable PID; '?' when the id can't be read), plugin/lib/fmcli.py (fm ask --pin PID: only with the plugin category, PID must be known to content_hash; pending approvals carry it), plugin/lib/fmhooks.py (_ask_target returns the pin; the dialog text names it; _grant stores plugin_pin: [PID, hash, epoch]; where the plugin grant is spent, _pin_problem refuses a mismatch, changed content or age ≥ APPROVAL_TTL before spending; _use_plugin_grant clears the pin), plugin/lib/fmsync.py (LOCAL_ONLY gains plugin_pin).
Steps: red tests first (test_hooks, test_cli, test_guard, test_plugins, test_sync), implement, docs (rules line on plugins, MASTER §9/§10, CHANGELOG), fm check, five-lens audit via fm audit prep, commit.
Constraints: no network in hooks; hashing only on grant and on spend; fail closed on errors in the spend path.
## Steps
1. [x] red tests: pin recorded on grant (dialog + chat), dialog names it, unknown PID refused, spend refused on wrong id / changed content / expired / no pin, matched spend clears it, guard details carry the target, sync strips plugin_pin, content_hash kinds
2. [x] implement: fmplugins.content_hash, fmguard targets, fm ask --pin, fmhooks grant/spend, fmsync LOCAL_ONLY
3. [x] docs: rules plugins line, MASTER §9 and §10, CHANGELOG; fm check green; commit
4. [x] five-lens audit (fm audit prep T-0036), fix findings test-first, record audits, done
## Resume here
T-0036 step 4: committed f8f3fdb; adversary/edge/intent reviewers running; then operator+maintainer; fix findings test-first; record 5 audits; fm task done T-0036; then final gates + eval, fast-forward main to foreman/build and push both (user approved in AskUserQuestion)
<!-- auto -->
- 2026-09-26T21:26:36Z step 4/4: five-lens audit (fm audit prep T-0036), fix findings test-first, record audits, done
- git: foreman/build; 0 uncommitted
## Docs impact
docs updated: plugin/rules/foreman.md (fm ask ID plugin --pin), MASTER.md (§9 Plugins bullet, §10 limitations on pins), CHANGELOG.md; eval prompts re-synced (plugin/tests/e2e/sync_evals.py); fm docs: no drift
## Verification evidence
- (step 1) `cd plugin/tests && python -m unittest test_hooks.PluginPins test_guard test_plugins.ContentHash test_sync` → red as intended: 65 tests, 15 failures, 1 error (pins, guard targets, content_hash, sync strip not implemented yet) [tree 72be4dced84f] (2026-09-26T21:19:54Z)
- (step 2) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 404 tests in 91.537s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (24 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.4    30.3     150  [0] / SessionEnd                  26.0    26.5     150  [0] [ran] [tree 88fbdf4181c8] (2026-09-26T21:23:41Z)
- (step 3) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 404 tests in 91.437s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (24 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.5    32.4     150  [0] / SessionEnd                  26.4    27.1     150  [0] [ran] [tree b56d8ef2d256] (2026-09-26T21:25:56Z)
- (step 4) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 409 tests in 93.800s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (24 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.8    32.7     150  [0] / SessionEnd                  26.2    27.0     150  [0] [ran] [tree a1d7fce8a078] (2026-09-26T21:35:29Z)
- (step 4) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 409 tests in 93.851s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (24 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.8    32.0     150  [0] / SessionEnd                  26.1    29.1     150  [0] [ran] [tree 53da6c8cf69a] (2026-09-26T21:43:58Z)
- (audit intent) `fm-reviewer intent lens (research t0036-intent)` → changes needed → MEDIUM remote-source pins cover only the marketplace entry: dialog now says so (test_the_dialog_says_when_a_pin_covers_only_a_remote_entry, d7f9d5b); LOW interpreter/slash disclosure superseded (they now spend no yes) [tree 53da6c8cf69a] (2026-09-26T21:44:09Z)
- (audit adversary) `fm-reviewer adversary lens + recheck of the fixes (t0036-adversary, t0036-adversary-recheck); wrapper spellings (npx, env, command, bash -c, sudo, nohup, xargs) probed against fmguard` → changes needed → HIGH pinned yes spent via interpreter code / slash prompt / marketplace add: fixed test-first d7f9d5b (regression test fails on old code, 4 failures); recheck verdict ok; wrappers all resolve to the right target or '?' [tree 53da6c8cf69a] (2026-09-26T21:44:09Z)
- (audit edge) `fm-reviewer edge lens (t0036-edge)` → changes needed → MEDIUM pin not re-checked under the lock, MEDIUM vanished plugin still granted, LOW malformed pin, LOW unreadable file: all fixed test-first d7f9d5b; LOW hash cache skipped (rare path, hashing moved out of the lock in 876f599) [tree 53da6c8cf69a] (2026-09-26T21:44:09Z)
- (audit operator) `fm-reviewer operator lens (t0036-operator)` → ok → LOW newest yes replaces a pin: intended, documented in MASTER (876f599); LOW setup-plugins.sh via Bash hides its installs from the guard: pre-existing, captured T-0039 [tree 53da6c8cf69a] (2026-09-26T21:44:09Z)
- (audit maintainer) `fm-reviewer maintainer lens (t0036-maintainer)` → changes needed → MEDIUM target carried in free text: one producer/parser in fmguard (plugin_mark/plugin_target), test uses the parser; MEDIUM hashing under the project lock: moved before the lock; LOW duplicated id regex → fmguard.PLUGIN_ID; LOW duplicated lookup → fmplugins._pin_source (876f599) [tree 53da6c8cf69a] (2026-09-26T21:44:09Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -k pin test_hooks test_cli` → exit 0 · Ran 9 tests in 3.968s / OK [ran] [tree 53da6c8cf69a] (2026-09-26T21:44:13Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_hooks.PluginPins test_guard` → exit 0 · Ran 53 tests in 4.811s / OK [ran] [tree 53da6c8cf69a] (2026-09-26T21:44:18Z)
- (ac 3) `cd plugin/tests && python3 -m unittest test_sync` → exit 0 · Ran 16 tests in 5.891s / OK [ran] [tree 53da6c8cf69a] (2026-09-26T21:44:24Z)
- (ac 4) `fm doctor && fm docs` → exit 0 · fm doctor: OK (25 pass, 1 warn, 0 fail) / No doc drift in ~/.claude/foreman. [ran] [tree 53da6c8cf69a] (2026-09-26T21:44:30Z)
- (ac 4) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 409 tests in 93.869s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.6    33.7     150  [0] / SessionEnd                  26.3    27.9     150  [0] [ran] [tree 53da6c8cf69a] (2026-09-26T21:46:26Z)
## Log
- 2026-09-26T17:28:40Z created
- 2026-09-26T21:13:09Z user approved core in Claude Code's permission prompt
- 2026-09-26T21:17:57Z planned from capture
- 2026-09-26T21:18:23Z set approved=True
- 2026-09-26T21:18:23Z approved: the user answered 'Build it now' in the AskUserQuestion prompt before going AFK; core granted via fm ask
- 2026-09-26T21:18:23Z focused
- 2026-09-26T21:46:26Z done
## Follow-ups captured
