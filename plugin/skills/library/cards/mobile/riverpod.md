---
name: riverpod
title: Riverpod
area: mobile
tags: [flutter, dart, riverpod, state-management, providers]
detect: [dep:flutter_riverpod, dep:riverpod, dep:hooks_riverpod, dep:riverpod_annotation, dep:riverpod_generator]
related: [flutter, bloc]
---
Riverpod state management for Dart and Flutter: providers, notifiers, AsyncValue, overrides and code generation.

## Verify
- `flutter analyze`: includes riverpod_lint rules when `riverpod_lint` is configured.
- `dart run build_runner build --delete-conflicting-outputs`: regenerates `*.g.dart` when using riverpod_generator.
- `flutter test`: provider and widget tests.
- `dart format --set-exit-if-changed .`: formatting.

## Test first
Test providers with a `ProviderContainer` and no widgets; override dependencies.
```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('cart total reflects added item', () {
    final c = ProviderContainer(overrides: [
      priceRepoProvider.overrideWithValue(FakePriceRepo()),
    ]);
    addTearDown(c.dispose);
    c.read(cartProvider.notifier).add('a');
    expect(c.read(cartTotalProvider), 100);
  });
}
```
For widgets, wrap in `ProviderScope(overrides: [...])`.

## Do
- Wrap the app in `ProviderScope`; declare providers as top-level finals (or with `@riverpod` annotations).
- Use `ref.watch` in `build` and provider bodies, `ref.read` in callbacks and event handlers, `ref.listen` for side effects.
- Model async data as `AsyncValue` and render with `.when(data:, loading:, error:)` (or pattern matching).
- Use `Notifier` / `AsyncNotifier` classes for mutable state with methods, not `StateNotifier` in new code.
- Use `.autoDispose` (the default with codegen) for screen-scoped state; `ref.keepAlive()` where a cache is wanted.
- Use `.family` or generated parameters for per-id providers.
- Select narrow slices with `ref.watch(p.select((s) => s.name))` to limit rebuilds.

## Avoid
- `ref.read` inside `build`: the widget never rebuilds on change. Use `ref.watch`.
- `ref.watch` inside callbacks such as `onPressed`: throws or misbehaves. Use `ref.read`.
- Constructing a `ProviderContainer` or provider inside a widget `build`: state resets every rebuild. Declare providers globally.
- `StateNotifierProvider` / `ChangeNotifierProvider` in new code: legacy. Use `NotifierProvider` / `AsyncNotifierProvider`.
- Reading a provider in `initState` with `ref.watch`: not allowed. Use `ref.read` or `ref.listenManual`.
- Mutating state objects in place: no notification. Assign a new immutable value to `state`.
- Hard-wiring singletons (Dio, DB) instead of exposing them as providers: untestable. Provide and override in tests.

## Review
- [ ] `watch` in builds, `read` in handlers, `listen` for side effects.
- [ ] State is immutable and replaced, not mutated.
- [ ] External dependencies come through providers and are overridden in tests.
- [ ] Async state shows loading and error branches.
- [ ] Generated files are regenerated and committed per repo convention.
