# Brainstorm — lens: capability map

- **Add a ⌘K command palette to the web UI that ranks actions by the forecast** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: assumption: none of the 58-cell ideas give the web UI a single entry point. Raycast and Linear set the pattern, with predicted actions (accept, dismiss, file a task, open a cell) listed first.
  Done when: pressing ⌘K on any page lists at least 5 actions, the top one matches the page's pending forecast, and a Playwright run can execute it by keyboard alone.

- **Clip the last failing command or a browser selection into the inbox** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: assumption: intake takes typed text only. Pocket and Raycast clip from the context the user is already in. `fm clip` would take the last N lines of terminal output or the clipboard, and the web UI could offer a bookmarklet. The result is a pre-grounded brief with the "already built?" check run.
  Done when: `fm clip` after a failing command files a capture whose body holds the output, and fm recall's already-built line appears on it.

- **Detect a regime change in the user model** — FEATURE — value 4 — effort M — risk med — category: user model
  Why: assumption: every predictor in the pack learns from history. When the user switches language, stack or project kind, the old habits mislead. The detector spots a shift in dominant file types or verbs, halves forecast confidence for a set window, and says so.
  Done when: replaying a planted history with a mid-way language switch drops hit@3 for at most N asks after the switch, with a "model resetting" line shown.

- **Tag user-model fields with a sharing class that the pack builder enforces** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: this very pack sends the user's verbatim "asked" and "dropped" lines to tool-less children, including two mistaken captures. Each stored line would carry one class: local-only, child-ok or publishable. The pack builder and cold-read charter would refuse local-only lines.
  Done when: a test plants a local-only line, builds a pack and a cold-read prompt, and finds the line in neither.

- **Publish foresight flags as SARIF diagnostics** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: T-0788 defers LSP for blast radius, and "SARIF from fm check" is already planned. Foresight flags (this path often gets reopened, this test is flaky) would reach VS Code, JetBrains and GitHub code scanning with no new UI.
  Done when: `fm foresee --sarif` output validates against the SARIF 2.1 schema and a flag appears on the right file and line in a SARIF viewer.

- **Show "needs N more asks" readiness per predictor** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: abstain-or-fail reporting is already in the ideas, but cold start is not covered. A new repo or machine has no history, so each predictor would declare a minimum evidence floor and `fm doctor` and the web UI would show progress toward it.
  Done when: on an empty-history fixture every predictor reports "not ready: 0/N" rather than silence, and the count moves after N seeded asks.

- **Check Foreman's own upgrade against a copy of the real state first** — FIX — value 4 — effort M — risk low — category: reliability
  Why: T-0418 (installed foreman-ui is stale) and T-2532 (working copy fails to import) show upgrades breaking on real installs. The check copies the state dir, runs the new library's `fm doctor` and the forecaster on it, and refuses the swap on any new error.
  Done when: a planted incompatible state-file change makes the dry-run refuse the update and name the file.

- **Add per-field provenance and an edit log to the user model** — FEATURE — value 3 — effort M — risk low — category: user model
  Why: the pack has ideas for "let the user model forget" and "tag by origin", but nothing records who changed what and when. Each learned habit would carry its source line, its date, and a user-visible undo.
  Done when: `fm me --log` lists every habit with its source line and `fm me --undo ID` restores the previous value.

- **Hold a forecast-versus-baseline scoreboard in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the pack asks for "baseline score", "calibration chart" and "hit rate by kind" in several places, but only as CLI output. One chart page with Brier and hit@3 for each predictor against the "repeat the last request" baseline would make the earned-or-delete judgement visible.
  Done when: the page renders from the ledger, shows a baseline line, and states "no data" for an empty predictor.

- **Wild: warm the model's prompt cache before the user's habitual start** — PERFORMANCE — value 2 — effort M — risk med — category: latency
  Why: assumption: the user starts sessions at repeatable times, and the night tick knows when. A tiny opt-in warm-up call before then would cut first-reply latency and cost. It sends content out, so it stays off unless a setting enables it.
  Done when: with the setting on, first-turn cached-token share rises on a recorded habitual start, and with it off, no call is made.

- **Wild: let a local model write the night's "dream journal" of tomorrow's likely work** — FEATURE — value 3 — effort M — risk low — category: local-first
  Why: assumption: a local engine can read the asked stream and the open queue with nothing sent out. It writes a dated markdown file of at most 5 guesses with reasons, scored the next evening by git outcomes.
  Done when: the file appears after a night tick with no network, and the next tick records hit, miss or expired for each guess.

- **Wild: replay a stranger's repository history as a free anticipation benchmark** — FEATURE — value 3 — effort L — risk low — category: evals
  Why: the pack asks for a planted-history benchmark but builds it by hand. Real open-source issue-to-fix history gives labelled next-asks at scale and avoids authoring bias, in line with the standing rule to use signals Foreman did not author.
  Done when: `fm exam foresight --corpus DIR` prints hit@3 for the forecaster and for the baseline on at least 3 cloned repos.

Next question: Which predictors would still beat "repeat the last request" on a user with under 30 asks, and what does the web UI show them before then?
Next question: Does any Anticipation output leave the machine, in a pack, a child prompt or a site publish, and who checks it?
