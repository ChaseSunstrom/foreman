# Brainstorm — lens: user value

- **Propagate one correction to every open item it touches** — FEATURE — value 4 — effort M — risk low — category: correction reach
  Why: The pack shows the same correction recurring across items. `fm quiet` stdin and `fm code` lease cleanup were both raised separately, so the user restated a fix that applied to other open work too. Assumption: a correction names a file, verb or symptom that other backlog items also cite.
  Done when: Recording one correction against a verb updates every open item that cites that verb, and a fixture with two such items shows both changed from one note.

- **Retire blocked items that a newer request has overtaken** — CLEAN — value 4 — effort S — risk low — category: blocked pile
  Why: The pack lists a stale blocked pile, and several "dropped" entries were redone under new wording, which left the old blocked item behind. Assumption: a newer request on the same subject makes the older blocked item obsolete.
  Done when: Filing a request that matches an open blocked item by subject marks the old one "superseded by T-id" in `fm status`, and the old item leaves the needs-you count.

- **Flag contradictions in the user's own standing instructions** — FEATURE — value 4 — effort M — risk low — category: instruction conflicts
  Why: The user has said "don't ask me for anything" and also approved specific steps, and a steer dropped the RETRY_WATCHDOG step after earlier work had planned it. Foreman currently has to infer which instruction wins. Assumption: standing instructions are stored and can be compared.
  Done when: Two stored instructions that conflict on the same verb or setting raise one question, naming both with dates, before the next queue starts.

- **Stop re-proposing a default the user has overridden twice** — FEATURE — value 3 — effort S — risk low — category: override memory
  Why: The user has pushed back on several defaults already (compact at 200k, builders on Sonnet). Assumption: a default the user has overridden twice will be overridden again.
  Done when: After two recorded overrides of one default, a later plan omits that default from its proposal, and a test shows the proposal text changes.

- **Mute a path's chatter until the user unmutes it** — FEATURE — value 3 — effort S — risk low — category: notification control
  Why: The pack shows many parallel streams (CI, hook bench, site deploy, brainstorm rounds) reporting into one surface. Assumption: the user will sometimes want one area silent for a day.
  Done when: `fm mute <path>` removes messages about files under that path from `fm status` and receipts, and `fm unmute <path>` restores them, verified by a test with two files.

- **Wild: the receipt you can argue with** — FEATURE — value 4 — effort M — risk med — category: receipt as contract
  Why: wild. The user edits the close receipt's wording in place, and each edit becomes the next acceptance check for that task. Their pushback on the pinned-to-commit criteria suggests they care what the check says, not just whether it passed.
  Done when: Editing one sentence of a receipt and saving it creates a new check that appears in the task's proof, and a fixture run shows that check failing on a seeded wrong result.

- **Wild: a whiteboard photo becomes a task graph** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: wild. The user's requests often arrive as a list of steps with dependencies, and a photo of a sketch carries that structure in one shot. Assumption: the user will sometimes plan on paper or a whiteboard before typing.
  Done when: A photo of a boxes-and-arrows sketch becomes a set of queued tasks with `depends-on` edges, and a fixture image with three boxes and two arrows produces three tasks and two edges.

- **Wild: answer a question by pointing at a line** — FEATURE — value 3 — effort M — risk low — category: answer input
  Why: wild. A blocked question often asks which file, function or line is meant, and the user has to type a path. Assumption: pointing at a file:line in the terminal or the web UI is faster than typing it.
  Done when: Pasting a `file_path:line_number` reference as the answer to a blocked question resolves the question and the item clears, verified by a fixture with one blocked question.

- **Wild: a second pane that shows what the user would say next** — FEATURE — value 2 — effort M — risk low — category: anticipation
  Why: wild. Foreman already has the user's past requests and their corrections in the pack, so it can offer the likely next message as a greyed suggestion that the user accepts or ignores. Assumption: the user repeats patterns across sessions.
  Done when: With an open session, a suggested next message appears beside the prompt, and accepting it with one key submits it, verified by a fixture session that repeats a prior request.
