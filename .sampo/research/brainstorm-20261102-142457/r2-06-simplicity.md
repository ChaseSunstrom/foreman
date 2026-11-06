# Brainstorm — lens: simplicity

- **Print a capability bill of materials** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: the pack gives growth (2129 files, 1388 of them skills) and a rule that growth waits until it is measured (T-2503), but no single table joins cost to yield. Assumption: skills, verbs, hooks and ledgers can each be mapped to a capability name. `fm lean bom` would print one row per capability with files, bytes, injected tokens, hook ms, last session-path call and last outcome measurement. Unmeasured rows are marked pending.
  Done when: `fm lean bom` prints a row for each of the 13 gen-0 capabilities, and a capability with no measurement shows "pending" rather than a zero.

- **Brown out unused verbs and skills for a shadow week** — FEATURE — value 4 — effort M — risk med — category: subtraction
  Why: `fm usage --prune` lists unused verbs but only proposes. Hiding them and counting the misses is stronger evidence than a usage count. Assumption: a hidden verb can print "browned out, run X to restore" and log the hit.
  Done when: with brownout on, a call to a hidden verb is logged with its name and restores in one command. After 7 days a report lists zero-hit verbs as retire candidates.

- **Run a shrink pass on every diff at ship** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: the standing rule says growth must earn its place, but nothing looks at the diff itself. A cold child gets the task brief and the diff and tries to produce a smaller one. Foreman keeps the smaller diff only if the full suite stays green.
  Done when: on a fixture diff with a planted redundant helper, the pass proposes the smaller version, the suite is green, and a run on a minimal diff proposes nothing.

- **Put removed things on a two-release deprecation clock** — CLEAN — value 3 — effort S — risk low — category: lifecycle
  Why: the c08 ask is a tombstone for removed flags, but that leaves tombstones in place forever. A marker gives each deprecated flag or verb a tombstone for two releases, then files its own removal task. Assumption: releases are countable from tags or version bumps.
  Done when: a flag marked deprecated at version N prints a tombstone with its replacement at N+1 and N+2, and a removal task is filed at N+2.

- **Find verbs that overlap** — CLEAN — value 3 — effort M — risk low — category: subtraction
  Why: many verbs have grown by mission (`fm prove`, `fm task evidence`, `fm shot`, `fm flow`, `fm verify-ledger`, `fm fsck`, `fm drill`). Assumption: verbs can be run on fixtures and compared on output shape and ledger reads. A report pairs verbs whose outputs or reads largely coincide and proposes a merge or alias for each pair.
  Done when: the report lists at least one real pair with the evidence, and a planted duplicate verb on a fixture is flagged.

- **Add a restraint exam kind** — FEATURE — value 4 — effort M — risk low — category: ceremony
  Why: the exams measure whether Foreman catches things, not whether it does too much on a trivial change. T-1231 (beat Claude Code on cost and time) and T-1266 (ceremony per task kind) both depend on that number. Assumption: ten trivial scenarios (typo, rename, comment) can be authored by a tool-less child.
  Done when: `fm exam` reports steps and seconds for foreman versus plain on trivial scenarios, and prints a flag when foreman exceeds 1.5× plain on any scenario.

- **Archive a steer once its automatic check enforces it** — CLEAN — value 3 — effort S — risk low — category: steers
  Why: 40-plus steers are injected as text, yet each now has an automatic check (`fm decide --check`). Assumption: a steer whose check has passed for 60 days with zero fires can leave the injected text. A passing steer moves to an "enforced" list and is injected only by name, and the list stays visible in `fm doctor`.
  Done when: injected steer tokens drop on a fixture ledger with an eligible steer, `fm doctor` still lists it, and breaking its check puts it back in the injected text.

- **Chart lean metrics across history** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: the map was taken at an "older HEAD", so there is no time axis for growth. Walking the commits and counting files, verbs and injected bytes per area shows where growth stopped earning anything. Assumption: counts can be recomputed from git without checkout.
  Done when: `fm lean history` prints a per-area series for the last 50 commits, and the totals for the newest commit match `fm lean bom`.

- **Freeze the safety core by path** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the guard and the ledger writer are the parts where a drive-by edit costs most. A `frozen.txt` lists paths, and ship refuses a diff touching one unless the task states an unfreeze reason, which is recorded. T-0794 mentions freezing the mod, so the idea exists in outline.
  Done when: a fixture diff that touches a frozen path fails `fm ship` with a Next: command, and the same diff with a recorded reason passes.

- **Wild: Hold a budget market for the footprint** — FEATURE — value 3 — effort L — risk med — category: lean
  Why: wild. The idea is a fixed total of injected tokens and hook milliseconds, with each capability bidding from its measured yield each generation. A new capability can enter only by outbidding an old one. Assumption: yield per capability can be computed from outcomes and exams.
  Done when: a generation run allocates the budget, a capability with no measurement gets the floor, and a new entry that cannot fit is refused.

- **Wild: Quiz a cold child on picking the verb** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: wild. The child sees only `fm help`, gets 30 plain-English intents and names the verb for each. Verbs never picked, and verb pairs that get confused, become retire or rename candidates. It needs no tools and costs a few cents.
  Done when: the quiz scores a pick rate per verb and lists the three most confused pairs.

- **Wild: Show remaining life in every verb's help line** — FEATURE — value 2 — effort S — risk low — category: lifecycle
  Why: wild. Each verb carries `(life 41d)`, reset by use, and a verb at zero is hidden from default help but never deleted without a task. A visible lifespan makes the growth cost felt, which a hidden usage count does not. Assumption: the verb's last use is already in the usage ledger.
  Done when: `fm help` shows a life count that resets after the verb is run, and a verb at 0 days disappears from default help but still runs.

Next question: which of Foreman's capabilities has the user never invoked by hand, and would anyone notice if it were off for a month?
Next question: what is the smallest install that still stops the commands the guard exists to stop, and what does the user lose with each step up from it?
