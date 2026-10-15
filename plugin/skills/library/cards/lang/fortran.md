---
name: fortran
title: Fortran
area: lang
tags: [fortran, fpm, gfortran, modules, numerics, test-drive]
detect: [ext:.f90, ext:.f95, ext:.f03, ext:.f08, ext:.F90, file:fpm.toml]
related: [bash]
---
Modern Fortran (2008+): modules, explicit interfaces, `implicit none`, fpm builds, numerical care.

## Verify
- `fpm build --flag "-Wall -Wextra -fcheck=all"`: builds with gfortran warnings and runtime bounds/pointer checks.
- `fpm test --flag "-fcheck=all -ffpe-trap=invalid,zero,overflow"`: tests trap NaN, divide-by-zero and overflow.
- `gfortran -fsyntax-only -Wall -std=f2018 src/mod.f90`: syntax and standards conformance without linking.
- `fpm run`: the app target runs, for `[[executable]]` projects.

## Test first
fpm discovers tests in `test/`; the `test-drive` package is a common harness (`[dev-dependencies]` in `fpm.toml`). A bare-bones test also works: stop with a non-zero code on failure.
```fortran
program test_parse
  use parse, only: parse_int
  implicit none
  integer :: n
  logical :: ok

  call parse_int("", n, ok)
  if (ok) error stop "blank input must be rejected"
  call parse_int("42", n, ok)
  if (.not. ok .or. n /= 42) error stop "42 must parse"
end program test_parse
```
`error stop` makes `fpm test` report the failure.

## Do
- Put every procedure in a module and `use` it; modules give explicit interfaces and catch argument mismatches at compile time.
- Start every unit with `implicit none`, and declare `intent(in|out|inout)` on all dummy arguments.
- Select kinds with `iso_fortran_env` (`real64`, `int32`) or `selected_real_kind`, not `real*8` or `double precision`.
- Use `allocatable` arrays and `pure`/`elemental` procedures; avoid raw `pointer` unless needed.
- Compare floats with a tolerance (`abs(a - b) <= tol * max(abs(a), abs(b))`), and use array operations over hand loops when clear.
- Check I/O with `iostat=` and `iomsg=`, and use `newunit=` to open files.
- Keep a free-form `.f90` layout and set `[build]` options in `fpm.toml`.

## Avoid
- Implicit typing (no `implicit none`): a typo creates a new variable silently. Add the statement everywhere.
- Mixing default `real` with `real64` literals: `1.0` is single precision. Write `1.0_real64`.
- Row-major loop order: Fortran arrays are column-major, so the first index should vary fastest in the inner loop.
- Passing array slices or mismatched ranks to external routines without an interface: wrong results. Use modules.
- `stop` inside library routines: kills the host program with no context. Return a status and let the caller decide.
- Uninitialized variables and uncleared `allocatable` assumptions: undefined values. Initialize, and test with `-finit-real=snan` when debugging.
- `equivalence`, `common` blocks and `goto`: obsolescent. Use modules and structured control flow.

## Review
- [ ] `implicit none` and `intent` are present in every new procedure and module.
- [ ] Build with `-Wall -Wextra -fcheck=all` emits no new warnings and the tests pass.
- [ ] Floating-point kinds are explicit, and comparisons use tolerances.
- [ ] I/O statements check `iostat`, and units are closed.
- [ ] Array loop order and allocation sizes are sensible for large inputs.
