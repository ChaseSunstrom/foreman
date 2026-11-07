---
id: T-2246
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T00:53:51Z
updated: 2026-10-31T13:36:30Z
builder_model: sonnet
base: 5d9dc235d64f52c912c3453635973c6e3b4323a0
base_tree: caa15554b8559d23818623dd89c8cc88ab25f028
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-10-31T13:23:58Z
plan0_scope: []
verified: strong
---
# A cold-read FAIL blocks only when it quotes, verbatim, the gen-0 line, steer or standing-intent clause it breaks; an ungrounded one is advisory
## Raw request
> PROPOSAL for the user (final report; the cold read is the user's steer 2, so its blocking rule is theirs to change): a cold-read FAIL blocks only when it quotes, verbatim, the gen-0 MUST/NEVER/DONE-WHEN line, steer or standing-intent clause it breaks; an ungrounded objection prints as advisory. Evidence: Mission 3's critique failed 18 puts across whole-file, per-line-accepted and per-section reads, with 1-20 objections a read, some reversing earlier ones (research/draft-critique-initiative.md, T-2221's log)
## Interpretation
The user approved T-2246's proposal (2026-10-31): Mission 3's critique failed 18 cold reads with 1-20 objections each, some reversing earlier ones. The reader must ground each FAIL in the charter it was given; a FAIL with no verbatim clause from that charter prints as advisory and doesn't block the put.
## Assumptions (confidence)
## Acceptance criteria
- [x] The cold-read prompt asks each FAIL for a 'BREAKS: <the clause, verbatim>' line; fmgenesis counts a FAIL as blocking only when that clause appears verbatim (whitespace-normalized) in the charter the reader was given (gen-0's MUST/NEVER/DONE-WHEN lines, steers, standing-intent clauses); others print as advisory, and a file whose only FAILs are advisory is filed — verify with `python3 plugin/tests/run.py test_genesis`
- [x] A reply that quotes a clause not in the charter, or none, can't block; a reply quoting a real MUST blocks as before — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Options: 1) a FAIL blocks only with a verbatim charter clause (BREAKS line, checked in code); 2) a FAIL blocks only if two reads agree; 3) cap objections per read. Choice 1: it is the user-approved proposal, checkable without a model, and it keeps every grounded objection blocking; 2 doubles cost and still admits shared hallucinations.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests with a stubbed reader: a FAIL citing a real NEVER line blocks; one citing an invented clause, or none, is advisory and the put files
2. [x] Add the BREAKS line to the prompt, parse it, check it verbatim against the charter text passed to the reader, demote the rest to advisory (alongside T-2207's existing advisory path)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -30` → exit 0 · Ran 157 tests in 9.8s (17 classes, 16 at a time; slowest: GenesisRead 9s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree ca9dc9c14cb8] (2026-10-31T13:25:15Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -30` → exit 0 · Ran 157 tests in 9.8s (17 classes, 16 at a time; slowest: GenesisRead 9s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree ca9dc9c14cb8] (2026-10-31T13:25:15Z)
- (step 1) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -30` → exit 0 · Ran 157 tests in 9.8s (17 classes, 16 at a time; slowest: GenesisRead 9s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree ca9dc9c14cb8] (2026-10-31T13:25:15Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 157 tests in 10.6s (17 classes, 16 at a time; slowest: GenesisRead 10s, GenesisCheck 8s, GenesisDrift 6s) / OK [ran] [tree ca9dc9c14cb8] (2026-10-31T13:25:30Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_genesis && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.36s] [ran] [tree ca9dc9c14cb8] (2026-10-31T13:25:59Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 159 tests in 14.5s (17 classes, 16 at a time; slowest: GenesisRead 14s, GenesisCheck 11s, GenesisDrift 10s) / OK [ran] [tree 37ba163fe247] (2026-10-31T13:32:08Z)
- `python3 plugin/tests/run.py test_genesis -k quotes_a_charter_clause_verbatim` → ✗ exit 1 · Ran 1 tests in 3.1s (1 classes, 16 at a time; slowest: GenesisRead 1s) / FAILED (1 classes: test_genesis.GenesisRead) (start tree + this task's tests) [ran] [tree 37ba163fe247] (2026-10-31T13:32:21Z)
- `python3 plugin/tests/run.py test_genesis -k quotes_a_charter_clause_verbatim` → exit 0 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: GenesisRead 1s) / OK [ran] [tree 37ba163fe247] (2026-10-31T13:32:21Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 160 tests in 9.2s (17 classes, 16 at a time; slowest: GenesisRead 9s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree caa1e33ccbfb] (2026-10-31T13:35:40Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 160 tests in 9.2s (17 classes, 16 at a time; slowest: GenesisRead 9s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree caa1e33ccbfb] (2026-10-31T13:36:05Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 160 tests in 9.2s (17 classes, 16 at a time; slowest: GenesisRead 9s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree caa1e33ccbfb] (2026-10-31T13:36:05Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 MEDIUM findings fixed test-first (fence-tag and fragment grounding; advisory lines becoming accepted), count mismatch now fails closed, loose count logged` → a FAIL blocks only with a verbatim charter clause (20+ chars or half the line, fence tags excluded); invented, empty, short and tag-only BREAKS are advisory (tested) [tree caa1e33ccbfb] (2026-10-31T13:36:05Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 MEDIUM findings fixed test-first (fence-tag and fragment grounding; advisory lines becoming accepted), count mismatch now fails closed, loose count logged` → advisory lines stay unaccepted, so three ungrounded FAILs then a grounded one still blocks (red→green); a stray quote still fails closed; a parse mismatch fails closed [tree caa1e33ccbfb] (2026-10-31T13:36:05Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 MEDIUM findings fixed test-first (fence-tag and fragment grounding; advisory lines becoming accepted), count mismatch now fails closed, loose count logged` → READ_CHILD change re-reads every tower file once (one-off); exam-tail gaming FAILs are now advisory unless they quote a charter clause, per the user's approved proposal [tree caa1e33ccbfb] (2026-10-31T13:36:05Z)
- (audit operator) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 MEDIUM findings fixed test-first (fence-tag and fragment grounding; advisory lines becoming accepted), count mismatch now fails closed, loose count logged` → genesis_read logs loose; advisory-only sections re-read on each put by design [tree caa1e33ccbfb] (2026-10-31T13:36:05Z)
- (audit maintainer) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 MEDIUM findings fixed test-first (fence-tag and fragment grounding; advisory lines becoming accepted), count mismatch now fails closed, loose count logged` → _grounded reparses the reply in _named's order; kept small rather than widening _named's tuple [tree caa1e33ccbfb] (2026-10-31T13:36:05Z)
## Log
- 2026-10-31T00:53:51Z created
- 2026-10-31T08:34:34Z evidence: gen-1/critique-initiative.md (Mission 3 critique) failed its cold read 3 times, 13 -> 13 -> 17 failed lines, each revision fixing the named facts while the reader raised new ones (including one asking to drop the user's yes-gate on running repo code, T-2202, refused); draft kept at /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/critique-initiative.md; its substance (free arm beats Haiku session arm on s31-006) is captured as T-2297
- 2026-10-31T08:55:52Z blocked: needs the user: the cold read is the user's steer 2; changing how it converges on narrative tower files is their call (final report)
- 2026-10-31T13:21:28Z unblocked
- 2026-10-31T13:21:28Z user approved (2026-10-31 13:2xZ: 'feel free to continue, I approve everything'): unblocked to build
- 2026-10-31T13:23:27Z planned from capture
- 2026-10-31T13:23:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2246.builder.md
- 2026-10-31T13:23:58Z focused
- 2026-10-31T13:23:58Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-10-31T13:31:45Z merged worktree-agent-a32977786b553b85d (2 file(s))
- 2026-10-31T13:31:48Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a32977786b553b85d
- 2026-10-31T13:31:48Z focused
- 2026-10-31T13:32:32Z scope: plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md
- 2026-10-31T13:36:28Z done
- 2026-10-31T13:36:30Z committed 63702c25 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2114 [FIX S, done, 2 steps] FIX S: genesis drift's cold read flags the seed's user-steer section (gen-0 doesn't name… — lesson: A seed that paraphrases gen-0 drifts: q…
- T-2243 [FEATURE M, done, 3 steps] fm genesis put: judge a long narrative tower file section by section (one cold read per… — lesson: Splitting a check into parts must ke…
- T-2191 [FEATURE L, done, 4 steps] The user's standing intent (steer 2026-10-30 #7, STANDING INTENT): file it in the tower… — lesson: A rule that says 'a format check is …
- decision 2026-10-30: [revisited: The user's standing intent (on top of every earlier steer] [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pytho…
## Lessons
- A demotion path (blocking to advisory) must not also promote the line to accepted, or it launders later real findings
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
