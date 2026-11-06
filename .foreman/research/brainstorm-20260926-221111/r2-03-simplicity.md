# Brainstorm — lens: simplicity

- **Route every injected note through one arbiter** — CLEAN — value 4 — effort M — risk low
  Why: Next, thrash, tripwire, outline, start-here, gates and drift notes each have their own emitter, and the per-turn cap is 400 chars. Assumption: each emitter enforces its own cap, so they can stack past it.
  Done when: a test fires all note sources in one turn and the injected text is ≤400 chars, priority-ordered, with no duplicate line.

- **Require evidence per criterion, not per step, for S and M** — CLEAN — value 4 — effort S — risk med
  Why: `fm task done` needs evidence for every step and every criterion, and for S tasks the two lists mostly overlap. That is double bookkeeping and extra turns. Assumption: steps rarely have their own verify command.
  Done when: an M task with all criteria evidenced and unchecked steps passes `fm task done`. L keeps per-step evidence, and `fm gates` says which rule applies.

- **Merge tiers M and L into one "full" tier** — CLEAN — value 3 — effort M — risk med
  Why: M and L differ only in the audit set (intent + one lens vs all five), and lens choice from diff signals is already proposed. Two tiers (S, full) cut the gate matrix, the docs and the tier hint. Assumption: no other code branches on L.
  Done when: `fm gates` shows only S and full, old briefs with `tier: L` or `M` still load, and the tests pass after a grep finds no remaining tier-L branch.

- **Make hooks pure decision functions** — CLEAN — value 4 — effort M — risk med
  Why: Stop alone mixes the evidence gate, question nudge, drive loop and circuit breaker with I/O. Assumption: they are entangled with file reads. Each hook becomes `decide(state, payload) -> Action`, with a thin shell that does the reads, writes and printing.
  Done when: the Stop and PreToolUse decisions are tested without touching the filesystem, and hook p50 latency is unchanged.

- **Enforce a core/extras import boundary** — CLEAN — value 3 — effort S — risk low
  Why: serve, watch, notify, plugins, share and digest are opt-in but sit in the same 8,000-line lib as the hook path. A test that imports each hook entry point and asserts that `sys.modules` contains no extras module protects the 30 ms latency and makes removal easy.
  Done when: that test passes, and moving the extras behind lazy imports keeps 474+ tests green.

- **Prune notes the model ignores** — CLEAN — value 3 — effort M — risk low
  Why: `fm usage` already records whether Next was followed. Extend that to every note type by giving each an id and checking whether the next tool call matches its advice. A note followed under 20% of the time over 30+ firings is switched off, and `fm doctor` lists what was dropped.
  Done when: a replayed trace with an always-ignored note type shows that type auto-disabled after the threshold, and the doctor line appears.

- **Report duplicated code in `fm doctor`** — CLEAN — value 2 — effort S — risk low
  Why: the unreferenced-code check exists, but clones don't show up in it. Hash normalized 6-line shingles across plugin/lib with stdlib only and list the top clone clusters. Assumption: growth over many rounds left copy-pasted helpers.
  Done when: `fm doctor` prints clone clusters on a fixture with a planted duplicate and prints nothing on a clean tree.
