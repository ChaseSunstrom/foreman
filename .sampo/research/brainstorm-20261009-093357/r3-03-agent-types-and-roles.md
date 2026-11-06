# Brainstorm — lens: agent types and roles

- **Add an fm-architect agent that ships fitness functions** — FEATURE — value 4 — effort M — risk low — category: agent roles
  Why: Today only builder/reviewer/recon/scout/debugger exist; L tasks get approaches in the brief but no role owns the design's long-term checks. Assumption: design drift is a recurring cause of rework.
  Done when: an L FEATURE plan spawns fm-architect, whose output includes ≥1 executable fitness check added to the brief's criteria and run at done.

- **Add an fm-closer agent for the done tail** — FEATURE — value 4 — effort M — risk low — category: agent roles
  Why: Done tail (CHANGELOG, docs, lessons, cleanup, ledger) is left to the main thread (T-0428) and the user said cleanup requests "never got done". A dedicated role owns it with a checklist.
  Done when: a finished task spawns fm-closer, and `fm task done` refuses until its returned checklist (changelog, docs, leftovers swept, lesson recorded) is all marked.

- **Add an fm-remediator that consumes audit findings** — FEATURE — value 4 — effort M — risk med — category: agent roles
  Why: T-0034 (headless audit lenses) is deferred; reviewers produce findings but nobody turns them into verified fixes. Remediator takes one finding, writes a failing test, fixes it, hands back.
  Done when: given a findings file with 3 items, remediator lanes produce 3 red→green commits, each citing its finding id.

- **Add an fm-interrogator agent for intake** — FEATURE — value 4 — effort M — risk low — category: agent roles
  Why: Intake is done by the main thread; the user's steers (cleanup never done, re-asks) show misreadings. A read-only role that reads only the raw request and the brief, then lists clauses unaccounted for, ambiguities, and XY smells.
  Done when: for a multi-clause request, the interrogator's output maps every clause to a criterion or a stated non-goal, and unmapped clauses block brief approval.

- **Add an fm-historian agent (Chesterton's fence)** — FEATURE — value 3 — effort S — risk low — category: agent roles
  Why: Cleanup/CLEAN tasks delete code; no role explains why something exists. Historian reads git log, briefs, decisions and vetoes for a path and returns origin and tripwires.
  Done when: a deletion step cannot be marked done until a historian note for each removed file/function is attached.

- **Add an fm-integrator that owns lane seams** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: Parallel lanes (T-0445, T-0446 queued) merge independently; nobody owns interfaces between them. Integrator writes the shared contract first and verifies the combined tree after merge.
  Done when: two lanes touching a shared function signature get a contract file before start, and the post-merge combined gate runs under the integrator's name.

- **Define agent roles as data with a per-role bench** — CLEAN — value 4 — effort M — risk low — category: agent roles
  Why: Five roles are hard-coded as agent files; no evidence which earn their cost. Assumption: role cards (prompt, tools, model, effort, return schema) can live in one data file that fm bench replays per role.
  Done when: `fm bench roles` outputs per-role first-pass rate and cost from finished tasks, and adding a role needs only a data entry.

- **Return a typed "noticed" field from every agent** — FEATURE — value 3 — effort S — risk low — category: agent protocol
  Why: Builders see adjacent bugs and the rule is to capture, not chase, but sub-agent summaries drop them. A required `noticed[]` field is auto-captured into the inbox.
  Done when: a builder that returns a noticed item causes a captured task to appear with provenance of the lane and step.

- **Wild: Hire an agent by sentence** — FEATURE — value 3 — effort L — risk med — category: agent roles — wild
  Why: assumption: user's needs vary (e.g. "a DBA who distrusts ORMs"). `fm hire "..."` synthesizes a role card, runs it against 3 replayed past tasks to check it behaves, and registers it.
  Done when: `fm hire` produces a role card plus a bench report, and the role is selectable by lanes.

- **Wild: Give each module a spokesperson agent** — FEATURE — value 3 — effort L — risk med — category: agent roles — wild
  Why: assumption: recon repeatedly rereads the same areas. A per-module agent with a distilled, tree-hash-invalidated context pack answers "how does X work, what breaks if I touch it" for other agents cheaply.
  Done when: a recon question on a module is answered from its spokesperson pack with no file reads, and the pack is marked stale after a touching commit.

- **Wild: Seat an empty chair for whoever isn't in the room** — FEATURE — value 3 — effort M — risk low — category: agent roles — wild
  Why: Plans consider the user but not downstream consumers, future maintainers or the operator at 3am. A role argues each absent party's interest in L plan reviews and records objections in the dissent register.
  Done when: an L plan review output has a section per absent party with at least one concrete objection or an explicit "none found, because…".

- **Interview every sub-agent on exit** — FEATURE — value 3 — effort S — risk low — category: agent protocol
  Why: Summaries drop what children tried and discarded. A short fixed exit interview (what surprised you, what did you skip, what would you check next) is stored with the lane.
  Done when: every lane record has an exit-interview block, and `fm recall` can find it.

- **Pair every builder with a rotating critic role** — FEATURE — value 3 — effort M — risk med — category: orchestration
  Why: Reviewers currently run after the fact with one lens; a critic assigned a distinct failure to hunt (edge, adversary, maintainer) per task, chosen by what the task type historically escapes on, raises catch rate. Assumption: escape data exists in the ledger.
  Done when: the critic lens per task is chosen from escape stats and logged, and its findings appear in the done packet.

- **Detect role drift in the ledger** — CLEAN — value 2 — effort S — risk low — category: agent protocol
  Why: Read-only roles (reviewer, recon, debugger) should never edit; builders should not merge. Assumption: tool-call events carry agent type.
  Done when: `fm doctor` flags any ledger event where an agent acted outside its role's declared permissions, tested with a fabricated event.
