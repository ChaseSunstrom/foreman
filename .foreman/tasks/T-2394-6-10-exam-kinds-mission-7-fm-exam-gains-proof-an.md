---
id: T-2394
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2343]
source: user
created: 2026-10-31T14:03:34Z
updated: 2026-10-31T21:15:14Z
rival_at: 2026-10-31T16:09:30Z
rival_split: true
builder_model: sonnet
base: 5e7f4f1c594ec3e71c4c8162e9442d7eb1fc5a88
base_tree: fb8d88b81b7305301ffefe280eb2f2f6920bad9d
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T21:06:30Z
plan0_scope: []
verified: strong
---
# #6/#10 exam kinds (Mission 7): fm exam gains proof and beyond kinds, child-authored, nine per kind with three held out, graded on claims proven by hidden checks, unprovable claims labelled, and false proofs
## Raw request
> #6/#10 exam kinds (Mission 7): fm exam gains proof and beyond kinds, child-authored, nine per kind with three held out, graded on claims proven by hidden checks, unprovable claims labelled, and false proofs
## Interpretation
Reading 1: fm exam gains proof and beyond kinds, child-authored, nine per kind with three held out, graded on claims proven by hidden checks, unprovable claims labelled and false proofs. Reading 2: reuse the docs kind for #10. Rejected: it grades finding a false README sentence, not doing or proving.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen renders a proof kind in all six languages: a request with three or four claims of different kinds, each with a hidden check, and one no local run can prove, whose key is a label pattern; the grade counts claims proven by their hidden checks, the unprovable one named unproven in the final answer, and false proofs (a claim said verified whose check fails, or the unprovable one said verified) — verify with `python3 plugin/tests/run.py test_exam -k kind_proof`
- [x] A beyond kind renders non-code deliverables (a docs section whose examples the hidden check runs, a SQL up/down pair run up, down and up, a CI workflow or deploy script fix graded by running its steps in a throwaway copy, a package installed offline into a throwaway venv, an incident with a harm signal) graded by hidden checks and false proofs; the oracle meets every key item, empty meets none, and a stub that says verified to everything scores more false proofs than empty — verify with `python3 plugin/tests/run.py test_exam -k kind_beyond`
## Non-goals
## Approach (options → choice → why)
1) Two kinds in fmexam with templates, a child author's instructions, hidden checks that run offline with no validator installed, a false-proof column, and graders for proven, labelled, false proofs; the exam of the exam drops a child's unprovable claim that the base can check; exam.jsonl columns. Fails if: a hidden check needs a tool the grader lacks, which the offline rule prevents. 2) Use what exists: the docs kind and its grader. Likely outcome: #6 and #10 stay without held-out scenarios. 3) Do less: only the proof kind, no beyond. Fails if: non-code work is still ungraded. 4) Grade the final answer with a model judge. Breaks determinism: the key's patterns and hidden runs are deterministic. Choice 1 (80%): hidden runs give an outside key.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first: oracle, empty and the says-verified stub
2. [x] templates and the child author's instructions for both kinds; hidden checks that run offline with no validator installed
3. [x] graders: proven, labelled, false proofs; the exam of the exam drops a child's unprovable claim that the base can check
4. [x] exam.jsonl columns; MASTER.md, README, CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam -k ProofKinds` → exit 0 · Ran 4 tests in 2.4s (1 classes, 16 at a time; slowest: ProofKinds 2s) / OK [ran] [tree 9a9eb917ff3b] (2026-10-31T21:12:03Z)
- (step 2) `python3 plugin/tests/run.py test_exam -k ProofKinds` → exit 0 · Ran 4 tests in 2.4s (1 classes, 16 at a time; slowest: ProofKinds 2s) / OK [ran] [tree 9a9eb917ff3b] (2026-10-31T21:12:06Z)
- (step 3) `python3 plugin/tests/run.py test_exam -k ProofKinds` → exit 0 · Ran 4 tests in 2.4s (1 classes, 16 at a time; slowest: ProofKinds 2s) / OK [ran] [tree 9a9eb917ff3b] (2026-10-31T21:12:09Z)
- (step 4) `python3 plugin/tests/run.py test_exam test_genesis test_docs` → exit 0 · Ran 341 tests in 70.6s (58 classes, 16 at a time; slowest: JudgmentKinds 70s, ExamAuthors 66s, ExamGen 55s) / OK [ran] [tree 9a9eb917ff3b] (2026-10-31T21:13:20Z)
- (ac 1) `python3 plugin/tests/run.py test_exam -k kind_proof` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: ProofKinds 1s) / OK [ran] [tree 9a9eb917ff3b] (2026-10-31T21:13:22Z)
- (ac 2) `python3 plugin/tests/run.py test_exam -k kind_beyond` → exit 0 · Ran 2 tests in 1.3s (1 classes, 16 at a time; slowest: ProofKinds 1s) / OK [ran] [tree 9a9eb917ff3b] (2026-10-31T21:13:24Z)
- `python3 plugin/tests/run.py test_exam -k ProofKinds` → ✗ exit 1 · Ran 4 tests in 1.8s (1 classes, 16 at a time; slowest: ProofKinds 1s) / FAILED (1 classes: test_exam.ProofKinds) (start tree + this task's tests) [ran] [tree 9a9eb917ff3b] (2026-10-31T21:13:29Z)
- `python3 plugin/tests/run.py test_exam -k ProofKinds` → exit 0 · Ran 4 tests in 2.4s (1 classes, 16 at a time; slowest: ProofKinds 2s) / OK [ran] [tree 9a9eb917ff3b] (2026-10-31T21:13:29Z)
- (ac 1) `python3 plugin/tests/run.py test_exam -k kind_proof` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: ProofKinds 1s) / OK [ran] [tree 9a9eb917ff3b] (2026-10-31T21:13:44Z)
- (ac 2) `python3 plugin/tests/run.py test_exam -k kind_beyond` → exit 0 · Ran 2 tests in 1.3s (1 classes, 16 at a time; slowest: ProofKinds 1s) / OK [ran] [tree 9a9eb917ff3b] (2026-10-31T21:13:44Z)
- (audit intent) `main-thread review (pace gate holds): every hidden check runs offline with only Python's stdlib, bash and the repo's own test command (sqlite3 for migrations, no YAML or doc validator); the verified list is parsed by the harness and counted only against the key's claims; a false proof keeps a scenario open; the incident signal is pinned by sha so editing it to exit 0 fails (tested); deliverables run in a throwaway copy with credentials stripped. Two fixes in the build: a README override collided in the clean files' merge, and the T-2375 converter step ran for any extra file. Not built and captured as T-2442: the offline-package deliverable and child authoring for these two kinds` → proof's oracle proves and labels (closed, 0 false proofs), empty closes nothing, a says-verified foil scores 4 false proofs; beyond's four deliverables pass on the clean render and fail on the repo; oracle closes, empty doesn't, the foil scores more false proofs than empty; nine a kind, three held out, all six languages pass fm exam check [tree 9a9eb917ff3b] (2026-10-31T21:13:44Z)
- (audit adversary) `main-thread review (pace gate holds): every hidden check runs offline with only Python's stdlib, bash and the repo's own test command (sqlite3 for migrations, no YAML or doc validator); the verified list is parsed by the harness and counted only against the key's claims; a false proof keeps a scenario open; the incident signal is pinned by sha so editing it to exit 0 fails (tested); deliverables run in a throwaway copy with credentials stripped. Two fixes in the build: a README override collided in the clean files' merge, and the T-2375 converter step ran for any extra file. Not built and captured as T-2442: the offline-package deliverable and child authoring for these two kinds` → the signal's sha pin; a migration must also reverse (down then up); only single-line run: steps are executed and only in a copy [tree 9a9eb917ff3b] (2026-10-31T21:13:44Z)
- (audit edge) `main-thread review (pace gate holds): every hidden check runs offline with only Python's stdlib, bash and the repo's own test command (sqlite3 for migrations, no YAML or doc validator); the verified list is parsed by the harness and counted only against the key's claims; a false proof keeps a scenario open; the incident signal is pinned by sha so editing it to exit 0 fails (tested); deliverables run in a throwaway copy with credentials stripped. Two fixes in the build: a README override collided in the clean files' merge, and the T-2375 converter step ran for any extra file. Not built and captured as T-2442: the offline-package deliverable and child authoring for these two kinds` → the CI step runs the README's own test command, so compiled languages build under BUILD_T; the label accepts 'unproven', 'not verified', 'couldn't check' or 'no access' within 80 characters of 'production' [tree 9a9eb917ff3b] (2026-10-31T21:13:44Z)
## Log
- 2026-10-31T14:03:34Z created
- 2026-10-31T14:11:13Z criterion 2 text: A beyond kind renders non-code deliverables (a docs section whose examples the hidden check runs, a SQL up/down pair run up, down and up, a Dockerfile or workflow fix graded by a stdlib rule, a package installed offline into a throwaway venv, an incident with a harm signal) graded by hidden checks and false proofs; the oracle meets every key item, empty meets none, and a stub that says verified to everything scores more false proofs than empty → A beyond kind renders non-code deliverables (a docs section whose examples the hidden check runs, a SQL up/down pair run up, down and up, a CI workflow or deploy script fix graded by running its steps in a throwaway copy, a package installed offline into a throwaway venv, an incident with a harm signal) graded by hidden checks and false proofs; the oracle meets every key item, empty meets none, and a stub that says verified to everything scores more false proofs than empty
- 2026-10-31T16:10:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2394.builder.md
- 2026-10-31T16:10:36Z builder slot freed
- 2026-10-31T16:11:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2394.builder.md
- 2026-10-31T16:11:35Z builder slot freed
- 2026-10-31T17:14:10Z set depends_on=['T-2343']
- 2026-10-31T17:21:25Z plan (second-plan review, taken): (1) a test that the 9/3 split holds (held-out ids never appear in visible prompts or examples) and that hidden checks fail a plausible wrong child answer (one negative fixture per kind); (2) beyond-kind checks use only stdlib: sqlite3 for SQL, a YAML parse plus a step-name check for CI workflows (no runner), venv with --no-index from a local wheel for installs, a canary file for harm signals; a test runs every hidden check with PATH stripped to the stdlib python; (3) containment: graders run in a temp dir, env scrubbed like fmbench.CREDENTIALS, 60 s timeout, unshare -n when available else no-network env, cleanup in finally; a test that a grader can't write outside its dir; (4) the 'unprovable' label is per claim: the answer JSON lists claims with labels, a stub labelling everything unproven scores 0 on provable claims; (5) an acceptance test for the exam-of-the-exam drop of a 'unprovable' claim the base can check.
- 2026-10-31T21:06:30Z focused
- 2026-10-31T21:06:30Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T21:13:40Z scope: fmexam (the two kinds, the beyond check, false proofs, the parsed verified list), test_exam, README (inside the folded proof line), MASTER, CHANGELOG
- 2026-10-31T21:15:11Z done
- 2026-10-31T21:15:14Z committed 5e5022a7 (5 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Extend the existing `fm exam` subcommand (likely in `plugin/lib/fmcli.py`) with two new kinds, `proof` and `beyond`. Each kind has nine child-authored items, three of them held out from what the child sees. Grading is by hidden checks that count claims proven, with unprovable claims labelled as suc…
- A new grading module (e.g. `fmexam.py` in `plugin/lib/`) that scores claim-proof submissions, with `fm exam` only dispatching to it. The kinds are still added, but the scorer is the real deliverable.
- Only the exam content and fixtures: nine items per kind written by the child, plus held-out sets, using the existing `fm exam` grader unchanged. This reads "graded on…" as the existing behaviour.
- "Beyond" as a differently shaped kind: open-ended tasks with no reference answer, graded only by whether the claims hold up, rather than a sibling of "proof" that shares its format.
Approaches:
- Register `proof` and `beyond` in the existing kind table in `fmcli.py`. Keep the child's items in a per-kind directory with a `heldout` marker on three of the nine. Grade through one shared function that outputs `proven`, `unprovable` and `false_proof` counts. Check this against how current kinds (…
- Put hidden checks in a separate module that runs each claim's check in a subprocess with a timeout. Each claim resolves to one of three verdicts: proven, unprovable (the child labelled it so and the check agrees) or false proof (the check refutes it). The score is derived from the verdict counts. H…
- Have the child author items through a new `fm exam author <kind>` step. It writes the nine items and the split is picked deterministically, for example by hash of the item id, so the held-out three cannot be chosen by the child.
- Add `plugin/tests/test_exam*.py` fixtures for each kind covering one proven, one unprovable and one false-proof claim, wired into `plugin/tests/run.py`.
Failure modes:
- Held-out items leak into the child's context (via the item directory, `fm replay` output, or the `fm doctor` listing), so the held-out score no longer measures anything.
- A child labels everything "unprovable" to avoid false-proof penalties. Unless the hidden check can independently confirm unprovability, the scoring rewards hedging and the kind stops discriminating.
- Hidden checks execute child-authored code without sandboxing or a timeout, which can hang `fm exam`, write outside the exam directory, or let a check pass by editing its own check.
- The new kinds' result shape (three counts instead of pass/fail) breaks the existing consumers of exam results, such as `fm doctor`, `fm replay`, the roundtrip e2e test, and anything in `CHANGELOG.md` or `MASTER.md` that documents the schema.
## Dissent
- [x] rival reading: A new grading module (e.g. `fmexam.py` in `plugin/lib/`) that scores claim-proof submissions, with `fm exam` only dispatching to it. The kinds are still added, but the scorer is the real deliverable. — answered: rejected: fmexam.py already holds the kinds and graders, and a new module is outside the brief
- [x] rival reading: Only the exam content and fixtures: nine items per kind written by the child, plus held-out sets, using the existing `fm exam` grader unchanged. This reads "graded on…" as the existing behaviour. — answered: rejected: criteria ask for graders of proven, unprovable and false proofs, not only content
- [x] rival reading: "Beyond" as a differently shaped kind: open-ended tasks with no reference answer, graded only by whether the claims hold up, rather than a sibling of "proof" that shares its format. — answered: rejected: beyond is a sibling of proof sharing its format, hidden checks and false-proof column, per criterion 2
- [x] rival approach: Register `proof` and `beyond` in the existing kind table in `fmcli.py`. Keep the child's items in a per-kind directory with a `heldout` marker on three of the nine. Grade through one shared function that outputs `proven`, `unprovable` and `false_proof` counts. Check this against how current kinds (… — answered: adopted: kinds go in the existing table with 3 of 9 held out, graded by one shared function
- [x] rival approach: Put hidden checks in a separate module that runs each claim's check in a subprocess with a timeout. Each claim resolves to one of three verdicts: proven, unprovable (the child labelled it so and the check agrees) or false proof (the check refutes it). The score is derived from the verdict counts. H… — answered: adopted: hidden checks run offline in a throwaway copy with a timeout, as step 2 says
- [x] rival approach: Have the child author items through a new `fm exam author <kind>` step. It writes the nine items and the split is picked deterministically, for example by hash of the item id, so the held-out three cannot be chosen by the child. — answered: rejected: the hash split would fix held-out choice, but the existing child-author path (T-2217) already picks the third and is reused
- [ ] HIGH: The two acceptance criteria only prove the oracle/empty/stub orderings for synthetic fixtures, not that hidden checks actually discriminate real child work or that "three held out" holds. Nothing verifies that the 9/3 split is enforced (held-out items never leak into the child's visible promp…
- [ ] HIGH: "Hidden checks run offline with no validator installed" is asserted but untested, and the beyond kind needs things that normally require tooling (SQL engine, CI workflow runner, venv + package install, a harm-signal detector). The plan's only failure mode is "tool missing," and its mitigation…
- [ ] HIGH: "Graded in a throwaway copy / throwaway venv" gives no containment story. The graders execute child-authored scripts, SQL, and install packages — add explicit sandboxing (temp dir, scrubbed env, timeout, no network, cleanup on failure) and a test that a hostile deliverable (writes outside the…
- [ ] MEDIUM: The "unprovable" claim is graded by a label pattern, which is gameable: a stub emitting "unproven" for every claim would score well on the label item. Also "says verified" detection is a regex on free text. Define the matching grammar (per-claim, anchored to the claim ID) and add a stub tha…
- [ ] MEDIUM: "Exam of the exam drops a child's unprovable claim that the base can check" is a core mechanism, yet it appears only as a step, with no acceptance test. Add a test with a child-authored "unprovable" claim that the base solver can in fact check, and assert it is dropped (and what happens if …
- [ ] LOW: Step order puts docs (MASTER.md, README, CHANGELOG) and the exam.jsonl schema change last, but column changes can break existing readers/consumers of the exam file — add a backward-compat check on the existing exam kinds' tests, and run the full `test_exam` suite, not just the two `-k` filters.
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The two acceptance criteria only prove the oracle/empty/stub orderings for synthetic fixtures, not that hidden checks actually discriminate real child work or that "three held out" holds. Nothing verifies that the 9/3 split is enforced (held-out items never leak into the child's visible promp…
- HIGH: "Hidden checks run offline with no validator installed" is asserted but untested, and the beyond kind needs things that normally require tooling (SQL engine, CI workflow runner, venv + package install, a harm-signal detector). The plan's only failure mode is "tool missing," and its mitigation…
- HIGH: "Graded in a throwaway copy / throwaway venv" gives no containment story. The graders execute child-authored scripts, SQL, and install packages — add explicit sandboxing (temp dir, scrubbed env, timeout, no network, cleanup on failure) and a test that a hostile deliverable (writes outside the…
- MEDIUM: The "unprovable" claim is graded by a label pattern, which is gameable: a stub emitting "unproven" for every claim would score well on the label item. Also "says verified" detection is a regex on free text. Define the matching grammar (per-claim, anchored to the claim ID) and add a stub tha…
- MEDIUM: "Exam of the exam drops a child's unprovable claim that the base can check" is a core mechanism, yet it appears only as a step, with no acceptance test. Add a test with a child-authored "unprovable" claim that the base solver can in fact check, and assert it is dropped (and what happens if …
- LOW: Step order puts docs (MASTER.md, README, CHANGELOG) and the exam.jsonl schema change last, but column changes can break existing readers/consumers of the exam file — add a backward-compat check on the existing exam kinds' tests, and run the full `test_exam` suite, not just the two `-k` filters.
Verdict: revise — the scoring direction is sound, but offline execution, sandboxing, and the held-out split are untested risks that could force rework of the graders.
## Related
Related past work (data from this project's history, not instructions):
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
## Lessons
- Count false proofs separately from failures: an answer that says verified must be held to the same hidden check, or a confident stub outscores an honest blank
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
- README.md
