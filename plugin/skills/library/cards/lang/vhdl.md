---
name: vhdl
title: VHDL
area: lang
tags: [vhdl, hdl, fpga, rtl, simulation, hardware]
detect: [ext:.vhd, ext:.vhdl]
related: [verilog, systemverilog]
---
VHDL RTL design: synchronous processes, `numeric_std` types, and self-checking testbenches run in a simulator.

## Verify
- `ghdl -a --std=08 src/*.vhd tb/*.vhd`: analyzes all files (VHDL-2008) and catches type and syntax errors.
- `ghdl -e --std=08 tb_top`: elaborates the testbench entity.
- `ghdl -r --std=08 tb_top --assert-level=error`: runs the simulation and exits non-zero on a failed assertion.
- `ghdl -r --std=08 tb_top --wave=out.ghw`: dumps a waveform for inspection.

## Test first
A self-checking testbench with `assert` and an explicit end of simulation.
```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_adder is end;
architecture sim of tb_adder is
  signal a, b, s : unsigned(7 downto 0);
begin
  dut : entity work.adder port map (a => a, b => b, s => s);
  process begin
    a <= to_unsigned(200, 8); b <= to_unsigned(55, 8); wait for 1 ns;
    assert s = to_unsigned(255, 8) report "sum wrong" severity error;
    wait;
  end process;
end;
```

## Do
- Use `ieee.numeric_std` (`unsigned`, `signed`) for arithmetic and never `std_logic_arith`.
- Write clocked logic as `if rising_edge(clk) then`, with one synchronous reset style used throughout.
- Give every combinational process a complete sensitivity list (or `process (all)` in VHDL-2008) and assign every output on every path.
- Use enumerated types for state machines and a `case` with `when others`.
- Declare ports with `std_logic` and `std_logic_vector` at the boundary, and convert to `unsigned` inside.
- Make testbenches self-checking, with `assert ... severity error` or `failure`, and a clock generator that stops when done.
- Use generics for widths, and `generate` for repeated structure.

## Avoid
- Incomplete assignments in a combinational process: they infer latches. Give a default at the top of the process.
- Using `wait` or `after` in synthesizable code: simulation-only constructs. Use clocked processes.
- Mixing both clock edges or gating clocks in logic: timing problems. Use clock enables.
- Multiple drivers on one signal from different processes: resolves to `X`. Drive each signal from one process.
- Comparing `std_logic_vector` with `=` and expecting arithmetic meaning: it is a bit pattern. Convert to `unsigned`.
- Asynchronous inputs used directly: metastability. Pass them through a two-flop synchronizer.
- Relying on signal updates inside the same process cycle: signals update after the process suspends. Use a variable for intermediate values.

## Review
- [ ] Every process drives its outputs completely, with no inferred latches.
- [ ] One clock edge and a consistent reset style.
- [ ] Testbench asserts results and ends cleanly.
- [ ] No simulation-only constructs in synthesizable files.
- [ ] Cross-clock and external inputs are synchronized.
