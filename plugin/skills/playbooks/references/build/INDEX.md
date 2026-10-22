<!-- Foreman's own index (written for Foreman, not ported). -->
# Build playbooks

Build and compile errors, one file per toolchain. Paths are relative to the playbooks skill.

- `references/build/cpp-build.md` — C++ build, CMake, and compilation error resolution specialist. Fixes build errors, linker issues, and…
- `references/build/csharp-build.md` — C# build errors: code prefixes (NU, NETSDK, MSB, CS), syntax errors hide the rest, nullable errors, NuGet restore.
- `references/build/go-build.md` — Go build errors: the lowest failing package first, module errors vs compiler errors, build tags, go.sum.
- `references/build/jvm-build.md` — Gradle/Maven build errors for Java and Kotlin: name the phase, the compiler line above the summary, classpath and JDK mismatches.
- `references/build/rust-build.md` — Rust build, compilation, and dependency error resolution specialist. Fixes cargo build errors, borrow…
- `references/build/shell-build.md` — Shell script errors: bash -n's give-up point, ShellCheck SC codes by severity, silent strict-mode exits, bats failures.
- `references/build/swift-build.md` — Swift build errors (SwiftPM, Xcode): skip summary lines, out-of-order errors, missing modules, Swift 6 concurrency.
- `references/build/typescript-build.md` — Build and TypeScript error resolution specialist. Fixes build/type errors only with minimal diffs, no…
