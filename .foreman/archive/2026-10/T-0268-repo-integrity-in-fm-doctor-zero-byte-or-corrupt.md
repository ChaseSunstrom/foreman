---
id: T-0268
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/lib/fmcli.py, plugin/tests/, plugin/skills/doctor/, MASTER.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-04T06:41:39Z
updated: 2026-10-04T07:05:00Z
base: 18ac1e42ef365e7abd2879b1dfc849c14b0468c3
base_tree: d77544e9a340ac3dad202a04e9eed3422ef12953
verified: strong
---
# Repo integrity in fm doctor: empty git objects and truncated state, fm doctor --repair
## Raw request
> Repo integrity in fm doctor: zero-byte or corrupt loose git objects and truncated state files, with fm doctor --repair quarantining empty objects
## Interpretation
A crash mid-write left four empty git objects today; git diff failed and fm doctor passed. Doctor should see crash damage in git objects and Foreman's state, and fix the safe part.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm doctor fails on zero-byte loose git objects in Foreman's or a project's repo, zero-byte briefs and unreadable state JSON, naming each — verify with `python3 plugin/tests/run.py -p "test_integrity*" -k Check`
- [x] fm doctor --repair moves empty loose objects into Foreman's quarantine (never deletes) and the check passes after — verify with `python3 plugin/tests/run.py -p "test_integrity*" -k Repair`
## Non-goals
## Approach (options → choice → why)
Options: git fsck (slow on big repos, needs the full object walk) vs a scandir of .git/objects/?? for zero-byte files plus a parse of the state JSON and briefs. Choice: the scan — milliseconds, finds exactly what a crash leaves, and fm check runs doctor as a gate. Repair only moves zero-byte loose objects (they hold nothing) to state/quarantine/; git rewrites any the working files still hold; anything else is reported, not touched.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_integrity.py (Check, Repair)
2. [x] Implement check_integrity and repair in fmdoctor, --repair in the parser
3. [x] Docs: MASTER.md, CHANGELOG.md, the doctor skill
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/doctor/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_integrity*"` → ✗ exit 1 · Ran 5 tests in 0.3s (2 classes, 16 at a time; slowest: Check 0s, Repair 0s) / FAILED (2 classes) [ran] [tree ee0cdade8df3] (2026-10-04T07:01:09Z)
- (step 2) `python3 plugin/tests/run.py -p "test_integrity*"` → exit 0 · Ran 5 tests in 0.3s (2 classes, 16 at a time; slowest: Check 0s, Repair 0s) / OK [ran] [tree b9a31afe1409] (2026-10-04T07:01:51Z)
- (step 3) `grep -c 'repair' MASTER.md CHANGELOG.md plugin/skills/doctor/SKILL.md` → exit 0 · CHANGELOG.md:1 / plugin/skills/doctor/SKILL.md:1 [ran] [tree b9a31afe1409] (2026-10-04T07:01:51Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            8 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.4    35.2     150  [0] / SessionEnd                  27.9    28.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → exit 0 · Ran 718 te [ran] [tree b9a31afe1409] (2026-10-04T07:02:38Z)
- (step 2) `python3 plugin/tests/run.py -p "test_integrity*"` → exit 0 · Ran 7 tests in 0.4s (2 classes, 16 at a time; slowest: Check 0s, Repair 0s) / OK [ran] [tree 6f3011be89bb] (2026-10-04T07:04:04Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.7    34.0     150  [0] / SessionEnd                  28.2    29.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → exit 0 · Ran 720 te [ran] [tree 6f3011be89bb] (2026-10-04T07:04:53Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_integrity*" -k Check` → exit 0 · Ran 5 tests in 0.4s (1 classes, 16 at a time; slowest: Check 0s) / OK [ran] [tree 6f3011be89bb] (2026-10-04T07:05:00Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_integrity*" -k Repair` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Repair 0s) / OK [ran] [tree 6f3011be89bb] (2026-10-04T07:05:00Z)
- (audit intent) `fm-reviewer pass over all lenses (research T-0268-review-1); 3 MEDIUM + 2 LOW fixed with tests` → criteria met — doctor names crash damage; --repair only moves empty objects [tree 6f3011be89bb] (2026-10-04T07:05:00Z)
- (audit adversary) `fm-reviewer pass over all lenses (research T-0268-review-1); 3 MEDIUM + 2 LOW fixed with tests` → ok — only object-named, zero-byte, non-symlink files in two-hex folders move; never deletes [tree 6f3011be89bb] (2026-10-04T07:05:00Z)
- (audit edge) `fm-reviewer pass over all lenses (research T-0268-review-1); 3 MEDIUM + 2 LOW fixed with tests` → fixed — git's tmp_obj_* and objects being written skipped (name + 5 s age), cross-filesystem moves via shutil.move with per-object errors, gc/prune races and vanished briefs tolerated [tree 6f3011be89bb] (2026-10-04T07:05:00Z)
- (audit operator) `fm-reviewer pass over all lenses (research T-0268-review-1); 3 MEDIUM + 2 LOW fixed with tests` → fixed — the count is repos actually scanned; all_projects read once per run [tree 6f3011be89bb] (2026-10-04T07:05:00Z)
- (audit maintainer) `fm-reviewer pass over all lenses (research T-0268-review-1); 3 MEDIUM + 2 LOW fixed with tests` → ok — tests for in-flight files, non-git roots, truncated state [tree 6f3011be89bb] (2026-10-04T07:05:00Z)
## Log
- 2026-10-04T06:41:39Z created
- 2026-10-04T07:00:58Z planned from capture
- 2026-10-04T07:00:58Z set scope=['plugin/lib/fmdoctor.py', 'plugin/lib/fmcli.py', 'plugin/tests/', 'plugin/skills/doctor/', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-04T07:00:58Z focused
- 2026-10-04T07:05:00Z done
- 2026-10-04T07:05:00Z committed 2c4af45 (6 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-pass-1: Source: research/brainstorm-20261004-013651 (4 lenses × 3 rounds, past the four earlier idea lists; 132 new titles). Pack: the user's words, …
- research T-0212-review: Verdict: changes needed.** There are no CRITICAL or HIGH findings. Two MEDIUM issues are worth fixing before relying on `compare`. I read the cod…
- research t0018-final-operator: Not directly related. I have sufficient evidence now. Let me finalize. [stale: plugin/uninstall.sh changed since it was written]
- research T-0087-review: Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW. […
- likely tests for the scope: plugin/tests/test_doctor.py
## Lessons
- A health check that is also a gate must never crash or flap: tolerate files vanishing mid-scan and ignore what a concurrent writer legitimately leaves for a moment
## Files touched
- plugin/tests/test_integrity.py
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/skills/doctor/SKILL.md
- CHANGELOG.md
- MASTER.md
