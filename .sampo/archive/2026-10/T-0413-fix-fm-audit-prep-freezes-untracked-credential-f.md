---
id: T-0413
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T04:59:20Z
updated: 2026-10-09T13:17:57Z
base: 94433f9ed3e1e657c01e218eba62350ab398a089
base_tree: 3e29315cc34b41444156374c025b80cbd2277adb
verified: strong
---
# Audit diffs leave out secrets
## Raw request
> FIX: fm audit prep freezes untracked credential files (JARVIS: /opt/jarvis/jarvis-core/.env.bak-20261009-ai-container) into state/audits/ID.diff with their secrets; JARVIS then tried rm -f on the diff and was refused as state-direct with no fm way to clear it. Redact secret values (or omit credential-file bodies) in the frozen diff, and the state-direct hint for audits/*.diff should say fm audit prep ID rewrites it
## Interpretation
fm audit prep freezes git diff base → working tree (untracked files included) into state/audits/ID.diff. An untracked, unignored credential file (JARVIS: .env.bak-20261009-ai-container) lands there with its secrets, and nothing in fm removes it; rm is refused as state-direct. The frozen diff should never hold secret values, and the refusal for an audits file should name the fm command that rewrites it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a frozen audit diff holds no credential-file body or key=value secret, and still names the file; the state-direct refusal for an audit diff names fm audit prep — verify with `python3 plugin/tests/run.py -k test_audit_diff_leaves_out_secrets -k test_audit_diff_refusal_names_prep`
## Non-goals
## Approach (options → choice → why)
(A, chosen) when writing the frozen diff: replace the body of every credential-named file's diff (the guard's _is_credential names: .env*, *.pem, *secret*, id_rsa …) with one line saying its contents were left out, and run c.redact over the rest (key=value secrets in ordinary files). The reviewer still sees the file was added or changed. The state-direct refusal for state/…/audits/ID.diff adds: fm audit prep ID rewrites it. (B, rejected) drop credential files from the diff entirely: the reviewer would not know one was added. (C, rejected) hint only: secrets stay in state until someone reruns prep.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: frozen diff of an untracked .env.bak and a key=value secret; refusal text
2. [x] redact the frozen diff in cmd_audit; hint in the state-direct message
3. [x] gate, changelog, ship
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_audit_diff_leaves_out_secrets -k test_audit_diff_refusal_names_prep` → ✗ exit 1 · Ran 2 tests in 0.3s (2 classes, 16 at a time; slowest: AuditPrep 0s, StateDirect 0s) / FAILED (2 classes) [ran] [tree fecc443f82df] (2026-10-09T05:02:35Z)
- (step 2) `python3 plugin/tests/run.py -k test_audit_diff_leaves_out_secrets -k test_audit_diff_refusal_names_prep` → exit 0 · Ran 2 tests in 0.3s (2 classes, 16 at a time; slowest: AuditPrep 0s, StateDirect 0s) / OK [ran] [tree 0ebe0932b26f] (2026-10-09T05:03:31Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.6    33.8     150  [0] / SessionEnd                  28.9    30.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 951 tests in [ran] [tree 0ebe0932b26f] (2026-10-09T05:05:11Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 05:05 UTC) [ran] [tree 0ebe0932b26f] (2026-10-09T05:05:13Z)
- (step 3) `fm check --evidence T-0413` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 05:05 UTC); cached (fm check --fresh reruns) [ran] [tree 0ebe0932b26f] (2026-10-09T05:05:13Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.4    34.6     150  [0] / SessionEnd                  29.3    32.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.90s]; python3 plugin/tests/run.py → exit 0 · Ran 953 tests in 38.2s (234 classes, 16 at a time [ran] [tree 791b2b8d2ed6] (2026-10-09T13:13:55Z)
- (ac 1) `python3 plugin/tests/run.py -k test_audit_diff_leaves_out_secrets -k test_audit_diff_refusal_names_prep` → exit 0 · Ran 2 tests in 0.3s (2 classes, 16 at a time; slowest: AuditPrep 0s, StateDirect 0s) / OK [ran] [tree 791b2b8d2ed6] (2026-10-09T13:17:57Z)
- (audit intent) `self: read the builder's diff (e6d5fcb) — redaction only on the written file; pre-audit and c.sensitive still read the raw diff (tested); merged by hand over a CHANGELOG conflict; gate on the merged tree exit 0` → JARVIS's case (untracked .env.bak frozen with keys) now leaves the body out and names the file; the refusal for rm of an audit diff names fm audit prep ID [tree 791b2b8d2ed6] (2026-10-09T13:17:57Z)
- (audit adversary) `self: read the builder's diff (e6d5fcb) — redaction only on the written file; pre-audit and c.sensitive still read the raw diff (tested); merged by hand over a CHANGELOG conflict; gate on the merged tree exit 0` → names checked on diff --git, ---/+++, rename/copy lines incl. git's quoted form, so a rename to or from a credential name is cut too; key=value secrets elsewhere go through c.redact [tree 791b2b8d2ed6] (2026-10-09T13:17:57Z)
- (audit edge) `self: read the builder's diff (e6d5fcb) — redaction only on the written file; pre-audit and c.sensitive still read the raw diff (tested); merged by hand over a CHANGELOG conflict; gate on the merged tree exit 0` → a mode-only change keeps just its header; a binary credential file is cut at 'Binary files'; a tracked tokens.json outside design folders is left out too (guard's rule, accepted) [tree 791b2b8d2ed6] (2026-10-09T13:17:57Z)
- (audit operator) `self: read the builder's diff (e6d5fcb) — redaction only on the written file; pre-audit and c.sensitive still read the raw diff (tested); merged by hand over a CHANGELOG conflict; gate on the merged tree exit 0` → the reviewer sees '(contents left out: a credential file)'; no setting [tree 791b2b8d2ed6] (2026-10-09T13:17:57Z)
- (audit maintainer) `self: read the builder's diff (e6d5fcb) — redaction only on the written file; pre-audit and c.sensitive still read the raw diff (tested); merged by hand over a CHANGELOG conflict; gate on the merged tree exit 0` → one helper reusing fmguard._is_credential and c.redact; no new rules [tree 791b2b8d2ed6] (2026-10-09T13:17:57Z)
## Log
- 2026-10-09T04:59:20Z created
- 2026-10-09T04:59:25Z set type=FIX
- 2026-10-09T05:00:34Z set tier=M
- 2026-10-09T05:01:27Z planned from capture
- 2026-10-09T05:01:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0413.builder.md
- 2026-10-09T05:01:36Z focused
- 2026-10-09T05:07:09Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2311dc16d3ebb838 (branch worktree-agent-a2311dc16d3ebb838 kept: not merged)
- 2026-10-09T05:07:09Z focused
- 2026-10-09T13:12:21Z user approved core in Claude Code's permission prompt
- 2026-10-09T13:17:57Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
- research T-0271-review-1: Changes needed. `task_prove_hunks` can record passing evidence when nothing was proven, and mishandles files with spaces and deleted files. I r…
- research T-0269-review-2: Verdict:** changes needed. I read the code only and ran nothing, so each "not blocked" below comes from tracing the code and is unexecuted.
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
## Lessons
- A frozen copy of the working tree is a second place secrets live: redact at the point it's written, not where it's read.
## Files touched
- .claude/worktrees/agent-a2311dc16d3ebb838/plugin/tests/test_guard.py
- .claude/worktrees/agent-a2311dc16d3ebb838/plugin/tests/test_cli.py
- .claude/worktrees/agent-a2311dc16d3ebb838/plugin/lib/fmcli.py
- .claude/worktrees/agent-a2311dc16d3ebb838/plugin/lib/fmguard.py
- .claude/worktrees/agent-a2311dc16d3ebb838/CHANGELOG.md
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmdocs.py
- plugin/lib/fmguard.py
- plugin/lib/fmplugins.py
- plugin/tests/test_cli.py
- plugin/tests/test_docsdrift.py
- plugin/tests/test_guard.py
- plugin/tests/test_guard_diff.py
- plugin/tests/test_hooks.py
