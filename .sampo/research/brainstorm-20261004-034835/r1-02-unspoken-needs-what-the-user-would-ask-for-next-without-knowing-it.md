# Brainstorm — lens: unspoken needs: what the user would ask for next without knowing it

- **Stream reviewer findings as they land** — FEATURE — value 5 — effort M — risk med — category: speed
  Why: 31+ drive stops idle ~1–2 min per review batch. Parking only moves the wait; streaming removes it. The reviewer emits one finding per line (NDJSON) and the drive starts fixing the first while the rest are still being read.
  Done when: a stubbed reviewer that emits three findings 5 s apart gets its first fix started before the third finding arrives (asserted from the ledger timestamps).

- **Review only the delta on re-review** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: reviews find 3–8 issues per batch, so each fix triggers another full pass. Assumption: re-reviews resend the whole diff, which fits ~100k tokens per run (2.0M / 20 runs).
  Done when: a re-review after a one-hunk fix sends a pack containing that hunk plus the prior findings, and its token count is under 30% of the first pass in a test.

- **Order child packs for prompt-cache reuse** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: the user wants to prevent runaway subagent spend without limiting use. Assumption: packs mix stable material (rules, lens text, map) with volatile material (diff) in no fixed order, so cache hits are lost.
  Done when: two lens runs on the same task share an identical byte prefix covering all stable sections, and `fm cost` reports cache-read tokens per child.

- **Track record per research source** — FEATURE — value 4 — effort M — risk low — category: research
  Why: research already verifies quotes and flags single-source claims. Each pass or fail is a free signal about the domain it came from, but the next search doesn't use it.
  Done when: after a quote check fails on a domain, a later `fm research ask` ranks that domain below one with verified quotes, and `fm research sources` shows the pass/fail counts.

- **Stop research on saturation** — FEATURE — value 3 — effort S — risk low — category: research
  Why: the user wants better research without runaway spend. Searching until the budget runs out wastes money, and stopping early wastes quality. Assumption: the loop has no marginal-yield test today.
  Done when: a run whose last two fetches add no new claim stops and reports "saturated after N sources", shown with a stubbed fetcher.

- **Rank ideas by measured friction counts** — FEATURE — value 4 — effort M — risk low — category: triage
  Why: six passes of model-guessed value scores produced a very long list. `fm friction` already counts escapes, stops and false positives, so ideas can be ranked by pain actually measured, with each idea linked to its events.
  Done when: `fm ideas rank` orders a fixture list so that the idea tied to 12 recorded events outranks one tied to 1, and shows the counts.

- **Select impacted tests per step, full suite at close** — PERFORMANCE — value 3 — effort M — risk med — category: speed
  Why: `fmmap` impact already exists and the user asked for speed without losing quality. The close gate stays full, so a missed test is caught at the end.
  Done when: a step touching one module runs only its impacted tests (asserted by a command log), the close gate runs everything, and `fm check` reports any failure the narrow run missed.

- **Wild: Hold a dojo of mutated old failures** — FEATURE — value 3 — effort L — risk med — category: learning
  Why: assumption: idle time and the failure ledger are free raw material. A budgeted child writes variants of past failures (different file, same class) and runs Foreman's guard and gates against them. Misses become lessons and bench cases.
  Done when: `fm dojo --budget 1` makes at least one variant from a recorded failure, runs it, and writes a lesson or bench case only for a variant that slipped through.

- **Wild: Show the source of every whisper** — FEATURE — value 4 — effort S — risk low — category: transparency
  Why: assumption: with this many nudges, hints and lessons, the user eventually asks "why did it say that?". `fm why` names the rule, lesson or config behind any hook output and offers to mute it.
  Done when: `fm why` on the last whisper prints its rule ID, trigger and mute command, and the mute makes the next identical trigger silent.

- **Wild: Export lessons as a redacted skill pack** — FEATURE — value 3 — effort M — risk med — category: sharing
  Why: the user wants Foreman to be "the best plugin possible". Distilled lessons, minus paths, names and secrets, are the kind of thing others would adopt. The command only writes a local folder, and publishing stays with the user.
  Done when: `fm export lessons` writes a skill folder whose content has no absolute paths, emails or token-shaped strings (checked by a scan test), and it never touches the network.

- **Wild: Escalate reviewers from cheap to strong** — PERFORMANCE — value 3 — effort L — risk high — category: tokens
  Why: the user does not want less capability, only less waste. A small model screens first and escalates to the full reviewer only when it flags something or the diff touches a sensitive area. Risk: it could miss real issues.
  Done when: on planted-defect bench cases the escalated setup finds as many defects as the full reviewer, and the token total per run is lower.
