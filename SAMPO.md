steer: RENAME: Foreman becomes Sampo. Start now, as the top priority (NOW:):
1. Finish the in-flight task and checkpoint the Genesis tower at a clean point: no open lane, and no exam or session
   arm running.
2. Do the rename.
3. Resume the tower, and the per-generation moonshots, under the new names. The current generation's Missions continue
   where they stopped.

The tower's history, exam runs, lineage and ledgers must survive the migration intact and readable through the new
paths; test that before resuming. Plan it as one L task with a recorded plan and approaches. Record it with fm decide,
and give the rename an automatic check. Independent parts (design directions, docs, site pages) run in parallel lanes.

## The names

| Now | New | Command |
|---|---|---|
| Foreman (the plugin, harness, product) | **Sampo**, the mill that produces by itself | `sampo` |
| the task loop / executor (what "Foreman" does: plan, build, prove) | **Smith** | `sampo smith` where a verb names the role |
| Genesis (prompt tower, `fm genesis`) | **Rune** | `sampo rune` |
| moonshots / moonshot campaign | **Moons** | `sampo moons` |
| the exam (`fm exam`) and the Inspector role | **Louhi** | `sampo louhi` |
| the not-yet ledger (not-yet.md) | **Underworld** | `sampo underworld` |
| the guard (fmguard, guard categories) | **Ward** | `sampo ward` |

The myth they come from: Ilmarinen the smith forged the Sampo; Väinämöinen sang runes that made things; Louhi set
impossible tasks; the stolen sun and moon were forged anew; lost words were fetched back from the underworld. Use it
once, on the site and in the README, as one short paragraph explaining the names. Nowhere else.

## Scope: everything that names Foreman

- **CLI.** `sampo` is the command. `fm` stays as a compatibility alias that works exactly as before and prints one
  deprecation line a day, kept for at least two releases. Verbs keep their meaning; only the renamed ones above change,
  each keeping its old spelling as an alias (fm genesis → sampo rune, fm exam → sampo louhi, and so on).
- **Plugin.** plugin.json, marketplace.json and the plugin and marketplace ids (foreman@foreman becomes sampo@sampo);
  slash commands and skills (/foreman:next → /sampo:next, and so on); agents (foreman:fm-builder → sampo:builder, and so
  on); the output style; the rules file; the CLAUDE.md block markers; the statusline and band text; the foreman-ui mod
  (sampo-ui) and its /fm and /fm-trust commands (old names stay as aliases).
- **Code.** Everything is renamed, internals included: modules, classes, functions, constants, test names, file names
  and folders that say foreman or fm. Do it mechanically with tests green at every step (fm edit / fm sub). Old import
  paths stay as thin shims for two releases so third-party scripts don't break. Environment variables FOREMAN_* become
  SAMPO_*, with the old ones still read. The Foreman-Task commit trailer becomes Sampo-Task, and both are read forever.
- **Paths and state.** ~/.claude/foreman becomes ~/.claude/sampo, and FOREMAN_HOME becomes SAMPO_HOME. Migration runs
  once, on first launch: move (not copy) state, briefs, ledgers, research and the Rune tower, then leave a symlink at
  the old path. It's idempotent, keeps a backup, records its manifest the way install-user does, and is undone by
  `sampo migrate --undo`. A machine that never upgrades keeps working.
- **Installs.** install.sh, uninstall.sh, setup-plugins.sh, fm install-user, fm doctor and fm agents (the Codex, Gemini
  and opencode adapters) all migrate an existing Foreman install in place: wiring, deny rules, the statusline wrapper,
  the ~/.local/bin link. A fresh install is pure Sampo.
- **Docs.** README, MASTER, INSTALL and CHANGELOG get a top entry explaining the rename and the aliases; past entries
  keep their history untouched.
- **Identity, logo and website:** a complete redesign, not a recolor. See "Design" below.
- **Tower records.** Rename going forward. gen-0, past seeds, critiques and lineage stay verbatim as history; gen-0 is
  never edited. The standing intent and the user's steers carry over unchanged in meaning.
- **Tests and evals.** Every test passes with the new names and still passes with the old aliases. Add migration tests:
  upgrade from a real Foreman state, re-run, undo, a half-migrated crash, a sensitive repo.

## Design: ancient forge meets living machine

Direction: Kalevala myth and an ancient northern forge, fused with brass-and-gear steampunk machinery and modern tech.
Think a rune-carved millstone that is also a precision engine: hammered bronze and iron, glowing forge light, carved
runes, turning gears, blueprint linework, terminal-crisp type. It should feel old as myth and precise as code. It must
never be generic fantasy and never generic SaaS.

**Logo.** A brand-new mark built around the Sampo: a mill or millstone that reads as a machine, with runes, gears and
forge light. Deliver:
- the full mark, a simplified icon that survives 16 px, a monochrome version and a wordmark;
- an animated version (the stone turns, runes light in sequence, sparks), plus a still frame;
- variants for the favicon, app icon, the README header, the social share image, the pane/statusline glyph and the
  Desktop app icon.

Draft at least three distinct directions with the directions skill and fm looks, and pick by a cold design review.
The old hard-hat logo is retired everywhere.

**Website.** Rebuild the site in this world, every page:
- the landing page, a page per feature, Rune (the tower, live), Louhi (the exam scorecard), Moons (the catalogue),
  Underworld, Ward, install and docs;
- a hero where the Sampo mill turns and its runes write themselves into the headline;
- scroll-driven scenes: the forge as you read about Smith, runes singing into place for Rune, Louhi's trials for the
  exam, moons being forged for Moons;
- shader backgrounds (forge glow, molten metal, parchment and blueprint, starfield for Moons) from the shader looks and
  fm scene;
- gears and dials as live data: real numbers from the exam, the tower and outcomes, never invented;
- tactile hover and press states, and sound off by default.

**Quality bar (all enforced):**
- Smooth on mid-range hardware, nothing loaded from other hosts, works with no JavaScript.
- Every animation has a reduced-motion still. Light and dark themes. Phone width down to 320 px.
- WCAG AA, keyboard navigable, and passes fm design lint.
- Visual QA by screenshots (fm shot, fm flow, fm critique) at desktop, tablet and phone sizes.

**Consistency.** The same palette, type and motion language carries through the pane and statusline, the fm code TUI
theme, Desktop, README diagrams, the Genesis/Rune page and the share images. Record it as one design system (tokens,
type, motion rules) that all of them read from.

**Proof.** A cold design review on a stronger model scores it against this brief and against the old site: art
direction, coherence, motion and accessibility. It doesn't ship until the review passes, and the review's findings
become fix tasks.

## Order

1. Plan, with a full inventory of every occurrence (`git grep -i foreman`, the state folders, the installed wiring),
   each one classified: rename, alias, or keep as history.
2. Build behind aliases first, so nothing breaks at any point.
3. Migration, with its tests.
4. Rename the visible surfaces.
5. The design system and logo directions, then the chosen logo, then the full website, then every other surface.
   Docs alongside.
6. A full `fm check`, then the lean check (the rename may not grow hook latency or injected context).
7. A cold review on a stronger model that greps for any user-visible "Foreman" left that isn't history or an alias.

## Protected core and outward actions: built, tested, then queued for the user

- The guard, hooks.json, rules/foreman.md, evals/**, BUILD_PROMPT.md and permission settings: build each change in a
  worktree and queue it with `fm ask ID core`.
- Renaming the GitHub repo (chasesunstrom/foreman to chasesunstrom/sampo; GitHub redirects the old URL), the Pages URL,
  the marketplace listing, and the Foreman Desktop repo and app (Sampo Desktop): prepare each change ready to apply, and
  list them in the final report. Never apply them unasked.
- Nothing a user already has may break. Every old command, path, plugin id, env var and trailer keeps working through
  aliases or the migration.

## Done when

- `sampo` and every renamed verb work, and every old name still works with a deprecation line.
- A real Foreman install upgrades in place, and `sampo migrate --undo` restores it exactly.
- No user-visible "Foreman" is left outside history and aliases (the cold review confirms).
- Full gates are green and docs are updated.
- The new logo and the animated site are live in the new design system across every surface, and the cold design
  review has passed.
- The outward steps are listed for the user.
