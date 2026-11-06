---
id: T-2616
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_proof.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-11-02T14:18:50Z
updated: 2026-11-02T18:06:28Z
base: c0c2ba3feb21e06716884db8594e2a309b7dd2e5
base_tree: 8be29feb541c56dc01c2cfb5eedab927249210c6
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T14:20:32Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_proof.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# The docs proof kind reads the lines a task itself landed, not every later doc edit
## Raw request
> FIX: the docs proof kind charges a task with every later doc edit: fmcore._need_docs diffs the task's base to HEAD (its own ponytail note), so 416 of the rollup's 601 docs items are CHANGELOG.md and, in a sample of 8, 5 of those tasks added no checkable claim themselves (T-2501: 30 claims to HEAD, 0 in its own commit). Diff base to the task's own landing commit (git log --grep '^T-NNNN:') when one is found, HEAD otherwise
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a task whose own commit adds no checkable doc claim is not listed for docs when a later commit adds one; a task whose own commit adds one still is — verify with `python3 plugin/tests/run.py test_proof.Proof.test_proof_kind_docs_reads_only_the_lines_the_task_itself_landed`
- [x] the proof tests still pass — verify with `python3 plugin/tests/run.py test_proof test_docsdrift`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] diff base to the task's landing commit when found
3. [x] docs: CHANGELOG, MASTER
## Resume here
## Docs impact
CHANGELOG (Unreleased entry); MASTER.md fm prove --rollup line (T-2616 note).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_proof.Proof.test_proof_kind_docs_reads_only_the_lines_the_task_itself_landed` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Proof 0s) / FAILED (1 classes: test_proof.Proof) [ran] [tree 2e2176cce5bd] [world 2f1906870a] (2026-11-02T14:20:43Z)
- (step 2) `python3 plugin/tests/run.py test_proof test_docsdrift` → exit 0 · Ran 55 tests in 18.5s (10 classes, 16 at a time; slowest: Proof 18s, Stop 2s, Meaning 2s) / OK [ran] [tree df9389ab071f] [world 2f1906870a] (2026-11-02T14:21:20Z)
- (step 3) `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 9206091ae195] [world 2f1906870a] (2026-11-02T14:24:22Z)
- (audit edge) `self (S)` → an older task with no id-prefixed commit falls back to HEAD (unchanged behavior); the live (active) task still diffs to the working tree; re.escape keeps the id literal in git's --grep; the memo key and ROLLUP_RULES retire the HEAD-era verdicts, recomputed 40 per call by the existing budget (settled in 5 calls here) [tree 2128e19e7327] (2026-11-02T14:24:34Z)
- (step 3) `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 2128e19e7327] [world 2f1906870a] (2026-11-02T14:24:51Z)
- (step 2) `python3 plugin/tests/run.py test_proof test_docsdrift test_core` → exit 0 · Ran 194 tests in 20.5s (38 classes, 16 at a time; slowest: Proof 20s, ConfidenceRoutes 6s, BriefIndex 3s) / OK [ran] [tree 8356bf5f5fb6] [world 2f1906870a] (2026-11-02T14:26:53Z)
- (step 3) `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree d8545ec805a4] [world 2f1906870a] (2026-11-02T14:28:32Z)
- (ac 1) `python3 plugin/tests/run.py test_proof.Proof.test_proof_kind_docs_reads_only_the_lines_the_task_itself_landed` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Proof 1s) / OK [ran] [tree d8545ec805a4] [world 2f1906870a] (2026-11-02T18:05:54Z)
- (ac 2) `python3 plugin/tests/run.py test_proof test_docsdrift` → exit 0 · Ran 56 tests in 17.3s (10 classes, 16 at a time; slowest: Proof 17s, Stop 2s, Meaning 2s) / OK [ran] [tree d8545ec805a4] [world 2f1906870a] (2026-11-02T18:05:54Z)
- (step 1) `python3 plugin/tests/run.py test_proof.Proof.test_proof_kind_docs_reads_only_the_lines_the_task_itself_landed` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Proof 1s) / OK [ran] [tree d8545ec805a4] [world 2f1906870a] (2026-11-02T18:05:54Z)
- (audit edge) `self (S): diff reviewed; landing-commit diff falls back to HEAD when no id-prefixed commit exists; live task still diffs to the worktree; history files skipped to match fmdocs (T-1817); ROLLUP_RULES in both cache keys retires stale verdicts` → older task with no id-prefixed commit → HEAD (unchanged); re.escape keeps the id literal in --grep; 601 → 421 docs items [tree d8545ec805a4] (2026-11-02T18:05:54Z)
- (audit self) `self (S): diff reviewed; landing-commit diff falls back to HEAD when no id-prefixed commit exists; live task still diffs to the worktree; history files skipped to match fmdocs (T-1817); ROLLUP_RULES in both cache keys retires stale verdicts` → no findings [tree d8545ec805a4] (2026-11-02T18:05:54Z)
## Log
- 2026-11-02T14:18:50Z created
- 2026-11-02T14:20:31Z planned from capture
- 2026-11-02T14:20:32Z focused
- 2026-11-02T14:20:32Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T14:22:53Z hypothesis: under the landing-commit diff the docs count settles well below 601 (sample: 5 of 8 CHANGELOG items had no own claim); the rollup recomputes 40 diffs per call, so it is read once it stops changing
- 2026-11-02T14:23:53Z ruled out: the docs class is mostly real. Settled at 597 of 601: only 70 of the 416 CHANGELOG-first tasks have an id-prefixed commit (older ones landed in merges), and the sample's zero-claim tasks also added --flag lines to MASTER.md themselves. The fix stands for prose-only doc edits from here on; the real lever is proving the claims, not recounting them
- 2026-11-02T14:24:23Z scope: fmcore unproven_summary's cache key gains ROLLUP_RULES so the rule change is recomputed
- 2026-11-02T14:28:32Z scope: widened to the history-file rule: the kind flagged CHANGELOG lines that fm prove --docs never reads (T-1817 skips them), so the run clearing it was hollow; same function, same honesty bug; 601 -> 421
- 2026-11-02T18:06:26Z done
- 2026-11-02T18:06:28Z committed 083fa7c6 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2395 [FEATURE M, done, 4 steps] Proof surfaces (Mission 7, #6/#10): the rollup by kind on MCP, the pane, fm code, the AGENTS.md block, Desktop through MCP and a site p…
- T-2334 [FIX M, done, 2 steps] A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit — lesson: A timeout is not …
- T-2610 [FIX M, done, 3 steps] Calibration reads compare like with like: a close or a task or choice bet counts once its 30-day window finished — lesson: When one read of…
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py
## Lessons
- A proof flag is only honest if the run that clears it reads the same lines: check the clearing verb's skip list when defining what a kind counts
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_proof.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
