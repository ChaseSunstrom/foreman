---
name: serial-uart
title: Serial and UART
area: hardware
tags: [serial, uart, rs232, rs485, framing, embedded, pyserial]
detect: [dep:pyserial, dep:serialport, dep:tokio-serial, dep:pyserial-asyncio, dep:go.bug.st/serial]
related: [i2c-spi, can-bus, raspberry-pi, ble]
---
Serial links: pick framing, timeouts and buffering deliberately, parse a byte stream with a state machine, and test with a loopback or fake port.

## Verify
- `python -m serial.tools.list_ports`: the expected port is present (pyserial).
- `python -m serial.tools.miniterm /dev/ttyUSB0 115200`: a manual session shows the device talking at that baud (port and speed are examples).
- `stty -F /dev/ttyUSB0 -a`: baud, parity and flow-control settings match the device (Linux).
- `pytest -q`: protocol tests pass against an in-memory stream with no device.

## Test first
Feed the parser bytes in awkward chunks. Frames must survive splits and noise.
```python
def test_frame_split_across_reads():
    p = Parser()
    out = []
    for chunk in (b"\x02\x05he", b"llo\x03\xAB"):
        out += p.feed(chunk)
    assert out == [b"hello"]

def test_bad_checksum_is_dropped_and_resyncs():
    p = Parser()
    out = p.feed(b"\x02\x01x\x03\x00" + b"\x02\x01y\x03" + bytes([checksum(b"y")]))
    assert out == [b"y"]
```

## Do
- Match both ends exactly: baud, data bits, parity, stop bits and flow control (commonly 8N1). Write them as one config object.
- Frame messages: a start byte or delimiter, a length, a payload and a checksum or CRC. Or use a newline for text protocols.
- Parse incrementally with a buffer and a state machine, resynchronising on the start byte after errors.
- Always set read and write timeouts. Treat a timeout as a normal event with defined handling.
- Read in a dedicated thread or an async task and hand frames over by a queue, so the main loop never blocks on the port.
- Put the port behind an interface (`read`, `write`, `close`) so tests can substitute a fake.
- Reconnect with backoff when the device unplugs, and close the port in a `finally`.
- Check voltage levels (3.3 V versus 5 V versus RS-232) and share ground before blaming software.

## Avoid
- Assuming one `read(n)` returns n bytes or one whole message: partial reads are normal. Accumulate into a buffer.
- Blocking read with no timeout: the program hangs forever when the device is silent. Set a timeout.
- Text decoding of binary frames: crashes on bad bytes. Decode only after framing, with `errors="replace"` for logs.
- Ignoring buffer overflow at high baud with slow readers: dropped bytes. Read continuously and use flow control if supported.
- Opening the same port from two processes: garbled or denied access. Hold one owner, and check permissions (dialout group on Linux).
- Using `readline()` on a binary protocol: breaks on a payload containing newline. Use length-prefixed framing.

## Review
- [ ] Line settings are in one config, matching the device documentation.
- [ ] Parser handles split frames, noise, bad checksums and resync, with tests.
- [ ] Every read and write has a timeout and a handled failure.
- [ ] Port is closed on every exit path and reconnects on unplug.
- [ ] Voltage levels and grounding are noted for the target wiring.
