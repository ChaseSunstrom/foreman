# Brainstorm — lens: delight

- **Unbox every adopted skill with a receipt card** — FEATURE — value 4 — effort M — risk low — category: integration delight
  Why: the user wants the six repos integrated "automatically", and anything adopted silently is anxiety-inducing. A card appears on adoption: what it is, source repo and pinned sha, licence badge (open vs source-available), metadata token cost (~100), and a one-key undo. It's added to a "shelf" in the home screen.
  Done when: adopting a fixture skill renders a card showing name, sha, licence and token cost, and pressing the undo key leaves the tree byte-identical.

- **Add a fitting room: try a skill on this run only** — FEATURE — value 5 — effort M — risk med — category: marketplace
  Why: assumption: people won't install 166 plugins blind. When a request matches an uninstalled marketplace skill, a quiet hint says "borrow the pdf skill for this run". It is installed into a lease, runs under the guard, and is removed at close, with a one-line "it helped / it didn't" verdict.
  Done when: a borrowed fixture skill is present during the run, gone afterwards, and the verdict line is written to the run record.

- **Show new arrivals and renames on the home screen** — FEATURE — value 4 — effort S — risk low — category: plugins
  Why: the pack notes claude-plugins-official carries renames and sha pins, and `fm scout` already watches releases. A strip reads "2 new, 1 renamed (your X is now Y)" with a one-key fix that rewrites the installed reference.
  Done when: given a fixture marketplace.json with a rename, the strip appears and the fix key updates the installed entry.

- **Draw each cookbook pattern as a live diagram of the run** — FEATURE — value 4 — effort M — risk low — category: run view
  Why: the cookbooks cover evaluator-optimizer, orchestrator-workers and plan-big-execute-small. A run on one of these shows its topology as a small box-and-arrow figure in which the active node pulses and failed edges go red.
  Done when: a seeded evaluator-optimizer run renders a diagram, and the golden frame shows the node active during its step.

- **Fill a capability bingo card from the six repos** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: the request is "fully featured/implemented", and the 25 claude-code features (agent view, /rewind, worktrees, hooks, fallback models…) are otherwise an invisible checklist. A 5×5 card on the app's home lights each cell when it is supported and has been used once, with a quiet flourish on a completed row.
  Done when: each cell maps to a probe command, and the card reads its state from the probes rather than from a hardcoded list.

- **Show a live spec meter while drafting a skill from a run** — FEATURE — value 4 — effort M — risk low — category: skills
  Why: anthropics/skills fixes the rules: name equals folder, description ≤1024, body <5k tokens. A "save this run as a skill" key drafts a SKILL.md with a visible meter whose checks tick green as the draft conforms.
  Done when: a draft with a 1,100-character description shows a red meter, and trimming it to 1,000 turns it green and writes a validator-passing skill.

- **Grade models on a prompt-engineering dojo** — FEATURE — value 4 — effort M — risk low — category: runners
  Why: the tutorial's chapters (roles, XML tags, prefill, few-shot, allow-"unknown") are a model exam, but its licence is unstated, so write original exercises from the ideas only. Results appear as chapter ribbons on each runner's card and feed routing.
  Done when: `fm code bench --dojo` runs at least 8 original exercises against a stub runner and prints a per-chapter pass ribbon.

- **Flip through a goal loop like a flipbook** — FEATURE — value 3 — effort M — risk low — category: replay
  Why: the claude-code /goal and ralph-wiggum Stop-hook loops make many near-identical iterations, which are hard to read in a log. Each iteration becomes a thumbnail (diff size, pass/fail dots), and arrow keys flip between them.
  Done when: a recorded 6-iteration loop opens in the flipbook, and the left and right keys step the diff view.

- **Greet finance projects with a vertical ribbon** — FEATURE — value 3 — effort S — risk low — category: domains
  Why: financial-services is Apache-2.0 with 7 verticals, and the docx/pdf/xlsx skills fit spreadsheet-heavy folders. Detecting .xlsx and .pdf-heavy projects puts a ribbon on that project's card: "finance pack available, 3 skills, 0 paid connectors needed".
  Done when: a fixture folder with xlsx files shows the ribbon, and a folder without them does not.

- **Wild: Open a "patch notes trailer" when Claude Code ships** — FEATURE — value 3 — effort M — risk low — category: scout
  Why: assumption: `fm scout` finds releases but they land as dry tasks. A 20-second in-app card reads like game patch notes: "new this release, already used by Foreman, auto-adopted, ignored (and why)".
  Done when: feeding a fixture CHANGELOG entry to the scout produces a card with the three groups populated.

- **Wild: Print a licence-aware collectible sticker per source repo** — FEATURE — value 2 — effort S — risk low — category: integration delight
  Why: the six repos have mixed licences (MIT, Apache-2.0, source-available, none stated). Each repo gets a sticker on the shelf that is honest about what Foreman may copy and what it may only learn from, and the guard refuses to vendor a no-licence repo's text.
  Done when: the sticker for the tutorial repo reads "ideas only", and an attempt to vendor its text is refused with that reason.

- **Wild: Offer "next to try" from the user's own history** — FEATURE — value 3 — effort M — risk med — category: discovery
  Why: assumption: with 166+ plugins, nobody can browse. Local-only matching of past requests to marketplace descriptions yields one suggestion a day, shown as a tile on the home screen, with nothing sent anywhere.
  Done when: seeded history containing PDF requests ranks the pdf skill first, and the match runs with the network blocked.
