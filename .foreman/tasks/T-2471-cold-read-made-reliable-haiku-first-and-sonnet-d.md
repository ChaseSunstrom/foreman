---
id: T-2471
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T14:55:07Z
updated: 2026-11-01T15:14:43Z
rival_at: 2026-11-01T14:55:54Z
rival_split: true
base: cd2f93a3bc598623a4c718c454ef2acddf4e0a97
base_tree: cf26b7a3299c8e2f51ecce2284f8a004b0053c2c
plan0_at: 2026-11-01T14:56:07Z
plan0_scope: []
verified: strong
---
# Cold read made reliable: Haiku first and Sonnet decides on a non-pass, a FAIL counts only with the quoted line and the MUST/NEVER or steer it breaks, verdicts cached by content hash, Haiku dropped past a third overruled
## Raw request
> Cold read made reliable: Haiku first and Sonnet decides on a non-pass, a FAIL counts only with the quoted line and the MUST/NEVER or steer it breaks, verdicts cached by content hash, Haiku dropped past a third overruled
## Interpretation
Readings: (a) the four rules apply to the tower-filing cold read (fmgenesis._read1/_read, READ_CHILD), the one that kept failing Missions 5-8 and the critiques; (b) every model read in Genesis (drift, novelty) too. (a): the user's call answers the parked question about the tower-filing read; drift and novelty are separate readers with their own rules. Outcome: puts converge; round 1's filings resume.
## Assumptions (confidence)
## Acceptance criteria
- [x] Haiku's non-pass goes to Sonnet, whose verdict stands; disagreements are logged and Haiku is dropped past a third overruled (3+ FAILs) — verify with `python3 plugin/tests/run.py test_genesis`
- [x] a FAIL without a quoted file line and a gen-0 MUST/NEVER or steer is a note and the file is filed; unchanged text keeps its cached verdict with no read — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) In _read1: a judge(model) step parses one reply; Haiku first, Sonnet on a non-pass, Sonnet's result used for everything after; grounding narrowed to gen-0 MUST/NEVER lines plus steer rows; a stray quote or ungrounded FAIL becomes a note; a verdicts file keyed by sha256 of the judged text short-circuits before any read; a readers file logs escalations and drops Haiku at 3+ FAILs with over a third overruled. Fails if: the cache returns a stale fail the user expects re-judged (rule 3 says never). 2) A separate reader module wrapping run_child with model fallback and cache for every Genesis reader. Fails if: drift and novelty change behaviour no one asked for, and the diff triples. 3) Keep Haiku-only and raise the pass bar (majority of 3 Haiku reads). Fails if: it ignores the user's explicit Sonnet rule. 4) Use what exists: fmideas.run_child already takes the model per call, _grounded already checks BREAKS against a given text, _reads/_key already store JSON state keyed by hash, and T-2207's carry logic stays as is; option 1 builds only on these. Fails if: run_child refuses sonnet under the budget (then the read is unread and blocks, as today). 5) Do less: only rule 3 (the cache) and keep the Haiku-only read. Fails if: Haiku's ungrounded fails still block new text, the non-convergence the user named. Choice 1 (85%): the smallest change that implements each rule where the read already happens, on what exists (4).
## Risks and rollback
What fails: a cached fail sticks until the text changes (by the user's rule); Sonnet reads cost more per escalation (the fm budget cap still gates each child); narrowing BREAKS to MUST/NEVER and steers lets a standing-intent-only objection through as a note. Undo: git revert the one commit; the verdicts and readers files are state and can be deleted.
## Execution prompt
## Steps
1. [x] red tests for the four rules (stub claude answers per model)
2. [x] judge(model), escalation and the readers log
3. [x] rule 2 grounding and notes; the content-hash verdict cache
## Resume here
## Docs impact
MASTER's fmgenesis line (T-2166 read) describes the four rules and both state files; CHANGELOG Unreleased entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisRead` → ✗ exit 1 · Ran 29 tests in 10.3s (2 classes, 16 at a time; slowest: GenesisRead 10s, GenesisReadRecord 1s) / FAILED (1 classes: test_genesis.GenesisRead) [ran] [tree 0f85e6de0802] (2026-11-01T14:57:08Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 181 tests in 10.9s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 7s, GenesisCheck 7s) / OK [ran] [tree c5a6a420e945] (2026-11-01T15:01:38Z)
- (step 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 181 tests in 10.9s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 7s, GenesisCheck 7s) / OK [ran] [tree c5a6a420e945] (2026-11-01T15:01:49Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 181 tests in 11.0s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree 3ea7c196b9e5] (2026-11-01T15:02:35Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 181 tests in 11.0s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree 3ea7c196b9e5] (2026-11-01T15:02:46Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 181 tests in 10.9s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 7s, GenesisCheck 7s) / OK [ran] [tree 3ea7c196b9e5] (2026-11-01T15:09:19Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 181 tests in 10.9s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 7s, GenesisCheck 7s) / OK [ran] [tree 3ea7c196b9e5] (2026-11-01T15:09:19Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisRead` → exit 0 · Ran 29 tests in 9.9s (2 classes, 16 at a time; slowest: GenesisRead 10s, GenesisReadRecord 1s) / OK [ran] [tree 3ea7c196b9e5] (2026-11-01T15:09:19Z)
- (audit intent) `main-thread lens pass over the fmgenesis diff and the 4 new tests; 2 real filings ran under it (critique-initiative.md: Sonnet decided 2 sections with 4 grounded fails, which were real errors, then filed on the revision; mission-finish.md re-filed)` → the user's four rules, each pinned by a test: Sonnet decides a non-pass and its verdict stands; a FAIL counts only with the file's line and a gen-0 MUST/NEVER or steer, else a note and the file files; verdicts cached by sha256 of the judged text, pass and fail; Haiku FAILs logged and Haiku dropped at 3+ with over a third overruled [tree 3ea7c196b9e5] (2026-11-01T15:09:19Z)
- (audit adversary) `main-thread lens pass over the fmgenesis diff and the 4 new tests; 2 real filings ran under it (critique-initiative.md: Sonnet decided 2 sections with 4 grounded fails, which were real errors, then filed on the revision; mission-finish.md re-filed)` → the reply stays untrusted (quotes matched against the file's own lines, BREAKS against the given MUST/NEVER and steer lines); an unread result (no reader ran, no verdict) still blocks and is never cached, so nothing is filed unjudged; the cache key is the redacted text the reader saw [tree 3ea7c196b9e5] (2026-11-01T15:09:19Z)
- (audit edge) `main-thread lens pass over the fmgenesis diff and the 4 new tests; 2 real filings ran under it (critique-initiative.md: Sonnet decided 2 sections with 4 grounded fails, which were real errors, then filed on the revision; mission-finish.md re-filed)` → identical sections share one verdict (rule 3); a cached fail sticks until the text changes; Sonnet unread after a Haiku fail is logged as unread, not an overrule; the 3-FAIL floor keeps one overrule from dropping Haiku [tree 3ea7c196b9e5] (2026-11-01T15:09:19Z)
- (audit operator) `main-thread lens pass over the fmgenesis diff and the 4 new tests; 2 real filings ran under it (critique-initiative.md: Sonnet decided 2 sections with 4 grounded fails, which were real errors, then filed on the revision; mission-finish.md re-filed)` → the failure message names the deciding model; notes say why they don't block; genesis-readers.json holds the disagreement log [tree 3ea7c196b9e5] (2026-11-01T15:09:19Z)
- (audit maintainer) `main-thread lens pass over the fmgenesis diff and the 4 new tests; 2 real filings ran under it (critique-initiative.md: Sonnet decided 2 sections with 4 grounded fails, which were real errors, then filed on the revision; mission-finish.md re-filed)` → judge(model) is one closure over the existing parse, carry and accept logic; the old stray-quote tests now assert the note [tree 3ea7c196b9e5] (2026-11-01T15:09:19Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 3ea7c196b9e5] (2026-11-01T15:10:13Z)
## Log
- 2026-11-01T14:55:07Z created
- 2026-11-01T14:55:28Z set approved=True
- 2026-11-01T14:56:06Z focused
- 2026-11-01T15:02:18Z scope: plugin/lib/fmgenesis.py (READ_CHILD, _read1, new helpers), plugin/tests/test_genesis.py, MASTER.md and CHANGELOG.md
- 2026-11-01T15:08:57Z step 4 removed: resume round 1's filings: Missions 5-8, the critiques, drift, selection, gen-2's seed
- 2026-11-01T15:08:57Z steer(self): step 4 (resume round 1's filings) moved out: fm genesis step drives the tower stages; the first two filings under the new read went through (critique-initiative.md on its 2nd put, mission-finish.md re-filed)
- 2026-11-01T15:09:44Z done
- 2026-11-01T15:09:47Z committed 099f595b (4 files)
- 2026-11-01T15:10:13Z guard authorization added: publish
- 2026-11-01T15:14:43Z publish grant used by fm ship
## Follow-ups captured
## Build vs reuse
Reuses fmideas.run_child (model per call), fmgenesis._grounded, _named, _reads/_key state files and T-2207's carry logic; nothing new beyond two small state files.
## Plan review
Self-critique: rule 1 escalates on any non-pass, not only FAIL, so an unparseable Haiku reply gets a real judge too; an unread result (no reader ran, or no CLEAN/FAIL from Sonnet) still blocks and is never cached: no file is filed unjudged. Rule 4's 3-FAIL floor is my default (a 1-of-1 ratio isn't a rate), recorded with fm decide. Approved under full autonomy.
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Two-tier LLM judge for the "cold read" check**: a cheap Haiku pass runs first. Any non-pass result escalates to Sonnet, which makes the final call. This is most likely a change to the audit/guard path (`plugin/lib/fmguard.py`, with `fmcore.py` for shared helpers). The agent definitions live in `p…
- **Evidence-gated FAIL**: a FAIL verdict is valid only if it quotes the offending line and names the MUST/NEVER rule or steer it violates. An unquoted or unattributed FAIL gets downgraded or rejected. This is a validation layer on the verdict parser and would touch the same code as the first reading.
- **Verdict cache plus Haiku circuit breaker**: verdicts are keyed by a content hash of the skill or doc under review. Haiku is disabled once more than a third of its non-pass verdicts are overruled by Sonnet. The state needs persisting, likely alongside the other `fm` state in `fmcore.py`.
- **Narrower reading**: "cold read" is an existing skill-description or skill-audit eval (`plugin/evals/`, `plugin/skills/`, `test_audit.py`), and the request only tunes its reliability. The tiering, cache and breaker would then be added to that one runner rather than built as a new component.
Approaches:
- **Single `judge()` wrapper in `fmguard.py`** (or a new `fmjudge.py` that `fmcli.py` calls). Order of operations:
- **Make the validator a pure function**: `validate_fail(verdict, source_text, rules)`. It checks that the quoted string occurs verbatim in the source and that the cited rule exists among the extracted MUST/NEVER lines or steers. A failing FAIL becomes "inconclusive" and goes to Sonnet, or is rejecte…
- **Keep the breaker's state in a small JSON counter**: store `{haiku_nonpass, overruled}` in the existing `fm` state directory, with a minimum sample size before the one-third threshold applies. `fm doctor` reports it, and a reset command or a decay window clears it.
- **Add the tier as a config knob** (model IDs, threshold, cache path) in the existing config rather than hard-coding it. `plugin/evals/` can then run the same judge against labeled cases to measure the overrule rate.
Failure modes:
- **Cache poisoning across rubric changes**: the key covers only the content hash, so edits to the MUST/NEVER rules or to the judge prompt return stale verdicts. The key must include the rubric text and the model tier. A Haiku-only verdict also must not satisfy a lookup that expects a Sonnet-confirme…
- **Breaker math drifts**: the denominator counts all Haiku calls rather than non-passes only, or the threshold trips on 2 of 3 samples. A tripped breaker that never resets silently doubles the Sonnet cost. A breaker that is never read by the caller does nothing, so the check in `fmhooks.py` hot path…
- **Quote validation is too strict or too loose**: the model normalizes whitespace, smart quotes or markdown, so real FAILs get rejected as unquoted. Substring matching on very short quotes accepts anything. A rule citation is checked only for being non-empty, not for existing in the source.
- **Hook latency and cost**: if the judge runs inside a hook, the two sequential LLM calls break the budget that `plugin/tests/bench_hooks.py --runs 20` enforces. Concurrent runs also race on the cache file without atomic writes.
## Dissent
- [x] rival reading: **Two-tier LLM judge for the "cold read" check**: a cheap Haiku pass runs first. Any non-pass result escalates to Sonnet, which makes the final call. This is most likely a change to the audit/guard path (`plugin/lib/fmguard.py`, with `fmcore.py` for shared helpers). The agent definitions live in `p… — answered: adopted: the two-tier judge, placed in fmgenesis._read1 where the tower read already runs (the guard is not a model path: models never decide there)
- [x] rival reading: **Evidence-gated FAIL**: a FAIL verdict is valid only if it quotes the offending line and names the MUST/NEVER rule or steer it violates. An unquoted or unattributed FAIL gets downgraded or rejected. This is a validation layer on the verdict parser and would touch the same code as the first reading. — answered: adopted: _named already checks the quote against the file's lines and _grounded the BREAKS clause; narrowed to gen-0 MUST/NEVER plus steers
- [x] rival reading: **Verdict cache plus Haiku circuit breaker**: verdicts are keyed by a content hash of the skill or doc under review. Haiku is disabled once more than a third of its non-pass verdicts are overruled by Sonnet. The state needs persisting, likely alongside the other `fm` state in `fmcore.py`. — answered: adopted: verdicts keyed by sha256 of the judged text; breaker counts FAILs (the user's word) with a 3-FAIL floor
- [x] rival reading: **Narrower reading**: "cold read" is an existing skill-description or skill-audit eval (`plugin/evals/`, `plugin/skills/`, `test_audit.py`), and the request only tunes its reliability. The tiering, cache and breaker would then be added to that one runner rather than built as a new component. — answered: rejected: the cold read is fmgenesis's tower-filing read (READ_CHILD), not a skill eval
- [x] rival approach: **Single `judge()` wrapper in `fmguard.py`** (or a new `fmjudge.py` that `fmcli.py` calls). Order of operations: — answered: rejected: a judge in fmguard puts a model inside the guard, which the gen-2 rule forbids (models advise, proof decides); fmgenesis owns the read
- [x] rival approach: **Make the validator a pure function**: `validate_fail(verdict, source_text, rules)`. It checks that the quoted string occurs verbatim in the source and that the cited rule exists among the extracted MUST/NEVER lines or steers. A failing FAIL becomes "inconclusive" and goes to Sonnet, or is rejecte… — answered: adopted: _grounded stays the pure check of the BREAKS clause, given only the MUST/NEVER and steer lines
- [x] rival approach: **Keep the breaker's state in a small JSON counter**: store `{haiku_nonpass, overruled}` in the existing `fm` state directory, with a minimum sample size before the one-third threshold applies. `fm doctor` reports it, and a reset command or a decay window clears it. — answered: adopted in part: a JSON counter with a 3-FAIL floor in the project's state dir; no doctor line or reset verb (YAGNI; deleting the file resets it)
- [x] rival approach: **Add the tier as a config knob** (model IDs, threshold, cache path) in the existing config rather than hard-coding it. `plugin/evals/` can then run the same judge against labeled cases to measure the overrule rate. — answered: rejected: model names and the threshold are fixed by the user's rule; a knob nobody asked for
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-01: [cites: user steer 2026-11-01: decision on the cold-read rule: keep it, make it reliable (Haiku first, Sonnet decides on FAIL; a FAIL quotes the lin…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
## Lessons
- A model reader converges only when its verdict is cached by content and a FAIL must cite both the file's line and the rule it breaks; otherwise every re-read re-rolls the dice
## Plan gaps
- failed first: step 1 red tests for the four rules (stub claude answers per model)
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
