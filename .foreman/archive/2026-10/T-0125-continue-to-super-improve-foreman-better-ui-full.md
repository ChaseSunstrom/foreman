---
id: T-0125
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmfriction.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_friction.py, plugin/rules/foreman.md, plugin/skills/reflect/SKILL.md, MASTER.md, CHANGELOG.md, README.md]
depends_on: []
source: user
created: 2026-10-03T04:44:01Z
updated: 2026-10-03T06:52:41Z
base: 3e4452436d13d5bc826cff99f375b7b210159f65
base_tree: 47499cbd10574bde464d8014c34ff26f454c2eab
verified: ok
---
# Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N closed tasks, one read-only subagent turns it into ≤5 grounded fixes filed to the self-inbox
## Raw request
> continue to super improve foreman, better UI, fully capable, way smarter, faster, less token usage, etc. recursive improvement, etc. record and improve based on your own findings of using the plugin yourself and what could be improved, etc.
## Interpretation
The user: 'keep recursively self improving, and know what I mean by that, so you keep improving yourself with sub agents, etc. RSI almost'. Foreman has the parts (reflect, the self-inbox, improve) but nothing starts them, so improvement happens only when the user asks. RSI here: Foreman reads its own friction on a schedule, a subagent turns it into fixes, the drive builds them, and the next pass checks whether those fixes removed the friction (and may tune the loop itself).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm friction prints guard blocks by category with examples, nudges, failed commands, slow gates, drive waits/reloads, corrections and steers, lessons, and the last pass's self items (closed / open / friction that recurred); --brief writes a self-contained subagent brief; --mark records the pass — verify with `python3 plugin/tests/run.py -p test_friction.py`
- [x] fm next says an RSI pass is due at a task boundary after N closed tasks since the last pass, never with --every 0 or a task active — verify with `python3 plugin/tests/run.py -p test_friction.py`
## Non-goals
## Approach (options → choice → why)
A) a digest command + a next-action trigger + one fm-recon subagent per pass (bounded: every N closed tasks, ≤5 findings, read-only agent, items go through the normal queue with tests and audits). B) an always-on background agent watching events: costly, unbounded, and it would edit outside the task discipline. C) only document /foreman:reflect harder: nothing starts it. Choice A; N is a project setting (fm friction --every N, 0 = off), on here.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests
2. [x] fmfriction.py + fm friction + next_for trigger
3. [x] docs: rules line, reflect skill, MASTER, CHANGELOG
4. [x] live: the first pass on Foreman itself (one fm-recon), findings captured --source self
## Resume here
## Docs impact
CHANGELOG; MASTER file map + loop paragraph; rules plain-words line; reflect skill
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_friction.py` → red first (no fm friction), then OK (2026-10-03T06:50:59Z)
- (step 2) `python3 plugin/tests/run.py -p test_friction.py` → OK: digest sections, brief, mark, next trigger every N / off / not mid-task (2026-10-03T06:50:59Z)
- (step 3) `fm check` → gates 5/5 after rules trimmed to 5881 chars and evals re-synced (2026-10-03T06:50:59Z)
- (step 4) `fm friction --brief → one foreman:fm-recon (research rsi-20261003-pass1) → 4 captures → fm friction --mark` → the first pass found 4 grounded fixes (2 spot-checked against the code: auto-evidence tagged ac-only at fmhooks.py:1007; drive_wait logged every Stop at :1257): T-0149 FIX evidence nudge, T-0150 SECURITY backtick exec, T-0151 FEATURE rm $VAR, T-0152 CLEAN drive_wait; pass marked [tree dcd543e7ffa3] (2026-10-03T06:52:27Z)
- (ac 1) `python3 plugin/tests/run.py -p test_friction.py` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: Friction 1s) / OK [ran] [tree dcd543e7ffa3] (2026-10-03T06:52:28Z)
- (ac 2) `python3 plugin/tests/run.py -p test_friction.py` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: Friction 1s) / OK [ran] [tree dcd543e7ffa3] (2026-10-03T06:52:28Z)
- (audit intent) `self-review plus the live first pass` → 'keep recursively self improving … with sub agents … RSI' — a pass now starts itself every 3 closed tasks (fm next), one read-only subagent turns Foreman's friction into grounded fixes that go through the normal queue, and the next digest reports whether those fixes removed their friction; the first pass ran live and filed 4 [tree dcd543e7ffa3] (2026-10-03T06:52:28Z)
- (audit operator) `self-review plus the live first pass` → bounded cost (one read-only fm-recon per 3 tasks, ≤5 findings, a ~4.5k-char digest); off by default elsewhere (--every 0); the digest reads all projects' ledgers (6000-line tails) and 30000 events, ~1 s; nothing edits Foreman outside a task [tree dcd543e7ffa3] (2026-10-03T06:52:28Z)
- (audit intent) `self-review plus the live first pass` → 'keep recursively self improving … with sub agents … RSI' — a pass now starts itself every 3 closed tasks (fm next), one read-only subagent turns Foreman's friction into grounded fixes that go through the normal queue, and the next digest reports whether those fixes removed their friction; the first pass ran live and filed 4 [tree dcd543e7ffa3] (2026-10-03T06:52:41Z)
- (audit operator) `self-review plus the live first pass` → bounded cost (one read-only fm-recon per 3 tasks, ≤5 findings, a ~4.5k-char digest); off by default elsewhere (--every 0); the digest reads all projects' ledgers (6000-line tails) and 30000 events, ~1 s; nothing edits Foreman outside a task [tree dcd543e7ffa3] (2026-10-03T06:52:41Z)
- (audit adversary) `self-review plus the live first pass` → the eval prompts changed only by the mechanical rules re-embed (5 files, one line each: the new plain-words entry); no grader, case or guard logic changed. The digest quotes user words and command targets into a subagent brief: it is read by a read-only agent and its findings are re-grounded and spot-checked before capture, and the brief's text is redacted by the ledger (redact_obj) at write time [tree dcd543e7ffa3] (2026-10-03T06:52:41Z)
## Log
- 2026-10-03T04:44:01Z created
- 2026-10-03T06:38:37Z steer: 'keep recursively self improving, and know what I mean by that, so you keep improving yourself with sub agents, etc. RSI almost' — a standing loop: subagents mine Foreman's own friction (events, ledger, guard blocks, failures, lessons, live snapshots) after each task and file fixes the drive works
- 2026-10-03T06:44:56Z planned from capture
- 2026-10-03T06:44:56Z focused
- 2026-10-03T06:52:41Z scope: plugin/evals/*/prompt.md — sync_evals.py re-embedded the rules (one plain-words line), as test_docs requires
- 2026-10-03T06:52:41Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Loop Design + Review (skills/playbooks/references/evals/loop-design-check.md)
- research t0018-final-intent: HIGH — round 6 shipped with no recorded reviewer audit — `research/` (missing `t0018-r6-*` files) vs `tasks/T-0018-...md:81`.
- research T-0120-review: Verdict
- research brainstorm-20261002-super: 171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:
- likely tests for the scope: plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/rules/foreman.md; re-ground the plan against them before editing
## Lessons
- Self-improvement only recurses if something starts it and the next pass checks the last one's fixes; the parts existed for weeks unused
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmfriction.py
- CHANGELOG.md
- MASTER.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/rules/foreman.md
- plugin/skills/reflect/SKILL.md
