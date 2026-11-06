# T-1838 review (fm-reviewer, one pass): approve with nits
- MEDIUM intent: cmd_route read b.meta.get("type") not Brief.type -> fixed (b.type), test red on old code.
- MEDIUM maintainer: live-library threshold test gave totals only -> names misses, asserts labelled books exist.
- LOW intent: held-out not asserted, --task untested -> tuned 13/8 and held 4/1 asserted separately (were 12/7, 3/0); CLI --task test.
- LOW intent: no CHANGELOG entry -> added.
- LOW edge: scan fallback would fail the test -> skips without FTS5.
- LOW edge: fm which past BIG queries the first 8 words -> accepted, noted in MASTER (a task's title comes first).
- adversary/operator: ok.
