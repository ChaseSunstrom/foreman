# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Count Sampo vocabulary in the user's own asks** — FEATURE — value 4 — effort S — risk low — category: obsolescence
  Why: assumption: the typed asks in the pack are plain English ("keep going", "I want wild") and almost never name a verb or task id. A surface the user never speaks to is vestigial, and anticipation may only need the few verbs the user's sentences map to.
  Done when: a zero-token report lists every verb and skill with the count of user messages that named it or its synonym over 60 days, and the zero-count ones are marked.

- **Scan the user's own tooling for hand-built twins** — FEATURE — value 3 — effort M — risk low — category: obsolescence
  Why: assumption: a user who builds `justfile`, alias or git-hook equivalents of a Sampo verb has already replaced it. Anticipation should stop drafting asks for that verb and the verb should go on the retirement list.
  Done when: a read-only scan of `~/.bashrc`, the registered repos' `Makefile`/`justfile` and `.git/hooks` names at least one verb with a matching command, or prints "none found" with the files it read.

- **Rank guard classes by undo time, not command shape** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: assumption: snapshots, git and the trash shrink the cost of a mistake. Blocks on classes the user can undo in under 30 seconds are the first the host's own permissions will make unnecessary. T-0034 and the Ward only guess at this.
  Done when: each Ward block class has a measured or probed undo time on this machine, and classes under the threshold can be set to log-only with a one-line receipt of what it would have lost.

- **Remove Exam readings that CI already runs** — CLEAN — value 3 — effort S — risk low — category: dedupe
  Why: the carried gap says every brief's Exam reads live state. If the repo's CI (`.github/workflows/test.yml`) already runs the same command, Sampo's copy is a second source of truth that will drift.
  Done when: filing a brief whose Exam command appears in CI config prints "CI already runs this; Exam links to it" and does not store a copy.

- **Track the zero-user-turn share by task kind** — PERFORMANCE — value 4 — effort S — risk low — category: measurement
  Why: assumption: anticipation exists to save the user's turns. If the share of tasks that close with zero user messages after the first ask rises on its own, the predictor's lift is shrinking whatever its hit rate says.
  Done when: `fm outcomes` prints, per task kind and week, the share of closes with no user turn after intake, and the anticipation hit rate is printed beside it.

- **Diff the anticipation card against the host's own memory file** — FEATURE — value 3 — effort M — risk low — category: host overlap
  Why: assumption: Claude Code's memory and `CLAUDE.md` now hold much of what the user model holds. Any card line already present in them is redundant and should be marked so.
  Done when: each card line is tagged "also in host memory" or "only here", and a count of "only here" lines is shown over time.

- **Run a monthly replacement bid** — FEATURE — value 3 — effort M — risk med — category: self-doubt — wild
  Why: assumption: Sampo only gets simpler when something forces it. A cold child sees only the README and the user's last 30 asks and must propose one cheaper replacement for the single most-used capability; Sampo builds it in a scratch worktree and replays history through it.
  Done when: a monthly file holds the bid, the replay's hit-rate delta and cost delta, and a verdict ("keep" or "replace") that a test can read.

- **Give every capability a sunset date that only evidence can extend** — CLEAN — value 4 — effort M — risk med — category: lifecycle — wild
  Why: the pack has many "retire-when" and "lifecycle ladder" ideas but each needs someone to act. Inverting the default makes disappearance automatic.
  Done when: a capability with no session-path use in 90 days is marked sunset in `fm doctor`, its skill is stubbed from default load, and `fm bring-back NAME` restores it.

- **Write a one-page Sampo-less manual and score it as the baseline** — FEATURE — value 4 — effort M — risk low — category: obsolescence
  Why: the question that decides everything is how much of Sampo's lift a single static file would give. A generated file of the standing steers, gates and map would answer it, and it doubles as the install for harnesses that have no hooks.
  Done when: one command writes the file from steers, the gates line and the map, and a replay of held-out asks with only that file scores within a stated margin of full Sampo, or the gap is printed.

- **Fire a tripwire from the model's own release** — PERFORMANCE — value 3 — effort M — risk low — category: models
  Why: pinned IDs (`claude-fable-5-1`, `claude-opus-5-5`) and the local qwen switch mean a model change is the likeliest cause of a sudden obsolescence. Re-running the necessity corpus automatically at the first call to an unseen model ID would tell the user the same day.
  Done when: the first session on a new model ID runs a small fixed corpus and writes "lift at risk: X of Y cases now pass without Sampo" to the morning card.

- **Hold a "Sampo went away" rehearsal for the morning** — FEATURE — value 3 — effort S — risk low — category: resilience — wild
  Why: assumption: the user wants major progress by morning, and a drive that stops at 3am leaves nothing. Run one night with hooks and verbs off, using only plain `claude -p` against the queue, and compare what landed.
  Done when: two nights' reports (full and bare) list tasks landed, cost and reverted closes side by side, with one verdict line.

- **Let a cold child write the obituary of each capability from ledger data** — FEATURE — value 2 — effort S — risk low — category: legibility — wild
  Why: assumption: a cold read written as an obituary is the quickest way to spot capabilities nobody would miss. The child sees only usage counts and the verb help line, and is told to say what was lost.
  Done when: a file holds one obituary per capability under 40 words each, and any with "nobody would notice" is listed first in `fm doctor`.

Next question: what would the user have to stop doing, or start doing, for Sampo's anticipation to be worth less tomorrow than today, and does the ledger already show the first sign of it?
Next question: which of Sampo's lifts are an artefact of the model it ran against, and which would survive a model one rung up?
