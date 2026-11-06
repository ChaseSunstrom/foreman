---
id: T-0782
type: PERFORMANCE
tier: S
status: dropped
priority: normal
scope: [plugin/hooks/hooks.json, plugin/tests/test_hooks_json.py, plugin/lib/fmdoctor.py]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T16:45:55Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
group: hook latency and output token cost
---
# Reads the outline-first hook can't act on spawn no hook: native if filters scope the Read hook to source files
## Raw request
> PERF: The Read PreToolUse hook earns its spawn or is scoped with a native if filter
> CONTEXT: T-0760, cluster hook-latency (32 ideas). hooks.json:48 spawns Python on every Read (bench p50 74-98 ms per hook). Hook handlers take an "if" permission-rule string (2.1.85) that skips the process when it doesn't match.
> DONE-WHEN: the Read hook's yield over 30 days is measured from the ledger (how often it returned anything); it is scoped with if (or removed) so Reads it never acts on spawn nothing; bench_hooks stays within budget.
## Interpretation
The PreToolUse Read entry (hooks.json) starts Python on every Read to run outline-first (T-0724), which only acts on whole-file reads of source files. Measured over 30 days: 4,186 Reads, 905 whole-file source reads; 1,550 ranged and 1,731 non-source (1,285 of them images) spawned it for nothing. Hook handlers take an if permission rule (2.1.85) that skips the spawn on no match; one handler per source extension the hook knows.
## Assumptions (confidence)
## Acceptance criteria
- [ ] hooks.json's Read entries each carry an if rule for one of the extensions _big_read_note/_outline_first act on, covering all of them, and the plugin validates — verify with `cd plugin/tests && python3 -m unittest test_hooks_json`
- [ ] a real claude -p Read of an image spawns no Foreman hook while a .py Read does (--include-hook-events) — verify with `claude plugin validate --strict plugin`
## Non-goals
## Approach (options → choice → why)
Options: a shell pre-check in the launcher (still a process); drop the hook (loses the measured 4.1M-token saving); one if-scoped handler per extension. Chose if handlers: a missed match only loses a hint, never a safety check (Reads aren't guarded here).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing hooks.json test  <- CURRENT
2. [ ] if-scoped Read handlers; validate
3. [ ] Live check with --include-hook-events
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:09:58Z planned from capture
- 2026-10-14T16:45:55Z dropped: measured: of 4,186 Reads in 30 days 3,281 spawn the hook for nothing, but the hook runs in ~35 ms (bench alone), so if-scoping saves ~2 min/month across all sessions; outline-first also outlines Markdown and any text with definitions (fmmap._DEF), so per-extension if rules (one handler each, no negation for images) would lose token savings worth far more. Not worth 10+ handler entries.
## Follow-ups captured
