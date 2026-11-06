**Verdict: changes needed.** There are three MEDIUM defects, all in `plugin/lib/fmgenesis.py`. The LOW items are nits. I read the diff and the code around it. I could not run anything, so none of the findings has a runtime reproducer. Each rests on a code path I traced.

## lens: intent
- MEDIUM — plugin/lib/fmgenesis.py:1275 — The stale check reads the local tree (`_stats_stale(p.root)`), but the push goes to the fetched remote main. If local `stats.json` is dated today and main's is old, `publish` returns "up to date" and the homepage stays stale. This is the situation in this working tree now: `stats.json` shows 2026-10-31 locally but is not on main. If local is stale and main is fresh, every publish does a fetch and a worktree for nothing (line 1288 then returns "up to date"). The `publish` docstring claim "an unchanged tower costs one export and no network" (line 1249) is then false. — Decide staleness on `wt` after the fetch. Skip the fetch by keeping a `stats_day` stamp in `genesis_live` meta, set when main was last seen fresh. — confidence 85%
- MEDIUM — plugin/lib/fmgenesis.py:1897 — `score` treats `checks_same=None` as 0. When one arm's newest long line predates `checks_passed`, a tie on true done is broken on missing data. Foreman 3/8 against a plain line with no checks gives "ahead", and the reverse gives "behind". The row is the deciding scorecard row, so this can flip pass or fail. — Break the tie only when both are non-None; otherwise leave it "level". — confidence 85%
- LOW — plugin/lib/fmgenesis.py:1860-1863 — The `long_row` docstring still says state is decided "on the true-done count". — Mention the checks tie-break. — confidence 90%

## lens: adversary
- LOW — plugin/lib/fmgenesis.py:1275,1288 — `_stats_ok` trusts the local path (own repo, or `fmprove.trusted(p.root)`). The script that runs is `wt/site/stats.py` from the fetched remote main, along with the `plugin/lib` it imports. It runs with the full environment and no sandbox. Content a collaborator merged to main runs under the grant given for the local tree. — Run the local tree's `stats.py` against `wt`, or require the fetched `stats.py` to match local HEAD. — confidence 60%

## lens: edge
- MEDIUM — plugin/lib/fmgenesis.py:81-92 — `_refresh_stats` ignores the exit code, stderr and timeout. If the script fails (no state, a bad `--state`, a 300 s timeout), `publish` records "pushed" or "up to date" and the homepage silently stays stale. That is the user's original complaint. The same stale tree retries every publish, holding the lock for up to 300 s. — Return a reason and put it in `_record` (for example "stats refresh failed: <stderr tail>") so `fm genesis status` shows it. — confidence 80%
- LOW — plugin/lib/fmgenesis.py:1293 — A stats-only push still carries the "Genesis: tower update" message. It also rewrites the `genesis.json` updated/rev fields through `copytree`. — Use a distinct message. — confidence 70%

## lens: operator
- Cost: publish only fires per tower change. The added work per stale publish is one fetch, one worktree and at most 300 s of `stats.py`. That is bounded, but only if the first finding is fixed. Otherwise a local tree that never merges main pays it on every publish.
- The Pages workflow triggers on `site/**` pushes (`.github/workflows/pages.yml:8`) and `build.py` fills the homepage from `stats.json`, so the push is enough to update the site.

## lens: maintainer
- LOW — plugin/tests/test_genesis.py:307-332 — The tests do not cover:
  - an untrusted tree skipping the refresh;
  - a failing or slow `stats.py`;
  - `genesis.json` and `genesis.js` carrying `checks_same`/`checks_total`;
  - a tie where one arm has `None` checks (the second finding).
  Add at least the untrusted-tree and failing-script cases. — confidence 85%
- LOW — The diff base (`335a7fce^`) pulls in T-2332, T-2246 and T-2252 hunks (`fmcore`, `fmguard`, `fmmandate`, `test_goal`, `test_guard`, `READ_CHILD`). These serve no T-2326 step. I did not review them.

## Acceptance criteria
1. Publish regenerates `stats.json` in the same data-only commit and refuses other paths: partly met. The happy path is tested at test_genesis.py:307. The stale-vs-main decision is wrong (first finding) and failure is silent (third). The stray check keeps refusing other paths (fmgenesis.py:1295).
2. Long card carries checks per arm and breaks a true-done tie on them; `genesis.js` shows "checks N of M": met. The data is in fmgenesis.py:1895, the text in fmgenesis.py:1917, the JS in genesis.js:269. The tie-break has the None defect (second finding).
3. Live homepage shows 2026-10-31: not verifiable from the code. `stats.json` is dated today locally, but I couldn't check that it reached main or the live site. The curl check only passes on 2026-10-31.

## Implicit decisions
- Staleness means `generated != date.today()` in local time.
- A stale refresh runs `stats.py --no-bench`, keeping the old hook timings.
- Trust is own repo or `fmprove` trust.
- A refresh failure is swallowed.
- Unknown checks count as 0 in the tie-break.
- The stats commit reuses the tower-update message.
- The scratch-worktree stats run has a 300 s timeout.

## Not checked
The live site, the T-2332, T-2246 and T-2252 hunks, MASTER.md (left out of the diff as generated), and a full read of `site/stats.py`'s helpers.

**Noticed:** none
