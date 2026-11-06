---
id: T-2946
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T09:30:30Z
updated: 2026-11-04T11:12:12Z
builder_model: haiku
base: 7fd70ad0efbe024de52dd374480224ed03b599ea
base_tree: 933cc4b302ec4ce9343cdfac9d3efcdb14633e9f
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-04T09:46:02Z
plan0_scope: []
lane_stop: merged 2026-11-04T10:48:22Z
verified: strong
unproven: [docs, meaning, ui-unshot]
---
# Leftover Foreman in user-visible text (T-2742 step 9 cold review): the guard's refusals…
## Raw request
> Leftover Foreman in user-visible text (T-2742 step 9 cold review): the guard's refusals and no-active-task block say 'Foreman guard:'/'Foreman:' (fmguard.py 244-330, 48-66, 2086, 2244, 3756, 3762) - emit 'Sampo guard:'/'Sampo:' and keep every reader matching both (replay.py:85, register.tsx:121, KEPT); the output style is named Foreman and triggers on 'Foreman project' (plugin/output-styles/foreman.md:2,9; setup.py:30 keeps reading foreman:Foreman); looks.html title and eyebrow; hooks.json description; hook:116 and bin/fm docstring; serve.py:67 ' (foreman)'; agents.py:194 markers write sampo and read foreman; doctor.py:991; site/pages.py:170 decisions tape through _say(); plugin/README.md, evals, observability, bench READMEs; widen test_rename_scan's surface list to fmguard.py, looks.html, hooks.json and those READMEs so the scan sees them
## Interpretation
Reading 1 (chosen): every place a user still reads "Foreman" outside history and the alias list says Sampo (or Ward for the guard), every reader of the old text keeps matching it (older transcripts and logs still carry it), and test_rename_scan's surface list widens to the files the cold review found it missed, so the scan's count is honest.
Reading 2 (ruled out): rename the guard's module and plugin ids too. The ids are aliases the rename keeps (T-2879 plans the id move); this task changes only text a user reads.
## Assumptions (confidence)
## Acceptance criteria
- [x] the guard's refusals say 'Ward: blocked <cat>:' and its no-task block 'Sampo:'; replay, cost, the mod and the hooks still read both the new and the old forms — verify with `python3 plugin/tests/run.py test_guard test_replay test_rename_scan`
- [x] the output style is named Sampo and triggers on 'Sampo project'; a stored foreman:Foreman still selects it — verify with `python3 plugin/tests/run.py test_setup test_rename_scan`
- [x] test_rename_scan covers fmguard.py, looks.html, hooks.json, hook, bin/fm and the plugin READMEs, and its BASELINE falls to the new count — verify with `python3 plugin/tests/run.py test_rename_scan`
- [x] the full gates pass — verify with `sampo check`
## Non-goals
## Approach (options → choice → why)
1) Writers first, readers already wide: the guard emits "Ward: blocked {cat}: …" (cost.py:1556, replay.py:85 and register.tsx:121 already read "Ward: blocked"), "Sampo: no active task …", and the posture texts say Sampo; the output style is named Sampo with setup.py selecting foreman:Sampo and still accepting a stored foreman:Foreman; the other strings and READMEs reworded; the scan's file list gains fmguard.py, looks.html, hooks.json, hook, bin/fm and the plugin READMEs, and BASELINE drops to what is left. Likely outcome: the scan reaches its new honest count, no reader breaks. Fails if: a test or mod matches the literal "Foreman guard:" text, which the builder greps for first.
2) use what exists: add the files to the scan only, and leave the text until T-2879. Likely outcome: an honest count, no user-visible change. Fails if: users keep reading "Foreman guard" on every refusal, the most-seen line.
3) do less: only the guard prefix and the output style (the main path). Likely outcome: the visible lines fixed in a small diff. Fails if: the scan still can't see the rest, so they come back unnoticed.
Choice 1 (85%): the cold review already found every site, and the readers already accept the new forms.
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, MASTER.md, plugin/tests/test_site.py, site/stats.py, site/build.py; past FIXes T-2061, T-2064.
## Execution prompt
## Steps
1. [x] widen the scan's surface list first (red: the new files' Foreman lines counted)
2. [x] guard writers to Ward/Sampo, keeping readers on both forms; fix tests that assert the old text
3. [x] output style, looks.html, hooks.json, hook, bin/fm, serve.py, agents.py markers, doctor.py, site/pages.py _say, READMEs
4. [x] BASELINE to the new count; full check
## Resume here
<!-- auto -->
- 2026-11-04T09:56:45Z step 3/4: output style, looks.html, hooks.json, hook, bin/fm, serve.py, agents.py markers, doctor.py, site/pages.py _say, READMEs
- git: worktree-agent-a450348821f974554; 21 uncommitted: bench/spec-suite/README.md, plugin/README.md, plugin/bin/fm, plugin/evals/README.md, plugin/hooks/hook, plugin/hooks/hooks.json, plugin/lib/fmguard.py, plugin/lib/looks.html, plugin/lib/sampo/agents.py, plugin/lib/sampo/serve.py
- touched since last checkpoint: plugin/tests/test_rename_scan.py, .fm-scratch/guard.json, .fm-scratch/g2.json, plugin/tests/test_guard.py, plugin/tests/test_pass4.py, plugin/tests/test_code.py, plugin/tests/test_docs.py, plugin/tests/test_setup.py, plugin/lib/sampo/setup.py, plugin/output-styles/foreman.md, .fm-scratch/ag.json, plugin/lib/sampo/agents.py, plugin/lib/sampo/serve.py, plugin/tests/test_agents.py, .fm-scratch/misc.json
## Docs impact
CHANGELOG line (T-2946); README and INSTALL already say Sampo
## Verification evidence
- (step 3) `python3 plugin/tests/run.py test_setup test_docs test_agents test_rename_scan test_guard test_replay 2>&1 | tail -4` → exit 0 · Ran 524 tests in 11.4s (141 classes, 16 at a time; slowest: Mutation 10s, Fences 8s, Hook 7s) / OK [ran] [tree 508228139a1e] [world 2f1906870a] (2026-11-04T09:58:50Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_replay test_rename_scan` → exit 0 · Ran 347 tests in 9.8s (98 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 6s, RenameScan 5s) / OK [ran] [tree 508228139a1e] [world 2f1906870a] (2026-11-04T09:59:06Z)
- (step 2) `python3 plugin/tests/run.py test_setup test_rename_scan` → exit 0 · Ran 52 tests in 3.3s (11 classes, 16 at a time; slowest: RenameScan 3s, Install 2s, NoClaude 2s) / OK [ran] [tree 508228139a1e] [world 2f1906870a] (2026-11-04T09:59:10Z)
- (step 3) `python3 plugin/tests/run.py test_agents test_docs` → exit 0 · Ran 139 tests in 8.5s (37 classes, 16 at a time; slowest: Fences 8s, Hook 5s, DocsProof 2s) / OK [ran] [tree 508228139a1e] [world 2f1906870a] (2026-11-04T09:59:19Z)
- (step 4) `sampo check --affected` → ✗ exit 1 · ✗ affected tests only (141): python3 plugin/tests/run.py test_affected_hubs test_agents test_approve_reads test_audit_run test_bench test_bench_family test_board_posture test_board_surfaces test_board [ran] [tree 508228139a1e] [world 2f1906870a] (2026-11-04T10:03:31Z)
- (step 4) `python3 plugin/tests/run.py test_exam test_rename_scan test_guard test_replay test_setup test_agents test_docs` → exit 0 · Ran 638 tests in 107.4s (168 classes, 16 at a time; slowest: LeanKind 101s, JudgmentKinds 75s, ExamAuthors 73s) / OK [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:56:07Z)
- `python3 plugin/tests/run.py test_rename_scan test_guard test_replay` → ✗ exit 1 · Ran 347 tests in 19.4s (98 classes, 16 at a time; slowest: Mutation 17s, GuardAgainstBash 13s, Trust 9s) / FAILED (2 classes: test_guard.InterpreterWrites, test_rename_scan.RenameScan) (start tree + this task's tests) [ran] [tree fabf0af611b5] [world 2f1906870a] (2026-11-04T10:57:04Z)
- `python3 plugin/tests/run.py test_rename_scan test_guard test_replay` → exit 0 · Ran 347 tests in 20.3s (98 classes, 16 at a time; slowest: Mutation 20s, GuardAgainstBash 17s, Trust 8s) / OK [ran] [tree fabf0af611b5] [world 2f1906870a] (2026-11-04T10:57:04Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_replay test_rename_scan` → exit 0 · Ran 347 tests in 19.7s (98 classes, 16 at a time; slowest: Mutation 19s, GuardAgainstBash 15s, RenameScan 10s) / OK [ran] [tree fabf0af611b5] [world 2f1906870a] (2026-11-04T11:07:49Z)
- (ac 2) `python3 plugin/tests/run.py test_setup test_rename_scan` → exit 0 · Ran 57 tests in 6.2s (11 classes, 16 at a time; slowest: RenameScan 6s, Install 3s, NoClaude 3s) / OK [ran] [tree fabf0af611b5] [world 2f1906870a] (2026-11-04T11:07:49Z)
- (ac 3) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 10 tests in 6.1s (1 classes, 16 at a time; slowest: RenameScan 6s) / OK [ran] [tree fabf0af611b5] [world 2f1906870a] (2026-11-04T11:07:49Z)
- (ac 4) `sampo check` → exit 0 · ✓ python3 plugin/tests/run.py → exit 0 · Ran 6199 tests in 343.7s (1325 classes, 16 at a time; slowest: LeanKind 117s, Worker 96s, Stop 76s) / OK (344.1 s) / ✓ fm replay → exit 0 · 4998 new to the cor [ran] [tree fabf0af611b5] [world 2f1906870a] (2026-11-04T11:07:49Z)
- (audit intent) `the T-2742 step-9 cold review found every site (fm-reviewer, intent lens); the builder grepped every reader before changing a writer; LeanKind's red (louhi's posture anchor copied the guard's text) was fixed on the branch` → no user-visible Foreman outside history and the alias list on the surfaces the review named; the scan widened to them and its BASELINE fell 19 → 16, each left a reader or a kept protocol string [tree fabf0af611b5] (2026-11-04T11:07:49Z)
- (audit adversary) `the T-2742 step-9 cold review found every site (fm-reviewer, intent lens); the builder grepped every reader before changing a writer; LeanKind's red (louhi's posture anchor copied the guard's text) was fixed on the branch` → every reader of the refusal text (replay _REFUSAL, cost, register.tsx, the guard's _hint, the guard-publish grader) matches both 'Ward: blocked' and 'Foreman guard: blocked', so old transcripts and logs still parse [tree fabf0af611b5] (2026-11-04T11:07:49Z)
- (audit maintainer) `the T-2742 step-9 cold review found every site (fm-reviewer, intent lens); the builder grepped every reader before changing a writer; LeanKind's red (louhi's posture anchor copied the guard's text) was fixed on the branch` → louhi's planted-mutation anchor duplicates the guard's posture text, so a rewording breaks LeanKind again; it should read the text from fmguard [tree fabf0af611b5] (2026-11-04T11:07:49Z)
## Log
- 2026-11-04T09:30:30Z created
- 2026-11-04T09:31:34Z planned: it has criteria and steps
- 2026-11-04T09:45:49Z set approved=True
- 2026-11-04T09:45:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2946.builder.md
- 2026-11-04T09:46:01Z focused
- 2026-11-04T09:46:02Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-04T10:48:22Z merged worktree-agent-a450348821f974554 (23 file(s))
- 2026-11-04T10:54:13Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a450348821f974554
- 2026-11-04T10:54:13Z focused
- 2026-11-04T10:56:20Z scope: the cold review's file list (guard, output style, setup, looks, hooks.json, hook, bin/fm, serve, agents, doctor, site/pages, READMEs, replay, cost, the mod's register.tsx, the guard-publish eval grader, louhi's posture anchor) and test_rename_scan
- 2026-11-04T11:12:11Z done
- 2026-11-04T11:12:12Z committed 2960fc75 (1 file)
## Follow-ups captured
## Scope
plugin/lib/fmguard.py, plugin/lib/sampo/{replay,cost,setup,serve,agents,doctor}.py, plugin/output-styles/foreman.md, plugin/lib/looks.html, plugin/hooks/hooks.json, plugin/hooks/hook, plugin/bin/fm, site/pages.py, plugin/README.md, plugin/evals/README.md, plugin/observability/*, bench/spec-suite/README.md, plugin/tests/**
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
## Why not caught
test_rename_scan's surface list left out fmguard.py, looks.html, hooks.json, the hook and the plugin READMEs; it now covers them
## Lessons
- A rename's scan must list every surface a user reads, or its count is a false zero: four surfaces were outside it
## Plan gaps
- failed first: step 4 BASELINE to the new count; full check
## Files touched
- plugin/tests/test_rename_scan.py
- .fm-scratch/guard.json
- plugin/lib/fmguard.py
- .fm-scratch/g2.json
- plugin/tests/test_guard.py
- plugin/tests/test_pass4.py
- plugin/tests/test_code.py
- plugin/tests/test_docs.py
- plugin/tests/test_setup.py
- plugin/lib/sampo/setup.py
- plugin/output-styles/foreman.md
- .fm-scratch/ag.json
- plugin/lib/sampo/agents.py
- plugin/lib/sampo/serve.py
- plugin/tests/test_agents.py
- .fm-scratch/misc.json
- plugin/bin/fm
- plugin/hooks/hook
- plugin/hooks/hooks.json
- plugin/lib/looks.html
- site/pages.py
- .fm-scratch/rd.json
- bench/spec-suite/README.md
- plugin/README.md
- plugin/evals/README.md
- plugin/observability/README.md
- .fm-scratch/g3.json
- plugin/evals/guard-publish/graders/blocked-in-trace.md
- plugin/lib/sampo/louhi.py
- CHANGELOG.md
