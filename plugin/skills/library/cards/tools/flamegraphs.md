---
name: flamegraphs
title: Flame graphs
area: tools
tags: [flamegraph, profiling, performance, visualization, perf, sampling]
detect: [file:*.folded, file:flamegraph.svg]
related: [perf, py-spy, node-inspector, memory-leaks]
---
Flame graphs: read sampled stacks where width means share of samples, then confirm with measurements.

## Verify
- `perf script | stackcollapse-perf.pl | flamegraph.pl > out.svg`: a graph from perf data (Brendan Gregg's FlameGraph scripts).
- `cargo flamegraph --bin NAME`: a graph for a Rust binary (requires the cargo-flamegraph tool and perf).
- `py-spy record -o out.svg -- python script.py`: a graph for Python.
- `wc -l out.folded`: the collapsed stack file is non-empty, so the profile captured samples.

## Test first
Practice check: the profile is evidence, and the failing check is a timing budget.
```sh
./bench --iterations 200 | tee before.txt     # record a baseline
# profile, change the hot frame, then:
./bench --iterations 200 | tee after.txt
# assert after is faster by the target; keep both text files in the review
```

## Do
- Read the x-axis as proportion of samples, not time order; the y-axis is stack depth.
- Look for wide plateaus at the top: the leaf functions where time is spent.
- Search for a symbol in the SVG (click Search) to see what share it covers.
- Use `--reverse` or an icicle layout in `flamegraph.pl` when you want callers of a hot leaf.
- Diff before and after with `difffolded.pl` and `flamegraph.pl` for a differential graph.
- Choose the right profile: CPU on-CPU for compute, off-CPU for blocking and waits.
- Keep a fixed workload and enough samples; profile at least ten seconds.
- Collapse recursion or inline noise when it hides structure.

## Avoid
- Treating the left-to-right order as time: stacks are sorted alphabetically. Width is the signal.
- Optimizing a thin frame: only wide frames matter. Cut the widest actionable one.
- Missing frames from no frame pointers or stripped symbols: you see unknown blocks. Rebuild with symbols and frame pointers.
- Using an on-CPU graph to explain latency from waiting: the time is off-CPU. Profile blocking too.
- One run, one conclusion: repeat and compare. A single capture may include startup or warm-up.
- Profiling a debug build: hot spots shift. Use the release build with symbols.
- Committing generated SVGs and folded files.

## Review
- [ ] The profile came from a release-like build with symbols, under realistic load.
- [ ] The chosen frame is wide, actionable, and verified with a benchmark.
- [ ] Before and after numbers support the claim.
- [ ] Generated artifacts are not committed.
