---
id: T-0943
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-15T20:27:39Z
updated: 2026-10-15T21:14:46Z
base: e51d081f40d53117aaa4df7e2da07d2098c25f55
base_tree: b54c0e4328e74b6984c9b3c6d39ac6b131104739
verified: strong
---
# lint_verify warns when a criterion's verify command touches a live service (aws, gcloud, az, kubectl, psql/mysql against a host, terraform apply)
## Raw request
> - `SKILL.md:17` and the live-cloud Verify commands (`cards/cloud/aws-iam.md:12-15`, `cards/data/postgres-locking.md:12`, `cards/infra/kubernetes.md:14-16`): turning these into `--ac` criteria would h…
> (noticed by an agent; research T-0933-review)
## Interpretation
From the T-0933 review: stack cards' Verify commands include live-service calls (aws iam simulate-principal-policy, kubectl get, psql -h prod). If an agent turns one into a criterion, fm check and fm lane merge would run it unattended against the user's ambient credentials. The library SKILL.md now says to keep those as manual checks. This makes Foreman warn when it happens, instead of trusting the agent to remember.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task ac add/edit with a verify command that calls a live cloud or cluster CLI prints a warning naming it (a manual check, not an unattended criterion) and still records the criterion; local commands get no warning — verify with `python3 plugin/tests/run.py -k LiveVerify`
## Non-goals
## Approach (options → choice → why)
Options: a warning in lint_verify, the one place criteria are checked when they are added (chosen); refuse such criteria (too strict: some projects test against a sandbox account on purpose); have the guard intercept fm check runs (late, and it fires on every run).
## Risks and rollback
## Execution prompt
## Steps
1. [x] LiveVerify test, then a pattern in fmcore.lint_verify returning a warning, not a refusal
## Resume here
## Docs impact
none: the warning text explains itself; the library SKILL.md already says live-service Verify commands stay manual
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k LiveVerify` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: LiveVerify 0s) / FAILED (1 classes) [ran] [tree 4d6463e72e8e] (2026-10-15T21:14:15Z)
- (step 1) `python3 plugin/tests/run.py -k LiveVerify` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: LiveVerify 0s) / OK [ran] [tree cbb20bb41788] (2026-10-15T21:14:44Z)
- (ac 1) `python3 plugin/tests/run.py -k LiveVerify` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: LiveVerify 0s) / OK [ran] [tree cbb20bb41788] (2026-10-15T21:14:45Z)
- (ac 1) `python3 plugin/tests/run.py -k LiveVerify` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: LiveVerify 0s) / OK [ran] [tree cbb20bb41788] (2026-10-15T21:14:45Z)
- (audit intent) `main-thread: the pattern is tested on 9 live and 7 local commands; a warning only, the criterion is still recorded` → ok: an agent turning a card's live Verify command into a criterion is told at once [tree cbb20bb41788] (2026-10-15T21:14:45Z)
- (audit edge) `main-thread: the pattern is tested on 9 live and 7 local commands; a warning only, the criterion is still recorded` → ok: terraform plan/validate, helm lint, kubectl kustomize, psql without a host and --version stay quiet [tree cbb20bb41788] (2026-10-15T21:14:45Z)
- (audit self) `main-thread: the pattern is tested on 9 live and 7 local commands; a warning only, the criterion is still recorded` → no findings [tree cbb20bb41788] (2026-10-15T21:14:45Z)
## Log
- 2026-10-15T20:27:39Z created
- 2026-10-15T21:11:03Z planned from capture
- 2026-10-15T21:14:01Z focused
- 2026-10-15T21:14:46Z done
- 2026-10-15T21:14:46Z committed 6e4ab3f (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0933-review: Changes needed. The code works and the 22 cards I sampled are accurate. Detect signals produce false-positive suggestions, and one manifest regex…
- playbook Cloud & Infrastructure Security Skill (skills/playbooks/references/security/cloud-infrastructure.md)
- T-0933 [FEATURE L, done, 5 steps] Stack library: 400+ on-demand implementation cards (fm lib) plus federated search over installed plugins' skills — lesson: Subagent-wri…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
## Lessons
- Enforce at the point of entry: lint_verify sees every criterion as it is written, so one warning there beats a rule every agent must remember.
## Plan gaps
- failed first: step 1 LiveVerify test, then a pattern in fmcore.lint_verify returning a warning, not a refusal
## Files touched
- plugin/tests/test_diff_gates.py
- plugin/lib/fmcore.py
