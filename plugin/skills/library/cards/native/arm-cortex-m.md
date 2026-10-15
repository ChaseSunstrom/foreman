---
name: arm-cortex-m
title: ARM Cortex-M Firmware
area: native
tags: [arm, cortex-m, nvic, linker-script, startup, fault-handling, embedded]
detect: [file:*.ld, file:startup_*.s, file:*.svd, file:openocd.cfg]
related: [stm32-hal, embedded-c, freertos, zephyr, platformio]
---
Cortex-M bare-metal and RTOS firmware: startup, linker script, NVIC priorities, hard fault diagnosis, memory barriers and size budgets.

## Verify
- `arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -Wall -Wextra -c src/main.c`: the CPU and FPU flags match the part (adjust to your core).
- `arm-none-eabi-size -A build/app.elf`: `.text`, `.data`, `.bss` within flash and RAM limits.
- `arm-none-eabi-nm --size-sort -S build/app.elf | tail`: the largest symbols.
- `arm-none-eabi-objdump -d -j .isr_vector build/app.elf | head`: vector table sits at the start of flash with a valid initial SP.
- `arm-none-eabi-addr2line -e build/app.elf -f 0x08001234`: a faulting PC resolves to a source line.

## Test first
Test logic on the host. For a fault handler, the first failing check is a deliberate fault captured and decoded.
```c
// host test: decode a stacked frame
#include <assert.h>
#include "fault.h"
int main(void) {
    uint32_t frame[8] = {0,0,0,0,0,0, 0x08001234, 0x01000000};
    fault_info_t f = fault_decode(frame, /*cfsr*/ 1u << 17);  // INVSTATE
    assert(f.pc == 0x08001234 && f.invstate);
    return 0;
}
```

## Do
- Keep startup minimal: set the stack pointer from the vector table, copy `.data` from flash, zero `.bss`, set up clocks, call constructors, then `main`.
- Define memory regions in the linker script (`FLASH`, `RAM`, optionally `CCM`) and use `ASSERT` for stack and heap fit.
- Set priority grouping once, give each IRQ a deliberate priority, and note that lower numbers preempt; only the upper implemented bits count.
- Write a HardFault handler that captures the stacked registers (R0-R3, R12, LR, PC, xPSR) and reads `SCB->CFSR`, `HFSR`, `MMFAR`, `BFAR`.
- Use `volatile` for MMIO and ISR-shared values; use CMSIS `__DSB()`/`__ISB()` after writes that change VTOR, MPU or clock configuration.
- Thumb function pointers need the low bit set; use the toolchain's symbols and do not construct them by hand.
- Enable the FPU in startup (`SCB->CPACR |= (0xF << 20)`) before any float code on FPU parts.
- Compile with `-ffunction-sections -fdata-sections` and link with `-Wl,--gc-sections` plus `-Wl,-Map=app.map`.

## Avoid
- Enabling interrupts before `.data` and `.bss` initialization: ISRs read garbage. Do startup in order.
- A mismatched `-mfloat-abi` between objects and libraries: link errors or wrong ABI. Use one set of flags everywhere.
- Stack placed at the bottom of RAM with heap growing into it: silent corruption. Place the stack at the top with a guard and check high-water marks.
- Misaligned multi-byte access on Cortex-M0: HardFault. Use `memcpy` for packed data.
- Calling a non-reentrant function (`printf`, `malloc`) from both an ISR and a task: races. Keep ISRs short and defer.
- Using `delay` loops for timing: depends on optimization. Use a hardware timer or SysTick.
- Optimizing away MMIO reads and busy-wait flags for lack of `volatile`.

## Review
- [ ] Core, FPU and ABI flags match the part and are identical across the build.
- [ ] Linker script regions match the datasheet, and `size` shows headroom.
- [ ] A HardFault handler reports registers and the fault status registers.
- [ ] IRQ priorities are explicit and consistent with RTOS limits.
- [ ] MMIO and shared flags use `volatile` and barriers where needed.
