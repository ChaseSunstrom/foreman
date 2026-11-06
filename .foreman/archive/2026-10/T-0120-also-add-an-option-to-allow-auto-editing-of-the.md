---
id: T-0120
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T04:11:36Z
updated: 2026-10-03T04:55:24Z
base: 6e5f87895e2b889200c66d747ff4a35c5094fb84
base_tree: 4e5e744bbf3d5b22cd56f28e20c4dcc190daa4a8
verified: ok
---
# /fm-trust: a switch only you can flip that lets Claude edit the guard and Claude Code settings
## Raw request
> also add an option to allow auto editing of the guard/claude code settings (has to be enabled via /command in CC, not available to the agent) etc.
## Interpretation
User: an option to allow auto-editing of the guard and Claude Code settings, enabled only through a slash command they type in Claude Code, never by the agent.
## Assumptions (confidence)
## Acceptance criteria
- [x] agent can't turn trust on (guard + fm refuse); /fm-trust typed turns it on; trusted: settings and guard edits pass, state never; off works from anywhere — verify with `python3 -m unittest discover -s plugin/tests -q`
- [x] mod: typed /fm-trust runs fm trust on with the marker, a scheduled one is refused; band warns while on — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Options: (a) the mod registers /fm-trust; its command.run checks origin (composer = typed at the prompt, bridge = their phone) and runs fm trust on with FOREMAN_TRUST_FROM=foreman-ui through process.run (not a tool call, so no guard); fm refuses trust on without that marker, and the guard refuses any agent command that runs fm trust on or sets the marker (self-authorize, never grantable); trusted, the guard lets core paths through except Foreman state; (b) a classic skill command detected in UserPromptSubmit. Choice (a): command.run tells a typed command from one the agent scheduled (CronCreate, ScheduleWakeup) or a skill call; UserPromptSubmit can't. Ceiling: the guard is a speed bump, not a sandbox: a script file hiding the call isn't caught; documented.
## Risks and rollback
Risk: weakening the guard. Mitigations: off by default, only a typed command turns it on, Foreman state stays unwritable, the band and session note warn while on, fm trust off from anywhere. Rollback: fm trust off; revert the commit.
## Execution prompt
## Steps
1. [x] red tests (python + mod)
2. [x] fm trust, guard ctx + self-authorize, session note
3. [x] mod /fm-trust + band warning
4. [x] gates, docs, one reviewer pass
## Resume here
## Docs impact
README.md, MASTER.md, CHANGELOG.md, plugin/rules/foreman.md: /fm-trust
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -q -p test_hooks.py -k Trust; claude plugin test mods/foreman-ui` → red: 2 python + 1 mod test fail (2026-10-03T04:36:21Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -q -p test_hooks.py` → exit 0 · Ran 114 tests in 50.289s / OK [ran] [tree 34f47eab529c] (2026-10-03T04:38:20Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -q -p test_hooks.py` → trust tests pass (2026-10-03T04:38:20Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 36 tests across 1 file. [1.77s] [ran] [tree 9b3ad49a87a0] (2026-10-03T04:39:02Z)
- (step 3) `claude plugin test mods/foreman-ui` → 36 pass, validate ok, tsc 0 (2026-10-03T04:39:02Z)
- (step 4) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 537 tests in 157.430s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.6    42.7     150  [0] / SessionEnd                  32.5    38.9     150  [0] [ran] [tree 953a6ffd26c5] (2026-10-03T04:42:12Z)
- (step 4) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 537 tests in 161.582s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.4    35.0     150  [0] / SessionEnd                  28.5    30.2     150  [0] [ran] [tree 953a6ffd26c5] (2026-10-03T04:43:30Z)
- (step 4) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 537 tests in 153.058s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.4    33.0     150  [0] / SessionEnd                  28.4    30.0     150  [0] [ran] [tree 95ffa4b393c7] (2026-10-03T04:47:50Z)
- (step 4) `fm check` → gates exit 0; review finding (quoted marker, substituted 'on') fixed test-first (2026-10-03T04:47:50Z)
- (step 4) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 537 tests in 152.200s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.2    33.5     150  [0] / SessionEnd                  28.6    29.7     150  [0] [ran] [tree e59372c81b38] (2026-10-03T04:52:39Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 537 tests in 152.600s / OK [ran] [tree e59372c81b38] (2026-10-03T04:55:24Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 36 tests across 1 file. [1.74s] [ran] [tree e59372c81b38] (2026-10-03T04:55:24Z)
- (audit intent) `one fm-reviewer pass (research T-0120-review) + automated security review; both env-marker findings resolved by removing the marker` → /fm-trust on, typed by the user, lets Claude edit the guard and Claude Code settings; verified live: the user's typed command wrote state/trust.json [tree e59372c81b38] (2026-10-03T04:55:24Z)
- (audit adversary) `one fm-reviewer pass (research T-0120-review) + automated security review; both env-marker findings resolved by removing the marker` → fm has no 'on'; the record lives in Foreman state, which every tool call is refused (state-direct, not grantable; tested with Write, echo >, tee, cp); the mod accepts only composer/bridge origins (scheduled prompt refused, tested); trust never covers state or whole-tree writes. Known ceiling: the standing yes covers Foreman's own code including enforcement files, as the dialog says [tree e59372c81b38] (2026-10-03T04:55:24Z)
- (audit edge) `one fm-reviewer pass (research T-0120-review) + automated security review; both env-marker findings resolved by removing the marker` → no project view yet → mod falls back to ~/.claude/foreman/state; unreadable or malformed record → not trusted; fm trust off when off is a no-op [tree e59372c81b38] (2026-10-03T04:55:24Z)
- (audit operator) `one fm-reviewer pass (research T-0120-review) + automated security review; both env-marker findings resolved by removing the marker` → band warns while on, session note, fm trust status, ledger trust_on/trust_off [tree e59372c81b38] (2026-10-03T04:55:24Z)
- (audit maintainer) `one fm-reviewer pass (research T-0120-review) + automated security review; both env-marker findings resolved by removing the marker` → one record (c.trust_path/c.trusted) read by guard ctx, session note and view [tree e59372c81b38] (2026-10-03T04:55:24Z)
## Log
- 2026-10-03T04:11:36Z created
- 2026-10-03T04:33:26Z planned from capture
- 2026-10-03T04:33:26Z focused
- 2026-10-03T04:35:38Z user approved core in Claude Code's permission prompt
- 2026-10-03T04:55:24Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0016-adversary: ":"standard","inference_geo":"not_available"},"input_transformations":[],"diagnostics":null,"context_management":null},"apiBlockIndex":0,"reque…
- research t0036-adversary: Confirmed: `check()` returns `Block` only when the category isn't in `ctx.allow`. Since `plugin` is in `ctx.allow` (from the earlier grant), `b…
- playbook Loop Design + Review (skills/playbooks/references/evals/loop-design-check.md)
- research t0016-edge: 901a8c8-aa34-4df7-8164-6500197eb1c7","version":"2.1.280","gitBranch":"foreman/build","slug":"starry-petting-quasar"}
## Lessons
- Authorize through a channel the agent's tools can't reach (a mod writing state directly), not a value the agent could also produce
## Files touched
- mods/foreman-ui/hooks/register.tsx
- plugin/rules/foreman.md
- README.md
- MASTER.md
- CHANGELOG.md
- plugin/tests/test_hooks.py
- plugin/lib/fmguard.py
- plugin/lib/fmcore.py
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmwatch.py
- plugin/tests/test_ui.py
