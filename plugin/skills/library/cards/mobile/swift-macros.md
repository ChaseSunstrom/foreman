---
name: swift-macros
title: Swift Macros
area: mobile
tags: [swift, macros, swiftsyntax, metaprogramming, spm, codegen]
detect: [dep:swift-syntax, file:Package.swift]
related: [swift-package-manager, swift-testing, xctest, xcodebuild]
---
Swift macros: compile-time code generation as a separate SwiftSyntax macro target, with the expansion tested as text.

## Verify
- `swift build`: the macro plugin and its client library build.
- `swift test`: expansion tests pass.
- `swift package resolve`: swift-syntax resolves at a version matching the toolchain.
- `swift build -c release`: macros still expand under optimization, and the plugin builds in release.

## Test first
Test the expansion with `SwiftSyntaxMacrosTestSupport` (or the macro testing package you already use). The macro's declared role decides what it may generate.
```swift
import SwiftSyntaxMacrosTestSupport
import XCTest
@testable import MyMacros

final class StringifyTests: XCTestCase {
    func testExpandsToTuple() {
        assertMacroExpansion(
            "#stringify(a + b)",
            expandedSource: "(a + b, \"a + b\")",
            macros: ["stringify": StringifyMacro.self]
        )
    }
}
```

## Do
- Lay out four pieces in `Package.swift`: a `.macro(name:)` target depending on `SwiftSyntaxMacros` and `SwiftCompilerPlugin`, a library declaring the macro, a client, and tests.
- Declare the macro with `@freestanding(expression)`, `@attached(member, names: ...)` and so on, naming every generated symbol in `names:` (`named(...)`, `arbitrary`, `prefixed(_)`).
- Implement the matching protocol (`ExpressionMacro`, `MemberMacro`, `PeerMacro`, `AccessorMacro`) and register types in a `CompilerPlugin` with `providingMacros`.
- Emit diagnostics with `context.diagnose(Diagnostic(node:message:))` when the macro is used on the wrong declaration.
- Use `context.makeUniqueName("x")` for local helpers, so names never clash with user code.
- Build output with string interpolation of SyntaxBuilder snippets, and read the node's arguments by walking `node.arguments`.
- Test every diagnostic path, and test expansion when attached to unsupported declarations.
- Prefer a plain function or generic over a macro when it would do.

## Avoid
- Generating names not listed in `names:`: the compiler rejects them. List all of them.
- Reaching into the file system, network or global state inside a macro: it runs sandboxed and must be deterministic.
- Matching syntax by its text with `description.contains`: it breaks on trivia. Inspect the typed syntax nodes.
- Pinning swift-syntax to a loose range: macro hosts break on toolchain upgrades. Match the version to your toolchain release and update together.
- Expecting type information: macros see syntax only, with no type checking. Require explicit types or arguments.
- Forgetting the `#externalMacro(module:type:)` path: an incorrect module or type name fails at the client's build with a vague error.
- Slow builds from the macro target: swift-syntax compiles from source, so keep the macro target small and avoid extra dependencies.

## Review
- [ ] Declared roles and `names:` match what the implementation emits.
- [ ] Misuse produces a clear diagnostic, and a test asserts it.
- [ ] Expansion tests cover each argument shape.
- [ ] swift-syntax is pinned deliberately.
- [ ] A client target compiles and runs the macro end to end.
