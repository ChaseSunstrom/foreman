# Brainstorm — lens: unspoken needs

- **Route stages to installed skills from a capability table** — FEATURE — value 5 — effort M — risk low — category: plugin-compat
  Why: the user's first ask was "better compat with plugins/skills". Pack: `fm next` names only Foreman files; a SECURITY task never surfaces `/security-review`, CLEAN never `/ponytail-audit`, UI never frontend-design. MASTER.md §7 is a static table nothing reads at runtime. Build the table from `fmplugins` find/check, keyed by type+stage, and have `next_action` append one named skill when installed.
  Done when: with security-review installed, `fm next` on a SECURITY task in the audit stage names `/security-review`; with it absent, the line is unchanged.

- **Probe third-party skills for conflicts by behavior, not name** — FIX — value 3 — effort M — risk med — category: plugin-compat
  Why: KNOWN_CONFLICTS is a hand-kept name dict, and superpowers/ECC were found by hand. assumption: new plugins keep appearing. Scan installed skill/hook descriptions for orchestrator signals (Stop hooks, "before any edit", task-tracking claims) and flag overlap with FOREMAN_OWNS.
  Done when: `fm plugins check` on a fixture plugin with a Stop hook and a "plan before coding" skill reports it as a likely conflict though its name is unlisted.

- **Mine skill-call outcomes into a per-stage skill scorecard** — FEATURE — value 3 — effort M — risk low — category: plugin-compat
  Why: routing (idea 1) is guesswork without feedback. fmcost already scans transcripts; count which skills ran in which stage and whether the task's audits later found issues or the user corrected. Demote routed hints that never help.
  Done when: `fm plugins score` lists each routed skill with runs, cost and a keep/drop verdict from a fixture transcript.

- **Make brainstorm lenses derive from the user's pushback clusters** — FEATURE — value 4 — effort S — risk low — category: brainstorming
  Why: the last probe was DRY (1 of 40 survived) and lens yield is tracked, but lenses are still fixed. The user's steers (panels, duplicated dashboard, unpanelled rows) form clear clusters. Generate one lens per cluster, e.g. "everything that looks off in UI", so rounds target live pain, not generic categories.
  Done when: `fm ideas` with a fixture of corrections emits a lens named for the dominant cluster and its pack includes those corrections.

- **Stop a brainstorm early when the first round is mostly dupes** — PERFORMANCE — value 4 — effort S — risk low — category: brainstorming
  Why: the usage-sensitive user paid for 40 titles to learn that the space was dry. With ~400 prior ideas, round 1 dupe rate predicts rounds 2+. Skip remaining rounds and say "dry" if over 70% match `--seen` by title words.
  Done when: a run whose round 1 has ≥70% seen titles ends with no round 2 and prints one "dry" line.

- **Add `fm ground-ideas` to auto-prefilter ideas against code and done work** — FEATURE — value 4 — effort M — risk med — category: brainstorming
  Why: the main thread grounds every idea manually, and most die (already done, premise false). Mechanically grep each idea's named mechanism (commands, files, flags) and mark "exists" or "missing" before the model reads the list.
  Done when: on the 2026-10-03 fixture, ideas naming existing commands (e.g. `fm replay`) are tagged "exists" with the file:line.

- **Give "background wait" a first-class drive state** — FIX — value 4 — effort M — risk med — category: drive
  Why: friction shows 21× the drive ended a turn to wait on background work and 5× for mod reload. The user wants the queue finished unattended. Register waits (pid, file, or task notification) so the Stop hook returns "waiting on X" instead of ending the turn or releasing the drive.
  Done when: a drive with a registered background job takes no stop-hook handback until the job finishes, proven by a replayed hook trace.

- **Keep a "user preferences as checks" file the intake reads for every plan** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: standing preferences (no commands to the user, quiet output, one reviewer pass) live in memory prose. A plan-time lint comparing steps against them (e.g. "step says 'run X yourself'") would catch violations before the user does.
  Done when: a plan containing "please run" fails the plan lint naming the preference.

- **Wild: Let Foreman adopt a skill it finds useful by writing a thin wrapper** — FEATURE — value 3 — effort L — risk high — category: plugin-compat
  Why: wild. When a third-party skill is good but overlaps Foreman's loop, generate a Foreman-owned stub that calls it at the right stage with the loop's guarantees (evidence, audit) around it, behind one `plugin`-category yes.
  Done when: after one yes, the wrapper exists and its stage routes to the third-party skill with evidence recorded.

- **Wild: Let a "skeptic of the queue" propose cutting tasks before the drive starts** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: wild. With the queue unattended and usage-sensitive, a cheap Haiku pass over queued briefs could flag the ones with low value, duplicates or false premises, which is what grounding discovered (39 of 40 ideas dead).
  Done when: `fm run` prints a one-line "N briefs flagged to skip" with reasons before starting, and flagged briefs wait for one yes.

- **Wild: Publish Foreman's integrations as a self-describing manifest other plugins can opt into** — FEATURE — value 2 — effort M — risk low — category: plugin-compat
  Why: wild. Today Foreman guesses what others do. A small `foreman.json` convention (stage, evidence command, conflicts) read by `fmplugins` lets any plugin declare where it fits.
  Done when: a fixture plugin with `foreman.json` declaring stage CLEAN appears in `fm next` routing without a table edit.
