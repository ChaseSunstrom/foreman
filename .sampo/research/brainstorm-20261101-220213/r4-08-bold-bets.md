# Brainstorm — lens: bold bets

- **Make the lean ratchet pay by deletion at ship** — FEATURE — value 5 — effort M — risk med — category: lean
  Why: gen-0 §6 says each generation removes at least what it adds; measured: 5 of 1219 stack cards used, SessionStart note ~2k chars x 89, 28 "Later from T-07xx" bundles open. Nothing enforces the subtraction at the moment a verb lands.
  Done when: `fm ship` on a task that adds a verb refuses unless the same task records a removed, merged or cold-shelved verb/card, and a test shows both the refusal and the pass.

- **Cold-shelve unused stack cards behind a lazy index** — PERFORMANCE — value 4 — effort M — risk low — category: context
  Why: `fm lib stats` shows 5 of 1219 cards used; the library inflates the repo (2098 files) and any listing.
  Done when: cards unused for 90 days move to a cold index, `fm lib show NAME` still loads one on demand, and the warm set count printed by `fm doctor` drops below 100.

- **Send the SessionStart note once as a hash plus delta** — PERFORMANCE — value 5 — effort M — risk med — category: context
  Why: the ~2k-char note is injected on 89 starts; average context per reply is 387k with no per-source breakdown.
  Done when: a second session start in an unchanged repo injects under 300 chars, and `fm cost` prints injected bytes per source for the last 100 replies.

- **Replace the brief guard's regex with a real shell tokenizer** — FIX — value 4 — effort S — risk low — category: guard
  Why: 2 brief-guard false positives read a dict key and a `.join(` call as written paths.
  Done when: both captured inputs pass, a corpus test of at least 50 real past briefs gives zero new blocks, and the old regex is deleted.

- **Fill the 61 coverage cells from re-runnable probes, not prose** — FEATURE — value 5 — effort L — risk med — category: coverage
  Why: the mission is those 61 cells, and the steer says a cell counts only if it names a concrete file or gap with no reused phrasing. Hand-written cells are the templating risk.
  Done when: each cell is generated from a probe's output (a path, a measured number or a recorded n/a with an expiry), a lint finds zero duplicate phrasing, and re-running the probes reproduces the file.

- **Print a guard parity matrix for every harness** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: Codex, Gemini and opencode have blocked tasks (T-0335 to T-0337) and Gemini's Stop isn't wired; "keeps the guard intact" is unproven off Claude Code.
  Done when: `fm doctor` lists each deny class (bypass-mode destructive, interpreter-driven fm, etc.) against each harness as enforced, advisory or absent, each backed by a test or an explicit "absent" with a reason.

- **Run the exam once with every optional hook off** — PERFORMANCE — value 4 — effort M — risk low — category: lean
  Why: the standing steer defers full exams, but a free-arm hooks-off run on the zero-token finders and oracle arms shows which weight earns nothing, which is the evidence T-2503's "pending" rows are waiting for.
  Done when: a report names each optional hook with its exam delta and bytes injected, and any with no delta files a subtraction task.

- **Show a guard block with the safe command to run instead** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: `core:interpreter-code-driving-foreman` blocked 42 times in 7 days, which says the model keeps retrying the same wrong thing.
  Done when: every block message for the top 5 rules names the exact replacement `fm` verb, and the 7-day repeat-block count for those rules falls in a later `fm friction` read.

- **Make hook latency a CI gate per event, tail included** — PERFORMANCE — value 4 — effort S — risk low — category: hooks
  Why: p95 is 278 ms over 13,533 runs but the tail is unreported, and `bench_hooks.py` is already a gate.
  Done when: the bench fails when any event's p99 exceeds a budget stored in one file, and `fm doctor` prints p50/p95/p99 per event.

- **Fuzz the guard against real shell parsing** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: a hand-written command parser is the classic bypass source, and bypass mode is the user's stated danger.
  Done when: a generator produces 10k shell-grammar commands, and every disagreement between the guard's verdict and a real `bash -n`/shlex parse of destructive intent is either fixed or listed in a known-gaps file with a test.

- **Wild: Lean twin — the same task with Foreman off and on** — FEATURE — value 4 — effort L — risk med — category: proof
  Why: wild; assumption: the only honest answer to "is it worth its weight" is a paired run, and replayed repo tasks already exist for the long-horizon tier.
  Done when: `fm twin TASK` replays one closed task on a scratch worktree with hooks off, then prints seconds, tokens and pass/fail beside the real run.

- **Wild: Plant a harmless forbidden command weekly to prove the guard is alive** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: wild; assumption: hooks fail open silently, and a guard that stopped firing would look identical to a quiet week.
  Done when: a nightly tick attempts a canary that must be blocked, and `fm doctor` goes red naming the surface if it isn't.

- **Wild: Guard playground on the site** — FEATURE — value 3 — effort M — risk med — category: site
  Why: wild; the site is a surface and trust in the guard is the product's central claim.
  Done when: a visitor pastes a command on the page and sees the verdict and rule from the real rule file compiled to a static bundle, with no server call.

- **Wild: One-file Foreman eject round trip** — CLEAN — value 3 — effort L — risk med — category: lean
  Why: wild; T-0794 lists eject and Lite mode as deferred, and "leave no trace" is the strongest leanness proof.
  Done when: install then eject on a scratch repo leaves a byte-identical tree apart from a listed receipt, tested in CI.

Next question: Which of the 61 empty cells are n/a by rule (a surface with no hooks) versus truly unbuilt, and who may accept an n/a?
Next question: What do cold-shelving and delta-injection cost a first-time user whose first session has no cache to lean on?
