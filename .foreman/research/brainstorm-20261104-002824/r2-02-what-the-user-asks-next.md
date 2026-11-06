# Brainstorm — lens: what the user asks next

- **Meter drive idle gaps while the queue is non-empty** — PERFORMANCE — value 5 — effort S — risk low — category: drive
  Why: five fixes in the same class (T-0575, T-0115, T-2873, T-2900, T-2901), each found only after a held night. The user wants major progress by morning, and no number shows the minutes lost to false waits.
  Done when: `sampo drive report` prints idle minutes with the queue non-empty, a cause per gap, and a total. A replayed fixture of the T-2873 bug shows a nonzero gap.

- **Verify each counted running agent against a live OS process** — FIX — value 4 — effort S — risk low — category: drive
  Why: the drive's three self-authored sources (engine list, event scan, tail) have each disagreed with reality. The OS is the one signal Sampo didn't author.
  Done when: an agent counted as running with no live pid or transcript growth for N minutes is dropped from the wait set with a ledger line. A test with a dead-pid agent releases the drive.

- **Lint public surfaces for private names and brand-bound orchestrators** — CLEAN — value 4 — effort S — risk low — category: site/docs
  Why: the user pushed back that "jarvis" must not show in the animation and that Claude must not be named as the orchestrator.
  Done when: the ship gate fails if site/, README or demo assets contain a configured deny-list term (profile names, hostnames, "Claude" as orchestrator in model-kind scenes). A planted `jarvis` in site/ turns the gate red.

- **Render UI changes to an SVG at task close** — FEATURE — value 4 — effort M — risk med — category: ui
  Why: the user asked for a pane and Smith TUI redesign, and they sleep while it is built. A tests-pass close shows nothing of what changed.
  Done when: closing a task that touches foreman-ui or the Smith TUI attaches a fixture-rendered SVG of the changed states (empty, running, error) to the finish card.

- **Census leftover old-name spellings by surface** — CLEAN — value 4 — effort S — risk low — category: rename
  Why: the Foreman→Sampo rename runs in stages (ids, internals, surfaces, site), and "any Foreman left?" is the obvious next question.
  Done when: `sampo doctor` lists remaining `foreman`/`fm` spellings per surface (docs, skills, site, UI strings, CLI help), minus an allowlist of intentional aliases, with counts.

- **Rewrite stale path references in open items after a module move** — FIX — value 3 — effort S — risk low — category: queue hygiene
  Why: a dropped item cited `fm*.py` paths that became shims in T-2748, so a self-filed item went stale. Four of five recent drops were stale self-filed items.
  Done when: after a move that adds a shim, open items citing the old path are rewritten to the new path or flagged, and none cites a shim path.

- **Keep an interrupt ledger with a zero target** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: "stop asking me for stuff, keep going" is a standing steer, yet ANDONs and questions still reached the user.
  Done when: every prompt, question and ANDON shown to the user is logged with the default Sampo could have taken. The morning card prints the count and the number that had a safe default.

- **Learn the user's vocabulary from corrections** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the user had to correct "jeff/jev" twice and clarify "moons", "tower" and "jarvis is just an endpoint". Children and lenses misread those terms each time.
  Done when: a glossary file records term → meaning → source message, and a generated glossary slice goes into every child's pack. A test shows a cold child resolving "jev" correctly.

- **Generate per-estate routing defaults from the model bench** — FEATURE — value 4 — effort M — risk med — category: local models
  Why: the Louhi model bench measures every local backend, and the next ask is "so route with the best one". Today the numbers sit on a site section.
  Done when: `sampo louhi models --apply` proposes profile defaults (which model per task kind, thinking on or off) with the bench row as provenance. Applying needs a flag, and the diff is printed.

- **Diff the landing pages visually at ship** — FEATURE — value 3 — effort M — risk med — category: site
  Why: 12's landing and forge pages were ported across several tasks, and a layout break doesn't fail a text test.
  Done when: `sampo ship` renders the key site pages headless and writes a before/after image diff. A diff above a threshold holds the push for review under the push grant.

- **Wild: run a moon tournament bracket** — FEATURE — value 3 — effort M — risk low — category: moons
  Why: wild. The user wants wild moons at 10,000 scale and said the earlier ones weren't. Pairing candidates and letting a local judge pick the weirder-and-valuable one gives an ordering without human triage.
  Done when: a bracket run over ≥64 candidates produces a ranked top 8 with each match's reason, and the winners' wildness scores beat the field median.

- **Wild: ratchet a moon's wildness with a local mutator** — FEATURE — value 4 — effort M — risk low — category: moons
  Why: wild. The user said moons "aren't that wild". A below-4 moon goes to the local 27B with "make it stranger, keep the can't/can line true" until a cold reviewer scores ≥4 or three tries fail.
  Done when: a batch of 20 sub-4 moons shows a measurable share lifted to ≥4, with the original kept and a lineage line.

- **Wild: invent moons only this hardware makes possible** — FEATURE — value 3 — effort M — risk low — category: moons
  Why: wild. The estate is a 27B on a server, small Ollama models, decision models, and a 3-minute model switch. Moons grounded in those facts can't be generic.
  Done when: a lens takes the estate file (models, latencies, idle hours) as its pack and produces moons that each cite an estate fact. A cold read confirms none would survive on a generic laptop.

Next question: which of the user's repeated corrections (names, wildness, stop-asking) have never become an automatic check, and how many times was each said before it did?
Next question: what share of last night's drive hours had work waiting while nothing was running, and which of the three running-agent sources caused it?
