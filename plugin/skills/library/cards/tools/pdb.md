---
name: pdb
title: pdb (Python debugger)
area: tools
tags: [python, pdb, debugger, breakpoint, pytest, post-mortem]
detect: [file:.pdbrc, file:pytest.ini, file:pyproject.toml]
related: [pytest, py-spy, memory-leaks, gdb-lldb]
---
Python's built-in debugger: breakpoints, post-mortem inspection and pytest integration.

## Verify
- `python -m pdb script.py ARGS`: runs under the debugger and stops at the first line or on an uncaught exception.
- `pytest -x --pdb`: drops into pdb at the first failing test.
- `pytest --trace tests/test_x.py::test_y`: stops at the start of one test.
- `PYTHONBREAKPOINT=0 pytest -q`: every leftover `breakpoint()` is disabled, so the suite runs unattended.

## Test first
Reproduce with a failing test, then inspect the failure state instead of adding prints.
```python
def test_total_with_discount():
    cart = Cart([Item("a", 100)])
    cart.apply("TEN")
    assert cart.total == 90   # fails: run `pytest -x --pdb`, then `p cart.__dict__`
```
Fix the code, keep the test.

## Do
- Insert `breakpoint()` (Python 3.7+); it honors `PYTHONBREAKPOINT` (set it to `0` to disable, or to another debugger's module).
- Commands: `n` (next), `s` (step in), `c` (continue), `r` (return), `l`/`ll` (list), `w` (stack), `u`/`d` (up/down), `p expr`, `pp expr`, `b file:line`, `b func`, `tbreak`, `cl` (clear), `unt`.
- Use `interact` to open a Python shell in the current frame.
- Post-mortem a crash: `python -m pdb -c continue script.py`, or `import pdb; pdb.post_mortem()` in an except block.
- Use conditional breakpoints: `b file.py:42, x > 3`.
- Put reusable commands in `.pdbrc`.
- Use `commands N` on a breakpoint to print values and continue, like a log point.
- For threads, async or remote processes, use `py-spy dump` or a remote debugger.

## Avoid
- Committing `breakpoint()`, `pdb.set_trace()` or `import pdb`: CI hangs waiting for stdin. Grep for them (`rg -n 'breakpoint\(\)|pdb\.set_trace'`) before commit.
- Debugging under pytest-xdist or with captured output: stdin is not a tty. Use `-s -n0`.
- Stepping into library internals for minutes: use `u`/`w` to read the stack, or `unt`, and set a breakpoint where your code resumes.
- Printing huge objects: use `pp` with a slice or `len`.
- Naming a variable like a pdb command (`c`, `n`, `l`): typing it runs the command. Use `p c` or `!c`.
- `import pdb` shadowed by a local `pdb.py`.

## Review
- [ ] No `breakpoint()` or `pdb.set_trace()` remains.
- [ ] The bug is pinned by a test that failed first.
- [ ] The root cause, not the symptom, is fixed.
- [ ] Tests run unattended in CI with `PYTHONBREAKPOINT=0` safe.
