---
name: changelogs
title: Changelogs and release notes
area: docs
tags: [changelog, releases, semver, conventional-commits, keep-a-changelog]
detect: [file:CHANGELOG.md, dep:semantic-release, dep:standard-version, dep:@changesets/cli, dep:release-please, dep:towncrier]
related: [api-docs, docs-as-code, readme-writing, adrs]
---
Changelogs for humans: one entry per notable change, grouped by type, newest first, linked to versions, with breaking changes and migrations called out.

## Verify
- `git log --oneline vPREV..HEAD`: the commits since the last release are what the new entry must cover (replace vPREV with the real tag).
- `grep -n "^## " CHANGELOG.md | head`: the newest version heading is on top, with an Unreleased section above it if used.
- `npx changeset status`: pending changesets exist for changed packages (when Changesets is in use).
- `towncrier build --draft`: the news fragments render into the expected release notes (when towncrier is in use).

## Test first
Before cutting a release, write the entry for the user-visible change and check it names the effect.
```md
## [Unreleased]
### Changed
- BREAKING: `parse()` now raises `ParseError` instead of returning `None`.
  Migrate by catching `ParseError`.
```
If the line cannot say what changes for a user, the change is not ready to release.

## Do
- Follow one format. The common one is a heading per version with the date (`## [1.4.0] - 2026-10-15`), newest first, sections Added, Changed, Deprecated, Removed, Fixed, Security.
- Write entries from the user's perspective: what they see or must do, not what files changed.
- Keep an Unreleased section updated in the same pull request as each change, or use per-change fragments (changesets, towncrier) to avoid merge conflicts.
- Mark breaking changes clearly and include migration steps or a link to them.
- Follow semantic versioning: breaking change means major, new feature means minor, fix means patch.
- Link each version heading to its compare view or tag, and tag the release commit with the same version.
- Name the issue or pull request number at the end of an entry where one exists.
- If you generate from conventional commits, review and edit the output before publishing.

## Avoid
- Dumping `git log` as the changelog: it is noise to readers. Curate user-visible changes only.
- Burying breaking changes in Fixed or Changed: users upgrade blind. Prefix BREAKING and add migration steps.
- Entries like "misc fixes" or "improvements": no information. Say what and where.
- Dates in ambiguous formats: use ISO 8601 (`2026-10-15`).
- Editing old release entries silently: history lies. Add a correction note in the next release.
- Version in the changelog differing from the package manifest or tag: confusion. Release all three together.

## Review
- [ ] Each entry says the user-facing effect in plain words.
- [ ] Breaking changes are labelled with a migration path.
- [ ] Version, date and tag match the manifest and the release commit.
- [ ] Sections follow the project's chosen format, newest first.
- [ ] Security fixes are listed without revealing exploit detail before the fix ships.
