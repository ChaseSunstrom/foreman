---
name: vcpkg
title: vcpkg
area: native
tags: [vcpkg, c, cpp, packages, manifest, cmake]
detect: [file:vcpkg.json, file:vcpkg-configuration.json, file:vcpkg/*]
related: [cmake, conan, googletest]
---
vcpkg manifest mode: dependencies in vcpkg.json, a pinned baseline, consumed through the CMake toolchain file.

## Verify
- `vcpkg install`: manifest dependencies build for the triplet (run in the directory with vcpkg.json).
- `cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake`: configure finds the packages.
- `vcpkg x-update-baseline`: the baseline moves to the current registry commit (review the diff).
- `cmake --build build && ctest --test-dir build --output-on-failure`: the project builds and passes with those versions.

## Test first
Add the test framework as a dependency and a failing test before the code. Declare it in the manifest, find it in CMake, run CTest.
```json
{
  "dependencies": ["fmt", { "name": "gtest", "host": false }],
  "builtin-baseline": "<40-char commit sha>"
}
```
```cmake
find_package(GTest CONFIG REQUIRED)
target_link_libraries(t PRIVATE GTest::gtest_main)
```
The build fails to link until the manifest has gtest, then the test fails for the behaviour.

## Do
- Use manifest mode (`vcpkg.json` at the repo root), not `vcpkg install <pkg>` classic mode, so versions travel with the repo.
- Set `builtin-baseline` to a commit of the vcpkg registry and use `overrides` to pin individual versions.
- Pass the toolchain file through a CMake preset (`CMAKE_TOOLCHAIN_FILE`) and set `VCPKG_TARGET_TRIPLET` when not using the default.
- Use `find_package(X CONFIG REQUIRED)` and link the imported targets that the port's usage message prints.
- Request features explicitly: `{ "name": "boost-asio", "features": [...] }`, and `"default-features": false` to trim builds.
- Keep custom ports and registries in `vcpkg-configuration.json` with a pinned `baseline`.
- Enable binary caching in CI so each run does not rebuild all ports.

## Avoid
- A missing or outdated `builtin-baseline`: resolution uses whatever versions the checkout has, so builds drift. Add it with `vcpkg x-update-baseline --add-initial-baseline`.
- Classic mode `vcpkg install foo` plus a global install tree: CI and teammates see different versions. Use the manifest.
- Setting the toolchain file after `project()` in CMakeLists.txt: it is ignored. Pass it on the command line or in a preset.
- Linking by guessed variable names like `${FOO_LIBRARIES}`: use the imported targets from the port's usage output.
- Committing the vcpkg installed tree or `vcpkg_installed/`: add to .gitignore.
- Assuming the triplet is the same as the host on Windows (`x64-windows` dynamic vs `x64-windows-static`): set it intentionally to match the CRT choice.

## Review
- [ ] vcpkg.json has a baseline; `overrides` only with a comment on why.
- [ ] Toolchain file is wired via preset or documented command.
- [ ] Features and default-features are chosen deliberately.
- [ ] Build artifacts (`vcpkg_installed`, `build`) are ignored by git.
- [ ] CI uses binary caching and the same triplet as developers.
