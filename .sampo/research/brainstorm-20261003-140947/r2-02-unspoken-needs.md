# Brainstorm — lens: unspoken needs

- **Make every Foreman-written file render-safe from the start** — FIX — value 4 — effort M — risk low — category: output hygiene
  Why: the user repeatedly says output "doesn't look right", and the mod needed a later "rows clean every escape sequence" fix. Assumption: raw `fm` output (task text, evidence, commit messages) still reaches panels without one sanitising step.
  Done when: a test feeds ANSI, tabs, CR, wide unicode and 500-char lines through `fm` output and every panel row renders within width with no stray escapes.

- **Add a "one voice" lint across `fm` output, hints and panel text** — CLEAN — value 4 — effort M — risk low — category: consistency
  Why: the user steered "everything still doesn't match foreman", with duplicated and mismatched items (AC vs audits, buttons, header). Assumption: the wording, casing and glyphs of status strings live in several places.
  Done when: a test fails if two surfaces name the same state with different words or glyphs, such as "audits" and "AC".

- **Keep a per-session "user said no" ledger the guard and rules consult** — FEATURE — value 4 — effort M — risk med — category: user intent
  Why: the denied `rm` of the dev-mods copy is recorded only as "dropped". The user's "don't type into my terminal" and "never hand me commands" are rules, but a denial isn't remembered across sessions. Assumption: denials are not persisted structurally.
  Done when: after a denied action, the same action in a new session is skipped with a one-line note citing the denial.

- **Add an agent-side "time to first useful action" probe per turn** — PERFORMANCE — value 4 — effort M — risk low — category: perceived speed
  Why: the user said "it feels slow, I don't know", and hook p95 is only ≈30 ms, so the slowness is elsewhere (rule reading, ceremony, round trips). Assumption: the ledger has timestamps to compute it.
  Done when: `fm` reports median seconds from prompt to first edit or probe, split into Foreman-attributable and not, for the last 20 turns.

- **Give parallel lanes a shared context budget and a merged summary** — FEATURE — value 4 — effort M — risk med — category: parallel
  Why: the user asked that parallel work not cause "context/speed/quality/usage issues". Cleanup and merge re-checks exist, but nothing is said about each lane's token cost or how results re-enter the main context. Assumption: lane outputs currently return unsummarised.
  Done when: `fm run --parallel N` returns one capped-length summary per lane plus a total usage line, and refuses N above a computed limit.

- **Pair every new guard rule with the false-positive it was grounded on** — CLEAN — value 3 — effort S — risk low — category: guard quality
  Why: the guard commits show repeated narrow patches (heredoc, backtick, `$'…'`, keywords), and the friction was false positives on Claude's own commands. Assumption: the regression tests don't yet state which real command motivated each rule.
  Done when: each guard test case carries a provenance tag, and a check fails when a rule has no allow-case and no block-case.

- **Wild: Let the dashboard show a "what the user would see right now" screenshot of itself in the ledger** — FEATURE — value 3 — effort L — risk med — category: visual QA
  Why: wild. The user keeps finding visual bugs (duplicate dashboard, mismatched headers) that the 58 mod tests miss, and a snapshot tool with its own tmux already exists. Assumption: the snapshot can run headlessly at task close.
  Done when: a UI-touching task cannot finish without a recorded frame, and a diff against the last golden frame is shown.

- **Wild: Add a "complaint court" that classifies each user complaint as bug, taste or misunderstanding** — FEATURE — value 3 — effort M — risk med — category: self-improvement
  Why: wild. The RSI loop mines friction events, yet the biggest signals are the user's own sentences ("looks weird", "feels slow"). Assumption: those aren't parsed into the loop's input.
  Done when: a complaint in the inbox gets a verdict and a linked fix task, and the loop's digest cites the user's words.

- **Wild: Run a "fresh eyes" Haiku that reads only the user-visible transcript and lists what looks off** — FEATURE — value 3 — effort M — risk low — category: visual QA
  Why: wild. The user's own eyes are the only detector for ugly output today. Assumption: a captured text frame is enough for a cheap model to flag duplicates and unpanelled rows.
  Done when: on a seeded frame with a duplicated dashboard, the pass names the duplication, and it costs under a set token cap.

- **Wild: Offer a "leave it as it is" register for things the user has accepted** — FEATURE — value 2 — effort S — risk low — category: user intent
  Why: wild. Much churn comes from re-touching settled areas, such as the panel look and the deny on removing the dev-mods copy. Assumption: nothing records "settled, don't redo".
  Done when: marking an area settled makes a task touching it show a one-line warning with the reason.
