---
id: T-1154
type: FIX
tier: S
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-16T10:23:43Z
updated: 2026-10-16T11:02:47Z
base: bb0a8d6fbdea77ccbc2c9e35463020b271ea7c01
base_tree: b50c98be814fdbacd19de5f2d0eea7ab17f9372b
plan0_at: 2026-10-16T10:58:41Z
plan0_scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
verified: strong
---
# Narrow-width card (90 cols): the progress reads '1/3' beside step 2's text, and the next l
## Raw request
> Narrow-width card (90 cols): the progress reads '1/3' beside step 2's text, and the next line repeats the same step ('→ T-1150 step 2/3: …'): show 'step 2/3' once, and use the second line for something new (the next action's verb, or nothing)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the narrow band reads 'step 2/2' (the current step's number) beside that step's text, and no '→' line repeats the current step — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing mod test on the narrow band
2. [x] Step label and the → line skip in register.tsx
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 124 tests across 2 files. [26.43s] [ran] [tree 0d5fc996851f] (2026-10-16T10:59:15Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 124 tests across 2 files. [27.00s] [ran] [tree 35aeacb8843b] (2026-10-16T10:59:52Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 124 tests across 2 files. [11.49s] [ran] [tree 42242982a2bb] (2026-10-16T11:01:12Z)
- `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 2 fail / Ran 124 tests across 2 files. [21.42s] (start tree + this task's tests) [ran] [tree 95e989653c14] (2026-10-16T11:01:53Z)
- `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 124 tests across 2 files. [11.11s] [ran] [tree 95e989653c14] (2026-10-16T11:01:53Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 124 tests across 2 files. [11.03s] [ran] [tree 95e989653c14] (2026-10-16T11:02:04Z)
- (audit edge) `self: both band layouts label the current step (done+1, capped at total); the → line is skipped only when fm next names the active task's step; other next actions still show` → all steps done shows step N/N, not N+1; no active task leaves the → line as before [tree 95e989653c14] (2026-10-16T11:02:04Z)
- (audit self) `self: both band layouts label the current step (done+1, capped at total); the → line is skipped only when fm next names the active task's step; other next actions still show` → no findings [tree 95e989653c14] (2026-10-16T11:02:04Z)
## Log
- 2026-10-16T10:23:43Z created
- 2026-10-16T10:58:40Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'CHANGELOG.md']
- 2026-10-16T10:58:40Z focused
- 2026-10-16T11:02:47Z done
- 2026-10-16T11:02:47Z committed efeb4cd (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- research T-1033-review: Verdict: changes needed.** Acceptance criterion 2 ("idle it shrinks to one summary line") is not implemented, and nothing tests it. I only read t…
- decision 2026-10-03: Self-improvement passes need N closed tasks AND 2 h since the last pass
- similar past tasks were M: consider --tier M
- similar finished tasks took 4–5 steps
## Plan gaps
- failed first: step 1 Failing mod test on the narrow band
- failed first: step 2 Step label and the → line skip in register.tsx
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
