# Brainstorm — lens: capability map

The pile is close to saturated. Everything below is a gap I couldn't match to an earlier title, or a combination that only works together.

- **Classify path classes once: generated, vendored, frozen, hot** — FEATURE — value 4 — effort M — risk low — category: map hygiene
  Why: assumption: `fm map` already knows layout and tests. The tier-drift and ".claude/ never 'left behind'" fixes show diff noise keeps leaking into close checks. One registry, auto-detected from headers like "DO NOT EDIT" and from lockfiles, would feed scope, blast radius, tier counting and reads. Edits to generated files would be refused with "edit the generator".
  Done when: a hand-edit to a file with a `@generated` header is refused with the generator named, and a 500-line vendored change doesn't move the task's tier.

- **Add a diff-hygiene gate to close** — FEATURE — value 4 — effort S — risk low — category: gates
  Why: assumption: no existing check is a Danger-style diff lint. It would flag a lockfile changed without its manifest, a newly added binary or large file, whitespace/EOL-only churn, mode flips, and files in the diff that no step or criterion names.
  Done when: a fixture diff with a stray 3 MB binary and a manifest-less lockfile bump gets two named warnings at `fm task finish`, and a clean diff gets none.

- **Inspect the built artifact before a release closes** — FEATURE — value 3 — effort M — risk low — category: release
  Why: T-0352 (publish Desktop with CI and release pipelines) is blocked, and the AppImage ships via `--desktop`. Source-level gates never look at what actually ships. The check would list tarball, wheel or AppImage contents against an expected manifest, a size budget and a secret/home-path scan, and optionally build twice and compare hashes.
  Done when: a release dry-run fails when a planted `.env` is in the archive or the size grows over budget, and passes on the clean tree.

- **Make one policy calendar drive everything time-shaped** — FEATURE — value 4 — effort M — risk med — category: policy
  Why: the pile has separate ideas for quiet hours, a calendar-aware autonomy dial, night runs and budget pace. They would be worth more as one schedule object: freeze windows (no push, release or merge Friday afternoon or on holidays), quiet hours, night-run windows and the autonomy level per window. Blocked actions would queue until the window opens.
  Done when: with a Friday freeze set, `git push` and a release are refused with the reopen time, and the queue shows them parked, not failed.

- **Query and save views over the queue** — FEATURE — value 3 — effort S — risk low — category: queue ergonomics
  Why: Taskwarrior and Linear users filter like `tier:M status:deferred age>30d`. The pile has global search but no filter language, and there are 14 backlog zombies and 13 deferred clusters to sweep. The same language would let bulk verbs (`defer`, `drop`, `set`) take a view as their target.
  Done when: `fm q 'status:deferred age>30d'` lists exactly the matching tasks, a saved view reruns by name, and `--json` output is stable.

- **Give every fm verb a documented exit-code and error-class contract** — CLEAN — value 3 — effort S — risk low — category: scripting
  Why: assumption: hooks, the mod, Desktop and consumer scripts parse stderr text. Distinct exit codes for refused, parked, needs-user, stale and internal error would let callers branch without regexes. This pairs with the "JSON surfaces contract test" item already in the pile.
  Done when: a table-driven test asserts each failure class returns its documented code for 10 representative verbs.

- **Show a "needs from you" manifest at plan time** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: the pile covers batching approvals, but not credentials, assets, URLs and access a queued task will need. Collecting those once means tasks park with a named missing input instead of stalling mid-run. The user's repeated "etc. etc. etc." mandates suggest long unattended stretches, where a mid-run stall is expensive.
  Done when: a queue of 3 tasks needing an API key and a design file prints one list before the drive starts, and the task with a missing input is parked, not started.

- **Support a patch-stack mode for forks and patched bundles** — FEATURE — value 3 — effort L — risk med — category: maintenance
  Why: the foreman-ui mod patches a Claude Code bundle, and T-0418 is blocked on updating the installed mod to 0.6.1. A patch-stack task type would track each patch with its intent and a re-apply check, rebase it when upstream moves, and report which patches no longer apply.
  Done when: on a fixture upstream bump, one patch is auto-reapplied and one is reported as conflicting with its recorded intent.

- **Add cross-task evidence reuse with a staleness proof** — PERFORMANCE — value 3 — effort M — risk med — category: gates
  Why: assumption: close-out re-runs checks another task already ran on an unchanged subtree. A tree-hash cache is in the pile, but this is the narrower, safer form: reuse a recorded pass only when every file the command read is byte-identical, otherwise rerun.
  Done when: two sequential tasks touching disjoint files run the shared lint once, and touching one of its inputs forces a rerun.

- **Wild: Gate risky approvals on fatigue signals** — FEATURE — value 3 — effort M — risk med — category: safety
  Why: wild. A rising typo rate in the user's messages, 3 a.m. timestamps and rapid repeated "yes" replies are risk signals. Foreman would require a second confirmation, or defer one-way doors until morning. Nobody asked for this, but it protects the user at the moment `--dangerously-skip` bypass mode is least safe.
  Done when: a replayed fixture of 10 rapid yeses after midnight turns a destructive grant into a "confirm again in the morning" parked ask.

- **Wild: Leave one small task for the user, with a hint ladder** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The pile covers comprehension debt as a map. This turns it into a weekly choice: Foreman picks a small, low-risk task, withholds it from the queue, and offers hints in three escalating levels. It keeps the human's hands in the code and is a conversation piece.
  Done when: `fm sharpen` picks a small task, hides it from the drive, and a hint level reveals only its own text.

- **Wild: Declare amnesty windows for spike weeks** — FEATURE — value 3 — effort M — risk med — category: gates
  Why: wild. The pile has a per-task SPIKE type with a discard guarantee, but not a project-wide time-boxed mode. For a declared week on tagged paths, gates drop to advisory and everything produced is labelled throwaway. At expiry Foreman forces a keep, port or delete decision per file.
  Done when: during amnesty a failing lint doesn't block close but is recorded, and on expiry the unresolved throwaway files appear in one decision list.
