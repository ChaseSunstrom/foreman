---
name: snapshot-testing
title: Snapshot testing
area: testing
tags: [snapshot, jest, insta, syrupy, regression, review]
detect: [dep:syrupy, dep:insta, dep:jest-snapshot, file:__snapshots__/*, file:*.snap, file:*.snap.new]
related: [golden-files, visual-regression, unit-test-design]
---
Snapshots pin serialized output and flag any change; useful only when small, deterministic and reviewed like source.

## Verify
- `npx jest --ci`: fails instead of writing missing snapshots, so CI never silently records new ones.
- `pytest -q --snapshot-update` (syrupy) then `git diff`: shows exactly what changed; review before committing.
- `cargo insta test` then `cargo insta review`: Rust snapshot diffs are accepted one by one (needs cargo-insta).
- `git diff --stat -- '*.snap' '__snapshots__'`: snapshot churn in the PR is intended and small.

## Test first
Snapshot a small, stable value; scrub the volatile parts.
```ts
test("renders invoice summary", () => {
  const out = render(invoice({ id: "fixed", date: new Date("2024-01-01") }));
  expect(out).toMatchInlineSnapshot(`
    "Invoice fixed - 2024-01-01 - $10.00"
  `);
});
```
Stored snapshots live in `__snapshots__/` (Jest, syrupy) or `snapshots/` (insta); inline ones sit in the test.

## Do
- Snapshot the smallest meaningful structure (a function result, one component), not a page.
- Prefer inline snapshots for short output so the expectation is in the test.
- Normalize volatile fields: timestamps, ids, random values, absolute paths, ordering.
- Review snapshot diffs in the PR as carefully as code.
- Name tests for the behavior; delete obsolete snapshots (`jest --ci` reports them, `-u` removes).
- Use explicit assertions for the properties that matter, and snapshots for the rest.

## Avoid
- Running `jest -u` or `--snapshot-update` to make red go green: it blesses a bug. Read the diff first.
- Huge component or DOM snapshots: nobody reviews them, and they fail on every change. Shrink the target.
- Unscrubbed dates, uuids, hashes: flaky snapshots. Freeze time and inject ids.
- Snapshots of objects with unstable key order or floats: serialize deterministically, round numbers.
- Committing `.snap.new` or pending files: accept or discard them.
- Using snapshots as the only test: they say "changed", not "wrong". Add an assertion for the key behavior.

## Review
- [ ] Each snapshot is small enough to read in the diff.
- [ ] No volatile value (time, id, path) is stored.
- [ ] Updated snapshots were reviewed and match the intended change.
- [ ] No obsolete or pending snapshot files are committed.
- [ ] Key behavior also has an explicit assertion.
