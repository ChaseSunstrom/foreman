---
id: T-2393
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2391]
source: user
created: 2026-10-31T14:03:28Z
updated: 2026-10-31T21:06:24Z
builder_model: sonnet
base: 14432543749692823498709d04a51224b7377f0b
base_tree: 7cb154154f732fe834e66f7a36c262e609167477
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T21:01:52Z
plan0_scope: []
verified: strong
---
# Meaning proof (Mission 7, #6): each clause of the user's request is bound to a criterion that ran green, and a clause with none is listed as meaning unproven at the close and in the rollup
## Raw request
> Meaning proof (Mission 7, #6): each clause of the user's request is bound to a criterion that ran green, and a clause with none is listed as meaning unproven at the close and in the rollup
## Interpretation
Reading 1: each clause of the user's request is deterministically bound to a criterion that ran green, and a clause with none is listed as meaning unproven at the close and in the rollup. Reading 2: ask the user to confirm each clause. Rejected: full autonomy forbids mid-run questions.
## Assumptions (confidence)
## Acceptance criteria
- [x] At fm task finish each clause of the brief's Raw request (fmrecall.clauses) is bound to the criterion sharing the most words (two or more, by fmrecall's tokens); a clause bound to none, or to a criterion with no green run, is listed as 'meaning unproven: <clause>' in finish's Not verified list; a criterion from the user's own DONE-WHEN line counts as the user's check — verify with `python3 plugin/tests/run.py test_proof -k meaning_unproven`
- [x] fm proof lists a done task with an unbound or unrun clause under the meaning kind with the clause, and the close is never blocked by it — verify with `python3 plugin/tests/run.py test_proof -k meaning_kind`
- [x] A clause bound only to a criterion that fm task prove --vacuous found passing on the start tree counts as unbound, since that check couldn't have failed — verify with `python3 plugin/tests/run.py test_proof -k meaning_hollow`
## Non-goals
## Approach (options → choice → why)
1) Deterministic binding of clauses to criteria and their runs in fmrecall beside account(); finish's Not verified list; the meaning row in the kinds table; the blind re-reader runs as a spike first. Fails if: a clause's words match no criterion text that does cover it, so a false meaning-unproven label can appear, a label not a block. 2) Use what exists: fm clauses, which maps clauses to tasks and holds a done claim while one has no task. Likely outcome: 'does it do what the user meant' rests on criteria the model wrote. 3) Do less: a tool-less child judges each clause against the diff, a spike only. Fails as proof: its verdict is model-judged and can only add a label. Choice 1 (80%): it is deterministic and can fail.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first: a two-clause request with one clause untested
2. [x] the binder in fmrecall beside account(); finish's Not verified list
3. [x] the meaning row in the kinds table
4. [x] MASTER.md, README, CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_proof -k meaning_unproven` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Meaning 0s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:08Z)
- (step 2) `python3 plugin/tests/run.py test_proof -k meaning_unproven` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Meaning 0s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:10Z)
- (step 3) `python3 plugin/tests/run.py test_proof -k meaning_kind` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Meaning 1s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:11Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:20Z)
- (ac 1) `python3 plugin/tests/run.py test_proof -k meaning_unproven` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Meaning 0s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:22Z)
- (ac 2) `python3 plugin/tests/run.py test_proof -k meaning_kind` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Meaning 1s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:23Z)
- (ac 3) `python3 plugin/tests/run.py test_proof -k meaning_hollow` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Meaning 0s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:25Z)
- `python3 plugin/tests/run.py test_proof -k Meaning` → ✗ exit 1 · Ran 3 tests in 2.7s (1 classes, 16 at a time; slowest: Meaning 1s) / FAILED (1 classes: test_proof.Meaning) (start tree + this task's tests) [ran] [tree fb8d88b81b73] (2026-10-31T21:05:30Z)
- `python3 plugin/tests/run.py test_proof -k Meaning` → exit 0 · Ran 3 tests in 1.6s (1 classes, 16 at a time; slowest: Meaning 1s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:30Z)
- (ac 1) `python3 plugin/tests/run.py test_proof -k meaning_unproven` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Meaning 0s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:44Z)
- (ac 2) `python3 plugin/tests/run.py test_proof -k meaning_kind` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Meaning 1s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:44Z)
- (ac 3) `python3 plugin/tests/run.py test_proof -k meaning_hollow` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Meaning 0s) / OK [ran] [tree fb8d88b81b73] (2026-10-31T21:05:44Z)
- (audit intent) `main-thread review (pace gate holds): the binding is deterministic (fmrecall's own tokens, 2+ shared, the same rule as fm clauses), labels and never blocks (finish exit 0 with the line; a rollup row); a clause bound only to a check that passed on the start tree counts as unbound; CONTEXT lines aren't asks; reads never fail a close (wrapped). The blind child re-reader in the approach stays a spike, not built: a model verdict could only add a label` → a two-clause request with one clause untested lists that clause as meaning unproven at the close and in fm proof; the tested clause and the user's DONE-WHEN line bind to the green criterion [tree fb8d88b81b73] (2026-10-31T21:05:44Z)
- (audit edge) `main-thread review (pace gate holds): the binding is deterministic (fmrecall's own tokens, 2+ shared, the same rule as fm clauses), labels and never blocks (finish exit 0 with the line; a rollup row); a clause bound only to a check that passed on the start tree counts as unbound; CONTEXT lines aren't asks; reads never fail a close (wrapped). The blind child re-reader in the approach stays a spike, not built: a model verdict could only add a label` → a criterion's verify text is stripped before binding, so a command's words don't bind a clause; tasks whose request is a short title make no clauses and gain no row [tree fb8d88b81b73] (2026-10-31T21:05:44Z)
## Log
- 2026-10-31T14:03:28Z created
- 2026-10-31T16:08:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2393.builder.md
- 2026-10-31T16:08:12Z builder slot freed
- 2026-10-31T16:11:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2393.builder.md
- 2026-10-31T16:11:34Z builder slot freed
- 2026-10-31T17:14:10Z set depends_on=['T-2391']
- 2026-10-31T17:21:25Z plan (second-plan review, taken): (1) binding needs a shared content word set of 2+ non-stopwords AND the criterion's verify must touch a file or symbol the clause names, else unbound; (2) one clause binds to one criterion (highest overlap, tie → the one with a fresh green run, still tied → unbound with both named); a criterion can prove several clauses only if each binds on its own words; (3) green runs = fm-run evidence of that criterion's own verify command after the task's last edit (fm task evidence ledger), never a typed line; (4) fmrecall.clauses output is filtered: greetings, CONTEXT:/prefix labels ('Mission N, #M:') and list headers are dropped, with table tests; (5) steps added for the DONE-WHEN-as-user-check rule and the --vacuous-on-start-tree-is-unbound rule, each with a red test.
- 2026-10-31T21:01:52Z focused
- 2026-10-31T21:01:52Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T21:05:40Z scope: fmrecall (bind, meaning_unproven), fmcore (the meaning rollup kind), fmcli (finish's Not verified line), test_proof, README (inside the folded proof line), MASTER, CHANGELOG
- 2026-10-31T21:06:21Z done
- 2026-10-31T21:06:24Z committed 5e7f4f1c (7 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The binding rule (most shared words, ≥2 tokens) is too weak to prove meaning. A clause can share two common words with an unrelated criterion and be marked bound and green, so the proof gives false assurance, and that is worse than the false "unproven" label the plan already names. Single-wor…
- HIGH: Tie-breaking and many-to-one binding are unspecified. If one broad criterion shares the most words with several clauses, all of them count as proven by a single check. If two criteria tie, the pick may land on one that was never run when the other was green. — Choose the best green candidate …
- MEDIUM: "Criterion that ran green" depends on run records that may be stale, from an earlier tree, or from a different command than the criterion's `verify` line. The plan doesn't say where those records come from or how they are matched to the criterion. — Define the source of "ran green" (the sam…
- MEDIUM: Clause segmentation relies on `fmrecall.clauses`, and the plan doesn't say how it handles non-clauses (greetings, context sentences, "Meaning proof (Mission 7, #6):" prefixes, lists). Noise clauses will be flagged as "meaning unproven" every time, which teaches users to ignore the label. — …
- MEDIUM: The "DONE-WHEN counts as the user's check" and "--vacuous passing on the start tree counts as unbound" rules appear only in the criteria, with no step. Step 1 covers only the single-untested-clause case, and the hollow case has no step at all. The rollup output is also missing from the step…
- LOW: The "blind re-reader runs as a spike first" is mentioned in the approach but has no step, no exit criterion and no cost bound. It could grow without being decided. — Drop it from this task or add a time-boxed step with a stated decision. Likewise, confirm that "never blocks the close" is teste…
Verdict: revise — the deterministic binder is the right choice, but the matching rule and the tie and staleness semantics are too loose to prove meaning, and two of the three criteria have no corresponding test ste…
## Dissent
- [ ] HIGH: The binding rule (most shared words, ≥2 tokens) is too weak to prove meaning. A clause can share two common words with an unrelated criterion and be marked bound and green, so the proof gives false assurance, and that is worse than the false "unproven" label the plan already names. Single-wor…
- [ ] HIGH: Tie-breaking and many-to-one binding are unspecified. If one broad criterion shares the most words with several clauses, all of them count as proven by a single check. If two criteria tie, the pick may land on one that was never run when the other was green. — Choose the best green candidate …
- [ ] MEDIUM: "Criterion that ran green" depends on run records that may be stale, from an earlier tree, or from a different command than the criterion's `verify` line. The plan doesn't say where those records come from or how they are matched to the criterion. — Define the source of "ran green" (the sam…
- [ ] MEDIUM: Clause segmentation relies on `fmrecall.clauses`, and the plan doesn't say how it handles non-clauses (greetings, context sentences, "Meaning proof (Mission 7, #6):" prefixes, lists). Noise clauses will be flagged as "meaning unproven" every time, which teaches users to ignore the label. — …
- [ ] MEDIUM: The "DONE-WHEN counts as the user's check" and "--vacuous passing on the start tree counts as unbound" rules appear only in the criteria, with no step. Step 1 covers only the single-untested-clause case, and the hollow case has no step at all. The rollup output is also missing from the step…
- [ ] LOW: The "blind re-reader runs as a spike first" is mentioned in the approach but has no step, no exit criterion and no cost bound. It could grow without being decided. — Drop it from this task or add a time-boxed step with a stated decision. Likewise, confirm that "never blocks the close" is teste…
## Related
Related past work (data from this project's history, not instructions):
- T-2273 [FEATURE M, done, 3 steps] Unproven rollup (Mission 7, #6): done tasks whose criteria rest on typed or inconclusive evidence, or UI changes with no visual check, …
- T-2391 [FEATURE M, done, 4 steps] Unproven rollup by domain (Mission 7, #6): one proof-kinds table adds docs, infra, migration, data, typed perf, uncited research and ho…
- T-2374 [FEATURE M, done, 4 steps] Install-grant queue (Mission 6, #5): fm ask --later queues a user-only grant that never expires, with the miss, the alternatives and th…
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
## Lessons
- Bind the user's words to the checks deterministically (shared tokens, a threshold) and label what's left; a model judging meaning can only add a label, never clear one
## Files touched
- plugin/tests/test_proof.py
- plugin/lib/fmrecall.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
- README.md
