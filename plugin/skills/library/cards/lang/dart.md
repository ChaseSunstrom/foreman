---
name: dart
title: Dart
area: lang
tags: [dart, pub, null-safety, analyzer, async, test]
detect: [ext:.dart, file:pubspec.yaml, file:analysis_options.yaml]
related: [bash]
---
Dart packages and CLIs: pub dependencies, sound null safety, the analyzer, `package:test`.

## Verify
- `dart pub get`: resolves dependencies and writes `pubspec.lock`.
- `dart analyze --fatal-infos`: analyzer and lints with infos treated as failures.
- `dart format --output=none --set-exit-if-changed .`: formatting is clean.
- `dart test`: runs `test/**_test.dart` (Flutter projects use `flutter test` instead).

## Test first
Tests live in `test/` with names ending `_test.dart`; `test` is a dev dependency.
```dart
import 'package:test/test.dart';
import 'package:myapp/parse.dart';

void main() {
  test('parseAmount rejects blank input', () {
    expect(() => parseAmount(''), throwsFormatException);
  });
  test('async loader surfaces errors', () {
    expect(loadUser('missing'), throwsA(isA<NotFound>()));
  });
}
```

## Do
- Enable lints in `analysis_options.yaml` (`include: package:lints/recommended.yaml`, or `package:flutter_lints/flutter.yaml`) and set `strict-casts`, `strict-inference`, `strict-raw-types` under `analyzer: language:`.
- Use `final` and `const` constructors; model data with `sealed class` and exhaustive `switch` expressions.
- Keep public API in `lib/` and implementation in `lib/src/`; export deliberately from one barrel file.
- Prefer `Future`/`async`/`await` with `try`/`catch`; close `StreamController`s and cancel `StreamSubscription`s.
- Use `dart fix --dry-run` then `dart fix --apply` for lint migrations.
- Constrain SDK in `pubspec.yaml` (`environment: sdk:`) and commit `pubspec.lock` for apps, not for libraries.

## Avoid
- The null-assertion `!` to quiet the analyzer: crashes at runtime. Use a null check, `??`, or restructure.
- Unawaited futures: errors vanish. Await them, or mark deliberate fire-and-forget with `unawaited()` from `dart:async`.
- Importing `package:myapp/src/...` from another package: breaks the encapsulation. Export from `lib/`.
- Mixing relative and package imports for the same file inside `lib/`: duplicates identity in some tools. Stay consistent.
- Pre-null-safety packages or `// @dart=2.9` pins: stale. Upgrade the dependency.
- Catching `Exception` or `Object` broadly and swallowing: catch the specific type and rethrow with `rethrow`.

## Review
- [ ] `dart analyze` is clean with no new `// ignore:` lines, and each ignore has a reason.
- [ ] Public APIs have doc comments (`///`) and no leaked `src/` types.
- [ ] Every `Future`, `Stream` and controller is awaited, listened to, or closed.
- [ ] New dependencies are in the right section (`dependencies` vs `dev_dependencies`).
- [ ] Tests cover the failure path and not just the happy path.
