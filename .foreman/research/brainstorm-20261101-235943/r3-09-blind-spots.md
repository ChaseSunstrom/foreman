# Brainstorm — lens: blind spots

The blind-spot lens on the eight missed asks (T-2532 to T-2547). For each class I name the question a brainstorm should have asked, ask it of the whole project, and list what that surfaces. The ideas below skip anything already in the "so far" list.

- **Fuzz every verb with empty, bare and lookalike arguments** — FIX — value 4 — effort M — risk low — category: reliability
  Why: The class is "which empty or default input is silently reinterpreted?" T-2527 read an empty `--commit` as HEAD, and T-2540 took two bare words as one add plus a dropped word. Nobody swept the other verbs for the same behaviour.
  Done when: a test runs each `fm` verb's flags with `""`, `" "`, `-` and doubled words, and every case either refuses with a named reason or provably acts as documented.

- **Audit every `hash % len` selection for instability** — CLEAN — value 3 — effort S — risk low — category: exam
  Why: Question: "what assignments shift when a list grows?" Adding a fifth BEYOND row would reassign most existing items (`_beyond` uses `hash % len`), and the exam has no item versioning. Other pickers, such as lens choice or scenario draw, may do the same.
  Done when: a lint finds every modulo-over-a-growing-list pick and each is either versioned, switched to rendezvous hashing, or listed with a reason it is stable.

- **Flag every flipped assertion at task finish** — FEATURE — value 4 — effort M — risk low — category: tests
  Why: Question: "which tests encode the old behaviour as truth?" T-2507's test had a last assertion that "encoded the re-offer", and it only surfaced in a steer. A flipped assertion is the signature of a changed contract.
  Done when: `fm task finish` lists assertions edited or removed in the diff, and refuses a non-test task whose flipped assertions have no one-line reason in the plan.

- **Count-parity lint for every generated list artifact** — CLEAN — value 4 — effort S — risk low — category: tower
  Why: Question: "what N-of-A equals N-of-B invariants do generated files have that no lint checks?" T-2547 caught briefs versus grounding lines only after the fact. Plans, coverage rows and exam items likely share the shape.
  Done when: `fm genesis check` runs one table of paired counts (briefs/grounding, steps/criteria, cells/probes) and goes red on any mismatch, with a test per pair.

- **Inventory the host's hook events against what Foreman handles** — SECURITY — value 4 — effort M — risk med — category: hooks
  Why: Question: "which events can the host emit that no fallback covers?" T-2532 fixed five named events only. PreCompact, SubagentStop and failure events may exist unhandled on Claude Code, Gemini and opencode.
  Done when: `fm doctor` diffs the host's documented event list against the registered handlers, and an unhandled event is a WARN naming its harness.

- **Fingerprint the environment on every gate flip** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: Question: "what differs between where the gate passed and where it failed?" T-2529 (setuptools) and T-2543 (ETXTBSY) were environment-dependent, and one dropped task shows 1 in 22 baselines was interpreter-specific.
  Done when: each gate result stores python version, setuptools presence and load, and a pass-then-fail flip prints the first differing fingerprint field.

- **Sweep steers and decisions for dangling references** — CLEAN — value 3 — effort S — risk low — category: steers
  Why: Question: "which standing rules point at things that have since changed?" Steers name T-2450, T-2444 and T-2462 as waiting, and a closed or dropped task leaves the rule firing on nothing.
  Done when: the sweep resolves every T-id, verb and flag a steer or decision cites, and names each steer whose target is closed, dropped or missing.

- **Audit persistent keys for state aliasing** — FIX — value 3 — effort M — risk med — category: state
  Why: Question: "which store keys merge distinct lifecycle states?" The session memory keyed on the id alone conflated a captured task's plan with its later draft until it moved to `id:status`.
  Done when: a test enumerates each persistent map's key shape and checks that two states of one entity never collide, with failures listed by file.

- **Wild: Typo-twin verbs.** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Generate near-miss argv for each verb by edit distance and synonym (`remove/delete/del`, as in T-2540). Check each refuses clearly or maps to the intended action, never to a different one.
  Done when: a generated corpus of at least 200 near-miss commands passes, and each failure files a vote under the unknown-verb ledger.

- **Wild: Opposite-day gate.** — PERFORMANCE — value 3 — effort M — risk low — category: reliability
  Why: wild. Once a week, run the suite with shuffled order, a skewed clock, an odd locale and an older Python, to catch gate flakes before a push does.
  Done when: a scheduled `fm night` job reports any test that changes verdict, with the perturbation that did it.

- **Wild: Obituary cards for dead steers.** — FEATURE — value 2 — effort S — risk low — category: steers
  Why: wild. When a dangling-reference sweep finds a steer with no live target, it drafts a one-line obituary. The user or a decision retires it with one word, and the reason lands in the final report.
  Done when: a seeded stale steer yields a card, and answering it removes the steer and its check.

- **Show the user what the guard saw but did not ask about** — FEATURE — value 3 — effort M — risk low — category: user value
  Why: assumption: silent fallbacks (T-2532, T-2542) were found by the user, not by Foreman. A "quiet events" digest in the web UI would give them a place to look before they have to ask.
  Done when: the web UI lists the last 24 hours of fallbacks, expired grants and skipped checks, each with a source and a count.

Next question: Which verbs take free text where a flag was meant, and what does each do with a bare word that is also a flag name?
Next question: Which of the eight missed asks were found by the user reading output, not by any check, and what do those reading habits tell us to show first?
