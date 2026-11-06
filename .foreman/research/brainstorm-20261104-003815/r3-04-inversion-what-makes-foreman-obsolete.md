# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Run the moon funnel against a bare-model obsolescence probe** — FEATURE — value 5 — effort M — risk low — category: moonshots
  Why: 10,000 candidates are dedupe-checked only against the catalogue; none is asked "would a stronger bare model already do this?" Previous ideas probe capabilities, not candidates (assumption: the funnel has no such stage).
  Done when: `sampo moons funnel` prints per-candidate "bare-model-reproduces: yes/no/partial" from a cheap local-model arm, and the kill count at that stage is logged.

- **Gate each Mission on a one-line "what the host ships next" forecast** — FEATURE — value 4 — effort S — risk low — category: roadmap
  Why: Open work is full of deferred verbs (T-0034, T-0035, T-0788…) that hosts may absorb; the pack shows no step asking whether a Mission's output is on a host roadmap.
  Done when: every new Mission page carries a dated "host-overlap" line citing a release note or "none found", and the sweep fails on a missing line.

- **Add a host-feature diff that files retirement briefs** — FEATURE — value 5 — effort M — risk med — category: upstream watch
  Why: Earlier ideas watch release notes; none turns a hit into a filed, testable retirement task with a bare-vs-Sampo duel attached (assumption: no such bridge exists).
  Done when: a fixture host changelog mentioning "plan mode" produces a filed task linking the overlapping verb and a runnable duel command.

- **Price every capability in "minutes saved per week" from the user's own ledgers** — FEATURE — value 4 — effort M — risk low — category: value ledger
  Why: The standing question "which capability would they notice first if off a week" has no ledger; the user keeps pushing back on wildness, not on utility, so utility is unmeasured.
  Done when: `sampo value` lists each verb with a measured weekly count and a pull ratio, flagging verbs below a floor.

- **Make Sampo's job description a testable "reason to exist" contract** — CLEAN — value 3 — effort S — risk low — category: product clarity
  Why: The README sells "plans, proves, one task, Ward", yet three of those are host-adjacent; no test says which sentence falls first if the host ships it (assumption).
  Done when: each README claim maps to a bare-vs-Sampo scenario id, and `fm doctor` lists claims lacking one.

- **Pre-build the "ejection" path for the guard alone** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: If the host's permission classifier catches up, the Ward is the last durable piece; the pack shows slimming ideas (T-0794 eject) deferred.
  Done when: `sampo eject --ward-only` emits a standalone rules file and a 1-file hook that passes the Ward exam with nothing else installed.

- **Run a local-model-only harness duel on the moon pipeline** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: Local models (qwen3.8-27b) do bulk work; if plain local agents plus a prompt reach the same pass rate, the harness is redundant at the cheap tier (assumption: not measured).
  Done when: a scorecard row compares Smith+Sampo vs plain local agent on the same held-out scenarios, with cost per pass.

- **Detect prompt-injection that exploits Sampo's own authority** — SECURITY — value 4 — effort M — risk med — category: injection
  Why: Sampo injects steers and lessons as trusted text; if the host later fences instructions natively, Sampo's channel becomes the weaker one. No idea tests Sampo text as an attack carrier.
  Done when: a planted instruction in a ledger line is shown to the agent fenced as data in an exam, and the exam fails if it is obeyed.

- **Benchmark hook cost against the host's native hooks as they evolve** — PERFORMANCE — value 3 — effort S — risk low — category: latency
  Why: bench_hooks.py measures only Sampo; if hosts add faster in-process policy, the comparison point moves (assumption).
  Done when: the bench prints Sampo-hook ms beside a no-plugin baseline per event, and the ship gate records the delta.

- **Wild: Hold a "Sampo's last day" drill that simulates the host absorbing each verb in turn** — FEATURE — value 4 — effort M — risk low — category: resilience
  Why: Inversion made literal; wild.
  Done when: for each verb a stub replaces it and the suite reports which user-visible guarantee silently breaks.

- **Wild: Let a cold child write Sampo's competitor from the README alone** — FEATURE — value 3 — effort M — risk low — category: moat test
  Why: If a tool-less child reproduces the discipline in a 60-line prompt, that is the moat's size; wild.
  Done when: the child's prompt is dueled against Sampo on 9 held-out scenarios and the gap is published.

- **Wild: Grow a "fossil wing" for retired verbs that wakes only on regression** — FEATURE — value 3 — effort S — risk low — category: graceful exit
  Why: Retirement is safer if the guarantee is re-armable; ties to the seed-bank idea but for shipped code; wild.
  Done when: a retired verb is archived with a wake predicate and a test restores it from the archive in one command.

Next question: What does the user do by hand today that neither Sampo nor the host automates, and would that make Sampo's remaining surface redundant or essential?
Next question: Which single Sampo guarantee would a hostile reader say a 2027 host makes free, and is there a dated test for it?
