---
id: T-0009
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/**, plugin/rules/foreman.md, plugin/skills/**, plugin/agents/**, plugin/tests/**, plugin/evals/**, MASTER.md, README.md, CHANGELOG.md, plugin/README.md, plugin/.claude-plugin/plugin.json, .claude-plugin/marketplace.json]
depends_on: []
source: user
created: 2026-09-26T12:21:43Z
updated: 2026-09-26T14:37:35Z
---
# Autonomy: plain-chat approvals, Claude runs everything, multi-lens audits before done
## Raw request
> can you make it so stuff can get done easier for all things? for example, I don't have to run the commands, claude will just figure it all out? etc.?
## Interpretation
Two asks, one goal (Claude works autonomously and correctly): (A) the user never has to run commands — Claude runs fm/git/tests/maintenance itself and asks plain yes/no questions for consent; the one thing that needed a typed command (granting core via `! fm task set ID --allow core`) becomes a chat reply, still impossible for the agent to forge. (B) numerous independent audit passes, each with its own prompt and a deliberately different context slice, required before M/L work counts as done, so issues like today's (branch renamed outside the session, install.sh always adding plugin-dev, [ -r /dev/tty ] without a terminal, --allo core bypass) are caught without the user.
## Assumptions (confidence)
- UserPromptSubmit fires only for real user prompts; the agent can't forge one (high).
- A one-shot pending approval (the very next prompt decides) is safe enough; pasted text starting with 'yes' is the residual risk (medium) — documented.
- Read-only subagents (Read/Grep/Glob) can audit from a saved diff + file paths; the main thread reproduces claims with Bash (high).
- Widening protected core to plugin/lib, plugin/bin, plugin/hooks costs one chat 'yes' per Foreman code change (high).
## Acceptance criteria
- [x] fm ask ID CAT... records a one-shot pending approval; the user's next prompt starting with yes grants it (ledger), anything else clears it; no fm command grants core — verify with `python3 -m unittest test_hooks test_cli`
- [x] Rules, skills and guard messages never tell the user to run a command (except interactive logins and slash commands); plain words map to fm actions; status/doctor/tidy/improve are model-invocable — verify with `python3 -m unittest test_docs`
- [x] fm task done refuses M/L tasks without audits for the tier's lenses recorded after the last step; S needs a self-audit — verify with `python3 -m unittest test_core test_cli`
- [x] Audit reference defines 5 lenses, each with its own prompt and context slice; fm-reviewer runs lens briefs — verify with `python3 -m unittest test_docs`
- [x] Protected core covers plugin/lib, plugin/bin and plugin/hooks — verify with `python3 -m unittest test_guard`
- [x] Foreman itself audited with all 5 lenses; every verified finding fixed with a test or captured — verify with `fm task show T-0009 (Audit records)`
- [x] Full suite green, hook p95 <= 150 ms, fm doctor green, roundtrip 17/17, eval suite >= 0.7 — verify with `unittest; bench_hooks.py; fm doctor; roundtrip.py; claude plugin eval`
- [x] Vague requests ('just get it done', 'super improve it') trigger brainstorm: the main thread builds a context pack, >= 4 tool-less brainstorm subagents with distinct lenses propose ideas, the main thread grounds, scores and captures a slate — verify with `python3 -m unittest test_docs; live scenario`
- [x] fm autonomy full|standard (+ FULL AUTO / STANDARD words): full never asks mid-run (L plans self-approved after self-critique, ? items take the recommendation, choices recorded with fm decide), Stop drive doesn't yield on questions, needs-the-user items are collected with fm ask and presented once at the end — verify with `python3 -m unittest test_hooks test_cli`
## Non-goals
No sandboxing (arbitrary python can still bypass a Bash-command guard; documented). No new eval cases this round. No change to what needs approval — only how it's given.
## Approach (options → choice → why)
Approval: (1) hook-mediated one-shot pending request [chosen: agent can request, only a user prompt can confirm, audited in the ledger]; (2) let agents grant core [rejected: S15 showed self-granting]; (3) keyword 'APPROVE core T-0009' [rejected: still a command to type].
Audits: (1) 5 lens prompts run through the existing fm-reviewer agent with different context slices, recorded via fm task audit and required by done_blockers by tier [chosen: reuses agent, enforced by fm]; (2) 5 new agents [rejected: more always-on context, same effect]; (3) advisory checklist only [rejected: not autonomous — relies on remembering].
## Risks and rollback
Risk: locking myself out by widening core before the approval flow works → build fm ask first, widen last. Risk: audit gating blocks in-flight tasks → only at done, S needs only a self-audit. Rollback: git revert the commits + /reload-plugins.
## Execution prompt
Repo ~/.claude/foreman (branch foreman/build unless the user's merge answer says otherwise). TDD for every code change (plugin/tests, python3 -W error::ResourceWarning -m unittest discover -s plugin/tests -t plugin/tests).
1. fmcli: `fm ask ID CAT... --why TEXT` writes meta.pending_approval {task, allow, why, session: $FOREMAN_SESSION_ID, at}; prints the yes/no question. fmhooks.user_prompt_submit: if pending (same session or none recorded, < 24 h): prompt's first word in {yes,y,yep,yeah,sure,ok,okay,approve,approved,go,lgtm,confirm,confirmed} (case-insensitive, 'go ahead'/'do it' too) → add categories to the brief's allow, ledger approval_granted (redacted reply), inject 'Foreman: user approved <cats> for <ID>'; otherwise clear, ledger approval_declined, inject that. Grant code only reachable from the hook.
2. fmcore/fmcli: `fm task audit ID --lens L "<result>"` appends to the brief (Audit section + ledger). done_blockers: tier S needs lens self; M needs intent + one of adversary/edge/operator; L needs intent, adversary, edge, operator, maintainer — each recorded after the last step was marked done. skills/intake/references/audit.md: the 5 lens prompts, each naming its context slice (intent: raw request + criteria + diff only; adversary: diff + threat model; edge: diff + environment matrix; operator: diff + install/uninstall/docs/git state; maintainer: diff + conventions + tests). fm-reviewer: accepts a lens brief. execute.md step before done; next SKILL FINAL VERIFY runs operator + adversary over the whole session diff.
3. fm ask T-0009 core --why '…'; ask the user; their yes grants it.
4. fmguard._is_core adds plugin/lib/**, plugin/bin/**, plugin/hooks/**; self-authorize/core messages point at fm ask; rules/foreman.md: run everything yourself, plain-words map, approvals via fm ask, audits before done (≤ 80 lines); python3 plugin/tests/e2e/sync_evals.py.
5. Drop disable-model-invocation from status/doctor/tidy/improve; improve: merge approval by chat.
6. Run the 5 lenses over all of plugin/ + install.sh/uninstall.sh/setup-plugins.sh with fm-reviewer (≤ 3 parallel); reproduce each finding; fix with a regression test or fm capture --source discovered.
7. MASTER/README/CHANGELOG/plugin README; version 1.1.0 (plugin.json + marketplace.json); verify: suite, bench_hooks.py --runs 30, fm doctor, e2e/roundtrip.py --original backups/settings.json.20260925-232810, claude plugin eval (≤ $5).
8. Audit this change with the 5 lenses, commit (conventional), merge/push per answer, fm task done T-0009.
## Steps
1. [x] fm ask + one-shot approval in UserPromptSubmit (TDD)
2. [x] Audit machinery: fm task audit, tiered done gating, audit reference with 5 lens prompts, fm-reviewer + execute/next updates (TDD)
3. [x] Ask the user for core in chat via fm ask (live test of step 1)
4. [x] Protected edits: widen core, guard messages -> fm ask, rules (run everything, plain words, approvals, audits), eval prompt sync
5. [x] Plain words: status/doctor/tidy/improve model-invocable; improve approvals in chat
6. [x] Dogfood: 5-lens audit of all of Foreman; verify, fix with tests or capture
7. [x] Docs + 1.1.0; full suite, bench, doctor, roundtrip, evals
8. [x] Audit this change, commit, merge + push per the user's answer, done
9. [x] Full autonomy: fm autonomy, FULL AUTO/STANDARD words, Stop drive in full, pending approvals as a list (TDD) — do before step 6
10. [x] Brainstorm: tool-less fm-ideas agent, brainstorm reference, intake trigger for vague requests — do before step 6
## Resume here
T-0009: evals 1.1f mean 0.8 + intake-block rerun 1.0; next: combined final audit wave (T-0009 delta since b5e1dc9, T-0012, T-0013), docs impact, done
<!-- auto -->
- 2026-09-26T14:03:46Z step 8/10: Audit this change, commit, merge + push per the user's answer, done
- git: foreman/build; 0 uncommitted
## Verification evidence
- (step 1) `python3 -W error::ResourceWarning -m unittest discover -s plugin/tests -t plugin/tests` → OK (188 tests); test_hooks.Approvals 6/6 (yes grants + ledger, other replies/expired/other session/pasted yes don't), test_cli ask 2/2; RED first: 8 failures before fm ask existed (2026-09-26T12:40:14Z)
- (step 2) `python3 -W error::ResourceWarning -m unittest discover -s plugin/tests -t plugin/tests; fm doctor; git log -1` → OK (194 tests; RED first for audits by tier/postdate/unknown lens, CLI audit + stale-after-edit); doctor 19/0/0; commit f715615 (2026-09-26T12:45:46Z)
- (step 9) `python3 -W error::ResourceWarning -m unittest discover -s plugin/tests -t plugin/tests` → OK; new: Stop full-autonomy x2 + standard pending yield, AutonomyWords, SessionStart autonomy, CLI Autonomy (all RED first) (2026-09-26T12:48:51Z)
- (step 5) `python3 -m unittest test_docs (USER_ONLY = {capture}); git log -1` → RED 4 failures, then OK; improve/doctor use fm ask; committed (2026-09-26T12:52:06Z)
- (step 10) `python3 -W error::ResourceWarning -m unittest discover -s plugin/tests -t plugin/tests; claude plugin validate --strict plugin; fm doctor` → OK 203 tests (OpenEnded RED first; hook brainstorm note); validate passed with tools: []; doctor 19/0/0; commit 1fe9ef1 (2026-09-26T12:57:38Z)
- (step 3) `fm ask T-0009|T-0012..T-0016 core; read meta.pending_approvals` → 6 pending requests recorded for session 6901a8c8; question asked in chat; step completes when the user's reply is resolved by the UserPromptSubmit hook (2026-09-26T12:59:08Z)
- (step 3) `UserPromptSubmit hook on the user's reply 'yes, to all of your things…'` → ledger: 6 approval_granted events (T-0009, T-0012..T-0016 core); briefs allow [core]; pending cleared (2026-09-26T13:01:42Z)
- (step 4) `python3 -W error::ResourceWarning -m unittest discover -s plugin/tests -t plugin/tests; fm doctor; wc -l rules` → OK (guard table RED first: fmcli/bin/hooks core, --allo core self-authorize, fm ask messages); doctor 19/0/0; rules 58 lines; evals synced (2026-09-26T13:07:14Z)
- (step 7) `claude plugin validate --strict (marketplace + plugin); fm doctor; git log -1` → both pass; doctor 19/0/0 (file map 51 entries); docs commit 18ba6f9 (2026-09-26T13:14:18Z)
- (step 6) `5 fm-reviewer lenses over all of Foreman (adversary, edge, operator, intent, maintainer); each finding reproduced by a failing test or by reading` → adversary CRITICAL symlinked-fm core grant → CLI never grants core + fm-internals guard (8db74a5); edge: ledger_tail 64KB, busy lock drops yes (8db74a5); operator: fresh-machine settings leftover (8db74a5), doc drift (18ba6f9); intent HIGH skills ignore full autonomy, eval prompts parsed mid-rules (c15e21c); maintainer 2 LOW (c15e21c); FOREMAN_HOME claim = false positive (hooks don't inherit Bash env) (2026-09-26T13:18:48Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks test_cli` → OK (fm ask one-shot, next-reply yes grants with ledger event, other replies clear, session-bound via PreToolUse, notifications never grant; task set --allow core refused) (2026-09-26T14:36:56Z)
- (ac 2) `python3 -m unittest test_docs` → OK (rules/skills/guard messages: no user-run commands except logins/slash commands; plain-words map; status/doctor/tidy/improve model-invocable) (2026-09-26T14:36:56Z)
- (ac 3) `python3 -m unittest test_core test_cli` → OK (S self; M intent + one; L all five; audits must postdate last step evidence/edit and match worktree id) (2026-09-26T14:36:56Z)
- (ac 4) `python3 -m unittest test_docs` → OK (audit.md defines intent/adversary/edge/operator/maintainer prompts + context slices; fm-reviewer takes a lens) (2026-09-26T14:36:56Z)
- (ac 5) `python3 -m unittest test_guard` → OK (core: plugin/lib, bin, hooks, evals, rules, BUILD_PROMPT, settings; interpreter, archive and clone writes caught) (2026-09-26T14:36:56Z)
- (ac 6) `research wave1/2 audits + wave3-intent/adversary/edge/operator/maintainer + wave3-reaudit; git log b5e1dc9..HEAD` → three 5-lens waves over all of Foreman; every verified finding fixed test-first (d67c4fb, 16370b4, 8f0a3ad, 78bedb0, uninstall fix) or documented as a limitation (2026-09-26T14:36:56Z)
- (ac 7) `unittest discover; bench_hooks --runs 30; fm doctor; e2e/roundtrip.py; claude plugin eval (eval-1.1h.json)` → 269 tests OK; max hook p95 42.5 ms; doctor 22/0/0; roundtrip 17/17; eval 5/5 cases, score 1.0 ($1.01) (2026-09-26T14:36:56Z)
- (ac 8) `python3 -m unittest test_docs; live: fm ideas --pack pack-t0014.md with 4 lenses` → OK; live: 4 tool-less claude -p children (user value, reliability, security, simplicity) → 7–8 grounded ideas each in research/brainstorm-20260926-093428; brainstorm skill grounds and scores (2026-09-26T14:36:56Z)
- (ac 9) `python3 -m unittest test_hooks test_cli` → OK (FULL AUTO/STANDARD words, fm autonomy, drive ignores questions in full, pending approvals skipped and listed, notifications can't flip autonomy) (2026-09-26T14:36:57Z)
- (audit intent) `fm-reviewer intent lens, wave 3 (user's verbatim asks only) over all changes since b5e1dc9; earlier waves in d67c4fb; research wave3-intent` → approve with nits; docs-gate and hint-vs-gate findings fixed (16370b4); the asks (no commands for the user, full auto, audits, brainstorm) met — evals 5/5, live brainstorm [tree 87785b803e70] (2026-09-26T14:37:10Z)
- (audit adversary) `fm-reviewer adversary lens wave 3 + independent re-audit of the fixes; research wave3-adversary, wave3-reaudit` → state-redirect CRITICAL and tar bypass fixed (16370b4, 8f0a3ad, 78bedb0); fm ask binding, core never self-grantable, notifications can't approve; no open findings [tree 87785b803e70] (2026-09-26T14:37:10Z)
- (audit edge) `fm-reviewer edge lens wave 3 + re-audit edge pass; research wave3-edge` → plan-only false positives, code-fence questions, fallback way back, worktree_id cost, ask lock race fixed test-first; XDG/TMPDIR split documented [tree 87785b803e70] (2026-09-26T14:37:10Z)
- (audit operator) `fm-reviewer operator lens wave 3; roundtrip after the uninstall reorder; research wave3-operator` → doctor env check, SessionStart isolation, restore-state, approvals recovery doc (16370b4); uninstall leftover plugin maps fixed; roundtrip 17/17 [tree 87785b803e70] (2026-09-26T14:37:10Z)
- (audit maintainer) `fm-reviewer maintainer lens wave 3; research wave3-maintainer` → module rule, ASK_TTL, lock names, retry message fixed (16370b4); no dead code from the removed fm-ideas agent [tree 87785b803e70] (2026-09-26T14:37:10Z)
- (step 8) `fm task audit ×5 (wave 3 + re-audit); git fetch . foreman/build:main (fast-forward); git push origin main` → 5 lenses recorded after the last edit; main 7ec5185..924fe06 pushed to github.com:ChaseSunstrom/foreman (user-approved merge + push); no state/local/backups/secrets in the 62-file diff (2026-09-26T14:37:20Z)
- (audit intent) `re-recorded after step 8 evidence; worktree id unchanged since the wave 3 audits and re-audit (research wave3-*)` → no open findings; see the earlier intent record for the findings and fixes [tree 87785b803e70] (2026-09-26T14:37:34Z)
- (audit adversary) `re-recorded after step 8 evidence; worktree id unchanged since the wave 3 audits and re-audit (research wave3-*)` → no open findings; see the earlier adversary record for the findings and fixes [tree 87785b803e70] (2026-09-26T14:37:35Z)
- (audit edge) `re-recorded after step 8 evidence; worktree id unchanged since the wave 3 audits and re-audit (research wave3-*)` → no open findings; see the earlier edge record for the findings and fixes [tree 87785b803e70] (2026-09-26T14:37:35Z)
- (audit operator) `re-recorded after step 8 evidence; worktree id unchanged since the wave 3 audits and re-audit (research wave3-*)` → no open findings; see the earlier operator record for the findings and fixes [tree 87785b803e70] (2026-09-26T14:37:35Z)
- (audit maintainer) `re-recorded after step 8 evidence; worktree id unchanged since the wave 3 audits and re-audit (research wave3-*)` → no open findings; see the earlier maintainer record for the findings and fixes [tree 87785b803e70] (2026-09-26T14:37:35Z)
## Log
- 2026-09-26T12:21:43Z created
- 2026-09-26T12:27:09Z planned from capture
- 2026-09-26T12:27:22Z scope: T-0011 (user, mid-turn: 'add numerous audit steps with different prompts/context … so claude can do it autonomously') merged in
- 2026-09-26T12:37:31Z set approved=True
- 2026-09-26T12:37:31Z approved by user in chat: 'yes' (all defaults: plan, S/M/L audit depth 1/2/5, widen core, merge+push now and after audits). Same message added: brainstorm mode for vague requests with tool-less brainstorm subagents; full-auto mode that asks nothing and completes everything
- 2026-09-26T12:38:07Z focused
- 2026-09-26T12:41:26Z discovered (edge): on resume Claude Code runs SessionStart under a transient id, so the CLAUDE_ENV_FILE export (FOREMAN_SESSION_ID) never reaches this conversation; fm and the ledger now prefer CLAUDE_CODE_SESSION_ID (test_session_comes_from_claude_code_first; helpers strip it for isolation)
- 2026-09-26T12:41:56Z steer: user asked mid-turn for enforced procedure, doc drift/context rot, remote forever mode, formatted output -> captured T-0012..T-0015 to follow T-0009
- 2026-09-26T12:44:06Z steer: user asked mid-turn for approved plugin/marketplace installs + conflict-free plugin integration -> captured T-0016
- 2026-09-26T12:49:58Z user asked to update the README too: already step 7 (docs)
- 2026-09-26T12:52:21Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmguard.py', 'plugin/rules/foreman.md', 'plugin/skills/**', 'plugin/agents/**', 'plugin/tests/**', 'plugin/evals/**', 'MASTER.md', 'README.md', 'CHANGELOG.md', 'plugin/README.md', 'plugin/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json']
- 2026-09-26T12:52:21Z scope widened: plugin/agents/** (new fm-ideas brainstorm agent, step 10)
- 2026-09-26T12:57:35Z set scope=['plugin/lib/**', 'plugin/rules/foreman.md', 'plugin/skills/**', 'plugin/agents/**', 'plugin/tests/**', 'plugin/evals/**', 'MASTER.md', 'README.md', 'CHANGELOG.md', 'plugin/README.md', 'plugin/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json']
- 2026-09-26T12:57:35Z scope widened: plugin/lib/** (fmdoctor accepts tools: [] for the tool-less brainstorm agent)
- 2026-09-26T13:01:15Z user approved core in chat
- 2026-09-26T13:03:00Z finding (live, after reload): agents/fm-ideas.md with tools: [] was listed with ALL tools; docs: omitted/empty tools inherits every tool and a subagent can't have zero tools. Fix: brainstormers run as tool-less child sessions via fm ideas (claude -p --tools '' --strict-mcp-config --mcp-config '{"mcpServers":{}}'), verified live: 'NONE'. fm doctor must reject empty tool lists again.
- 2026-09-26T13:08:06Z discovered: guard can't see interpreter writes (python heredoc/-c, node -e) to core/state paths; fixing inline (blocks AC5); T-0017 dropped as merged
- 2026-09-26T13:15:06Z paused: focus moved to T-0012
- 2026-09-26T13:15:39Z intent audit (HIGH, verified by reading skills/intake/SKILL.md §4 and skills/next/SKILL.md step 5): approval gate doesn't branch on autonomy → fix on return
- 2026-09-26T13:17:24Z focused
- 2026-09-26T13:19:21Z paused: focus moved to T-0012
- 2026-09-26T13:23:53Z process: the state fallback, S self-audit and doctor state-dir fixes were made while T-0012 was focused (touched events attributed to T-0012); commit e11e5b5
- 2026-09-26T13:23:53Z focused
- 2026-09-26T13:31:01Z paused: focus moved to T-0012
- 2026-09-26T13:34:06Z final adversary re-audit (verified by reading): CRITICAL fm ask session id comes from agent-controlled env → bind to the hook's trusted session; HIGH Bash edits don't advance audit freshness → worktree content fingerprint per audit. Fix next.
- 2026-09-26T13:36:06Z focused
- 2026-09-26T13:42:25Z inline (blocks AC7): T-0008 eval fixes — scaffolds with the calculator app, fair graders, untagged-request classification note; state fallback already made fm work in the sandbox (1.1c: capture succeeded)
- 2026-09-26T13:44:41Z paused: focus moved to T-0012
- 2026-09-26T13:47:41Z focused
- 2026-09-26T13:47:41Z eval 1.1d: mean 0.6 (intake-block 1.0). one-liner revealed split-brain state: sandboxed fm used the fallback while hooks used the default → sticky shared fallback with migration; mid-task-capture: rewrite the case without a task id, scaffold the half-done fix
- 2026-09-26T13:50:28Z paused: focus moved to T-0013
- 2026-09-26T13:55:17Z focused
- 2026-09-26T13:55:18Z eval 1.1e: mid-task-capture 1.0; intake-block 0 because drive pushed execution after 'don't implement anything yet' and missed questions outside the last 400 chars; one-liner briefed the task but the final prose didn't restate it → drive hold on plan-only prompts, questions anywhere, trace-based classification grader
- 2026-09-26T13:57:58Z paused: focus moved to T-0013
- 2026-09-26T14:02:54Z focused
- 2026-09-26T14:03:46Z paused: focus moved to T-0012
- 2026-09-26T14:21:50Z audit wave 3 (intent/adversary/edge/operator/maintainer; research wave3-*) findings fixed test-first in 16370b4: fallback-state redirect closed, restore-state, docs checked at done, notifications not user words, plan-only regex, fences, worktree_id stat cache, guard module rule, named locks, ASK_TTL, doctor env check
- 2026-09-26T14:37:35Z done
## Follow-ups captured
## Docs impact
README.md: you never run a command, open-ended requests, audits, full auto, permissions (fm ask), uninstall order; MASTER.md: plain words, fm ask, CLI line, file map (fmideas), §9 pending approvals + uninstall, §10 limitations; CHANGELOG.md 1.1.0; plugin/rules/foreman.md: you run everything, consent, autonomy, audits; plugin/README.md; plugin/skills/intake/references/audit.md (lens prompts).
