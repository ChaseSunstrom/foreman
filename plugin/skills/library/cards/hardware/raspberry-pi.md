---
name: raspberry-pi
title: Raspberry Pi
area: hardware
tags: [raspberry-pi, gpio, linux, embedded, gpiozero, systemd]
detect: [dep:gpiozero, dep:RPi.GPIO, dep:lgpio, dep:picamera2, dep:smbus2, dep:spidev, dep:rpi-lgpio]
related: [python, systemd, mqtt]
---
Raspberry Pi projects: GPIO, I2C and SPI from Python, Raspberry Pi OS services, headless operation.

## Verify
- `pinctrl get`: current pin functions and levels on Raspberry Pi OS (confirms wiring and overlays).
- `vcgencmd get_throttled`: `0x0` means no undervoltage or thermal throttling.
- `i2cdetect -y 1`: the expected I2C device addresses respond on bus 1.
- `GPIOZERO_PIN_FACTORY=mock pytest -q`: tests run on any machine with mock pins.
- `systemctl status myapp.service`: the service is active and not restart-looping.

## Test first
gpiozero ships a mock pin factory; drive pins in tests without hardware.
```python
from gpiozero import Device, LED, Button
from gpiozero.pins.mock import MockFactory

def setup_function():
    Device.pin_factory = MockFactory()

def test_button_turns_led_on():
    led, btn = LED(17), Button(2)
    btn.pin.drive_low()          # press (active low with pull-up)
    app_tick(led, btn)
    assert led.is_lit
```
Keep hardware access behind a small class with an interface so logic tests pass fakes. Mark real-hardware tests and run them only on the device.

## Do
- Use `gpiozero` (or `lgpio`) for GPIO; it works on Pi 5 and handles cleanup on exit.
- Identify pins by BCM number and document the wiring in the README.
- Enable I2C, SPI or camera through `raspi-config` non-interactive mode or `config.txt` overlays under `/boot/firmware`.
- Run long-lived programs as a systemd unit with `Restart=on-failure`, a dedicated user in the `gpio`, `i2c`, `spi` groups, and `WorkingDirectory` set.
- Debounce inputs (`bounce_time`) and treat sensor reads as fallible: retry, timeout, validate range.
- Use a hardware watchdog or a heartbeat when it must stay unattended.
- Write to SD sparingly: log to RAM or journald with limits; use `tmpfs` for scratch.
- Provide an adequate supply and check throttling before blaming software.

## Avoid
- `RPi.GPIO` on a Pi 5: it does not work there. Use `gpiozero` with lgpio, or the `rpi-lgpio` compatibility package.
- Running scripts as root with `sudo` to reach GPIO: add the user to the right groups instead.
- Polling in a tight loop: pegs a core. Use edge callbacks (`when_pressed`) or sleep.
- `pip install` into the system Python on current Raspberry Pi OS: externally-managed error. Use a venv (`python -m venv --system-site-packages` if you need apt-provided libs such as picamera2).
- Editing `/boot/config.txt` on current images: the file lives at `/boot/firmware/config.txt`.
- Hardcoding 3.3 V assumptions: GPIO is not 5 V tolerant. Use a level shifter.
- Forgetting pull-ups on I2C or floating inputs: random reads. Set `pull_up` explicitly.

## Review
- [ ] Logic is testable with the mock pin factory; hardware access is isolated.
- [ ] The service runs as a non-root user with `Restart=` set.
- [ ] Pin numbering is BCM and documented; voltage levels are safe.
- [ ] Inputs are debounced and sensor errors handled.
- [ ] Setup steps (interfaces, packages, venv) are scripted or in the README.
