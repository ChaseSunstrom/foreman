**Verdict: merge after fixes.** I found no CRITICAL or HIGH defects. I could not run anything, so the tests and the timing figures are unverified.

**Findings**
- MEDIUM — `fmrelate.py:360-362` — The day and `relate_seen` are claimed before the child runs. If the child fails (offline, budget, timeout), no relate runs again until the next day and 3 further new tasks. Only mention edges are applied, and the failure note is lost because spawn sends stdout to DEVNULL. Fix: write `relate_day` and `relate_seen` only after the child succeeds, and use a short-lived claim key to dedupe concurrent triggers. Confidence: high.
- MEDIUM — `fmrelate.py:338-349` with `due()` — `--clear` is undone by the next daily auto-run, which needs only 3 new tasks. Fix: `--clear` sets `relate_off`, and `--if-due` honours it. A single wrong edge cannot be removed either. Confidence: high.
- MEDIUM — `fmserve.py:308` — `_batch.free()` checks only `depends_on`. `fm run` can put A and B, which has an inferred edge on A, in the same parallel batch, which defeats the ordering. Fix: use `c._deps(b)`. Confidence: high.
- MEDIUM (estimated, not measured) — `fmcore.py:1267`, `fmcore.py:1297` — These sit on the per-prompt hot path.
  - `rank_inbox` now calls `_deps(x)` inside an O(n²) loop. Each call allocates two lists and a dict.
  - `order_queue` replaced a heap with a `min()` scan that calls `_key` twice per element. That is O(n²) on every `regen_views` and `fm next`.
  - Fix: precompute `{id: _deps}` and `{id: _key}` once. Confidence: medium.
- LOW — `fmrelate.py:372` — `--no-child` and sensitive projects use `keep=False`, so they wipe the child's earlier edges and groups. Use `keep=True` whenever no child ran.
- LOW — `fmrelate.py:306`, `fmcore.py:1279` — Batched members are sent to the child and can carry edges. `order_queue` drops edges to members because they are not runnable, so a dependent never waits for the host. Fix: exclude batched tasks from `opened`, or map their edges to the host.
- LOW — `fmcore.py:1297` — The edge is hard. A hallucinated edge from an urgent task to a big task puts the urgent one behind it, including for `fm run`. Ignore inferred deps for urgent dependents.
- LOW — `fmrelate.py:313` — There is no cap on edges. Add a limit of about 5 per task.
- LOW — `fmrelate.py:283` — A mention is always read as "B waits on A". The text "T-0200 will build on this" inverts it. There is no per-edge veto.
- LOW — `fmtidy.py:126` — The cycle hint says to edit `depends_on`, but the cycle can run through an inferred edge. It should suggest `fm relate --clear`.
- LOW — The first run happens silently in every project with 3 or more open tasks. An intake after that day's SessionStart run waits until the next day.

**Adversary**
- The child's reply is treated as data. Only ids that are open pass through, and the reason and theme go through `_clean`. That removes newlines, `#`, end brackets, secrets and control characters.
- I traced the frontmatter round trip and found no way to inject a key or break a brief file.
- There is no loop: `run_child` sets `FOREMAN_NO_BACKGROUND`, and `spawn` honours it.
- A group theme of `true` parses back as a boolean. This is cosmetic.

**rank_inbox age term**
- Safe. `int()` floors the age, `None` becomes 0, and a negative age becomes 0 or more.
- It fixes a real defect. A float age read at each call ranked same-second captures newest first.
- I found no existing test that depends on age ordering (grep for `age_days` and `created`). The full suite was not run.

**Acceptance criteria**
- Both edge sources and the three meta keys: met (`apply`).
- `--clear` undoes them: met, but the auto-run reverses it (see above).
- `order_queue` and `rank_inbox` honour inferred deps and keep groups adjacent: met, with the batch gap above.
- At most once a day, with 3 or more new open tasks, detached from SessionStart and after an intake of 3 or more: met.
- Unknown ids and cycles are dropped: met.
- Hook latency is low (a cheap `due()` check and one detached Popen); I did not measure it.

**Maintainer**
- `run_child` is reused. `c.mutate` is not, which is reasonable because the code writes many briefs under one lock.
- This is the third copy of the Popen detach pattern (`fmhooks` second-session, `fmmap`).
- Missing tests: child failure keeping earlier edges, a cycle with `depends_on`, injection characters in the reason, batched tasks, `--no-child`, and the `rank_inbox` age change.

**Not checked:** running the test suite, real `claude` behaviour, and timing.
