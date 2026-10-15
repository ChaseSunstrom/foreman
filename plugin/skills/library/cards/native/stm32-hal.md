---
name: stm32-hal
title: STM32 HAL and CubeMX
area: native
tags: [stm32, hal, cubemx, arm, embedded, c, interrupts, dma]
detect: [file:*.ioc, file:stm32*_hal_conf.h, file:startup_stm32*.s, file:STM32*_FLASH.ld]
related: [arm-cortex-m, embedded-c, freertos, platformio, cmake]
---
STM32 HAL: CubeMX project layout, USER CODE sections, interrupt-safe callbacks, DMA, timeouts and clock setup.

## Verify
- `cmake --build build -j` (or `make -j`): builds with `arm-none-eabi-gcc` and the CubeMX startup file and linker script.
- `arm-none-eabi-size build/app.elf`: flash and RAM use stay within the device limits.
- `arm-none-eabi-objdump -h build/app.elf | grep -E '\.text|\.data|\.bss'`: sections land in expected regions.
- `openocd -f interface/stlink.cfg -f target/stm32f4x.cfg -c "program build/app.elf verify reset exit"`: flash and verify (pick the matching target file).
- `ctest --test-dir build-host --output-on-failure`: host-built unit tests for logic, using the fake HAL.

## Test first
Keep logic out of the ISR and the HAL call sites; test it on the host with a fake.
```c
// tests/test_ring.c (host build)
#include <assert.h>
#include "ring.h"

int main(void) {
    ring_t r; ring_init(&r);
    for (int i = 0; i < RING_CAP; i++) assert(ring_put(&r, i));
    assert(!ring_put(&r, 99));           // full is reported, not overwritten
    return 0;
}
```

## Do
- Regenerate from the `.ioc` in CubeMX and put your code only between `/* USER CODE BEGIN x */` and `/* USER CODE END x */`: anything else is overwritten.
- Check every `HAL_StatusTypeDef` return; map `HAL_TIMEOUT` and `HAL_ERROR` to handled outcomes.
- Prefer interrupt or DMA transfers (`HAL_UART_Receive_DMA`, `HAL_ADC_Start_DMA`) over blocking calls with `HAL_MAX_DELAY`.
- Do the minimum in callbacks (`HAL_UART_RxCpltCallback`, `HAL_GPIO_EXTI_Callback`): set a flag or push to a queue; process in the main loop or a task.
- Mark flags shared with ISRs `volatile` and use atomic access for multi-byte values (`__disable_irq()` briefly, or C11 atomics).
- Use `HAL_GetTick()` differences (`now - start >= timeout`) for timeouts; it wraps safely with unsigned math.
- Set NVIC priorities deliberately, and under FreeRTOS keep API-calling ISR priorities numerically at or above `configMAX_SYSCALL_INTERRUPT_PRIORITY`.
- For DMA buffers on cache-equipped parts (F7, H7), place them in non-cacheable memory or clean and invalidate the D-cache.

## Avoid
- Editing generated code outside USER CODE blocks: lost on regeneration. Move logic to your own files.
- `HAL_Delay` in an ISR or with SysTick at lower priority than the caller: deadlock. Use flags and the main loop.
- `HAL_MAX_DELAY` timeouts: one stuck peripheral freezes the system. Use finite timeouts.
- `printf` with floats or heavy retarget in ISRs: slow and stack-hungry. Log via a queue.
- Forgetting to enable the peripheral clock (`__HAL_RCC_xxx_CLK_ENABLE`): silent no-op. Check the generated init order.
- Not clearing the wrong interrupt flag, or restarting DMA reception inside its own complete callback without re-arming: lost data.
- Large stack buffers in ISRs or tasks: overflow. Make them static or sized to the stack.

## Review
- [ ] Custom code sits only inside USER CODE regions or separate files.
- [ ] Every HAL status is checked, and timeouts are finite.
- [ ] ISR-shared data is `volatile` and accessed atomically.
- [ ] DMA buffers handle alignment and cache coherence.
- [ ] Flash and RAM headroom was measured with `arm-none-eabi-size`.
