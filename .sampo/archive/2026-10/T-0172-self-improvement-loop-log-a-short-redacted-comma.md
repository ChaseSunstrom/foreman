---
id: T-0172
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmfriction.py, plugin/tests/test_friction.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-10-03T08:54:00Z
updated: 2026-10-03T09:14:41Z
base: 399524504a7ba4628cc3d6041e9e786109d3d8e8
base_tree: 5901b52e9db13ce4c9a9df9bf24a3a4ec0542a1e
verified: strong
---
# Guard blocks log a short redacted command, and the friction digest shows one per kind
## Raw request
> Self-improvement loop: log a short redacted command with each guard block so the friction digest can ground false positives (pass 2 couldn't ground a state-direct block)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A guard block's event carries the redacted, one-line, 160-character command, and fm friction shows an example per block kind — verify with `python3 plugin/tests/run.py -k test_friction`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red assertion
2. [x] Log and show the command
3. [x] CHANGELOG and MASTER
## Resume here
## Docs impact
MASTER (Self-improvement loop) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_friction` → ✗ exit 1 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: Friction 1s) / FAILED (1 classes) [ran] [tree 2d674eb9c2ee] (2026-10-03T09:13:26Z)
- (step 1) `python3 plugin/tests/run.py -k test_friction` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Friction 1s) / OK [ran] [tree f66dd42f1ef1] (2026-10-03T09:13:36Z)
- (step 2) `python3 plugin/tests/run.py -k test_friction -k test_hooks` → exit 0 · Ran 124 tests in 13.4s (21 classes, 16 at a time; slowest: Stop 13s, Approvals 9s, PromptApprovals 7s) / OK [ran] [tree f66dd42f1ef1] (2026-10-03T09:13:50Z)
- (step 3) `grep -q T-0172 MASTER.md && grep -q T-0172 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 1ea38275e838] (2026-10-03T09:14:39Z)
- (ac 1) `python3 plugin/tests/run.py -k test_friction` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Friction 1s) / OK [ran] [tree 1ea38275e838] (2026-10-03T09:14:40Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 09:14 UTC); cached (fm check --fresh reruns) [ran] [tree 1ea38275e838] (2026-10-03T09:14:40Z)
- (audit adversary) `self: the test blocks npm publish through the real hook and finds the example in the digest; the command passes c.redact before it's written and c.plain/c.fit before it's shown; events.jsonl already holds the category and detail, so this adds one short field` → a command can carry a secret: it is redacted with fmcore's patterns before the event is written and cut to 160 characters; nothing new leaves the machine [tree 1ea38275e838] (2026-10-03T09:14:40Z)
- (audit self) `self: the test blocks npm publish through the real hook and finds the example in the digest; the command passes c.redact before it's written and c.plain/c.fit before it's shown; events.jsonl already holds the category and detail, so this adds one short field` → no findings [tree 1ea38275e838] (2026-10-03T09:14:40Z)
## Log
- 2026-10-03T08:54:00Z created
- 2026-10-03T09:13:22Z planned from capture
- 2026-10-03T09:13:22Z focused
- 2026-10-03T09:14:41Z done
- 2026-10-03T09:14:41Z committed 9feed92 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0154 [FIX S, done, 1 steps] Self-improvement pass waits at least 2 h after the last one, so it has friction to read
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- similar finished tasks took 1–4 steps
- likely tests for the scope: plugin/tests/test_friction.py, plugin/tests/test_hooks.py
## Lessons
- A self-improvement loop needs the raw evidence of each friction, not just its label: the pass couldn't tell a false block from a true one by category.
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmhooks.py
- plugin/lib/fmfriction.py
- CHANGELOG.md
- MASTER.md
