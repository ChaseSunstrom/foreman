---
name: can-bus
title: CAN bus
area: hardware
tags: [can, canbus, socketcan, dbc, automotive, embedded]
detect: [dep:python-can, dep:cantools, dep:socketcan, dep:can-dbc]
related: [serial-uart, i2c-spi, raspberry-pi]
---
CAN and CAN FD messaging: SocketCAN interfaces on Linux, DBC-defined signals, arbitration IDs, bit timing and termination, tested with a virtual interface.

## Verify
- `ip -details link show can0`: the interface is up with the expected bitrate, state and error counters (Linux).
- `candump can0`: frames from the bus are visible (can-utils).
- `cansend can0 123#DEADBEEF`: a frame is transmitted and another node or `candump` sees it.
- `pytest -q`: signal encoding and decoding tests pass against a DBC file and a virtual bus.

## Test first
Test encoding with the DBC, and run the app against SocketCAN's virtual interface or python-can's virtual bus.
```python
import can, cantools

db = cantools.database.load_file("vehicle.dbc")

def test_speed_signal_roundtrip():
    msg = db.get_message_by_name("Speed")
    data = msg.encode({"Kph": 88.5})
    assert abs(msg.decode(data)["Kph"] - 88.5) < 0.1

def test_app_replies_on_virtual_bus():
    with can.Bus(interface="virtual", channel="t") as a, \
         can.Bus(interface="virtual", channel="t") as b:
        a.send(can.Message(arbitration_id=0x100, data=[1], is_extended_id=False))
        assert b.recv(1.0).arbitration_id == 0x100
```

## Do
- Define messages and signals in a DBC file (or equivalent) and generate codecs from it. Keep one source of truth for IDs, scaling, units and byte order.
- Set the same bitrate on every node, and for CAN FD set the data-phase bitrate and sample points. Terminate with 120 ohms at each end of the bus only.
- Mind standard (11-bit) versus extended (29-bit) IDs. Pass `is_extended_id` explicitly.
- Use lower IDs for higher priority, and keep cyclic messages on fixed periods with a timeout check on the receiver.
- Filter in the kernel or adapter (`can_filters`) to cut load.
- Handle bus-off and error frames: log counters, back off, and re-enable the interface with a limit.
- Add a rolling counter and checksum to safety-relevant messages, and validate them on receive.

## Avoid
- Bit-shifting signals by hand: byte-order and sign errors (Intel versus Motorola). Use the DBC codec.
- Termination at every node or none: reflections and error frames. Exactly two 120 ohm terminators (about 60 ohm measured across CAN_H and CAN_L).
- Flooding at 100 percent bus load: arbitration loss and starvation. Budget the load under about 50 to 70 percent.
- Blocking `recv` with no timeout: hangs on silence. Use timeouts and a `Notifier` or thread.
- Mixed bitrates on one bus: error storms. Align every node.
- Testing only on real hardware: slow and flaky. Use `vcan0` (`ip link add dev vcan0 type vcan`) or the virtual interface.

## Review
- [ ] IDs, scaling and byte order come from one DBC, with round-trip tests.
- [ ] Bitrate, ID width and termination are documented for the target bus.
- [ ] Receive paths have timeouts, counters and bus-off recovery.
- [ ] Cyclic messages have period and staleness checks.
- [ ] Tests run on a virtual bus in CI.
