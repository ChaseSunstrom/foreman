# Brainstorm — lens: user value

- **Store every captured message verbatim and retitle vague captures** — FIX — value 4 — effort S — risk low — category: intake
  Why: T-0756 was captured as "also, the …" (the first "fix foreman" message, truncated), T-0317 as "There's new bug feedback", and T-0757 as "and reordering of operations, so like for all of these things…". The user's actual words are lost or unreadable. This is an evidence-backed fix.
  Done when: a test feeds a 600-character message with a leading "also," into capture, and `fm task show` returns the full text byte-for-byte with a title that names the subject.

- **Honour inline model pins in requests (`@haiku`, `@sonnet`, `@opus`, `@fable`)** — FEATURE — value 4 — effort S — risk low — category: delegation
  Why: T-0755 asks "can foreman spawn agents of lower models?". Per-call `model` and `effort` already exist on the Agent tool, but the user has no way to say it in prose. Existing ideas route automatically from a learned table; this lets the user override per clause.
  Done when: the request "@haiku rename these fields, @opus review the migration" produces two lanes whose Agent calls carry those model values, and both appear in the ledger.

- **Fold a burst of messages into one milestone with the operations reordered** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: T-0757 asks to put all of these things into one task or milestone and reorder the operations. Existing ideas fuse by shared file footprint or split oversized briefs. None groups by arrival burst and reorders the user's own list by dependency.
  Done when: five messages sent within 3 minutes become one milestone with child tasks in dependency order. The ledger shows the original order and the reason for each move.

- **Resync Foreman's step pointer after a native rewind or forked session** — FIX — value 4 — effort M — risk med — category: resume
  Why: T-0759 shows the step pointer drifting from the work done. Claude Code's checkpoint rewind and `--fork-session` move the conversation and files, but Foreman's STATE and ledger keep going forward. Assumption: a rewind can be detected from the transcript or a hook payload.
  Done when: a scripted session that rewinds two steps shows STATE's current step matching the rewound tree on the next prompt, and `fm doctor` flags any mismatch.

- **Close the loop on each complaint in the user's own words** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the recurring complaints ("sits idle", "starts different steps without updating the step") are tasks that get fixed silently. Assumption: users would value a first-line message saying "you said X, fixed in 1.2.28, here's how to tell".
  Done when: after a release that closes a task born from a user message, the next session's first reply quotes that message and the fix, and shows it once only.

- **Adjudicate gray-zone guard cases with a cheap prompt-type hook** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: the dropped items show repeated guard false positives (the quoted heredoc, `python -c` with `import fmcli`, `--focus &&`). Each cost the user a turn. A haiku judge that sees the parsed effects could resolve the "can't prove" cases. Assumption: the prompt hook type is usable, and a timeout fails closed. The prompt-injection risk is why risk is med.
  Done when: on the recorded false-positive corpus the adjudicated allow rate is at least 80%, and every red-team case still blocks.

- **Mirror lessons into path-scoped native rules** — PERFORMANCE — value 3 — effort M — risk low — category: context
  Why: hooks are latency-gated, and lessons are injected through hook output. Assumption: Claude Code loads `.claude/rules/*.md` files with `paths` frontmatter only when matching files are touched, at zero hook cost. Existing ideas inject at the action through hooks. This version needs no process spawn.
  Done when: a lesson tied to `plugin/lib/fmguard*.py` appears in context only after a read of a matching file, and `bench_hooks.py` shows no added per-prompt time.

- **Benchmark the native auto-mode classifier against the guard corpus** — CLEAN — value 3 — effort M — risk med — category: simplification
  Why: guard surface keeps growing (T-0275 is deferred, and each fix adds rules). Assumption: auto permission mode has a classifier that blocks destructive actions. If it catches the same cases, those rules can be deleted.
  Done when: a report lists corpus cases caught by both, only by the guard, and only by the classifier. At least one duplicate rule is removed with the corpus still green.

- **Replace "needs sudo" blockers with a userland fallback** — FIX — value 3 — effort M — risk low — category: autonomy
  Why: T-0325 is blocked on `sudo pacman -S libappindicator-gtk3`, and the user never wants to be handed commands. Options include bundling the library in the AppImage or degrading to a windowed status. Wild: it also covers T-0418 and T-0335.
  Done when: T-0325 closes with the tray working on a machine that lacks the system package, with no command handed to the user.

- **Wild: Show which model wrote each hunk (model-tinted blame)** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: with haiku and sonnet lanes (T-0755), the user needs to see where cheap hands wrote code and whether those hunks survived review. Assumption: the model can be stamped per lane and mapped to hunks via the existing step attribution.
  Done when: `fm blame <file>` colours lines by model and effort, and the pane shows the share of surviving lines per model.

- **Wild: Rewind by sentence ("undo the part where you…")** — FEATURE — value 3 — effort L — risk med — category: control
  Why: the user steers in plain words, and the pack shows frequent corrections. Foreman has step-scoped revert, but nothing maps a phrase to a step. Assumption: a cheap model can match the phrase to ledger steps with a confidence score. It asks only below 0.7.
  Done when: the phrase "undo the part where you renamed the config key" reverts that step's hunks and moves the pointer back, and a wrong match is itself undoable.

- **Wild: Fire a two-second "what will you do with this?" card on every captured message** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the captured items T-0755 to T-0760 sat unacknowledged while the user suspected idleness. Assumption: a one-line reply with class, queue slot and model tier, and a way to bump it, gives certainty without interrupting the work.
  Done when: every captured message yields an acknowledgment line within one hook turn, and a bump to the front changes the queue order visibly.
