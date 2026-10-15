---
name: arm-assembly
title: ARM assembly
area: lang
tags: [assembly, arm, aarch64, abi, low-level, embedded]
detect: [ext:.s, ext:.S]
related: [c, x86-assembly, cmake]
---
ARM and AArch64 assembly: obey the procedure call standard, keep the stack aligned and test from a C harness.

## Verify
- `aarch64-linux-gnu-gcc -c -o out.o src.S`: assembles through the C preprocessor with a cross toolchain (use `arm-none-eabi-gcc` for 32-bit bare metal).
- `aarch64-linux-gnu-objdump -d out.o`: disassembly of what was produced.
- `qemu-aarch64 -L /usr/aarch64-linux-gnu ./prog`: runs the cross-built binary under user emulation, when qemu is installed.
- `file prog`: confirms the binary targets the intended architecture.

## Test first
Call the routine from C and assert on the result.
```c
#include <assert.h>
#include <stdint.h>
extern int64_t clamp(int64_t v, int64_t lo, int64_t hi);

int main(void) {
    assert(clamp(5, 0, 3) == 3);
    assert(clamp(-1, 0, 3) == 0);
    assert(clamp(2, 0, 3) == 2);
    return 0;
}
```
Cross-compile it with the assembly file and run under emulation, or natively on ARM hardware.

## Do
- Follow AAPCS64: arguments in x0-x7, return in x0, x19-x29 are callee-saved, x30 is the link register.
- Save `x29` and `x30` in the prologue (`stp x29, x30, [sp, #-16]!`) and restore them before `ret`, in any routine that calls another.
- Keep `sp` 16-byte aligned at all times on AArch64.
- On 32-bit ARM, follow AAPCS: args in r0-r3, callee-saved r4-r11, `lr` for return, and decide ARM versus Thumb state explicitly.
- Mark routines with `.global`, `.type name, %function` and `.size`, and put code in `.text`.
- Load constants with `mov` and `movk`, or `ldr` from a literal pool, and use `adrp` plus `:lo12:` for symbol addresses.
- Document the register contract above each routine.

## Avoid
- Overwriting `x30` with `bl` and then returning: you jump to yourself. Save the link register first.
- Misaligned `sp`: hardware faults on AArch64. Adjust in 16-byte steps.
- Confusing `w` and `x` registers: `w` writes zero the upper 32 bits. Use the right width for pointers and 64-bit values.
- x86 habits (flags everywhere, memory operands in arithmetic): ARM is load/store, so load into registers first.
- Assuming the branch range is unlimited: conditional branches have short reach. Use a trampoline or `b` when the target is far.
- Missing cache maintenance after writing code at runtime: use the sync barriers and instruction cache invalidation the architecture requires.
- Using x18: it is platform-reserved on several systems. Treat it as unavailable.

## Review
- [ ] AAPCS register use and stack alignment are respected.
- [ ] The link register is saved wherever there is a nested call.
- [ ] A cross-built test runs under emulation or on hardware.
- [ ] Register widths match the data type.
- [ ] Symbol addressing uses position-independent forms.
