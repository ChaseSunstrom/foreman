# Brainstorm — lens: sci-fi: the 2030 harness that takes one line and works for weeks to a finished best-in-class result, worked back to what Python and Foreman can do today

- **Precompute the goal verdict on every ledger write** — PERFORMANCE — value 4 — effort M — risk med — category: hooks
  Why: Stop, SessionStart and PreCompact would each re-derive done-vs-stopped from the hash-chained ledger and the briefs, and the bench_hooks gate and ~10 KB cap are hard limits. After a weeks-long goal the ledger is long. Write a tiny `verdict.json` (cause, distance, next action, tail hash) at write time and have hooks read only that file plus the chain tail. Full-chain verification moves to `fm doctor`.
  Done when: a synthetic goal with 5,000 ledger events keeps the Stop hook under the bench_hooks budget, and a hand-edited `verdict.json` is detected against the tail hash.

- **Keep the goal card byte-stable for prompt caching** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: assumption: a card re-injected each session will carry a changing progress count and timestamp near its top, which breaks cached prefixes on every turn. Put the stable parts first (original line, contents list, sealed clauses) and put volatile progress in one trailing line.
  Done when: two renders of the card taken after a task closes share an identical prefix up to the final progress line, and a test pins that.

- **Learn each criterion's file footprint and re-verify only on change** — PERFORMANCE — value 4 — effort M — risk med — category: verify
  Why: the closing audit re-runs every done-when across many tasks, and "all green" claims are expensive to recheck on each resume. Record which files each verify command read (before/after hash diff of the touched tree plus its declared inputs). Reuse a passing result only while those hashes match, and fall back to a full run when the footprint is unknown.
  Done when: editing one file re-runs only the criteria whose footprint contains it, and a criterion with no recorded footprint always re-runs.

- **Run the closing audit's verifies in a bounded pool** — PERFORMANCE — value 3 — effort S — risk med — category: finish
  Why: assumption: goal-close runs dozens of independent verify commands one after another, which makes finishing a goal slow. Fan out independent criteria to N workers in isolated temp dirs and cap CPU. Criteria that share state (a database, a port) are marked serial.
  Done when: a 12-criterion fixture closes in less than half the serial time with identical verdicts, and a shared-port fixture still runs serially.

- **Detect stall by yield decay, not just by no progress** — FEATURE — value 4 — effort M — risk low — category: pacing
  Why: the Stop drive only stops on a hard no-progress rule, and a goal can crawl for days closing one trivial criterion per leg. Track criteria closed per leg and per dollar. When the trailing yield drops below a fraction of the goal's own median, force a replan leg (re-read the contents list, cut or split) before the drive continues.
  Done when: a replayed ledger with three consecutive near-zero-yield legs triggers a replan action in `fm goal step`, and a steady-yield ledger does not.

- **Project the goal into a managed block of CLAUDE.md, AGENTS.md and GEMINI.md** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: the Codex, Gemini and opencode shims and Desktop have no Stop hook, so the weeks-long goal only exists where the hooks run. A delimited, hash-stamped block carries the goal line, distance, next action and a ≤2 KB paste-able resume prompt for web or Desktop sessions. Refuse to overwrite hand edits outside the block, and remove the block when the goal is done.
  Done when: `fm goal sync` writes identical blocks to all three files, leaves other text byte-identical, and a block edited by hand is reported rather than clobbered.

- **Wild: Make a synced folder the universal device surface** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: assumption: the user has phone, watch and e-ink access to some synced directory, and Foreman's rule is to push nothing outward without a grant. `inbox/` takes a dropped text file as a steer or a new goal line (it passes through the untrusted-text quoting). `outbox/` gets a ≤200-byte status file after every transition that anything can poll. There is no server and no network code in Foreman.
  Done when: a file dropped in `inbox/` appears as a quoted steer in the next session's card within one hook run, and `outbox/status.txt` updates on a state change.

- **Notify only on state transitions** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: a multi-week run needs the user to hear about exactly three things: done, stopped (with cause), and blocked on a grant. Emit an OSC 9/777 sequence or `notify-send` only on those transitions, once each, with a settings off-switch. Dry rounds and progress lines never notify.
  Done when: a simulated run through ten legs fires exactly one notification per transition, and none fire when the setting is off.

- **Wild: Fast-forward a three-week goal in a minute** — CLEAN — value 4 — effort L — risk med — category: testing
  Why: the gap map names crashes, compactions, usage limits and drive caps, but a real goal takes days to hit them in sequence. A scripted fake agent and a fake clock drive the real goal engine through every event ordering (kill mid-write, limit mid-leg, compact at a seam, stale baton). Invariants checked: never `verified_done` while a criterion is unmet, never a lost task, and resume is idempotent.
  Done when: the simulator enumerates at least 500 event sequences in under 60 s, and a deliberately broken resume path makes it fail with the minimal sequence printed.

- **File a capability gap to Genesis when a goal can't proceed** — FEATURE — value 4 — effort M — risk low — category: genesis
  Why: Genesis already has a tower, but a goal that hits "cannot run here" (no test runner, no way to verify a surface) only ends as stopped. File a Genesis candidate with the goal line, the missing capability and the failing step, and link it back. The goal stays typed as waiting on that capability, not dropped.
  Done when: a goal blocked on an absent verifier creates one deduplicated Genesis candidate carrying its evidence, and the goal shows "waiting on capability" until it is closed.

- **Wild: Alternate pilots across vendors, each reviewing the other's leg** — FEATURE — value 3 — effort L — risk high — category: multi-agent
  Why: the baton already hands work to another agent. Alternating Claude and a shim agent each leg, with the incoming pilot first auditing the outgoing pilot's closed criteria, gives independent eyes on a weeks-long run without extra orchestration. Assumption: the shims can read the baton and run `fm task finish`.
  Done when: on a fixture goal, leg 2 run by a second agent reopens a criterion planted as falsely closed in leg 1, and the ledger shows the disagreement.

- **Wild: Interview a goal's ledger with cited answers** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: weeks in, the user and any new session ask "why did we cut X?" or "when did we choose Y?". A read-only local query over decisions, steers and cut lines answers only with ledger line citations and says "not recorded" otherwise. Quote all stored text as data, as c.plain does.
  Done when: `fm goal why "<question>"` returns the matching `fm decide` entry with its ledger id, and returns "not recorded" for a planted question with no entry.

- **Seal a ledger tail checkpoint every day so a mid-write kill is cheap to heal** — CLEAN — value 3 — effort S — risk low — category: resilience
  Why: assumption: a crash while appending leaves a torn last event, and recovery has to scan from the start. A daily signed checkpoint (index, hash, byte offset) lets resume truncate or repair only the tail, and it records the repair as an event.
  Done when: truncating the last ledger line mid-write is repaired on the next hook in under 50 ms with a "repaired tail" event, and earlier events are untouched.

Next question: What does the goal engine cost per day in hook time, tokens and disk on a three-week goal, and which of those grows with age instead of with work done?
Next question: Which surfaces can only show a goal (Desktop, web, shim agents), and what is the smallest thing each must do to keep it from being quietly finished early?
