# Brainstorm — lens: unspoken needs

- **Probe whether a fix should travel before building it** — FEATURE — value 5 — effort M — risk low — category: scope
  Why: the user had to say "I don't just mean Foreman itself, any project" and "it should be transferable in git". Foreman read both as self-improvement for this repo. Assumption: the same narrow reading will recur on other requests.
  Done when: at plan time, a task that touches Foreman internals records one line, "applies to: this repo / any project / machine", and a test shows a generic-sounding request defaults to the portable design (hint file in git).

- **Run a sibling sweep when a fix closes** — FEATURE — value 5 — effort M — risk low — category: regression
  Why: T-0990's `~/.local/bin` fallback fixed one bug and bypassed the tests' claude lockout, which then reached the paid binary. The "Catch it earlier" drops show the same shape. A fix to a shared helper breaks its callers.
  Done when: closing a fix lists other call sites or patterns that match the changed code and which tests cover them. A seeded case (helper change, uncovered caller) blocks the close until a test or a waiver exists.

- **Run the gates under an environment matrix** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: recent bugs are all environment assumptions: native-only claude with no `~/.local/bin` on PATH, a PATH-replacing test, the env-file prelude repeating 8x. Assumption: more such bugs exist on other shells, HOME layouts and distros.
  Done when: `fm doctor --matrix` runs the roundtrip gate under at least 4 hostile profiles (no claude on PATH, claude native-only, read-only HOME, `sh` instead of bash), each pass or fail is reported, and a seeded regression turns one red.

- **Preview the pane without a reload** — FEATURE — value 4 — effort M — risk low — category: ui loop
  Why: the user's feedback comes "after reload" ("still cluttered, graphs too big"), so every layout round costs a full reload and a screenshot harness that has already leaked into a real session once. Assumption: a hot preview shortens the design loop.
  Done when: `fm ui preview --size 120x40` renders the current pane from fixture state in a scratch terminal or file, diffs it against the last approved render, and never touches live session state.

- **Measure density instead of waiting for "still cluttered"** — FEATURE — value 4 — effort S — risk low — category: ui quality
  Why: the user steers on the same properties repeatedly: filled dock, no gaps, fewer facts per line, aligned rows, no empty regions. These are measurable.
  Done when: a render test reports empty-cell ratio, facts per line and unaligned rows for 5 terminal sizes. It fails above thresholds taken from the user's stated rules, and a deliberately sparse layout fails it.

- **Refuse near-duplicate ideas before they cost a review** — CLEAN — value 3 — effort M — risk low — category: brainstorm
  Why: the "Ideas so far" list has roughly 400 entries and many restate each other ("resume manifest", "resume capsule", "resume ledger", "heartbeat checkpoint"). Rounds spend tokens re-reading and re-judging them. Assumption: clustering by title and keywords catches most repeats.
  Done when: `fm ideas` drops new ideas whose similarity to a catalog entry exceeds a threshold and lists what they matched. The pack carries cluster digests (title plus count) instead of every line. A round with only duplicates reports "dry".

- **Give every adopted idea a sunset clause** — FEATURE — value 4 — effort M — risk med — category: simplification
  Why: the user wants Foreman "genuinely the best" and also lighter (Lite mode, retire adapters, root clutter). Features only ever accumulate. Assumption: the user prefers deletion when the evidence is clear.
  Done when: each shipped feature declares one metric (hits, firings, saves) with a review date. `fm sunset` lists features whose metric stayed flat, and each becomes an open deletion task with its numbers.

- **Show a brain diff in every PR** — FEATURE — value 3 — effort S — risk low — category: shared learning
  Why: learned hints now travel by git (T-1032), so a teammate's PR may change how other sessions behave without anyone reading it.
  Done when: a CI step or `fm brain diff main` prints added, changed and retired hints in plain language with the incidents behind them. A PR that edits a hint file produces it.

- **Say what you took from the request** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the user's asks are long and multi-part ("playbooks too, MCP, LSP, everything…"), and the steers show parts got dropped or narrowed. Assumption: a short restatement catches this cheaply.
  Done when: at task start, a two-line "I understood: … / not doing: …" note is stored on the task, and `fm task finish` checks each clause against the evidence.

- **Wild: Develop Foreman under a pinned stable twin** — FEATURE — value 4 — effort L — risk med — category: dogfooding
  Why: the harness Stop hook already took focus from the working session once, and Foreman edits its own hooks while running on them. Assumption: a hook edit that crashes mid-session is a real risk.
  Done when: sessions in the Foreman repo run hooks from the last released snapshot, the working tree's hooks are exercised only through a candidate channel, and a deliberately broken hook edit leaves the live session unaffected.

- **Wild: Open the next session with a ten-second "what I'd fix first" pitch** — FEATURE — value 3 — effort M — risk low — category: initiative
  Why: the user asked "why have you not really improved?" and says they shouldn't have to ask for things. Assumption: leading with evidence of its own pain points (repeated obstacles, slow gates, deferred items) beats waiting for a request.
  Done when: SessionStart prints at most 3 evidence-linked proposals, each accepted or declined with one word. Declines are remembered, and a declined one is not offered again for 30 days.

- **Wild: Let the user reject an idea once and have Foreman learn the whole category** — FEATURE — value 3 — effort M — risk low — category: taste
  Why: the user dropped items as "harness noise" and "covered", and Foreman keeps proposing near neighbours. Assumption: a one-word reason on a drop is cheap to give.
  Done when: dropping an idea takes an optional reason tag. A later brainstorm round reads the tags, suppresses matching ideas, and states the suppression ("3 hidden: you called this noise").
