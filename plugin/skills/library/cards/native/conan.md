---
name: conan
title: Conan 2
area: native
tags: [conan, c, cpp, packages, dependencies, profiles]
detect: [file:conanfile.py, file:conanfile.txt, file:conan.lock, file:conandata.yml]
related: [cmake, vcpkg, meson, bazel]
---
Conan 2 C/C++ dependency management: conanfile, profiles, lockfiles, CMake integration.

## Verify
- `conan install . --build=missing`: dependencies resolve and build for the current profile.
- `conan create . --build=missing -tf=""`: the recipe builds as a package (drop `-tf=""` to also run test_package).
- `conan lock create .`: a lockfile pins the resolved graph.
- `conan graph info .`: the dependency graph and options are what you expect.

## Test first
A recipe's `test_package/` consumes the built package; write it first. It has its own conanfile with a `test()` method and a small program.
```python
from conan import ConanFile
from conan.tools.build import can_run

class TestPkg(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "CMakeDeps"
    def requirements(self):
        self.requires(self.tested_reference_str)
    def test(self):
        if can_run(self):
            self.run("./example", env="conanrun")
```
`conan create .` fails until the package exports what the example uses.

## Do
- Use the Conan 2 API (`from conan import ConanFile`) and declare tools via `generators = "CMakeDeps", "CMakeToolchain"`, `layout`: `cmake_layout(self)`.
- Prefer `conanfile.txt` for consumers with `[requires]`, `[generators]`; use `conanfile.py` when you need logic or a package recipe.
- Run CMake with the generated toolchain: `cmake --preset conan-release` (presets are written by `CMakeToolchain`).
- Put compiler, standard and build type in profiles (`conan profile detect`, `-pr:h`/`-pr:b` for host/build), not in the recipe.
- Use version ranges sparingly and commit a lockfile for applications.
- Declare `build_requires`-style tools as `tool_requires`, and package options with defaults in `options`/`default_options`.
- Implement `package_info` with `cpp_info.libs` and `set_property("cmake_target_name", ...)` so consumers link the right target.

## Avoid
- Conan 1 idioms (`conan install ..` with `-s` only, `build_requires`, `cmake_find_package`, `cmake_paths` generators, `self.cpp_info.names`): removed or renamed in 2. Use the 2 APIs above.
- Mixing settings between install and build (e.g. Release deps with a Debug build): use the same profile and `build_type` throughout.
- Skipping `--build=missing` on a clean cache and being surprised by missing binaries.
- Forgetting `-pr:b` for tool requirements when cross compiling: tools get built for the wrong platform.
- Hard-coding absolute paths or network access inside `build()`: recipes must be reproducible; use `source()` with checksums via `get(..., sha256=...)`.
- Editing a recipe without changing the version or revision and expecting caches to refresh: run `conan remove` or bump.

## Review
- [ ] Profiles define compiler/standard/build_type; the recipe does not.
- [ ] Applications commit a lockfile or pinned versions.
- [ ] `test_package` exists and passes for packages.
- [ ] Sources are downloaded with a checksum.
- [ ] Targets and libs in `package_info` match what consumers use.
