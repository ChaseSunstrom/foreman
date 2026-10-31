<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Phone app crash: iOS, Android, RN, Flutter

Use when an iOS, Android, React, Expo or Flutter app crashes on a phone or tablet, or a push notification or deep link fails there.

Built on the cards `fm lib show react-native`, `fm lib show expo`, `fm lib show flutter`, `fm lib show swiftui`, `fm lib show push-notifications` and `fm lib show deep-links`.

1. **Get the crash text**, not the symptom: `adb logcat -b crash -d`, `xcrun simctl spawn booted log show --last 5m --predicate 'process == "App"'`, or the Metro and `flutter logs` output. A JS red box and a native crash are different bugs.
2. **Same build type.** Reproduce in a Release or profile build on a device; debug builds hide timing, minification and permission bugs (`npx react-native run-android --mode release`).
3. **Classify:** state after backgrounding, permission denied, main-thread work, an unhandled null from an API, a deep link or notification payload shape.
4. **Write the failing test at the lowest layer:** a unit test on the payload parser, a widget test (`flutter test`), a Jest test, or an XCTest with the real payload from the log.
5. **Fix, then run the platform's analyzer and tests:**
   ```bash
   npx tsc --noEmit && npx jest
   flutter analyze && flutter test
   xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'
   ```

Pass: the crash log no longer reproduces on a device-class build and the new test is in the suite.

Stop when it needs a store-side setting (push credentials, signing) you cannot reach.
