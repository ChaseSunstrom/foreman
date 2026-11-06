# Brainstorm — lens: brainstorm and ideation quality

- **Route each stage to the installed skill that fits it** — FEATURE — value 5 — effort M — risk low — category: plugin compat
  Why: `next_action` names only Foreman's own procedure files. A SECURITY task never surfaces `/security-review`, CLEAN never surfaces `/ponytail-audit`, and UI never surfaces frontend-design. The MASTER.md §7 table is prose that nothing reads. Build a small capability index from enabled plugins' skill descriptions, which `fmplugins` already parses for cost, and map stage and type to skill, emitting one line.
  Done when: with security-review installed, `fm next` on a SECURITY task names it. With it disabled, the line is absent.

- **Import third-party review findings as audit evidence** — FEATURE — value 4 — effort M — risk med — category: plugin compat
  Why: Code-review is listed for FINAL VERIFY, but the audit gate demands a `fm-reviewer` pass anyway, so the user pays twice. Let a code-review or security-review result, captured as tool output, satisfy the matching audit lens. Mark it by provenance so it never satisfies the intent lens.
  Done when: a task whose diff was reviewed by `/security-review` passes the security lens at done with no `fm-reviewer` spawn, and `fm cost` shows no extra call.

- **Pre-ground ideas mechanically before the main thread reads them** — PERFORMANCE — value 5 — effort M — risk low — category: brainstorm
  Why: The last probe lost 39 of 40 titles at grounding (already done, false premise, or low value). A `--ground` pass can extract backticked identifiers and command names from each idea. It greps for them in `lib/` and `fm help`, and tags each idea `exists`, `missing` or `unverifiable`, so the model only reads the survivors.
  Done when: replaying the 2026-10-03 probe flags the "already done" ideas by name without any model call.

- **Skip a brainstorm run when the evidence hasn't changed** — PERFORMANCE — value 4 — effort S — risk low — category: brainstorm
  Why: About 15 runs happened, the last was DRY, and each run costs parallel `claude -p` children. Hash the new inputs since the last run (commits, friction rows, user corrections). If the delta is below a threshold, `fm ideas` prints "dry, nothing new since <date>" and spawns zero children, unless `--force`.
  Done when: two back-to-back `fm ideas` runs spawn children only the first time.

- **Generate lenses from friction clusters, not a fixed list** — FEATURE — value 4 — effort M — risk low — category: brainstorm
  Why: Lenses are static, while `fm friction` already knows the real hotspots (21× drive stalls on background work, 5× mod reloads). Make the top clusters into lenses ("remove this stall") whose pack contains only that cluster's raw rows. Ideas then arrive anchored to evidence.
  Done when: `fm ideas --lens auto` produces lenses named after the current top-3 friction categories.

- **Record why each idea died and feed reason codes back to children** — FEATURE — value 4 — effort S — risk low — category: brainstorm
  Why: There are 350+ idea titles in the "so far" list, but no reason a title died. Store one of `done`, `false-premise`, `low-value` or `duplicate` per rejected idea. Include the top reasons plus 3 examples in the pack, instead of the full title list.
  Done when: a new pack's "don't repeat" section shrinks, and `ideas.md` shows a reason column.

- **Generate the integrations table from fmplugins and re-map on plugin change** — CLEAN — value 3 — effort S — risk low — category: plugin compat
  Why: The §7 table is hand-written, and `FOREMAN_OWNS` and `KNOWN_CONFLICTS` are separate hand-kept dicts. A new or updated plugin silently falls out of date. Compute a fingerprint of installed plugin versions at SessionStart. If it changed, run `check` once and note only the diff.
  Done when: installing a plugin that conflicts with an owned area produces a one-line note at the next SessionStart and nothing after.

- **Wild: Run a skill duel to retire duplicates** — FEATURE — value 3 — effort L — risk med — category: plugin compat
  Why: Foreman's `fm-reviewer` overlaps with code-review, simplify and ponytail. Run both on the same recorded diff in a temp worktree and compare the findings that survive grounding. Keep the cheaper one per lens, and the user decides with one yes or no.
  Done when: `fm duel review` prints per-tool catch counts and token cost for a fixed fixture diff.

- **Wild: Draft a new skill from repeated manual work** — FEATURE — value 3 — effort M — risk med — category: self-extension
  Why: `fmrepeats` already finds repeated manual work, but it stops at reporting. Turn a repeated sequence into a skill draft in a worktree, eval-gated. Installing it needs the `plugin`-category yes.
  Done when: a seeded repeating command sequence yields a draft skill that passes `claude plugin eval` in the worktree.

- **Wild: Let ideas be falsifiable bets** — FEATURE — value 3 — effort M — risk low — category: brainstorm
  Why: Slates get accepted and then nobody learns whether they helped. Each accepted idea carries one metric and a check-after-N-tasks date. A later `fm friction` pass re-measures it, and a failed bet is retired and counted against its lens.
  Done when: a slate item shows its bet, and 10 tasks later `fm ideas --review` reports hit or miss with the number.

- **Wild: Make a scout fleet that grounds ideas with read-only tools** — PERFORMANCE — value 3 — effort L — risk med — category: brainstorm
  Why: Children are tool-less, so grounding falls to the expensive main thread. After mechanical pre-grounding, hand the `unverifiable` ideas to cheap `fm-scout` (Haiku) runs that return one verdict line each. The main thread then sees only ideas that survive the scouts.
  Done when: for a 40-idea batch, main-thread tokens spent on grounding drop measurably, as shown by `fm cost`.
