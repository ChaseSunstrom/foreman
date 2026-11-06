---
id: T-1804
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T01:37:22Z
updated: 2026-10-28T01:47:23Z
base: d5abfe078f39933452e9e83ab558b5754233d22a
base_tree: 44414e4c55d7ddcf2b8f8c632b316d9e9aaefe89
plan0_at: 2026-10-28T01:46:56Z
plan0_scope: []
verified: strong
---
# CI actions on Node 24 majors
## Raw request
> CI actions pinned to Node 20 majors (checkout v4, setup-python v5, pages actions): bump the pinned SHAs before runners drop Node 20
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] workflows use Node 24 action releases pinned by SHA — verify with `! grep -nE 'checkout@11d5960a|setup-python@a26af69b|upload-pages-artifact@56afc609|configure-pages@983d7736|deploy-pages@d6db9016' .github/workflows/*.yml`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] bump the five pinned actions to Node 24 releases at least two weeks old
## Resume here
## Docs impact
## Verification evidence
- (step 1) `! grep -nE 'checkout@11d5960a|setup-python@a26af69b|upload-pages-artifact@56afc609|configure-pages@983d7736|deploy-pages@d6db9016' .github/workflows/test.yml .github/workflows/pages.yml` → exit 0 · (no output) [ran] [tree a7bb882d4687] (2026-10-28T01:47:06Z)
- (ac 1) `! grep -nE 'checkout@11d5960a|setup-python@a26af69b|upload-pages-artifact@56afc609|configure-pages@983d7736|deploy-pages@d6db9016' .github/workflows/*.yml` → exit 0 · (no output) [ran] [tree a7bb882d4687] (2026-10-28T01:47:16Z)
- (audit intent) `main-thread review: SHAs resolved from the actions' own tag refs (annotated tags dereferenced), releases 5+ weeks old; release notes scanned for breaking changes: setup-python v7 drops pip-install (unused) and EOL Pythons (we use 3.12/3.14); upload-pages-artifact v4+ skips dotfiles (site/build.py writes none)` → every action in both workflows now runs on Node 24, pinned by SHA with its version in the comment [tree a7bb882d4687] (2026-10-28T01:47:16Z)
- (audit operator) `main-thread review: SHAs resolved from the actions' own tag refs (annotated tags dereferenced), releases 5+ weeks old; release notes scanned for breaking changes: setup-python v7 drops pip-install (unused) and EOL Pythons (we use 3.12/3.14); upload-pages-artifact v4+ skips dotfiles (site/build.py writes none)` → pages deploy is outward; the bump keeps inputs unchanged and the next push to main exercises both workflows [tree a7bb882d4687] (2026-10-28T01:47:16Z)
- (audit self) `main-thread review: SHAs resolved from the actions' own tag refs (annotated tags dereferenced), releases 5+ weeks old; release notes scanned for breaking changes: setup-python v7 drops pip-install (unused) and EOL Pythons (we use 3.12/3.14); upload-pages-artifact v4+ skips dotfiles (site/build.py writes none)` → no findings [tree a7bb882d4687] (2026-10-28T01:47:16Z)
## Log
- 2026-10-28T01:37:22Z created
- 2026-10-28T01:46:54Z set status=captured
- 2026-10-28T01:46:54Z planned from capture
- 2026-10-28T01:46:55Z focused
- 2026-10-28T01:47:20Z done
- 2026-10-28T01:47:23Z committed b4c1e45f (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research ask-for-a-tauri-2-app-built-with-bun-what-do-20261006-0037: Asked 2026-10-06 · 2 sub-question(s) · 16 claims: 5 quote found, 6 quote not found, 5 unchecked. ✓ m…
- T-1245 [SECURITY S, done, 2 steps] Pages workflow: build job with contents read only, deploy job with pages and id-token write; every action in both workflows pinned to …
- T-1407 [FEATURE M, done, 1 steps] Toolchain activation: before workers and checks, fm code activates the project's pinned to — lesson: Ask a version manager where an ins…
- decision 2026-10-21: fm code's no-setup default picks only a runner whose read-only mode is verified here (claude); codex/gemini plan only when named, with a note
- similar finished tasks took 1–2 steps
## Why not caught
none: a deprecation warning on runners, not a failure; it surfaced in CI annotations
## Lessons
- pin GitHub actions by SHA from git/ref/tags (dereference annotated tags), never a tag younger than two weeks
## Files touched
- .github/workflows/pages.yml
- .github/workflows/test.yml
