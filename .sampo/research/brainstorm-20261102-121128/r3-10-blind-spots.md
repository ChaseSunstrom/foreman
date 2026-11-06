# Brainstorm — lens: blind spots

- **Fingerprint Foreman's own output so echoes can't pass as user input** — FIX — value 4 — effort M — risk low — category: input authorship
  Why: T-2554 and T-2624 show Foreman-authored text (Mission briefs, pasted keys) re-entering as "the user's asks". Question missed: which strings did Foreman emit that can come back through the paste channel? Assumption: hook notes, receipts and Mission text get quoted in user pastes.
  Done when: a user message that quotes a hook note or Mission brief verbatim is tagged `echo` in the intake, and a test shows `fmforesight._requests` skips it.

- **Age every pending decision and escalate stale ones** — FEATURE — value 4 — effort S — risk low — category: silent abstention
  Why: T-2566 let a select abstain silently, and T-2503's lean "pending" rows wait indefinitely for a measurement. Question missed: how long has each "undecided" state been undecided? Nothing records the age.
  Done when: `fm doctor` lists each pending lean or select row with its age in days, and a row older than 14 days becomes a WARN naming the missing measurement.

- **Detect dead deciders by their abstain rate** — FEATURE — value 4 — effort M — risk low — category: silent abstention
  Why: the earlier "report coverage" idea covers a single call. Nothing covers a decider that has abstained on 100% of calls for a month, which is dead code that looks like caution. Assumption: deciders can log an abstain with a reason.
  Done when: a decider with an abstain rate ≥95% over 30 days and ≥20 calls shows up in `fm doctor`, and a fixture decider that always abstains triggers it in a test.

- **Check installed units still execute after an OS upgrade** — FIX — value 4 — effort M — risk low — category: unattended liveness
  Why: T-2542 checks that timers fire. It doesn't check that each unit's ExecStart still resolves, for example after a rolling Arch Python bump or a moved venv, since it only reads systemd's last result. Assumption: the host is a rolling distro (the hardened kernel suggests so).
  Done when: `fm doctor` resolves every installed foreman-* ExecStart and runs it in a dry mode, and a test with a renamed interpreter path reports the unit as broken.

- **Scaffold deciders with the blind-spot checks built in** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: five asks in a row (T-2534 to T-2566) were the same shape: a decider lacking a measurement, a liveness check, authorship filtering or abstention reporting. Question missed: what must every new decider declare? A template makes the answers mandatory.
  Done when: `fm new decider NAME` generates a module plus a conformance test, and that test fails if the module declares no min-sample, author filter, abstain reason or clock injection.

- **Time ledger readers against 10× ledger size** — PERFORMANCE — value 3 — effort M — risk low — category: performance
  Why: the pack shows many windowed readers (30-day Brier, bet settlement, calibration) and `bench_hooks.py` only measures hooks. Question missed: what do readers cost at 10× the data? Assumption: readers scan whole files.
  Done when: a bench builds a synthetic ledger 10× the current size and fails if any reader's median time exceeds a recorded budget, with a checkpoint or index named for the worst offender.

- **Stamp records with a host id so two machines can't blur ledgers** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: the pack covers a host wipe but not two hosts (laptop and server) writing state for the same repo, which would make outcomes and bets double-count. Assumption: the user runs Foreman on more than one machine.
  Done when: every new ledger row carries a host id, and a merge of two fixture ledgers keeps both without duplicate bets.

- **Mutate each DONE-WHEN to find vacuous passes** — FEATURE — value 4 — effort M — risk low — category: criteria quality
  Why: T-2583's own example broke its own rule, and steer-check vacuity is already proposed. Task criteria in general have no such test. Question missed: how could this DONE-WHEN pass while the work is wrong?
  Done when: at `fm capture`, a tool-less child proposes 3 wrong implementations, and a criterion that passes on any of them is flagged before the task starts.

- **Run the nightly on awkward repo shapes** — CLEAN — value 3 — effort M — risk low — category: portability
  Why: the map, cards and readers were built on this one repo. Question missed: which readers abstain or misreport on a repo with no tests, no git history or a monorepo? Assumption: the fixtures under `plugin/tests/fixtures` are all well-formed.
  Done when: a nightly run over 4 synthetic repos (no tests, no history, monorepo, non-Python) lists every reader that errored or silently abstained.

- **Wild: Run the placebo shuffle to expose circular readers** — FEATURE — value 3 — effort M — risk low — category: measurement integrity
  Why: assumption: some scores depend on who wrote the record. Shuffle author tags and bet outcomes in a copy of the ledger. Any reader whose answer doesn't change is blind to authorship, and any score that survives a shuffled outcome is not measuring outcomes. Wild.
  Done when: `fm doctor --placebo` runs every reader on a shuffled copy and names each one whose output didn't move.

- **Wild: Validate brainstorm questions against past misses** — FEATURE — value 4 — effort M — risk low — category: meta-process
  Why: "Next question" lines are never scored. Replay each stored question on the pack as it stood before a later ask (T-2534, T-2554) and check whether it would have surfaced that ask. Keep the questions that would have and drop the rest. Wild.
  Done when: a report lists each past `Next question` with hit or miss against later user asks, and the next brainstorm is fed only the hits.

- **Wild: Canary a rolling-distro upgrade before pacman runs it** — SECURITY — value 3 — effort L — risk med — category: ops
  Why: a Foreman install that stops working after a Python, systemd or bash update would be silent, for the same reason as T-2542. Assumption: a container with the testing repo's packages can run the e2e roundtrip.
  Done when: a weekly job runs `roundtrip.py` and the doctor in a container with next-update packages, and a failure there appears in `fm doctor` as "upgrade will break X".

- **Wild: Show the user which of their own words each rule came from** — FEATURE — value 3 — effort S — risk low — category: steer provenance
  Why: the steers list has about 35 standing rules and several (T-2462 waiting on T-2441, round-first) are already superseded or sitting in task text. Question missed: which steer is still obeyed, and which is just text? Each rule gets a source quote and a "last enforced" date.
  Done when: `fm decide --list` prints source date, quote and last-enforced date per steer, and a steer never enforced in 60 days is shown as "idle".

- **Alert when a user correction repeats a class a prior ask fixed** — FIX — value 4 — effort M — risk low — category: ask clustering
  Why: the five missed classes each arrived as one ask and nothing linked them to earlier siblings. Assumption: asks from the same week share a failure class (a decider with no measurement, a silent abstention).
  Done when: `fm capture` compares a new ask to the last 30 closed tasks by class tag, and 2 or more matches print "third of its kind: sweep the class?" with the sibling ids.

Next question: which of Foreman's ~35 standing rules and steers does no code path currently enforce, and could a reader count that gap per rule?
Next question: where does a Foreman-written number reach the user (doctor, site, README) with no stored denominator or source, and what outside check would catch it first?
