---
id: T-2318
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T11:02:24Z
updated: 2026-10-31T11:17:57Z
builder_model: sonnet
base: 022091b3d2d135af3ce96c06f6cc20c97ec05908
base_tree: a6ac7800886f22b0e9d68336ed1894b0d5043238
plan0_at: 2026-10-31T11:07:10Z
plan0_scope: []
verified: strong
---
# fm audit prep's git diff can't take an option from --base and runs no repo diff driver
## Raw request
> SECURITY: fm audit prep's diff (fmcli.py ~5409: git -C root diff a z) passes --base's value as a revision with no --end-of-options, so a value starting with -- reads as a git option (e.g. --output=FILE writes a file), and it runs without --no-ext-diff/--no-textconv and the fsmonitor/hooksPath overrides other Foreman git calls use: add them and refuse a --base that isn't a revision
## Interpretation
cmd_audit runs git -C root diff A Z with A from --base and no --end-of-options, so a --base value starting with -- is read as a git option (e.g. --output=FILE writes a file); and it runs without --no-ext-diff, --no-textconv and the core.fsmonitor/hooksPath overrides the other Foreman git calls carry.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm audit prep --base '--output=FILE' refuses (not a revision) and writes no file; every git diff/log call in cmd_audit carries --no-ext-diff --no-textconv, core.fsmonitor=false and core.hooksPath=/dev/null, with revisions resolved through rev-parse --verify --end-of-options — verify with `python3 plugin/tests/run.py test_audit`
## Non-goals
## Approach (options → choice → why)
Options: 1) resolve every revision to a sha with rev-parse --verify --end-of-options, then pass shas only, plus the safe diff options; 2) reject any --base starting with -; 3) add -- between revisions and paths only. Choice 1: a sha can't be an option, and an unknown name fails clearly; 2 alone leaves textconv and ext-diff; 3 doesn't stop an option in the revision slot.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests: a --base starting with -- refuses and writes nothing; the diff call's argv carries the safe options
2. [x] Resolve --base (and other revisions) with rev-parse --verify --end-of-options before use; route cmd_audit's git diff through the safe option set
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_audit 2>&1 | tail -15` → ✗ exit 1 · Ran 38 tests in 6.0s (17 classes, 16 at a time; slowest: AuditRun 6s, DesignLens 5s, ImportCards 2s) / FAILED (1 classes) [ran] [tree bc0879d93f4b] (2026-10-31T11:07:57Z)
- (ac 1) `python3 plugin/tests/run.py test_audit 2>&1 | tail -6` → exit 0 · Ran 38 tests in 6.1s (17 classes, 16 at a time; slowest: AuditRun 6s, DesignLens 6s, ImportCards 3s) / OK [ran] [tree 81a91083c889] (2026-10-31T11:08:06Z)
- (step 1) `python3 plugin/tests/run.py test_audit 2>&1 | tail -6` → exit 0 · Ran 38 tests in 6.1s (17 classes, 16 at a time; slowest: AuditRun 6s, DesignLens 6s, ImportCards 3s) / OK [ran] [tree 81a91083c889] (2026-10-31T11:08:06Z)
- (step 1) `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 38 tests in 6.4s (17 classes, 16 at a time; slowest: AuditRun 6s, DesignLens 6s, ImportCards 3s) / OK [ran] [tree 81a91083c889] (2026-10-31T11:08:15Z)
- (step 2) `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 38 tests in 7.0s (17 classes, 16 at a time; slowest: AuditRun 7s, DesignLens 6s, ImportCards 3s) / OK [ran] [tree 81a91083c889] (2026-10-31T11:08:22Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_verbs test_cli test_guard_cases test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.47s] [ran] [tree 81a91083c889] (2026-10-31T11:09:12Z)
- (step 1) `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 41 tests in 13.4s (17 classes, 16 at a time; slowest: AuditRun 13s, DesignLens 12s, ImportCards 6s) / OK [ran] [tree 8f3c67fda29c] (2026-10-31T11:12:08Z)
- (step 2) `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 41 tests in 12.2s (17 classes, 16 at a time; slowest: AuditRun 12s, DesignLens 11s, ImportCards 5s) / OK [ran] [tree 8f3c67fda29c] (2026-10-31T11:12:20Z)
- `python3 plugin/tests/run.py test_audit` → ✗ exit 1 · Ran 41 tests in 13.4s (17 classes, 16 at a time; slowest: AuditRun 12s, DesignLens 10s, ImportCards 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8f3c67fda29c] (2026-10-31T11:12:52Z)
- `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 41 tests in 17.0s (17 classes, 16 at a time; slowest: AuditRun 17s, DesignLens 16s, ImportCards 9s) / OK [ran] [tree 8f3c67fda29c] (2026-10-31T11:12:52Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_verbs test_builder test_cli test_docs test_guard_cases test_lanes test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.57s] [ran] [tree ece5a5ab2219] (2026-10-31T11:14:34Z)
- (step 1) `python3 plugin/tests/run.py test_audit test_builder` → exit 0 · Ran 70 tests in 11.9s (25 classes, 16 at a time; slowest: DesignLens 11s, Contract 11s, AuditRun 10s) / OK [ran] [tree 109b0e3d2b89] (2026-10-31T11:16:00Z)
- (step 2) `python3 plugin/tests/run.py test_audit test_builder` → exit 0 · Ran 70 tests in 12.0s (25 classes, 16 at a time; slowest: DesignLens 12s, Contract 11s, AuditRun 10s) / OK [ran] [tree 109b0e3d2b89] (2026-10-31T11:16:12Z)
- `python3 plugin/tests/run.py test_audit` → ✗ exit 1 · Ran 43 tests in 14.0s (17 classes, 16 at a time; slowest: DesignLens 12s, AuditRun 10s, ImportCards 4s) / FAILED (1 classes: test_audit.DesignLens) (start tree + this task's tests) [ran] [tree 109b0e3d2b89] (2026-10-31T11:16:39Z)
- `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 43 tests in 11.8s (17 classes, 16 at a time; slowest: DesignLens 11s, AuditRun 9s, ImportCards 4s) / OK [ran] [tree 109b0e3d2b89] (2026-10-31T11:16:39Z)
- (ac 1) `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 43 tests in 11.7s (17 classes, 16 at a time; slowest: DesignLens 11s, AuditRun 9s, ImportCards 4s) / OK [ran] [tree 2c2c9cff101a] (2026-10-31T11:17:02Z)
- (audit intent) `self-review of the 12-line change: each side of every diff pair resolves through rev-parse --verify -q --end-of-options X^{tree} before use, so only ids reach git diff; an unknown or option-like value refuses with 'not a revision'; the diff carries -c core.fsmonitor=false -c core.hooksPath=/dev/null --no-ext-diff --no-textconv; conflict with T-2312 resolved by the builder keeping both test sets` → audit prep can't be steered into writing files or running repo drivers through --base [tree 2c2c9cff101a] (2026-10-31T11:17:02Z)
- (audit adversary) `self-review of the 12-line change: each side of every diff pair resolves through rev-parse --verify -q --end-of-options X^{tree} before use, so only ids reach git diff; an unknown or option-like value refuses with 'not a revision'; the diff carries -c core.fsmonitor=false -c core.hooksPath=/dev/null --no-ext-diff --no-textconv; conflict with T-2312 resolved by the builder keeping both test sets` → --base=--output=FILE refuses and writes nothing (test); a repo diff.external driver never runs (test); only tree ids reach git diff, so no ref name reads as an option [tree 2c2c9cff101a] (2026-10-31T11:17:02Z)
- (audit edge) `self-review of the 12-line change: each side of every diff pair resolves through rev-parse --verify -q --end-of-options X^{tree} before use, so only ids reach git diff; an unknown or option-like value refuses with 'not a revision'; the diff carries -c core.fsmonitor=false -c core.hooksPath=/dev/null --no-ext-diff --no-textconv; conflict with T-2312 resolved by the builder keeping both test sets` → argparse already refuses a bare --base --x, so the =-form is the case; resolving to ^{tree} keeps the same diff text [tree 2c2c9cff101a] (2026-10-31T11:17:02Z)
## Log
- 2026-10-31T11:02:24Z created
- 2026-10-31T11:06:58Z planned from capture
- 2026-10-31T11:06:58Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2318.builder.md
- 2026-10-31T11:07:09Z focused
- 2026-10-31T11:15:45Z merged worktree-agent-a039c195a670e1051 (2 file(s))
- 2026-10-31T11:15:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a039c195a670e1051
- 2026-10-31T11:15:46Z focused
- 2026-10-31T11:16:50Z scope: plugin/lib/fmcli.py (cmd_audit's diff), plugin/tests/test_audit.py, CHANGELOG.md
- 2026-10-31T11:17:55Z done
- 2026-10-31T11:17:57Z committed 3339f087 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0269-review-1: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict [stale: plugin/lib/fmcore.py, plugin/lib/fmguard.py chang…
- research T-0269-review-2: Verdict:** changes needed. I read the code only and ran nothing, so each "not blocked" below comes from tracing the code and is unexecuted.
- research t0018-r4-adversary: fSTe81D17ZxNHRCBuwq4","type":"message","role":"assistant","content":[{"type":"text","text":"## Verdict: changes needed\n\n## Findings\n\n**C…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
## Lessons
- Resolve user-supplied revisions to ids before passing them to git: an id can never be an option
## Files touched
- plugin/tests/test_audit.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmlanes.py
- plugin/tests/test_builder.py
