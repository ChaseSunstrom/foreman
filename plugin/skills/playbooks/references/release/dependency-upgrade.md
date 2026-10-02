<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Dependency upgrade

Use when bumping a library, toolchain or runtime.

1. **One upgrade per task.** Read the changelog/release notes between the current and target version; list breaking changes and deprecations that touch this code (grep for each API).
2. **Baseline:** full gate green before the bump; record timings if performance matters.
3. **Bump** the manifest and lockfile together with the tool's own command (not hand edits); keep transitive changes visible in the diff.
4. **Fix forward** compile errors and deprecations in small commits; no unrelated refactors.
5. **Verify:** full gate, plus the paths the release notes flag; compare timings/bundle size against the baseline.
6. **Security:** check the new version's advisories and that the package name/source didn't change (typosquats, new maintainers). A new dependency needs the user's yes.
