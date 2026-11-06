---
id: T-0263
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/, plugin/tests/, MASTER.md, CHANGELOG.md, plugin/skills/, mods/foreman-ui/]
depends_on: []
source: user
created: 2026-10-04T06:22:25Z
updated: 2026-10-04T06:29:48Z
batch: [T-0248, T-0249, T-0246]
base: 4cb043aecaccf4a4ca3f479e9f81e61f064d1e9e
base_tree: 54c332d82718581c96cc72af091edf5a0748a9e4
verified: strong
---
# Handoff: diff tour, proof sections in fm pr, AGENTS.md export
## Raw request
> T-0248: FEATURE: diff tour — fm tour ID prints the task's changed files in dependency order (imports first) with each file's change size and the step that touched it
> DONE-WHEN: a two-file diff where one imports the other lists the imported one first
> T-0249: FEATURE: PR proof pack — fm proof ID writes a markdown pack (criteria and their runs, red→green, audit lenses, bench results) for a PR body
> DONE-WHEN: fm proof on a finished task prints those sections
> T-0246: FEATURE: AGENTS.md export — fm export agents writes an AGENTS.md (rules summary, lessons, playbook index, project map) for other harnesses
> DONE-WHEN: fm export agents writes a file under a size cap with those sections
## Interpretation
Make finished work easy to hand over: a reading order for the diff, a PR body with its proof, and the project's working knowledge for other harnesses (Codex, Cursor, Gemini read AGENTS.md).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0248: fm tour ID lists the task's changed files imported-first, with +/- sizes and the step that touched each — verify with `python3 plugin/tests/run.py -p "test_handoff*" -k Tour`
- [x] T-0249: fm pr on a finished task also prints its red→green command, each audit lens's result, its assumptions and its bench replays (fm pr already covers the PR body: no new fm proof) — verify with `python3 plugin/tests/run.py -p "test_handoff*" -k Proof`
- [x] T-0246: fm export agents writes AGENTS.md (working rules, user corrections, map, lessons, decisions, playbook index) under 32 KiB and never overwrites one it didn't write without --force — verify with `python3 plugin/tests/run.py -p "test_handoff*" -k Export`
## Non-goals
## Approach (options → choice → why)
Tour in fmmap (it already has changed() and the name-stem dependency heuristic of fm impact): graphlib.TopologicalSorter over 'B names A's stem' edges, cycles fall back to most-depended-on first; step = the first step whose first evidence came after the file's last edit. Proof: extend fmcost.cmd_pr (fm pr already is the PR body) — Brief.red_green_cmd() so red_green() and pr share one loop. Export: cmd_export in fmcost beside pr/digest; a generated-by marker guards hand-written files; 32 KiB = Codex's default project_doc_max_bytes. Rejected: a separate fm proof (duplicates fm pr; the covered check from T-0256 flags it).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_handoff.py (Tour, Proof, Export) fail
2. [x] Implement fm tour, fm pr proof sections, fm export agents
3. [x] foreman-ui: no pane change — tour, pr and export are on-demand prints with no state to show; the mod suite stays green
4. [x] Docs: MASTER.md, CHANGELOG.md
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_handoff*"` → ✗ exit 1 · Ran 5 tests in 0.7s (3 classes, 16 at a time; slowest: Proof 1s, Tour 1s, Export 0s) / FAILED (3 classes) [ran] [tree 33205ce71914] (2026-10-04T06:23:13Z)
- (step 2) `python3 plugin/tests/run.py -p "test_handoff*" -p "test_help*"` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Help 0s) / OK [ran] [tree f5d1da8e58da] (2026-10-04T06:25:52Z)
- (step 3) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.77s] [ran] [tree f5d1da8e58da] (2026-10-04T06:25:55Z)
- (step 2) `python3 plugin/tests/run.py -p "test_handoff*"` → exit 0 · Ran 5 tests in 0.6s (3 classes, 16 at a time; slowest: Tour 1s, Proof 1s, Export 0s) / OK [ran] [tree f5d1da8e58da] (2026-10-04T06:25:59Z)
- (step 4) `grep -c 'fm tour\|export agents' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:2 / CHANGELOG.md:1 [ran] [tree 0209e3f2164c] (2026-10-04T06:26:08Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.7    32.5     150  [0] / SessionEnd                  27.6    29.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:16 UTC; python3 plugin/tests/run.py → e [ran] [tree 0209e3f2164c] (2026-10-04T06:26:58Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.6    32.3     150  [0] / SessionEnd                  27.3    29.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:16 UTC; python3 plugin/tests/run.py → e [ran] [tree 3075ab82eea1] (2026-10-04T06:29:40Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_handoff*" -k Tour` → exit 0 · Ran 3 tests in 1.1s (1 classes, 16 at a time; slowest: Tour 1s) / OK [ran] [tree 3075ab82eea1] (2026-10-04T06:29:48Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_handoff*" -k Proof` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Proof 1s) / OK [ran] [tree 3075ab82eea1] (2026-10-04T06:29:48Z)
- (ac 3) `python3 plugin/tests/run.py -p "test_handoff*" -k Export` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: Export 1s) / OK [ran] [tree 3075ab82eea1] (2026-10-04T06:29:48Z)
- (audit intent) `one fm-reviewer pass over all five lenses (research T-0263-review-1); 3 MEDIUM + 4 LOW fixed with tests` → criteria met; fm pr carries the proof instead of a duplicate fm proof [tree 3075ab82eea1] (2026-10-04T06:29:48Z)
- (audit adversary) `one fm-reviewer pass over all five lenses (research T-0263-review-1); 3 MEDIUM + 4 LOW fixed with tests` → fixed — playbook paths plugin-relative, sensitive projects export no one's words, corrections/lessons defanged, symlink targets refused, hostile bench JSON ignored [tree 3075ab82eea1] (2026-10-04T06:29:48Z)
- (audit edge) `one fm-reviewer pass over all five lenses (research T-0263-review-1); 3 MEDIUM + 4 LOW fixed with tests` → fixed — --no-renames in tour, unreadable/dir --out is a usage error; batch members tour from focus (documented) [tree 3075ab82eea1] (2026-10-04T06:29:48Z)
- (audit operator) `one fm-reviewer pass over all five lenses (research T-0263-review-1); 3 MEDIUM + 4 LOW fixed with tests` → ok — docs, help tiers; export prints a read-before-committing note [tree 3075ab82eea1] (2026-10-04T06:29:48Z)
- (audit maintainer) `one fm-reviewer pass over all five lenses (research T-0263-review-1); 3 MEDIUM + 4 LOW fixed with tests` → fixed — _DEF spacing; tests for corrections, sensitive, symlink, rename, hostile JSON [tree 3075ab82eea1] (2026-10-04T06:29:48Z)
## Log
- 2026-10-04T06:22:25Z created
- 2026-10-04T06:22:56Z set scope=['plugin/lib/', 'plugin/tests/', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/', 'mods/foreman-ui/']
- 2026-10-04T06:22:56Z focused
- 2026-10-04T06:29:48Z done
- 2026-10-04T06:29:48Z committed 6628b0d (7 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- playbook Living Docs Governance (skills/playbooks/references/context/living-docs.md)
- research brainstorm-20260926-smarter-slate: Secret redaction before evidence/ledger/sync (security): premise false: fmcore.redact runs on typed and --run evidence (add_e…
- research brainstorm-20260926-super-slate: Built under T-0071, in rounds (inbox items folded in):
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_budget.py, plugin/tests/test_core.py, plugin/tests/test_docs.py, plugin/tests/test_doctor.py, plugin/tests/test_evolve.py, plugin/tests/test_friction.py,…
## Lessons
- Anything written for other people or tools (AGENTS.md, PR bodies) needs its own privacy pass: redact() catches secrets, not the user's words, absolute home paths or a sensitive project's history
## Files touched
- plugin/tests/test_handoff.py
- plugin/lib/fmcore.py
- plugin/lib/fmmap.py
- plugin/lib/fmcost.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
