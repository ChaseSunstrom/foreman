---
name: embedded-c
title: Embedded C
area: native
tags: [embedded, c, firmware, mcu, interrupts, volatile, misra]
detect: [file:*.ld, file:*.s, file:*.S, file:startup_*.c, file:openocd.cfg, file:*.svd]
related: [freertos, platformio, zephyr, esp-idf, sanitizers]
---
Bare-metal and RTOS firmware in C: registers, interrupts, memory limits, and testing logic on the host.

## Verify
- `arm-none-eabi-size build/firmware.elf`: flash and RAM use fit the part (text+data vs the linker script regions).
- `arm-none-eabi-gcc -Wall -Wextra -Wconversion -Wshadow -Wundef -fanalyzer -c src/driver.c -o /dev/null`: warnings and static analysis on the unit (substitute the target's toolchain prefix).
- `cppcheck --enable=warning,style --error-exitcode=1 src/`: static findings fail the build.
- `make -C test && ./test/run`: host-side unit tests of the logic (see below).

## Test first
Keep logic (parsers, state machines, ring buffers) free of register access and test it on the host with the native compiler and a small harness (Unity, CMocka, or plain asserts). Hardware goes behind a small struct of function pointers or link-time stubs.
```c
#include <assert.h>
#include "ringbuf.h"

void test_push_when_full_fails(void) {
    uint8_t mem[2]; ringbuf_t r; ringbuf_init(&r, mem, sizeof mem);
    assert(ringbuf_push(&r, 1) && ringbuf_push(&r, 2));
    assert(!ringbuf_push(&r, 3));
}
```

## Do
- Use `<stdint.h>` fixed-width types, and `static_assert` on struct sizes and register offsets.
- Mark memory-mapped registers and ISR-shared flags `volatile`; make shared multi-word data safe with a critical section or atomic access.
- Keep ISRs short: set a flag or push to a queue, process in the main loop or a task.
- Use fixed buffers and static allocation; no `malloc` after init (or none at all). Check stack depth with a linker map and stack watermarks.
- Put hardware access in a HAL layer with one header per peripheral; keep application logic hardware-free.
- Enable a watchdog and define reset-reason handling; verify clocks and pin muxing against the datasheet.
- Read the `.map` file when the image grows; use `-ffunction-sections -fdata-sections -Wl,--gc-sections`.

## Avoid
- `volatile` as a thread-safety fix: it prevents caching but not tearing or reordering. Use critical sections, atomics or disabling interrupts briefly.
- Calling blocking, `printf` or allocating functions from an ISR: undefined timing or deadlock. Defer to a task.
- Read-modify-write on a register shared with an ISR without protection: lost updates.
- Assuming `int` size, struct padding or endianness in wire formats: use fixed-width types and explicit (de)serialisation, never a struct cast.
- Shifting or comparing signed values with unsigned: UB and silent bugs. Enable `-Wconversion -Wsign-compare`.
- Busy-wait loops with no timeout on hardware flags: a dead peripheral hangs the device. Add a bounded timeout.
- Debug-only code paths (`assert`) that change behaviour in release: test the release build too.

## Review
- [ ] Image size is within flash/RAM budget with headroom; stacks are sized.
- [ ] ISR-shared data is volatile and protected; ISRs do no blocking work.
- [ ] Logic has host-side tests; hardware access is behind an interface.
- [ ] Every wait on hardware has a timeout and an error path.
- [ ] Warnings are on and treated as errors; no unexplained casts.
