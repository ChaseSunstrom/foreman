Verdict: approve with nits (tests not run by the reviewer).

## lens: adversary
- MEDIUM (plausible) — fmgenesis.health / fmmcp exam_scorecard — held-out results reach sessions on every surface. RESOLVED: the shared line carries only aggregate N/M pass and the Haiku count, never scenario ids; the tool description says it is the done gate for the user; recorded with fm decide (same data is one fm exam scorecard call away).
- LOW — fmgenesis.health — os.stat(__file__) outside a try could raise out of health(). FIXED: try/except OSError, falls back to 0.
- Dismissed by the reviewer: sha1 is a cache key; g["exam"] is built from integers then plain+defang; MCP output is c.redact'd and the sensitive gate runs first; fixed argv, no properties; exam.jsonl is in the tower dir so the cache refreshes.

## Acceptance criteria
- MCP tool: met, tested. Genesis line: met, tested in fm state and fm ui. Refresh after an update: met for fmgenesis.py; step() lives there, so that is the file whose change alters the line.

## Implicit decisions
- exam part omitted with no graded or Haiku line; exam_scorecard reports foreman at bar 0.8; an exception in _exam_count drops only that part; exit 1 is an answer.
