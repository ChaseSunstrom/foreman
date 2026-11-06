# Brainstorm — lens: capability map

- **Trace each request clause to a brief, a diff hunk and a test** — FEATURE — value 5 — effort M — risk low — category: traceability
  Why: the best requirements-traceability tools (DOORS, Jama, Gherkin step coverage) trace at the clause level. The pack's Mission asks are one-line, but the grid and Exam are per brief. Nothing numbers the clauses of the ask itself, so a clause can drop out unseen. Assumption: asks decompose into 2–6 atomic clauses.
  Done when: `fm mission clauses <file>` prints each numbered clause with its brief id, or `OMITTED: <reason>`, and a Mission with an unmapped, unreasoned clause fails `fm genesis check`.

- **Make each stated non-goal a diff check** — FEATURE — value 4 — effort M — risk med — category: scope
  Why: MoSCoW's "won't" column is the only part of a request that a diff can violate silently. The pack has "check the diff against the plan's scope" and "decisions not taken", but neither turns a "don't touch X" into a check. Assumption: users state non-goals in prose, such as "leave ledger conservation out".
  Done when: a brief with `Non-goal: path or verb` fails its finish gate if the diff touches it, tested with a planted violation.

- **Ship a request-kind axis template** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: the grid is one fixed shape for every request. A bug needs reproduce, root cause, siblings, regression test and monitor. A feature needs value, rollout, undo and docs. The Heilmeier catechism and Cynefin both choose axes by kind. Assumption: intake can classify request kind from existing task types (FIX, FEATURE, CLEAN, ...).
  Done when: a FIX Mission and a FEATURE Mission print different required axes, and a missing axis is named in the left-out receipt.

- **Keep an outcome-measure cookbook with live readings** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the carried gap is that every Exam names an outcome measure and a live-state reading, and the pack asks how many are vacuous. A library keyed by brief kind (latency p95, recall per language, adoption count, error rate) gives the writer a runnable default, each entry with its read-only command and today's value.
  Done when: `fm exam measure --kind fix-regression` prints a template with a command that runs read-only and a numeric value today, and 3 or more brief kinds are covered.

- **Render each Mission as an assurance case** — FEATURE — value 3 — effort M — risk low — category: proof
  Why: Goal Structuring Notation (used in safety certification) ties a top claim through sub-claims to evidence, so a missing leg shows as an undeveloped node. This fits "exhaustive, and says what it left out". Dissent scores and canaries become evidence nodes. Assumption: the Mission file can carry a claim tree without a new store.
  Done when: the Mission page shows a claim tree where every leaf is a command result or marked "undeveloped", and the check fails on an unmarked leaf.

- **Write a reading manifest per Mission** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: "what I left out" is a guess unless you know what was read. The map already says "3 left out", but at repo level. A manifest of files, ledgers and pack sections each lens actually cited makes omissions factual.
  Done when: each Mission file ends with "Read: N files; never opened among those the grid names: …", and a test shows an unread cited file is listed.

- **Score FMEA risk for each empty cell** — FEATURE — value 3 — effort M — risk low — category: prioritisation
  Why: FMEA (ISO/IEC 60812) ranks failure modes by severity × likelihood × detectability. The pack has sting-ranked angry reviews and regret ranking, but no detectability factor. A silent failure ranks above a loud one of equal sting.
  Done when: left-out cells list severity, likelihood and detectability (1–5 each) and sort by their product, and a cell with no existing detector scores detectability 5.

- **Add a scope dial with a price preview** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: the pack already has "record which scope width a request was taken at". The user never chooses it. Preview the cost: "narrow: 3 cells, ~$X; wide: 14 cells, ~$Y; the rest left out".
  Done when: `fm mission plan` prints three widths with cell counts and cost estimates before filing, and the chosen width lands on the page.

- **Write a press-release-first line for each brief** (wild) — FEATURE — value 3 — effort S — risk low — category: clarity
  Why: Amazon's working-backwards PR/FAQ forces the user-visible win into one sentence before building. A brief that can't state it is a candidate for "doing less". Wild: nobody asked, and the Exam could check that the sentence is true on landing.
  Done when: each brief has a `Headline:` line, and a close fails if the headline's named command doesn't produce the named output.

- **Find the nearest past Mission by grid shape** (wild) — FEATURE — value 4 — effort M — risk low — category: reference-class
  Why: reference-class forecasting, applied to omissions. Hash each Mission's filled, empty and n/a pattern, then show the three most similar past Missions and what their follow-ups turned out to need. This is the only idea here that uses 3 generations of history as evidence.
  Done when: opening a Mission prints three neighbours with their post-close fixes, and a seeded test finds a planted twin.

- **Run an opposite-day Mission** (wild) — FEATURE — value 2 — effort S — risk low — category: dissent
  Why: file the Mission as if the request wanted the reverse ("what would make things worse?") and keep only what survives both framings. A cheap way to find hidden assumptions. It also feeds the dissent-scoring carried gap.
  Done when: a Mission page has an "inverse reading" section, and the overlap with the real slate is listed as "robust".

- **Give each clause a Kano class and a "would anyone notice" test** — FEATURE — value 3 — effort S — risk low — category: value
  Why: Kano separates must-haves from delighters, and "nobody asked, nobody noticed" appears as a shelf idea in the pack. Tagging clauses lets the left-out receipt say which omissions hurt.
  Done when: each clause carries `must`, `expected` or `delight`, and the receipt lists omitted `must` clauses first.

- **Time-stamp Exam readings by when the outcome can be observed** — FEATURE — value 3 — effort S — risk low — category: exam
  Why: some outcomes read only after days, as in the M-12 "survives 14 days" spike. The pack has "dated bets" and a stale verdict. Declaring the observation delay up front stops a brief from closing on a reading that can't yet exist.
  Done when: an Exam line carries `observable-after: Nd`, and `fm task finish` reports "pending until <date>" rather than pass or fail.

Next question: which of these clause-level or axis-level checks would the user actually read, and which would they just skim past and trust?
Next question: when a request has no clear atomic clauses (a vague "make it better"), what does exhaustive coverage even mean, and who decides?
