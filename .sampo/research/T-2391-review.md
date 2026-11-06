T-2391 review (fm-reviewer, one pass): changes needed; fixed in f2f89238 before merge, test-first.
MEDIUM fixed: typed/red/inconclusive upgrades fell back to --run 'true' (a vacuous green that cleared the row): no fallback; empty or lint_verify-flagged commands read 'waiting: needs a check that can fail'.
MEDIUM fixed: clear patterns matched anywhere (echo prove --docs cleared docs; pytest test_schema.py cleared data): matched from the first word after env assignments; a pipe or || true clears nothing; the green run must follow the last touch of the row's files.
MEDIUM fixed: a git timeout memoized 'no claims' forever: not memoized on failure.
LOW fixed: _VACUOUS_RUN anchored; no-base docs read unknown; raw perf medians; cache keyed on done briefs, only the 30-day window written, cold timing in --json; renderers called with a stub instead of a source grep.
Open: one-second touch timestamps treat same-second edits as proven; the cache misses later edits to a done task's files until the next done-brief change or day.
