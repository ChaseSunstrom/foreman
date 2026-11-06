# Brainstorm — lens: grid

Surfaces here are the web UI, plus the `fm` CLI and the Genesis site as entry points. Actors are the user, the agent, other agents (lanes and lens children) and the unattended run. Each idea names its cell as surface × actor × failure mode.

- **Author each outcome measure blind** — FEATURE — value 4 — effort M — risk low — category: briefs
  Cell: CLI × agent × wrong.
  Why: a builder that writes its own outcome measure can pick one its fix satisfies. The standing rule already has a separate tool-less child write exam scenarios, but no rule covers a brief's Exam line.
  Done when: filing a brief records a measure author, and a test fails when the author is the same session that wrote the fix.

- **Give dissents a fourth state, "outcome never observed"** — FIX — value 4 — effort S — risk low — category: scoring
  Cell: web UI × user × unclear.
  Why: scoring dissents against outcomes silently counts a dissent with no observable outcome as a miss or a hit. Assumption: some outcomes never occur inside the settle window.
  Done when: a dissent with no outcome by its deadline shows as "unsettled" and is left out of the hit-rate denominator, with the count printed beside it.

- **Require a today's-value on every outcome measure** — FEATURE — value 4 — effort S — risk low — category: briefs
  Cell: CLI × agent × missing.
  Why: the carried gap asks for an outcome measure, but "improve X" cannot be judged without X's current reading.
  Done when: the filing lint refuses an `outcome:` line that has no `now:` value taken from a command it ran.

- **Bind each live-state reading to the checkout it was taken in** — SECURITY — value 3 — effort M — risk low — category: briefs
  Cell: CLI × unattended × wrong.
  Why: lanes use worktrees and the installed copy can differ from the source, so a `live:` reading can pass against a different tree than the one shipped. Assumption: readings don't currently record where they ran.
  Done when: a reading stores HEAD, worktree path and ledger epoch, and a close run from a different checkout reports "not comparable" instead of pass.

- **Canonicalize cell ids across lens children** — CLEAN — value 3 — effort S — risk low — category: grid
  Cell: CLI × other agents × unclear.
  Why: ten lenses name the same cell ten ways, which is visible in how many near-duplicate ideas the pack's idea list holds.
  Done when: an idea whose cell isn't `surface.actor.mode` from the fixed vocabulary is rejected at collection, and two lenses' ideas for one cell collapse into one row.

- **Claim a cell before two lanes build it** — FEATURE — value 3 — effort M — risk med — category: lanes
  Cell: web UI × other agents × wrong.
  Why: parallel lanes filed from one grid can fill the same cell twice, and a merge conflict is the cheaper symptom. Assumption: briefs don't currently carry a cell id.
  Done when: a second lane asking for a claimed cell is refused and shown the holder.

- **Write the left-out receipt incrementally, per cell** — FIX — value 4 — effort S — risk low — category: reliability
  Cell: web UI × unattended × missing.
  Why: "say what it left out" is written at the end, so a crash or usage-limit kill leaves no list, which is exactly when the list matters most.
  Done when: killing a Mission mid-run still leaves a receipt listing every cell decided so far, and the web page marks it "interrupted".

- **Scan docs and site text in every canary** — FIX — value 3 — effort S — risk low — category: grounding
  Cell: CLI × agent × missing.
  Why: "already built" often lives in MASTER.md or `site/genesis` prose and not in code, so a code-only canary reports "not found" for something documented.
  Done when: a canary for a known documented-only feature returns a hit from the docs path, tested on a planted case.

- **Mine a sixth failure-mode column from dropped items** — FEATURE — value 3 — effort M — risk low — category: grid
  Cell: web UI × user × missing.
  Why: drops are filed as "by design", "gap", "already met", and none of these fit missing, wrong, slow, unsafe or unclear.
  Done when: the grid report lists any drop reason that recurs 3 or more times and fits none of the five columns, as a proposed column.

- **Fold the web grid to the top five empty cells by sting** — FEATURE — value 3 — effort M — risk low — category: web UI
  Cell: web UI × user × slow.
  Why: a full actor × surface × mode grid is a wall of cells and reading it costs the user more time than the Mission saved. Assumption: they will read only the top.
  Done when: the grid page opens with five cells ranked by sting and the rest behind one click, and each cell shows its "N left out" count.

- **Audit the receipt with an independent reader** — FEATURE — value 4 — effort M — risk low — category: reliability
  Cell: CLI × unattended × wrong.
  Why: the run that left things out also writes the list of what it left out. The standing rule already prefers signals Foreman didn't author.
  Done when: a tool-less child given only the request and the filed briefs lists omissions, and any omission absent from the receipt is printed as a miss.

- **Test the axes, not the cells (wild)** — FEATURE — value 3 — effort M — risk low — category: grid
  Cell: CLI × other agents × missing.
  Why: wild; assumption that fixed axes hide whole rows (for example a "second machine" actor).
  Done when: a child proposes its own axes from the request alone, and any row of its grid with no counterpart in ours is reported.

- **Revoke an n/a with a user story (wild)** — FEATURE — value 3 — effort S — risk low — category: grid
  Cell: web UI × user × wrong.
  Why: wild; every n/a is a claim that nobody lives in that cell, and nothing tests it.
  Done when: a cold child writes a one-paragraph user story for a sampled n/a, and a judge one rank stronger rating it plausible turns the cell back into an empty one.

- **Draw one random empty cell a week for a cheap probe (wild)** — FEATURE — value 2 — effort M — risk low — category: measurement
  Cell: CLI × unattended × unclear.
  Why: wild; no one knows whether empty cells matter, and a random hold-out is the only unbiased test.
  Done when: each week one random empty cell gets a probe, and the report shows how many such probes found a real defect.

Cells I left empty:
- Web UI × unattended × slow: nothing in the pack shows a slow web page.
- Site × any × unsafe: the site is static published data, and a leak scan is already listed.
- Agent × user × slow: it is covered by earlier stop-on-saturation ideas.

Next question: which of the five failure modes has never produced a filed item in this repo, and is that because it does not apply or because nobody looks for it?
Next question: when a brief's `live:` reading is run twice an hour apart, how often do the two readings differ on this repo?
