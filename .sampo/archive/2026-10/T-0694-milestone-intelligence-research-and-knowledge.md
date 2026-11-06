---
id: T-0694
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:18Z
updated: 2026-10-09T20:57:50Z
batch: [T-0594, T-0599, T-0600, T-0618, T-0659, T-0660]
base: 4b629289fd127d241c48c860c3e140e8d69accfe
base_tree: 249b4f7ba5e0b986f7d6fc18161dea859b867e3b
verified: strong
---
# Milestone: Intelligence — Research and knowledge
## Raw request
> T-0594: FEATURE: Dependency truth (I085, value 5/5, effort M, risk low)
>   first version: fm deps --calls: for each package behind, grep the project's call sites of imported names and attach release-note questions; plus a hook-free 'fm probe' note in intake that checks the installed version's source/--help before trusting docs. Start with installed version vs latest and import-site listing.
>   what it is: Closes the knowledge-cutoff gap by probing installed dependencies, release notes and upstream.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0599: FEATURE: Question-first research (I083, value 4/5, effort S, risk low)
>   first version: Make fm research ask end its note with a Decision section: recommendation plus 'would change if' lines, from the same child call; tie to the RESEARCH task finish.
>   what it is: Builds a question tree before reading, stops when the decision stops moving, and ends in a memo saying what would change it.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0600: FEATURE: Domain pitfall packs (I089, value 4/5, effort S, risk low)
>   first version: Chesterton gate as a CLEAN-type step: fm next on a task that deletes files or lines runs fm why on them and requires one line of origin per deletion in the brief (warning, not a hard block). Pitfall packs skipped.
>   what it is: Collects pitfalls per domain and runs reference-frame voting.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0618: FEATURE: Prior art (I086, value 4/5, effort M, risk med)
>   first version: fm recall --repos: grep/ripgrep other registered projects (fm projects) for the request's identifiers and titles, local read-only, redact per share rules; cite file:line. FEATURE L intake lists hits in Approach.
>   what it is: Searches the user's repos and the market before building.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0659: FEATURE: Project knowledge base (I087, value 3/5, effort M, risk low)
>   first version: fm recall --explain QUESTION: a cited walkthrough from fm map, fm why and outline hits via fm second child; start by emitting the file:line citations without a child.
>   what it is: Keeps verified facts, glossaries and cited walkthroughs of how things work.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0660: FEATURE: Known-world map and idle study (I088, value 3/5, effort M, risk low)
>   first version: Cheap first step: fm night job that tracks which files the sessions never read (from transcripts/ledger) in fm map hot-vs-cold, then queues a recon of cold hot-path files as research debt. Skip curiosity engine and git-blame style.
>   what it is: Maps what has never been read and studies dependencies and changelogs when idle.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 9 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0594, T-0599, T-0600, T-0618, T-0659, T-0660 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0694. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0594: Dependency truth (I085, value 5/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_knowledge.py -k Deps`
- [x] T-0599: Question-first research (I083, value 4/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_knowledge.py -k Decision`
- [x] T-0600: Domain pitfall packs (I089, value 4/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_knowledge.py -k Chesterton`
- [x] T-0618: Prior art (I086, value 4/5, effort M, risk med) works — verify with `python3 plugin/tests/run.py -p test_knowledge.py -k PriorArt`
- [x] T-0659: Project knowledge base (I087, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_knowledge.py -k Explain`
- [x] T-0660: Known-world map and idle study (I088, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_knowledge.py -k Cold`
## Non-goals
## Approach (options → choice → why)
Options: (a) an indexing service over every project (embeddings, a docs crawler); (b) local, on-demand reads with git grep and what Foreman already records; (c) model children for each answer. Choice: (b), model-free first versions and local only (the user wants everything private and local). Deps: fm deps --calls lists each dependency's installed version (read locally) and its import sites with the names used, no network; planning.md says to probe the installed version before trusting docs. Research: every fm research ask note ends with a Decision prompt naming the task's Decision section, and a RESEARCH task closing without one warns. Chesterton: closing a task that deleted files warns until an Origins section says why each existed (fm why). Prior art: fm recall --repos greps other registered projects that opted into sharing (fm share on) and aren't sensitive, citing file:line, lines redacted. Explain: fm recall --explain cites the definitions of the identifiers a question names. Cold map: fm map --cold lists the most-changed files no session has read (events' Read targets); --capture files one inbox item, a free night job runs it, and research debt skips it (local files never go to web research).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0594: Dependency truth (I085, value 5/5, effort M, risk low)
2. [x] T-0599: Question-first research (I083, value 4/5, effort S, risk low)
3. [x] T-0600: Domain pitfall packs (I089, value 4/5, effort S, risk low)
4. [x] T-0618: Prior art (I086, value 4/5, effort M, risk med)
5. [x] T-0659: Project knowledge base (I087, value 3/5, effort M, risk low)
6. [x] T-0660: Known-world map and idle study (I088, value 3/5, effort M, risk low)
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md (Unreleased: research and knowledge), ~/.claude/foreman/MASTER.md (fmrecall, fmmap, fmoutside), ~/.claude/foreman/plugin/skills/intake/references/planning.md (R2 probes)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_knowledge.py` → ✗ exit 1 · Ran 6 tests in 0.4s (6 classes, 16 at a time; slowest: PriorArt 0s, Decision 0s, Chesterton 0s) / FAILED (6 classes) [ran] [tree dbedaa709421] (2026-10-09T20:53:33Z)
- (step 1) `python3 plugin/tests/run.py -p test_knowledge.py -k Deps` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Deps 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:56:20Z)
- (step 2) `python3 plugin/tests/run.py -p test_knowledge.py -k Decision` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Decision 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:56:21Z)
- (step 3) `python3 plugin/tests/run.py -p test_knowledge.py -k Chesterton` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Chesterton 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:56:21Z)
- (step 4) `python3 plugin/tests/run.py -p test_knowledge.py -k PriorArt` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: PriorArt 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:56:22Z)
- (step 5) `python3 plugin/tests/run.py -p test_knowledge.py -k Explain` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Explain 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:56:22Z)
- (step 6) `python3 plugin/tests/run.py -p test_knowledge.py -k Cold` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Cold 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:56:23Z)
- (ac 1) `python3 plugin/tests/run.py -p test_knowledge.py -k Deps` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Deps 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:57:49Z)
- (ac 2) `python3 plugin/tests/run.py -p test_knowledge.py -k Decision` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Decision 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:57:49Z)
- (ac 3) `python3 plugin/tests/run.py -p test_knowledge.py -k Chesterton` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Chesterton 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:57:49Z)
- (ac 4) `python3 plugin/tests/run.py -p test_knowledge.py -k PriorArt` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: PriorArt 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:57:49Z)
- (ac 5) `python3 plugin/tests/run.py -p test_knowledge.py -k Explain` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Explain 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:57:49Z)
- (ac 6) `python3 plugin/tests/run.py -p test_knowledge.py -k Cold` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Cold 0s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:57:49Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1225 tests in 72.3s (396 classes, 16 at a time; slowest: Stop 47s, TaskLifecycle 30s, Bench 28s) / OK [ran] [tree f0785475f6f8] (2026-10-09T20:57:49Z)
- (audit intent) `main-thread review of the diff against the six first versions; explain, cold map and deps --calls tried on this project` → all six first versions shipped local and model-free; the research decision is written by the session that holds the context (a prompt in the note plus a close warning), not by another child call, which keeps research ask's cost unchanged [tree f0785475f6f8] (2026-10-09T20:57:49Z)
- (audit adversary) `main-thread review of the diff against the six first versions; explain, cold map and deps --calls tried on this project` → prior art reads only projects that opted in with fm share on and aren't sensitive, lines redacted; cold-file items are kept out of the night research-debt job so local file names never go to web research; deps --calls makes no network call (tested with a dead proxy) [tree f0785475f6f8] (2026-10-09T20:57:49Z)
- (audit edge) `main-thread review of the diff against the six first versions; explain, cold map and deps --calls tried on this project` → fixed: a new explain() was shadowed by the existing fm explain function of the same name (renamed where_defined); deletions are measured against the task's start commit, committed or not; one open cold-file item at a time (tested twice) [tree f0785475f6f8] (2026-10-09T20:57:49Z)
## Log
- 2026-10-09T15:40:18Z created
- 2026-10-09T20:53:06Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_knowledge.py -k Deps`
- 2026-10-09T20:53:06Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_knowledge.py -k Decision`
- 2026-10-09T20:53:07Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_knowledge.py -k Chesterton`
- 2026-10-09T20:53:07Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_knowledge.py -k PriorArt`
- 2026-10-09T20:53:07Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_knowledge.py -k Explain`
- 2026-10-09T20:53:07Z criterion 6 verify: `` → `python3 plugin/tests/run.py -p test_knowledge.py -k Cold`
- 2026-10-09T20:53:07Z focused
- 2026-10-09T20:57:50Z done
- 2026-10-09T20:57:50Z committed 1bf6d2e (11 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 3–7 steps
## Lessons
- Privacy rules belong in the data path, not the docs: the opt-in and sensitive checks sit in the function that reads other projects, and the web-research job filters what it may send
## Plan gaps
- failed first: step 1 T-0594: Dependency truth (I085, value 5/5, effort M, risk low)
## Files touched
- plugin/tests/test_knowledge.py
- plugin/lib/fmcli.py
- plugin/lib/fmoutside.py
- plugin/lib/fmmap.py
- plugin/lib/fmnight.py
- plugin/tests/test_night.py
- plugin/lib/fmresearch.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/intake/references/planning.md
