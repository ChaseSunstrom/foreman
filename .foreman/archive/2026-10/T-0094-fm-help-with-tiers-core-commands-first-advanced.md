---
id: T-0094
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_help.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-02T19:52:49Z
updated: 2026-10-03T08:16:08Z
base: cde655d5d951b1991e4a5f2e733fc5019282d299
base_tree: ed23e17b02250ed6a3aa21e6b04387c16ce40b96
verified: ok
---
# fm help: every command once, in tiers, everyday ones first; fm alone prints it
## Raw request
> fm help with tiers (core commands first, advanced, internal)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm help lists every registered command exactly once under tier headings, the everyday tier first, and bare fm prints the same — verify with `python3 plugin/tests/run.py -k test_help`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test
2. [x] Tiers and cmd_help; bare fm prints it
3. [x] CHANGELOG
## Resume here
## Docs impact
MASTER (Commands line) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_help` → exit 0 · Ran 2 tests in 0.4s (2 classes, 16 at a time; slowest: PromptApprovals 0s, Help 0s) / OK [ran] [tree a694a2113043] (2026-10-03T08:15:25Z)
- (step 2) `python3 plugin/tests/run.py -k test_help` → exit 0 · Ran 2 tests in 0.4s (2 classes, 16 at a time; slowest: PromptApprovals 0s, Help 0s) / OK [ran] [tree a694a2113043] (2026-10-03T08:15:25Z)
- (step 3) `grep -q T-0094 CHANGELOG.md` → exit 0 · (no output) [ran] [tree a694a2113043] (2026-10-03T08:15:25Z)
- (ac 1) `python3 plugin/tests/run.py -k test_help` → exit 0 · Ran 2 tests in 0.4s (2 classes, 16 at a time; slowest: PromptApprovals 0s, Help 0s) / OK [ran] [tree a694a2113043] (2026-10-03T08:16:08Z)
- (ac 2) `fm check` → exit 0 · ✓ claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 57 tests across 1 file. [2.42s] (2.5 s) / ✓ python3 plugin/tests/run.py → exit 0 · Ran 566 tests in 19.8s (115 classes, 16 at a time; slowe [ran] [tree a694a2113043] (2026-10-03T08:16:08Z)
- (audit self) `self: the test derives the command list from the parser, so a new command without a tier fails it; bare fm prints the same text; --json gives the tiers` → no findings [tree a694a2113043] (2026-10-03T08:16:08Z)
## Log
- 2026-10-02T19:52:49Z created
- 2026-10-03T08:14:18Z planned from capture
- 2026-10-03T08:14:18Z focused
- 2026-10-03T08:14:37Z scope: MASTER.md — the self-docs check needs every command named there
- 2026-10-03T08:16:08Z done
- 2026-10-03T08:16:08Z committed 622d526 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0036-intent: MEDIUM** — `plugin/lib/fmplugins.py:388-398` (`content_hash`) — For a plugin that is not locally mirrored by its marketplace (a genuinely remote s…
- research t0016-maintainer: ds failures from removing tracked plugins/marketplaces only as a print statement (`err = ...; print(f\"Could not remove {what} {name}: {err}\"…
- research t0063-final-review: MEDIUM — `plugin/lib/fmcore.py:842-845` (FIX red→green requirement) and `plugin/lib/fmcli.py:71-73` (M/L lesson requirement) — the user expl…
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
## Preflight
Changed in scope since this was planned (2026-10-02): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Lessons
- A help index that a test derives from the parser can't drift from the commands.
## Files touched
- plugin/tests/test_help.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
