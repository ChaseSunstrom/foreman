---
name: flutter-testing
title: Flutter Testing
area: mobile
tags: [flutter, dart, testing, widget-tests, integration, golden]
detect: [dep:flutter_test, dep:integration_test, file:pubspec.yaml]
related: [flutter, bloc, riverpod]
---
Flutter testing: unit, widget and integration tests with `flutter_test`, where widget tests drive the UI in a fake-async environment.

## Verify
- `flutter analyze`: static analysis and lints pass.
- `flutter test`: runs unit and widget tests under `test/`.
- `flutter test --coverage`: writes `coverage/lcov.info`.
- `flutter test integration_test`: runs integration tests on a connected device or emulator.
- `flutter test --update-goldens`: regenerates golden images, to be used only for intended visual changes.

## Test first
Widget tests live in `test/`, mirroring `lib/`.
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:app/counter_page.dart';

void main() {
  testWidgets('tap increments the counter', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: CounterPage()));
    expect(find.text('0'), findsOneWidget);

    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    expect(find.text('1'), findsOneWidget);
  });
}
```

## Do
- Wrap widgets under test in `MaterialApp` (or the needed `Directionality` and `MediaQuery`), and provide state through the same providers or blocs the app uses, overridden with fakes.
- Use `tester.pump()` for one frame and `tester.pumpAndSettle()` for animations to finish. Use `pump(Duration)` where a timer or an infinite animation never settles.
- Find by `Key`, type or semantics (`find.bySemanticsLabel`), not by index or widget internals.
- Use `fakeAsync` and `tester.runAsync` for timers and real I/O, and never use real delays.
- Mock with `mocktail` (null-safe, no codegen), and register fallback values with `registerFallbackValue`.
- Add golden tests with `await expectLater(find.byType(Card), matchesGoldenFile('card.png'))`, pinned to one platform and font in CI.
- Write integration tests with `IntegrationTestWidgetsFlutterBinding.ensureInitialized()` in `integration_test/`, and keep them few and end to end.
- Test BLoC with `bloc_test` and Riverpod with a `ProviderContainer` and overrides.

## Avoid
- `pumpAndSettle` with an infinite animation (spinners): the test times out. Pump a fixed duration.
- Forgetting `await` on `tester` calls: the assertion runs before the frame. Await every call.
- Real network, shared preferences or platform channels in widget tests: stub them with `TestDefaultBinaryMessengerBinding` handlers or fakes.
- Golden files generated on different OS or fonts: diffs everywhere. Generate in CI's environment or use a golden toolkit.
- Finding widgets by text that localization changes: use keys.
- Testing private widget state through `State` casts: test visible behavior.

## Review
- [ ] Tests await every `tester` call and use the right pump.
- [ ] No real I/O, timers or network.
- [ ] Finders use keys or semantics, not positions.
- [ ] Golden tests run in a pinned environment and regenerate only on intent.
- [ ] Unit, widget and integration coverage match the risk of the change.
