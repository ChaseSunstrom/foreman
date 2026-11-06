# Brainstorm — lens: meaning: did it do what the user meant

- **Replay each user pushback as a standing probe over later work** — FEATURE — value 5 — effort M — risk low — category: meaning
  Why: the pack's pushbacks ("don't showcase it as jarvis", "not wild enough", "jev, the classifier") each repeated a meaning miss; the steered list shows the same correction landing three times (never show jarvis, never name Claude). Earlier ideas turn pushbacks into probes in general, but none keys the probe to the *noun or phrase* the user corrected and sweeps every later artifact (scene, README, site, hook text) for it.
  Done when: after a recorded pushback naming a word or role, `sampo check` fails on any new public file containing it, and the failing line quotes the pushback it came from.

- **Compile "I meant X, not Y" into a reading pair** — FEATURE — value 5 — effort M — risk med — category: intent
  Why: "I meant jeff as the classifier, similar to jev" and "no, jev, the classifier model" were two corrections of one misreading. Assumption: intake stores only the final request, never the misreading that was rejected.
  Done when: a correction message creates a record holding rejected reading and accepted reading, and the next plan for a similar ask lists the rejected one under "not what you meant".

- **Ask one disambiguating question when a proper noun has no referent in the repo** — FIX — value 4 — effort S — risk low — category: intake
  Why: "jeff", "jev", "jarvis" were names Sampo could not resolve (jarvis is an endpoint profile, jev needed research). Assumption: a zero-token grep finds no definition for them before the build began. Distinct from earlier "resolve proper nouns": this one proposes a single bounded question with a default, not a block, so it respects "stop asking me for stuff".
  Done when: an ask containing an unresolved capitalised or quoted token yields one question with a default answer and a 60s timeout, and zero questions when every token resolves.

- **Check the rendered artifact against the ask, not the source** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: the animation request produced a scene that said "jarvis" and named Claude; source tests passed but the pictured output was wrong. Assumption: no test reads the rendered SVG text.
  Done when: a criterion can name phrases that must appear and must not appear in a rendered SVG/HTML's extracted text, and a deliberate violation fails the close.

- **Turn "wild", "simple", "like X" into a measurable rubric at intake** — FEATURE — value 4 — effort M — risk med — category: criteria
  Why: the user said the moons "aren't that wild"; the fix was judged only after rejection. Moonshot wildness already has a 1–5 reviewer, but ordinary asks with adjectives do not.
  Done when: an ask containing a quality adjective gets a stated rubric (anchors with examples) in the plan, and the close cites the anchor it met.

- **Echo the endpoint-neutral rule as a lint on every orchestrator mention** — SECURITY — value 3 — effort S — risk low — category: public surfaces
  Why: the brief says public surfaces must name models by role and the orchestrator as any agent. Assumption: only hand-typed lists catch it today.
  Done when: a lint fails the ship gate on a vendor model name, user machine name or product name used as "the orchestrator" in site, README or scene text, with an allowlist for the changelog.

- **Settle each "what I took you to mean" against the user's next message** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the pack's lens question asks which dissents were vindicated; the cheapest signal is whether the following message corrects the reading. Assumption: none recorded today.
  Done when: each plan stores its stated interpretation, and a following correction marks it wrong in a ledger readable by `sampo outcomes` with a per-kind miss rate.

- **Block a close whose evidence checks the builder's sentence, not the user's** — FIX — value 4 — effort M — risk med — category: verification
  Why: T-2873 and the drive fixes show "tests pass" while the user still had to re-ask three times (T-2873 for the same running-agent bug). Assumption: the Done-when was written by the builder.
  Done when: a close quotes the user's original phrase beside each Done-when clause and fails if a clause has no mapped phrase.

- **Run a cold user-proxy over finished artifacts** — FEATURE — value 4 — effort M — risk med — category: meaning check
  Why: the user's words ("not that moon-y") are taste calls a unit test can't make. Assumption: a tool-less child given only the user's last five messages and the artifact can guess "would they push back?".
  Done when: before close, a proxy emits a yes/no with the quoted message it leaned on, and its past calls are scored against real pushbacks in `sampo outcomes`.

- **Wild: Print the pushback before it happens** — FEATURE — value 4 — effort M — risk med — category: foresight (wild)
  Why: assumption: the three top misses (names, wildness, scene wording) were guessable from earlier messages.
  Done when: at plan time a child writes the most likely correction in the user's voice, and a later real correction is scored against it with a match flag.

- **Wild: Freeze a "mystery orchestrator" in every demo** — FEATURE — value 3 — effort S — risk low — category: delight (wild)
  Why: the user wants any orchestrator to work, so scenes should rotate the agent shown; this also makes a hard-coded name visible.
  Done when: rendering a scene five times shows five different role-neutral agent labels with no test edit, and a hard-coded name fails a render test.

- **Wild: Keep a "words I may never say" shelf the user can read** — FEATURE — value 3 — effort S — risk low — category: trust (wild)
  Why: steers about jarvis, Claude and vendor names live scattered across rules. Assumption: no single list exists.
  Done when: one command prints every forbidden or required word with its originating message date, and each entry has an automatic check.

- **Mark each plan clause as quoted, inferred or invented** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the pack reveals Foreman-filed work (T-2884, T-2893) that the user then had to adjust. Assumption: briefs don't distinguish what the user said from what Sampo added.
  Done when: every Done-when line carries one of three tags, and invented lines are listed first for the user to strike.

Next question: Which user corrections in the last 30 days were about a word or label versus about scope, and does the ledger even record that split?
Next question: Does any existing check read what a finished artifact looks like to a stranger, rather than what its source contains?
