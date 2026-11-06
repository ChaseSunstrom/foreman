---
id: T-1032
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmfixes.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/lib/fmrecall.py, plugin/lib/fmsync.py, plugin/tests/test_fixes.py, plugin/tests/test_shot.py, mods/foreman-ui/tools/shot.py, README.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-16T02:40:12Z
updated: 2026-10-16T03:11:18Z
base: 587c941eaaff2ca5f92dd73047a88004c0081bc8
base_tree: 039605847f3198995430ffdf94c8f043d0cfe13e
verified: strong
---
# Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e.
## Raw request
> Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e.g. the harness stalling at Claude Code's folder-trust prompt on every recording), Foreman records the obstacle's signature and the fix, then detects it next time and applies or injects the fix automatically; start with the trust prompt in shot.py
## Interpretation
Foreman should get better on its own from what goes wrong: when a session hits an obstacle (a command failing the same way, a refusal, an interactive prompt that stalls an automated run) and then gets past it, the obstacle's signature and what got past it are kept; the next time any session meets that signature, Foreman recognises it and hands Claude the known fix at that moment (or applies it where that is safe), without the user asking. The harness stalling at Claude Code's folder-trust prompt on every recording is the first case and must never happen again.
## Assumptions (confidence)
## Acceptance criteria
- [x] A Bash failure followed by a successful command of the same program is kept as a known fix, and the same failure later (another project too) gets that fix in its context — verify with `python3 plugin/tests/run.py test_fixes`
- [x] A command that failed before is flagged before it runs again, with what worked; worked/failed counts move and a losing fix stops being offered — verify with `python3 plugin/tests/run.py test_fixes`
- [x] fm fix add/list/rm work; a signature met 3 times captures one self task — verify with `python3 plugin/tests/run.py test_fixes`
- [x] shot.py start answers the folder-trust prompt for Foreman-made folders and never for others — verify with `python3 plugin/tests/run.py test_shot`
## Non-goals
## Approach (options → choice → why)
A complete version: (1) a global known-fixes store (state_dir/shared/fixes.json: signature, the failed command, what got past it, seen/used/worked counts, source); (2) automatic learning in the hooks: a Bash failure is remembered per session, and when a command of the same program succeeds within the next few calls the pair is kept, with no one asking; (3) recall: the next failure with that signature, in any project, gets the known fix in its context, ahead of the old pointer to a past task; and a command that failed before is flagged before it runs again, with what worked; (4) feedback: a fix that worked again counts up, one that didn't counts down and a losing fix stops being offered; (5) fm fix add/list/rm for obstacles hooks can't see (dialogs, stalls); (6) escalation: a signature met 3+ times captures one Foreman self task to make it impossible in code; (7) the harness answers Claude Code's folder-trust prompt itself, only for folders Foreman made (temp, scratchpad) or its own repo. Options: (a) only fm fix add, with a rule telling Claude to record: relies on the agent, which the user ruled out; (b) automatic pairing in the hooks plus recall and pre-emption; (c) a background claude -p reading transcripts to extract obstacle/fix pairs: catches more, costs tokens every session; (d) recurring obstacles become self tasks so code removes them. Choice: (b) as the core with (a) for what hooks can't see and (d) as the escalation; (c) captured for later. Safety: hooks never run a stored fix, they only say it; fixes are commands this machine's own sessions ran, redacted; signatures strip paths and numbers; trust is auto-answered only for Foreman-made folders (a cloned repo's hooks would run once trusted).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: learn, recall across projects, pre-run flag, feedback, fm fix CLI, escalation; shot trust answer
2. [x] fmfixes.py: store, learn, match, pre-note, feedback, escalation
3. [x] Hooks: post_tool_use (success learns, failure remembers), post_tool_use_failure (known fix first), pre_tool_use Bash (flag a known-bad command)
4. [x] fm fix add/list/rm, fm help tier, MASTER/rules line
5. [x] shot.py: answer the trust prompt for Foreman-made folders
6. [x] README, CHANGELOG, live check
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_fixes test_shot` → ✗ exit 1 · Ran 14 tests in 3.2s (4 classes, 16 at a time; slowest: KnownFixes 3s, Harness 0s, Trust 0s) / FAILED (2 classes) [ran] [tree e0a1b9dc7dfc] (2026-10-16T02:48:55Z)
- (step 1) `python3 plugin/tests/run.py test_fixes test_shot` → exit 0 · Ran 14 tests in 6.6s (4 classes, 16 at a time; slowest: KnownFixes 6s, Harness 0s, Trust 0s) / OK [ran] [tree f68d97ae4982] (2026-10-16T02:51:58Z)
- (step 2) `python3 plugin/tests/run.py test_fixes test_shot` → exit 0 · Ran 14 tests in 6.8s (4 classes, 16 at a time; slowest: KnownFixes 7s, Harness 0s, OneOff 0s) / OK [ran] [tree f68d97ae4982] (2026-10-16T02:52:05Z)
- (step 3) `python3 plugin/tests/run.py test_fixes test_shot` → exit 0 · Ran 14 tests in 7.2s (4 classes, 16 at a time; slowest: KnownFixes 7s, Harness 0s, OneOff 0s) / OK [ran] [tree f68d97ae4982] (2026-10-16T02:52:13Z)
- (step 4) `python3 plugin/tests/run.py test_fixes test_shot` → exit 0 · Ran 14 tests in 4.6s (4 classes, 16 at a time; slowest: KnownFixes 4s, Harness 0s, Trust 0s) / OK [ran] [tree f68d97ae4982] (2026-10-16T02:52:19Z)
- (step 5) `python3 plugin/tests/run.py test_fixes test_shot` → exit 0 · Ran 14 tests in 3.4s (4 classes, 16 at a time; slowest: KnownFixes 3s, Harness 0s, OneOff 0s) / OK [ran] [tree f68d97ae4982] (2026-10-16T02:52:23Z)
- (step 6) `python3 plugin/tests/run.py test_fixes test_shot test_sync test_recall test_docs test_doctor` → exit 0 · Ran 120 tests in 24.5s (38 classes, 16 at a time; slowest: Command 24s, ViewsRepair 17s, Recall 15s) / OK [ran] [tree 2a91ca0a4300] (2026-10-16T02:56:13Z)
- (step 6) `python3 plugin/tests/run.py test_fixes test_shot test_sync test_recall test_docs test_doctor` → exit 0 · Ran 123 tests in 24.7s (38 classes, 16 at a time; slowest: Command 25s, ViewsRepair 17s, Recall 15s) / OK [ran] [tree eeaeab81804f] (2026-10-16T03:01:30Z)
- (ac 1) `python3 plugin/tests/run.py test_fixes` → exit 0 · Ran 14 tests in 4.6s (1 classes, 16 at a time; slowest: KnownFixes 4s) / OK [ran] [tree eeaeab81804f] (2026-10-16T03:08:21Z)
- (ac 2) `python3 plugin/tests/run.py test_fixes` → exit 0 · Ran 14 tests in 4.6s (1 classes, 16 at a time; slowest: KnownFixes 4s) / OK [ran] [tree eeaeab81804f] (2026-10-16T03:08:21Z)
- (ac 3) `python3 plugin/tests/run.py test_fixes` → exit 0 · Ran 14 tests in 4.6s (1 classes, 16 at a time; slowest: KnownFixes 4s) / OK [ran] [tree eeaeab81804f] (2026-10-16T03:08:21Z)
- (ac 4) `python3 plugin/tests/run.py test_shot` → exit 0 · Ran 4 tests in 0.2s (3 classes, 16 at a time; slowest: Harness 0s, Trust 0s, OneOff 0s) / OK [ran] [tree eeaeab81804f] (2026-10-16T03:08:21Z)
- (audit intent) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first (provenance/trust for repo fixes, edit-between, sensitive projects, harness trust gate, bounded state, consistent redaction); a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness` → learns with no one asking, recalls across projects, flags before rerun, travels through fm sync, escalates; seen live [tree eeaeab81804f] (2026-10-16T03:08:21Z)
- (audit adversary) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first (provenance/trust for repo fixes, edit-between, sensitive projects, harness trust gate, bounded state, consistent redaction); a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness` → a repo's fixes are hints only (exact match, never pre-run, adopt with fm fix trust); secrets redacted; harness never trusts a folder with Claude Code config [tree eeaeab81804f] (2026-10-16T03:08:21Z)
- (audit edge) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first (provenance/trust for repo fixes, edit-between, sensitive projects, harness trust gate, bounded state, consistent redaction); a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness` → retries, look-arounds and code edits teach nothing; losing fixes stop; sensitive projects stay local; state pruned [tree eeaeab81804f] (2026-10-16T03:08:21Z)
- (audit operator) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first (provenance/trust for repo fixes, edit-between, sensitive projects, harness trust gate, bounded state, consistent redaction); a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness` → fm doctor OK; fm fix list|add|rm|trust; stores under state/shared and the project's fixes.md; hooks never run a fix; full gates green [tree eeaeab81804f] (2026-10-16T03:08:21Z)
- (audit maintainer) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first (provenance/trust for repo fixes, edit-between, sensitive projects, harness trust gate, bounded state, consistent redaction); a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness` → one module (fmfixes) with docstring, MASTER.md row, fm help tier; tests cover each behaviour incl. a mutation check [tree eeaeab81804f] (2026-10-16T03:08:21Z)
- (audit intent) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first (provenance/trust for repo fixes, edit-between, sensitive projects, harness trust gate, bounded state, consistent redaction); a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness` → learns with no one asking, recalls across projects, flags before rerun, travels through fm sync, escalates; seen live [tree aa1461d237cf] (2026-10-16T03:10:56Z)
- (audit adversary) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first (provenance/trust for repo fixes, edit-between, sensitive projects, harness trust gate, bounded state, consistent redaction); a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness` → a repo's fixes are hints only (exact match, never pre-run, adopt with fm fix trust); secrets redacted (tested on a stored record); harness never trusts a folder with Claude Code config [tree aa1461d237cf] (2026-10-16T03:10:56Z)
- (audit edge) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first (provenance/trust for repo fixes, edit-between, sensitive projects, harness trust gate, bounded state, consistent redaction); a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness` → retries, look-arounds and code edits teach nothing; losing fixes stop; sensitive projects stay local; state pruned [tree aa1461d237cf] (2026-10-16T03:10:56Z)
- (audit operator) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first (provenance/trust for repo fixes, edit-between, sensitive projects, harness trust gate, bounded state, consistent redaction); a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness` → fm doctor OK; fm fix list|add|rm|trust; stores under state/shared and the project's fixes.md; hooks never run a fix; full gates green [tree aa1461d237cf] (2026-10-16T03:10:56Z)
- (audit maintainer) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first (provenance/trust for repo fixes, edit-between, sensitive projects, harness trust gate, bounded state, consistent redaction); a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness` → one module (fmfixes) with docstring, MASTER.md row, fm help tier; tests cover each behaviour incl. a mutation check [tree aa1461d237cf] (2026-10-16T03:10:56Z)
- (audit intent) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first; a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness; the last change (a runtime-built fake key in one test) re-run green` → learns with no one asking, recalls across projects, flags before rerun, travels through fm sync, escalates; seen live [tree aa1461d237cf] (2026-10-16T03:11:17Z)
- (audit adversary) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first; a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness; the last change (a runtime-built fake key in one test) re-run green` → a repo's fixes are hints only (exact match, never pre-run, adopt with fm fix trust); secrets redacted (tested on a stored record); harness never trusts a folder with Claude Code config [tree aa1461d237cf] (2026-10-16T03:11:17Z)
- (audit edge) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first; a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness; the last change (a runtime-built fake key in one test) re-run green` → retries, look-arounds and code edits teach nothing; losing fixes stop; sensitive projects stay local; state pruned [tree aa1461d237cf] (2026-10-16T03:11:17Z)
- (audit operator) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first; a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness; the last change (a runtime-built fake key in one test) re-run green` → fm doctor OK; fm fix list|add|rm|trust; stores under state/shared and the project's fixes.md; hooks never run a fix; full gates green [tree aa1461d237cf] (2026-10-16T03:11:17Z)
- (audit maintainer) `one fm-reviewer pass plus the automated security review; all 4 MEDIUM and the LOW findings fixed test-first; a shadowed TestCase.fail in my own tests found and fixed; mutation check on the edit guard; live in this session and in the harness; the last change (a runtime-built fake key in one test) re-run green` → one module (fmfixes) with docstring, MASTER.md row, fm help tier; tests cover each behaviour incl. a mutation check [tree aa1461d237cf] (2026-10-16T03:11:17Z)
## Log
- 2026-10-16T02:40:12Z created
- 2026-10-16T02:42:14Z set scope=['plugin/lib/fmfixes.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmrecall.py', 'plugin/tests/test_fixes.py', 'plugin/tests/test_shot.py', 'mods/foreman-ui/tools/shot.py', 'plugin/rules/foreman.md', 'README.md', 'CHANGELOG.md', 'MASTER.md', 'plugin/lib/fmdoctor.py']
- 2026-10-16T02:42:43Z steer: not just Foreman itself, any project; fixes must travel with git so other sessions/clones/teammates use them (project fixes in the repo, machine-wide ones in Foreman state)
- 2026-10-16T02:43:32Z set scope=['plugin/lib/fmfixes.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmsync.py', 'plugin/tests/test_fixes.py', 'plugin/tests/test_shot.py', 'plugin/tests/test_sync.py', 'mods/foreman-ui/tools/shot.py', 'plugin/rules/foreman.md', 'README.md', 'CHANGELOG.md', 'MASTER.md', 'plugin/lib/fmdoctor.py']
- 2026-10-16T02:47:02Z focused
- 2026-10-16T02:47:08Z set approved=True
- 2026-10-16T02:47:08Z focused
- 2026-10-16T02:56:13Z set scope=['plugin/lib/fmfixes.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmsync.py', 'plugin/tests/test_fixes.py', 'plugin/tests/test_shot.py', 'mods/foreman-ui/tools/shot.py', 'README.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T03:11:11Z scope: plugin/rules/foreman.md got a Known-fixes line, then lost it (the rules file is capped at 6000 chars); plugin/evals/*/prompt.md were regenerated by sync_evals.py for that line and back again: no net change in either
- 2026-10-16T03:11:18Z done
- 2026-10-16T03:11:18Z committed 7afe459 (11 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- decision 2026-10-15: Recommendation: close the gaps where a small model has to guess a command (done: T-0969, T-0985, T-0986, T-0987); no separate small-model mode or MC…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_doctor.py, plugin/tests/test_hooks.py, plugin/tests/test_recall.py, plugin/tests/test_shot.py, plugin/tests/test_sync.py
## Build vs reuse
Reuses fmrecall.failure_signature (the same normalised signature failures.jsonl keys on), note_failure's injection path in post_tool_use_failure, the PreToolUse note list (as _tripwire_note), fm sync's mirror with decisions.md's line-union merge for the git transport, c.redact/c.plain for what is stored and shown, c.lock and write_atomic, and fm capture for the escalation. New: fmfixes.py (the store, the pairing heuristic, recall, the pre-run note) and fm fix; nothing in the repo pairs a failure with what got past it.
## Lessons
- Never name a unittest helper fail(): assertIn/assertNotIn call self.fail to raise, so a shadowing helper turns their failures into silent passes.
## Plan gaps
- failed first: step 1 Failing tests: learn, recall across projects, pre-run flag, feedback, fm fix CLI, escalation; shot …
## Files touched
- plugin/tests/test_fixes.py
- plugin/tests/test_shot.py
- plugin/lib/fmfixes.py
- plugin/lib/fmhooks.py
- plugin/lib/fmsync.py
- plugin/lib/fmcli.py
- mods/foreman-ui/tools/shot.py
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- MASTER.md
- plugin/lib/fmrecall.py
- CHANGELOG.md
- README.md
