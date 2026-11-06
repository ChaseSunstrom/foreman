---
id: T-0088
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-02T18:36:49Z
updated: 2026-10-02T19:01:08Z
base: 849ee3f68d6e3bcf639251779bfd42bb98344b58
verified: strong
---
# Round I core: fm ui --json view model + section aliases/ticks, one-call planning, literal-aware sensitive(), check timeout label (T-0074 T-0076 T-0080 T-0081 T-0083)
## Raw request
> Round I core: fm ui --json view model + section aliases/ticks, one-call planning, literal-aware sensitive(), check timeout label (T-0074 T-0076 T-0080 T-0081 T-0083)
## Interpretation
Bundle the five core items from the T-0082 slate into one task so one core grant covers them (core needs the user's yes; asked once at the end per full autonomy).
## Assumptions (confidence)
## Acceptance criteria
- [x] round I behaviours (sensitive literals, section aliases + kept ticks, timeout label, one-call planning) — verify with `python3 -m unittest discover -s plugin/tests -p 'test_round_i.py' -q`
- [x] fm ui --json contract and task show --json steps/criteria/depends — verify with `python3 -m unittest discover -s plugin/tests -p test_ui.py -q`
- [x] full suite green — verify with `python3 -m unittest discover -s plugin/tests -q`
## Non-goals
## Approach (options → choice → why)
Options: (a) one umbrella task, TDD per item, one core grant; (b) five tasks, five grants. Choice: (a). Why: same pattern as rounds A–H (T-0071), one prompt for the user.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0074 literal-aware sensitive()
2. [x] T-0080/T-0075 section aliases + kept ticks
3. [x] T-0081 timeout label
4. [x] T-0083 one-call planning
5. [x] T-0076 brief_json + fm ui --json
6. [x] docs: MASTER CLI line, CHANGELOG
## Resume here
## Docs impact
MASTER.md (CLI line: fm ui, task new --interpretation/--approach), CHANGELOG.md (round I)
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_round_i.py -q` → exit 0 · Ran 1 test in 0.007s / OK [ran] [tree 8f15f9733b10] (2026-10-02T18:43:45Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_round_i.py -q` → exit 0 · Ran 5 tests in 2.588s / OK [ran] [tree a8607080944a] (2026-10-02T18:44:58Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -p test_round_i.py -q` → exit 0 · Ran 5 tests in 2.573s / OK [ran] [tree a8607080944a] (2026-10-02T18:45:00Z)
- (step 4) `python3 -m unittest discover -s plugin/tests -p test_round_i.py -q` → exit 0 · Ran 5 tests in 2.576s / OK [ran] [tree a8607080944a] (2026-10-02T18:45:03Z)
- (step 5) `python3 -m unittest discover -s plugin/tests -p test_ui.py -q` → exit 0 · Ran 4 tests in 1.479s / OK [ran] [tree 700b649ff5e8] (2026-10-02T18:46:55Z)
- (step 6) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree e55940148e9b] (2026-10-02T18:49:35Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -p 'test_round_i.py' -q` → exit 0 · Ran 5 tests in 2.560s / OK [ran] [tree e55940148e9b] (2026-10-02T18:49:37Z)
- (ac 2) `python3 -m unittest discover -s plugin/tests -p test_ui.py -q` → exit 0 · Ran 4 tests in 1.456s / OK [ran] [tree e55940148e9b] (2026-10-02T18:49:39Z)
- (ac 3) `python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 506 tests in 141.174s / OK [ran] [tree e55940148e9b] (2026-10-02T18:52:04Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -p 'test_round_i.py' -q` → exit 0 · Ran 5 tests in 2.578s / OK [ran] [tree fce489d36b96] (2026-10-02T18:58:37Z)
- (ac 2) `python3 -m unittest discover -s plugin/tests -p test_ui.py -q` → exit 0 · Ran 5 tests in 1.815s / OK [ran] [tree fce489d36b96] (2026-10-02T18:58:39Z)
- (ac 3) `python3 -m unittest discover -s plugin/tests -q` → exit 0 · Ran 507 tests in 137.863s / OK [ran] [tree fce489d36b96] (2026-10-02T19:00:57Z)
- (audit intent) `fm-reviewer five-lens pass (research T-0088-review), findings verified against code; ride-alongs T-0075/T-0084 logged as scope` → pass: every slate item implemented and tested [tree fce489d36b96] (2026-10-02T19:01:04Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-0088-review), findings verified against code; f-string fields hid eval( from sensitive() — fixed test-first (f/rf/fr literals kept)` → fixed: MEDIUM closed; keep_ticks renumbering LOW: no new hole (done_blockers checks ticks) [tree fce489d36b96] (2026-10-02T19:01:04Z)
- (audit edge) `fm-reviewer five-lens pass (research T-0088-review), findings verified against code; ledger appends didn't move watched dirs — ledger.jsonl added to watch, tested; no-project path tested` → fixed: LOW closed [tree fce489d36b96] (2026-10-02T19:01:04Z)
- (audit operator) `fm-reviewer five-lens pass (research T-0088-review), findings verified against code; install.sh installed the mod unasked — --no-mod flag + explicit message; version bump left to release` → fixed: MEDIUM closed [tree fce489d36b96] (2026-10-02T19:01:04Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-0088-review), findings verified against code; brief_detail reuses brief_summary, recent_hook_errors extracted; step/criterion text now plain()` → pass: view() double brief load accepted (79 ms live) [tree fce489d36b96] (2026-10-02T19:01:04Z)
## Log
- 2026-10-02T18:36:49Z created
- 2026-10-02T18:43:22Z set approved=True
- 2026-10-02T18:43:22Z focused
- 2026-10-02T18:43:28Z user approved core in Claude Code's permission prompt
- 2026-10-02T18:53:54Z scope: T-0075 rides along with T-0080 (keep_ticks); T-0084 mod files, install.sh, uninstall.sh, marketplace and README belong to T-0084 and share this tree
- 2026-10-02T19:01:05Z done
- 2026-10-02T19:01:08Z includes T-0074: sensitive() ignores regex/string literals and 'guard' in paths
- 2026-10-02T19:01:08Z includes T-0075: Fm task set --section 'Acceptance criteria' drops the evidence↔criterion link: fm task don
- 2026-10-02T19:01:08Z includes T-0076: fm ui --json: one view-model snapshot for every surface (incl. steps, criteria, depends)
- 2026-10-02T19:01:08Z includes T-0080: fm task set --section resolves template headings and keeps criterion ticks
- 2026-10-02T19:01:08Z includes T-0081: fm check says 'timed out after N s' on a timeout
- 2026-10-02T19:01:08Z includes T-0083: fm task new plans an M/L brief in one call (--interpretation, --approach)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- research t0041-slate-review: HIGH — INTENT — slate item 9 (`brainstorm-20260926-smarter-slate.md:16`)** "Sensitive-path audits: a diff touching auth/crypto/secrets/exec/…
- research t0018-final-intent: HIGH — round 6 shipped with no recorded reviewer audit — `research/` (missing `t0018-r6-*` files) vs `tasks/T-0018-...md:81`.
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
## Lessons
- Bundle protected-core items into one umbrella task so the user grants core once; ask at the end of the non-core work, not per item.
## Files touched
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/tests/test_ui.py
- install.sh
- README.md
- .claude-plugin/marketplace.json
- .gitignore
- CHANGELOG.md
- MASTER.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/hooks.json
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmdoctor.py
- plugin/lib/fmwatch.py
- plugin/tests/test_round_i.py
- plugin/uninstall.sh
