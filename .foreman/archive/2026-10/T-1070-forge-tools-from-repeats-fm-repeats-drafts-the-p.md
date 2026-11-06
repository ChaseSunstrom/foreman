---
id: T-1070
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmrepeats.py, plugin/lib/fmcli.py, plugin/tests/test_repeats.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T06:36:42Z
base: d9f213c19adc2184e76642253cc93fbedef4a1ed
base_tree: 85ec02a3919eface45f7f762995883144240c22f
verified: strong
---
# Forge tools from repeats: fm repeats drafts the project skill or script for a repeated pro
## Raw request
> FEATURE: Forge tools from repeats: fm repeats drafts the project skill or script for a repeated procedure and files it as a task ready to accept (wild C16)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
`fm repeats --forge` takes a repeated command shape or step and drafts the project tool for it, then files it as a captured task ready to accept. Covered already: detection of repeated commands and steps (fmrepeats.py:41 `scan`), suggestions of a gate, script or skill (fmrepeats.py:78 `suggest`), and a playbook draft file (`draft`, fmrepeats.py:105; `--draft`, fmcli.py:4644). Missing: a draft of the actual script or `.claude/skills/<name>/SKILL.md`, and the task that carries it.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a repeated command seeded as in test_repeats, `fm repeats --forge` writes a draft script under research/ and captures one task naming it; run twice, it captures no duplicate — verify with `python3 plugin/tests/run.py test_repeats`
## Non-goals
## Approach (options → choice → why)
(a) A child model writes the tool. (b) Deterministic templates plus a captured task. (c) Only extend `--draft`. Choose (b): free, testable and offline. For a command shape, the draft is `scripts/<kebab>.sh` wrapping the example command, with a "fm check add" line if it is a gate. For a step, it is a SKILL.md skeleton with the step texts from the tasks that share it. Drafts go in research/ like `draft()`. The task is captured with the draft path in its request and a step "review, move into the repo, `fm repeats dismiss`". Never auto-adopt. Add `forge(p, key=None)` in fmrepeats.py and a `--forge` flag on `repeats`. The task is captured through the same capture function the other commands use (find it with `grep "def capture"` in fmcli.py).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: seed three briefs that share the evidence command. `fm repeats --forge --json` returns `{drafts:[{path,task}]}`. The file exists and contains the command. A repeated step gives a SKILL.md draft. A second run files nothing new. A dismissed shape is skipped.
2. [x] Implement `forge` and the flag.
## Resume here
## Docs impact
MASTER.md Forge; CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_repeats` → ✗ exit 1 · Ran 12 tests in 19.7s (3 classes, 16 at a time; slowest: Repeats 20s, Bench 3s, Playbook 2s) / FAILED (1 classes) [ran] [tree bcaf3c600b55] (2026-10-16T06:13:56Z)
- (step 2) `python3 plugin/tests/run.py test_repeats` → exit 0 · Ran 12 tests in 19.3s (3 classes, 16 at a time; slowest: Repeats 19s, Bench 2s, Playbook 1s) / OK [ran] [tree 633f263d87b9] (2026-10-16T06:14:34Z)
- (step 2) `python3 plugin/tests/run.py test_repeats` → ✗ exit 1 · Ran 14 tests in 29.4s (3 classes, 16 at a time; slowest: Repeats 29s, Bench 2s, Playbook 1s) / FAILED (1 classes) [ran] [tree 6028a8e3a932] (2026-10-16T06:27:09Z)
- (step 2) `python3 plugin/tests/run.py test_repeats` → exit 0 · Ran 14 tests in 29.0s (3 classes, 16 at a time; slowest: Repeats 29s, Bench 2s, Playbook 1s) / OK [ran] [tree c1b9d821b15c] (2026-10-16T06:27:44Z)
- (ac 1) `python3 plugin/tests/run.py test_repeats` → exit 0 · Ran 14 tests in 17.6s (3 classes, 16 at a time; slowest: Repeats 17s, Bench 2s, Playbook 1s) / OK [ran] [tree 7fb18416df59] (2026-10-16T06:35:59Z)
- (audit intent) `review: one fm-reviewer pass; 7 findings fixed by the builder test-first (missing draft restored, hashed names against collisions, readable titles and relative keys, quoted YAML description plus a data banner, a real step and criterion, quoted dismiss hint, bullet cap); non-executable mode and token redaction asserted` → repeated manual work becomes a ready draft tool and one task to adopt it [tree 7fb18416df59] (2026-10-16T06:35:59Z)
- (audit adversary) `review: one fm-reviewer pass; 7 findings fixed by the builder test-first (missing draft restored, hashed names against collisions, readable titles and relative keys, quoted YAML description plus a data banner, a real step and criterion, quoted dismiss hint, bullet cap); non-executable mode and token redaction asserted` → drafts are 0644, never run by Foreman, secrets redacted, step text labelled as data; the dismiss hint is shell-quoted [tree 7fb18416df59] (2026-10-16T06:35:59Z)
- (audit edge) `review: one fm-reviewer pass; 7 findings fixed by the builder test-first (missing draft restored, hashed names against collisions, readable titles and relative keys, quoted YAML description plus a data banner, a real step and criterion, quoted dismiss hint, bullet cap); non-executable mode and token redaction asserted` → deleted drafts are restored; shapes sharing a prefix get separate drafts; colons in steps can't break the frontmatter [tree 7fb18416df59] (2026-10-16T06:35:59Z)
- (audit operator) `review: one fm-reviewer pass; 7 findings fixed by the builder test-first (missing draft restored, hashed names against collisions, readable titles and relative keys, quoted YAML description plus a data banner, a real step and criterion, quoted dismiss hint, bullet cap); non-executable mode and token redaction asserted` → titles name the shape or step; one task per draft, never twice [tree 7fb18416df59] (2026-10-16T06:35:59Z)
- (audit maintainer) `review: one fm-reviewer pass; 7 findings fixed by the builder test-first (missing draft restored, hashed names against collisions, readable titles and relative keys, quoted YAML description plus a data banner, a real step and criterion, quoted dismiss hint, bullet cap); non-executable mode and token redaction asserted` → forge() in fmrepeats on capture_once's key dedupe; the step and criterion are added after capture [tree 7fb18416df59] (2026-10-16T06:35:59Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:23:03Z set scope=['plugin/lib/fmrepeats.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_repeats.py']
- 2026-10-16T04:23:03Z set tier=M
- 2026-10-16T06:12:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1070.builder.md
- 2026-10-16T06:12:54Z focused
- 2026-10-16T06:35:30Z merged worktree-agent-aeee0394d57071a7a (3 file(s))
- 2026-10-16T06:35:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aeee0394d57071a7a
- 2026-10-16T06:35:40Z focused
- 2026-10-16T06:35:41Z scope: CHANGELOG.md, MASTER.md — docs for fm repeats --forge
- 2026-10-16T06:36:41Z done
- 2026-10-16T06:36:42Z committed d76f0c2 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_repeats.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmrepeats.py, plugin/tests/test_repeats.py; re-ground the plan against them before editing
## Lessons
- A draft generated from history is untrusted input on its way to becoming code: redact it, never make it executable, label it
## Plan gaps
- failed first: step 1 Failing tests: seed three briefs that share the evidence command. `fm repeats --forge --json` retur…
## Files touched
- plugin/tests/test_repeats.py
- plugin/lib/fmrepeats.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
