---
name: bazel
title: Bazel
area: native
tags: [bazel, build, cc, hermetic, bzlmod, monorepo]
detect: [file:MODULE.bazel, file:WORKSPACE, file:WORKSPACE.bazel, file:BUILD.bazel, file:.bazelrc, file:.bazelversion]
related: [cmake, googletest, sanitizers, conan]
---
Bazel builds: hermetic targets, explicit deps and visibility, Bzlmod for external dependencies.

## Verify
- `bazel build //...`: every target in the workspace builds.
- `bazel test //... --test_output=errors`: all tests run and failing logs are shown.
- `bazel query 'deps(//app:main)'`: the dependency graph is what you declared.
- `bazel test //pkg:all --runs_per_test=20`: a flaky test shows up.

## Test first
Tests are `cc_test` (or language equivalent) targets next to the code in `BUILD.bazel`. Add the target and failing test before the implementation.
```python
cc_test(
    name = "parser_test",
    srcs = ["parser_test.cc"],
    deps = [
        ":parser",
        "@googletest//:gtest_main",
    ],
)
```
`bazel test //pkg:parser_test` must fail for the missing behaviour, not for a missing dep.

## Do
- Declare every dependency in `deps`; a target may only include headers from direct deps. Keep `hdrs` (public) and `srcs`/private headers separate.
- Use `visibility` narrowly (`//visibility:private` default, package groups for shared libs).
- Pin the Bazel version in `.bazelversion` and put shared flags in `.bazelrc` with named configs (`build:asan --copt=-fsanitize=address`, used as `--config=asan`).
- Prefer Bzlmod (`MODULE.bazel`, `bazel_dep(name = ..., version = ...)`) for new external deps.
- Keep rules hermetic: use `genrule`/rules with declared `srcs` and `outs`, no network or absolute paths.
- Use `select()` with `config_setting`/`platforms` for per-OS or per-config differences.
- Use remote cache flags only through `.bazelrc` configs so local builds still work.

## Avoid
- `glob` over directories that include generated or unrelated files: it hides missing deps. Glob narrow patterns, or list files.
- `//visibility:public` on everything: it erodes layering. Restrict and widen when needed.
- New `WORKSPACE` http_archive deps in a Bzlmod repo: they are legacy. Use `bazel_dep` or a module extension.
- `tags = ["local"]` or `--spawn_strategy=local` to hide sandbox failures: the build is missing declared inputs. Declare `data`/`srcs`.
- `bazel clean` as a fix: it indicates non-hermetic rules. Find the undeclared input.
- Depending on `//:all` of a package from another package: couples to everything in it.
- `cc_library` with `includes`/`copts` set globally in `.bazelrc` for one target's need: put it on the target.

## Review
- [ ] Each target lists all direct deps and no unused ones.
- [ ] Visibility is minimal; tests are not exported to production targets.
- [ ] External deps are versioned and checksummed (`MODULE.bazel` or `sha256`).
- [ ] `.bazelversion` is present; sanitizer and release configs exist in `.bazelrc`.
- [ ] No `local`-tagged workarounds without a comment.
