---
id: T-2188
type: FEATURE
tier: L
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-30T16:48:00Z
updated: 2026-10-31T03:00:54Z
base: bc7a0b6f23cd9c1c7740b5280033a86baf7bb78d
base_tree: 3603ca38f013dbbf83741cfab6c0d3159b3e37c7
plan0_at: 2026-10-31T02:44:34Z
plan0_scope: []
verified: strong
---
# The Genesis frame may grow, never shrink (steer 2026-10-30 #6, from gen 2 on): gen-0…
## Raw request
> FEATURE!: The Genesis frame may grow, never shrink (steer 2026-10-30 #6, from gen 2 on): gen-0 stays fixed as the constitution; any generation may add a capability beyond §2's 13 as spec.md '§2+N', coverage rows (areas), columns (surfaces) or stages, and lenses, reference sources and exam kinds. Each addition needs evidence (ideas, failures, misses or outcomes that fit no existing category), a cold fm second read confirming it isn't a renamed existing one and serves gen-0's goals, an exam kind or an explicit 'unmeasurable, why', and a lineage.md entry. New categories get cells, Missions and exam scenarios like the originals and later generations build on them; nothing added is ever removed. The §8 report lists every category Foreman added itself
## Interpretation
Steer 2026-10-30 #6, a standing rule from gen 2 on. gen-0 is the constitution and never changes (drift and the seal keep it); the working frame around it may only grow. A generation may add a capability past §2's 13 (spec.md '§2+N', with its exam kinds), coverage areas, surfaces or stages, and lenses, reference sources or exam kinds. Each addition carries evidence (ideas, failures, misses or outcomes that fit no existing category), a cold fm second read confirming it isn't a renamed existing category and serves gen-0's goals, an exam kind or an explicit 'unmeasurable, why', and a lineage.md entry. Once added, a category is treated like an original: coverage cells, Missions, exam scenarios, scorecard rows, and later generations build on it; none is ever removed. The §8 report lists every category Foreman added itself. This pairs with T-2187: a moonshot that keeps fitting no cell is the evidence a new category needs.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis grow adds a capability, area, surface, stage, lens, source or exam kind to frame.md only with evidence, a measure (exam kind or 'unmeasurable: why') and a cold read that passes it as new and serving gen-0; each addition writes a lineage.md line — verify with `python3 plugin/tests/run.py test_genesis`
- [x] an added capability gets its coverage row, scorecard row, seed Missions and exam kinds like §2's; fm genesis check fails a frame.md that lost or changed an entry — verify with `python3 plugin/tests/run.py test_genesis`
- [x] report.md lists every category Foreman added itself — verify with `python3 plugin/tests/run.py test_genesis`
- [x] fm genesis grow refuses below gen 2 and refuses a name colliding with gen-0 §2 or an existing entry; check fails when frame.md differs from the ledger's frame_grow events, and reports an added capability pending until its coverage row and exam kind exist, failing it at that generation's sweep — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Revised after fm second plan (verdict revise). (1) Cold read: frame.md is a tower file filed only through fm genesis put, so it gets the same cold read (acceptance, previous reads, stray quotes shown); the genesis_read event gains the filed text's hash, and check requires the last read of frame.md to have passed on exactly the filed text. Tests stub the reader, proving the plumbing; the judgment is the cold read's. (2) Never shrink, anchored: each grow logs a frame_grow event (entry id, kind, name, evidence refs, measure, entry hash) to the hash-chained ledger (fm verify-ledger); check fails when frame.md's entries differ from the ledger's frame_grow events, so hand edits fail even with a recomputed file. frame.md lives in state, written only by fm verbs (guard-protected like genesis-accepted.json). (3) Gen gate: grow refuses below gen 2 and refuses a name that collides with gen-0 §2 or an existing entry. (4) Ordering: an added capability is 'pending' until its coverage row and exam kind (or 'unmeasurable: why') exist; check reports pending in the generation it was added and fails if still pending at that generation's sweep. (5) Mistakes: append-only corrections (an entry with corrects: ID); the original stays and its name resolves to the correction. (6) Evidence must reference existing artifacts (task ids, research names, exam run ids) and check verifies they exist; report.md's 'Foreman added' list is the frame_grow events whose source is a session, apart from those citing a user steer's decision row. Rejected: a hash chain inside frame.md (self-anchored, forgeable), a model judging renames in check (nondeterministic), letting grow run in gen 0-1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: grow's refusals, frame.md's hash chain, a frame capability in coverage, scorecard and seed, the report list
2. [x] fm genesis grow and frame.md (OWNED), the cold read, the lineage line
3. [x] coverage, _caps, scorecard and seed read the frame; check fails a shrunk frame
4. [x] report section; the steer 6 rule gets its check; docs (MASTER, CHANGELOG, genesis skill, site Genesis page)
## Resume here
<!-- auto -->
- 2026-10-31T02:49:31Z step 2/4: fm genesis grow and frame.md (OWNED), the cold read, the lineage line
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/skills/genesis/SKILL.md, plugin/tests/test_genesis.py
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2188_test.txt, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2188.edit, plugin/lib/fmcli.py, plugin/tests/test_genesis.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2188b.edit, plugin/lib/fmgenesis.py, CHANGELOG.md, MASTER.md, plugin/skills/genesis/SKILL.md
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/genesis/SKILL.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisFrame` → ✗ exit 1 · Ran 4 tests in 0.661s / FAILED (failures=4) (start tree + this task's tests) [ran] [tree ea2205871ee6] (2026-10-31T02:47:44Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisFrame` → exit 0 · Ran 4 tests in 0.707s / OK [ran] [tree ea2205871ee6] (2026-10-31T02:47:44Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_exam test_cli test_docs` → exit 0 · Ran 383 tests in 63.3s (85 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 53s, TaskLifecycle 29s) / OK [ran] [tree ea2205871ee6] (2026-10-31T02:49:22Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_exam test_cli test_docs` → exit 0 · Ran 383 tests in 63.4s (85 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 53s, TaskLifecycle 28s) / OK [ran] [tree ea2205871ee6] (2026-10-31T02:50:26Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_exam test_cli test_docs` → exit 0 · Ran 383 tests in 63.2s (85 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 53s, TaskLifecycle 29s) / OK [ran] [tree ea2205871ee6] (2026-10-31T02:51:29Z)
- (step 4) `python3 plugin/tests/run.py test_genesis test_exam test_cli test_docs` → exit 0 · Ran 383 tests in 63.1s (85 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 53s, TaskLifecycle 28s) / OK [ran] [tree ea2205871ee6] (2026-10-31T02:52:32Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_exam test_cli test_docs` → exit 0 · Ran 384 tests in 63.2s (85 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 53s, TaskLifecycle 28s) / OK [ran] [tree 70ea57ea66b4] (2026-10-31T02:56:44Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_exam test_cli test_docs` → exit 0 · Ran 384 tests in 63.1s (85 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 53s, TaskLifecycle 28s) / OK [ran] [tree 70ea57ea66b4] (2026-10-31T02:57:47Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_exam test_cli test_docs` → exit 0 · Ran 384 tests in 63.3s (85 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 53s, TaskLifecycle 28s) / OK [ran] [tree 70ea57ea66b4] (2026-10-31T02:58:51Z)
- (step 4) `python3 plugin/tests/run.py test_genesis test_exam test_cli test_docs` → exit 0 · Ran 384 tests in 63.4s (85 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 53s, TaskLifecycle 28s) / OK [ran] [tree 70ea57ea66b4] (2026-10-31T02:59:54Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 130 tests in 7.0s (16 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 6s, GenesisDrift 5s) / OK [ran] [tree 70ea57ea66b4] (2026-10-31T03:00:17Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 130 tests in 7.0s (16 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 6s, GenesisDrift 5s) / OK [ran] [tree 70ea57ea66b4] (2026-10-31T03:00:17Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 130 tests in 7.0s (16 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 6s, GenesisDrift 5s) / OK [ran] [tree 70ea57ea66b4] (2026-10-31T03:00:17Z)
- (ac 4) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 130 tests in 7.0s (16 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 6s, GenesisDrift 5s) / OK [ran] [tree 70ea57ea66b4] (2026-10-31T03:00:17Z)
- (audit intent) `fm-reviewer five lenses: changes needed, all fixed: the entry is redacted before hashing (a token in evidence no longer false-fails as changed), names compare casefolded without numbering or punctuation ('1. Initiative', 'Initiative.' refused), the report needs a line naming F-N and the name as words, the cold read sees only the new entry plus the existing category names (an old entry can't block a grow), id, file, event and lineage line go under the genesis-lineage lock, a hand-added entry never feeds all_caps, added numbers follow §2's highest, an unmeasurable capability maps to no kind and scores 'unmeasurable' (ok), the duplicate genesis_grow event is gone; fm log can't forge frame_grow (T-2244) and put refuses frame.md; test_genesis test_exam test_cli test_docs 384 green; red-to-green proven` → from gen 2 the frame grows by fm genesis grow only, each addition with evidence, a measure and a cold read; added capabilities join spec, scorecard, seed and export; check fails a shrink, a rewrite or a hand edit, and a filed report missing an addition [tree 70ea57ea66b4] (2026-10-31T03:00:17Z)
- (audit adversary) `fm-reviewer five lenses: changes needed, all fixed: the entry is redacted before hashing (a token in evidence no longer false-fails as changed), names compare casefolded without numbering or punctuation ('1. Initiative', 'Initiative.' refused), the report needs a line naming F-N and the name as words, the cold read sees only the new entry plus the existing category names (an old entry can't block a grow), id, file, event and lineage line go under the genesis-lineage lock, a hand-added entry never feeds all_caps, added numbers follow §2's highest, an unmeasurable capability maps to no kind and scores 'unmeasurable' (ok), the duplicate genesis_grow event is gone; fm log can't forge frame_grow (T-2244) and put refuses frame.md; test_genesis test_exam test_cli test_docs 384 green; red-to-green proven` → frame_grow events can't be forged through fm log; frame.md is OWNED and lives in state; a hand-added entry fails check and feeds nothing [tree 70ea57ea66b4] (2026-10-31T03:00:17Z)
- (audit edge) `fm-reviewer five lenses: changes needed, all fixed: the entry is redacted before hashing (a token in evidence no longer false-fails as changed), names compare casefolded without numbering or punctuation ('1. Initiative', 'Initiative.' refused), the report needs a line naming F-N and the name as words, the cold read sees only the new entry plus the existing category names (an old entry can't block a grow), id, file, event and lineage line go under the genesis-lineage lock, a hand-added entry never feeds all_caps, added numbers follow §2's highest, an unmeasurable capability maps to no kind and scores 'unmeasurable' (ok), the duplicate genesis_grow event is gone; fm log can't forge frame_grow (T-2244) and put refuses frame.md; test_genesis test_exam test_cli test_docs 384 green; red-to-green proven` → name variants, a redacted secret in evidence, two grows at once (lock), a Frame section mid-lineage, 'unmeasurable: .' refused, word-bounded report matching [tree 70ea57ea66b4] (2026-10-31T03:00:17Z)
- (audit operator) `fm-reviewer five lenses: changes needed, all fixed: the entry is redacted before hashing (a token in evidence no longer false-fails as changed), names compare casefolded without numbering or punctuation ('1. Initiative', 'Initiative.' refused), the report needs a line naming F-N and the name as words, the cold read sees only the new entry plus the existing category names (an old entry can't block a grow), id, file, event and lineage line go under the genesis-lineage lock, a hand-added entry never feeds all_caps, added numbers follow §2's highest, an unmeasurable capability maps to no kind and scores 'unmeasurable' (ok), the duplicate genesis_grow event is gone; fm log can't forge frame_grow (T-2244) and put refuses frame.md; test_genesis test_exam test_cli test_docs 384 green; red-to-green proven` → one cold read of one entry per grow; all_caps reads the ledger only when frame.md has entries [tree 70ea57ea66b4] (2026-10-31T03:00:17Z)
- (audit maintainer) `fm-reviewer five lenses: changes needed, all fixed: the entry is redacted before hashing (a token in evidence no longer false-fails as changed), names compare casefolded without numbering or punctuation ('1. Initiative', 'Initiative.' refused), the report needs a line naming F-N and the name as words, the cold read sees only the new entry plus the existing category names (an old entry can't block a grow), id, file, event and lineage line go under the genesis-lineage lock, a hand-added entry never feeds all_caps, added numbers follow §2's highest, an unmeasurable capability maps to no kind and scores 'unmeasurable' (ok), the duplicate genesis_grow event is gone; fm log can't forge frame_grow (T-2244) and put refuses frame.md; test_genesis test_exam test_cli test_docs 384 green; red-to-green proven` → one _norm_name and one _grown used by grow, all_caps and check; non-capability kinds are recorded and checked, wiring them is follow-up work the skill states [tree 70ea57ea66b4] (2026-10-31T03:00:17Z)
## Log
- 2026-10-30T16:48:00Z created
- 2026-10-30T16:48:05Z set tier=L
- 2026-10-30T16:50:27Z planned: it has criteria and steps
- 2026-10-30T19:00:39Z set approved=True
- 2026-10-30T19:00:39Z approved on the user's yes 2026-10-30: 'I approve all changes btw, you don't need to ask for my approval'
- 2026-10-31T00:11:36Z fm second plan: revise; plan revised (cold read via fm genesis put with the text hash on the event, ledger frame_grow events as the never-shrink anchor, gen-2 gate and §2 collision refusal, pending state instead of grow-then-fail, append-only corrections, evidence refs checked)
- 2026-10-31T02:44:33Z focused
- 2026-10-31T03:00:10Z scope: plugin/lib/fmgenesis.py, plugin/lib/fmcli.py (genesis grow flags), plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md, plugin/skills/genesis/SKILL.md
- 2026-10-31T03:00:52Z done
- 2026-10-31T03:00:54Z committed b3697fd5 (6 files)
## Follow-ups captured
## Build vs reuse
Reuses: the OWNED tower-file mechanism (only its verb writes it), put()'s cold second read, gen-0's seal/hash pattern (seal, sealed) for frame.md's never-shrink chain, _caps/coverage()/scorecard()/seed() as the readers that gain frame capabilities, lineage.md's sections for the lineage line, and fm genesis check's problem list. New: fm genesis grow KIND NAME --evidence, frame.md's format and hash chain, the report's 'added by Foreman' list.
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The "cold fm second read" is the only gate against renamed categories, but the plan doesn't say how it runs or how a test can verify it. A cold read is an LLM judgment, so `test_genesis` either stubs it (proving only the plumbing) or is nondeterministic. Nothing shows the read is truly cold (…
- HIGH: "Never shrink" is enforced by a hash chain, but the plan doesn't say what anchors it. If frame.md is OWNED but only `fm genesis check` verifies it, anyone who edits the file can recompute the whole chain and pass. Also unspecified: does the chain cover the full entry (evidence, measure, verdi…
- HIGH: "From gen 2 on" is not in the acceptance criteria or the steps. Nothing says what `grow` does in gen 0 or gen 1, and nothing prevents a grow from touching gen-0's §2 or its constitution. — Make `grow` refuse when the current generation is below 2 and refuse any entry that collides with or mod…
- MEDIUM: The consistency rule is circular. `check` fails when a frame capability has no coverage row or exam kind, but `grow` appends the entry first and the row, scorecard row and seed Missions come later. Every grow therefore leaves the repo in a failing state, and the 'unmeasurable, why' escape h…
- MEDIUM: Removing entries is forbidden, but nothing covers a bad or mistaken entry (a typo in a name, a wrong evidence line). With no remedy, each error is permanent, and people will bypass the tooling by editing the file by hand. — Allow append-only amendments (a `supersedes` or `corrects` entry th…
- LOW: "Evidence" is checked only as present, so one meaningless line passes. The report's "every category Foreman added itself" also needs a defined source, since frame.md could contain human-added entries. — Require evidence lines to reference existing artifacts (idea, failure or miss IDs) and vali…
Verdict: revise — the design direction is sound, but the cold-read gate, the hash chain's trust anchor and the generation gate are underspecified, and the check/grow ordering would leave the repo failing after ever…
## Dissent
- [ ] HIGH: The "cold fm second read" is the only gate against renamed categories, but the plan doesn't say how it runs or how a test can verify it. A cold read is an LLM judgment, so `test_genesis` either stubs it (proving only the plumbing) or is nondeterministic. Nothing shows the read is truly cold (…
- [ ] HIGH: "Never shrink" is enforced by a hash chain, but the plan doesn't say what anchors it. If frame.md is OWNED but only `fm genesis check` verifies it, anyone who edits the file can recompute the whole chain and pass. Also unspecified: does the chain cover the full entry (evidence, measure, verdi…
- [ ] HIGH: "From gen 2 on" is not in the acceptance criteria or the steps. Nothing says what `grow` does in gen 0 or gen 1, and nothing prevents a grow from touching gen-0's §2 or its constitution. — Make `grow` refuse when the current generation is below 2 and refuse any entry that collides with or mod…
- [ ] MEDIUM: The consistency rule is circular. `check` fails when a frame capability has no coverage row or exam kind, but `grow` appends the entry first and the row, scorecard row and seed Missions come later. Every grow therefore leaves the repo in a failing state, and the 'unmeasurable, why' escape h…
- [ ] MEDIUM: Removing entries is forbidden, but nothing covers a bad or mistaken entry (a typo in a name, a wrong evidence line). With no remedy, each error is permanent, and people will bypass the tooling by editing the file by hand. — Allow append-only amendments (a `supersedes` or `corrects` entry th…
- [ ] LOW: "Evidence" is checked only as present, so one meaningless line passes. The report's "every category Foreman added itself" also needs a defined source, since frame.md could contain human-added entries. — Require evidence lines to reference existing artifacts (idea, failure or miss IDs) and vali…
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (sixth): the frame may grow, never shrink] [check: pending T-2188] Standing rule from gen 2 on: the Genesis fram…
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
## Lessons
- When an anchor hashes content, hash exactly what gets written (after redaction), or the writer's own transform breaks the anchor
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/genesis/SKILL.md
