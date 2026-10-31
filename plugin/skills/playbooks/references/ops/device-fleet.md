<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Keep a Raspberry Pi, MQTT or home automation setup running

Use when a headless Pi, a Home Assistant install, a ROS 2 robot or an MQTT sensor network goes quiet, reboots, or loses devices.

Built on the cards `fm lib show raspberry-pi`, `fm lib show home-assistant`, `fm lib show mqtt` and `fm lib show ros2`.

1. **Power and thermals first:** `vcgencmd get_throttled` must print `0x0`; undervoltage looks like random crashes and SD-card corruption.
2. **Is the service up?** `systemctl status <unit>` and `journalctl -u <unit> -b --no-pager | tail -50`. A restart loop names its reason there.
3. **Messages flowing?** One subscriber on the topic tree shows whether devices publish:
   ```bash
   mosquitto_sub -h localhost -t 'app/#' -v -C 1 -W 10
   ```
   A retained or last-will message tells you the last known state of a device.
4. **Home Assistant:** after any config edit, `hass --script check_config -c config` before restarting; an invalid config is the common cause of "everything vanished".
5. **ROS 2:** `ros2 node list` and `ros2 topic hz <topic>` show a dead node or a stalled publisher.
6. **Make it observable:** log to the journal, alert on silence for N minutes (see the observability playbook), and keep the SD card writes low.

Pass: the device publishes again for a full day with no throttling flags and no restarts in `journalctl`.

Stop when the fault is physical (power supply, cable, SD card) and say which.
