---
name: play-store-release
title: Play Store Release
area: mobile
tags: [android, play-store, aab, signing, release, gradle]
detect: [file:*.gradle.kts, file:AndroidManifest.xml, file:proguard-rules.pro]
related: [fastlane, app-store-release, push-notifications, in-app-purchases, compose-performance]
---
Android release: a signed, R8-shrunk app bundle with Play App Signing, tested through internal and closed tracks and rolled out in stages.

## Verify
- `./gradlew :app:bundleRelease`: builds the release `.aab` Play requires.
- `./gradlew :app:lintRelease`: release lint, including missing permissions and target SDK problems.
- `./gradlew :app:testReleaseUnitTest`: unit tests pass against the release variant.
- `bundletool validate --bundle=app/build/outputs/bundle/release/app-release.aab`: the bundle is structurally valid.
- `bundletool build-apks --bundle=app-release.aab --output=app.apks --mode=universal`: produces installable APKs for a device test of the exact artifact.

## Test first
The first failing check is the release build itself: make the bundle build and the minified app launch before touching listings.
```sh
./gradlew :app:bundleRelease                      # fails on signing, R8 or lint errors
bundletool build-apks --bundle=app/build/outputs/bundle/release/app-release.aab \
  --output=/tmp/app.apks --mode=universal
# install the universal apk from /tmp/app.apks on a device and smoke test login and one flow
```

## Do
- Increase `versionCode` for every upload, and keep `versionName` for display. Derive both from CI so they never collide.
- Enroll in Play App Signing, keep an upload key, and read the keystore path and passwords from environment variables or a local untracked file in `signingConfigs`.
- Enable `isMinifyEnabled = true` and `isShrinkResources = true` for release, with keep rules for reflection, serialization and JNI in `proguard-rules.pro`.
- Upload the mapping file (and native debug symbols) so crash reports deobfuscate.
- Set `targetSdk` to what the Play policy currently requires, and test behavior changes for that level.
- Declare only needed permissions, and complete the Data safety form to match the SDKs in use.
- Roll out in tracks: internal, closed, then production with a staged percentage, and halt the rollout if the crash rate rises.
- Publish with the Play Developer API or fastlane `supply` using a service account.

## Avoid
- Uploading an APK where an AAB is required: new apps need the bundle format. Build `bundleRelease`.
- Testing only the debug build: R8 removes classes the release needs, causing release-only crashes. Smoke test the minified build.
- Committing the keystore or its passwords: keep them out of the repo and in secrets.
- Losing the upload key without Play App Signing enrolled: updates become impossible. Enroll and back up the key.
- Reused `versionCode`: the upload is rejected. Bump it.
- A Data safety form that disagrees with SDK behavior (ads, analytics): policy enforcement follows. Audit SDKs.
- Shipping at 100% on day one: roll out staged.

## Review
- [ ] `versionCode` is higher than the last upload, and signing is by upload key with Play App Signing.
- [ ] The minified release build was installed and exercised on a device.
- [ ] Mapping and symbol files are uploaded.
- [ ] Permissions, target SDK and the Data safety form are consistent.
- [ ] Rollout is staged with a stop condition.
