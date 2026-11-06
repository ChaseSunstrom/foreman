# Brainstorm — lens: agent types and roles

- **Add a shared-file steward agent** — FEATURE — value 4 — effort S — risk low — category: agent roles
  Why: T-0428 made builders leave CHANGELOG.md to the main thread, and T-0423 and T-0428 each needed hand-added changelog lines. Lanes that touch shared files cause merge friction, and the main thread spends turns on bookkeeping.
  Done when: two lanes each queue a changelog or doc note, and one steward pass applies both to CHANGELOG.md in a single commit with no merge conflict. A test asserts that no builder diff touches the file.

- **Add an fm-reproducer agent for FIX tasks** — FEATURE — value 4 — effort M — risk low — category: agent roles
  Why: The roster has a debugger (hypotheses) but nothing whose sole job is turning a report into a minimal failing case. `fm task prove` needs red→green. Intake notes mention reproducing first, but no role owns it, so builders may "fix" what they never saw fail.
  Done when: for a FIX brief, a read-only run emits a runnable repro command plus the observed output. The debugger and builder take that artifact as input. A brief with no reproducible case is marked "unreproduced" instead of proceeding.

- **Add an fm-profiler agent for PERFORMANCE work** — FEATURE — value 3 — effort M — risk low — category: agent roles
  Why: PERFORMANCE is a task type, and `bench_hooks.py` and the hook-SLO items (C089) exist. No specialist measures before changing anything. Builders guess at hot spots.
  Done when: a PERFORMANCE task gets a profile with a ranked cost breakdown before any edit. After the edit, the same measurement is rerun, and the brief records before/after numbers with run counts.

- **Add an fm-designer reviewer lens for UI tasks** — FEATURE — value 4 — effort M — risk med — category: reviewers
  Why: The user steered "beautiful UI with smooth animations" for the Tauri app. The audit lenses (self, intent, adversary, edge, operator, maintainer) have no design lens. Assumption: UI tasks currently pass review without anyone judging the visuals.
  Done when: for a task touching foreman-ui or desktop files, the reviewer reads smoke screenshots and returns findings on hierarchy, spacing, state coverage and motion. It flags a deliberately broken empty-state fixture.

- **Add a mid-task discovery triager** — FEATURE — value 4 — effort M — risk low — category: scope control
  Why: Foreman "captures new requests instead of chasing them", but a builder that finds a side problem has only a binary choice: ignore it or drift. The "scope drift" item (C050) is checked only at done. A small role could sort each discovery on the spot into fold in now, capture as a task, or note as a blocker, with the reason recorded.
  Done when: a lane's "noticed" item gets one of three verdicts within a single call. The verdict appears in the ledger, and a captured item shows up in the queue with its source task.

- **Add a release-captain agent** — FEATURE — value 3 — effort M — risk med — category: agent roles
  Why: T-0431 (Release 1.2.16) is active, and one-command releases (C086) were requested. Releasing is a fixed sequence (changelog, version bump, gates, install round trip) done by hand each time. A named role with a checklist and evidence output would make the sequence repeatable.
  Done when: the captain's run produces a release PR or tag candidate with a checklist showing each gate's evidence. It stops before publishing and asks.

- **Let agents file grievances against instructions** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: `fm friction` digests blocks, corrections and steers from the user's side. Agents that hit contradictory or impossible instructions, such as a guard rule versus a brief step, have no channel. T-0275 and the refusal-fix items suggest those conflicts exist. This differs from the "noticed" field: it is specifically "this rule blocked me for no good reason" and is aggregated per rule.
  Done when: a child return can carry `grievance: {rule, what_i_needed}`. `fm friction` lists the top rules by count and a recon pass proposes edits.

- **Dispatch stack-specialist builders from the project map** — FEATURE — value 3 — effort M — risk med — category: agent roles
  Why: The repo spans Python libs, a Tauri/Rust app and a TSX mod (register.tsx). One generic fm-builder serves all of them. Assumption: stack-specific idioms and pitfalls would reduce rework. Pitfall packs exist as ideas, but nobody picks the agent flavour from `fm map` layout.
  Done when: a task touching `.tsx` files gets a builder variant loaded with that stack's checks and conventions. Bench shows the variant is no worse than the generic builder.

- **Write a chronicler that narrates from raw events only** — FEATURE — value 3 — effort M — risk low — category: reporting
  Why: Close-outs are written by the actor, so they carry its own framing, and "hindsight rewriting" is already a worry. A separate read-only role produces the user-facing summary from ledger events and diffs. It cannot see the builder's own prose.
  Done when: the summary lists only claims traceable to a ledger event or diff hunk, and each claim is linked. A test seeds a false builder summary and the chronicler's version omits it.

- **Wild: Employ an ombudsman agent that works for the user against Foreman** — FEATURE — value 4 — effort M — risk med — category: oversight
  Why: Wild. The user's steers include "cleanup requests never got done — trace why". An independent role could audit Foreman's own conduct weekly: asked-for-but-undone items, over-asks, ignored steers. It reports to the user directly, not through the main thread.
  Done when: the weekly report cites each dropped request with its message and what happened since. The report is written by a run that cannot edit state.

- **Wild: Audition agent configurations on a one-minute probe** — FEATURE — value 3 — effort M — risk med — category: routing
  Why: Wild. Routing today is by task type and tier. Before a long L lane, run two or three cheap candidate setups (model, effort, role card) on a bounded probe of the real task, such as "find the failing test and propose step 1". Score them on the probe and cast the winner.
  Done when: the ledger records the audition scores and the chosen setup. On the bench, auditioned choices beat the static default on cost per first-time pass.

- **Wild: Exchange role cards with bench provenance** — FEATURE — value 2 — effort L — risk med — category: ecosystem
  Why: Wild. Roles are prompts plus tool scopes plus bench scores. Export a role as a card carrying its measured record, and import someone else's. Imports run on the local bench and are rejected if they regress. Assumption: Foreman users want to share roles.
  Done when: `fm role export` writes a card with scores. Importing a card runs the local bench and refuses one that lowers any gated metric.

- **Add a grader-of-graders for new roles** — FEATURE — value 3 — effort M — risk low — category: agent roles
  Why: Roles such as the reproducer, profiler and designer would multiply the roster without evidence they help. A probation rule says each new role runs shadowed on N real tasks. The main thread records whether its output was used or discarded. After N tasks, the role is kept, revised or removed.
  Done when: each new role has a probation record, and one with 0 uses in N tasks is flagged for removal in `fm doctor`.
