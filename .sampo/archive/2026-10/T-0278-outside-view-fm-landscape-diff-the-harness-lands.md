---
id: T-0278
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/, plugin/tests/, MASTER.md, CHANGELOG.md]
depends_on: [T-0227]
source: user
created: 2026-10-04T07:46:35Z
updated: 2026-10-04T07:55:40Z
batch: [T-0237, T-0238]
base: 14d14d651ad777c5db6d04fa6d13ad7185362511
base_tree: ac67a52b4c8dfe0acbe8b807a6aac5c52ef8dc6f
verified: strong
---
# Outside view: fm landscape (diff the harness landscape against the last scan) and fm deps (new majors of dependencies, …
## Raw request
> T-0237: FEATURE: fm landscape — a recurring scout that re-runs the harness landscape research through fm research ask and diffs it against the last note: new capabilities people want that Foreman lacks #T-0227
> CONTEXT: research/harness-landscape-20261003.md; fmresearch
> DONE-WHEN: with stubbed research, fm landscape writes a dated note and a diff against the previous one
> T-0238: FEATURE: dependency-release watch — fm deps checks the project's dependencies (requirements, pyproject, package.json, Cargo.toml) against their latest releases and, for a new major, pre-researches the migration with fm research ask #T-0227
> CONTEXT: stdlib urllib to PyPI/npm/crates JSON APIs (public https only, like fmresearch.fetch)
> DONE-WHEN: with a fake registry response, fm deps lists an outdated major and offers the migration research
## Interpretation
Two outside views: what people want from harnesses now (and what changed since the last look), and which of a project's dependencies moved to a new major (with the migration researched before it bites).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0237: fm landscape runs the landscape question through fm research ask into a dated landscape note and appends a Since section against the previous landscape note: what's new, what's gone, and which new items an fm command already covers — verify with `python3 plugin/tests/run.py -p "test_outside*" -k Landscape`
- [x] T-0238: fm deps reads requirements*.txt, pyproject.toml, package.json and Cargo.toml, compares each dependency's major version with its registry's latest (PyPI, npm, crates.io), lists outdated majors with a migration question, and --research asks them — verify with `python3 plugin/tests/run.py -p "test_outside*" -k Deps`
## Non-goals
## Approach (options → choice → why)
Landscape: reuse fmresearch._ask with a fixed, dated question; extract items from the previous landscape note (bullets and numbered lines, marks and links stripped — it may be hand-written prose) and diff by the same word-overlap rule cross_check uses; new items run through fmrecall.covered so ones an fm command already does are marked; --if-due skips within 30 days. Deps: stdlib parsers (tomllib, json, a requirements regex); registry JSON over https with base URLs overridable by env (FOREMAN_PYPI_URL, FOREMAN_NPM_URL, FOREMAN_CRATES_URL — tests use a local server); majors compared on the first number of the pinned or lower-bound version; --research runs one fm research ask per outdated major (budgeted). Rejected: a lockfile resolver (semver ranges vary per ecosystem; the major of the stated bound is what a migration is about).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_outside.py (Landscape, Deps) with a stub claude and a local registry server
2. [x] fmoutside.py: cmd_landscape, cmd_deps; parser entries; help tier
3. [x] Docs: MASTER.md, CHANGELOG.md
## Resume here
<!-- auto -->
- 2026-10-04T07:47:58Z steps 0/3 done
- git: foreman/build; 2 uncommitted: plugin/lib/fmoutside.py, plugin/tests/test_outside.py
- touched since last checkpoint: plugin/tests/test_outside.py, plugin/lib/fmoutside.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_outside*"` → ✗ exit 1 · Ran 2 tests in 0.6s (2 classes, 16 at a time; slowest: Deps 1s, Landscape 0s) / FAILED (2 classes) [ran] [tree b3fbb0aea592] (2026-10-04T07:47:08Z)
- (step 2) `python3 plugin/tests/run.py -p test_outside.py` → exit 0 · Ran 2 tests in 0.8s (2 classes, 16 at a time; slowest: Deps 1s, Landscape 0s) / OK [ran] [tree 388452aa62b3] (2026-10-04T07:50:21Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.4    31.8     150  [0] / SessionEnd                  28.6    30.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 07:39 UTC; python3 plugin/tests/run.py → exit 0 · Ran 754 te [ran] [tree 2be426e6fa80] (2026-10-04T07:51:30Z)
- (step 3) `python3 plugin/tests/run.py -p test_outside.py` → exit 0 · Ran 4 tests in 1.4s (2 classes, 16 at a time; slowest: Deps 1s, Landscape 0s) / OK [ran] [tree 62df935ddd43] (2026-10-04T07:54:17Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_outside.py` → 2/3 hunks proven; unproven: plugin/lib/fmcli.py @@ -1933 +1933 @@ HELP_TIERS = [ [inconclusive] [ran] [tree 62df935ddd43] (2026-10-04T07:55:15Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p 'test_outside.py' && python3 plugin/tests/run.py -p 'test_help*.py'` → exit 0 · 3/3 hunks proven [ran] [tree 62df935ddd43] (2026-10-04T07:55:26Z)
- (step 1) `python3 plugin/tests/run.py -p test_outside.py` → exit 0 · Ran 4 tests in 1.4s (2 classes, 16 at a time; slowest: Deps 1s, Landscape 0s) / OK [ran] [tree 62df935ddd43] (2026-10-04T07:55:38Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_outside*" -k Landscape` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Landscape 0s) / OK [ran] [tree 62df935ddd43] (2026-10-04T07:55:40Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_outside*" -k Deps` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: Deps 1s) / OK [ran] [tree 62df935ddd43] (2026-10-04T07:55:40Z)
- (audit adversary) `one fm-reviewer pass (T-0278-review-1): 3 MEDIUM (registry fetch skipped the public-https/redirect guard; bare >= lower bounds reported as behind; --research untested) and 4 LOW (non-claim bullets as items, IncompleteRead crash, npm names unvalidated, brittle help-text assert) — all fixed test-first; hunks 3/3 proven` → registry requests public https only with redirects re-checked; npm names validated; outbound note text redacted+defanged [tree 62df935ddd43] (2026-10-04T07:55:40Z)
- (audit edge) `one fm-reviewer pass (T-0278-review-1): 3 MEDIUM (registry fetch skipped the public-https/redirect guard; bare >= lower bounds reported as behind; --research untested) and 4 LOW (non-claim bullets as items, IncompleteRead crash, npm names unvalidated, brittle help-text assert) — all fixed test-first; hunks 3/3 proven` → missing research dir, unreachable registry, uncapped specs, truncated responses, same-day rerun overwrites the day's note [tree 62df935ddd43] (2026-10-04T07:55:40Z)
- (audit intent) `one fm-reviewer pass (T-0278-review-1): 3 MEDIUM (registry fetch skipped the public-https/redirect guard; bare >= lower bounds reported as behind; --research untested) and 4 LOW (non-claim bullets as items, IncompleteRead crash, npm names unvalidated, brittle help-text assert) — all fixed test-first; hunks 3/3 proven` → both criteria met with tests (Landscape, Deps incl. --research) [tree 62df935ddd43] (2026-10-04T07:55:40Z)
## Log
- 2026-10-04T07:46:35Z created
- 2026-10-04T07:46:49Z set scope=['plugin/lib/', 'plugin/tests/', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-04T07:46:49Z focused
- 2026-10-04T07:55:40Z done
- 2026-10-04T07:55:40Z committed fccad6b (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- playbook /search-first — Research Before You Code (skills/playbooks/references/ground/search-first.md)
- research T-0206-review: Verdict: changes needed.** There is one MEDIUM robustness bug and two LOWs. I found no HIGH SSRF hole. I traced this by reading the code and did …
- T-0213 [RESEARCH M, done, 1 steps] Research other great plugins and what people want agent harnesses to do; add the best to F — lesson: Landscape research is cheapest as…
- the similar finished task took 1 steps
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_budget.py, plugin/tests/test_core.py, plugin/tests/test_docs.py, plugin/tests/test_doctor.py, plugin/tests/test_evolve.py, plugin/tests/test_friction.py,…
## Lessons
- A dependency 'behind a major' needs the spec's cap: >= alone never is
## Files touched
- plugin/tests/test_outside.py
- plugin/lib/fmoutside.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
