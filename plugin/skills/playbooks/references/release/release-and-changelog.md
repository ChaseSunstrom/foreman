<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Release and changelog

Use when cutting a version, tagging, or publishing.

1. **Gate first:** the full gate on the exact commit you'll tag (`fm check`), from a clean tree; no "fix after tagging".
2. **Version:** follow the project's scheme (semver: breaking → major, feature → minor, fix → patch). Bump every place that carries it (manifests, lockfiles, plugin.json, marketplace entries) in one commit.
3. **Changelog:** one entry per user-visible change, written for users (what changed and why it matters), grouped Added / Changed / Fixed / Removed; link task ids. Move "Unreleased" under the new version with the date.
4. **Breaking changes** get a migration note: what to change, before → after.
5. **Tag and publish** only with the user's yes (outward and hard to undo): `git tag -a vX.Y.Z -m …`, push the tag, then the package/registry publish.
6. **After:** confirm the published artifact installs and runs from scratch; record the evidence; open the next "Unreleased" section.
