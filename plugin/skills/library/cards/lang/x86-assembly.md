---
name: x86-assembly
title: x86 assembly
area: lang
tags: [assembly, x86, x86-64, nasm, abi, low-level]
detect: [ext:.asm, ext:.nasm, ext:.inc]
related: [c, arm-assembly, cmake]
---
x86-64 assembly: follow the platform calling convention, preserve callee-saved registers and test from a C harness.

## Verify
- `nasm -f elf64 -Wall -o out.o src.asm`: assembles with warnings on (use `-f macho64` or `-f win64` on those platforms).
- `objdump -d -M intel out.o`: disassembly shows the encoding you intended.
- `gcc -o prog main.c out.o`: links against a C test driver.
- `valgrind ./prog`: catches stack and memory misuse in the harness on Linux.

## Test first
Call the routine from C and assert on the result.
```c
#include <assert.h>
#include <stdint.h>
extern int64_t add3(int64_t a, int64_t b, int64_t c);

int main(void) {
    assert(add3(1, 2, 3) == 6);
    assert(add3(-1, 1, 0) == 0);
    return 0;
}
```
Implement `add3` in the assembly file to make it pass, and keep the C driver beside it.

## Do
- Know the ABI: System V passes integer args in rdi, rsi, rdx, rcx, r8 and r9 and returns in rax. Windows x64 uses rcx, rdx, r8 and r9 plus 32 bytes of shadow space.
- Preserve callee-saved registers (rbx, rbp, r12-r15 on System V) and restore them before `ret`.
- Keep the stack 16-byte aligned at every `call`.
- Declare `global`, `section .text`, and mark the stack non-executable with `section .note.GNU-stack noexec` on Linux.
- Use rip-relative addressing (`default rel`) for position-independent code.
- Comment each block with the register contract: inputs, outputs and clobbers.
- Use `xor eax, eax` to zero and `lea` for address and simple arithmetic.
- Test edge values: zero, negative, maximum and unaligned inputs.

## Avoid
- Clobbering callee-saved registers: the caller crashes later and far away. Push them and pop in reverse.
- A misaligned stack at `call`: SSE instructions in libc fault. Adjust with `sub rsp, 8` or an even number of pushes.
- Assuming 32-bit writes keep upper bits: writing `eax` zero-extends to rax, but writing `ax` or `al` does not. Know which you want.
- Mixing up AT&T and Intel operand order: the source and destination swap. Pick one syntax per project.
- `int 0x80` in 64-bit code: it uses the 32-bit ABI. Use `syscall` with the 64-bit numbers.
- Writing below rsp and relying on it: signal handlers overwrite it, apart from the red zone rules. Reserve the space with `sub rsp`.
- Relying on flags across a `call`: they are not preserved.

## Review
- [ ] Register contract documented per routine.
- [ ] Callee-saved registers are preserved and the stack is aligned.
- [ ] Each routine has a C-driven test with edge values.
- [ ] Syscalls and ABI match the target OS.
- [ ] No hardcoded addresses where relative addressing is possible.
