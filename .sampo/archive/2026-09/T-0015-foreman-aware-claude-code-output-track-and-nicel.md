---
id: T-0015
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/output-styles/**, plugin/.claude-plugin/plugin.json, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmwatch.py, plugin/lib/fmsetup.py, plugin/hooks/statusline, plugin/tests/**, plugin/rules/foreman.md, MASTER.md, README.md]
depends_on: [T-0012]
source: user
created: 2026-09-26T12:41:56Z
updated: 2026-09-26T15:45:15Z
---
# Foreman-aware conversation view: output style, richer badge and statusline, pending-approval display, live step tracking
## Raw request
> Foreman-aware Claude Code output: track and nicely format the steps Foreman is taking (stage, step n/m, evidence, audits) in the conversation view so it isn't just a wall of code changes; make it really nice and complete
## Interpretation
The conversation should read as Foreman's progress, not a wall of diffs: where we are (task, stage, step n/m), what was just verified (evidence), what was captured, what's next, and anything waiting on the user, formatted consistently and compactly. Claude Code can't hide tool diffs from hooks (research), so the view is improved around them: a Foreman output style shapes every reply, the per-reply badge and the statusline carry live progress, and pending approvals are shown explicitly so a 'yes' is never ambiguous.
## Assumptions (confidence)
## Acceptance criteria
- [x] Plugin ships an output style (valid per claude plugin validate --strict) with the Foreman reply format; install-user selects it reversibly unless the user has one — verify with `python3 -m unittest test_docs test_setup; claude plugin validate --strict`
- [x] Badge shows task, stage and step n/m; statusline shows progress bar, audits done/required, queue/inbox, autonomy and any pending approval with exactly what a yes grants — verify with `python3 -m unittest test_visibility`
- [x] fm watch shows the stage timeline and recent evidence/captures/approvals — verify with `python3 -m unittest test_visibility`
- [x] Hook p95 <= 150 ms; MessageDisplay <= 100 ms; statusline renders < 100 ms — verify with `python3 plugin/tests/bench_hooks.py --runs 30`
- [x] fm ask raises Claude Code's native permission prompt stating what it grants; only an approved dialog for that exact call grants; chat messages don't cancel it — verify with `python3 -m unittest test_hooks.PromptApprovals; live: after /reload-plugins, fm ask shows a prompt and approving it grants (ledger via=prompt)`
## Non-goals
## Approach (options → choice → why)
(1) Plugin output style 'foreman' (keep-coding-instructions: true) + MessageDisplay badge with stage/step/evidence counts + two-line statusline (progress bar, audits, pending approval) + fm watch stages timeline [chosen: every supported surface, zero or near-zero tokens except the style's short format rules]. (2) Put formatting rules in rules/foreman.md only [rejected: always-on lines, weaker]. (3) Patch Claude Code rendering [rejected: unsupported].
Reply format (output style): header line '▌T-0009 · FEATURE L · execute · step 3/10'; per step '▸ Step n/m — title' then '✓ <cmd> → <result>' evidence lines; code changes summarized as 'Changed: file (why)' instead of pasted code; '⚑ Captured T-00xx' for new asks; closing 'Next: …' and '⚠ Needs you: …' only when something does. fm install-user sets outputStyle to the Foreman style (recorded, reverted by uninstall; skipped if the user already chose one).
Statusline line 2: '▸ T-0009 FEATURE L ███████░░░ 7/10 · audits 2/5 · q4 in3 · full auto · ⚠ reply yes = core for T-0009'.
## Risks and rollback
Risk: output style overrides a style the user picked → only set when none is set, recorded, reverted. Risk: statusline gets too wide → truncate to terminal width. Rollback: git revert; uninstall-user restores outputStyle.
## Execution prompt
## Steps
1. [x] Stage/progress model shared by badge, statusline, watch (TDD; builds on T-0012 stages)
2. [x] Output style + manifest + install-user selection (TDD)
3. [x] Badge, statusline line 2, pending approval display (TDD)
4. [x] fm watch timeline; bench; live look; docs; audits
5. [x] Approvals as native Claude Code prompts: PreToolUse ask on fm ask, PermissionRequest marks the dialog shown, PostToolUse grants; rules: questions via AskUserQuestion (TDD)
## Resume here
T-0015: all 5 steps done (068ca37). Audits running: adversary, edge, intent over scratchpad/t0015.diff; operator + maintainer next. Live check of prompt approvals pending the user's /reload-plugins (registers PermissionRequest, loads output style): then fm ask T-0020 core and fm ask T-0019 core as lone commands → native prompts → verify grants via prompt (ledger via=prompt).
<!-- auto -->
- 2026-09-26T15:26:16Z steps 5/5 done
- git: foreman/build; 0 uncommitted
## Verification evidence
- (step 1) `python3 -m unittest test_visibility.Progress; full suite` → RED (2 errors, 1 failure) then OK: state_dict active carries stage + audits {done, required} (last_change-aware), asks list; 294 tests OK (2026-09-26T15:12:42Z)
- (step 3) `python3 -m unittest test_visibility test_hooks.MessageDisplay; bench_hooks --runs 30` → OK: badge '[T-0001 FIX · executing 1/2 · hh:mm]'; statusline line 2 '▸ T-0001 FIX S █████░░░░░ 1/2 · executing · audits 0/1 · q0 in0 · standard · ⚠ reply yes = publish for T-0001' (≤ COLUMNS), none when idle; fm ask refreshes it; MessageDisplay p95 37.4 ms (2026-09-26T15:12:43Z)
- (step 2) `python3 -m unittest test_setup test_docs.OutputStyle; claude plugin validate --strict plugin; live probe (research output-styles-probe)` → RED (2 errors) then OK: plugin/output-styles/foreman.md (name Foreman, keep-coding-instructions: true, < 260 words); install-user sets outputStyle foreman:Foreman only when none is set, recorded; uninstall removes only its own; validate passed; probe showed plugin styles are selected as <plugin>:<name> (2026-09-26T15:14:44Z)
- (step 5) `python3 -m unittest test_hooks.PromptApprovals; full suite; claude plugin validate --strict; fm doctor` → RED (2 errors, 2 failures) then OK: ask decision with the grant text; chained ask denied; grant only after PermissionRequest + PostToolUse of the same tool_use_id; refused dialog cleared by the next message; fm ask after approval leaves nothing pending; 302 tests OK; validate passed; doctor 23/0/0. Live prompt check pending /reload-plugins (new PermissionRequest hook) (2026-09-26T15:23:24Z)
- (step 4) `python3 -m unittest test_visibility.Watch; fm watch --once (live); statusline timing (20 runs); bench_hooks; fm install-user; docs` → OK: stage timeline, Recent feed, Waiting on you; live view renders them; statusline p50 90 / p95 93 ms (was 101/110: children now start before the fmcore import; claude-hud alone 60 ms); hooks p95 ≤ 42 ms, MessageDisplay 37 ms; outputStyle foreman:Foreman set; README/MASTER/CHANGELOG/rules updated (2026-09-26T15:25:41Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_docs test_setup; claude plugin validate --strict plugin` → OK; validate passed; output-styles/foreman.md (keep-coding-instructions: true); install-user sets outputStyle foreman:Foreman only when unset, recorded, removed by uninstall (2026-09-26T15:26:36Z)
- (ac 2) `python3 -m unittest test_visibility (Progress, Statusline)` → OK: badge '<id> <type> · <stage> n/m'; line 2 progress bar, audits done/required, q/in, autonomy, '⚠ reply yes = <cats> for <id>' (2026-09-26T15:26:36Z)
- (ac 3) `python3 -m unittest test_visibility.Watch; fm watch --once` → OK: stage timeline with audits, Recent feed (evidence/audits/captures/decisions/approvals/done), Waiting on you (2026-09-26T15:26:36Z)
- (ac 4) `python3 plugin/tests/bench_hooks.py --runs 30; statusline timing 20 runs` → hooks p95 ≤ 42 ms; MessageDisplay p95 37 ms; statusline p50 90 / p95 93 ms (incl. claude-hud 60 ms) (2026-09-26T15:26:36Z)
- (ac 5) `live after /reload-plugins: fm ask T-0020 core; fm ask T-0019 core (lone commands); ledger + briefs + prompts.json + meta; python3 -m unittest test_hooks.PromptApprovals` → user saw and approved native prompts; approval_granted via=prompt for both; allow [core] on T-0019/T-0020; no pending left; earlier probe showed PreToolUse 'ask' prompts even in bypass mode; unit tests OK (2026-09-26T15:28:55Z)
- (audit intent) `fm-reviewer intent lens (user's verbatim asks A–C) over t0015.diff; research t0015-intent` → grants were the only prompts → Stop hook sends text questions back once to become AskUserQuestion prompts; headless and global-style limits documented (1b175e1) [tree 6a1046c56fd5] (2026-09-26T15:45:14Z)
- (audit adversary) `fm-reviewer adversary lens over t0015.diff, re-audit of 1b175e1, final check of f602cb0; research t0015-edge-adversary, t0015-reaudit, t0015-final-check; live: dialog shown in bypass mode, grants via=prompt` → dialog text undisguisable (id format, Cc/Cf/Zl/Zp stripped, redacted why), fm ask refused under fm run / with -p / unknown options, -h output fixed (1b175e1, f602cb0, this commit); grant only after a dialog for that call [tree 6a1046c56fd5] (2026-09-26T15:45:15Z)
- (audit edge) `fm-reviewer edge lens over t0015.diff; research t0015-edge-adversary` → headless ask refused, statusline children collected on failure, COLUMNS=0 safe, bound flag logged, CLI freshness check (1b175e1) [tree 6a1046c56fd5] (2026-09-26T15:45:15Z)
- (audit operator) `fm-reviewer operator lens over t0015-all.diff; research t0015-operator` → reload hint when a dialog was approved before /reload-plugins, unmatched grants logged, nudge quiet under fm run, why redacted, doctor checks hook registration (f602cb0) [tree 6a1046c56fd5] (2026-09-26T15:45:15Z)
- (audit maintainer) `fm-reviewer maintainer lens over t0015-all.diff; research t0015-maintainer` → one parser (fm's argparse), one APPROVAL_TTL, one _grant, shared STAGES and fit (f602cb0); glyph-pinning tests kept as characterization tests [tree 6a1046c56fd5] (2026-09-26T15:45:15Z)
## Log
- 2026-09-26T12:41:56Z created
- 2026-09-26T12:52:49Z design note: show pending fm ask approvals in the statusline (what a yes would grant, for which task) so the user sees exactly what they approve
- 2026-09-26T12:58:34Z planned from capture
- 2026-09-26T12:58:35Z set depends_on=['T-0012']
- 2026-09-26T13:01:15Z user approved core in chat
- 2026-09-26T13:01:42Z set approved=True
- 2026-09-26T13:01:42Z approved by user in chat: 'yes, to all of your things … you have FULL permission for the rest of this session to go full auto'
- 2026-09-26T15:07:58Z focused
- 2026-09-26T15:17:09Z steer (user, 2026-09-26): 'can you have it so requests/blockers that need the user show up as prompts in CC, instead of in the messages? so you can keep working and not have to worry about breaking pending things' → scope widened: fm ask raises Claude Code's native permission prompt (PreToolUse ask + PermissionRequest + PostToolUse grant); questions/decisions use AskUserQuestion; chat yes stays as fallback
- 2026-09-26T15:45:15Z done
## Follow-ups captured
## Docs impact
README.md: Permissions (approvals are Claude Code prompts), Headless unchanged; MASTER.md: plain words/approvals paragraph, file map (plugin/output-styles/foreman.md), §9 approvals flow, §10 limitations (dialog trust, chat fallback); CHANGELOG.md: Unreleased (conversation view, prompt approvals); plugin/rules/foreman.md: ask through prompts (fm ask, AskUserQuestion); plugin/README.md: consent line; plugin/output-styles/foreman.md (new).
