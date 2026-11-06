# Brainstorm — lens: multi-agent deliberation

- **Sort every disagreement by its cause, then route it** — FEATURE — value 5 — effort M — risk low — category: deliberation
  Why: the pack has panels, debates and `fm second`, but no idea types *why* panelists split. Facts, values, definitions, framing and missing information each need a different resolver. Assumption: the panel's output can be tagged with a cause cheaply.
  Done when: a seeded split between two panelists is tagged and sent to the matching resolver (fact → probe, value → taste model or ask, definition → glossary, missing info → fm-recon), with the route recorded in the brief.

- **Mine the interests behind each position** — FEATURE — value 4 — effort S — risk low — category: negotiation
  Why: deadlocks come from positions ("use a queue", "keep it synchronous"). A mediator agent extracts each camp's stated constraints and proposes a third option that satisfies both. Assumption: most real splits have a feasible synthesis.
  Done when: on a recorded deadlocked panel, the mediator outputs a table of positions vs interests plus one synthesized option that passes every listed constraint, and the main thread can accept it with one command.

- **Co-design the deciding experiment with adversarial collaboration** — FEATURE — value 4 — effort M — risk low — category: debate
  Why: debates in the pack end in judgment. Here two agents holding opposite hypotheses must jointly write the probe both agree would change their mind, committing before it runs. This is stronger than an experiment agent imposed on both.
  Done when: `fm second --collab` produces a probe file signed off in advance by both sides with a "I will concede if…" line each, and the run's result auto-updates the decision record.

- **Compute the verdict from an argument graph** — FEATURE — value 4 — effort L — risk med — category: reasoning
  Why: the pack's dissent register and minority report keep opinions, not structure. Claims, supports and attacks stored as a graph let a small solver (grounded semantics) show which claims survive unrebutted. Dangling attacks mark what was never answered.
  Done when: a panel run emits a graph file, `fm task graph T-id` lists surviving and defeated claims, and a test with a hand-built graph yields the known grounded set.

- **Bind arguments to citations that resolve mechanically** — CLEAN — value 4 — effort S — risk low — category: rigor
  Why: persuasive but unsupported panelist claims sway judges. A validator checks every cited `file:line`, ledger event or brief line, and uncited or unresolvable claims are struck from the tally and flagged.
  Done when: a panel transcript containing a fabricated citation has that claim excluded and listed under "struck", and a test pins this.

- **Audit every flip in a panelist's position** — FEATURE — value 3 — effort S — risk low — category: groupthink
  Why: the pack detects groupthink between panelists but not why one agent changed its mind. A flip must name the new evidence; rhetoric-only flips (the same facts, a different mood) are marked as capitulation and discounted.
  Done when: in a two-round panel, a flip with no new citation shows as "capitulation" in the report and its vote weight drops.

- **Keep case law for panel rulings** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: decisions and lessons are recalled, but rulings on *disputes* aren't stored as precedent. Store the dispute, the ruling, the distinguishing facts and any later overruling. Retrieval cites precedent, and a new panel must say "following X" or "distinguishing X because…".
  Done when: opening a panel on a dispute similar to a stored one surfaces the precedent, and the final record contains an explicit follow-or-distinguish line.

- **Let any lane raise a point of order mid-execution** — FEATURE — value 4 — effort M — risk med — category: live objections
  Why: deliberation today happens at plan time, but surprises land during execution. A builder or reviewer files a one-line objection that pauses its lane. A cheap tribunal sustains or overrules it within a time cap, and frivolous objections lower that agent's future standing. Assumption: lane pause and resume already works (heartbeat, exact-step resume).
  Done when: an injected objection pauses a test lane, the tribunal rules, the lane resumes or replans, and the ledger shows objection, ruling and elapsed time.

- **Credit panelists by marginal contribution** — FEATURE — value 3 — effort M — risk low — category: attribution
  Why: weighting by precision and calibration exists, but not "did this seat change the outcome?". Replay finished panels from `fm bench` with each panelist removed (Shapley-style) to find seats that never matter. Those can be dropped, saving tokens.
  Done when: `fm bench panel` prints per-role marginal contribution over N recorded panels, and a role with zero effect is flagged for removal.

- **Pair the inside view with a base-rate view** — FEATURE — value 3 — effort S — risk low — category: forecasting
  Why: the pack has "predict failure from similar tasks" but not as a deliberation seat. An outside-view agent gets only the task fingerprint and bench/ledger base rates, with no plan. A large gap between its estimate and the planner's effort/risk estimate is the escalation trigger.
  Done when: an M/L plan shows both estimates side by side, and a gap over a threshold forces a second planning pass.

- **Watch the council live and bang the gavel (wild)** — FEATURE — value 4 — effort M — risk low — category: UI deliberation
  Why: a distinctly new surface. Foreman-ui shows a panel as stances on a spectrum that visibly shift between rounds, the user can drop in a heckle or a "weigh this more" gavel, and it enters as a named panelist with a veto-style vote. Assumption: round outputs are stored in a streamable format.
  Done when: the desktop app renders a running panel's rounds live, and a user injection appears in the next round's input and in the record.

- **Seat an empty chair for whoever isn't in the room (wild)** — FEATURE — value 3 — effort S — risk low — category: perspective
  Why: audit lenses cover known roles. The empty-chair agent argues for the absent party: the newcomer reading the code in 2 years, the user on Windows, the repo at 10× size, the unattended 3 a.m. run. The chair is rotated by task type and the user can name one.
  Done when: every L plan records one empty-chair objection and its resolution (accepted, rejected with reason), and the chair differs between at least two task types in tests.

- **Draw a stranger juror from another field (wild)** — FEATURE — value 3 — effort S — risk low — category: analogy
  Why: panels of same-model specialists share blind spots. One seat is a deliberately off-domain persona (an ER nurse on triage, an air-traffic controller on handoffs, a game designer on onboarding) who must answer only by analogy. Its yield is tracked, so it keeps the seat only if its ideas get used.
  Done when: a panel includes the stranger seat, its analogy is listed separately in the report, and `fm bench` shows accepted-vs-ignored counts for that seat.

- **Hold a Delphi rounds mode with a convergence stop (wild-ish)** — FEATURE — value 3 — effort M — risk low — category: consensus
  Why: when many cheap agents estimate (effort, risk, root-cause ranking), anonymized rounds with the group's median fed back usually converge. Stopping when the variance flattens bounds the cost, and unresolved outliers are escalated rather than averaged away.
  Done when: a five-estimator run reports per-round variance, stops when it plateaus, and lists the outlier with its stated reason.
