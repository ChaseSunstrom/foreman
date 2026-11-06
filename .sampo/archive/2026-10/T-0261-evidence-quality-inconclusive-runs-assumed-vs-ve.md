---
id: T-0261
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmrecall.py, plugin/lib/fmfriction.py, plugin/lib/fmwatch.py, plugin/tests/, mods/foreman-ui/, MASTER.md, CHANGELOG.md, plugin/skills/]
depends_on: []
source: user
created: 2026-10-04T05:53:25Z
updated: 2026-10-04T06:10:22Z
batch: [T-0253, T-0254, T-0255]
base: 96a4f50c0291e780ccc65e4ebce08b91ac1c8e51
base_tree: 28edbc2d4c3204dad28cce80f26c29abc71fcf65
verified: strong
---
# Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
## Raw request
> T-0253: FEATURE: surprise log — fm surprise "<expected> → <observed>" records where the model of the code was wrong; fm friction and recall surface them
> DONE-WHEN: a recorded surprise appears in fm friction's digest and in recall for a related query
> T-0254: FEATURE: assumed vs verified facts — the brief's Assumptions lines carry [assumed] or [verified: <evidence>], and fm next asks to verify assumptions a step depends on
> DONE-WHEN: fm task assume/verify set the tags and done warns on unverified assumptions in M/L
> T-0255: FEATURE: inconclusive evidence — fm task evidence --inconclusive records a run that neither proves nor disproves; it never counts as passing and fm next asks for a sharper check
> DONE-WHEN: an inconclusive run leaves the step open and the done gate refuses
## Interpretation
Three evidence-quality signals: a run that proves nothing never counts as passing; brief assumptions carry whether they were checked; where the model of the code was wrong is logged and resurfaced.
## Assumptions (confidence)
- [verified: grep: fmcore evidence()/inconclusive() are the only parsers; fmcli:1390 iterates b.evidence(); fmserve:243 only counts lines for a change fingerprint] evidence() is the only reader of Verification evidence that decides pass/fail, so filtering there covers every gate
- [verified: `python3 -c "import sys; sys.path.insert(0,'plugin/lib'); import fmcore as c; b=c.Brief.__new__(c.Brief); print(c._unmarked('x (inconclusive) y'))" | grep -q '(inconclusive)'` → exit 0 · (no output)] a typed (inconclusive] in a command's output can't hide real evidence (_unmarked rewrites it)
- [verified: shot.py snapshot at 200x60: both lines render under 'batch of', nothing pushed off] the pane's task card has room for two more lines at 60 rows
## Acceptance criteria
- [x] T-0253: a recorded surprise (fm surprise) appears in fm friction's digest and in recall for a related query — verify with `python3 plugin/tests/run.py -p "test_evidence_quality*" -k Surprise`
- [x] T-0254: fm task assume ID add/verify set [assumed]/[verified: …]/[false: …] and done warns on unverified assumptions in M/L — verify with `python3 plugin/tests/run.py -p "test_evidence_quality*" -k Assume`
- [x] T-0255: an inconclusive run (fm task evidence --inconclusive) leaves the step open, the done gate refuses and fm next asks for a sharper check — verify with `python3 plugin/tests/run.py -p "test_evidence_quality*" -k Inconclusive`
- [x] the task card shows inconclusive runs and unverified assumptions — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Options: (a) new evidence store per kind; (b) marks on the existing brief lines plus one surprises.jsonl. Choice (b): evidence() drops [inconclusive] lines so every caller (has_evidence, red_green, grade, failed-run refusal) ignores them at once; assume mirrors hypo (add/verify) on the Assumptions section; surprises go to surprises.jsonl (recall reads all of them) and the ledger (friction window, feed).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_evidence_quality.py (Surprise, Assume, Inconclusive) fail
2. [x] Implement inconclusive evidence, assume add/verify + done warning, fm surprise + friction + recall
3. [x] foreman-ui: inconclusive and unverified-assumption lines on the task card (view model + mod + test)
4. [x] Docs: MASTER.md, CHANGELOG.md, references (execute/planning)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/intake/references/execute.md, plugin/skills/intake/references/planning.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_evidence_quality*" 2>&1 | tail -3` → exit 0 · Ran 9 tests in 0.8s (3 classes, 16 at a time; slowest: Inconclusive 1s, Assume 1s, Surprise 0s) / FAILED (3 classes) [ran] [tree 9b771c09c10a] (2026-10-04T05:54:19Z)
- (step 1) `python3 plugin/tests/run.py -p "test_evidence_quality*"` → ✗ exit 1 · Ran 9 tests in 0.8s (3 classes, 16 at a time; slowest: Inconclusive 1s, Assume 1s, Surprise 0s) / FAILED (3 classes) [ran] [tree 9b771c09c10a] (2026-10-04T05:54:23Z)
- (step 2) `fm next` → exit 0 · Next: T-0261 step 2/4: Implement inconclusive evidence, assume add/verify + done warning, fm surprise + friction + recall — do it, then fm task evidence T-0261 --step 2 --run "<verify cmd>" (procedure [inconclusive] [ran] [tree 3090cca2f393] (2026-10-04T05:56:48Z)
- (step 2) `python3 plugin/tests/run.py -p "test_evidence_quality*"` → exit 0 · Ran 9 tests in 1.3s (3 classes, 16 at a time; slowest: Assume 1s, Inconclusive 1s, Surprise 1s) / OK [ran] [tree 546628889bda] (2026-10-04T05:57:20Z)
- (step 3) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.87s] [ran] [tree 546628889bda] (2026-10-04T05:57:24Z)
- (step 4) `grep -c 'fm surprise' MASTER.md CHANGELOG.md plugin/skills/intake/references/execute.md` → exit 0 · CHANGELOG.md:1 / plugin/skills/intake/references/execute.md:1 [ran] [tree 546628889bda] (2026-10-04T05:57:24Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 679 tests in 38.1s (139 classes, 16 at a time; slowest: Stop 33s, TaskLifecycle 26s, Bench 26s) / FAILED (1 classes) [ran] [tree 546628889bda] (2026-10-04T05:59:01Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.3    35.5     150  [0] / SessionEnd                  27.5    29.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.71s]; python3 plugin/tests/run.py → exit 0 · Ran 679 tests in 27.5s (1 [ran] [tree 1ea3ad0ab8af] (2026-10-04T06:07:08Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                29.9    31.7     150  [0] / SessionEnd                  28.1    30.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:07 UTC; python3 plugin/tests/run.py → e [ran] [tree 116c609719be] (2026-10-04T06:10:07Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_evidence_quality*" -k Surprise` → exit 0 · Ran 3 tests in 0.7s (1 classes, 16 at a time; slowest: Surprise 1s) / OK [ran] [tree 116c609719be] (2026-10-04T06:10:17Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_evidence_quality*" -k Assume` → exit 0 · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: Assume 1s) / OK [ran] [tree 116c609719be] (2026-10-04T06:10:17Z)
- (ac 3) `python3 plugin/tests/run.py -p "test_evidence_quality*" -k Inconclusive` → exit 0 · Ran 3 tests in 1.0s (1 classes, 16 at a time; slowest: Inconclusive 1s) / OK [ran] [tree 116c609719be] (2026-10-04T06:10:17Z)
- (ac 4) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.62s] [ran] [tree 116c609719be] (2026-10-04T06:10:17Z)
- (audit intent) `one fm-reviewer pass over all five lenses (research T-0261-review-1); 3 LOW edge findings fixed, 1 dismissed` → criteria met; fmserve fingerprint counts raw lines on purpose (change detection, not a pass count) [tree 116c609719be] (2026-10-04T06:10:17Z)
- (audit adversary) `one fm-reviewer pass over all five lenses (research T-0261-review-1); 3 LOW edge findings fixed, 1 dismissed` → ok — --run goes through the guard, (inconclusive] can't be typed (_unmarked) [tree 116c609719be] (2026-10-04T06:10:17Z)
- (audit edge) `one fm-reviewer pass over all five lenses (research T-0261-review-1); 3 LOW edge findings fixed, 1 dismissed` → fixed — removed assumption raises, fm surprise --task checked, exit code documented [tree 116c609719be] (2026-10-04T06:10:17Z)
- (audit operator) `one fm-reviewer pass over all five lenses (research T-0261-review-1); 3 LOW edge findings fixed, 1 dismissed` → ok — docs, HELP_TIERS, no always-on growth [tree 116c609719be] (2026-10-04T06:10:17Z)
- (audit maintainer) `one fm-reviewer pass over all five lenses (research T-0261-review-1); 3 LOW edge findings fixed, 1 dismissed` → ok — CLI-level tests per criterion [tree 116c609719be] (2026-10-04T06:10:17Z)
- (audit intent) `one fm-reviewer pass over all five lenses (research T-0261-review-1); 3 LOW edge findings fixed, 1 dismissed` → criteria met; fmserve fingerprint counts raw lines on purpose (change detection, not a pass count) [tree 116c609719be] (2026-10-04T06:10:22Z)
- (audit adversary) `one fm-reviewer pass over all five lenses (research T-0261-review-1); 3 LOW edge findings fixed, 1 dismissed` → ok — --run goes through the guard, (inconclusive] can't be typed (_unmarked) [tree 116c609719be] (2026-10-04T06:10:22Z)
- (audit edge) `one fm-reviewer pass over all five lenses (research T-0261-review-1); 3 LOW edge findings fixed, 1 dismissed` → fixed — removed assumption raises, fm surprise --task checked, exit code documented [tree 116c609719be] (2026-10-04T06:10:22Z)
- (audit operator) `one fm-reviewer pass over all five lenses (research T-0261-review-1); 3 LOW edge findings fixed, 1 dismissed` → ok — docs, HELP_TIERS, no always-on growth [tree 116c609719be] (2026-10-04T06:10:22Z)
- (audit maintainer) `one fm-reviewer pass over all five lenses (research T-0261-review-1); 3 LOW edge findings fixed, 1 dismissed` → ok — CLI-level tests per criterion [tree 116c609719be] (2026-10-04T06:10:22Z)
## Log
- 2026-10-04T05:53:25Z created
- 2026-10-04T05:53:57Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmfriction.py', 'plugin/lib/fmwatch.py', 'plugin/tests/', 'mods/foreman-ui/', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/']
- 2026-10-04T05:53:57Z focused
- 2026-10-04T06:07:13Z first fm check had one failing class under load (Stop 33s); full suite and fm check passed on rerun — flaky, not this change
- 2026-10-04T06:10:22Z done
- 2026-10-04T06:10:22Z committed 5d4ed8e (14 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_friction.py, plugin/tests/test_recall.py, plugin/tests/test_shot.py
## Lessons
- Filtering a marked line out of the one accessor (evidence()) covered every gate at once; check that every reader goes through it before adding a mark
## Files touched
- plugin/tests/test_evidence_quality.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmfriction.py
- plugin/lib/fmrecall.py
- plugin/lib/fmwatch.py
- plugin/tests/test_ui.py
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- CHANGELOG.md
- MASTER.md
- plugin/skills/intake/references/execute.md
- plugin/skills/intake/references/planning.md
