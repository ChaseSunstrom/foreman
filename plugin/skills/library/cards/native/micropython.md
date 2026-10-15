---
name: micropython
title: MicroPython
area: native
tags: [micropython, python, microcontroller, esp32, rp2040, embedded, asyncio]
detect: [dep:micropython*, dep:mpremote, dep:mpy-cross, file:boot.py, file:mpconfigboard.h]
related: [esp-idf, embedded-c, platformio, arm-cortex-m]
---
MicroPython: mpremote workflow, boot.py vs main.py, memory discipline, interrupt handlers, asyncio and host-side tests.

## Verify
- `mpremote connect list`: the board is visible on a serial port.
- `mpremote fs cp main.py :main.py && mpremote reset`: copy and restart the board.
- `mpremote run script.py`: run a script on the device without saving it.
- `python -m pytest tests/`: pure-logic tests run on the host CPython.
- `mpy-cross -o out.mpy mod.py`: the module compiles to bytecode for the target version.

## Test first
Keep hardware access behind a small function and test logic on the host with a fake pin.
```python
# tests/test_debounce.py
from debounce import Debouncer

class FakePin:
    def __init__(self, vals): self.vals = iter(vals)
    def value(self): return next(self.vals)

def test_press_needs_three_equal_samples():
    d = Debouncer(FakePin([1, 0, 1, 1, 1]), samples=3)
    assert [d.read() for _ in range(5)][-1] == 1
```

## Do
- Keep `boot.py` minimal (network, pin states); put the app in `main.py` with a top-level `try/except` that logs and resets or enters a safe state.
- Use `machine.Pin`, `machine.I2C`, `machine.PWM` with explicit pin numbers from a single `config.py`.
- Preallocate buffers (`bytearray`) and use `memoryview` slices and `readinto` to avoid heap churn; call `gc.collect()` at known quiet points and check `gc.mem_free()`.
- Use `asyncio` (`import asyncio` on current builds) with `async def` and `asyncio.sleep_ms`; keep tasks cooperative.
- In `Pin.irq` handlers do minimal work: no allocation, no exceptions, no prints. Set a flag or use `micropython.schedule(fn, arg)`; mark with `@micropython.native` or `viper` only after profiling.
- Use `machine.WDT` in production code and feed it from the main loop.
- Freeze stable modules into firmware or use `.mpy` files to save RAM.
- Use `time.ticks_ms()`, `ticks_diff()` and `ticks_add()` for timing math.

## Avoid
- Allocating (f-strings, list appends, `str` concatenation) inside an IRQ handler: raises MemoryError or crashes. Preallocate, then schedule.
- Blocking `time.sleep` in an asyncio program: stalls every task. Use `await asyncio.sleep`.
- Comparing `time.ticks_ms()` values with `>=`: breaks at wraparound. Use `ticks_diff`.
- Large module imports at runtime on small heaps: fragmentation. Import early, or freeze.
- Infinite retry loops on Wi-Fi without backoff or a watchdog: bricks the field behavior. Add timeout and reset.
- Copying CPython-only libraries (threading, `typing` at runtime, full `json` options): missing. Check what the port supports.
- Storing Wi-Fi credentials in the repo: use a git-ignored `secrets.py`.

## Review
- [ ] Hardware pin and bus config lives in one file.
- [ ] No allocation in IRQ handlers; a flag or `schedule` is used.
- [ ] Time comparisons use ticks helpers.
- [ ] A watchdog or safe-state fallback exists in `main.py`.
- [ ] Logic is host-tested; device smoke test run with `mpremote`.
