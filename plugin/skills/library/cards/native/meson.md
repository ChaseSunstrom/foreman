---
name: meson
title: Meson
area: native
tags: [meson, ninja, c, cpp, build, wraps]
detect: [file:meson.build, file:meson.options, file:meson_options.txt, file:subprojects/*.wrap]
related: [cmake, googletest, sanitizers, valgrind]
---
Meson builds: declarative meson.build, Ninja backend, built-in test runner, wraps for dependencies.

## Verify
- `meson setup build --wipe`: a clean configure succeeds (use `--reconfigure` to keep options).
- `meson compile -C build`: the project builds.
- `meson test -C build --print-errorlogs`: tests run and failures show output.
- `meson test -C build --wrap=valgrind`: tests run under Valgrind (if installed).

## Test first
Tests are `test()` entries in meson.build, usually in `tests/meson.build`. Add the executable and `test()` first, see it fail.
```meson
t = executable('parser_test', 'parser_test.c',
  dependencies: [parser_dep])
test('parser rejects empty', t)
```
`meson test -C build 'parser rejects empty'` fails until the code is right.

## Do
- Set `project('x', 'c', version: '...', default_options: ['warning_level=3', 'c_std=c11'])`.
- Express dependencies with `dependency('name')` and pass the result via `dependencies:`; use `declare_dependency` to export your own library to subprojects and tests.
- Use `meson_options.txt` (or `meson.options` in newer releases) for build options and read them with `get_option()`.
- Configure per build type with `-Dbuildtype=debug|release` and `-Db_sanitize=address,undefined` for sanitizer builds.
- Use `subprojects/*.wrap` files (`meson wrap install NAME`) for vendored dependencies; commit the wrap, not the downloaded source.
- Generate files with `custom_target` or `configure_file`, declaring `input`/`output` so Ninja tracks them.
- Keep `include_directories('include')` and `install_headers` explicit.

## Avoid
- `run_command` to list sources with `ls`/`find`: it breaks reconfigure tracking and portability. List files in meson.build.
- Passing `-Wall` and similar through `c_args`: use `warning_level` and `werror` options.
- Editing the build directory by hand or reusing one across option changes: use `meson configure build -Dopt=val` or recreate.
- Calling `shared_library` when the dependency should be static or the reverse without `default_library`: use `library()` and the `default_library` option.
- Forgetting `dependencies:` on `test()` executables: link errors that look like missing symbols.
- Relying on the compiler's default C standard: set `c_std`/`cpp_std` explicitly.

## Review
- [ ] Warnings are enabled (`warning_level`) and `werror` is on in CI.
- [ ] Tests are registered with `test()` and run under `meson test`.
- [ ] Options come from `get_option()`, not environment variables.
- [ ] Wraps are pinned to a revision or hash; no vendored copy of the dependency in the tree.
- [ ] Sanitizer build is exercised with `-Db_sanitize`.
