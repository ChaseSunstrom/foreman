## Verdict
Approve with nits. The feature meets the acceptance criterion in code. I did not run the tests, because I only had read tools. There are no HIGH findings.

## lens: intent
- MEDIUM — plugin/lib/fmrisk.py:~124-126 — `fm risk` text prints only the rule and the rewrite. `fmguard._hint` (fmguard.py:169-203) returns "" for most rules, for example any plain `core:path-py` block. Those rows read `1× core:path` with no rewrite and no detail, so the user can't tell what to change. The request was "with the rewrite that passes". — When `rewrite` is empty, print `c.fit(h["detail"], 100)` (already computed) instead. — confidence 85%.
  - file: plugin/lib/fmrisk.py; line: 125; short_summary: "Rows with no hint show neither rewrite nor detail"; failure_scenario: a rule hit 5 times that has no `_hint` branch prints `5× core:path-py` and nothing else; category: incomplete-feature; verdict: CONFIRMED.

## lens: operator
- MEDIUM — plugin/lib/fmrisk.py:~91 and fmhooks.py:623 — The SessionStart line is capped at 420 characters, but `CTX_BUDGET` is 2000 (fmhooks.py:22). That is 21% of the budget. The line sits in `tail`, which every fallback tier keeps. When the text is over budget, the map, "Resume here" and the queue are dropped first to make room. The request said "one short line". The line repeats on every SessionStart source (startup, resume, compact, clear) for 7 days after a rule's third hit, with no decay. — Keep only the first sentence of the rewrite and drop "(last: …)". That gives about 200 characters. — confidence 75%.
  - file: plugin/lib/fmrisk.py; line: 91; short_summary: "Collision line can take 420 of 2000 context chars"; failure_scenario: the top rule is the python-pipe hint (about 450 characters), so the line is 420 characters, a project with a long queue loses its map and queue tiers at every SessionStart; category: context-budget; verdict: PLAUSIBLE.
- LOW — plugin/lib/fmrisk.py:75 — The comment says "a quiet week costs no import". In practice almost every week has a block, so every SessionStart now imports `fmguard`. Before this change it was never imported on that path. `fmguard` has 89 `re.compile` calls. I did not measure the cost. — Measure it, or move the hint text into a small shared table. Reword the comment. — confidence 60%.

## lens: maintainer
- MEDIUM — plugin/tests/test_risk.py:108-135 — Nothing tests the 7-day window. Deleting `since=since` in `collisions()` leaves the test green, because every event is fresh. The `?` and category fallback when `rule` is missing is also untested. — Append a ledger line with a `ts` 8 days old, since `log_event` can't set `ts`. Assert it is excluded. Add one event with no `rule`. — confidence 90%.
  - file: plugin/tests/test_risk.py; line: 108; short_summary: "7-day window and rule-less fallback untested"; failure_scenario: remove the `since` filter and the whole suite still passes; category: test-coverage; verdict: CONFIRMED.
- LOW — plugin/tests/test_risk.py:116 — The test uses `core:path`. The guard's real `rule_id` makes `core:path-py` for a `.py` file (fmguard.py:106-108). The fixture isn't a rule the guard can emit. — Use a real rule name. — confidence 70%.

## lens: adversary: ok
The `detail` text is redacted, defanged and fitted. The `rule` comes from `[a-z]+` words in `rule_id`, and the rewrite is static text.

## lens: edge: ok
- LOW — plugin/lib/fmguard.py:188-202 — `_hint` runs on the ledger's `detail[:200]` (fmhooks.py:1792). The `endswith(...)` hints can miss when a long path pushes the suffix past 200 characters. I have no reproducer.

## Acceptance criteria
- Collisions in `fm risk` (text and JSON) and a SessionStart line at 3+ hits, nothing at 2: met in code. The test covers the 2-hit and 3-hit cases, both outputs and JSON. I did not run it.

## Implicit decisions
- The window is a rolling 7 days (UTC), not calendar days.
- Only the top rule is named at SessionStart.
- Rules group by the guard's `rule_id`, falling back to the category.
- The newest event's detail decides the rewrite.
- `fm risk` text shows the top 8 rules and cuts the rewrite at 160 characters.
- "Spends risk" is read from the newest event's category.

## Not checked
I did not run the tests or time the `fmguard` import. I did not check `fm risk` JSON consumers (UI or pane).

**Noticed:** CHANGELOG and MASTER entries are fine. `fmrisk.collisions` is not memoized the way `status` is, which only matters if more callers appear.
