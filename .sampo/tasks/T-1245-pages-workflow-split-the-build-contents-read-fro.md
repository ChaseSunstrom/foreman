---
id: T-1245
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-16T21:06:17Z
updated: 2026-10-20T17:33:53Z
base: d4e46d226536b64070dbd135797b93b1ff2cd93d
base_tree: fec734e9bb7de9aa8c87f10af474c2f2a966b981
plan0_at: 2026-10-20T17:25:45Z
plan0_scope: []
verified: strong
---
# Pages workflow: build job with contents read only, deploy job with pages and id-token write; every action in both workflows pinned to a commit SHA
## Raw request
> Pages workflow: split the build (contents: read) from the deploy job (pages/id-token write) and pin actions by SHA; site review LOW
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] pages.yml has a build job (contents: read, uploads the artifact) and a deploy job (needs build; pages: write, id-token: [REDACTED] and no top-level write permission; every uses: line in .github/workflows pins a 40-character commit SHA with its version in a comment — verify with `python3 plugin/tests/run.py test_workflows`
## Non-goals
## Approach (options → choice → why)
Options: (a) split build and deploy, pin by SHA with the tag in a comment (GitHub's own hardening guide); (b) keep one job, narrow nothing (a compromised build step holds the deploy token); (c) pin by tag only (tags move). Choice: (a); a test keeps every future uses: line pinned.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: test_workflows.py reads both workflows and checks the job permissions and the pins
2. [x] Split the jobs, pin each action (gh api repos/<action>/commits/<tag>), docs
## Resume here
## Docs impact
CHANGELOG (with T-1279's missing line)
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_workflows 2>&1 | tail -8` → ✗ exit 1 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Workflows 0s) / FAILED (1 classes) [ran] [tree 936bffaa73ca] (2026-10-20T17:25:59Z)
- (ac 1) `python3 plugin/tests/run.py test_workflows 2>&1 | grep -E "^(FAIL|OK|Ran)"` → ✗ exit 1 · Ran 5 tests in 0.2s (2 classes, 16 at a time; slowest: Workflows 0s, CiWorkflows 0s) / FAILED (1 classes) [ran] [tree 724d6a28a862] (2026-10-20T17:26:11Z)
- (ac 1) `python3 plugin/tests/run.py test_workflows 2>&1 | grep -E "^(FAIL|OK|Ran)"` → exit 0 · Ran 5 tests in 0.2s (2 classes, 16 at a time; slowest: Workflows 0s, CiWorkflows 0s) / OK [ran] [tree 2bac6a756b15] (2026-10-20T17:26:22Z)
- (step 1) `python3 plugin/tests/run.py test_workflows 2>&1 | grep -E "^(FAIL|OK|Ran)"` → exit 0 · Ran 5 tests in 0.2s (2 classes, 16 at a time; slowest: Workflows 0s, CiWorkflows 0s) / OK [ran] [tree 2bac6a756b15] (2026-10-20T17:26:22Z)
- (step 2) `python3 plugin/tests/run.py test_workflows` → exit 0 · Ran 5 tests in 0.2s (2 classes, 16 at a time; slowest: Workflows 0s, CiWorkflows 0s) / OK [ran] [tree 2bac6a756b15] (2026-10-20T17:26:22Z)
- (step 1) `python3 plugin/tests/run.py test_workflows` → exit 0 · Ran 5 tests in 0.2s (2 classes, 16 at a time; slowest: Workflows 0s, CiWorkflows 0s) / OK [ran] [tree 2bac6a756b15] (2026-10-20T17:26:24Z)
- (ac 1) `python3 plugin/tests/run.py test_workflows` → exit 0 · Ran 5 tests in 0.2s (2 classes, 16 at a time; slowest: Workflows 0s, CiWorkflows 0s) / OK [ran] [tree fcdd4f34a84c] (2026-10-20T17:32:59Z)
- (audit intent) `main session read the split workflow, checked each pinned SHA against its tag with gh api, and moved configure-pages into the deploy job (it reads the Pages settings, which a contents-read token may not)` → the site review asked that the build, which runs the repo's code, hold no deploy rights; now only the deploy job has them [tree fcdd4f34a84c] (2026-10-20T17:32:59Z)
- (audit adversary) `main session read the split workflow, checked each pinned SHA against its tag with gh api, and moved configure-pages into the deploy job (it reads the Pages settings, which a contents-read token may not)` → a compromised build step gets a contents-read token and the artifact upload only; tags can't move under the pins; the test fails any unpinned uses: line [tree fcdd4f34a84c] (2026-10-20T17:32:59Z)
- (audit operator) `main session read the split workflow, checked each pinned SHA against its tag with gh api, and moved configure-pages into the deploy job (it reads the Pages settings, which a contents-read token may not)` → SHA pins don't update themselves; bump them by tag when an action ships a fix [tree fcdd4f34a84c] (2026-10-20T17:32:59Z)
- (audit self) `main session read the split workflow, checked each pinned SHA against its tag with gh api, and moved configure-pages into the deploy job (it reads the Pages settings, which a contents-read token may not)` → no findings [tree fcdd4f34a84c] (2026-10-20T17:32:59Z)
## Log
- 2026-10-16T21:06:17Z created
- 2026-10-20T17:20:59Z planned from capture
- 2026-10-20T17:25:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1245.builder.md
- 2026-10-20T17:25:45Z focused
- 2026-10-20T17:30:21Z merged worktree-agent-afc2227c289d6de76 (3 file(s))
- 2026-10-20T17:30:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afc2227c289d6de76
- 2026-10-20T17:32:59Z focused
- 2026-10-20T17:33:52Z done
- 2026-10-20T17:33:53Z committed dcce07f0 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1220-review: Changes needed. Nothing is critical. Three MEDIUM defects are worth fixing before the next publish. I read the code and the data files and did no…
- T-1220 [FEATURE L, done, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history — lesson: A stdlib site g…
- T-1206 [FEATURE M, done, 3 steps] A GitHub Pages site for Foreman: one modern page with the real demo, the loop, the guard and install — lesson: A marketing page for a d…
- decision 2026-10-15: T-0964: queue 7 of the rival gaps (T-0969..T-0975); keep the LATER ones (PR-per-task flow, best-of-N lanes, diff-comment review page, plan/edit mode…
## Lessons
- A job split needs each step's own token needs checked: configure-pages reads Pages settings, so it belongs with the deploy
## Files touched
- plugin/tests/test_workflows.py
- .github/workflows/test.yml
- .github/workflows/pages.yml
- CHANGELOG.md
- plugin/lib/fmcode.py
- plugin/tests/test_code_worker.py
