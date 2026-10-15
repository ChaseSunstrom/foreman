---
name: bloc
title: Bloc
area: mobile
tags: [flutter, dart, bloc, cubit, state-management, streams]
detect: [dep:bloc, dep:flutter_bloc, dep:bloc_test, dep:hydrated_bloc]
related: [flutter, riverpod]
---
Bloc and Cubit state management: events in, immutable states out, BlocProvider and BlocBuilder in the widget tree.

## Verify
- `flutter analyze`: static analysis (add `bloc_lint` rules if configured).
- `flutter test`: bloc and widget tests.
- `dart format --set-exit-if-changed .`: formatting.
- `flutter test test/features/cart`: one feature while iterating.

## Test first
Use `bloc_test`; mock repositories with `mocktail`.
```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  blocTest<CounterCubit, int>(
    'increment emits next value',
    build: () => CounterCubit(),
    act: (c) => c.increment(),
    expect: () => [1],
  );
}
```
For events: `act: (b) => b.add(LoadRequested())`, `expect: () => [isA<Loading>(), isA<Loaded>()]`.

## Do
- Use `Cubit` for simple state with methods, `Bloc` when events need transformation (debounce, restartable) via `on<Event>(handler, transformer:)`.
- Make states immutable and comparable: `Equatable` or `freezed`, so equal states are not re-emitted.
- Model screen state as a sealed hierarchy or a status enum plus data (initial, loading, success, failure).
- Provide with `BlocProvider(create: ...)` high enough for all consumers; use `BlocProvider.value` only to share an existing instance.
- Use `BlocBuilder` for UI, `BlocListener` for one-off side effects (navigation, snackbars), `BlocConsumer` for both, and `buildWhen` / `BlocSelector` to narrow rebuilds.
- Inject repositories through the constructor and register them with `RepositoryProvider`.
- Handle errors inside handlers: emit a failure state, and override `onError` for logging.

## Avoid
- Emitting after the handler completes or after `close`: `emit` throws. Use `await emit.forEach` / `emit.onEach` for streams, and check `isClosed` in callbacks.
- Mutating a state object and re-emitting it: equality says unchanged and the UI does not rebuild. Create a new instance with `copyWith`.
- Calling `context.read` or `.watch` for a bloc above its provider: `ProviderNotFoundException`. Provide higher, or pass `BlocProvider.value`.
- Navigation inside `BlocBuilder`: runs on every rebuild. Use `BlocListener`.
- `BlocProvider(create: (_) => existingBloc)`: the provider closes it on dispose. Use `.value` for existing instances.
- Business logic in widgets or states talking to other blocs directly: couple them via repositories or listen at the UI layer.
- Handling every event with the default concurrent transformer on search or submit: out-of-order results. Use `restartable()` or `droppable()` from `bloc_concurrency`.

## Review
- [ ] States are immutable and value-comparable.
- [ ] Every bloc has `blocTest` cases for success and failure paths.
- [ ] Side effects run in listeners, not builders.
- [ ] Created blocs are closed by their provider, and shared ones use `.value`.
- [ ] Event concurrency is chosen deliberately for search and submit flows.
