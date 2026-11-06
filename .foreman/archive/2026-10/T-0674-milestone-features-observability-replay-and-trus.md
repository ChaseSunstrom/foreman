---
id: T-0674
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:14Z
updated: 2026-10-09T17:20:53Z
batch: [T-0464, T-0483, T-0484]
base: a3de9b785a8f7c9193342061d9b1769e6f90f27e
base_tree: 4c548934bc4bcb62a194948fb9bb8232c07e75a6
verified: strong
---
# Milestone: Features — Observability, replay and trust
## Raw request
> T-0464: FEATURE: Explain why (C064, value 3/5, effort S, risk low)
>   first version: First version: fm explain on a guard block or a drive/Stop decision prints the rule, inputs and ledger events behind it from existing logs (breaker, ledger). Skip per-action keystroke UI and round-trip counts.
>   what it is: Answer why did you do that with causal traces, wall-clock critical paths and budget causality.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0483: FEATURE: Task replay as a scrubbable story (C061, value 3/5, effort M, risk low)
>   first version: First version: fm task show ID --story prints the ledger as chapters (plan, steps, evidence, reviews, close) with times, rendered in the desktop Review tab. Skip time-lapse and shareable receipts (see trust passports).
>   what it is: Replay a finished task or day as a scrubbable timeline, time-lapse or receipt.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0484: FEATURE: Ask the project's memory (C065, value 3/5, effort M, risk low)
>   first version: First version: fm recall --ask QUESTION over briefs, ledger, decisions, research using keyword/BM25 ranking in stdlib (sqlite3 FTS5 is stdlib) with cited task ids. Skip embeddings and OTel export.
>   what it is: Search and question the ledger, history and code by meaning, locally.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 9 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0464, T-0483, T-0484 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0674. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0464: Explain why (C064, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_trust.py -k ExplainBlock`
- [x] T-0483: Task replay as a scrubbable story (C061, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_trust.py -k StoryView`
- [x] T-0484: Ask the project's memory (C065, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_trust.py -k AskMemory`
## Non-goals
## Approach (options → choice → why)
One milestone, three first slices, one test file plugin/tests/test_trust.py: ExplainBlock (fm explain on the last guard block or drive decision prints the rule, its inputs and the ledger events behind it, from existing logs), StoryView (fm task show ID --story: the ledger as chapters with times), AskMemory (fm recall --ask QUESTION: sqlite3 FTS5/BM25 over briefs, ledger, decisions and research, answers cite task ids; stdlib only). Member tests first; per step its own class; full gates once at close.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0464: Explain why (C064, value 3/5, effort S, risk low)
2. [x] T-0483: Task replay as a scrubbable story (C061, value 3/5, effort M, risk low)
3. [x] T-0484: Ask the project's memory (C065, value 3/5, effort M, risk low)
## Resume here
## Docs impact
CHANGELOG entry; MASTER.md Recall and lessons paragraph; fm help entries (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_trust.py` → ✗ exit 1 · Ran 11 tests in 4.6s (3 classes, 16 at a time; slowest: AskMemory 5s, StoryView 2s, ExplainBlock 1s) / FAILED (3 classes) [ran] [tree aafac56a3d84] (2026-10-09T17:11:23Z)
- (step 1) `python3 plugin/tests/run.py -p test_trust.py -k ExplainBlock` → exit 0 · Ran 4 tests in 1.3s (1 classes, 16 at a time; slowest: ExplainBlock 1s) / OK [ran] [tree dcc4ec9484a4] (2026-10-09T17:15:17Z)
- (step 2) `python3 plugin/tests/run.py -p test_trust.py -k StoryView` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: StoryView 1s) / OK [ran] [tree dcc4ec9484a4] (2026-10-09T17:15:24Z)
- (step 3) `python3 plugin/tests/run.py -p test_trust.py -k AskMemory` → exit 0 · Ran 4 tests in 8.3s (1 classes, 16 at a time; slowest: AskMemory 8s) / OK [ran] [tree dcc4ec9484a4] (2026-10-09T17:16:01Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (29 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.3    37.4     150  [0] / SessionEnd                  29.8    32.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 16:32 UTC; python3 plugin/tests/run.py → exit 0 · Ran 1069 tests i [ran] [tree 10dd5e4e4691] (2026-10-09T17:17:49Z)
- (step 1) `python3 plugin/tests/run.py -p test_trust.py -k ExplainBlock` → exit 0 · Ran 4 tests in 2.2s (1 classes, 16 at a time; slowest: ExplainBlock 2s) / OK [ran] [tree c6dd2de95898] (2026-10-09T17:19:57Z)
- (step 1) `python3 plugin/tests/run.py -p test_trust.py -k StoryView` → exit 0 · Ran 3 tests in 2.6s (1 classes, 16 at a time; slowest: StoryView 3s) / OK [ran] [tree c6dd2de95898] (2026-10-09T17:20:00Z)
- (step 1) `python3 plugin/tests/run.py -p test_trust.py -k AskMemory` → exit 0 · Ran 5 tests in 9.8s (1 classes, 16 at a time; slowest: AskMemory 10s) / OK [ran] [tree c6dd2de95898] (2026-10-09T17:20:10Z)
- (ac 1) `python3 plugin/tests/run.py -p test_trust.py -k ExplainBlock` → exit 0 · Ran 4 tests in 1.6s (1 classes, 16 at a time; slowest: ExplainBlock 2s) / OK [ran] [tree 0b9d93405446] (2026-10-09T17:20:52Z)
- (ac 2) `python3 plugin/tests/run.py -p test_trust.py -k StoryView` → exit 0 · Ran 3 tests in 1.7s (1 classes, 16 at a time; slowest: StoryView 2s) / OK [ran] [tree 0b9d93405446] (2026-10-09T17:20:52Z)
- (ac 3) `python3 plugin/tests/run.py -p test_trust.py -k AskMemory` → exit 0 · Ran 5 tests in 6.1s (1 classes, 16 at a time; slowest: AskMemory 6s) / OK [ran] [tree 0b9d93405446] (2026-10-09T17:20:52Z)
- (audit adversary) `main-thread review of the builder's branch (one reviewer was refused by the budget guard): FTS5 MATCH gets quoted [a-z0-9_] words only, so no query syntax gets through; the Stop path only adds a project field to five events; explain and story redact; ask didn't redact on output` → recall --ask passages now redacted on the way out (every write path already redacts; a regression test locks both); FTS5 query built from quoted word tokens, no operators [tree 0b9d93405446] (2026-10-09T17:20:52Z)
- (audit edge) `main-thread review of the builder's branch (one reviewer was refused by the budget guard): FTS5 MATCH gets quoted [a-z0-9_] words only, so no query syntax gets through; the Stop path only adds a project field to five events; explain and story redact; ask didn't redact on output` → no FTS5 in the Python's SQLite falls back to plain recall; archived months read for --story; explain reads the last 20k event lines [tree 0b9d93405446] (2026-10-09T17:20:52Z)
- (audit intent) `main-thread review of the builder's branch (one reviewer was refused by the budget guard): FTS5 MATCH gets quoted [a-z0-9_] words only, so no query syntax gets through; the Stop path only adds a project field to five events; explain and story redact; ask didn't redact on output` → all three members' criteria re-run green on main after the merge [tree 0b9d93405446] (2026-10-09T17:20:52Z)
## Log
- 2026-10-09T15:40:14Z created
- 2026-10-09T16:08:41Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_trust.py -k ExplainBlock`
- 2026-10-09T16:08:42Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_trust.py -k StoryView`
- 2026-10-09T16:08:42Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_trust.py -k AskMemory`
- 2026-10-09T16:08:43Z set approved=True
- 2026-10-09T17:05:01Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0674.builder.md
- 2026-10-09T17:06:18Z focused
- 2026-10-09T17:19:50Z merged worktree-agent-a556e96b471a37748 (5 file(s))
- 2026-10-09T17:20:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a556e96b471a37748
- 2026-10-09T17:20:25Z focused
- 2026-10-09T17:20:52Z done
- 2026-10-09T17:20:53Z committed 21dd857 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0553 [FEATURE M, dropped, 0 steps] Task replay as a scrubbable story (C061, value 3/5, effort M, risk low)
- T-0554 [FEATURE M, dropped, 0 steps] Ask the project's memory (C065, value 3/5, effort M, risk low)
- T-0534 [FEATURE M, dropped, 0 steps] Explain why (C064, value 3/5, effort S, risk low)
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
## Lessons
- Check where secrets enter before adding redaction: every write path here already redacted, so the output redact is defense in depth, and the test is a lock, not a red→green.
## Files touched
- .claude/worktrees/agent-a556e96b471a37748/plugin/tests/test_trust.py
- .claude/worktrees/agent-a556e96b471a37748/plugin/lib/fmhooks.py
- .claude/worktrees/agent-a556e96b471a37748/plugin/lib/fmrecall.py
- .claude/worktrees/agent-a556e96b471a37748/plugin/lib/fmcli.py
- .claude/worktrees/agent-a556e96b471a37748/MASTER.md
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmideas.py
- plugin/lib/fmrecall.py
- plugin/lib/fmrelate.py
- plugin/lib/fmresearch.py
- plugin/lib/fmsession.py
- plugin/tests/test_builder.py
- plugin/tests/test_guard_pipes.py
- plugin/tests/test_panic.py
- plugin/tests/test_secrets.py
- plugin/tests/test_trust.py
