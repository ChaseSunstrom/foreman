# T-1798 brainstorm triage (2026-10-28)

Source: research/brainstorm-20261028-025248 (4 rounds × 14 lenses, 626 distinct ideas; the simplicity lens failed in round 3).
Grounded: the 14 value-5/effort-S and 18 value-5/effort-M ideas, each checked against the code by a scout.

## Built (no work)
- Confirm a red CI alarm against the newest run: fmforesight.py:88 (T-1810)
- Scan staged diffs for secrets before commit/push: fmcli.py:1757, fmsecrets.staged_leaks
- Fail a gate that runs zero tests: fmcore.py:558 _NO_TESTS, test_never_ran.py
- Deny reads of credential stores: fmguard.py:306 _CRED_DIRS (T-1224)
- Refuse `fm answer` from a model run: the guard's USER_ONLY_FM has `decide --answer` (T-1064)
- Version skew warning: fmdoctor.check_version_skew plus T-1810's session-start sweep
- Track every promise: fmcli.capture_promises (source: promise)

## Build now
- T-1818: CI workflows, hook configs, install scripts and pre-commit configs count as security-sensitive, so the adversary lens is required (today `.github/workflows/*.yml`, `hooks/hooks.json`, `install.sh` are not).

## Captured (next rounds)
- Prompt-cache misses in fm cost: turns that rewrote the whole cache after a gap past the TTL, named with their cost.
- One panic command: stop every run, free locks and leases, write a stop record (fm pause + PANIC only stop new starts today).
- Plugin parity matrix: each user-facing verb reachable through the installed plugin, checked in a test (T-1520 made them reachable; nothing checks it stays so).
- Dropped result → the redo starts from the drop reason and the first attempt's failing check.

## Killed (why)
- Preview a run's decisions with a 5 s countdown: the user said don't ask; `fm decide --review` reports them after.
- Human-typed nonce for destructive verbs: the guard's `fm ask` already gates those; a nonce would block full autonomy.
- Model-subprocess env allowlist: the children are the same agent with the same authority; an allowlist breaks tools (PATH, proxies, auth) for little gain. fmbench's denylist covers the test leak (T-1791).
- Review card + blocked close for CI/hook diffs: replaced by T-1818 (the adversary lens), no user stop under full autonomy.
- Scope outward grants to a SHA: the task is the grant's scope; expiring it mid-task would stop autonomous releases.
- Gate-lock fencing token, per-run push credentials, merge-conflict lane, rules retune duel, playbook quarantine (drafts are never adopted by themselves already): speculative or low value against their cost.
- Machine-wide spend ledger, coverage-map test selection, orphan registry: partial already (fm cost scans every project; fm check --affected; fmcode.stop_survivors); revisit if a failure shows the gap.
