# Brainstorm — lens: unspoken needs

- **Fix the brief-guard path false positives** — FIX — value 4 — effort S — risk low — category: guard
  Why: the pack records 2 brief-guard false positives that read a dict key and a `.join(` call as written paths. A guard that cries wolf trains the user to bypass it.
  Done when: a test feeds a brief containing `d["a/b"]` and `",".join(x)` and the guard passes it, while a brief that really writes a protected path is still blocked.

- **Replay the user's real command history through the guard** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: assumption: false positives and misses surface only by accident today. Standing rules prize signals Foreman didn't author, and the user's own shell and tool history is one.
  Done when: `fm guard replay --days 30` prints false-positive and false-negative candidates per rule, and it runs with no network.

- **Turn the top repeated block into a hint before it fires** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: `core:interpreter-code-driving-foreman` blocked 42 times in 7 days. Agents keep making the same wrong move, so the missing piece is teaching the safe alternative.
  Done when: the block message and a one-line SessionStart hint name the replacement verb, and that rule's weekly block count drops by at least 80% over the next week.

- **Print a guard parity matrix per harness** — FEATURE — value 5 — effort M — risk med — category: safety / devices
  Why: T-0335, T-0336 and T-0337 are blocked, and Gemini's Stop hook isn't wired. "Guard intact" is claimed for Codex, Gemini and opencode, but nothing shows which rules enforce there.
  Done when: `fm doctor` lists each guard rule against each harness as enforced, advisory or absent, and a README claim that contradicts the matrix turns the sweep red.

- **Inject the SessionStart note once, then only deltas** — PERFORMANCE — value 4 — effort S — risk low — category: context
  Why: the ~2k-character note went out 89 times. An unchanged state should not pay twice.
  Done when: a resumed session whose state hash is unchanged injects under 300 characters, and a test shows the full note returns when the hash changes.

- **Attribute per-reply context by source** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: context averages 387k per reply, but nothing says how much of it Foreman adds. Assumption: most of it is conversation history, which makes the lean ratchet blind to the real figure.
  Done when: `fm cost --by-source` reports Foreman's injected bytes as a share of reply context, per harness.

- **Move unused stack cards to a cold shelf** — CLEAN — value 3 — effort M — risk low — category: simplicity
  Why: 5 of 1219 cards have been used, and the repo is 2,098 files. A card nobody called costs index and map weight.
  Done when: cards unused for 60 days leave the hot index, `fm lib show NAME` still fetches them, and `fm map` counts fall with the subtraction recorded.

- **Give each surface its own latency and bytes budget in doctor** — FEATURE — value 4 — effort M — risk med — category: lean
  Why: the p95 of 278 ms is one blended number. Headless and server runs likely want a guard-only profile (T-0794 is deferred), and a blended figure hides which surface regressed.
  Done when: `fm doctor` prints p95 and injected bytes per surface and fails when any exceeds its stored budget.

- **Lint the 61 new coverage cells for templating before they are written** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: the standing rule says a templated or reused cell doesn't count. Filling 61 at once invites reused phrasing, so catching it at write time beats failing the sweep afterwards.
  Done when: a write with 80%+ word overlap with another cell in its row or column is refused with the neighbour named, and genuine n/a cells need a reason.

- **Show carrying cost per use for each capability** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: T-2503 holds growth as "pending" until a measurement exists, but nothing says what a capability costs per time it is used. The 5-of-1219 figure shows how lopsided that can be.
  Done when: `fm burden --per-use` ranks capabilities by injected bytes, hook ms and files divided by recorded uses, and the top three feed the next Seed's subtraction list.

- **Wild: Run an airplane-mode proof** — FEATURE — value 3 — effort M — risk low — category: privacy
  Why: wild, and it answers the open question about proofs that need no network or secrets. A single command runs the lean and safe checks with the network off and no model calls, and states which ones couldn't run.
  Done when: `fm doctor --offline` finishes in a network-less namespace and lists each skipped check with its reason.

- **Wild: Slim the hard hat on the status line** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The user keeps asking for subtraction, so make a net deletion visible. The logo or status glyph shows a small diet mark that moves when a generation removes more than it adds.
  Done when: the mark changes state between a net-growth and a net-shrink generation, and a screenshot of the web UI shows both states.

- **Wild: Hold a nightly guard-drift rehearsal against the newest host builds** — SECURITY — value 4 — effort M — risk med — category: safety
  Why: wild. Hook payload shapes change between host versions, and the guard fails silently if the shape moves. The night tick installs the newest Claude Code, Codex and Gemini in a scratch directory and fires known-bad commands.
  Done when: a seeded payload-shape change turns the next nightly report red, and the digest names the host and the rule that stopped blocking.

Next question: Which lean and safe checks does the user already run by hand, such as reading `fm doctor` or watching hook latency, that a gate could own for them?
Next question: Which empty coverage cells are true n/a, such as site × operate, and who is allowed to record that instead of inventing an idea?
