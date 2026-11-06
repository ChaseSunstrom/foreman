---
id: T-0965
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-15T21:39:47Z
updated: 2026-10-15T22:49:46Z
base: e061abf300ac742c6f3c02d639b732b0ff1f613c
base_tree: 2373481b191e5954b2a67e2bf07c5156e11f4e28
verified: strong
---
# - The harness hook file has 40+ hook entries, many on every tool call. That is a token and
## Raw request
> - The harness hook file has 40+ hook entries, many on every tool call. That is a token and latency risk Foreman deliberately avoids (MASTER:172), which is worth a doc note
> (noticed by an agent; research T-0964-harness)
## Interpretation
Rivals wire 40+ hooks, many on every tool call. Say in the README how Foreman stays light, so the cost is visible and checkable.
## Assumptions (confidence)
## Acceptance criteria
- [x] README says which hooks run synchronously and where their latency shows — verify with `grep -q 'Stays light' README.md`
## Non-goals
## Approach (options → choice → why)
Options: one README line naming which events run synchronously and where the latency shows (chosen: true today, checkable with fm doctor); a benchmark section (no rival numbers measured here).
## Risks and rollback
## Execution prompt
## Steps
1. [x] README line
## Resume here
## Docs impact
README
## Verification evidence
- (ac 1) `grep -q 'Stays light' README.md` → exit 0 · (no output) [ran] [tree 44d272be8135] (2026-10-15T22:49:43Z)
- (step 1) `grep -q 'Stays light' README.md` → exit 0 · (no output) [ran] [tree 44d272be8135] (2026-10-15T22:49:43Z)
- (audit intent) `self: claims checked against hooks.json (sync entries: PreToolUse, PostToolUseValidate) and the live pane (p95 18 ms)` → one README line; numbers point at fm doctor and the pane [tree 44d272be8135] (2026-10-15T22:49:43Z)
- (audit maintainer) `self: claims checked against hooks.json (sync entries: PreToolUse, PostToolUseValidate) and the live pane (p95 18 ms)` → no number is hard-coded except the observed ~20 ms, which the line attributes to this machine [tree 44d272be8135] (2026-10-15T22:49:43Z)
## Log
- 2026-10-15T21:39:47Z created
- 2026-10-15T22:49:37Z focused
- 2026-10-15T22:49:45Z done
- 2026-10-15T22:49:46Z committed 8ba3214 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0964-harness: 1) **What the harness is.** claude-code-harness is a plan, work, review loop run as skills (`/harness-plan`, `-work`, `-review`, `-sync`, `-rele…
- research T-0964-workflow: Reading of the brief:** Foreman's status below comes from grep hits in `MASTER.md` and `README.md` only. I did not read the code. Many matching…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
## Lessons
- none: a docs line
## Files touched
- README.md
