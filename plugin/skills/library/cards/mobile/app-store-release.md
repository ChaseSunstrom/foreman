---
name: app-store-release
title: App Store Release
area: mobile
tags: [ios, app-store, testflight, signing, release, review]
detect: [file:*.xcodeproj, file:Fastfile, file:ExportOptions.plist, file:*.entitlements]
related: [fastlane, xcodebuild, play-store-release, push-notifications, in-app-purchases]
---
iOS release: archive a signed build, validate it, ship through TestFlight, and meet App Review's metadata and privacy requirements first.

## Verify
- `xcodebuild archive -scheme App -configuration Release -archivePath build/App.xcarchive`: a Release archive builds and signs.
- `xcodebuild -exportArchive -archivePath build/App.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath build/out`: the export produces an `.ipa` with the chosen method.
- `xcrun altool --validate-app -f build/out/App.ipa -t ios --apiKey KEY --apiIssuer ISSUER`: App Store Connect validation passes before upload.
- `plutil -lint Info.plist PrivacyInfo.xcprivacy`: plists are well formed.

## Test first
The check that fails first is the release gate: archive and validate before any store metadata work.
```sh
# fails when signing, version or privacy manifests are wrong
xcodebuild archive -scheme App -configuration Release -archivePath build/App.xcarchive
test -f build/App.xcarchive/Info.plist
/usr/libexec/PlistBuddy -c "Print :ApplicationProperties:CFBundleShortVersionString" \
  build/App.xcarchive/Info.plist
```

## Do
- Bump `CFBundleShortVersionString` (marketing) and `CFBundleVersion` (build number, unique and increasing per version) on each upload.
- Sign with automatic or fastlane `match` managed profiles and a distribution certificate, and use an App Store Connect API key for CI, not a personal Apple ID password.
- Ship a privacy manifest (`PrivacyInfo.xcprivacy`) listing required-reason API use, and fill the App Privacy answers to match the data the SDKs collect.
- Add a usage description string for every protected resource used (`NSCameraUsageDescription` and others), written for the user.
- Test the exact archive on TestFlight (internal first, then external, which needs beta review) before submitting.
- Provide demo credentials and notes for reviewers when the app requires a login.
- Use phased release for production rollouts, and keep a rollback plan (a fixed build ready).
- Strip debug symbols properly and upload dSYMs to your crash tool.

## Avoid
- Reusing a build number: upload is rejected. Increment it automatically in CI.
- Missing usage description keys: the app crashes on access and review rejects it. Add every key.
- Hardcoded debug or staging endpoints and test accounts in the Release configuration: put them in per-configuration settings.
- Referencing purchases without using StoreKit for digital goods: review rejects it. Use in-app purchase for digital content.
- Submitting without account deletion in apps that allow account creation: add an in-app deletion path.
- Committing certificates, `.p8` keys or profiles to the repo: keep them in a secret store.
- Relying on a Mac with manual Xcode UI steps for the release: script it so it repeats.

## Review
- [ ] Build number is unique, and the version matches release notes.
- [ ] Privacy manifest, usage strings and App Privacy answers agree with actual SDK behavior.
- [ ] The uploaded archive was run on a real device through TestFlight.
- [ ] Reviewer notes and demo login are present, and account deletion exists if sign-up exists.
- [ ] Release uses production endpoints, with dSYMs uploaded.
