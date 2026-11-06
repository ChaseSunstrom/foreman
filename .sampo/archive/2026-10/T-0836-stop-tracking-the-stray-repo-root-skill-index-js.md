---
id: T-0836
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T18:48:28Z
updated: 2026-10-14T19:32:15Z
base: af240341e0090ec6e80b2075bdab01d800664ff8
base_tree: e11ce2e8019cbf7c432fd9c5460485f625d079ef
verified: strong
---
# Stop tracking the stray repo-root skill-index.json (a cache with local home paths, unused since the index moved to state) and ignore it
## Raw request
> Stop tracking the stray repo-root skill-index.json (a cache with local home paths, unused since the index moved to state) and ignore it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] skill-index.json is untracked and ignored, and no tracked file names a local home path — verify with `test -z "$(git ls-files skill-index.json)" && git check-ignore -q skill-index.json`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] git rm --cached, .gitignore line, check no reader uses the root copy
## Resume here
## Docs impact
none: .gitignore line
## Verification evidence
- (step 1) `test -z "$(git ls-files skill-index.json)" && git check-ignore -q skill-index.json && test -z "$(git grep -I -l ~)"` → exit 0 · (no output) [ran] [tree b96d282267ff] (2026-10-14T19:31:37Z)
- (ac 1) `test -z "$(git ls-files skill-index.json)" && git check-ignore -q skill-index.json` → exit 0 · (no output) [ran] [tree b96d282267ff] (2026-10-14T19:32:15Z)
- (audit edge) `self: the root copy was a stray cache from a manual 'Update' commit (10-05); fmplugins writes the index under the project's state dir, nothing reads the root file; no tracked file names a local home path now` → history keeps the old file in the public repo; rewriting a public branch's history is destructive and left alone [tree b96d282267ff] (2026-10-14T19:32:15Z)
- (audit self) `self: the root copy was a stray cache from a manual 'Update' commit (10-05); fmplugins writes the index under the project's state dir, nothing reads the root file; no tracked file names a local home path now` → no findings [tree b96d282267ff] (2026-10-14T19:32:15Z)
## Log
- 2026-10-14T18:48:28Z created
- 2026-10-14T18:48:28Z focused
- 2026-10-14T19:31:31Z user approved core in Claude Code's permission prompt
- 2026-10-14T19:32:15Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0018-r3-operator: 3","isSidechain":true,"agentId":"a8c97e63300d81c73","message":{"model":"claude-sonnet-5","id":"msg_011CfSRu7Xczh871gZj2Mqhv","type":"message"…
- research claude-code-features-20261014: Foreman uses: 14 hook events, 4 async hooks, 6 agents (tools/model/color only), output style, statusline.
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
- similar past tasks were L: consider --tier L
- the similar finished task took 3 steps
## Lessons
- A cache written next to the code can be committed by a blanket 'Update'; keep caches under state/ and ignore stray ones by name
## Files touched
- .gitignore
- skill-index.json
