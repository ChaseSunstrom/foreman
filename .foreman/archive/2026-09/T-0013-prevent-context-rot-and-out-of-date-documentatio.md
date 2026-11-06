---
id: T-0013
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmdoctor.py, plugin/lib/fmtidy.py, plugin/lib/fmsetup.py, plugin/tests/**, plugin/rules/foreman.md, plugin/skills/**, MASTER.md, README.md]
depends_on: []
source: user
created: 2026-09-26T12:41:56Z
updated: 2026-09-26T14:33:17Z
---
# Context rot and doc drift defenses
## Raw request
> Prevent context rot and out-of-date documentation: detect docs that drift from code/CLI/rules, require doc updates as part of done, keep long sessions grounded (fresh re-injection of the brief, compaction hygiene)
## Interpretation
Two kinds of rot. (1) Context rot: long sessions degrade the model's grip on the task. Defenses: compact earlier and more often at safe points (Foreman state makes compaction cheap: PreCompact checkpoint + SessionStart re-injection), keep every turn anchored with the next action (T-0012), and run each task in a fresh session in headless mode (T-0014). (2) Doc drift: docs that no longer match code. Defenses: docs impact recorded per M/L task, doctor checks for Foreman's own docs, and a drift scan for any repo.
## Assumptions (confidence)
## Acceptance criteria
- [x] M/L tasks can't be done without a Docs impact section (files updated or 'none: why'); docs it names must exist and show no drift — verify with `python3 -m unittest test_core test_cli`
- [x] fm docs reports markdown references to missing paths in any repo, and npm/make commands that aren't defined where package.json/Makefile exist; tidy and fm task done surface it — verify with `python3 -m unittest test_docsdrift test_tidy test_cli`
- [x] fm doctor fails when Foreman's own docs drift (fm subcommands vs MASTER.md, commands named in rules/skills/README, skills/agents list, install.sh flags vs README) — verify with `python3 -m unittest test_doctor`
- [x] Context: compaction threshold configured reversibly if supported; context use visible; task-boundary note above threshold — verify with `python3 -m unittest test_setup test_hooks; live check`
## Non-goals
## Approach (options → choice → why)
Docs: (1) a 'Docs impact' section required by done_blockers for M/L (files updated, or 'none: <why>') + fm docs drift scan (markdown references to paths, fm/npm/make commands and CLI flags that don't exist) wired into tidy/doctor and the operator audit lens [chosen: deterministic, cheap]; (2) LLM doc review every task [rejected: costly, nondeterministic — the operator lens already covers judgement].
Foreman's own docs: doctor checks every fm subcommand is in MASTER.md, every fm command named in rules/skills/README exists, every skill/agent is listed, README flags match install.sh --help.
Context: earlier auto-compaction if Claude Code supports a threshold setting (verify; install-user records it for uninstall); statusline shows context use; at a task boundary above the threshold the Stop note says so factually; fresh-session-per-task in the headless runner (T-0014).
## Risks and rollback
Risk: drift scanner false positives (code blocks, examples) → skip fenced blocks marked as examples, report-only by default. Risk: docs gate nags on doc-less changes → 'none: why' is one line. Rollback: git revert; fm uninstall-user restores settings.
## Execution prompt
## Steps
1. [x] Docs impact gate (TDD)
2. [x] fm docs drift scanner + tidy/doctor wiring (TDD)
3. [x] Foreman self-doc checks in doctor (TDD)
4. [x] Context: compaction threshold + context-use note (verify support first; TDD)
5. [x] Docs, audits, bench
## Resume here
T-0013 step 5 next: docs, audits, bench
<!-- auto -->
- 2026-09-26T14:02:54Z step 5/5: Docs, audits, bench
- git: foreman/build; 0 uncommitted
## Verification evidence
- (step 1) `python3 -m unittest test_core (docs impact gate, documenting stage); full suite` → RED 2 failures then OK; suite OK (2026-09-26T13:51:55Z)
- (step 2) `python3 -m unittest test_docsdrift test_tidy; fm docs ~/.claude/foreman` → RED then OK; precision tuned from 304 (noise) to 0 on Foreman, 5/5 seeded drifts found in the test repo (2026-09-26T13:54:47Z)
- (step 3) `python3 -m unittest test_doctor (self docs); fm doctor` → RED then OK; found and fixed MASTER.md missing fm init; doctor 21/0/0 (2026-09-26T14:00:13Z)
- (step 4) `docs: CLAUDE_AUTOCOMPACT_PCT_OVERRIDE (env-vars.md) and statusline context_window.used_percentage (statusline.md); python3 -m unittest test_setup test_hooks; fm install-user` → verified in docs; RED then OK; live settings env CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70 recorded in manifest env_added (2026-09-26T14:02:39Z)
- (step 5) `MASTER/README/CHANGELOG updated (16370b4, 8f0a3ad); audit wave 3 + re-audit fixed; unittest discover; bench_hooks --runs 30; fm doctor; fm docs` → docs name fm docs, Docs impact at done, state fallback + restore, hints vs gates; 272 tests OK; p95 SessionStart 40.9, UserPromptSubmit 40.6, PreToolUse 42.5 ms; doctor 22/0/0; no doc drift (2026-09-26T14:30:25Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_core test_cli` → OK (docs impact gate; named docs must exist and be drift-free: test_docs_named_in_docs_impact_must_exist_and_be_current) (2026-09-26T14:30:25Z)
- (ac 2) `python3 -m unittest test_docsdrift test_tidy test_cli; fm docs` → OK; fm docs on Foreman: no drift; tidy docs_drift findings; done reports other drift (2026-09-26T14:30:25Z)
- (ac 3) `python3 -m unittest test_doctor; fm doctor` → OK; doctor 22 pass incl. self docs (2026-09-26T14:30:26Z)
- (ac 4) `python3 -m unittest test_setup test_hooks; jq .env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE ~/.claude/settings.json; statusline with used_percentage 63` → OK; live 70 (manifest env_added, reversed by uninstall-user); statusline shows 'Context ██████░░░░ 63%'; Stop note at >=60% at task boundary (test_hooks) (2026-09-26T14:30:26Z)
- (step 5) `python3 -m unittest discover -s plugin/tests -t plugin/tests` → Ran 267 tests in 49.4s — OK (corrects the 272 in the earlier line) (2026-09-26T14:31:23Z)
- (audit intent) `fm-reviewer intent lens over wave3.diff + wave3-stages-early.diff (user's verbatim asks A–C only); research wave3-intent` → approve with nits: docs gate free-text → named docs must exist and be drift-free at done, other drift reported (16370b4); hint-vs-gate wording fixed in README/CHANGELOG/MASTER [tree 99736f772dcc] (2026-09-26T14:33:17Z)
- (audit adversary) `fm-reviewer adversary lens over wave3 diffs, then re-audit (adversary+edge) of 16370b4; research wave3-adversary, wave3-reaudit` → CRITICAL fallback-marker state redirect → guard protects all fallback locations, private-dir markers only (16370b4); re-audit CRITICAL tar -x -C bypass → archives/clones/-t/wget -P checked by destination (8f0a3ad, 78bedb0); no open findings [tree 99736f772dcc] (2026-09-26T14:33:17Z)
- (audit edge) `fm-reviewer edge lens over wave3 diffs + re-audit edge pass; research wave3-edge` → plan-only false positives, ? in code fences, sticky fallback with no way back, worktree_id cost, ask lock race → all fixed test-first (16370b4); XDG/TMPDIR disagreement documented as a limitation; eval setup symlinks verified by eval 1.1g [tree 99736f772dcc] (2026-09-26T14:33:17Z)
- (audit operator) `fm-reviewer operator lens over wave3 diffs (upgrade path, env var, fallback, approvals, messages, hook failures); research wave3-operator; plus roundtrip after the uninstall reorder` → doctor env check, SessionStart next_for isolation, fallback WARN with fm doctor --restore-state, pending-approval recovery documented (16370b4); uninstall leftover maps fixed (roundtrip 17/17) [tree 99736f772dcc] (2026-09-26T14:33:17Z)
- (audit maintainer) `fm-reviewer maintainer lens over wave3 diffs; research wave3-maintainer` → one Foreman-module rule in the guard, shared ASK_TTL, named lock waits, fm ask retry message (16370b4); check_self_docs size left as is (four short checks, one caller) [tree 99736f772dcc] (2026-09-26T14:33:17Z)
## Log
- 2026-09-26T12:41:56Z created
- 2026-09-26T12:51:09Z planned from capture
- 2026-09-26T13:01:15Z user approved core in chat
- 2026-09-26T13:01:42Z set approved=True
- 2026-09-26T13:01:42Z approved by user in chat: 'yes, to all of your things … you have FULL permission for the rest of this session to go full auto'
- 2026-09-26T13:50:28Z focused
- 2026-09-26T13:55:17Z paused: focus moved to T-0009
- 2026-09-26T13:57:58Z focused
- 2026-09-26T14:02:54Z paused: focus moved to T-0009
- 2026-09-26T14:21:50Z audit wave 3 (intent/adversary/edge/operator/maintainer; research wave3-*) findings fixed test-first in 16370b4: fallback-state redirect closed, restore-state, docs checked at done, notifications not user words, plan-only regex, fences, worktree_id stat cache, guard module rule, named locks, ASK_TTL, doctor env check
- 2026-09-26T14:24:20Z scope: AC2 narrowed to what fm docs can check without noise — generic fm commands and CLI flags produced 304 false findings on Foreman (step 2) and can't be verified in arbitrary repos; Foreman's own fm commands and flags are covered by doctor (AC3). 'doctor surfaces it' → 'fm task done surfaces it' (audit wave 3 intent finding); AC1 now includes named docs existing and drift-free (16370b4)
- 2026-09-26T14:31:23Z correction: step 5 evidence said '272 tests OK'; the actual run is 267 tests, all OK
- 2026-09-26T14:33:17Z done
## Follow-ups captured
## Docs impact
MASTER.md: CLI line (docs, doctor --restore-state), §9 state location, §10 hints vs gates + guard note; README.md: Docs stay current; CHANGELOG.md: 1.1.0 context/docs + final audit wave entries; plugin/rules/foreman.md: Docs impact + fm docs.
