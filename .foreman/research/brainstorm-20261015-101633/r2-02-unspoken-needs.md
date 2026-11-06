# Brainstorm — lens: unspoken needs

Note: the pile is close to saturated. These ten-plus ideas come from what the user's phrasing implies, and I've avoided the listed ones.

- **Count "keep going" prompts as stalls** — FEATURE — value 4 — effort S — risk low — category: autonomy
  Why: the request itself is "can you keep going?", sent after a round closed at its own finish line. The user is acting as the loop driver, and nothing records that. Assumption: the Stop hook can see the previous stop's disposition.
  Done when: a prompt that is only a continuation nudge ("keep going", "continue", "go on") writes a stall record with the preceding stop reason, and `fm doctor` shows the weekly count.

- **Pick the next round from one friction table** — FEATURE — value 4 — effort M — risk low — category: product sense
  Why: the pile holds ~2000 ideas, and round 5 is still brainstorming from a list. Real pain signals are scattered: guard blocks the user overrode, close warnings ignored, stall records, idle-while-queued minutes, doctor failures, retries after refusals, drops. Assumption: each signal is already logged somewhere.
  Done when: `fm friction` prints one ranked table of those signals, and a round brief starts from its top 5. With an empty table it says "nothing hurts, don't brainstorm".

- **Lint CLAUDE.md and rival skills for contradictions with Foreman's contract** — FEATURE — value 4 — effort M — risk med — category: coexistence
  Why: the rival survey and `--apply-conflicts` handle competing plugins, but not instruction text. For example, "commit after every edit" in a user's CLAUDE.md fights "close before commit". Assumption: contradictions exist in real setups and nobody sees them.
  Done when: `fm doctor` flags a seeded CLAUDE.md line that contradicts a Foreman rule, quoting both lines and the file path.

- **Audit the final message's claims against the tool log** — FEATURE — value 4 — effort M — risk med — category: honesty
  Why: Foreman records evidence for criteria, but the closing prose ("all tests pass", "I fixed X and Y") is unchecked. Assumption: the Stop hook can read the last assistant text.
  Done when: a final message claiming "tests pass" with no matching passing run in the task's tool log is blocked once with the unmatched claim named.

- **Mark evidence stale when the user steers** — FIX — value 4 — effort M — risk med — category: plan integrity
  Why: the user's history is full of steers and drops. A criterion changed mid-task can still carry green evidence recorded for the old wording. Assumption: nothing links an amendment to existing evidence.
  Done when: editing a task's criterion flips its recorded evidence to "stale", and `fm task finish` refuses until it is re-run.

- **Rank the morning diff review by risk, with a "safe to skim" verdict** — FEATURE — value 5 — effort M — risk med — category: trust handover
  Why: the user is running long unattended rounds and can't read 40 diffs. Assumption: the review is the real bottleneck now, not the work.
  Done when: after an overnight run, `fm review` lists the 5 hunks to read first, each with the reason it ranked (untested lines, guard-adjacent file, hot path), plus one line saying which files the evidence covers fully.

- **Verify document deliverables, not just code** — FEATURE — value 3 — effort M — risk low — category: non-code evidence
  Why: the installer ships Office/PDF skills (`--docs`), but evidence assumes tests and commands. Assumption: users produce docs, decks and READMEs under tasks.
  Done when: a task whose deliverable is a doc fails its gate on a seeded broken link, leftover `TODO`/lorem text, or a missing heading, and passes once fixed.

- **Attach before/after screenshots as evidence on UI tasks** — FEATURE — value 3 — effort M — risk low — category: UI evidence
  Why: foreman-ui (tsx) and the web UI exist, but the closing evidence is text. Assumption: a headless browser is available, or the native browser tool can be used.
  Done when: closing a UI task stores a before and an after image of the named route in its evidence, and the close-out lists their paths.

- **Wild: Seed a canary defect to measure reviewer recall** — FEATURE — value 4 — effort M — risk med — category: review quality
  Why: T-0034's lens reviewers have no recall number, only findings. Assumption: reviewers run on a throwaway copy of the diff, never the real tree.
  Done when: `fm audit --canary` plants a known bug in a scratch copy, runs the reviewers, and prints caught or missed. A miss rate above a set threshold fails a bench gate.

- **Wild: Get an independent second opinion from a different vendor's CLI** — FEATURE — value 3 — effort M — risk high — category: independence
  Why: the codex/gemini/opencode adapters (T-0335, T-0336) sit blocked with no purpose beyond parity. A same-family reviewer shares the builder's blind spots. It needs an explicit opt-in because the diff leaves the machine.
  Done when: with the setting on, an L task's close sends a redacted diff to the configured CLI and records its verdict; with it off, nothing is sent and a test proves that.

- **Wild: Add `fm teach`, a mode that narrates and quizzes** — FEATURE — value 2 — effort M — risk low — category: audience
  Why: assumption: people who ask "why" and are learning are an unserved audience, and a plugin they can learn from spreads by word of mouth.
  Done when: with the mode on, each plan step gets a one-line "why this" and a closing 3-question recap, and `fm task finish` is unchanged.

- **Wild: Add a "reviewer FAQ" to every close-out** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: Foreman argues against the plan before work, but nothing pre-answers the questions a skeptical reviewer would ask of the finished diff. Assumption: three questions are enough.
  Done when: every L close-out ends with three likely questions, each answered with a pointer to evidence, and none of those pointers is dead.
