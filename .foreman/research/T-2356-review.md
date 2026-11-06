T-2356 review (fm-reviewer, one pass): changes needed; fixed in af7ed840 before merge.
MEDIUM fixed: issue titles and labels went through c.plain only into model context and a CONTEXT: line: c.defang(c.redact(c.fit(...))).
MEDIUM fixed: the docstring claimed the timer runs --tick (it didn't): reworded; the timer is T-2357's (now depends on T-2356 and T-2374); a nonexistent 'fm night --install' reference removed.
MEDIUM fixed: daily [outward] rows per kind and repo showed as pending user items in fm todo for 7 days: routine polls are only night_tick events; fm decide --review lists the fetches.
LOW fixed: a per-day cap of 20 issues per repo; corrupt tick.json coerced, listing and log in finally; lock contention, --repo argv and night_tick events tested.
Clean per review: gh argv only for _REPO-matched approved repos, no shell, body defanged/quoted, sweep detached with a non-blocking lock, no model tokens, NO_NET and sensitive gate every remote read.
Open: nothing writes meta.watch until T-2357, so the watches are inert until then.
