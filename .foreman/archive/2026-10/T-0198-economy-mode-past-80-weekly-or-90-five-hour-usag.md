---
id: T-0198
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx,mods/foreman-ui/tests/foreman-ui.test.tsx,CHANGELOG.md,MASTER.md]
depends_on: []
source: user
created: 2026-10-03T19:53:58Z
updated: 2026-10-03T19:56:29Z
base: 8ee47b12955616636fb1380a9f06dc6ff09e4114
base_tree: 0b80892925cff16efbd0ed1b79240d0aaf77c46e
verified: strong
---
# Economy mode: past 80% weekly (or 90% five-hour) usage, the system prompt tells Claude to work leaner, and a toast says so once
## Raw request
> Economy mode: past 80% weekly (or 90% five-hour) usage, the system prompt tells Claude to work leaner, and a toast says so once
## Interpretation
The user is usage-sensitive (a session once burned 20% of their weekly quota) and asked for 'more token efficient'. The engine reports the account's rate-limit windows to mods (session.usage / session.measure), but nothing in Foreman reads them, so Claude works the same at 95% weekly as at 5%. Brainstorm round 5 probe (bold bets: quota brake), grounded against the mod API.
## Assumptions (confidence)
## Acceptance criteria
- [x] past a threshold the system prompt carries the economy section and a toast fires once; below it neither — verify with `cd mods/foreman-ui && claude plugin test .`
## Non-goals
## Approach (options → choice → why)
A (chosen): a prompt.compose hook appends one session section, foreman-ui:economy, while a window is past its threshold (seven_day 80, five_hour 90): no brainstorms or multi-round fm ideas, at most one combined reviewer pass, no other subagents unless needed, targeted reads, quiet replies; correctness and the guard unchanged. Its text names the threshold, not the live percent, so it changes the prompt (and its cache) only when crossing. The poll that drives the context meter toasts once on entering. B (rejected): prompt.submit context on each prompt — misses the drive's Stop-hook continuations and repeats the text every prompt. C (rejected): the Python side — hooks never see the rate limits.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] economy section in prompt.compose; toast on entering
3. [x] sync the dev copy, gates, docs
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (economy mode)
## Verification evidence
- (step 1) `cd mods/foreman-ui && claude plugin test .` → ✗ exit 1 · 1 fail / Ran 60 tests across 1 file. [2.63s] [ran] [tree 99a75a0d6c20] (2026-10-03T19:54:09Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → ✗ exit 1 · 1 fail / Ran 60 tests across 1 file. [2.62s] [ran] [tree b1cc667199e6] (2026-10-03T19:54:29Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 60 tests across 1 file. [2.60s] [ran] [tree b3c55dfc23a1] (2026-10-03T19:55:29Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (26 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · skipped: nothing under plugin/**, install.sh changed since its pass at 19:50 UTC; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 19:50 UTC; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 60 tests across 1 file. [2.88s]; pyth [ran] [tree 99cced0e67c2] (2026-10-03T19:56:15Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 60 tests across 1 file. [2.66s] [ran] [tree 99cced0e67c2] (2026-10-03T19:56:29Z)
- (audit intent) `self: the mod test (41% weekly → no section; 84.5% → one session section naming 'past 80%'; 86% → the same text; one toast over two polls); validate passes; the dev copy is synced and loads when this turn ends` → the user's usage sensitivity now reaches the model itself: past the threshold Claude is told to economize without anyone asking, and the person sees one toast saying why [tree 99cced0e67c2] (2026-10-03T19:56:29Z)
- (audit edge) `self: the mod test (41% weekly → no section; 84.5% → one session section naming 'past 80%'; 86% → the same text; one toast over two polls); validate passes; the dev copy is synced and loads when this turn ends` → no rate-limit readings (an API key, before the first response) or usage() failing → no section; both windows hot → one section naming both; a figure hovering at 80 flips the section only on whole-point moves; a mod reload while hot toasts once more (the flag is the module's) [tree 99cced0e67c2] (2026-10-03T19:56:29Z)
- (audit operator) `self: the mod test (41% weekly → no section; 84.5% → one session section naming 'past 80%'; 86% → the same text; one toast over two polls); validate passes; the dev copy is synced and loads when this turn ends` → one appended session section after the engine's (never a shared one after it, which would skip the hook); the text is stable per threshold, so the prompt cache breaks only on crossing; nothing changes below the thresholds [tree 99cced0e67c2] (2026-10-03T19:56:29Z)
## Log
- 2026-10-03T19:53:58Z created
- 2026-10-03T19:53:58Z focused
- 2026-10-03T19:56:29Z done
- 2026-10-03T19:56:29Z committed 7727f91 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0061 [PERFORMANCE M, done, 0 steps] Fm ideas defaults to four lenses (user value, reliability, simplicity, bold bets); the oth
- research brainstorm-20261003-round4: 127 new ideas (6 lenses x 2 rounds, past the 152 of rounds 1-3). Grounded against the code and this session.
- T-0179 [FEATURE M, done, 3 steps] Each reply is a panel: a round-bordered box per message, the closing report accented — lesson: Check a layout change in the live render…
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- similar finished tasks took 0–3 steps
## Lessons
- Measured preferences belong where they act: the user's usage sensitivity lived in a memory note; the engine already pushed the number, and one prompt section turns it into behaviour.
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
- MASTER.md
