---
id: T-0224
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T04:59:37Z
updated: 2026-10-04T05:16:26Z
base: 263266b1e874f7ba961a3aef11adc2b532b2dfa2
base_tree: 4fa707bb11edc7955cb89ae8a251565b16ce6af8
verified: strong
---
# Fm evolve — a bench-gated self-improvement loop: a mutation child proposes one revision or
## Raw request
> FEATURE: fm evolve — a bench-gated self-improvement loop: a mutation child proposes one revision or deletion of one Foreman text component (a skill, reference, rule section) from bench failures and friction, the candidate is built in a worktree, benched and gated against live, and winners wait on an evolve branch for the user's yes
> CONTEXT: plugin/lib/fmbench.py run_case keeps only pass/cost/turns; the replay's FOREMAN_STATE folder is deleted with the worktree
> CONTEXT: fmbench.py; /foreman:improve should require fm bench gate before proposing a merge
> CONTEXT: fmbench.build needs finished briefs today; commits with tests exist in every repo the user works on
> CONTEXT: fm run --models S=…,M=…,L=… is manual today (fmserve._models)
> CONTEXT: /foreman:improve is manual today; fm bench + gate are the referee; merging Foreman changes is always the user's call
> DONE-WHEN: a stubbed replay that writes Foreman events shows them summarized in its result and in fm bench show
> DONE-WHEN: tests show --runs 2 aggregates and fm bench gate passes an equal candidate and fails a worse one
> DONE-WHEN: a test repo's commit with a test and a fix becomes a valid case without any brief
> DONE-WHEN: a stubbed run where the cheap model passes recommends it and --save stores it
> DONE-WHEN: with stubbed claude, one evolve generation builds a candidate worktree with the proposed edit, benches both, and reports keep/drop from the gate
## Interpretation
The user wants Foreman to improve itself recursively, measured. fm bench + gate now make a fitness function; automate one generation of the loop: propose a revision (or deletion: ablation) of one Foreman instruction file from bench failures and friction, build it on its own branch, bench both arms on the same cases, gate, keep or drop. Merging stays the user's call.
## Assumptions (confidence)
## Acceptance criteria
- [x] with stubbed claude, one generation writes the child's revision on an evolve branch in a worktree, benches both arms, keeps it when the gate passes and removes it when it fails; --drop empties the target — verify with `python3 plugin/tests/run.py -k test_evolve`
- [x] one live generation runs end to end on a real target — verify with `fm bench list`
## Non-goals
## Approach (options → choice → why)
A) agentic evolve session with tools editing the worktree: powerful but unbounded and costly. B) tool-less mutation child (like fm ideas) that returns the whole revised file for one --target; fm writes it into a worktree branch evolve/<stamp> of Foreman's repo (--repo, default the repo holding this plugin), benches live and candidate (or reuses --live LABEL) with run_case_n, gates with fmbench.gate; keep → branch + commit stay with a report, drop → worktree and branch removed. Choice: B — bounded cost (one child + 2 arms × cases × runs), deterministic, testable with stubs.
## Risks and rollback
Candidate code never touches the live plugin; worktree outside the repo, branch named evolve/*. A mutated candidate still must ship the guard (fm bench refuses otherwise). Costs: --max 3 cases, --runs 1 default. Rollback: additive module + CLI.
## Execution prompt
## Steps
1. [x] Tests first (fixture Foreman repo with a fake plugin, stub claude)
2. [x] fmevolve.py generation + CLI
3. [x] Live generation; improve skill and docs
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/improve/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_evolve` → exit 0 · Ran 3 tests in 3.0s (1 classes, 16 at a time; slowest: Evolve 3s) / OK [ran] [tree 2925f58d7c58] (2026-10-04T05:12:46Z)
- (step 2) `python3 plugin/tests/run.py -k test_evolve` → exit 0 · Ran 3 tests in 3.0s (1 classes, 16 at a time; slowest: Evolve 3s) / OK [ran] [tree 2925f58d7c58] (2026-10-04T05:12:49Z)
- (step 1) `python3 plugin/tests/run.py -k test_evolve` → exit 0 · Ran 7 tests in 6.3s (1 classes, 16 at a time; slowest: Evolve 6s) / OK [ran] [tree 46e923c0f951] (2026-10-04T05:15:07Z)
- (step 2) `python3 plugin/tests/run.py -k test_evolve` → exit 0 · Ran 7 tests in 6.3s (1 classes, 16 at a time; slowest: Evolve 6s) / OK [ran] [tree 46e923c0f951] (2026-10-04T05:15:13Z)
- (step 3) `fm bench list` → exit 0 · evolve-20261004-001230-live: 1/1 passed · $0.11 · 7.0 turns/case / evolve-20261004-001230-cand: 1/1 passed · $0.13 · 10.0 turns/case [ran] [tree 46e923c0f951] (2026-10-04T05:15:13Z)
- `python3 plugin/tests/run.py -k test_evolve` → ✗ exit 1 · Ran 7 tests in 4.5s (1 classes, 16 at a time; slowest: Evolve 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 46e923c0f951] (2026-10-04T05:15:24Z)
- `python3 plugin/tests/run.py -k test_evolve` → exit 0 · Ran 7 tests in 6.3s (1 classes, 16 at a time; slowest: Evolve 6s) / OK [ran] [tree 46e923c0f951] (2026-10-04T05:15:24Z)
- (ac 1) `python3 plugin/tests/run.py -k test_evolve` → exit 0 · Ran 7 tests in 6.3s (1 classes, 16 at a time; slowest: Evolve 6s) / OK [ran] [tree 9e87fde42c81] (2026-10-04T05:16:26Z)
- (ac 2) `fm bench list` → exit 0 · evolve-20261004-001230-live: 1/1 passed · $0.11 · 7.0 turns/case / evolve-20261004-001230-cand: 1/1 passed · $0.13 · 10.0 turns/case [ran] [tree 9e87fde42c81] (2026-10-04T05:16:26Z)
- (audit adversary) `three fm-reviewer passes in parallel (fm audit prep --split), every finding verified and fixed test-first; one live generation` → fixed HIGH — run_arm skipped the guard check and targets could be the guard, hooks or fm, which an LLM rewrite would then run in bypass mode → targets limited to instruction .md files, run_arm itself refuses guardless plugins (tested); output parsed to the last </file>; --live label validated and pinned to HEAD and model [tree 9e87fde42c81] (2026-10-04T05:16:26Z)
- (audit edge) `three fm-reviewer passes in parallel (fm audit prep --split), every finding verified and fixed test-first; one live generation` → fixed MEDIUM — commit result unchecked (gpgsign/hooks) → checked with --no-verify and gpgsign off; dropped candidates leave no worktree or branch (tested), cleanup failures reported; frontmatter must survive (tested) [tree 9e87fde42c81] (2026-10-04T05:16:26Z)
- (audit intent) `three fm-reviewer passes in parallel (fm audit prep --split), every finding verified and fixed test-first; one live generation` → fixed HIGH — arms differed by uncommitted work → both arms from HEAD, the child sees HEAD's text (tested); a tie isn't kept (no clutter) except as an ablation finding; live generation on intake/SKILL.md: sensible revision, 1/1 both arms, cost +20% → gate rejected, nothing left behind [tree 9e87fde42c81] (2026-10-04T05:16:26Z)
- (audit operator) `three fm-reviewer passes in parallel (fm audit prep --split), every finding verified and fixed test-first; one live generation` → candidates live in <repo>.evolve/<time> on evolve/* branches only when better; output names how to review or discard; exit 0 kept, 1 not kept, 2 no change [tree 9e87fde42c81] (2026-10-04T05:16:26Z)
- (audit maintainer) `three fm-reviewer passes in parallel (fm audit prep --split), every finding verified and fixed test-first; one live generation` → one module over fmbench's run_arm/gate/_worktree; the dead _git wrapper removed [tree 9e87fde42c81] (2026-10-04T05:16:26Z)
## Log
- 2026-10-04T04:59:37Z created
- 2026-10-04T04:59:44Z set tier=L
- 2026-10-04T05:10:39Z focused
- 2026-10-04T05:10:40Z set approved=True
- 2026-10-04T05:16:26Z done
- 2026-10-04T05:16:26Z committed d756663 (7 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0220 [FEATURE S, done, 1 steps] Replay diagnostics — each bench case keeps a summary of the replay's own Foreman ledger (t
- T-0221 [FEATURE S, done, 1 steps] Bench rigor — fm bench run --runs N reports per-case pass fraction and cost/turns spread,
- T-0223 [FEATURE M, done, 1 steps] Fm bench models — replay the cases once per model and recommend the cheapest model that pa — lesson: Recommend from measured pass total…
- T-0222 [FEATURE S, done, 1 steps] Fm bench build --commits RANGE --verify CMD — bench cases from any repo's history (commits
- similar finished tasks took 1–1 steps
- start here (files T-0220 touched): plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_bench.py, CHANGELOG.md, MASTER.md
## Lessons
- A self-modifying loop needs the same trust boundary as its runner: restrict what may be mutated (text, not code) and put the safety check in the shared function every path goes through, not in one CLI command
## Files touched
- plugin/tests/test_evolve.py
- plugin/lib/fmbench.py
- plugin/lib/fmevolve.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/improve/SKILL.md
