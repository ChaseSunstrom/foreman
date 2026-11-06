# Brainstorm — lens: blind spots

Most immune mechanisms are already in "Ideas so far", so I stayed with the blind-spot lens. Answering one earlier question: the learner never tested with poisoned input is the user model (`fmforesight`). T-2554 shows it was already fed Foreman's own test captures, which is the poisoned-input case.

The ideas below come from asking the question behind each missed ask (T-2533 to T-2554) of the whole project. In that list the question was roughly "what does Foreman produce or believe that nothing outside it checks?"

- **Verify landed edits survive until ship** — FEATURE — value 4 — effort M — risk low — category: integrity
  Why: Cursor's top complaint was silent edit reversion (cloud sync racing local saves, format-on-save). Assumption: Foreman never re-hashes files it changed after the write.
  Done when: a test reverts a file after `fm task finish`, and `fm ship` names the lost path and refuses.

- **Lint agent instruction files for drift** — FEATURE — value 3 — effort S — risk low — category: cross-tool
  Why: the frontier names stale, divergent CLAUDE.md, AGENTS.md and Cursor rules as a pain point. Assumption: nothing diffs them against each other or against the code.
  Done when: a fixture where AGENTS.md cites a verb that no longer exists, and disagrees with CLAUDE.md on a rule, yields two named findings.

- **Flag conflicts between filed ideas before filing** — CLEAN — value 3 — effort M — risk low — category: intake
  Why: the catalog holds opposing items ("add a verb" vs "pay with a deletion", "delete the grid" vs "fill 58 cells"). Existing checks cover steer collisions and already-built, not idea against idea.
  Done when: filing a task that reverses a queued one prints the pair and the reason.

- **Reject accepted-but-ignored flags** — FIX — value 3 — effort M — risk low — category: CLI
  Why: the steers over `--by harness` and `fm next --last` show flag belief drifting from the parser. Assumption: some flags are parsed yet never change output.
  Done when: a test walks the argparse tree and fails on any flag whose presence leaves output byte-identical on a fixture.

- **Merge ledgers across the user's machines** — FIX — value 3 — effort M — risk med — category: devices
  Why: the pack's ideas assume a second machine (unpushed work, shared signatures), but nothing says the append-only ledgers union cleanly. Assumption: they conflict on sync.
  Done when: two diverged state dirs merge to the union with no duplicate bets and with per-machine ids.

- **Run opt-in multi-lens audit with clonal weights** — FEATURE — value 4 — effort M — risk med — category: review
  Why: the frontier shows parallel fresh-context review is the demanded fit, and it conflicts with the one-pass token rule. Immune twist (affinity maturation): a lens that found a confirmed defect gets more budget next time, and a silent lens shrinks.
  Done when: after five audits over seeded defects, lens budgets shift measurably toward the lenses that found them, and the default stays one pass.

- **Export a redacted support bundle** — FEATURE — value 3 — effort S — risk low — category: docs/support
  Why: with agent use at 59% and trust low, newcomers will report bugs. Assumption: there is no safe way to share Foreman's state. `fm doctor --bundle` writes a local file with secrets and paths stripped, and the user reviews it before anything leaves.
  Done when: a planted fake token and home path are absent from the bundle, and nothing is sent anywhere.

- **Print "what changed since your last session" after an upgrade** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the lean ratchet knows verb counts and injection sizes per generation, but the user gets no diff of them. Assumption: upgrades are silent.
  Done when: after bumping a fixture version, the next SessionStart prints at most five lines on added and removed verbs, hooks and injected chars.

- **Show a label on every adoption gauge for what it excludes** — FIX — value 3 — effort S — risk low — category: trust
  Why: 75% distrust AI answers. The same question from T-2554 (what feeds the number?) applies to every gauge. Mostly covered, so this is second-order: the label must name the excluded inputs by count.
  Done when: each gauge line in `fm doctor` ends with "excludes N (kinds)".

- **Hold an uninstall rehearsal (wild)** — FEATURE — value 4 — effort M — risk low — category: churn
  Why: wild. A stub user whose only goal is to remove Foreman fast narrates each annoyance that would make them do it. This is the inverse of the first-hour walkthrough. Assumption: no one measures reasons to leave.
  Done when: the run emits a ranked list of at least three annoyances, each tied to a hook note, prompt or latency.

- **Map negative space locally (wild)** — FEATURE — value 4 — effort M — risk low — category: brainstorm
  Why: wild. The catalog is about 2,000 lines and the real misses were 8. Embed all ideas on this machine with no network, cluster them, and name the sparse regions. A blind child then writes asks for each empty region.
  Done when: a planted missing class in a fixture catalog is named as an empty region.

- **Add a placebo lens (wild)** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: wild. One lens is fed random topic words. If its filed-and-kept rate matches the real lenses, the lens ledger and "Score each brainstorm by the asks it missed" are measuring noise.
  Done when: the next generation report shows the placebo's kept rate beside every real lens.

- **Seal each lens's prediction and settle it at 30 days** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: the user model forecasts asks, but brainstorm lenses do not forecast which of their ideas will be asked for. Settling that through the existing Brier machinery gives every lens a score.
  Done when: `fm outcomes` shows a Brier score per lens after 20 settled ideas.

Next question: which of Foreman's outputs does the user act on without checking it against anything outside Foreman, and what would a one-line external check cost?
Next question: what does the user do in the first hour after something Foreman did goes wrong, and which of those steps have no verb?
