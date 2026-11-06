---
id: T-0262
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/, plugin/tests/, mods/foreman-ui/, MASTER.md, CHANGELOG.md, plugin/skills/]
depends_on: []
source: user
created: 2026-10-04T06:10:25Z
updated: 2026-10-04T06:22:22Z
batch: [T-0256, T-0247, T-0250]
base: 5d4ed8e2aa0be30920b0d735ba07c3ed9c680411
base_tree: 116c609719be39a1d3676820c9f9894c82ee014b
verified: strong
---
# Smarter nudges: already-covered requests, decision revisit triggers, quieter ignored hints
## Raw request
> T-0256: FEATURE: could this task be avoided — fm task new and intake check recall and the map for an existing command or feature that already covers the request and say so first
> DONE-WHEN: a request matching an existing fm command's help text gets the note
> T-0247: FEATURE: decision revisit triggers — fm decide --revisit "after DATE | when PATH changes" and fm next surfaces a decision whose trigger fired
> DONE-WHEN: a decision with a path trigger shows in fm next after that file changes
> T-0250: FEATURE: fm next quiets ignored hints — a hint kind ignored many times with no later failure is shortened, and restored when its absence correlates with a failed gate
> CONTEXT: fm cost counts next followed/ignored (fmcost.py)
> DONE-WHEN: after N ignored hints of one kind the injected Next line drops that hint's detail
## Interpretation
Three nudges that make fm next and intake smarter: don't build what an fm command already does, re-check a decision when the facts under it move, and stop repeating a hint that is ignored until ignoring it costs a failed gate.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0256: fm capture and fm task new say first when an fm command's help already covers the request — verify with `python3 plugin/tests/run.py -p "test_nudges*" -k Covered`
- [x] T-0247: fm decide --revisit "after DATE | when PATH changes"; fm next surfaces a decision whose trigger fired until fm decide --revisited — verify with `python3 plugin/tests/run.py -p "test_nudges*" -k Revisit`
- [x] T-0250: a next hint (batch, skills) shown QUIET_AFTER times without use drops its detail; using it or a failed gate restores it — verify with `python3 plugin/tests/run.py -p "test_nudges*" -k QuietHints`
- [x] the pane shows a fired decision trigger — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Covered: fmrecall.covered() matches the request's tokens against every fm command's help (≥3 shared, ≥60% of the help's words) — reuses recall's tokenizer, no new index. Revisit: a [revisit: …] tag in the decisions.md row (path triggers keep a content hash), parsed by fmcore.fired_decisions() in next_for; --revisited WORDS settles one. Hints: hints.json per project (ignored counts and the kinds last shown) updated where UserPromptSubmit injects Next, reset by fm batch / the Skill tool / a failed fm check; next_for renders the short form past QUIET_AFTER. Rejected: scanning events.jsonl at each injection (slow on a big log).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_nudges.py (Covered, Revisit, QuietHints) fail
2. [x] Implement covered(), --revisit/--revisited + fired_decisions in next_for, hints.json counters + quiet forms
3. [x] foreman-ui: fired decision triggers in the view and pane
4. [x] Docs: MASTER.md, CHANGELOG.md
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_nudges*"` → ✗ exit 1 · Ran 7 tests in 0.5s (3 classes, 16 at a time; slowest: Revisit 0s, QuietHints 0s, Covered 0s) / FAILED (3 classes) [ran] [tree 94b9533844e2] (2026-10-04T06:11:33Z)
- (step 2) `python3 plugin/tests/run.py -p "test_nudges*"` → exit 0 · Ran 8 tests in 1.0s (3 classes, 16 at a time; slowest: QuietHints 1s, Revisit 1s, Covered 0s) / OK [ran] [tree f977f0b2bceb] (2026-10-04T06:13:25Z)
- (step 3) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.72s] [ran] [tree d985488683ec] (2026-10-04T06:14:10Z)
- (step 4) `grep -c 'revisit' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:2 / CHANGELOG.md:2 [ran] [tree 66380ecb58b3] (2026-10-04T06:14:22Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 688 tests in 28.5s (142 classes, 16 at a time; slowest: Stop 21s, TaskLifecycle 19s, Parallel 18s) / FAILED (1 classes) [ran] [tree 66380ecb58b3] (2026-10-04T06:16:13Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail) (slower: 9.3 s vs a usual 6.0 s); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                42.0    42.8     150  [0] / SessionEnd                  38.3    55.0     150  [0] (slower: 16.0 s vs a usual 10.6 s); claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** [ran] [tree 5662d6096404] (2026-10-04T06:19:01Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                29.7    31.2     150  [0] / SessionEnd                  27.5    29.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:16 UTC; python3 plugin/tests/run.py → e [ran] [tree 54c332d82718] (2026-10-04T06:22:11Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_nudges*" -k Covered` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Covered 0s) / OK [ran] [tree 54c332d82718] (2026-10-04T06:22:22Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_nudges*" -k Revisit` → exit 0 · Ran 6 tests in 1.3s (1 classes, 16 at a time; slowest: Revisit 1s) / OK [ran] [tree 54c332d82718] (2026-10-04T06:22:22Z)
- (ac 3) `python3 plugin/tests/run.py -p "test_nudges*" -k QuietHints` → exit 0 · Ran 3 tests in 1.0s (1 classes, 16 at a time; slowest: QuietHints 1s) / OK [ran] [tree 54c332d82718] (2026-10-04T06:22:22Z)
- (ac 4) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.61s] [ran] [tree 54c332d82718] (2026-10-04T06:22:22Z)
- (audit intent) `one fm-reviewer pass over all five lenses (research T-0262-review-1); 2 MEDIUM + 3 LOW fixed with tests, rest accepted` → criteria met; covered() now also needs 25% of the request's words (long pastes were noise) [tree 54c332d82718] (2026-10-04T06:22:22Z)
- (audit adversary) `one fm-reviewer pass over all five lenses (research T-0262-review-1); 2 MEDIUM + 3 LOW fixed with tests, rest accepted` → fixed — fire-time path containment; only fm's leading tag run fires or settles [tree 54c332d82718] (2026-10-04T06:22:22Z)
- (audit edge) `one fm-reviewer pass over all five lenses (research T-0262-review-1); 2 MEDIUM + 3 LOW fixed with tests, rest accepted` → fixed — tag parsing from the leading run, settle words whole and 4+ chars, decision text can't open with a tag, hint writes swallow OSError and skip no-op writes; trailing-backslash cell split left (cosmetic) [tree 54c332d82718] (2026-10-04T06:22:22Z)
- (audit operator) `one fm-reviewer pass over all five lenses (research T-0262-review-1); 2 MEDIUM + 3 LOW fixed with tests, rest accepted` → ok — docs updated, hooks wrap every hint call, no always-on growth [tree 54c332d82718] (2026-10-04T06:22:22Z)
- (audit maintainer) `one fm-reviewer pass over all five lenses (research T-0262-review-1); 2 MEDIUM + 3 LOW fixed with tests, rest accepted` → ok — re-arm, forged-tag, long-paste tests added; 'ignored' = Next changed again, accepted as the proxy [tree 54c332d82718] (2026-10-04T06:22:22Z)
## Log
- 2026-10-04T06:10:25Z created
- 2026-10-04T06:11:21Z set scope=['plugin/lib/', 'plugin/tests/', 'mods/foreman-ui/', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/']
- 2026-10-04T06:11:21Z focused
- 2026-10-04T06:22:22Z done
- 2026-10-04T06:22:22Z committed 4cb043a (12 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- research brainstorm-20261003-round6: Runs: brainstorm-20261003-230652 (5 lenses + deepen 3: 78 new titles) and brainstorm-20261003-230844 (4 lenses + deepen 2: 61 new ti…
- research T-0108-review: [instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok [stale: mods/foreman-ui/hooks/register.tsx, plugin/lib/f…
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_budget.py, plugin/tests/test_core.py, plugin/tests/test_docs.py, plugin/tests/test_doctor.py, plugin/tests/test_evolve.py, plugin/tests/test_friction.py,…
## Lessons
- Text Foreman later parses for tags must be parsed only from the run fm itself writes, never by searching the whole row: user text in other cells forges or settles them
## Files touched
- plugin/tests/test_nudges.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- plugin/lib/fmhooks.py
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmwatch.py
- plugin/tests/test_ui.py
- CHANGELOG.md
- MASTER.md
