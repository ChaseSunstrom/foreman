# Brainstorm — lens: delight

- **Open each session with a one-line "where we left off" greeting** — FEATURE — value 4 — effort S — risk low — category: session start
  Why: Resume exists after `/compact` and new sessions, but the user's steers ("JARVIS idled", refusals that don't name the task) show they feel lost at re-entry. assumption: the resume point is currently printed raw, not as a human sentence.
  Done when: starting a session in a project with an active task prints one sentence naming the task, the step, and the next action, and a test asserts its text for a fixture brief.

- **Show each refusal as a before/after command pair** — FEATURE — value 4 — effort M — risk low — category: guard UX
  Why: Several asks (T-0404 focus-in-the-line hint, T-0409 name the task to resume, rm symlink) were refusals that left the user guessing what to type instead. Not the same as "carry its fix" in the list: this renders the refused command next to the corrected one, with the changed token highlighted.
  Done when: a refused `fm focus T-1; sed -i …` yields output containing both lines, with the split into two commands shown, covered by a guard test.

- **Add a "close-out card" at task done that reads like a good commit story** — FEATURE — value 3 — effort S — risk low — category: done moment
  Why: Receipts and proof cards are listed, but not a plain-language three-line narrative (asked, found surprising, proved how) built from the brief, `fm surprise` entries and evidence. assumption: surprises are logged but rarely surfaced at the end.
  Done when: `fm task done` prints a card with "asked / surprised by / proved by" lines populated from the brief, and an empty surprise list collapses that line.

- **Name each lane after what it is doing, not its id** — FEATURE — value 3 — effort S — risk low — category: lanes
  Why: JARVIS runs several lanes and the user speaks in task ids (T-0278, T-0280) that mean nothing at a glance. assumption: lane listings show ids and paths only.
  Done when: `fm lane list` and the UI show a short slug from the brief title next to each id, and the slug is stable across renames.

- **Let the statusline carry a tiny "mood" glyph of the run's health** — FEATURE — value 3 — effort S — risk low — category: statusline
  Why: The user cares that budget stays silent until 75% and that idling is never silent. A single glyph (steady, waiting on background, blocked on you, near pace) conveys that without text. Distinct from the gauge and pace-mood ideas already listed because it is derived only from drive state.
  Done when: the statusline emits one of four glyphs for fixture states (working, background wait, needs-user, pace over 75%), each tested.

- **Offer "undo that" after any Foreman-initiated change** — FEATURE — value 4 — effort M — risk med — category: reversibility
  Why: Cleanup, lane merges, tidy and focus changes are all outward actions on a repo the user shares with sessions mid-task. assumption: only some commands have an explicit inverse. Differs from the snapshot idea by being one friendly verb tied to the last Foreman action in the ledger.
  Done when: after `fm lane merge`, `fm undo` restores the prior main HEAD and says what it did, tested on a temp repo.

- **Give `fm help` a "you probably want this" row based on the current state** — FEATURE — value 3 — effort S — risk low — category: discoverability
  Why: There are 70+ commands; usage data (`fm usage`) already shows unused ones. assumption: help is static tiers.
  Done when: in a state with an inbox item and no active task, `fm help` places `capture`/`focus` first, with a test per state.

- **Wild: Let the band breathe with the pulse of the work** — FEATURE — value 2 — effort M — risk low — category: motion
  Why: wild. The band is stateful; a slow idle breathing while background jobs run, a quick tick on evidence, and a stillness when blocked would make "is it alive or stuck?" answerable without reading. Honours reduced-motion.
  Done when: the band shows three distinct animation states in the mod, disabled when reduced motion is set, with a snapshot test per state.

- **Wild: Hand the user a "field notes" page Foreman writes about their own habits** — FEATURE — value 3 — effort M — risk low — category: personality
  Why: wild. Taste and usage data exist; a dry, affectionate weekly page ("you reject anything that adds a verb; you ask for releases on Fridays") turns telemetry into something people share. Overlaps taste portrait only in source data; this is a periodic, witty digest.
  Done when: `fm digest --notes` writes a page with at least three observations, each citing a ledger event, and all edits to it are user-writable.

- **Wild: Name the session's "unsung fix" at the end of a long run** — FEATURE — value 2 — effort S — risk low — category: recognition
  Why: wild. Long unattended runs produce dozens of micro-fixes; surfacing the one that removed the most future friction (by recall hits or repeated refusals eliminated) rewards the discipline and teaches what mattered.
  Done when: the end-of-run summary names one task with a stated reason derived from ledger counts, and is deterministic for a fixture ledger.

- **Wild: Let the user pin a "lucky charm" rule that Foreman greets when it saves them** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: wild. When a veto or lesson actually blocks a repeat mistake, a short "that one again — caught" line credits the rule by name, so the user sees rules earning their keep and prunes the ones that never fire.
  Done when: a guard block caused by a veto prints the veto's text and increments a visible hit count shown in `fm vetoes`.

- **Make the first run feel guided: an interactive `fm hello` that does a real tiny task** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: Install is one line and then 70 commands. assumption: no guided first task exists. A scripted FIX on a scratch repo teaches capture→plan→verify→done in two minutes.
  Done when: `fm hello` creates a throwaway repo, runs a three-step task with real evidence, and ends with the user seeing their own ledger entry; a test runs it non-interactively.

- **Say "nothing to do" with a reason and a suggestion, never silence** — FEATURE — value 4 — effort S — risk low — category: drive
  Why: The user's repeated complaint: JARVIS idled with 20+ queued and "nothing else to do". Extend the offer-queued-work work so an empty state explains why each candidate was skipped (blocked, deferred, needs approval) and names the cheapest unblock.
  Done when: a drained-queue Stop with deferred items outputs one line per skipped item with its reason, tested with a fixture queue.
