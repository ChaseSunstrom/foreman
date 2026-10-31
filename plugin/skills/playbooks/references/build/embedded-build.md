<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Embedded firmware build failures

Use when firmware will not build or link: PlatformIO, ESP-IDF, Zephyr or STM32 projects, a Cortex-M linker script, or an overflowing flash or RAM region.

Built on the cards `fm lib show platformio`, `fm lib show esp-idf`, `fm lib show zephyr`, `fm lib show stm32-hal`, `fm lib show arm-cortex-m` and `fm lib show cmake`.

1. **Confirm the target and toolchain** before reading errors: a wrong board or an unsourced environment makes everything fail.
   ```bash
   pio run -e <env> 2>&1 | tail -40
   idf.py set-target esp32 && idf.py build      # after sourcing export.sh
   west build -b <board> -p auto
   arm-none-eabi-gcc --version
   ```
2. **Separate compile, link and size errors.** `undefined reference` is a missing source, library or `extern "C"`; `region 'FLASH' overflowed` or `will not fit in region` is size, not a bug in the line it names.
3. **Size errors:** read the map file or `size`/`idf.py size-components` and find the biggest contributor first. Lower `-O` level or turn off logging only with the owner's say-so.
4. **Config errors** (`sdkconfig`, `prj.conf`, `platformio.ini`): change the source file (`sdkconfig.defaults`, `prj.conf`), never the generated copy, and rebuild clean once.
5. **Host test the logic** that does not need the chip: `pio test -e native`.

Pass: the build exits 0 for the real target, `size` shows the regions inside their limits, and `pio check -e <env> --fail-on-defect=medium` (when configured) still passes.

Stop when the failure is hardware-only (flash, boot or hard fault): hand it to the serial and bus playbook with the board attached.
