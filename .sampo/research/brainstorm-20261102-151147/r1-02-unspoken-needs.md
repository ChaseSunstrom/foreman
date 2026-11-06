# Brainstorm — lens: unspoken needs

- **Lint every brief's factual claims against the repo before it files** — FIX — value 4 — effort S — risk low — category: grounding
  Why: T-2659 and T-2671 show the user having to ask for grounding with spot checks on each claim a brief rests on, and 3 of 4 slate items were already built. A zero-token pass could pull backticked verbs, file paths and numbers out of a brief and check each exists (grep, `fm help`, `ls`). It would store the hit or miss next to the brief, so a spot check is a re-run and not a judgement.
  Done when: a brief naming a nonexistent verb or path is refused at filing with the missing token named, and a brief with all tokens real files with a claims table attached.

- **A/B the "ideas so far" list against a no-list pack** — FEATURE — value 4 — effort S — risk low — category: brainstorm quality
  Why: the list is thousands of lines and the same idea recurs under new titles. "Unproven" as a third state, restore drills and gauge cross-checks each appear about ten times. Whether the list prevents repeats or only costs tokens has never been measured. Run one lens twice on the same pack, once with the list and once with a nearest-5 lookup, and compare the share of novel ideas.
  Done when: a report gives novel-idea rate and tokens for both arms on 3 lenses, and the pack builder uses whichever arm wins.

- **Plant a canary grant and prove no spawned process class can spend it** — SECURITY — value 4 — effort M — risk low — category: authority
  Why: the earlier question about which lanes, ticks, `fm code` tools and prover children inherit the push grant, credentials or ledger key is unanswered. Create a dummy grant and key. Spawn each child class (lane, tick, tool, prover, brainstorm child) and have it try to use them. Print the matrix.
  Done when: `fm doctor` shows one row per child class with "can use grant: no/yes", and a planted leak in one class turns its row red in a test.

- **Break the guard's own state one file at a time and record what each unattended path does** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the earlier question about a missing, truncated or unreadable rules file, grant store or last-good copy at hook time is unanswered. In a scratch home, delete, truncate and chmod each file, then run the hook, drive and tick paths. Assert each path fails closed or open as declared and writes a ledger line saying so.
  Done when: a 3×3 table of (file × fault) results exists, every cell has a ledger record, and an undeclared silent fail-open fails the test.

- **Give sub-agents a "blocked by policy" outcome with the one-line widening command** — FEATURE — value 3 — effort S — risk low — category: agents
  Why: the earlier question about a sub-agent whose allowlist blocks the only way to finish is open. Today that probably reads as a plain failure. Record `blocked_by: allowlist <tool>`, keep it distinct from failed, and surface it in `fm next` with the exact grant to widen.
  Done when: a fixture lane whose only route needs a denied tool ends as `policy-wall` and `fm next` shows the grant command.

- **Mine the user's interrupts after Foreman output as the "felt cost" signal** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: nobody knows which footprint measure the user feels (tokens, hook latency or notes). The user's Esc or Ctrl-C within a few seconds of an injected note or a slow hook is a signal Foreman did not author. Rank sources by interrupts per hundred appearances.
  Done when: `fm burden --felt` lists sources by interrupt rate with sample sizes, and a replayed transcript with planted interrupts ranks the planted source first.

- **Tally retries, hedges, fallbacks and skips with their dollars on every receipt** — FEATURE — value 3 — effort S — risk low — category: spend
  Why: these behaviours change spend or outcomes unseen until the receipt. One line such as "3 retries $0.41, 1 fallback $0.12, 2 skips" makes them visible without a new ledger. It would read events already recorded.
  Done when: the drive receipt shows the line, and a fixture run with a planted fallback shows its cost.

- **Witness protected paths across IDE terminals, cron and CI** — SECURITY — value 3 — effort M — risk med — category: guard coverage
  Why: the guard cannot see surfaces it does not control. Hash a small list of precious paths and git state at session start and end. Report any change not matched to a ledgered command as "unexplained change", with the time window.
  Done when: editing a protected file from a plain shell between two sessions yields an "unexplained change" line at the next session start.

- **Add `fm why-not` to explain why a nudge or guard rule did not fire** — FEATURE — value 3 — effort S — risk low — category: debuggability
  Why: `fm why` exists for what fired. The reverse question ("why didn't it warn me?") is how a user finds a dead decider. It would replay the last event through each rule and name the clause that fell short.
  Done when: for a recorded command the guard allowed, `fm why-not` names each rule's closest-miss reason.

- **(wild) Ghost reviewer: a tool-less child trained on the user's drops votes keep or drop on each slate first** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: drops like "mostly built" or "value 2 after re-grounding" recur and the user pays for each. The child sees only the steers and the last 50 drop reasons, and its votes are later scored against what the user does.
  Done when: a slate shows the ghost's predicted drops, and a weekly line gives its hit rate against real drops.

- **(wild) Seeded-gap recall test for brainstorms** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: nobody knows if "exhaustive" holds. Plant a known real gap in a fixture repo (an untested writer, say), run the lenses, and score how many surface it. This is a recall number for the brainstorm that no Foreman author produced.
  Done when: `fm exam brainstorm` prints per-lens recall on 5 planted gaps.

- **(wild) Print a silence letter: what I considered saying and held back** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: quiet reads as dead, and the hold-back reasons (mute rules, dedupe, budget) are already computed. A short weekly count by reason shows restraint and exposes over-muted deciders.
  Done when: the weekly digest includes "held back N: reason counts", and a muted decider appears in it.

Next question: which of Foreman's silent behaviours would the user be upset to learn about only from a receipt, and does the pack have any record of the user reacting to one?
Next question: for each deferred "later: needs…" task, is the needed evidence something Foreman could observe itself, or only the user?
