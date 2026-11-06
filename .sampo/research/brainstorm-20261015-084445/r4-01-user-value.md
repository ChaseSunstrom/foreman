# Brainstorm — lens: user value

I couldn't find much that's truly new for the user-value lens. Rounds 1–3 and the survey gaps already cover most of it, so most of these are second-order or combinations. Each one says what it adds beyond the nearest existing idea.

- **Add `fm away <until>`, one verb for "I'm gone"** — FEATURE — value 5 — effort M — risk med — category: unattended
  Why: the pile has the parts (charter, quiet hours, walk-away check, morning card, budget, no-push rules) but no single entry point. The user's "keep going… recursively" suggests they want to walk away with one sentence. Assumption: one verb binding existing parts beats the parts.
  Done when: `fm away friday-9am` starts a bounded run, refuses to push or release, and the next session opens with one "while you were away" card listing finished, blocked and asked items.

- **Hold a sleep inhibitor while an unattended run is live** — FEATURE — value 4 — effort S — risk low — category: unattended
  Why: assumption: overnight or night runs die when the laptop sleeps. The pile only reconciles after suspend and never prevents it.
  Done when: `fm run` and `fm night` take `systemd-inhibit` (Linux) or `caffeinate` (macOS) for their lifetime, and the lock is gone after a clean exit or a kill.

- **Learn the project's runbook from commands that worked** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: the test runner was run 1,586 times, yet a fresh `fm check` can't detect it and `fm repeats` suggests bad gates. Success-verified commands (exit 0, repeated, in the project root) can fill a 3–5 line runbook: test, lint, build, dev server.
  Done when: after a few sessions `fm check` proposes the observed whole-suite command, and a failing command never enters the runbook.

- **Add `fm rescue` for a half-finished human branch** — FEATURE — value 4 — effort M — risk med — category: adoption
  Why: assumption: newcomers arrive mid-work, not with an empty queue. Beyond "adopt manual commits", this runs the branch's gates, lists what's red and unfinished from the diff and TODOs, and files a finish plan as queued tasks.
  Done when: on a seeded broken branch, `fm rescue` prints red gates plus a ≤6-step finish plan and creates the matching tasks.

- **Print a verified "try it yourself" line at every close** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: the pile has acceptance artifacts and demo transcripts, but a hands-on check the user can run is different. Foreman runs the line itself first and prints it only if it exits 0.
  Done when: a FEATURE close prints one copy-paste command, and a command that fails Foreman's own dry run is never printed.

- **Snapshot all of `~/.claude` at session start and add `fm claude-undo`** — SECURITY — value 3 — effort S — risk low — category: trust
  Why: rivals also rewrite settings, and ECC's hook-conflict complaints show it hurts. The existing journal only covers Foreman's own wiring. This one is plugin-agnostic.
  Done when: after a third-party plugin edits `settings.json`, `fm claude-undo` restores the prior bytes and prints the diff first.

- **Bench the user's own CLAUDE.md lines against their ledger** — FEATURE — value 3 — effort L — risk med — category: self-knowledge
  Why: existing ablation covers Foreman's rules, not the user's. Rules load every session, and the user has shown they care about footprint.
  Done when: `fm ablate-claude-md` reports which lines changed behaviour on replayed tasks and proposes deleting the ones that never did.

- **Wild: React to the user's red test run before they read it** — FEATURE — value 4 — effort L — risk high — category: ambient
  Why: wild. The user runs tests by hand constantly. A file-event watcher notices a red suite in the user's own terminal and prepares a candidate fix in a lane, offered with one key and never applied.
  Done when: a manually broken test produces a ready lane diff within 60 seconds, with nothing applied to the user's tree.

- **Wild: Disclose Foreman's competence per stack at plan time** — FEATURE — value 3 — effort M — risk low — category: honesty
  Why: wild. Per-ecosystem held-rates already exist in the ledger. Showing "Go: 70% held, so I'll verify harder here" is honest and also tunes ceremony.
  Done when: a plan on a low-held-rate stack shows the rate and enables one extra gate, and a high-rate stack shows nothing.

- **Wild: Offer a "foreman walk-through" card on new repos' first session** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: wild. Three hazards, three useful commands and one thing it would fix first, spoken in Foreman's voice from `fm map`, in under 10 lines. It's distinct from a full tour because it ends in a single suggested first task.
  Done when: a first session on an unseen repo shows the card once, and each hazard names a real file.

- **Show a "what you can safely ignore" line per task** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: the open-warning pile is large and users often override close warnings. Listing the checks that passed with strong evidence lets the user skip them.
  Done when: a close prints at most one line naming gates verified by recorded evidence, and a task with weak evidence prints none.

- **Stamp each queued brief with "needs a human?" up front** — FEATURE — value 3 — effort S — risk low — category: queue
  Why: blocked items such as T-0325 (needs sudo) and T-0418 (update the mod) sit unseen. Predicting human-only steps at capture lets `fm away` skip them and `fm run` batch them into one "your chores" list.
  Done when: capturing "install libappindicator" sets the flag, and `fm away` omits flagged tasks.
