---
id: T-0883
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-15T15:25:29Z
updated: 2026-10-15T16:40:33Z
base: 627409b6fd61467057ce76339939592e86914a16
base_tree: 7d7b4a5e3154530bcb11e3e805d24c4f2d640f03
verified: strong
---
# Guard tests keep their temp folder outside /tmp when ~/.cache doesn't exist, and ~user is checked against the passwd entry
## Raw request
> Guard tests fail when HOME isn't the user's passwd home (HOME=~/.cache/x: credentials under {repo}/config not blocked, ~user expansion, rm -rf ../other allowed) — check whether the guard mixes pwd home and $HOME
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the guard tests pass with a fresh HOME that has no .cache — verify with `env -i PATH=/usr/bin:/bin HOME=~/.cache/fm-fresh-home USER=chase LANG=C.UTF-8 python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] reproduce with a fresh HOME, then fix the harness
## Resume here
## Docs impact
## Verification evidence
- (step 1) `env -i PATH=/usr/bin:/bin HOME=~/.cache/fm-fresh-home USER=chase LANG=C.UTF-8 python3 plugin/tests/run.py test_guard` → exit 0 · Ran 101 tests in 4.4s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree 5a1b0d953946] (2026-10-15T16:38:43Z)
- (ac 1) `env -i PATH=/usr/bin:/bin HOME=~/.cache/fm-fresh-home USER=chase LANG=C.UTF-8 python3 plugin/tests/run.py test_guard` → exit 0 · Ran 101 tests in 4.5s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree 5a1b0d953946] (2026-10-15T16:40:16Z)
- (audit self) `self review: harness creates its non-/tmp base when missing; ~user is checked against the passwd entry; reproduced red with a fresh HOME, green after (101 OK)` → no findings [tree 5a1b0d953946] (2026-10-15T16:40:16Z)
- (audit adversary) `self review: harness creates its non-/tmp base when missing; ~user is checked against the passwd entry; reproduced red with a fresh HOME, green after (101 OK)` → test-only change; the guard itself is untouched, and the fix makes CI exercise the real outside-the-project paths instead of silently testing scratch ones (a fresh-HOME run had 16 guard assertions quietly testing the wrong thing) [tree 5a1b0d953946] (2026-10-15T16:40:20Z)
- (audit self) `self review: harness creates its non-/tmp base when missing; ~user is checked against the passwd entry; reproduced red with a fresh HOME, green after (101 OK)` → no findings [tree 5a1b0d953946] (2026-10-15T16:40:20Z)
## Log
- 2026-10-15T15:25:29Z created
- 2026-10-15T16:38:02Z planned from capture
- 2026-10-15T16:38:03Z focused
- 2026-10-15T16:38:26Z criterion 1 verify: `bash -c 'H=$(mktemp -d -p ~/.cache) && env -i PATH=/usr/bin:/bin HOME=$H USER=$USER LANG=C.UTF-8 python3 plugin/tests/run.py test_guard; r=$?; rm -rf "$H"; exit $r'` → `env -i PATH=/usr/bin:/bin HOME=~/.cache/fm-fresh-home USER=chase LANG=C.UTF-8 python3 plugin/tests/run.py test_guard`
- 2026-10-15T16:40:21Z done
- 2026-10-15T16:40:21Z committed b2cbed8 (1 file)
- 2026-10-15T16:40:33Z includes T-0891: Catch it earlier: local runs always had ~/.cache or XDG_RUNTIME_DIR; CI's fresh HOME is th
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0169 [FIX S, done, 3 steps] Guard: a secret-sounding file name under the scratchpad or /tmp isn't a credential; its real path still is checked — lesson: A name-based h…
- research T-0324-review: Verdict: changes needed.** One fail-open path and two config-clobber paths are verified. I read the code but ran nothing, so each failing input b…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- the similar finished task took 3 steps
## Regression test
none separate: the fix is in the test harness itself. Before it, the same command with a fresh HOME (no ~/.cache) failed (test_guard: FAILED; 16 guard failures in a full run, the temp folder fell back to /tmp, which the guard treats as scratch); after it, 101 OK
## Why not caught
local runs always had ~/.cache or XDG_RUNTIME_DIR; CI's fresh HOME is the first place without either
## Files touched
- plugin/tests/test_guard.py
