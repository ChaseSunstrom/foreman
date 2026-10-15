---
name: xcodebuild
title: xcodebuild
area: mobile
tags: [xcode, ios, macos, build, cli, ci, simulator]
detect: [file:*.xcodeproj, file:*.xcworkspace, file:*.xcconfig, file:*.xctestplan]
related: [swift-package-manager, xctest, fastlane, swiftui, uikit]
---
xcodebuild and simctl: command-line builds, tests, destinations, test plans, archives and signing.

## Verify
- `xcodebuild -list`: schemes, targets and configurations available in the project or workspace.
- `xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 15' build`: compiles for a simulator.
- `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15' -resultBundlePath build/Test.xcresult`: runs tests and keeps a result bundle.
- `xcrun simctl list devices available`: destinations that exist on this machine.
- `xcodebuild -showBuildSettings -scheme App`: effective settings, for signing and version debugging.

## Test first
The failing check is a red `xcodebuild test`. Run one test while iterating.
```
xcodebuild test -scheme App \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -only-testing:AppTests/CartModelTests/testTotalIncludesTax
```
For a build or CI change, run the exact command locally first and see it fail for the reason being fixed.

## Do
- Use `-workspace` when CocoaPods or multiple projects exist, otherwise `-project`; always pass `-scheme`.
- Pass `-destination` explicitly; add `-derivedDataPath build/DerivedData` so CI caches and cleans one place.
- Make schemes shared (checked in under `xcshareddata`) so CI can see them.
- Use test plans (`-testPlan`) to choose configurations and skip slow suites.
- Archive with `xcodebuild archive -scheme App -archivePath build/App.xcarchive`, then `-exportArchive` with an `ExportOptions.plist`.
- Set versions via build settings (`MARKETING_VERSION`, `CURRENT_PROJECT_VERSION`) in xcconfig files.
- Pipe through `xcbeautify` or `xcpretty` only for display, and keep `set -o pipefail` so failures still fail the job.

## Avoid
- `-sdk iphonesimulator` with no `-destination`: ambiguous destination warnings or wrong device. Name the destination.
- Piping into a formatter without `pipefail`: the pipeline reports success on failing builds. Enable `pipefail`.
- Simulator names that are not installed on the CI image: "Unable to find a destination". Check `simctl list` and use the id (`id=UDID`) where stable.
- Committing signing certificates or provisioning secrets: use the keychain and CI secrets (see fastlane `match`).
- Disabling signing globally to get green (`CODE_SIGNING_ALLOWED=NO`) for release builds: fine for test runs, wrong for archives.
- Reusing stale DerivedData after big changes: phantom errors. Delete the derived data path.
- Unshared schemes: works locally, "scheme not found" in CI.

## Review
- [ ] The scheme is shared and the command names scheme and destination.
- [ ] CI keeps the `.xcresult` and fails on non-zero exit even when piped.
- [ ] Version and build number come from settings, not hand-edited plists.
- [ ] No secrets or profiles in the repo.
- [ ] The same commands run locally and in CI.
