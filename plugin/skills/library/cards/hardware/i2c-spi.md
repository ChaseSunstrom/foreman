---
name: i2c-spi
title: I2C and SPI buses
area: hardware
tags: [i2c, spi, sensors, embedded, linux, bus]
detect: [dep:smbus2, dep:spidev, dep:adafruit-circuitpython-busdevice, dep:rppal, dep:smbus]
related: [raspberry-pi, serial-uart, can-bus]
---
I2C and SPI peripherals: confirm wiring and addresses from the shell, wrap bus access in a small driver that tests can fake, handle NACKs and timing.

## Verify
- `i2cdetect -y 1`: the device ACKs at its expected address on bus 1 (i2c-tools; bus number varies by board).
- `i2cget -y 1 0x68 0x75`: a register read returns the datasheet's identity value (address and register are examples).
- `ls /dev/i2c-* /dev/spidev*`: the bus nodes exist, meaning the interface is enabled in the OS.
- `pytest -q`: driver tests pass against a fake bus with no hardware.

## Test first
Give the driver a bus object it calls. Test decoding with a fake that returns scripted bytes.
```python
class FakeBus:
    def __init__(self, regs): self.regs, self.writes = regs, []
    def read_i2c_block_data(self, addr, reg, n): return self.regs[reg][:n]
    def write_byte_data(self, addr, reg, val): self.writes.append((reg, val))

def test_temperature_decodes_signed_16bit():
    bus = FakeBus({0x00: [0xFF, 0x38]})        # -200 raw
    assert Sensor(bus, 0x48).raw_temp() == -200

def test_init_writes_config_once():
    bus = FakeBus({0x75: [0x68]})
    Sensor(bus, 0x68).begin()
    assert bus.writes == [(0x6B, 0x00)]
```

## Do
- Read the datasheet for address, register map, endianness, and signed or unsigned fields. Put them in named constants.
- Check the identity (WHO_AM_I) register at startup and fail loudly on mismatch.
- On I2C, use block reads for multi-byte values to get a coherent sample, and keep transfers short.
- On SPI, set mode (CPOL and CPHA), clock speed and bit order to the datasheet. Hold chip select for the whole transaction.
- Retry transient I2C errors a few times with a short delay, then raise a typed error.
- Wait the datasheet's conversion or settling time between configuring and reading.
- Add a calibration offset and scale per device: real sensors read off.
- Share one bus object with a lock if multiple threads use it.

## Avoid
- Assuming the address: 7-bit versus 8-bit notation (0x68 versus 0xD0) shifts it. Use the 7-bit address that `i2cdetect` shows.
- Missing or weak pull-ups on I2C: random NACKs. Check 2.2k to 10k to the supply rail, and the logic level (3.3 V versus 5 V).
- Too-fast SPI over long wires: corrupted reads. Lower the clock until stable, then measure.
- Forgetting that SPI is full duplex: a read must clock out dummy bytes. Send zeros of the same length.
- Sharing one chip select between devices: bus contention. One CS per device.
- Reading before the sensor is ready: stale or zero values. Poll the ready flag or wait the conversion time.

## Review
- [ ] Bus access sits behind an interface that tests fake.
- [ ] Identity register is checked at init.
- [ ] Mode, speed and address are named constants taken from the datasheet.
- [ ] Errors and retries are bounded and surface a clear exception.
- [ ] Units, signedness and calibration are tested.
