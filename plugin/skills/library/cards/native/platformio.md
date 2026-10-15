---
name: platformio
title: PlatformIO
area: native
tags: [platformio, embedded, arduino, firmware, unity, mcu]
detect: [file:platformio.ini, dep:platformio]
related: [embedded-c, freertos, esp-idf, zephyr]
---
PlatformIO projects: platformio.ini environments, `pio` CLI builds, native and on-device Unity tests.

## Verify
- `pio run -e <env>`: the environment builds.
- `pio test -e native`: Unity tests run on the host (needs a `[env:native]` with `platform = native`).
- `pio check -e <env> --fail-on-defect=medium`: static analysis fails on medium or higher defects.
- `pio run -e <env> -t size`: flash and RAM use after the build.

## Test first
Tests live in `test/` (one folder per suite, `test_*` prefixed) and use Unity. Put pure logic in `lib/` so the `native` env can test it.
```ini
[env:native]
platform = native
test_framework = unity
```
```c
#include <unity.h>
#include "ringbuf.h"

void test_pop_empty_fails(void) {
    ringbuf_t r; uint8_t m[2]; ringbuf_init(&r, m, 2);
    TEST_ASSERT_FALSE(ringbuf_pop(&r, NULL));
}
int main(void) { UNITY_BEGIN(); RUN_TEST(test_pop_empty_fails); return UNITY_END(); }
```
`pio test -e native` fails until the logic is correct.

## Do
- Define one `[env:name]` per board and share settings in `[env]` or a `[common]` section with `${common.build_flags}`.
- Pin `platform = name@x.y.z` and `lib_deps = owner/Library@^1.2.3` so builds are reproducible.
- Set `framework`, `board`, `monitor_speed` and `upload_protocol` explicitly.
- Use `build_flags = -Wall -Wextra -DFEATURE_X` for compile-time options and `build_src_filter` to exclude files per env.
- Put reusable, testable code in `lib/<name>/`, hardware entry points in `src/`.
- Use `extra_scripts` (pre/post Python) only for things the config cannot express.
- Commit `platformio.ini`; ignore `.pio/`.

## Avoid
- Unpinned `platform` and `lib_deps`: a registry update breaks the build later. Pin versions.
- Testing only on-device: slow and not CI friendly. Add a `native` env for logic.
- Putting Arduino `setup()`/`loop()` logic in untestable `main.cpp`: move logic into a library that takes dependencies as arguments.
- Using `#include` of libraries not listed in `lib_deps`: it works from a global cache and fails on a clean machine.
- Mixing board-specific flags into `[env]` shared by other boards: use per-env `build_flags`.
- Running `pio upload` in CI without a device: use `pio run` and `pio test -e native`.

## Review
- [ ] platform and libraries are version pinned.
- [ ] A `native` env runs the logic tests.
- [ ] `pio check` and `-Wall -Wextra` are clean.
- [ ] `.pio/` is gitignored; secrets are not in platformio.ini (use `build_flags` from env vars `${sysenv.NAME}`).
- [ ] Flash/RAM use has headroom per board.
