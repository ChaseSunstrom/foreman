---
id: T-0074
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-09-27T04:34:42Z
updated: 2026-10-02T19:01:08Z
base: 849ee3f68d6e3bcf639251779bfd42bb98344b58
done_in: T-0088
---
# sensitive() ignores regex/string literals and 'guard' in paths
## Raw request
> sensitive() flags Foreman's own regex literals (shell=True, eval( inside patterns) and any path containing 'guard'; consider matching added code only outside string literals
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] eval( / shell=True inside a string literal on an added line is not flagged; real eval( still is (guard paths stay flagged: a guard is security code) — verify with `python3 -m unittest discover -s plugin/tests -p test_round_i.py -q`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red test  <- CURRENT
2. [ ] strip string literals before matching added lines; drop bare guard from path regex
## Resume here
<!-- auto -->
- 2026-10-02T18:36:39Z step 1/2: red test
- git: foreman/build; 1 uncommitted: plugin/tests/test_round_i.py
- touched since last checkpoint: plugin/tests/test_round_i.py
## Docs impact
## Verification evidence
## Log
- 2026-09-27T04:34:42Z created
- 2026-10-02T18:34:52Z planned from capture
- 2026-10-02T18:35:35Z focused
- 2026-10-02T18:35:46Z steer: keep 'guard' paths sensitive — fmguard and auth guards are security code; fix literals only
- 2026-10-02T18:36:53Z paused: focus moved to T-0084
- 2026-10-02T19:01:08Z done in T-0088
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0018-r2-edge: ect, not just the offending one. Fix: `gates = {shape(x) for x in (c.read_meta(p).get(\"checks\") or []) if isinstance(x, str)}`, and/or wrap `ch…
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- research t0018-r3-adversary: `). `_read` (fmsync.py:31-33) does a plain `open(path)`, which follows the symlink. The `decisions.md` (fmsync.py:109-114) and `research/*.m…
- research t0018-r1-maintainer: "fm: {e.args[0] if e.args else e}\"` — for a `KeyError('intent')` that prints exactly `fm: intent`, which reads like a value, not an error,…
