<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Verify a mobile app change

Use when app code changed and you must show it works on the platform, not only that it compiles.

Built on the cards `fm lib show xctest`, `fm lib show swift-testing`, `fm lib show flutter-testing`, `fm lib show expo` and `fm lib show react-native`.

1. **Static first:** `npx tsc --noEmit`, `flutter analyze`, or the Xcode build for the scheme.
2. **Logic tests with no UI:**
   ```bash
   npx jest
   flutter test
   swift test
   xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15' -only-testing:AppTests/CartTests
   ```
3. **One component or widget test per bug**, using the exact payload or state that failed.
4. **Dependency match:** `npx expo-doctor` and `npx expo install --check` catch SDK mismatches that only crash at runtime.
5. **Release-type run on a device** for anything touching permissions, push, deep links, offline, or timing; debug simulators hide these.
6. **Say what you did not run:** the other platform, a real device, a store build.

Pass: the commands for the platforms you changed exit 0, a new test failed first, and the report lists each platform not exercised.
