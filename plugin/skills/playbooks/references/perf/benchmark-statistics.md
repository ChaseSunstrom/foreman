<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Is the difference real?

Use when a benchmark, A/B run, eval or bench gate shows a gain or loss and you must decide whether it is a real change or noise.

1. **Measure the noise first:** run the unchanged baseline at least 5 times and keep the spread (standard deviation, or the pass fraction per case). One run of each side proves nothing.
2. **Judge against the band:** a delta within about ±2 standard errors is noise; between 1 and 2 is inconclusive, so say how many runs would settle it. Only outside the band is it a win or a loss.
3. **Calibrate by simulation:** feed the gate pairs drawn from the same distribution and check it calls them noise about as often as it claims; tune the band until it does.
4. **Equal budgets:** both sides get the same turns, tokens, time and seed set. A run stopped at its cap is inconclusive, not a failure.
5. **Measure what the user feels:** wall time, success rate or cost per solved case, not CPU time on a busy machine. Note the load beside the number.
6. **Ablate one thing at a time:** a bundle that wins hides a part that loses.
7. **Keep the raw runs** next to the summary so the call can be checked again with more runs later.

Mined from T-1260, T-1435, T-1439, T-1464, T-1375.
