---
name: zephyr
title: Zephyr RTOS
area: native
tags: [zephyr, rtos, west, devicetree, kconfig, ztest]
detect: [file:prj.conf, file:west.yml, file:*.overlay, file:Kconfig, file:testcase.yaml]
related: [embedded-c, freertos, cmake, platformio]
---
Zephyr applications: west workspace, Kconfig (prj.conf), devicetree overlays, threads and ZTest.

## Verify
- `west build -b <board> app -p auto`: builds for a board (pristine when config changed).
- `west twister -T tests -p native_sim --inline-logs`: runs ZTest suites on the simulated board.
- `west build -t menuconfig`: the effective Kconfig options are what prj.conf intends.
- `west build -t rom_report` (or `ram_report`): memory use per symbol.

## Test first
Tests are ZTest suites under `tests/`, each with `prj.conf`, `testcase.yaml` and a `CMakeLists.txt`, run by Twister on `native_sim` or hardware.
```c
#include <zephyr/ztest.h>
#include "ringbuf_app.h"

ZTEST(ringbuf, test_pop_empty_fails) {
    struct rb r; uint8_t m[2]; rb_init(&r, m, 2);
    zassert_false(rb_pop(&r, NULL), "pop on empty must fail");
}
ZTEST_SUITE(ringbuf, NULL, NULL, NULL, NULL, NULL);
```
```yaml
tests:
  app.ringbuf:
    platform_allow: native_sim
```

## Do
- Select features with Kconfig in `prj.conf` (`CONFIG_GPIO=y`, `CONFIG_LOG=y`), per-board in `boards/<board>.conf`.
- Describe hardware in devicetree, adjust with `app.overlay` or `boards/<board>.overlay`; get devices with `DEVICE_DT_GET(DT_NODELABEL(x))` and check `device_is_ready()`.
- Use `K_THREAD_DEFINE` or `k_thread_create` with sized stacks; use `k_msgq`, `k_sem`, `k_work` to hand ISR work to threads.
- Log with `LOG_MODULE_REGISTER(name, LOG_LEVEL_INF)` and `LOG_INF/ERR`.
- Check return codes (negative errno) from every driver API.
- Manage dependencies in `west.yml` and pin revisions of module projects.
- Add `CONFIG_ASSERT=y` and `CONFIG_STACK_SENTINEL`/`CONFIG_THREAD_ANALYZER` during development.

## Avoid
- Editing `build/zephyr/.config` or expecting a changed prj.conf to apply on a stale build: rebuild with `-p`.
- Overlay node labels or property names guessed from memory: check the binding and the board's DTS; wrong names compile out the driver silently or fail the build.
- Skipping `device_is_ready()`: using an uninitialised device crashes later with no clue.
- Sleeping or locking in ISRs: use `k_work_submit` or a semaphore give; ISR-safe APIs only.
- Old header paths (`#include <zephyr.h>`, `<device.h>`, `<kernel.h>`) from pre-2.x-era examples: use `<zephyr/kernel.h>`, `<zephyr/device.h>`.
- Hard-coded GPIO pins and ports: derive them from devicetree aliases (`GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios)`).
- Unpinned west modules: builds change on `west update`.

## Review
- [ ] Hardware comes from devicetree, features from Kconfig; no board constants in C.
- [ ] Driver return codes and device readiness are checked.
- [ ] Tests run in Twister on `native_sim`.
- [ ] Thread stacks sized, priorities and ISR handoffs documented.
- [ ] west.yml revisions are pinned.
