---
id: T-0180
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py,plugin/tests/test_guard.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: self
created: 2026-10-03T18:43:02Z
updated: 2026-10-03T18:51:05Z
base: ed25a902b454036a2af04e77eb45dcf179cd80ff
base_tree: 99b6361665d2119d96c0c17899638d9291ffb84b
verified: strong
---
# Guard: a standing or trusted yes covers a finding's plain path only — relative shell writes named by their real path, annotated details never
## Raw request
> Guard: a relative shell write to core reports the path as typed, so a standing yes never covers it (sed -i plugin/lib/x.py blocked, the same Edit allowed); and _standing_covers accepts annotated details ('/…/lib/$x (… could be fmguard.py)', tree writes) that sit string-wise under lib/ — report the resolved path and refuse annotated details — evidence: RSI pass 3, fmguard.py _target_cats detail and _standing_covers
## Interpretation
RSI pass 3: _target_cats names a literal relative target as typed, so _standing_covers (absolute paths only) never covers a relative shell write to Foreman code that an Edit would be allowed; and _standing_covers reads annotated details as paths, so '<lib>/fmguard.py (written from interpreter code)', '<lib>/$x (not known before it runs…)' and '<lib>/sub (a tree write over it)' all sit string-wise under lib/ — a standing yes then covers a python script writing the guard file itself.
## Assumptions (confidence)
## Acceptance criteria
- [x] a standing or trusted yes covers plain paths only — verify with `python3 plugin/tests/run.py -k test_a_standing_or_trusted_yes_covers_plain_paths_only`
## Non-goals
## Approach (options → choice → why)
A: one helper names the plain path a detail stands for — the interpreter suffix stripped, anything else annotated (a tree write, an unknown target) None — and both coverage checks use it; _target_cats names a resolved target by its absolute path. B (rejected): special-case each annotation in each check, the way the tree-write suffix was in _trust_covers alone, which is how the gap appeared.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] plain-path helper; absolute detail for resolved targets
3. [x] gates, docs, audit
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (what a standing yes covers)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_standing_or_trusted_yes_covers_plain_paths_only` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / FAILED (1 classes) [ran] [tree 310fda35ac7d] (2026-10-03T18:49:16Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_standing_or_trusted_yes_covers_plain_paths_only` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / FAILED (1 classes) [ran] [tree d1ae1e9cb912] (2026-10-03T18:49:27Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_standing_or_trusted_yes_covers_plain_paths_only` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree c3f9d020cb10] (2026-10-03T18:49:51Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    32.7     150  [0] / SessionEnd                  28.4    29.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 57 tests across 1 file. [2.47s]; python3 plugin/tests/run.py → exit 0 · Ran 602 tests in 22.3s (1 [ran] [tree c3f9d020cb10] (2026-10-03T18:50:45Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_standing_or_trusted_yes_covers_plain_paths_only` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree a6f2e8cc9e94] (2026-10-03T18:51:05Z)
- (audit intent) `self-review against the test table (standing and trusted, plain and annotated details), all guard and differential tests, 602 tests` → both pass-3 findings fixed — a relative shell write to Foreman code is covered by the standing yes as the same Edit is, and annotated details no longer read as paths under lib/ [tree a6f2e8cc9e94] (2026-10-03T18:51:05Z)
- (audit adversary) `self-review against the test table (standing and trusted, plain and annotated details), all guard and differential tests, 602 tests` → the coverage checks share one plain-path reading: the interpreter suffix stripped, anything else annotated refused, so a script writing fmguard.py, an unknown target and a tree write over plugin/ all ask under standing and trust; cp -r into lib/sub stays covered (one place, never the guard file); a path that itself contains ' (' isn't covered and asks, which only over-asks [tree a6f2e8cc9e94] (2026-10-03T18:51:05Z)
## Log
- 2026-10-03T18:43:02Z created
- 2026-10-03T18:49:07Z planned from capture
- 2026-10-03T18:49:07Z focused
- 2026-10-03T18:51:05Z done
- 2026-10-03T18:51:05Z committed 37d04ca (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0176 [FIX M, done, 3 steps] Guard: a python heredoc that provably writes only through open() counts only those files as written — lesson: Prove a relaxation by allowli…
- research T-0120-review: Verdict
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- similar finished tasks took 3–3 steps
- start here (files T-0176 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py, MASTER.md, CHANGELOG.md
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- When a check reads a string another part builds, give the format one reader: three coverage gaps came from details that grew annotations each reader handled differently.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- MASTER.md
- CHANGELOG.md
