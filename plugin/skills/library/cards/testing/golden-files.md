---
name: golden-files
title: Golden files
area: testing
tags: [golden, fixtures, testdata, update-flag, diff, cli]
detect: [file:testdata/*.golden, file:*.golden, file:golden/*, dep:pytest-golden, dep:goldie]
related: [snapshot-testing, regression-tests, characterization-tests]
---
Golden files hold expected output on disk (rendered text, CLI output, generated code) compared byte for byte, with an explicit update switch.

## Verify
- `go test ./... -run TestRender`: output matches `testdata/*.golden`.
- `go test ./... -update`: regenerates goldens when the test defines an `update` flag; then `git diff testdata` shows the change.
- `git status --porcelain testdata`: no stray or uncommitted golden after a run.

## Test first
Produce actual output, compare with the file, print a diff on mismatch, and gate regeneration behind a flag.
```go
var update = flag.Bool("update", false, "rewrite golden files")

func TestRenderReport(t *testing.T) {
	got := Render(sampleReport())
	path := "testdata/report.golden"
	if *update { os.WriteFile(path, got, 0o644) }
	want, _ := os.ReadFile(path)
	if !bytes.Equal(got, want) { t.Errorf("mismatch:\n%s", diff(want, got)) }
}
```
Goldens live in `testdata/` next to the test, one per case.

## Do
- Make inputs and output deterministic: fixed time, seeded random, sorted maps, stable newlines.
- Gate rewriting behind an explicit flag or env var; never write on normal runs.
- Show a readable unified diff on failure, not just "not equal".
- Name goldens after the case and keep one file per case in a subdirectory.
- Review the golden diff in the PR like source.
- Normalize platform differences (path separators, CRLF) before comparing.
- Store binary or large outputs sparingly; compare structured parts when you can.

## Avoid
- Auto-updating goldens in CI or on every run: the test can never fail. Update only locally, deliberately.
- Goldens containing timestamps, absolute paths or hostnames: fail on other machines. Scrub them.
- One giant golden for many cases: any change fails everything. Split per case.
- Generating the expected file with the code under test and never reading it: it may pin a bug. Inspect the first golden by hand.
- Missing golden treated as empty: a typo passes. Fail when the file is absent.
- Trailing-newline or encoding drift from editors: set `.gitattributes` to preserve bytes.

## Review
- [ ] Update path is explicit and off by default.
- [ ] Goldens contain no environment-specific data.
- [ ] A failing run prints a useful diff.
- [ ] Golden changes in the PR were read and are intended.
- [ ] Missing golden fails the test.
