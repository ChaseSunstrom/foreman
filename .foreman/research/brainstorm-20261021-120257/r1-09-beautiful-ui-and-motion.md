# Brainstorm — lens: beautiful UI and motion

- **Draw the run as its named cookbook pattern** — FEATURE — value 4 — effort M — risk low — category: run view
  Why: the pack lists cookbook patterns (evaluator-optimizer, orchestrator-workers, plan-big-execute-small) as things to integrate, but nothing shows which one a run is following. Assumption: run events already carry plan, step and check phases.
  Done when: a recorded run renders a labelled loop diagram in which the active edge pulses and the retry loop's count ticks up, and a golden-frame test covers all three patterns.

- **Open a marketplace shelf for all six repos** — FEATURE — value 5 — effort L — risk med — category: marketplace
  Why: the user wants the six repos integrated "automatically". Skills, plugins-official (166+ plugins, sha-pinned) and financial-services all ship marketplace.json. Assumption: stdlib can parse them; fetching needs a network setting.
  Done when: `fm code` → Shelf lists entries from a fixture marketplace.json grouped by category, with source kind, pinned-sha chip and licence glyph. Moving to a card opens a capability card of hooks, commands, MCP servers and scripts, with a guard verdict, in under 100 ms.

- **Unpack plugins on a quarantine stage before trust** — SECURITY — value 5 — effort M — risk low — category: install flow
  Why: the constraint is "third-party skills and plugins run nothing unguarded". Install should read as a visible review, not a hidden copy.
  Done when: installing a fixture plugin animates its files fanning into a tree. Each file gets a guard stamp, and an executable script gets an amber hold. The sequence ends in a receipt, and no file is written to the live plugin dir until the user presses accept.

- **Show a context loadout screen for skills** — FEATURE — value 4 — effort M — risk low — category: skills
  Why: skills cost about 100 tokens of metadata each and under 5k when activated (pack data). Users have no view of that budget. Assumption: a token estimate per skill can be computed from file size.
  Done when: the Loadout screen shows each skill as a slot with a stacked bar (metadata vs body). The total bar eases as skills are toggled, and a skill activated during a run lights up with a glow that fades over 600 ms.

- **Give every imported asset a licence and provenance glyph** — FEATURE — value 3 — effort S — risk low — category: marketplace
  Why: the pack notes mixed licences. docx/pdf/pptx/xlsx are source-available, the tutorial has no stated licence, and about half the official marketplace is third-party. Colour must not be the only signal.
  Done when: every shelf and loadout row shows one of four distinct shapes (open, source-available, unknown, first-party). A lint test fails if any row relies on colour alone.

- **Render the upstream feed as a changelog stream with a pulse** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: `fm scout` already watches Claude Code releases. The repos need a calm view of sha drift, renames, new plugins and licence changes. Assumption: the feed refresh is rate-limited.
  Done when: a fixture update produces a new row that pulses once, then settles. Drifted pins show a before/after sha diff, and an unchanged feed produces zero redraws.

- **Draw a hook pipeline rail with travelling signals** (wild) — FEATURE — value 4 — effort M — risk low — category: guard viz
  Why: the pack's Claude Code hook features (defer, if, onFailure) and Foreman's guard are invisible to the user. Third-party plugin hooks should be visibly different from first-party ones.
  Done when: a replayed tool call travels PreToolUse → PostToolUse as a dot along a rail. A denied call stops at the guard node with a short bounce and a reason line, and the third-party node uses a different glyph. A golden frame covers the denial.

- **Map skill trigger overlap as a constellation** (wild) — FEATURE — value 3 — effort M — risk low — category: skills
  Why: with 19 skills from anthropics plus 73 of Foreman's own, description overlap means collisions. The user can't see them as text.
  Done when: skills are placed by description similarity (a stdlib token-overlap measure), and pairs above a threshold are joined by a glowing edge. Selecting a pair shows the overlapping phrases, and the layout is deterministic for a given fixture.

- **Show the feature-parity wall as a tile grid** — FEATURE — value 4 — effort M — risk low — category: roadmap
  Why: the request asks for "10x better, modelled on the Claude Code repo". CHANGELOG items can become tiles that fill as `fm code` gains them. Assumption: a feature manifest maps each tile to a check that runs.
  Done when: each tile has three states (missing, partial, proven), and a tile turns solid only when its linked check passes. The header shows the percentage and eases when it changes.

- **Draw the runner wiring diagram with a preflight pulse** — FEATURE — value 4 — effort M — risk low — category: setup
  Why: runners come from models.json, code.toml and detected CLIs, and the planned preflight lamps are not built. "Work with anything" needs a picture of what is connected.
  Done when: runners appear as nodes wired to the default. Preflight sends a pulse down each wire, and a broken one turns red with its cause, such as "CLI not on PATH". Rendering needs no network.

- **Tint the request box by prompt-craft** — FEATURE — value 3 — effort M — risk med — category: request box
  Why: the tutorial repo is ideas-only (no licence) and teaches clear and direct requests, XML data vs instructions, and allowing "unknown". Teaching in place beats a lesson screen. Assumption: heuristics, no model call.
  Done when: file paths, pasted data and vague verbs get distinct tints as the user types. A hint line appears only when the request has no checkable outcome, and it stays silent otherwise.

- **Replace the home screen with a project deck that morphs into the run** (wild) — FEATURE — value 4 — effort L — risk med — category: home
  Why: the home view ranks projects, and the user asked for "full management" from one app. A card that expands into its run keeps spatial context. Assumption: a frame clock exists from the earlier motion work.
  Done when: pressing Enter on a card plays a 300 ms expand into the run view. Esc plays it in reverse, reduced-motion swaps in a cut, and a snapshot test captures the first, middle and last frames.

- **Adopt a vertical pack as a themed workspace skin** (wild) — FEATURE — value 3 — effort L — risk high — category: domain packs
  Why: financial-services ships 7 verticals of agents, commands and connectors. A finance pack could bring its own vocabulary and panels, which suits "work with anything". Assumption: packs can declare a small skin file without running code.
  Done when: a fixture pack with a skin file changes the accent, the panel titles and one summary widget. Removing the pack restores the default exactly, and no pack code runs to render it.
