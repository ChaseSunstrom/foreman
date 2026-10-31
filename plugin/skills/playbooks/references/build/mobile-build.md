<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Mobile build failures: Xcode, Expo, Flutter

Use when an iOS or Android app build fails: `xcodebuild`, `npx expo` or EAS, `flutter build`, or a fastlane lane that wraps them.

Built on the cards `fm lib show xcodebuild`, `fm lib show expo`, `fm lib show flutter`, `fm lib show fastlane` and `fm lib show swift-package-manager`.

1. **Name the layer.** Dependency resolution (SwiftPM, CocoaPods, pub, npm), compile, code signing, or packaging. Each fails with a different tool and the first error line is the one to fix; later ones echo it.
2. **Reproduce from the command line, not the IDE:**
   ```bash
   xcodebuild -list
   xcodebuild -scheme App -destination 'platform=iOS Simulator,name=iPhone 15' build 2>&1 | tail -40
   npx expo-doctor && npx expo install --check
   flutter analyze && flutter build apk --debug
   ```
3. **Resolution errors first.** Delete nothing yet: `xcodebuild -resolvePackageDependencies`, `npx expo install --check` (SDK-matched versions), `flutter pub get`. A lockfile diff you did not intend is the bug.
4. **Signing is not a compile error.** "No profiles" or "code signing" failures need the team, bundle id and match state checked (`bundle exec fastlane lanes`, then the signing lane), never `CODE_SIGNING_ALLOWED=NO` committed to fix a release build.
5. **Fix the smallest cause, rebuild from a fresh run.** One change per rebuild.
6. **Prove both platforms** when the code is shared: a fix that builds iOS can break Android.

Pass: the original command exits 0 and `git diff --stat` shows only the files the cause lives in.

Stop and report when the fix needs an SDK, Xcode or Flutter major upgrade (hand it to the dependency-upgrade playbook).
