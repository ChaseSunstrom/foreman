# Brainstorm — lens: performance

- **Serve git status from fsmonitor and the untracked cache** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: Hooks and gates shell out to git on every call, and the hook bench already misses its budget under load (dropped item: PreToolUse:Bash:script p95 ~310 ms vs 300 ms). assumption: each hook runs a full `git status`.
  Done when: bench_hooks on the 1,835-file repo shows a lower median for PreToolUse:Bash:script with `core.fsmonitor` and `core.untrackedCache` on, against a same-run baseline.

- **Read git objects through one long-lived `cat-file --batch` process** — PERFORMANCE — value 3 — effort M — risk low — category: process spawns
  Why: a full read costs 124 s CPU and the box plus startup is most of it (steered). assumption: a verb spawns one git process per file it inspects.
  Done when: a full read's spawned-process count, counted by a test shim, drops by at least 10x on the fixture.

- **Cache the statusLine output for one second** — PERFORMANCE — value 3 — effort S — risk low — category: process storm
  Why: the glance line is rendered on every redraw, so each redraw starts a fresh fm process. assumption: the statusLine command re-runs on each refresh.
  Done when: 20 redraws inside one second start one fm process, and the other 19 read the cached line.

- **Wake gate-lock waiters from a kernel event, not a sleep loop** — PERFORMANCE — value 3 — effort S — risk low — category: lock wait
  Why: a full check can wait 15 minutes for another run's lock (user ask). assumption: waiters poll on a timer, so they wake late and burn wakeups.
  Done when: a test that releases the lock lets a waiter acquire it within 50 ms.

- **Start the longest brainstorm lens first** — PERFORMANCE — value 3 — effort S — risk low — category: fan-out wall time
  Why: a round finishes only when its slowest child does, and children run under a 480 s kill. assumption: lenses dispatch in a fixed order, so a slow lens often starts last.
  Done when: on a six-lens fixture with recorded durations, round wall time is within 10% of the slowest child's time.

- **Print the first line of `fm status` before the probes finish** — PERFORMANCE — value 2 — effort S — risk low — category: perceived latency
  Why: status waits for every probe before printing anything. assumption: the first useful line needs only the journal tail.
  Done when: with one probe stubbed to sleep 5 s, the first line appears within 50 ms.

- **Coalesce background wakeups onto one timer wheel** — PERFORMANCE — value 2 — effort M — risk low — category: idle wakeups
  Why: the 10-minute sweep, the watchdogs and the deadlines each wake the machine separately. assumption: they keep independent timers.
  Done when: with the sweep and a watchdog active, an idle minute records at most one wakeup.

- **Precompress and hash-name the site's assets** — PERFORMANCE — value 2 — effort S — risk low — category: site delivery
  Why: the Pages site ships the HTML, the demo SVG and the MP4 on every publish with no cache-busting. assumption: the build emits neither compressed siblings nor fingerprinted names.
  Done when: the built site has `.br` siblings and content-hashed asset names, and a repeat load fetches no unchanged bytes.

- **Yield checks to keystrokes with ionice and a cgroup weight** — PERFORMANCE — value 3 — effort M — risk low — category: interactive responsiveness
  Why: a full suite running beside a typing user competes for CPU, and the hook bench already shows p95 drift under load. assumption: checks run at normal priority.
  Done when: keypress-to-echo latency stays under 100 ms p95 while the full suite runs.

- **Wild: prefetch the next queued task's files into the page cache** — PERFORMANCE — value 2 — effort S — risk low — category: cold reads
  Why: assumption: the first tool result of each task waits on cold reads while the model is still thinking about the previous one.
  Done when: time-to-first-tool-result on the next task is measurably lower warm than cold on the fixture.

- **Wild: autotune the hook's interpreter flags at install** — PERFORMANCE — value 2 — effort S — risk low — category: startup cost
  Why: assumption: the best interpreter flag set differs across Python builds, so one fixed set is not always fastest.
  Done when: install times three flag sets, pins the fastest, and the bench confirms it beats the default on this machine.

- **Wild: warm the prompt cache when the user focuses the prompt box** — PERFORMANCE — value 2 — effort M — risk medium — category: cache economics
  Why: assumption: a long idle gap lets the cache expire, so the first reply re-bills the whole pack. Warming costs tokens, so it needs a measured break-even.
  Done when: after a 10-minute idle gap with warming on, `fm cost` shows at least 90% of the first reply's input as cache reads, and the warm's spend is below the saving.
