---
name: flutter
title: Flutter
area: mobile
tags: [flutter, dart, mobile, widgets, cross-platform, ui]
detect: [dep:flutter, dep:flutter_test, file:pubspec.yaml, ext:.dart]
related: [riverpod, bloc, fastlane, xcodebuild]
---
Flutter apps: widget tree, state ownership, async UI, widget tests and platform builds.

## Verify
- `flutter analyze`: static analysis against analysis_options.yaml.
- `dart format --set-exit-if-changed .`: formatting (exits non-zero when files change).
- `flutter test`: unit and widget tests.
- `flutter test integration_test`: integration tests on a device or emulator, when present.
- `flutter build apk --debug`: Android build compiles (use `flutter build ios --no-codesign` on macOS).

## Test first
Widget tests live in `test/` with the `_test.dart` suffix and use `flutter_test`.
```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:app/counter.dart';

void main() {
  testWidgets('tap increments', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: Counter()));
    await tester.tap(find.byKey(const Key('inc')));
    await tester.pump();
    expect(find.text('1'), findsOneWidget);
  });
}
```

## Do
- Split big `build` methods into small `const` widgets (classes, not helper methods), so rebuilds stay local.
- Put state at the lowest common owner; use one state-management approach project-wide (Riverpod, Bloc or similar).
- Use `const` constructors wherever possible; enable `prefer_const_constructors` in lints.
- Await in `initState` via a method, never `async` on `initState`; use `FutureBuilder`/`StreamBuilder` or the state library for async data.
- Check `mounted` before using `BuildContext` after an `await`.
- Dispose controllers, focus nodes, animation controllers and subscriptions in `dispose`.
- Give list items keys when they reorder, and use `ListView.builder` for long lists.

## Avoid
- Using `BuildContext` across async gaps without `if (!context.mounted) return;`: crashes on disposed widgets.
- Calling `setState` after `dispose`: error. Cancel timers and subscriptions in `dispose`.
- Creating futures inside `build` for `FutureBuilder`: refires on every rebuild. Create once in `initState` or the state layer.
- `Opacity`, `ClipRRect` and `saveLayer`-heavy widgets in long lists: jank. Profile in `--profile` mode.
- Hardcoded widths and font sizes: overflow on small devices or large text. Use `LayoutBuilder`, `Flexible` and theme text styles.
- `WillPopScope`: deprecated. Use `PopScope`.
- Using `print` for logs in shipped code: use `debugPrint` or a logger, and `avoid_print` lint.

## Review
- [ ] `flutter analyze` and format are clean with no ignores added.
- [ ] Async gaps guard `context.mounted`; controllers are disposed.
- [ ] Widgets are small, const where possible, and keyed in dynamic lists.
- [ ] One state-management pattern is used consistently.
- [ ] Widget tests cover the new UI path and an error or empty state.
