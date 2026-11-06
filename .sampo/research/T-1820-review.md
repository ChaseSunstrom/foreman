**Verdict:** approve with nits. The 2× pricing is correct and applied everywhere. The "what to change" half of the request is not built.

## lens: intent
- MEDIUM — plugin/lib/fmcost.py:724-725 — The request was "each with its cost and what to change", and no remediation text exists anywhere in the diff. The AC and the CHANGELOG entry both drop that half silently. The output now gives only a cause and a number. Fix: after the cause, add a short hint per cause. A ttl bust gets "keep the session warm or use the 1 h cache". A context edit gets "stop editing CLAUDE.md, tools or MCP mid-session". Or log the cut as a Non-goal and capture it. — high
- LOW — plugin/lib/fmcost.py:725 — `≈ 86k` carries no unit. It sits after the cause list and reads as a token count or a dollar figure. It is actually input-equivalent tokens, upper-bounded as `w × (price − 0.1)`. Fix: write `… ≈ 86k input-equivalent lost`. — high

## lens: edge
- LOW — plugin/lib/fmcost.py:700 — The expired cache was written by the previous turn, but the TTL is picked from the bust row's own `h`. A session that moves from the 5 min cache to the 1 h cache (after a restart or a setting change) shows its first 1 h write after a 10-minute gap as "context edit". The previous cache was 5 min and had expired, so this should be "ttl". The reverse mix also misreads. Fix: keep `prev_h` on the row and use `CACHE_TTL_1H_S if r["prev_h"] else CACHE_TTL_S`. — medium

## lens: maintainer
- LOW — plugin/tests/test_economics.py:42-63 — The new test covers only the 1 h session's warm side (10-minute gap, "context edit"). A 1 h session with a gap over an hour should be "ttl", and nothing tests it. If `CACHE_TTL_1H_S` were mistyped, the test would still pass. Fix: add a fourth row to the fixture. — high
- LOW — plugin/tests/test_economics.py:42-63 — The `weighted()` unit assertion covers the shared helper, but `fmbudget.transcript_tokens`, `fmserve._session_tokens` and `cmd_digest` are not exercised with 1 h rows. They route through `weighted`, so the risk is low. — medium

## lens: operator
- No findings. `fmbudget.WEIGHTS` was removed, and my grep found no other reader of it. `fmbudget`'s lazy `import fmcost` avoids loading the module on every hook start and does not create an import cycle. Added work per message is one dict lookup. My grep of `plugin/lib` found no other place that sums input-equivalent tokens.

## lens: adversary
- No findings. The only input is local transcript JSON. A non-numeric `ephemeral_1h_input_tokens` would raise TypeError, but the old `(u.get(k) or 0) * w` raised the same way for the other fields.

## Acceptance criteria
- 1 h writes weigh 2× everywhere input-equivalent is summed: met. `weighted()` is used in cost, task_costs, unexplained, digest, serve and budget (the diff), and my grep found no other sum.
- A 1 h session's 10-minute-gap bust is a context edit: met, by the new test (gap 600 s, limit 3600 s).
- Each session names its busts' cost: met as a per-session total, not per bust, and without units (see above).
- I did not run `python3 plugin/tests/run.py -k SessionCost -k test_cost_labels_each_cache_bust`. I traced the test's arithmetic by hand and it matches, including the `≈ 86k` rounding of 85500.
- The existing `test_ideas.py:274` substring `2 busts (1 context edit, 1 ttl)` still matches, because the new text is appended after the `)`.

## Files vs steps
- All hunks serve steps 2 and 3. `test_economics.py` has no step but is the expected test for the change.

## Implicit decisions
- The 1 h price is 2.0 (`WRITE_1H`), hardcoded and not model-aware.
- Bust cost is `rewritten × (price − 0.1)`, assuming all of it would otherwise have been read.
- The tier is detected from `cache_creation.ephemeral_1h_input_tokens > 0` on that one row.
- `bust_cost` is a new JSON key, in input-equivalent tokens.
- `weighted()` lives in `fmcost` and `fmbudget` imports it lazily.

## Not checked
- I did not run the test suite.
- I did not confirm that the "about 10% cheaper" figure in the CHANGELOG matches real transcripts.
- I did not check MASTER.md for any mention of the pricing weights beyond a grep for `1.25`.

Noticed: `_sessions` in plugin/lib/fmcost.py (lines 687-730) now has a dict-literal line over 150 characters (line 714) and mixes pricing logic into the row-building loop; worth splitting out a `_price_row` helper.
