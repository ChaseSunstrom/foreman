---
name: freertos
title: FreeRTOS
area: native
tags: [freertos, rtos, tasks, queues, interrupts, embedded]
detect: [file:FreeRTOSConfig.h, file:tasks.c, file:FreeRTOS*]
related: [embedded-c, esp-idf, zephyr, platformio]
---
FreeRTOS firmware: tasks, queues, semaphores and timers, with ISR-safe handoff and sized stacks.

## Verify
- `grep -nE "configASSERT|configCHECK_FOR_STACK_OVERFLOW|configUSE_MALLOC_FAILED_HOOK" FreeRTOSConfig.h`: assertions, stack-overflow and malloc-failed checks are enabled.
- `arm-none-eabi-size build/firmware.elf`: static RAM (heap array plus task stacks) fits (use the target's toolchain prefix).
- `make -C test && ./test/run`: logic tested on the host with the POSIX port or with FreeRTOS calls stubbed.
- `grep -rn "FromISR" src/ | head`: ISR code uses the `FromISR` variants.

## Test first
Test the logic that tasks call, not the tasks. Keep task bodies thin; pass the queue/handles in so the logic runs in a host test without the scheduler.
```c
#include <assert.h>
#include "cmd_parser.h"

void test_parser_rejects_overlong_frame(void) {
    uint8_t f[300] = {0};
    assert(cmd_parse(f, sizeof f) == CMD_ERR_LEN);
}
```
For scheduling behaviour, use the POSIX/Linux simulator port and assert on a queue's content after a bounded `vTaskDelay`.

## Do
- Enable `configASSERT` and `configCHECK_FOR_STACK_OVERFLOW 2`, implement `vApplicationStackOverflowHook` and `vApplicationMallocFailedHook`.
- Size stacks in words (not bytes) and measure with `uxTaskGetStackHighWaterMark`; leave margin.
- Use queues, task notifications or semaphores for ISR-to-task signalling; call `xQueueSendFromISR` and finish with `portYIELD_FROM_ISR(woken)`.
- Block with timeouts (`pdMS_TO_TICKS(ms)`) and handle the timeout result; never `portMAX_DELAY` without a plan for a stuck peer.
- Use mutexes (priority inheritance) for shared resources and binary semaphores for signalling.
- Create all tasks and objects before `vTaskStartScheduler()`, and check returned handles for NULL.
- Set interrupt priorities for ISRs that call FreeRTOS at or below `configMAX_SYSCALL_INTERRUPT_PRIORITY` (numerically >=).

## Avoid
- Calling a non-ISR API (`xQueueSend`, `vTaskDelay`, `xSemaphoreTake`) from an ISR: use `FromISR` forms.
- Sharing data between tasks with a global and `volatile` only: use a queue, notification or mutex.
- Using a mutex from an ISR or to signal between tasks: use a semaphore or notification.
- Stack-heavy locals (big buffers, `printf` with floats) in small-stack tasks: move to static storage or enlarge the stack.
- `vTaskDelay` for periodic work: it drifts. Use `vTaskDelayUntil` (or `xTaskDelayUntil`) or a software timer.
- Long work in timer callbacks: they run in the timer service task and delay all timers. Notify a task.
- Deleting tasks that hold resources, or `heap_1` with dynamic delete: choose the heap scheme (`heap_4`) to match the allocation pattern.
- Priority inversions through unbounded busy loops at high priority: starve lower tasks and the idle task (watchdog trips).

## Review
- [ ] Every ISR-called API is a `FromISR` variant with correct yield handling.
- [ ] Stack sizes have measured headroom; overflow hook enabled.
- [ ] Shared state uses a queue or lock; no priority-inversion path.
- [ ] Blocking calls have timeouts with error handling.
- [ ] Heap scheme and `configTOTAL_HEAP_SIZE` match worst-case use.
