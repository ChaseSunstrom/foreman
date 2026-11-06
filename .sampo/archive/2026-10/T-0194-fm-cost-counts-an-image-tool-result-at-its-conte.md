---
id: T-0194
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcost.py,plugin/tests/test_speed.py,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T19:44:53Z
updated: 2026-10-03T19:45:58Z
base: d2450226ea9dd86e83c5354e43ae94f558215c4e
base_tree: 065ddea3c0123c456e908aee1dc6f797f42cd1b5
verified: strong
---
# fm cost counts an image tool result at its context cost, not its base64 length
## Raw request
> fm cost counts an image tool result at its context cost, not its base64 length
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an image result counts as about 1,600 tokens of context — verify with `python3 plugin/tests/run.py -k test_cost_reads_the_transcripts`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] size image blocks at their token cost
3. [x] gates
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_cost_reads_the_transcripts` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Speed 0s) / FAILED (1 classes) [ran] [tree 5d20aac282d1] (2026-10-03T19:44:53Z)
- (step 2) `python3 plugin/tests/run.py -k test_cost_reads_the_transcripts` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Speed 0s) / OK [ran] [tree b6fe21789d2c] (2026-10-03T19:45:00Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.5    34.9     150  [0] / SessionEnd                  28.7    30.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 19:08 UTC; python3 plugin/tests/run.py → e [ran] [tree b6fe21789d2c] (2026-10-03T19:45:52Z)
- (ac 1) `python3 plugin/tests/run.py -k test_cost_reads_the_transcripts` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Speed 0s) / OK [ran] [tree b6fe21789d2c] (2026-10-03T19:45:58Z)
- (audit self) `self-review: only image blocks inside a list content change; text results and string contents are measured as before; the real report moved from Read 85% to Read 59% · Bash 34%` → no findings [tree b6fe21789d2c] (2026-10-03T19:45:58Z)
## Log
- 2026-10-03T19:44:53Z created
- 2026-10-03T19:44:53Z focused
- 2026-10-03T19:45:58Z done
- 2026-10-03T19:45:58Z committed 519881c (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0188 [FEATURE M, done, 3 steps] fm cost says where the time went: the model's against each tool's, shell commands by what they ran — lesson: Measure before speeding up…
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- playbook Context Budget (skills/playbooks/references/context/context-budget.md)
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Lessons
- A size measured in transcript bytes isn't context: base64 images are megabytes on disk and a fixed ~1,600 tokens to the model.
## Files touched
- plugin/tests/test_speed.py
- CHANGELOG.md
- plugin/lib/fmcost.py
