# Rounds 4-6 slate (T-0018), from research/brainstorm-20260926-122701 (6 lenses, ~45 ideas)

## Grounded out (premise already true)
- drive no-progress watchdog: exists (fmhooks _progressed + DRIVE_MAX 50) · eval rules drift test: exists (test_docs.test_eval_cases_embed_the_current_rules) · atomic/locked state writes: exist (write_atomic + lock) · hook latency regression: bench_hooks is an fm check gate (exits 1 over budget) · sync import lockdown: done in round 3 · rules copy generation: sync_evals.py + test · TaskCompleted removal: keep (enabled by CLAUDE_CODE_ENABLE_TODO_TOOLS).
## Rejected (risk or value)
- guard fast path (p95 fine; risk of skipping a check) · fm check parallel/cached verdicts (masks flaky gates) · serve unit ProtectSystem=strict (read-only home breaks Claude's work) · scope-declared guard relaxation (high risk) · heuristic rewrite to shlex-only (the coarse interpreter heuristics are deliberate; audit-found cases already in tests).
## Slate (value/effort/risk)
Round 4 — safety
1. Guard falls back to the committed fmguard when the working copy raises (T-0033) · 5/M/med · all lenses
2. Persistence vectors gated as `system`: crontab, shell rc files, .git/hooks · 4/M/med · security
3. Terminal-safe text: control characters stripped from titles and text the dashboard/statusline print · 3/S/low · security
4. fm sync export redacts secrets; import skips oversize files · 4/S/low · security
Round 5 — workflow
5. `fm research add NAME --from-agent FILE` keeps a subagent's final report (not the transcript tail) + `fm audit prep --note` (T-0031) · 4/S/low · user value, reliability, simplicity, bold
6. `fm task drop ID --done-in T-XXXX`: done inside another task, shown as done (T-0032) · 3/S/low
7. Statusline/progress show the current step's label (umbrella rounds visible) · 3/S/low · user value, simplicity
8. fm doctor names the latest hook error's cause · 3/S/low · reliability
Round 6 — performance, measured first
9. fm sync incoming(): (mtime,size) cache before hashing · 2/S/low
10. Hook import-time check (python -X importtime) and lazy imports where it measurably helps · 2/S/low
## Follow-ups (captured, not in the slate)
- fm audit run: headless read-only lens reviewers with a structured findings file (L)
- fm eval capture: eval cases from real task histories (L)
- plugin approvals pinned to source + content hash (M)
