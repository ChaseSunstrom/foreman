---
id: T-2385
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T14:02:37Z
updated: 2026-10-31T15:47:27Z
builder_model: sonnet
base: 9ae0b87d78df105c7e27f1c511ab89eb117185e7
base_tree: 930be79ba41e1e5de7a444cf7163cedb2aa365b6
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T14:35:43Z
plan0_scope: []
verified: strong
---
# Infra proof (Mission 7, #6/#10): fm prove --infra runs the ecosystem's own validators on a task's infra files in a throwaway copy, offline, and labels a file unproven when its validator isn't installed
## Raw request
> Infra proof (Mission 7, #6/#10): fm prove --infra runs the ecosystem's own validators on a task's infra files in a throwaway copy, offline, and labels a file unproven when its validator isn't installed
## Interpretation
Gap map #10 infra proof (3): infra changes close on a claim. The guard asks before live applies and about 60 cards describe the tools, but nothing runs a validator on a changed Dockerfile, workflow or Terraform file. On this machine only docker and systemd-analyze are installed, so most files would be labelled unproven here until a grant installs the rest.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm prove --infra [PATH] classifies Dockerfiles, compose files, Terraform, Helm charts, Kubernetes manifests, CI workflows, shell scripts and systemd units and runs each class's validator when it is on PATH (hadolint, docker compose config, terraform validate only where .terraform is already initialised, helm lint, kubeconform, actionlint, shellcheck, systemd-analyze verify) on a throwaway copy; a failing validator fails the file, a missing one makes it unproven naming the tool; nothing is installed, downloaded or run against an account; exit 0 none failed, 1 a failure, 2 nothing checked — verify with `python3 plugin/tests/run.py test_prove -k infra_proof`
- [x] fm task finish runs fm prove --infra on the infra files the task touched and records the result as run evidence; a missing validator is reported once to the capability-miss path (Mission 6), never installed — verify with `python3 plugin/tests/run.py test_prove -k infra_finish`
## Non-goals
## Approach (options → choice → why)
1) fm prove --infra: the ecosystem's validators found from the stack cards' globs, offline, on a throwaway copy; missing tools labelled unproven and handed to the capability-miss path. 2) terraform plan or kubectl --dry-run=server against the real account: rejected unprompted, it leaves the machine and needs the user's grant, so it is named in the final report. 3) Foreman's own lint rules per file type: rejected, hand-written rules against standing intent 5. Choice 1: ecosystem tools, local and reversible.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first with stub validators on PATH: one passing, one failing, one absent
2. [x] classes from the stack cards' detect globs (fmlib), one validator command per class in a table
3. [x] throwaway copy, scrubbed environment, timeout; the guard's live-command list stays the boundary
4. [x] finish reach and the capability-miss note; MASTER.md, README, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T14:58:31Z steps 4/4 done
- git: worktree-agent-a95c4be9345c9d047; 1 uncommitted: plugin/lib/fminfra.py
- touched since last checkpoint: MASTER.md, README.md, plugin/lib/fminfra.py
## Docs impact
README.md, MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_prove -k infra_finish 2>&1 | tail -40` → ✗ exit 1 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: InfraFinish 1s) / FAILED (1 classes: test_prove.InfraFinish) [ran] [tree 0b9b96b9c4a9] (2026-10-31T14:46:20Z)
- (ac 2) `python3 plugin/tests/run.py test_prove -k infra_finish 2>&1 | tail -40` → ✗ exit 1 · Ran 3 tests in 2.5s (1 classes, 16 at a time; slowest: InfraFinish 2s) / FAILED (1 classes: test_prove.InfraFinish) [ran] [tree 81f583616ba0] (2026-10-31T14:46:28Z)
- (ac 2) `python3 plugin/tests/run.py test_prove -k infra_finish 2>&1 | tail -30` → exit 0 · Ran 3 tests in 4.1s (1 classes, 16 at a time; slowest: InfraFinish 4s) / OK [ran] [tree c6d1b45b5d79] (2026-10-31T14:46:39Z)
- (step 1) `python3 plugin/tests/run.py test_prove -k infra_finish 2>&1 | tail -30` → exit 0 · Ran 3 tests in 4.1s (1 classes, 16 at a time; slowest: InfraFinish 4s) / OK [ran] [tree c6d1b45b5d79] (2026-10-31T14:46:39Z)
- (step 4) `python3 plugin/tests/run.py test_prove 2>&1 | tail -8` → exit 0 · Ran 25 tests in 7.7s (6 classes, 16 at a time; slowest: InfraProof 7s, InfraFinish 6s, VerifyStrength 3s) / OK [ran] [tree fa4a58a04077] (2026-10-31T14:47:12Z)
- (step 1) `python3 plugin/tests/run.py test_prove -k infra_proof` → exit 0 · Ran 10 tests in 10.4s (1 classes, 16 at a time; slowest: InfraProof 9s) / OK [ran] [tree fa4a58a04077] (2026-10-31T14:47:27Z)
- (step 2) `python3 plugin/tests/run.py test_prove -k infra_proof` → exit 0 · Ran 10 tests in 8.5s (1 classes, 16 at a time; slowest: InfraProof 8s) / OK [ran] [tree fa4a58a04077] (2026-10-31T14:47:38Z)
- (step 3) `python3 plugin/tests/run.py test_prove -k infra_proof` → exit 0 · Ran 10 tests in 7.6s (1 classes, 16 at a time; slowest: InfraProof 7s) / OK [ran] [tree fa4a58a04077] (2026-10-31T14:47:47Z)
- (step 4) `python3 plugin/tests/run.py test_prove -k infra_finish` → exit 0 · Ran 3 tests in 5.0s (1 classes, 16 at a time; slowest: InfraFinish 5s) / OK [ran] [tree fa4a58a04077] (2026-10-31T14:47:53Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 430 tests in 54.5s (94 classes, 16 at a time; slowest: TaskLifecycle 54s, VerifyStrength 30s, BoardVerbs 27s) / FAILED (1 classes: test_docs.ReadmeShape) [ran] [tree fa4a58a04077] (2026-10-31T14:48:51Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 430 tests in 79.9s (94 classes, 16 at a time; slowest: TaskLifecycle 79s, BoardVerbs 51s, VerifyStrength 50s) / FAILED (1 classes: test_docs.ReadmeShape) [ran] [tree 903af4a71da6] (2026-10-31T14:50:25Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.86s] [ran] [tree cad0a29298b3] (2026-10-31T14:52:15Z)
- (step 1) `python3 plugin/tests/run.py test_prove` → exit 0 · Ran 33 tests in 11.7s (6 classes, 16 at a time; slowest: InfraProof 11s, InfraFinish 8s, VerifyStrength 4s) / OK [ran] [tree acfbcf1b4fe8] (2026-10-31T15:00:48Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [57.66s] [ran] [tree acfbcf1b4fe8] (2026-10-31T15:03:10Z)
- (step 1) `python3 plugin/tests/run.py test_prove` → exit 0 · Ran 30 tests in 5.6s (5 classes, 16 at a time; slowest: DocsProof 5s, VerifyStrength 2s, Migration 2s) / OK [ran] [tree b06efae68646] (2026-10-31T15:34:48Z)
- (step 1) `python3 plugin/tests/run.py test_prove test_docsdrift test_tool_loop` → exit 0 · Ran 84 tests in 55.4s (10 classes, 16 at a time; slowest: MissLoop 55s, InfraProof 8s, InfraFinish 6s) / OK [ran] [tree 4f20679bea11] (2026-10-31T15:45:34Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k infra_proof` → exit 0 · Ran 17 tests in 8.4s (1 classes, 16 at a time; slowest: InfraProof 8s) / OK [ran] [tree 578cdd0254ad] (2026-10-31T15:46:04Z)
- (ac 2) `python3 plugin/tests/run.py test_prove -k infra_finish` → exit 0 · Ran 4 tests in 5.0s (1 classes, 16 at a time; slowest: InfraFinish 5s) / OK [ran] [tree 578cdd0254ad] (2026-10-31T15:46:04Z)
- (audit intent) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 6 MEDIUM), all fixed on the branch: a silent non-zero exit fails, a bad shebang is unproven, shellcheck and hadolint at warning, a compose include URL is unproven and never run, validators under unshare -r -n where it works, terraform missing providers unproven, every failing file named, the copy is listed files only with a 200 MB cap and a 90 s finish budget; merge conflicts with T-2381 resolved keeping both; 84 tests OK after merge` → infra files are proven by their own validators offline; a missing validator labels unproven, never pass (tested with stubs) [tree 578cdd0254ad] (2026-10-31T15:46:04Z)
- (audit adversary) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 6 MEDIUM), all fixed on the branch: a silent non-zero exit fails, a bad shebang is unproven, shellcheck and hadolint at warning, a compose include URL is unproven and never run, validators under unshare -r -n where it works, terraform missing providers unproven, every failing file named, the copy is listed files only with a 200 MB cap and a 90 s finish budget; merge conflicts with T-2381 resolved keeping both; 84 tests OK after merge` → no verb in the table reaches a network or account; compose includes with URLs never run; unshare -n where available; output redacted [tree 578cdd0254ad] (2026-10-31T15:46:04Z)
- (audit edge) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 6 MEDIUM), all fixed on the branch: a silent non-zero exit fails, a bad shebang is unproven, shellcheck and hadolint at warning, a compose include URL is unproven and never run, validators under unshare -r -n where it works, terraform missing providers unproven, every failing file named, the copy is listed files only with a 200 MB cap and a 90 s finish budget; merge conflicts with T-2381 resolved keeping both; 84 tests OK after merge` → a validator that dies silently fails; a broken tool is unproven, not a crash [tree 578cdd0254ad] (2026-10-31T15:46:04Z)
- (audit operator) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 6 MEDIUM), all fixed on the branch: a silent non-zero exit fails, a bad shebang is unproven, shellcheck and hadolint at warning, a compose include URL is unproven and never run, validators under unshare -r -n where it works, terraform missing providers unproven, every failing file named, the copy is listed files only with a 200 MB cap and a 90 s finish budget; merge conflicts with T-2381 resolved keeping both; 84 tests OK after merge` → copy capped at 200 MB, finish budget 90 s, each tool clamped to the time left [tree 578cdd0254ad] (2026-10-31T15:46:04Z)
- (audit maintainer) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 6 MEDIUM), all fixed on the branch: a silent non-zero exit fails, a bad shebang is unproven, shellcheck and hadolint at warning, a compose include URL is unproven and never run, validators under unshare -r -n where it works, terraform missing providers unproven, every failing file named, the copy is listed files only with a 200 MB cap and a 90 s finish budget; merge conflicts with T-2381 resolved keeping both; 84 tests OK after merge` → the weakest link is the real validators' flags (stubs only on this machine), noted [tree 578cdd0254ad] (2026-10-31T15:46:04Z)
## Log
- 2026-10-31T14:02:37Z created
- 2026-10-31T14:35:29Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2385.builder.md
- 2026-10-31T14:35:42Z focused
- 2026-10-31T14:35:43Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T15:44:34Z merged worktree-agent-a95c4be9345c9d047 (6 file(s))
- 2026-10-31T15:44:35Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a95c4be9345c9d047
- 2026-10-31T15:44:36Z focused
- 2026-10-31T15:45:49Z scope: plugin/lib/fminfra.py, plugin/lib/fmprove.py, plugin/lib/fmcli.py, plugin/tests/test_prove.py, README.md, MASTER.md, CHANGELOG.md
- 2026-10-31T15:47:23Z done
- 2026-10-31T15:47:27Z committed 522e9dd5 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2389 [FEATURE M, planned, 4 steps] Release proof (Mission 7, #10): fm prove --release builds the repo's artifact offline, installs it into a throwaway prefix and runs …
- T-2273 [FEATURE M, done, 3 steps] Unproven rollup (Mission 7, #6): done tasks whose criteria rest on typed or inconclusive evidence, or UI changes with no visual check, …
- T-2387 [FEATURE M, planned, 4 steps] Data proof (Mission 7, #10): fm prove --data runs a data command on a throwaway copy of its database and checks the task's declared …
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
## Lessons
- A validator's silence isn't a pass: only a clean exit with output that says so proves anything
## Files touched
- plugin/tests/test_prove.py
- plugin/lib/fminfra.py
- plugin/lib/fmprove.py
- plugin/lib/fmcli.py
- README.md
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmcode.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmdocs.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmeco.py
- plugin/lib/fmfixes.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/lib/fmlong.py
- plugin/lib/fmmiss.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmrecall.py
- plugin/lib/fmtrials.py
- plugin/skills/intake/references/planning.md
- plugin/tests/bench_hooks.py
- plugin/tests/helpers.py
- plugin/tests/test_backlog.py
- plugin/tests/test_batch.py
- plugin/tests/test_builder.py
- plugin/tests/test_clean_helpers.py
- plugin/tests/test_cli.py
