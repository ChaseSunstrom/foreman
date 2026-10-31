<!-- Foreman's own playbook (written for Foreman, not ported). -->
# A device on a serial, I2C, CAN or BLE link does not answer

Use when hardware does not respond, answers garbled bytes, loses frames of data or only works sometimes.

Built on the cards `fm lib show serial-uart`, `fm lib show i2c-spi`, `fm lib show can-bus`, `fm lib show ble`, `fm lib show mqtt` and `fm lib show raspberry-pi`.

1. **Prove the link before the code.** Power, ground, wiring, the node exists:
   ```bash
   python -m serial.tools.list_ports
   i2cdetect -y 1
   ip -details link show can0
   bluetoothctl info AA:BB:CC:DD:EE:FF
   vcgencmd get_throttled     # 0x0 means no undervoltage
   ```
2. **Watch the wire with a second tool** (`candump can0`, `miniterm`, `mosquitto_sub -t 'app/#' -v`) so you see what is sent and received without your code in the way.
3. **Garbage is almost always framing:** baud, parity, stop bits, voltage level, or a missing newline terminator. Check `stty -F /dev/ttyUSB0 -a` against the datasheet.
4. **Intermittent means timing:** a read without a timeout, a bus shared with another process, a reconnect that never fires. Add a timeout and a retry cap with a named error.
5. **Reproduce in software:** a loopback or fake port test with the captured bytes (`pytest -q`), then fix the parser or driver.

Pass: the second tool and your code agree on the traffic, and a test replays the failing capture.

Stop and ask for hands-on help for wiring, voltage or termination problems; code cannot fix them.
