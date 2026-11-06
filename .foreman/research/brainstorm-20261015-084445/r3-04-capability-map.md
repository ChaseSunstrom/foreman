# Brainstorm — lens: capability map

These are second-order and combination ideas built on the new evidence (A–D). The pile above is large, so several ideas deliberately fuse or extend existing entries rather than add a new verb.

- **Build one seeded-bug fixture kit for every showcase surface** — FEATURE — value 5 — effort M — risk low — category: onboarding
  Why: The pile proposes `fm demo`, `fm tour`, a stranger test, a bench seed, a cold-user docs test and a clean-HOME gate. Each would otherwise build its own toy repo. Evidence: the bench has 1 case and the README has no demo (A1, C).
  Done when: `plugin/tests/fixtures/kit/` holds at least 5 seeded-bug repos (one per common stack), each with a known-good fix patch and its expected evidence. `fm demo`, the newcomer gate and `fm bench` all load from it, and a test fails if any of the three stops using it.

- **Track install-day milestones and nudge the next missing one once** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: A newcomer hits dead ends at `fm init`, `capture`, `task new` and `done` (A5, A6, A9). Nothing tells them which step comes next. The milestones are first capture, first task, first `finish`, first green doctor. Each is derivable from existing ledger rows.
  Done when: In a clean HOME, `fm status` shows one line, "next: <milestone>", until the milestone is hit. Each nudge prints at most once, and the line disappears after the fourth milestone.

- **Add `fm doctor --publish`, a marketplace-readiness lint** — FEATURE — value 3 — effort S — risk low — category: distribution
  Why: Rivals install through the Anthropic marketplace or npx, and Foreman lacks that path (B). A lint covering manifest fields, no `~/.claude` writes at install, and hook and skill frontmatter validity would make that path attainable.
  Done when: The command exits non-zero with a per-rule fix line on a deliberately broken manifest fixture, and exits 0 on the shipped plugin.

- **Keep rival task files and the Foreman queue in sync in both directions** — FEATURE — value 3 — effort M — risk med — category: interop
  Why: Task Master, CCPM and spec-kit users already have `.taskmaster/` or `specs/` trees. The pile has one-shot import but no continuous coexistence, so assumption: users try Foreman beside a rival before switching.
  Done when: Editing `.taskmaster/tasks.json` in a fixture repo updates the matching Foreman task on the next hook turn. A Foreman `finish` writes the status back, and a conflicting edit on both sides is reported instead of overwritten.

- **Print a "ceremony tax" line comparing a Foreman task with a bare-Claude baseline** — FEATURE — value 4 — effort M — risk med — category: proof of value
  Why: There is no published evidence Foreman helps (C). Fixture-kit tasks can be timed with and without Foreman. That gives a per-stack, reproducible number (turns, tokens, held or not) without needing users' data.
  Done when: `fm bench --vs bare` runs the fixture kit twice (Foreman on and off, stub model in CI) and writes one table with turns, tokens and verified-fix rate per case.

- **Show the effect of each install change before applying it** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: The default install enables bypass, a statusline wrapper, 20 deny rules and autocompact 70%, and says only "confirm once" (A2). A dry-run could show, for each change, what behaviour it alters and which doctor probe verifies it.
  Done when: `install.sh --plan` prints one row per `~/.claude` change in the form "setting → why → how to undo", and writes nothing. `--apply` records the same rows in an uninstall manifest.

- **Wild: Make the README a self-verifying transcript** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: assumption: a recorded real run on the first screen persuades more than prose (A1). If the transcript is generated from the fixture kit, it cannot drift from the product.
  Done when: A release script regenerates the README's first-screen block from a real fixture-kit run. A test fails when the block differs from fresh output.

- **Wild: Give each repo a "Foreman scar map" built from its own fixed-later tasks** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: 18 of 688 tasks were fixed later (C). Tagging the files and gates involved gives a per-repo weak-spot map. It can raise audit lenses on those paths and also seed bench cases.
  Done when: After 3 fixed-later tasks touching `src/a.py`, the next task editing it gets one extra audit lens. The scar-map file lists each entry with its source task id.

- **Wild: Add `fm wager`, a one-line prediction logged before any task and scored at close** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: Rival comparisons hinge on trust. A cheap, user-visible track record ("you predicted S, it was M; 7 of 10 right") builds trust with newcomers and gives the grading of folded tasks real labels (C).
  Done when: `fm wager "S, 20 min"` stores the guess. `task finish` prints the actual tier and time, and `fm digest` shows the running hit rate.

- **Merge `fm digest`, `fm stats` and `fm cost` into one per-week view that credits folded tasks to their parent** — CLEAN — value 4 — effort M — risk low — category: simplification
  Why: 159 of this week's 370 done tasks show as "ungraded" because they were folded into others (C). The fmcost grab-bag is a named over-engineering cluster (D). One view with parent-credited grades fixes both without deleting a feature.
  Done when: `fm digest --week` shows zero "ungraded" rows for folded tasks. The old verbs forward to it with a one-line notice, and a test asserts the parent-credit rule.
