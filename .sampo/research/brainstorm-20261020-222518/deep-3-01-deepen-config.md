# Brainstorm — lens: deepen: config

- **Resolve one config object, then print it as a receipt** — FEATURE — value 5 — effort M — risk low — category: config core
  Why: the runner, worker, model, theme, motion and guard settings are read at separate call sites (the dropped `models.json` helper note shows two resolvers already); the nixie run "isn't doing anything" because no one could see which runner or planner was chosen. Builds on layered config, provenance and the single resolved object ideas, as one `Resolved` that every surface (CLI, TUI, home) consumes.
  Done when: `fm code config show --json` prints every effective value with its source layer (default/global/project/env/flag), and a test fails if any module reads `models.json` or a setting except through it.

- **Show the resolved plan before the first token** — FEATURE — value 5 — effort S — risk low — category: setup UX
  Why: the user's stalled nixie run gave no hint of what was launching (claude planner, 66k–133k tokens per call). One line at start: runner, where it came from, context loaded, expected cost, timeout.
  Done when: `fm code "x"` prints a "using claude (auto-detected, no config) · plugins off · cap 5m" line within 1 s, and the TUI shows the same in its header.

- **Make config self-diagnosing with `fm code doctor`** — FEATURE — value 5 — effort M — risk low — category: doctor
  Why: the user hit `fm` not on PATH, no model set, and a nested Claude loading Foreman's own hooks; each was found by hand. Doctor checks PATH, each CLI's version and login, endpoint reachability, the models.json schema, duplicate Foreman (plugin and CLI both active), and offers a fix per finding.
  Done when: with a seeded broken HOME (no PATH link, bad JSON, duplicate hooks) doctor reports each with a one-line fix, and `--fix` repairs them on a copy.

- **Probe every runner for real and cache a capability card** — FEATURE — value 4 — effort M — risk med — category: runners
  Why: "manage ANY CLI/model" needs known capabilities (streams JSON? plan mode? context size? tool use?), and `fm code bench` already grades models. A one-time probe records latency, tokens per call, stream support and a pass or fail on a seeded task; the default is picked on evidence, not order.
  Done when: `fm code runners --probe` writes a card per runner and `fm code` with no config picks the best one, with the reason shown by `config explain`.

- **Keep project config in the repo, and trust it deliberately** — SECURITY — value 4 — effort M — risk med — category: project config
  Why: multi-project is the ask; per-project `.foreman/code.toml` should travel with the repo. A repo-supplied `CMD {prompt}` worker template is a command-execution vector, so project config can't add commands until the user approves its hash.
  Done when: a cloned repo whose config adds a worker template is refused, with `fm code trust` showing the diff; changing the file revokes the trust; the guard tests are unchanged.

- **Detect duplicate Foreman and say who wins** — FIX — value 4 — effort S — risk low — category: plugin conflict
  Why: the explicit request "no duplicate Foreman when it runs Claude Code as a worker". Beyond T-1327's nested-session rule, config should record the "who is the Foreman here" decision (the CLI harness vs. the plugin hooks) and detect both active in any session.
  Done when: a worker session started by fm code shows exactly one Foreman's hooks in its settings dump, and `config explain foreman.mode` names the reason.

- **Write config as typed schema with migration and last-good fallback** — CLEAN — value 4 — effort M — risk low — category: config core
  Why: merges the atomic-write, schema-version and last-good ideas. Corrupt JSON after a crash must not stop `fm code` from opening.
  Done when: truncating `models.json` mid-write makes `fm code` load the last-good copy, warn once, and a v1 file migrates to v2 with a backup.

- **Edit config inside the TUI with live preview** — FEATURE — value 4 — effort M — risk low — category: TUI settings
  Why: the user dislikes text walls; a typed settings screen (picker for runner, theme gallery, motion slider, timeouts) writes through the resolved-config layer and shows the effect at once. Pairs with T-1311's theme gallery.
  Done when: changing the theme in the settings screen alters the frame the next tick and `config show` reflects it with source "tui".

- **Wild: Say "make it faster and cheaper" and get a config diff** — FEATURE — value 4 — effort M — risk med — category: plain-words config
  Why: wild. Combines plain-word settings with bench evidence: the model proposes a diff against the real schema (the model fills only a checked JSON slot, the harness's own style), shows the predicted effect from past run stats, and applies it only on confirmation.
  Done when: the request yields a schema-valid diff with the evidence cited, an invalid key is rejected by the validator, and nothing is written without a yes.

- **Wild: Offer a config time machine tied to run results** — FEATURE — value 3 — effort M — risk low — category: history
  Why: wild. Every run's receipt stores a config hash, and the snapshots are in a log. When runs start failing or costing more, `fm code config blame` bisects which change did it, and `config undo` restores it.
  Done when: after changing the runner between two seeded runs, `config blame` names that change as the first bad one and `undo` restores the previous file byte for byte.

- **Wild: Retire settings that never matter** — CLEAN — value 2 — effort S — risk low — category: config hygiene
  Why: wild; a sunset test per setting. Record which settings were ever set away from the default and used; after N releases unused ones are flagged for removal, which keeps config small.
  Done when: `config audit` lists settings with zero non-default uses across the recorded runs, and a deprecated key still loads with a warning.

- **Make the stall watchdog a config policy, not a hope** — FIX — value 5 — effort S — risk low — category: reliability
  Why: the nixie run sat silent for minutes. Per-runner `quiet_after`/`give_up_after` settings, defaulting from the probe card, trigger a visible heartbeat, then an offer to switch runner or stop and kill the whole process group.
  Done when: a fake CLI that prints nothing triggers the "quiet 30 s" cue, then the abort at the limit, and no child survives.

- **Notice friction and open the config fix by itself** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: the user wants Foreman to figure it out unasked. Phrases such as "isn't doing anything" or "why can't I" plus a stalled run or a missing runner create a captured task with the run's resolved config attached, so the brainstorm starts from facts.
  Done when: a seeded transcript with that phrase and a stalled run creates exactly one task containing the config receipt, with no duplicate on a repeat.
