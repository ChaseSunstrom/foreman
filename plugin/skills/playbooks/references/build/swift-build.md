<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Swift build errors (SwiftPM, Xcode)

Use when `swift build`, `swift test` or `xcodebuild` fails to compile. The goal is a green build with the smallest
diff that fixes the cause. Built on the library cards `fm lib show swift` (the baseline),
`fm lib show swift-package-manager` (Package.swift, resolution), `fm lib show xcodebuild` (schemes, destinations,
signing) and `fm lib show swift-concurrency` (Swift 6 isolation and Sendable errors).

## Diagnostic commands

```bash
swift --version                                    # compiler and language mode in use
swift build 2>&1 | grep -E ': (error|warning):'    # SwiftPM: only the diagnostics
swift package resolve && swift package show-dependencies
swiftc -typecheck Sources/App/*.swift              # one target's files, no linking
xcodebuild -list                                   # schemes and targets
xcodebuild -scheme App -showdestinations           # pick a destination that exists here
xcodebuild -scheme App -destination 'generic/platform=iOS Simulator' build 2>&1 | grep -E ': (error|warning):'
```

## First error

Diagnostics look like `Sources/App/Store.swift:42:17: error: message`, with `note:` lines and a source excerpt
underneath. The notes often carry the fix (`chain the optional using '?'`, `add stubs for conformance`).

1. **Skip the summary lines.** SwiftPM ends with lines like `error: emit-module command failed with exit code 1`
   and Xcode with `** BUILD FAILED **` and a list of failed commands; neither is the error. Grep for `: error:`.
2. **Printed order is not file order.** The type checker reports in the order it checks, not top to bottom: a
   check here printed an error on line 7, then line 9, then line 4 of one file. Sort the `: error:` lines by
   file and line, and fix a broken declaration (a type, a signature, a protocol) before its uses, since uses of a
   broken declaration fail too. Pass: you name the `file:line:col` you fix and why it goes first.
3. **Module-level errors first.** `no such module 'X'` or a manifest error stops a whole target; fix those before
   any type error inside it.
4. **Rebuild after each fix.** With incremental builds a stale error can linger in Xcode's issue navigator; trust a
   fresh command-line run over the IDE list.

## Common causes

| Error text | Usual cause | Fix |
|---|---|---|
| `cannot find 'Foo' in scope` | Missing `import`, typo, `internal` declaration used from another module, file not in the target | Import the module, make the declaration `public`/`package`, or add the file to the target |
| `no such module 'Foo'` | Product not listed in this target's `dependencies` in Package.swift, or package not linked to the Xcode target | Add `.product(name: "Foo", package: "foo")` to the target; in Xcode, link it under the target's frameworks |
| `no such module 'UIKit'` on macOS or Linux | Platform-only framework | Guard with `#if canImport(UIKit)`, or build for the right platform |
| `cannot convert value of type 'String' to expected argument type 'Int'` | Type mismatch | Convert explicitly (`Int(s)` returns an optional: handle `nil`) |
| `value of optional type 'String?' must be unwrapped to refer to member …` | Optional used as non-optional | `if let`/`guard let`, `?.` or `??`; `!` only when a comment says why it can't be nil |
| `value of type 'T' has no member 'x'` | Typo, wrong type, or member defined in an extension of another module not imported | Fix the name or import the module |
| `type 'T' does not conform to protocol 'P'` | Missing or mismatched requirement | Implement the members the notes list, with their exact signatures |
| `the compiler is unable to type-check this expression in reasonable time` | Long literal or operator chain with heavy inference | Split it into named sub-expressions with explicit types |
| `main actor-isolated property 'x' can not be referenced from a nonisolated context` | Swift 6 isolation | Mark the caller `@MainActor`, or `await` the access from an async context |
| `sending 'x' risks causing data races` / `… is not concurrency-safe because it is nonisolated global shared mutable state` | Non-Sendable value or global var crossing isolation | Make it `Sendable` (value type, immutable), isolate it to an actor, or make the global a `let` |
| `Dependencies could not be resolved because …` | Version requirements that no release satisfies | Read the chain in the message; relax one `from:` requirement, then `swift package resolve`; commit Package.resolved |

## Verify

```bash
swift build && swift test                       # SwiftPM packages
xcodebuild -scheme App -destination 'platform=iOS Simulator,name=<a name from -showdestinations>' build test
```

Pass: exit 0, and for Xcode the output ends with `** TEST SUCCEEDED **` (or `** BUILD SUCCEEDED **` for a
build-only scheme). Swift needs macOS for Xcode and Apple frameworks: on Linux, `swift build` covers only the
packages that build there; say so in the evidence rather than skipping it silently.

## Rules

- No new `@unchecked Sendable`, `nonisolated(unsafe)`, `@preconcurrency import` or language-mode downgrade
  (`swiftLanguageModes: [.v5]`, `SWIFT_VERSION = 5`) in the diff to quiet a concurrency error without a comment
  naming the invariant that makes it safe.
- No `try!` or force-unwrap added to get past a type error.
- Package.resolved changes only when a dependency requirement changed in the same diff.

## Stop conditions

Stop and report when the same error survives three fixes, when Swift 6 isolation errors need the ownership of
shared state redesigned, or when the build needs a platform (Xcode, a simulator, signing) this machine lacks.

## Report

```text
[FIXED] Sources/App/Store.swift:42:17  value of optional type 'User?' must be unwrapped
Fix: guard let with an early return of .notFound
Build: swift build OK | swift test OK | files: Sources/App/Store.swift
```
