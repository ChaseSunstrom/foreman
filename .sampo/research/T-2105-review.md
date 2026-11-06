**Verdict** — changes needed. The confirm task shows the user a false reason, and nothing tests the site export that AC3 relies on. Both fixes are small.

## lens: intent
- MEDIUM — ~/.claude/foreman/plugin/lib/fmscout.py:340 — `capture` sets `meta["confirm"]` but not `confirm_why`. `plan_gaps` then falls back to "a child found this request in an old session" (fmcore.py:2616), which is false for 'Start Genesis here?'. Fix: set `b.meta["confirm_why"]` from the finding, as fmbench.py:907 does, and assert it in `GenesisPropose`. Confidence: high.
- LOW — ~/.claude/foreman/plugin/lib/fmhooks.py:3277 — the scout idle run fires only under full autonomy, so under standard autonomy Genesis never offers itself automatically. AC1 only covers full, but the README wording "offers itself" implies more. Fix: say "under full autonomy, or on `fm scout`" in the README and SKILL.md. Confidence: medium.

## lens: adversary
- No findings. The probe reads local briefs only. The confirm gate holds under every autonomy level, and `_drive` skips tasks that wait on the user.

## lens: edge
- LOW — ~/.claude/foreman/plugin/lib/fmscout.py:105 — blocked and deferred tasks don't count as "open". `probe_brainstorm` holds the queue for them and this probe doesn't, so Genesis can be offered with parked work still waiting. Fix: decide it on purpose, either keep it and note it in the probe docstring or match `probe_brainstorm`. Confidence: medium.
- LOW — ~/.claude/foreman/plugin/lib/fmgenesis.py:400 — the export verdict regex `^Verdict: (\w+)` ignores the staleness rule `step` applies at line 291. The site can show a clean drift or sweep verdict that `step` treats as stale. Fix: reuse the staleness check, or label the verdict "as written". Confidence: medium.

## lens: operator
- LOW — ~/.claude/foreman/plugin/lib/fmhooks.py:3283 — the idle reason "Plan it and work it (fm next)" is wrong for a confirm item, which needs a yes first. Fix: add a confirm branch that says "ask the user (fm ask ID confirm)". Confidence: medium.
- LOW — ~/.claude/foreman/plugin/lib/fmscout.py:104 — `probe_genesis` calls `load_briefs(include_archive=True)` on every scout run, even after the key is spent. I couldn't measure the cost of loading the archive, but it grows with history: 813 archived briefs here. Fix: check `scout_keys` for `genesis:start` first and return [] before loading. Confidence: medium.

## lens: maintainer
- MEDIUM — ~/.claude/foreman/plugin/tests/test_genesis.py — nothing tests the export's drift and sweep verdicts or the `genesis.js` changes, though AC3 says the site shows each generation's verdicts. A regression there would pass the suite. Fix: add a test that `export` gives verdict keys "clean" and "red" for a drift and a sweep file, and that `genesis.js` contains the strings it reads. Confidence: high.
- LOW — ~/.claude/foreman/plugin/lib/fmgenesis.py:302 — the three-reverted breaker only affects `step`. `fm genesis seed` isn't blocked while stopped, so the stop is advisory. SKILL.md also says "seed N" in one place and "seed N+1" in another, and "until done, stopped or blocked" in one place and "blocked: work the rest of the queue" in another. Fix: pick one wording, and document that `seed` is not blocked. Confidence: medium.

## Acceptance criteria
- AC1: met. `probe_genesis` gates on open tasks, an existing gen-0 and fewer than 10 done. The confirm gate holds at every autonomy level, and the key is captured once through `scout_keys`. I did not run the tests.
- AC2: met. The breaker returns kind "stopped" after three consecutive `- reverted` verdicts, and `_next_for` says "Genesis stopped at gen N". I did not run the tests.
- AC3: partly verifiable. The skill file, the README and MASTER entries and the `test_docs` registration are all in the diff. The site's drift and sweep verdicts are untested (see maintainer).

## Implicit decisions
- Blocked and deferred tasks don't hold the queue.
- The done count includes archived briefs.
- One offer ever, keyed `genesis:start`.
- Scout sets the finding at tier L and type FEATURE.
- There is no `propose` verb and no rules routing line. This follows the fm decide recorded on T-2105.
- The breaker counts only `- reverted` verdicts in lineage.md.

## Not checked
- I ran no tests.
- I did not see the site page rendered.
- I did not review the generated MASTER.md diff.
- I could not measure the archive load cost.

Noticed: `fm genesis seed` isn't blocked while the tower is stopped, so the breaker is advisory.
Noticed: the Stop-hook reason text "Plan it and work it" suits ordinary tasks, not confirm items.
