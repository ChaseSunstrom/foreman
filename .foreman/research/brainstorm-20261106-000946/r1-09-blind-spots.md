# Brainstorm — lens: blind spots

## The missed asks, and the questions they should have caught

**T-3312 (Kalevala depth), T-3316 (headroom census), T-3321 (fleet git-refs), T-3339 (landscape scan), T-3340 (bench queue fixture), T-3342 (mirror rename), T-3352 (hook latency), T-3353 (prompt injection).**

The common thread: every one of these was a **capability the user had to name themselves**, and no earlier lens asked *"what fixed set/cap/surface/measure does this project already have that nobody has ever inventoried?"* or *"where is the boundary between this box and the outside?"*

The single un-asked question for the whole project: **For every "Sampo does X", can Sampo answer "what is the complete set of X, and what is the maximum X can grow to?"** — i.e., does every capability ship with its own census and its own ceiling, or only its happy path?

Secondary question: **Every external surface (host, network, other agent, other machine, other user) is treated as *data* by some capability — but is there one capability that treats *Sampo's own outputs* as an external surface to be scanned?** The blind spots cluster at boundaries, and the boundary of "what Sampo said into the world" is the one nobody mapped.

---

## Ideas (blind-spot lens)

- **Name a "boundary census" verb that lists every external surface Sampo touches and what it sends to each** (FEATURE) — value 5 — effort M — risk low — category: audit
  Why: T-3321 (git-refs fleet), T-3339 (landscape scan), T-3342 (mirror rename), T-3353 (prompts) are all boundary asks the user had to make. No capability answers "what does Sampo send to git, to the network, to the host, to other machines, to the model, and what does it keep." This is the class of T-3316 (headroom) generalized: a capability that inventories its own edges.
  Done when: `sampo boundary` prints one line per surface (host hooks, git, network, local models, other machines, model endpoints, public site) with what bytes crossed in the last 24h and which grant covers it.

- **Give every "fixed set" capability its own ceiling and census, or refuse to call it a capability** (FIX) — value 5 — effort M — risk low — category: coverage
  Why: T-3312 (Kalevala depth) and T-3316 (headroom) both exist because a capability (genesis depth, caps) had no "what is the complete set" answer. The user asked for the census and the cap because the pack never surfaced them. Every capability in the grid should ship with `samo cap <name>` and `samo census <name>` or be marked n/a with a reason.
  Done when: every coverage.md row has a `cap:` and `census:` field, and `sampo doctor` flags any row missing one.

- **Make "what did Sampo just say into the world?" a first-class scan target** (FEATURE) — value 5 — effort M — risk med — category: security
  Why: T-3353 (prompt injection) and T-3339 (landscape scan) and T-3321 (fleet refs) all touch "text crossing a boundary." But no capability scans *Sampo's own outbound* (morning card, site publish, forge comments, PR bodies, ledger lines shared across machines) for the same injection classes the Ward guards inbound. The blind spot: the Ward guards the model's *inputs*; nobody guards Sampo's *outputs* as a boundary.
  Done when: `sampo egress` scans the last 24h of outbound text (site, forge, PR, shared ledger) and reports any line matching an injection class or a canary.

- **Wire every capability to its own "what is the maximum this can grow to" — a headroom line in the capability map** (FEATURE) — value 4 — effort S — risk low — category: coverage
  Why: T-3316 (headroom census) was the user asking for a cap inventory. The question a brainstorm should have asked: "for each capability, what is the hard ceiling, and what happens when it is hit?" The capability map (lens: capability map) lists capabilities but not their ceilings.
  Done when: each capability row in the map has a `max:` field and an `overflow:` behaviour (queue, drop, fail, escalate).

- **Name the "other machines" surface explicitly and give it its own data-flow ledger** (FEATURE) — value 5 — effort L — risk med — category: privacy
  Why: T-3321 (fleet git-refs) and the standing steer "manage across sessions… even without direct access… not only one machine" both point to a multi-machine surface that no earlier brainstorm mapped as a *data-flow boundary*. The question: "when Sampo on machine A sends anything to machine B, is that send logged, granted, and reversible?" The pack treats other machines as an assumption, not a surface.
  Done when: `sampo fleet` shows per-machine send/receive ledger with grant refs, and a `sampo fleet cut <machine>` that severs and records the severance.

- **Give the landscape scan a "what did I already build that this would make obsolete" column** (FIX) — value 4 — effort S — risk low — category: coverage
  Why: T-3339 (landscape scan) lists new items but never asks "does this new tool replace a capability Sampo already has?" The blind spot: a scan that only adds, never subtracts. The user had to ask for the scan; nobody asked what the scan should *remove*.
  Done when: each landscape item carries a `replaces:` field naming a Sampo capability or "none," and `sampo doctor` flags capabilities with no `replaces` challenger for 90 days.

- **Make the bench fixture a *living* thing that names what it covers and what it leaves out** (FIX) — value 4 — effort M — risk low — category: measurement
  Why: T-3340 (bench queue fixture) was a user request to *build* the fixture. The blind spot: a fixture with no "what is this bench's domain?" answer. The question a brainstorm should have asked: "what is the complete set of task kinds this bench exercises, and what is the first kind it does not?"
  Done when: `samo bench scope` prints the covered task kinds and the first three uncovered kinds, with a "add to bench" command for each.

- **Give the mirror rename a permanent "old-name residue" counter in `samo doctor`** (FIX) — value 4 — effort S — risk low — category: reliability
  Why: T-3342 (mirror rename) was the user catching a rename residue. The blind spot: renames are treated as one-shot; nobody asks "how many references to the old name remain, and when will they be gone?" The class: every rename or migration leaves a residue that decays, and no capability tracks the decay.
  Done when: `samo doctor` prints `old-name residue: N` per active migration, and `samo migrate` records a residue-decay curve.

- **Wire hook latency to a "budget per hook" and name the hook that is eating the budget** (FIX) — value 4 — effort S — risk low — category: performance
  Why: T-3352 (measure hook handler) was the user asking for the number. The blind spot: a latency number with no "what is the budget, and which hook is over?" The class: every measured quantity without a budget is a number, not a control.
  Done when: each hook has a `budget_ms` in the hook table, and `samo doctor` prints the worst-budget-violator per session.

- **Treat "Sampo's own prompts" as an external surface with its own injection scan** (FEATURE) — value 5 — effort M — risk med — category: security
  Why: T-3353 (prompt injection) is the user asking to scan *the prompts Sampo loads*. The blind spot: the Ward guards the model's tool-call inputs; nobody guards the *prompt text Sampo injects* (MASTER.md, skills, hooks, cards) as a boundary. The question: "if a repo file, a lesson, a card, or a steer contained an injection, does Sampo detect it before it reaches the model?"
  Done when: `samo prompt-scan` scans all injected text (MASTER.md, skills, cards, steers) for injection classes and reports the worst offender per session.

- **Name the "what does the user's *other tool* do that Sampo should not?" boundary** (FEATURE) — value 4 — effort M — risk med — category: coverage
  Why: T-3339 (landscape scan) and T-3321 (fleet) both touch "what is outside Sampo." The blind spot: Sampo has no "what does the host or another tool already do" surface. The question: "for every capability Sampo has, what is the host-native equivalent, and does Sampo still add value?" This is the retirement question, but as a *surface*, not a one-time audit.
  Done when: `samo native` prints per-capability: host-native equivalent, Sampo delta, and a retirement probe (a test that fails when the host catches up).

- **wild — Give the *user's silence* a boundary: "what did Sampo say into the silence?"** (FEATURE) — value 5 — effort L — risk high — category: delight
  Why: The pack has "silence as a label" but never "what did Sampo *do* into the silence?" The blind spot: silence is treated as a user signal, not as a *surface Sampo writes into*. The question: "when the user is absent, what does Sampo send into that absence, and is any of it wrong?"
  Done when: `samo silence` prints what Sampo sent (morning card, triggers, self-edits, lane merges) during the user's last absence window, with a "was this wanted?" per-line veto.

- **wild — Name the "what does *this box* know that the *other box* doesn't?" boundary** (FEATURE) — value 5 — effort L — risk high — category: privacy
  Why: T-3321 (fleet) and the multi-machine steer both point to a knowledge-asymmetry boundary. The blind spot: Sampo has no "what is known on machine A but not machine B" surface. The question: "if I lost machine B, what does Sampo on machine A still know, and what does it lose?"
  Done when: `samo fleet know` prints per-machine: knowledge held locally (lessons, models, ledgers), knowledge synced, and knowledge at risk if the machine is lost.

- **wild — Give the *whole project* a "what is the complete set of things Sampo has never been asked to do?" boundary** (FEATURE) — value 5 — effort L — risk high — category: coverage
  Why: Every blind spot in this class is "the user had to name a thing Sampo didn't have." The meta-blind-spot: no capability answers "what is the *absence* in the capability map?" The question: "what is the first task the user will ask for that no coverage.md cell, no capability, and no lens predicts?"
  Done when: `samo void` prints the first three "absent cells" (task kinds with no capability, no lens, no exam) and files a "predict this" task for each.

---

Next question: Does every *outbound* surface (site, forge, PR, shared ledger, other machine) have a named grant, a canary, and a reversal path, or is only the *inbound* surface (Ward) mapped?

Next question: For the user's multi-machine steer ("even without direct access… not only one machine"), is there a *single* capability that answers "what is the complete set of machines, what does each know, and what does each send," or is that answer scattered across fleet, boundary, and privacy with no one owning it?
