# Brainstorm — lens: performance

- **Split the read verbs from the run verbs** — PERFORMANCE — value 4 — effort S — risk low — category: CLI startup
  Why: The profile found box and startup cost dominate, and a full read took 124 s of CPU. `status`, `why` and `doctor` shouldn't import the runner, TUI or web code. Assumption: those imports are where the startup time goes.
  Done when: `python -X importtime` shows `fm status` loading no runner or TUI module, and its median wall time on the bench drops.

- **Make `fm map` incremental by directory mtime** — PERFORMANCE — value 4 — effort M — risk low — category: repo map
  Why: The map covers 1,835 files and is rebuilt whole each time. Assumption: most files are unchanged between runs, so only dirty directories need re-reading.
  Done when: touching one file and re-running `fm map` re-reads only that file's directory, and the output matches a full rebuild byte for byte.

- **Stream each brainstorm child into the ledger as it finishes** — PERFORMANCE — value 4 — effort M — risk low — category: brainstorm latency
  Why: A round waits for every lens, so the slowest child sets the round's wall time. Assumption: lens latency varies a lot, which the 480 s class cap hints at.
  Done when: with one child held back 60 s, the other lenses' ideas are filed before that child returns, and no idea is filed twice.

- **Pin the hook bench to one isolated core** — PERFORMANCE — value 4 — effort S — risk low — category: benchmark noise
  Why: The PreToolUse:Bash p95 read ~310 ms under load but ~272 ms when quiet, so the bench measures the box more than Foreman. Assumption: `cpuset` or `taskset` is available on the target machines.
  Done when: five `bench_hooks` runs on a loaded machine give a p95 within 10% of the quiet-machine p95.

- **Build the git test fixture once per session and copy it with reflinks** — PERFORMANCE — value 3 — effort S — risk low — category: test speed
  Why: Tests set up repos from scratch, which costs time on every test. Assumption: the setup is the same each time and only the test's own writes differ.
  Done when: the suite's wall time drops, and a test that writes to its repo leaves the next test's repo untouched.

- **Run doctor's probes in parallel under one shared deadline** — PERFORMANCE — value 3 — effort S — risk low — category: doctor latency
  Why: Doctor's many checks look sequential, so one hung probe delays the whole report. Assumption: the probes are independent.
  Done when: with one probe hung for 30 s, `fm doctor` finishes within 2.5 s and names that probe as timed out.

- **Pre-render the Today and History charts as static SVG at build time** — PERFORMANCE — value 3 — effort S — risk low — category: site load
  Why: The site's data changes once per build, so per-view chart scripting is wasted work. Assumption: the chart data is available at build time.
  Done when: the charts paint with JavaScript disabled, and the chart script bytes sent to the page drop to zero.

- **Print a per-phase breakdown on every slow run's receipt** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: The 124 s profile was done by hand, and no receipt says where a slow run's time went. Assumption: the journal already records phase timestamps.
  Done when: a run over its phase budget prints its three slowest phases with seconds, and `fm cost` reports the same numbers from the journal.

- **Send model calls over a warm HTTP/2 connection** — PERFORMANCE — value 2 — effort M — risk med — category: model latency
  Why: Each `claude -p` child starts cold and pays its own TLS setup. Assumption: that setup is a large share of short calls, which the journal could confirm.
  Done when: the journal shows time-to-first-token for the second short call in a queue below the first.

- **Wild: time every hook call from outside with an eBPF probe** — FEATURE — value 2 — effort L — risk med — category: zero-overhead timing
  Why: Wild: a kernel probe times each hook process without any code in Foreman, so the bench can't be skewed by its own timer. Assumption: the user can load eBPF probes.
  Done when: the probe reports latency for 1,000 real hook calls, and its p95 agrees with the in-process timer within 5 ms.

- **Wild: mmap the rules file as a fixed table the guard reads without parsing** — PERFORMANCE — value 3 — effort M — risk low — category: guard latency
  Why: Wild: the guard parses the rules text on every call. Assumption: the parse is a measurable part of a hook's time.
  Done when: guard verdicts match the parsed path across the full corpus, and a hook call reads no rules text.

- **Wild: compress cold journals with a zstd dictionary trained on Foreman's own events** — PERFORMANCE — value 2 — effort M — risk low — category: journal size
  Why: Wild: journal events repeat the same fields, so a dictionary trained on them should compress far better than generic zstd. Assumption: most journal bytes are these repeated shapes.
  Done when: a month of archived journal shrinks by at least half and reads back byte for byte.
