# Brainstorm — lens: self-improving harness

- **Score done-claims against what happened next** — FEATURE — value 5 — effort M — risk low — category: self-measurement
  Why: the pack plans scoreboards and per-task interventions, but nothing checks whether a "done" was true. Evidence: the user's repeated "still cluttered" and "why have you not improved" show escapes that Foreman never counted. It never learns which evidence grades the user ends up reopening.
  Done when: `fm improve --escapes` lists closed tasks followed within 7 days by a user ask or ledger event touching the same files, and shows the escape rate per evidence grade and per reviewer lens.

- **Synthesize a verb from repeated tool sequences** — FEATURE — value 5 — effort M — risk med — category: self-extension
  Why: assumption: ledger tool events let the n-grams of Bash/Read sequences be mined. Examples are the screenshot, harness and README re-record chain and the repeated gate runs. Nothing turns a recurring recipe into one command.
  Done when: after a recipe appears 3 times, `fm macro propose` writes a `fm do <name>` script with a fixture test that replays the recipe in a temp dir, and the macro is enabled only when that test passes.

- **Predict the user's follow-up and draft it** — FEATURE — value 4 — effort M — risk low — category: prediction
  Why: asks arrive in chains ("pane graph" → "node graph?" → "less empty"; cards → bulk cards; UI change → re-record README). Mining the order of asks per task type gives the likely next ask.
  Done when: on closing a task of a type with ≥3 historical follow-ups, the close-out names the top predicted follow-up and creates it as a draft task, and `fm digest` reports the predictor's hit rate.

- **Treat the user's frustration as a control signal** — FEATURE — value 4 — effort S — risk low — category: intent telemetry
  Why: phrases like "still cluttered", "why have you not", "reload" and repeated steers on one topic recur. UserPromptSubmit already sees every prompt. A tiny lexicon plus repeat-topic counter could tighten behaviour.
  Done when: a second complaint on the same topic within a session switches the task to strict mode (visual evidence required, no scope growth, one-line plan confirm). A test feeds recorded prompts and sees the mode flip and the strict-mode note injected.

- **Compile `--help` into a verified card** — FEATURE — value 4 — effort M — risk low — category: cards
  Why: only 6 of 1,084 cards ever fired, and the user asked for bulk cards for uncovered dependencies. Many are CLIs whose `--help` tree and man pages are ground truth, so no web docs are needed.
  Done when: `fm lib forge-cli <bin>` walks `--help` recursively, writes a card in the existing format, and runs each documented example flag with `--help`/dry-run to check it. A card with a failing example is not written.

- **Model-check Foreman's own state machine** — FIX — value 4 — effort M — risk low — category: reliability
  Why: the plan lists many concurrency items (CAS step advance, Stop re-entry, leases, torn writes) and each is tested one case at a time. A bounded explorer over the real reducer functions covers all orderings.
  Done when: `fm doctor --explore` enumerates all event sequences up to depth 6 (start, stop, compact, resume, close, crash) against invariants (one owner per task, a monotonic step pointer, no lost ledger line) and prints a shortest counterexample or "none".

- **Fuzz the guard with an obfuscation closure** — SECURITY — value 4 — effort M — risk low — category: provable safety
  Why: T-0275 shows the guard misses commands run through scripts. A generator that rewrites each dangerous seed (quoting, `${IFS}`, `base64|sh`, env indirection, `xargs`, aliases) shows what slips through.
  Done when: the test generates ≥500 variants per seed class, asserts 100% deny on the "never run" classes, and fails with the first uncaught variant printed.

- **Keep a calibration ledger for forecasts** — FEATURE — value 3 — effort M — risk low — category: delegation
  Why: this is a first, cheap version of the subagent market. Today the router uses pass rate only. Having each lane or lens declare cost, files touched and a pass probability before dispatch gives a Brier score per model and lens, and the reputation can reweight dispatch.
  Done when: each dispatch records a forecast, each close settles it, and `fm improve --calibration` shows a per-lens score. Dispatch prefers the better-calibrated lens on ties.

- **Bisect behaviour across Foreman versions** — FEATURE — value 3 — effort L — risk med — category: regression (wild)
  Why: when the weekly scoreboard drops, no one knows which Foreman change caused it. Bisecting gates exists, but not behaviour.
  Done when: `fm bisect-behaviour` runs a canary set of 5 scripted Haiku tasks across plugin git tags and prints the first tag where the pass rate drops beyond a variance floor.

- **Drive hermetic sessions with a synthetic user** — FEATURE — value 4 — effort L — risk med — category: self-evaluation (wild)
  Why: the user's steers and drops form a corpus of terse, ambiguous, impatient prompts, and the harness session once hijacked the queue. A Haiku persona seeded from those prompts could run overnight in the fenced harness and score results against the taste profile.
  Done when: `fm night --persona` runs N fenced sessions, never touches the real queue, and the morning receipt lists rubric violations with transcripts.

- **Run a cold-stranger usability test on Foreman itself** — FEATURE — value 3 — effort S — risk low — category: dogfooding (wild)
  Why: assumption: a fresh Haiku with only the README and `fm --help` will expose confusing verbs better than the maintainers do. 73 skills and many verbs are hard to navigate cold.
  Done when: `fm selftest-docs` gives the cold agent 5 common goals ("resume a stopped builder", "see what was learned") and files a task for each goal it cannot finish in ≤10 commands.

- **Hold a nightly rule tribunal** — FEATURE — value 3 — effort M — risk med — category: self-pruning (wild)
  Why: rules and hints accumulate and nothing reasons across them. A cheap judge reads recent ledger and steer text and rules on each rule: keep, merge with a named duplicate, or retire with the receipts.
  Done when: `fm tribunal` outputs verdicts that each cite ≥1 ledger line, and applying one is reversible via the changelog.
