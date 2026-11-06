---
id: T-0012
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/tests/**, plugin/rules/foreman.md, plugin/skills/**, MASTER.md]
depends_on: []
source: user
created: 2026-09-26T12:41:56Z
updated: 2026-09-26T14:33:17Z
---
# Harness-enforced procedure: stage machine, next-action injection, no edits without a planned task
## Raw request
> Enforce the procedure from the harness, not from Claude's own tool choices (context rot degrades that): hooks track each task's stage (capture, expand, ground, plan, execute, verify, audit, reflect, record), inject the next required action every turn and gate transitions
## Interpretation
The procedure must not depend on Claude remembering which skill or step comes next (long contexts degrade that). Foreman derives each task's stage from its brief, computes the one next required action, injects it every turn, and refuses transitions whose preconditions aren't met.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm next prints the single next required action for the active/next task, derived from the brief (stage, what's missing, which reference to use) — verify with `python3 -m unittest test_core test_cli`
- [x] fm focus refuses briefs that aren't fully planned for their tier, listing what's missing — verify with `python3 -m unittest test_cli`
- [x] Write/Edit in a registered project with no active task is denied with a one-command fix; scratch and out-of-project paths are exempt — verify with `python3 -m unittest test_hooks test_guard`
- [x] UserPromptSubmit and the Stop drive reason include 'Next: …' within their budgets — verify with `python3 -m unittest test_hooks`
- [x] Hook p95 stays <= 150 ms — verify with `python3 plugin/tests/bench_hooks.py --runs 30`
## Non-goals
## Approach (options → choice → why)
(1) Derived stage + fm refusals + hook injection [chosen: deterministic, no new state to drift, reuses done_blockers]. (2) Stored stage field advanced by commands [rejected: can drift from the brief's real content]. (3) Rules only [rejected: that's today's gap].
Stages: captured → planned (Interpretation, >=1 criterion with --verify, >=1 step; M/L also Approach; L in standard autonomy also approved) → executing (focused) → verifying (all steps done) → auditing (tier audits missing) → done.
Enforcement: fm focus refuses a brief that isn't planned-complete (exit 2, lists what's missing; S needs 1 criterion + 1 step); PreToolUse denies Write/Edit in a registered project while no task is active (one command away: fm task new … --tier S), scratch/tmp/out-of-project paths exempt; fm next prints the next required action; UserPromptSubmit and the Stop drive reason carry 'Next: …'; the stage's procedure reference is named by fm (FIX → debugging.md + regression-test.md, audits → audit.md) so Claude doesn't choose it.
## Risks and rollback
Risk: gate blocks legitimate quick edits → the fix is one command (fm task new … --tier S) and the message says so; exempt paths. Risk: in-flight briefs lacking criteria can't be focused → fm lists exactly what to add. Rollback: git revert.
## Execution prompt
## Steps
1. [x] Stage derivation + fm next (TDD)
2. [x] fm focus plan gate (TDD)
3. [x] No-task edit gate in PreToolUse (TDD; core file fmhooks/fmguard)
4. [x] Next-action injection in UserPromptSubmit + Stop (TDD)
5. [x] Rules/skills: point at fm next; audits + bench + docs
## Resume here
T-0012 step 5: rules edit pending (after eval work); then audits
<!-- auto -->
- 2026-09-26T14:05:54Z step 5/5: Rules/skills: point at fm next; audits + bench + docs
- git: foreman/build; 0 uncommitted
## Verification evidence
- (step 1) `python3 -m unittest test_core.Stages test_cli.NextAction; full suite; fm next (live)` → RED first (errors, then failure), then OK; suite OK; live: 'Next: T-0012 step 1/5 … (procedure: execute.md (TDD))' (2026-09-26T13:17:24Z)
- (step 2) `python3 -m unittest test_cli (test_focus_requires_a_plan, test_unapproved_L_focus_depends_on_autonomy); full suite` → RED 2 failures, then OK; suite OK (2026-09-26T13:23:53Z)
- (step 3) `python3 -m unittest test_hooks.NoTaskGate test_cli.OneCommandTask; full suite; bench` → RED 3 failures then OK (found: /tmp-wide scratch exemption hid the gate); suite OK; PreToolUse p95 ~35 ms (2026-09-26T13:32:49Z)
- (step 4) `python3 -m unittest test_hooks (next action in UserPromptSubmit/SessionStart/Stop); suite; bench` → RED 3 then OK; suite OK; p95 SessionStart 39 ms, UserPromptSubmit 37 ms, Stop 38 ms (2026-09-26T13:36:06Z)
- (step 5) `grep -c 'fm next' rules/foreman.md skills/next,resume MASTER.md; unittest discover (265); bench_hooks --runs 30; fm doctor; audit wave 3 fixed in 16370b4` → each file names fm next (rules 60 lines); 265 tests OK; p95 SessionStart 39.7, UserPromptSubmit 40.4, PreToolUse 39.5, Stop 42.6 ms (budget 150); doctor 22 pass 0 warn 0 fail (2026-09-26T14:21:58Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_core test_cli; fm next (live)` → OK; live: 'Next: T-0012: fm task ac T-0012 check 1 …' derived from the brief (2026-09-26T14:23:58Z)
- (ac 2) `python3 -m unittest test_cli` → OK (test_focus_requires_a_plan, test_unapproved_L_focus_depends_on_autonomy) (2026-09-26T14:23:58Z)
- (ac 3) `python3 -m unittest test_hooks test_guard` → OK (NoTaskGate: deny with --focus fix; scratch, /tmp, ~/.claude/projects, outside paths allowed) (2026-09-26T14:23:58Z)
- (ac 4) `python3 -m unittest test_hooks` → OK (Next: in UserPromptSubmit, SessionStart and Stop drive reason) (2026-09-26T14:23:58Z)
- (ac 5) `python3 plugin/tests/bench_hooks.py --runs 30` → p95: SessionStart 39.7, UserPromptSubmit 40.4, PreToolUse 39.5, Stop 42.6 ms (<= 150) (2026-09-26T14:23:58Z)
- (audit intent) `fm-reviewer intent lens over wave3.diff + wave3-stages-early.diff (user's verbatim asks A–C only); research wave3-intent` → approve with nits: docs gate free-text → named docs must exist and be drift-free at done, other drift reported (16370b4); hint-vs-gate wording fixed in README/CHANGELOG/MASTER [tree 99736f772dcc] (2026-09-26T14:33:16Z)
- (audit adversary) `fm-reviewer adversary lens over wave3 diffs, then re-audit (adversary+edge) of 16370b4; research wave3-adversary, wave3-reaudit` → CRITICAL fallback-marker state redirect → guard protects all fallback locations, private-dir markers only (16370b4); re-audit CRITICAL tar -x -C bypass → archives/clones/-t/wget -P checked by destination (8f0a3ad, 78bedb0); no open findings [tree 99736f772dcc] (2026-09-26T14:33:16Z)
- (audit edge) `fm-reviewer edge lens over wave3 diffs + re-audit edge pass; research wave3-edge` → plan-only false positives, ? in code fences, sticky fallback with no way back, worktree_id cost, ask lock race → all fixed test-first (16370b4); XDG/TMPDIR disagreement documented as a limitation; eval setup symlinks verified by eval 1.1g [tree 99736f772dcc] (2026-09-26T14:33:16Z)
- (audit operator) `fm-reviewer operator lens over wave3 diffs (upgrade path, env var, fallback, approvals, messages, hook failures); research wave3-operator; plus roundtrip after the uninstall reorder` → doctor env check, SessionStart next_for isolation, fallback WARN with fm doctor --restore-state, pending-approval recovery documented (16370b4); uninstall leftover maps fixed (roundtrip 17/17) [tree 99736f772dcc] (2026-09-26T14:33:16Z)
- (audit maintainer) `fm-reviewer maintainer lens over wave3 diffs; research wave3-maintainer` → one Foreman-module rule in the guard, shared ASK_TTL, named lock waits, fm ask retry message (16370b4); check_self_docs size left as is (four short checks, one caller) [tree 99736f772dcc] (2026-09-26T14:33:17Z)
## Log
- 2026-09-26T12:41:56Z created
- 2026-09-26T12:50:46Z planned from capture
- 2026-09-26T13:01:15Z user approved core in chat
- 2026-09-26T13:01:41Z set approved=True
- 2026-09-26T13:01:41Z approved by user in chat: 'yes, to all of your things … you have FULL permission for the rest of this session to go full auto'
- 2026-09-26T13:14:47Z design note (observed live): writes to Claude's auto memory (~/.claude/projects/*/memory/) triggered the scope note; the scope note and the new no-task edit gate must exempt auto memory, the scratchpad and tmp
- 2026-09-26T13:15:06Z focused
- 2026-09-26T13:17:24Z paused: focus moved to T-0009
- 2026-09-26T13:19:21Z focused
- 2026-09-26T13:23:53Z process: state fallback + S self-audit fixes (T-0009 findings) were edited while T-0012 was focused; committed separately and logged on T-0009
- 2026-09-26T13:23:53Z paused: focus moved to T-0009
- 2026-09-26T13:31:01Z focused
- 2026-09-26T13:36:06Z paused: focus moved to T-0009
- 2026-09-26T13:44:41Z focused
- 2026-09-26T13:47:41Z paused: focus moved to T-0009
- 2026-09-26T14:03:46Z focused
- 2026-09-26T14:21:50Z audit wave 3 (intent/adversary/edge/operator/maintainer; research wave3-*) findings fixed test-first in 16370b4: fallback-state redirect closed, restore-state, docs checked at done, notifications not user words, plan-only regex, fences, worktree_id stat cache, guard module rule, named locks, ASK_TTL, doctor env check
- 2026-09-26T14:33:17Z done
## Follow-ups captured
## Docs impact
MASTER.md: stage machine paragraph, fm next in CLI line, §9 state location + pending approvals, §10 hints vs gates; plugin/rules/foreman.md: fm next, the gates, Docs impact; README.md: harness-enforced procedure; CHANGELOG.md 1.1.0 entries (hint vs gate wording).
