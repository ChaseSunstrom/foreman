# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Run a host-absorption diff on every upgrade** — FEATURE — value 5 — effort M — risk low — category: obsolescence
  Why: the pack's open work (T-0335/T-0337) shows non-Claude hosts lagging, and earlier ideas only watch release notes; nothing diffs the host's real command and tool surface against Sampo's verbs. Assumption: the host exposes `--help` or a tool list that can be parsed.
  Done when: after a host version change, `sampo doctor` prints a table of Sampo verbs with the host feature that overlaps each, or "none", and files a retirement brief for each overlap.

- **Score each capability against the bare model on the user's closed tasks** — PERFORMANCE — value 5 — effort L — risk med — category: counterfactual
  Why: the "Questions left" ask which capability the user would notice missing first; the duel T-1231 is deferred and no per-capability delta exists. Assumption: closed tasks can be replayed headless with one capability muted.
  Done when: a table lists every capability with first-time-pass delta and cost delta versus bare, with confidence intervals, and any with delta ≤ 0 is flagged "retire candidate".

- **Compile each steer into a bare-model pass/fail pair** — FEATURE — value 4 — effort M — risk low — category: steers
  Why: the 80 standing steers are injected as prose; if a stock model already obeys one unprompted, it's dead weight. Assumption: most steers can be phrased as a checkable scenario.
  Done when: `sampo steer audit` runs each steer's scenario with and without the steer on a bare model and marks each "needed" or "native".

- **Make the Ward an exportable standalone guard** — SECURITY — value 5 — effort M — risk med — category: survival
  Why: the Ward is the one capability a host is least likely to match in a user's own rules, and the pack stresses non-Claude hosts and the shim plugins. If everything else is absorbed, this alone must still run. Assumption: the rules engine has no hard dependency on the rest of the package.
  Done when: a single-file Ward runs under a hook of any listed harness with zero imports from `sampo.*`, and its Ward exam passes unchanged.

- **Measure hook cost as a share of the host's native turn** — PERFORMANCE — value 4 — effort S — risk low — category: overhead
  Why: `bench_hooks.py` exists but reports absolute milliseconds; obsolescence appears when native hooks get faster than ours. Assumption: host turn latency can be read from its transcript timestamps.
  Done when: the bench prints hook time as a percentage of median turn time per event, and the ship gate fails above a stated percentage.

- **Add an eject path that leaves the user's repo with no Sampo residue** — CLEAN — value 4 — effort M — risk low — category: exit
  Why: T-0794 lists "eject" as deferred; a product that is easy to leave is trusted longer, and the user asked for harness-neutrality. Assumption: all writes land under known state paths and marked blocks.
  Done when: `sampo eject --plan` lists every file and config entry, and after apply a diff against a pre-install snapshot is empty except an exported GOAL/lessons bundle.

- **Tag each lesson with the model version that taught it and retest on upgrade** — FEATURE — value 4 — effort M — risk low — category: lessons
  Why: T-0217 gives lessons a confidence, but nothing expires one when a stronger model stops making the mistake. Assumption: a lesson comes with a reproducible failing scenario.
  Done when: on a model ID change, each lesson's scenario is rerun bare and lessons that pass are marked "absorbed" and stop being injected.

- **Gate new verbs on a "native-by" forecast with a sunset date** — CLEAN — value 3 — effort S — risk low — category: governance
  Why: the Genesis machinery adds capabilities by the dozen and never removes one except by proven harm. Assumption: a forecast date is a reasonable proxy.
  Done when: `sampo genesis check` fails a new capability lacking a sunset date and a measurable retire-when predicate.

- **Secure the retirement path itself against silent deletion by the push grant** — SECURITY — value 3 — effort S — risk med — category: safety
  Why: a question left open asks whether the standing push grant lets a deletion ship unattended; removing a guard clause is the worst deletion. Assumption: protected files are enumerable.
  Done when: any retirement touching a guard clause or protected-core path blocks `fm ship` until a human-signed token exists, shown by a failing test.

- **Wild: Run a quarterly "Sampo's last day" drill** — FEATURE — value 4 — effort M — risk low — category: rehearsal
  Why: wild. Each verb is simulated as absorbed by the host in turn, and goals are completed with it disabled.
  Done when: a report shows which goals still pass with each verb off, and the verbs that never mattered are listed.

- **Wild: Let a cold child write Sampo's competitor from the README alone** — FEATURE — value 3 — effort M — risk low — category: competition
  Why: wild. If a tool-less child can rebuild the discipline in 50 lines from the public pitch, that part is already commodity.
  Done when: the child's rebuild runs against the exam's finders arm and the score gap against Sampo is recorded per capability.

- **Wild: Keep a fossil wing for retired verbs that wakes on regression** — CLEAN — value 3 — effort M — risk med — category: retirement
  Why: wild; the no-idea-killed rule conflicts with lean pressure, and dormant-with-wake-predicate satisfies both. Assumption: a regression signal exists per verb.
  Done when: a retired verb costs zero injected characters and zero hook time, and re-enables itself in a test when its predicate fires.

- **Add a retire-when counter that cites the false done each gate prevents** — FEATURE — value 4 — effort M — risk low — category: evidence
  Why: the six known false dones are the only hard proof the goal path earns its place. Assumption: the long tier can replay them against the host's native goal mode.
  Done when: each done-gate clause lists the false done it blocks and the date a bare host first passes it.

Next question: Which single capability would the user keep if everything else were absorbed, and does the pack's usage data show it?
Next question: What is the cheapest signal that a host or model release has made a verb redundant, available before the user notices?
