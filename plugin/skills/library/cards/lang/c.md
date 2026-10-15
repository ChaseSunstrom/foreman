---
name: c
title: C
area: lang
tags: [c, gcc, clang, make, cmake, sanitizers, memory]
detect: [ext:.c, ext:.h, file:Makefile, file:CMakeLists.txt]
related: [cpp, rust, cmake]
---
C baseline: warnings as errors, sanitizers in test builds, bounds and ownership stated at every API, and a build that fails loudly.

## Verify
- `cc -std=c11 -Wall -Wextra -Werror -c src/foo.c -o /dev/null`: one file compiles warning-free (use the project's flags if it has a build).
- `make test` (or `ctest --test-dir build`): the project's own test target.
- `cc -g -fsanitize=address,undefined -fno-omit-frame-pointer ...`: a test build that traps overflows, use-after-free and UB.
- `valgrind --error-exitcode=1 ./test_bin`: leaks and invalid reads when sanitizers are unavailable.

## Test first
A tiny harness with `assert` or the project's (Unity, Check, cmocka). Test the boundary input.
```c
#include <assert.h>
#include <string.h>
#include "copy.h"

int main(void) {
    char dst[4];
    assert(safe_copy(dst, sizeof dst, "toolong") == -1);
    assert(safe_copy(dst, sizeof dst, "abc") == 0 && strcmp(dst, "abc") == 0);
    return 0;
}
```
Build tests without `-DNDEBUG`, or `assert` compiles away.

## Do
- Pass a length with every buffer; return an error code and check it at every call.
- Use `size_t` for sizes and indexes; check multiplication and addition overflow before `malloc`.
- Document ownership: who allocates, who frees; free in one place and set the pointer to NULL.
- Use `goto cleanup` for single-exit resource release.
- Use `snprintf`, `memcpy` with checked sizes, and `strnlen`.
- Initialize all variables; use `const` on read-only pointers and `static` on file-local functions.
- Compile with `-Wall -Wextra -Wconversion` plus a sanitizer build in CI.

## Avoid
- `gets`, `strcpy`, `strcat`, `sprintf`: unbounded writes. Use `fgets`, `snprintf` and explicit lengths.
- Unchecked `malloc` and `realloc`: NULL deref, and `p = realloc(p, n)` leaks on failure. Assign to a temp first.
- `scanf("%s")` with no width: overflow. Use `%Ns` or `fgets`.
- Signed overflow, shifting by the type width, or reading uninitialized memory: undefined behavior. Use unsigned arithmetic and checks.
- Returning a pointer to a local array: dangling. Allocate or take a caller buffer.
- `sizeof` on an array parameter: it is a pointer. Pass the length.
- Using the result of `strncpy` as a C string: may lack a terminator. Terminate explicitly.
- Comparing with `==` on floats or on strings: use `strcmp` and tolerances.

## Review
- [ ] Every buffer write is bounded by a checked length.
- [ ] Each allocation has one owner and one free; error paths release everything.
- [ ] Return values of allocators and I/O are checked.
- [ ] Test build ran under ASan and UBSan, warnings clean.
- [ ] No banned functions (`gets`, `strcpy`, `sprintf`).
