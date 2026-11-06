# Brainstorm — lens: deepen: plugin compat

- **Add a stage-hint line to `fm next` from a cached capability index** — FEATURE — value 5 — effort M — risk low — category: plugin routing
  Why: `next_action` names only Foreman files; a SECURITY task never surfaces `/security-review`. Combines the registry and "route each stage" ideas into one zero-extra-token mechanism: `fmplugins` scans installed SKILL.md frontmatter once, writes `capabilities.json` (stage → skill, cost chars), and `next_action` appends one line ("CLEAN: /ponytail-audit available") only when the stage matches.
  Done when: with ponytail installed, `fm next` on a CLEAN-stage task prints a line naming `/ponytail-audit`; with it disabled, the line vanishes; test covers both.

- **Rebuild the capability index on plugin change via a cheap mtime check** — CLEAN — value 4 — effort S — risk low — category: plugin sync
  Why: MASTER.md §7 is a static table that can go stale (ECC, superpowers entries). Generate it from fmplugins output; the SessionStart hook compares installed-plugins mtime to the index and re-maps only on change.
  Done when: enabling a plugin changes the index and `fm doctor` flags a hand-edited §7 that drifts from the generated one.

- **Ingest third-party review findings as audit evidence** — FEATURE — value 4 — effort M — risk med — category: audit import
  Why: the audit lenses use one fm-reviewer pass; code-review/security-review output is discarded after display. Add `fm audit import --lens security FILE|-` that parses severity-tagged findings into the brief's audits section, so `task done` accepts them in place of the reviewer pass for that lens (saves one agent run).
  Done when: a task with an imported security-review report satisfies the security lens gate without spawning fm-reviewer; unparseable input is rejected with a clear message.

- **Let a skill declare itself a lens via a `fm-lens` frontmatter key** — FEATURE — value 3 — effort M — risk med — category: audit lenses
  Why: "installed skills as pluggable audit lenses" extended with an opt-in contract: lens name, how to invoke, and the output shape that `audit import` parses. Without the contract, Foreman never runs unknown skills.
  Done when: a fixture skill with the key appears in `fm audit lenses`, and a task can require it.

- **Warn on always-on cost delta at plugin enable time** — PERFORMANCE — value 4 — effort S — risk low — category: plugin cost
  Why: `fmplugins check` computes always-on tokens (~4 chars/token) but only on demand; ECC cost 41k. Show the delta and the projected weekly burn in the `fm ask` yes/no prompt, so consent is informed for the usage-sensitive user.
  Done when: the install/enable prompt text contains "+N tokens/turn", verified against a fixture plugin.

- **Detect runtime conflicts from hook-collision traces** — FIX — value 3 — effort M — risk med — category: conflict detection
  Why: KNOWN_CONFLICTS is a static dict. `fm friction` already reads hook latency and failed calls; add a detector for two plugins both injecting a Stop or PreToolUse response in the same turn, or duplicate "next step" text in context, and surface it in the digest.
  Done when: a replayed fixture session with two Stop-hook injectors yields a friction entry naming both plugins.

- **Publish `foreman-integration.json` that plugins can target (wild)** — FEATURE — value 3 — effort M — risk low — category: plugin manifest
  Why: assumption: other authors would adopt a contract. Ship a schema declaring stages, evidence format, and the lens output shape that `audit import` and the registry consume; Foreman's own skills validate against it, so the format is tested.
  Done when: `fm plugins validate PATH` passes for Foreman's own plugin and fails for a fixture with a wrong stage name.

- **Run a skill duel to retire duplicate skills (wild)** — FEATURE — value 3 — effort L — risk med — category: skill evaluation
  Why: simplify vs ponytail vs `/clean` playbook overlap. Run both on the same diff in a worktree via `claude -p`, compare findings after grounding, and record a verdict in the capability index (prefer A for CLEAN). Spend is capped at a single user-approved run per pair.
  Done when: `fm plugins duel A B --diff REF` writes a verdict file with finding counts and token cost, and the index records the preferred skill.

- **Auto-port a foreign skill into a trimmed playbook (wild)** — FEATURE — value 2 — effort L — risk med — category: skill import
  Why: assumption: some third-party skills are valuable but verbose. Generate a Foreman playbook from a skill with a cost note and a link to the original, loaded on demand only, never always-on. File creation stays under the guarded `plugin` category.
  Done when: `fm plugins port SKILL` outputs a playbook file with the token delta, and the guard asks for consent before writing it.

- **Learn which routed skills actually helped, and prune the hints** — FEATURE — value 4 — effort M — risk low — category: routing feedback
  Why: hints that get ignored add noise. Record whether a surfaced skill was invoked and whether it produced a finding adopted into evidence; `fm friction` shows hit-rate, and hints below a threshold after N tasks stop appearing (quiet-output preference).
  Done when: after simulated tasks where a hint is never used, that hint disappears from `fm next`, and the friction digest shows its hit-rate.
