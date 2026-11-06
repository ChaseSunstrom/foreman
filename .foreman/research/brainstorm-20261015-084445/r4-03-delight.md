# Brainstorm — lens: delight

Delight is saturated in this pile, so each idea below names its nearest existing neighbour and the new mechanism that separates it. The newcomer evidence (A.1–A.11) is where these have the most grounding.

- **Give `fm` a shell front door with `eval "$(fm shellinit)"`** — FEATURE — value 4 — effort S — risk low — category: first-run
  Why: A.3 (`fm` is "command not found" in a shell), plus the README says "run fm …" everywhere. Nearest: "Put fm on the shell PATH", completions. New: one line gives PATH, tab-completion with live task IDs, and a direnv-style one-liner on `cd` into a managed project ("foreman: 3 queued, 1 needs you"). Assumption: bash/zsh/fish are all supported.
  Done when: in a clean HOME, after the one line, `fm status` works in a plain shell and `cd` into a project prints exactly one status line.

- **Add `fm oops`, a one-word "that was wrong"** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: gate false positives and wrong tiers are known, and the user's pushbacks are the best signal. Nearest: allow-once, "teach this" prompt. New: one verb that does four things at once. It grants allow-once for the last block, logs a corpus entry, undoes a mis-tiered hold, and prints a one-line promise ("won't block `git -C` here again").
  Done when: after a guard block, `fm oops` lets the retry through and adds a replay-corpus case. A test asserts the same command then passes the guard replay.

- **Name each major incident and use the name in recall** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: 18 fixed-later tasks and 688 tasks exist, but T-ids are opaque and no one remembers T-0612. Nearest: failure museum, dead-end atlas. New: a short human name per big FIX ("the Slow-Wifi Incident"), stored in the brief. Plan-time recall says "this looks like the Slow-Wifi Incident".
  Done when: a FIX close-out stores a ≤4-word name, and `fm recall` finds it by name.

- **Quote the user's own request back, side by side with Foreman's reading** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: "FIX: login times out" is terse, and A.1 says Foreman's value is abstract at first sight. Nearest: intent beside the request. New: the first three tasks only, Foreman shows "You said / I'm reading it as / I'll prove it by" as a three-line card. It stops after three tasks or on `fm nope`.
  Done when: tasks 1–3 on a fresh install print the card, and task 4 does not.

- **Show true repo trivia instead of a spinner on gates over 20 s** — FEATURE — value 2 — effort S — risk low — category: observability
  Why: the test runner is the most repeated command (1,586 calls), so waits are the most frequent dead time. Nearest: "gate waits as review tour". New: rotating facts computed locally from the map and ledger (slowest test, oldest TODO, most-edited file, an unanswered capture). Each fact is real and clickable.
  Done when: a gate over 20 s shows ≥2 distinct facts, none repeated within a run, and zero model calls are used.

- **Put a "was it worth it?" one-key rating on close, feeding the held-rate evidence** — FEATURE — value 4 — effort S — risk low — category: proof
  Why: C says 160 of 370 tasks are "ungraded" and there is no published evidence Foreman helps. A cheap human label is the missing ground truth. Nearest: one-tap verdict on selected tasks. New: only tasks that would otherwise be ungraded get asked, one key, silent after three skips.
  Done when: an ungraded task shows the prompt once, and `fm digest` counts the answer.

- **Replace jargon in the first-session band with a swappable "plain" vocabulary** — FEATURE — value 3 — effort M — risk low — category: first-run
  Why: A.11 lists brief, evidence, audits, scope, drive, lane and focus as unexplained. Nearest: plain-words mode, glossary. New: the band and `fm status` render through one term table. Week-one text says "proof" and "check your work", and the real terms appear once the user has used them.
  Done when: a snapshot of a fresh-install `fm status` contains none of the seven jargon words.

- **Wild: Add "On this day" to the greeting** — FEATURE — value 2 — effort S — risk low — category: ritual — wild
  Why: assumption: users with long histories enjoy nostalgia. Nearest: spaced resurfacing of decisions. New: one line from the ledger or git log ("a month ago you shipped the compact-output cap"), shown only when something notable exists.
  Done when: on a date with a matching closed task, the greeting shows it, and otherwise it is silent.

- **Wild: Play a Foreman quest with `fm quest`, a text adventure through the verbs** — FEATURE — value 3 — effort M — risk low — category: learning — wild
  Why: A.4 says `fm --help` is 100 verbs of brace blob. Nearest: `fm learn`, `fm hello`, `fm tour`. New: a tiny no-model dungeon whose rooms are the core eight verbs, each solved by running the real verb on a fixture. The ending unlocks `fm help --all`.
  Done when: a scripted playthrough passes in CI with zero model calls and leaves the user's repo untouched.

- **Wild: Keep a weekly queue bingo card** — FEATURE — value 2 — effort S — risk low — category: ritual — wild
  Why: assumption: light gamification of good habits (first-time pass, net deletion, caught secret, overnight run, folded duplicate) lifts engagement. Nearest: shelf of firsts. New: a recurring 3×3 card from the ledger, shown in Sunday's digest, with no scores and no sharing.
  Done when: the digest renders a card whose squares each cite a ledger event.

- **Wild: Let the uninstall be a graceful goodbye that proves it left nothing** — FEATURE — value 3 — effort M — risk low — category: trust — wild
  Why: A.10 says uninstall leaves residue and prints "defaultMode = None". Nearest: exit interview, byte-identical uninstall. New: a before/after tree diff printed at the end ("restored 7 settings, removed 41 files, 0 left"). It ends with a one-line "what would have kept you?" saved locally.
  Done when: install then uninstall in a clean HOME leaves a byte-identical `~/.claude`, and the printed diff matches the real one.

- **Offer a polite handoff line when a rival skill takes the wheel** — FEATURE — value 3 — effort S — risk med — category: coexistence
  Why: B shows users run superpowers and spec-kit, and hook conflicts are their top complaint. Nearest: peace-treaty card, coexist. New: at runtime, when a known rival skill is invoked, Foreman says once "superpowers is driving; I'm keeping the guard, resume and done-gate" and records that.
  Done when: invoking a rival skill triggers the line once per session, and the done-gate still blocks an evidence-less close.
