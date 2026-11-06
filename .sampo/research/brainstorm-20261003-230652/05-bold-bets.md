# Brainstorm — lens: bold bets

- **Route stages to installed skills via a capability registry** — FEATURE — value 5 — effort M — risk low — category: plugin compat
  Why: `fm next` names only Foreman's own procedures. A SECURITY task never surfaces `/security-review`, CLEAN never surfaces `/ponytail-audit`, UI never surfaces frontend-design. MASTER.md §7 is a static table nothing reads at runtime. Have `fmplugins` scan installed skill descriptions once per plugin-set hash into a `stage → skill` map (seeded from §7, user-overridable), and have `next_action` append one "use X" pointer only when the skill is installed and not conflicting.
  Done when: with ponytail installed, `fm next` on a CLEAN-type task in execute names `/ponytail-audit`; with it removed, the line is absent (test covers both).

- **Treat installed skills as pluggable audit lenses** — FEATURE — value 4 — effort M — risk med — category: plugin compat
  Why: audits use five fixed lenses through one fm-reviewer pass. Third-party reviewers (security-review, code-review, simplify) duplicate that work when run separately. Let a lens declare `via: skill-name`, so the single reviewer pass loads that skill's checklist text instead of Foreman's, and a done-gate accepts its verdict as the lens evidence. Assumption: skill bodies can be read from disk by fm-reviewer.
  Done when: a task with a `security` lens configured to use security-review records that lens as audited by that skill, and `fm task done` accepts it with no second pass.

- **Import foreign skills as Foreman playbooks with a cost note** — FEATURE — value 3 — effort M — risk low — category: plugin compat
  Why: ECC (41k always-on tokens) was disabled, yet its procedures were ported by hand into playbooks. Make that repeatable: `fm plugins absorb <plugin>` extracts on-demand procedure sections into recall-indexed playbook stubs, so the plugin stays disabled and its knowledge is reachable through `fm recall`/`fm next`. Pin the source sha; guard category `plugin` applies.
  Done when: absorbing a fixture plugin makes `fm recall <its topic>` return the stub, and `fm plugins check` reports no added always-on tokens.

- **Auto-detect third-party conflicts at runtime from observed behavior** — FIX — value 3 — effort S — risk low — category: plugin compat
  Why: KNOWN_CONFLICTS is a hand-kept dict. A new plugin that injects its own planning or "must use" hooks goes unnoticed until it causes friction. Scan enabled plugins' hook registrations and skill descriptions for ownership phrases ("always", "before any", "plan", "brainstorm") and warn once in `fm doctor` with the matching FOREMAN_OWNS area.
  Done when: a fixture plugin with a SessionStart "always brainstorm first" hook is flagged by `fm doctor` as a conflict with brainstorming.

- **Make brainstorm lenses learn from grounding outcomes per project** — FEATURE — value 4 — effort M — risk low — category: brainstorming
  Why: the last probe found 1 of 40 survived, and the user's usage sensitivity makes dry runs expensive. Record each idea's grounded verdict (done, false premise, low value, accepted) against its lens and category, and have `fm ideas` refuse to launch when the recent per-lens yield is below a threshold, printing the single cheapest remaining lens, rather than running anyway.
  Done when: after a recorded all-dry history, `fm ideas` exits before spawning children and names the reason.

- **Ground ideas mechanically before the main thread sees them** — PERFORMANCE — value 4 — effort M — risk med — category: brainstorming
  Why: the main thread greps every idea against code, which is the costly step, and most die as "already done". After children return, run a stdlib pass that checks each title's nouns against `fm help` commands, module names, CHANGELOG and the "ideas so far" list, and tags likely duplicates with the matching file or command. Only untagged ideas reach grounding.
  Done when: replaying the 2026-10-03 probe's 40 titles tags at least 30 of the 39 dead ones with a cited match.

- **Add a "stuck" consult that forks to a no-context solver** — FEATURE — value 3 — effort M — risk med — category: problem solving
  Why: three failed attempts blocks with diagnosis, which ends the unattended run. Before blocking, spawn one `claude -p` child with only the brief, the failing command output and the ruled-out list, asked for three structurally different hypotheses. Bounded to one call per step. Assumption: fresh context breaks the fixation that caused the failures.
  Done when: on a seeded failing step, the third failure writes a "consult" section with ≥2 hypotheses to the brief before the block.

- **Wild: Mine installed skills' own failure modes with a skill-vs-Foreman duel** — FEATURE — value 3 — effort L — risk med — category: plugin compat
  Why: wild. For each stage mapping, run a past task's brief once with Foreman's playbook and once with the third-party skill in a worktree, compare gate outcomes and tokens, and keep the cheaper winner as the routing default. Assumption: briefs can be replayed deterministically enough to compare.
  Done when: `fm plugins bench <skill>` writes a table of tokens and gate results for both arms on one past brief.

- **Wild: Let Foreman write new skills from its own repeated recipes** — FEATURE — value 3 — effort M — risk med — category: self-extension
  Why: wild. `fmrepeats` already finds repeated manual work, but creation under ~/.claude is guarded. Draft a skill folder in a staging dir when a pattern recurs three times, run `claude plugin eval` on it, and ask one yes/no to install.
  Done when: a fixture history with three identical sequences produces a staged skill that passes eval and awaits one yes.

- **Wild: Offer a "second project's lessons" lens in brainstorms** — FEATURE — value 2 — effort S — risk low — category: brainstorming
  Why: wild. Per-project recall means a lesson learned in one repo never informs another. Add one lens that gets the other projects' top lessons and asks "which of these would have prevented a failure here?", so cross-pollination costs one child.
  Done when: `fm ideas --lens cross` includes lessons from another project's store in the child pack.

- **Wild: Publish Foreman's integration map as a machine-readable manifest other plugins can target** — FEATURE — value 2 — effort S — risk low — category: plugin compat
  Why: wild. Compatibility is one-sided today. Ship `foreman.integration.json` (stages, evidence formats, lens verdicts) so plugin authors can declare "I fill the SECURITY stage" and `fm plugins check` reads it instead of guessing.
  Done when: a fixture plugin carrying the manifest is routed for its declared stage without a registry entry.
