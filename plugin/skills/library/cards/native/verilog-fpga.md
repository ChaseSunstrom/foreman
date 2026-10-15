---
name: verilog-fpga
title: Verilog / SystemVerilog FPGA
area: native
tags: [verilog, systemverilog, fpga, rtl, simulation, yosys, verilator]
detect: [ext:.v, ext:.sv, ext:.vhd, file:*.xdc, file:*.pcf, file:*.qsf, file:*.lpf]
related: [embedded-c, zephyr, arm-cortex-m]
---
Verilog/SystemVerilog RTL: self-checking testbenches, lint, synthesis checks, clock-domain and reset discipline.

## Verify
- `verilator --lint-only -Wall -sv rtl/top.sv`: synthesizability and width/latch warnings.
- `iverilog -g2012 -o sim.out rtl/*.sv tb/tb_top.sv && vvp sim.out`: run the testbench; it must print PASS and exit.
- `yosys -p "read_verilog -sv rtl/top.sv; synth -top top; stat"`: synthesizes, and `stat` shows cell counts and inferred latches.
- `verilator --binary --assert -sv --top-module tb_top tb/tb_top.sv rtl/*.sv && ./obj_dir/Vtb_top`: fast simulation with assertions on.
- `sby -f formal.sby`: SymbiYosys formal proof, if the project has a `.sby` file.

## Test first
Write a self-checking testbench that fails (`$fatal`) on mismatch; no waveform eyeballing.
```systemverilog
module tb_counter;
  logic clk = 0, rst = 1; logic [3:0] q;
  counter dut(.clk, .rst, .q);
  always #5 clk = ~clk;
  initial begin
    repeat (2) @(posedge clk); rst = 0;
    repeat (3) @(posedge clk);
    if (q !== 4'd3) $fatal(1, "expected 3, got %0d", q);
    $display("PASS"); $finish;
  end
endmodule
```

## Do
- Use `always_ff @(posedge clk)` for registers with nonblocking `<=`, and `always_comb` with blocking `=` for combinational logic.
- Give every register a reset value; pick sync or async reset once per design and keep it. Synchronize an async reset release.
- Cross clock domains with 2-flop synchronizers for single bits, and async FIFOs or handshakes for buses; never pass multi-bit values through bare flops.
- Declare widths and signedness explicitly (`logic signed [7:0]`); use `default_nettype none` at the top of files.
- Assign every output in every branch of combinational blocks (default assignments at the top) to avoid latches.
- Add `assert property` checks (SVA) for protocol invariants, and run them in simulation.
- Constrain clocks in `.xdc`/`.sdc` and read the timing report: setup slack must be non-negative.
- Parameterize with `parameter`/`localparam` and `generate`; keep one module per file named for the file.

## Avoid
- Blocking `=` in clocked blocks or nonblocking in combinational ones: simulation vs synthesis mismatch. Follow the split above.
- Incomplete `case`/`if` in combinational logic: infers latches. Add `default` and defaults at the top.
- Mixing `#delay` statements into RTL: ignored in synthesis. Keep delays in testbenches.
- Using `==` on values that might be X in testbenches: passes wrongly. Use `!==` and `===`.
- Gating clocks with logic, or deriving clocks from counters: glitches and timing failures. Use clock enables or PLL/clock primitives.
- Testbenches that only dump waves and never assert: no regression value. Check results in code.
- Reading a signal from another clock domain without synchronizer: metastability, intermittent bugs.

## Review
- [ ] Lint is clean with no unexplained waivers; no inferred latches in the synthesis report.
- [ ] Testbench is self-checking and exits non-zero on failure.
- [ ] Every clock crossing and reset has a stated method.
- [ ] Timing constraints exist, and slack is positive after place and route.
- [ ] Widths are explicit, and `default_nettype none` is set.
