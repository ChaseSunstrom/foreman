---
name: ble
title: Bluetooth Low Energy
area: hardware
tags: [ble, bluetooth, gatt, central, peripheral, mtu, bleak]
detect: [dep:bleak, dep:@abandonware/noble, dep:noble, dep:btleplug, dep:flutter_blue_plus, dep:react-native-ble-plx, dep:bleno]
related: [serial-uart, mqtt, raspberry-pi]
---
BLE clients and peripherals: scan, connect, discover GATT, subscribe to notifications, with timeouts, reconnection and a fake device for tests.

## Verify
- `bluetoothctl scan on`: the device advertises and is visible from this host (BlueZ on Linux).
- `bluetoothctl info AA:BB:CC:DD:EE:FF`: services, RSSI and connection state for a device (address is an example).
- `pytest -q`: protocol and reconnect tests pass against a fake client with no radio.

## Test first
Hide the BLE library behind a small client interface. Test parsing and reconnect logic with a fake.
```python
class FakeLink:
    def __init__(self): self.handlers, self.connected = {}, False
    async def connect(self): self.connected = True
    async def start_notify(self, uuid, cb): self.handlers[uuid] = cb
    def push(self, uuid, data): self.handlers[uuid](None, bytearray(data))

async def test_heart_rate_parses_8bit_and_16bit():
    link, got = FakeLink(), []
    dev = HeartRate(link, got.append)
    await dev.start()
    link.push(HR_UUID, [0x00, 72])
    link.push(HR_UUID, [0x01, 0x2C, 0x01])
    assert got == [72, 300]
```

## Do
- Scan with a service-UUID filter and a timeout, and connect by address or by name from the advertisement data.
- Discover services after connecting, then read, write or subscribe by characteristic UUID, never by cached handle.
- Subscribe to notifications rather than polling, and write the CCCD through the library's `start_notify`.
- Parse with explicit struct formats (`struct.unpack("<H", ...)`), using the profile's flags and byte order.
- Respect the MTU: default payload is 20 bytes (MTU 23). Request a larger MTU where supported and chunk longer writes.
- Set a connect timeout and reconnect with backoff on disconnect callbacks, resubscribing after each reconnect.
- Use write-with-response for commands and write-without-response only for streaming.
- Bond or encrypt for anything sensitive, and never rely on an advertised name for identity.

## Avoid
- Treating the connection as permanent: links drop on range, power and OS suspend. Handle the disconnect callback and resubscribe.
- Connecting while scanning on one adapter: failures and slowness on many stacks. Stop the scan first.
- Caching addresses on macOS or iOS as stable: the OS hides MAC addresses and uses per-device UUIDs. Store what the platform gives you.
- Multiple concurrent connection attempts to one peripheral: BlueZ reports "operation in progress". Serialise connects with a lock.
- Writing more than the MTU in one call without chunking: truncated or failed writes. Chunk to MTU minus 3.
- Parsing notifications assuming one per packet: fragmentation is protocol-defined. Use your own framing on long messages.

## Review
- [ ] BLE library calls sit behind an interface with a fake in tests.
- [ ] Scan, connect and every GATT operation have timeouts.
- [ ] Disconnect triggers reconnect with backoff and resubscribe.
- [ ] Payload parsing is tested with flags, byte order and short packets.
- [ ] Pairing, permissions and platform differences are documented.
