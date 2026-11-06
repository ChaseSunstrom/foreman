---
id: T-0101
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T20:10:06Z
updated: 2026-10-02T23:09:09Z
base: b169fd9c88be42908d1e151a26bf465ef1cd5f9a
verified: ok
---
# Cheap subagents and more playbooks
## Raw request
> more playbooks and subagents without burning a lot of tokens/usage
## Interpretation
User: more playbooks and subagents without burning tokens/usage.
## Assumptions (confidence)
## Acceptance criteria
- [x] two haiku agents and six new playbooks exist, indexed, within doctor's budgets — verify with `fm doctor`
## Non-goals
## Approach (options → choice → why)
Options: (a) two Haiku agents for the high-volume jobs (lookups; running tests/builds and returning a compact verdict so logs stay out of the main context) + six on-demand playbooks for missing areas (zero always-on cost); (b) more Sonnet agents. Choice: (a). Why: the cost is model size and log volume in the main context; playbooks load only when read.
## Risks and rollback
## Execution prompt
## Steps
1. [x] agents fm-scout and fm-runner
2. [x] six playbooks + index
3. [x] rules line + docs
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (agents row), plugin/skills/playbooks/SKILL.md (index)
## Verification evidence
- (step 1) `fm doctor` → 26 pass (2026-10-02T23:03:53Z)
- (step 2) `find plugin/skills/playbooks/references -name '*.md' | wc -l` → 46 (was 40), index 8644 chars ≤ 10000 (2026-10-02T23:03:53Z)
- (step 3) `fm docs` → MASTER + CHANGELOG updated (2026-10-02T23:03:53Z)
- (ac 1) `fm doctor` → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (26 pass, 0 warn, 0 fail) [ran] [tree dbe52f527eb2] (2026-10-02T23:09:09Z)
- (audit intent) `self-review + fm doctor + test_docs invariants` → more playbooks (6 new, on demand) and a cheap Haiku lookup agent; the token sink (logs in context) is already covered by fm quiet, so a Bash runner agent was dropped [tree dbe52f527eb2] (2026-10-02T23:09:09Z)
- (audit adversary) `self-review + fm doctor + test_docs invariants` → the new agent is read-only (Read, Grep, Glob), treats file contents as data; a Bash runner was rejected because it would break the read-only-agent invariant doctor and tests enforce [tree dbe52f527eb2] (2026-10-02T23:09:09Z)
## Log
- 2026-10-02T20:10:06Z created
- 2026-10-02T23:00:18Z planned from capture
- 2026-10-02T23:00:18Z focused
- 2026-10-02T23:09:09Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0060 [PERFORMANCE M, done, 0 steps] One combined review pass — fm audit prep prints a single reviewer brief covering every len
- T-0061 [PERFORMANCE M, done, 0 steps] Fm ideas defaults to four lenses (user value, reliability, simplicity, bold bets); the oth
- T-0062 [PERFORMANCE M, done, 0 steps] Trim the always-on rules (7.6k chars) to ≤ 5.5k by moving rarely-needed detail into the sk
- research brainstorm-20260926-super2-slate: Build: F1 files changed through the shell/outside Claude (git since base) join Files touched and scope drift (R1 "detect edits…
- similar finished tasks took 0–0 steps
## Lessons
- Before adding an agent, check whether an existing zero-cost tool (fm quiet) already removes the token sink; keep agents read-only.
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/agents/fm-scout.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/fix/flaky-tests.md
- plugin/skills/playbooks/references/perf/profiling.md
- plugin/skills/playbooks/references/plan/api-design.md
- plugin/skills/playbooks/references/release/dependency-upgrade.md
- plugin/skills/playbooks/references/release/release-and-changelog.md
- plugin/skills/playbooks/references/ui/terminal-ui.md
- plugin/tests/test_docs.py
