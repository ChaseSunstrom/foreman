---
id: T-2202
type: SECURITY
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T19:29:49Z
updated: 2026-10-30T19:41:14Z
base: 164d5040d251eb3448e252212c8b8422a43a0151
base_tree: bbf3d1a8340b50c79f6dd957e375f740ead269c0
plan0_at: 2026-10-30T19:30:00Z
plan0_scope: []
verified: strong
---
# fm prove's consent can't be forged: a tree's tests run only on the user's own --yes-run (remembered per tree in Foreman state) or in Foreman's home; elsewhere untested candidates stay leads and cold kinds still prove
## Raw request
> fm prove's consent can't be forged: a tree's tests run only on the user's own --yes-run (remembered per tree in Foreman state) or in Foreman's home; elsewhere untested candidates stay leads and cold kinds still prove
## Interpretation
A background security review found fm prove's automatic consent forgeable: anyone can author a commit with the user's email, so a cloned repo passes 'HEAD is your own commit' and its tests run unasked once the rules point a session at fm prove. The consent must come from something only the user can produce. Running repo code is the only risky part: fm find and the cold re-find (docs, dep, secret) never execute the tree.
## Assumptions (confidence)
## Acceptance criteria
- [x] a tree whose HEAD author is the user's email but never got --yes-run proves no untested candidate and runs none of its code — verify with `python3 plugin/tests/run.py test_find`
- [x] after one --yes-run the same tree proves untested candidates without the flag — verify with `python3 plugin/tests/run.py test_find`
## Non-goals
## Approach (options → choice → why)
Complete version: (1) consent only from the user's own --yes-run (already user-only in the guard), remembered per tree (realpath) in state_dir()/prove-trusted.json, which only fm writes (state-direct is never authorizable); (2) Foreman's own home counts as trusted (fm check already runs its tests on every close); (3) without consent fm prove still runs: cold kinds prove, untested candidates become leads saying the user's yes is needed, no exit 2; (4) docs, guard text and help say so. Approaches weighed: A reflog check (HEAD made by a local commit) — forgeable through a shipped .git and passes a user commit atop a cloned tree; B verified signatures (git verify-commit with an allowed-signers file outside the repo) — needs signing set up, most users have none; C always require --yes-run, nothing remembered — safe but sessions could never prove in the user's own repos, defeating Mission 3; D user-granted per-tree trust remembered in Foreman state (chosen: same model as Claude Code's folder trust). Build vs reuse: reuse USER_ONLY_FM, c.state_dir, the state-direct guard; no new verb.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: replace the HEAD-is-yours test with forge + trust tests
2. [x] fmprove: trusted()/remember() in state_dir, prove(run=…), cmd_prove never exits 2 for consent
3. [x] guard message, fmcli help, MASTER, CHANGELOG, README wording
4. [x] review fixes: no Foreman-home auto-trust (FOREMAN_HOME made any tree trusted), a failed remember is reported, unrun untested candidates don't take --limit slots, docs say a yes is per path and governs Foreman's initiative
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_find` → ✗ exit 1 · Ran 38 tests in 7.1s (15 classes, 16 at a time; slowest: FindCli 7s, FindRenders 6s, FindProve 4s) / FAILED (1 classes) [ran] [tree 8f5e9ad997af] (2026-10-30T19:30:55Z)
- (step 2) `python3 plugin/tests/run.py test_find test_guard test_guard_exec_vectors` → exit 0 · Ran 339 tests in 9.4s (103 classes, 16 at a time; slowest: Mutation 9s, FindCli 6s, GuardAgainstBash 6s) / OK [ran] [tree 89b0effc7470] (2026-10-30T19:32:21Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_find` → exit 0 · Ran 118 tests in 8.4s (36 classes, 16 at a time; slowest: Fences 8s, FindCli 6s, FindProve 2s) / OK [ran] [tree 6dcba06a19f8] (2026-10-30T19:33:01Z)
- (step 4) `python3 plugin/tests/run.py test_find` → ✗ exit 1 · Ran 38 tests in 6.0s (15 classes, 16 at a time; slowest: FindCli 6s, FindProve 2s, FindRenders 2s) / FAILED (1 classes) [ran] [tree 895c6eedd74a] (2026-10-30T19:35:43Z)
- (step 4) `python3 plugin/tests/run.py test_find test_guard test_guard_exec_vectors test_docs` → exit 0 · Ran 419 tests in 9.7s (124 classes, 16 at a time; slowest: Mutation 9s, Fences 8s, GuardAgainstBash 6s) / OK [ran] [tree 7026a61f53de] (2026-10-30T19:36:20Z)
- (ac 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 38 tests in 6.0s (15 classes, 16 at a time; slowest: FindCli 6s, FindProve 3s, FindRenders 2s) / OK [ran] [tree 7026a61f53de] (2026-10-30T19:37:06Z)
- (ac 2) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 38 tests in 6.0s (15 classes, 16 at a time; slowest: FindCli 6s, FindProve 3s, FindRenders 2s) / OK [ran] [tree 7026a61f53de] (2026-10-30T19:37:06Z)
- (step 1) `python3 plugin/tests/run.py test_find test_guard test_guard_exec_vectors test_docs` → exit 0 · Ran 419 tests in 9.7s (124 classes, 16 at a time; slowest: Mutation 9s, Fences 8s, FindCli 6s) / OK [ran] [tree 7026a61f53de] (2026-10-30T19:37:06Z)
- (audit intent) `one foreman:fm-reviewer five-lens pass (research T-2202-review): HIGH FOREMAN_HOME trust fixed, FOREMAN_STATE route decided (fm decide), MEDIUM limit slots and LOW remember fixed, all tested` → both criteria met by test_your_email_on_head_is_no_consent...; unrun candidates no longer crowd provable ones out of --limit [tree 7026a61f53de] (2026-10-30T19:37:06Z)
- (audit adversary) `one foreman:fm-reviewer five-lens pass (research T-2202-review): HIGH FOREMAN_HOME trust fixed, FOREMAN_STATE route decided (fm decide), MEDIUM limit slots and LOW remember fixed, all tested` → author email, FOREMAN_HOME and a session-passed --yes-run can't say yes; a self-written FOREMAN_STATE list is a deliberate run the docs name, decided not guarded [tree 7026a61f53de] (2026-10-30T19:37:06Z)
- (audit edge) `one foreman:fm-reviewer five-lens pass (research T-2202-review): HIGH FOREMAN_HOME trust fixed, FOREMAN_STATE route decided (fm decide), MEDIUM limit slots and LOW remember fixed, all tested` → corrupt trust list trusts nothing; prefix-sharing sibling stays untrusted; unwritable state reported, run continues [tree 7026a61f53de] (2026-10-30T19:37:06Z)
- (audit operator) `one foreman:fm-reviewer five-lens pass (research T-2202-review): HIGH FOREMAN_HOME trust fixed, FOREMAN_STATE route decided (fm decide), MEDIUM limit slots and LOW remember fixed, all tested` → no hooks, loops or cost; one small JSON state file written only on the user's yes [tree 7026a61f53de] (2026-10-30T19:37:06Z)
- (audit maintainer) `one foreman:fm-reviewer five-lens pass (research T-2202-review): HIGH FOREMAN_HOME trust fixed, FOREMAN_STATE route decided (fm decide), MEDIUM limit slots and LOW remember fixed, all tested` → own_tree removed with no callers left; the trust code is 3 small functions with tests [tree 7026a61f53de] (2026-10-30T19:37:06Z)
## Log
- 2026-10-30T19:29:49Z created
- 2026-10-30T19:29:58Z set approved=True
- 2026-10-30T19:29:58Z approved under the user's standing yes: "I approve all changes btw, you don't need to ask for my approval"
- 2026-10-30T19:29:59Z focused
- 2026-10-30T19:36:49Z replan after review: no Foreman-home exception (FOREMAN_HOME is a session's to set); Approach item (2) withdrawn
- 2026-10-30T19:37:42Z done
- 2026-10-30T19:37:44Z committed 9134ca17 (7 files)
- 2026-10-30T19:38:00Z guard authorization added: publish
- 2026-10-30T19:38:39Z guard authorization added: publish
- 2026-10-30T19:41:14Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- research T-2122-review: Verdict: changes needed (1 HIGH, 9 MEDIUM, 3 LOW); reviewer ran nothing (read-only).
- T-2122 [FEATURE L, done, 2 steps] fm find prove: proof tickets, red 3/3 for an assertion and mutate-to-confirm; unproven candidates become leads (Mission 3 brief 3) — le…
- decision 2026-10-30: Proven kinds (dep, docs, secret) file without a cold re-run; scout never refiles a regression
- similar finished tasks took 2–2 steps
## Why not caught
T-2122's review treated a global git email as unforgeable without asking who can write a commit's author field; the background security review asked
## Lessons
- A consent check must read only what the user alone can produce: anything inside the tree (an author email) or in the session's environment (FOREMAN_HOME) is a claim
## Plan gaps
- added late: review fixes: no Foreman-home auto-trust (FOREMAN_HOME made any tree trusted), a failed remember is reported, unrun unt…
- failed first: step 1 red: replace the HEAD-is-yours test with forge + trust tests
- failed first: step 4 review fixes: no Foreman-home auto-trust (FOREMAN_HOME made any tree trusted), a failed remember is…
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmcli.py
- plugin/lib/fmguard.py
- plugin/lib/fmprove.py
- plugin/tests/test_guard.py
- CHANGELOG.md
- MASTER.md
