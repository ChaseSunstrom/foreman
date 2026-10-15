---
name: esp-idf
title: ESP-IDF
area: native
tags: [esp-idf, esp32, freertos, cmake, firmware, idf-py]
detect: [file:sdkconfig, file:sdkconfig.defaults, file:partitions.csv, file:idf_component.yml, file:main/CMakeLists.txt]
related: [freertos, embedded-c, cmake, platformio]
---
ESP32 firmware with Espressif's IDF: components, Kconfig/sdkconfig, FreeRTOS tasks, idf.py workflow.

## Verify
- `idf.py set-target esp32 && idf.py build`: builds for the target (replace with the actual chip; the environment must be sourced with export.sh).
- `idf.py size-components`: flash and RAM per component.
- `idf.py -p /dev/ttyUSB0 flash monitor`: flashes and shows logs on a real board.
- `pytest --target esp32 --embedded-services idf,esp` in a test app: pytest-embedded runs on-device or QEMU tests (when pytest-embedded is installed).

## Test first
Logic goes in a component and is tested with Unity in the component's `test/` directory, built as a test app (`unit-test-app` or a project with `TEST_COMPONENTS`).
```c
#include "unity.h"
#include "ringbuf.h"

TEST_CASE("pop on empty fails", "[ringbuf]") {
    ringbuf_t r; uint8_t m[2]; ringbuf_init(&r, m, 2);
    TEST_ASSERT_FALSE(ringbuf_pop(&r, NULL));
}
```
Pure logic can also be built and tested on the host (Linux target) with `idf.py --preview set-target linux`.

## Do
- Keep each module as a component (`components/x/CMakeLists.txt` with `idf_component_register(SRCS ... INCLUDE_DIRS ... REQUIRES ... PRIV_REQUIRES ...)`).
- Declare third-party components in `idf_component.yml` and commit `dependencies.lock`.
- Configure through `menuconfig`, commit `sdkconfig.defaults` (per-target `sdkconfig.defaults.esp32s3`), and do not hand-edit `sdkconfig`.
- Check every `esp_err_t` with `ESP_ERROR_CHECK` (fatal) or `ESP_RETURN_ON_ERROR` / explicit handling for recoverable paths.
- Use `xTaskCreate`/`xTaskCreatePinnedToCore` with sized stacks, and `esp_log` (`ESP_LOGI(TAG, ...)`) not `printf`.
- Initialise NVS (`nvs_flash_init`), handle `ESP_ERR_NVS_NO_FREE_PAGES`, and register event handlers via `esp_event`.
- Define a `partitions.csv` when you need OTA or custom storage, and enable rollback/secure boot deliberately.

## Avoid
- Calling non-ISR FreeRTOS APIs from an ISR: use the `...FromISR` variants and `IRAM_ATTR` handlers.
- Blocking in event-loop or timer callbacks: they run in shared tasks and stall Wi-Fi/system events. Hand off to a task.
- Under-sized task stacks (silent corruption or `Stack canary watchpoint`): size, then check high water mark with `uxTaskGetStackHighWaterMark`.
- Editing `sdkconfig` and expecting it to be shared: it is generated; put intent in `sdkconfig.defaults`.
- Old `esp_wifi` or driver APIs copied from older examples (legacy `driver/i2c.h`, `driver/adc.h`): current releases offer newer driver APIs; check the version's docs.
- Hard-coding Wi-Fi credentials or keys in source: use Kconfig, NVS or provisioning.
- Using `delay` loops instead of `vTaskDelay`: they starve the idle task and trigger the task watchdog.

## Review
- [ ] Every `esp_err_t` is handled or checked.
- [ ] Task stacks and priorities are justified; ISRs only signal.
- [ ] `sdkconfig.defaults` carries all non-default config; lockfile committed.
- [ ] No secrets in source or sdkconfig.
- [ ] Partition table fits the image with OTA slack.
