# Brainstorm — lens: user value

- **Show the user's sentence as concrete before/after examples to confirm** — FEATURE — value 5 — effort M — risk low — category: intent
  Why: the request lists "does it do what the user meant" as the hardest case to verify. The steers show the user correcting readings after the fact (T-2583's "8+ characters" versus its own 7-character example).
  Done when: `fm task new` on an ambiguous ask prints 2–3 concrete input→output examples. One-word picks are stored as the task's acceptance examples, and `fm task finish` runs them or marks them unproven.

- **Keep an unproven register with the cheapest next probe** — FEATURE — value 5 — effort M — risk low — category: honesty
  Why: the request says what can't be proven gets labelled unproven. A label alone decays. Assumption: today it's prose in a receipt, not a queryable object.
  Done when: `fm unproven` lists every unproven claim across tasks with its age, the cheapest probe that would settle it, and who must act. Closing a task with an unlabelled claim is refused.

- **Use one proof-strength badge everywhere** — FEATURE — value 4 — effort S — risk low — category: ux
  Why: the request spans UI, data, docs, infra and perf, each with its own vocabulary. Assumption: `fm shot`, `fm flow` and the other provers each phrase their verdicts differently.
  Done when: every prover emits one of claimed / ran / observed / reproduced / unproven. The status line, `fm status` and the finish card show the same one-character badge, and a test fails if a prover emits a verdict outside the set.

- **Check docs for drift in flags, defaults and env vars** — FEATURE — value 4 — effort M — risk med — category: docs
  Why: the request names "docs against code", and the pack's recent commits show that doc claims drift. Command blocks can be run, but a quoted default or flag name is never executed.
  Done when: `fm docs prove` extracts flags, defaults, env vars and verb names from README/MASTER.md. It diffs them against argparse and code constants, and a planted wrong default is reported with file:line on both sides.

- **Give `fm shot` region contracts instead of whole-page pixel diffs** — FEATURE — value 4 — effort M — risk med — category: ui
  Why: the request names UI proof, and the pack notes the pane's #262626 background differing from the design (T-1217). Whole-page diffs flake, so users learn to ignore them.
  Done when: a task can declare "this region/element must contain X, be visible, and have contrast ≥ 4.5". `fm shot` asserts those through the DOM or accessibility tree, and an unrelated pixel change doesn't fail it.

- **Replay each flow under hostile conditions** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: a flow that passes at 1280px with a fast network and a mouse says little about what real users hit. Assumption: `fm flow` currently runs one condition.
  Done when: `fm flow --matrix` replays a recorded flow at a narrow viewport, throttled network and keyboard-only. The result is a per-condition pass/fail table, and an untried condition is listed as unproven.

- **Prove data changes with invariants and an eyeball sample** — FEATURE — value 4 — effort M — risk med — category: data
  Why: the request lists "data". Passing unit tests rarely show what a migration did to real rows.
  Done when: `fm data prove` snapshots row counts, null rates and declared invariants before and after a change. It prints 5 changed rows side by side for the user, and any invariant it couldn't evaluate is labelled unproven.

- **Label how far an infra change got up a proof ladder** — FEATURE — value 4 — effort M — risk low — category: ops
  Why: the request lists "infra and ops", where a change usually can't be fully proven locally. Saying "rung 3 of 5 reached" is more useful than a single pass.
  Done when: the infra prover reports the highest rung actually run (lint → plan/dry-run → local emulation → staging → live) and names the next rung and what it needs. The finish card shows that rung.

- **Declare a noise floor in every performance claim** — PERFORMANCE — value 3 — effort S — risk low — category: perf
  Why: the request lists "performance". T-2605 shows noisy benches already caused a flake, and the pack lists "inconclusive under noise" as a need.
  Done when: `fm perf prove` runs N interleaved before/after trials and prints the median delta with its spread. A delta inside the spread reads "inconclusive", not "faster".

- **Ship a red fixture with every prover** — CLEAN — value 4 — effort M — risk low — category: reliability
  Why: assumption: a prover that can't fail would look the same as one that works. The pack's steers already require planted violations for checks.
  Done when: `fm doctor` runs each prover (`shot`, `flow`, `docs`, `data`, `perf`) against a planted-broken fixture and goes red if any returns "proven".

- **Wild: let the user witness a claim from their phone** — FEATURE — value 3 — effort M — risk med — category: human-witness
  Why: wild. Some things (a real device, a real email arriving) only the user can see. A tap-to-confirm page on the local web UI records "human-observed" with a timestamp, so it's labelled differently from machine proof.
  Done when: an unproven item with a witness step shows a tap page. A tap moves it to human-observed with the time, and no tap leaves it unproven.

- **Wild: have a cold agent attempt the user's sentence on the running product** — FEATURE — value 4 — effort L — risk med — category: intent
  Why: wild. Instead of testing what we built, try what the user asked. An agent sees only the user's verbatim sentence and the running UI, and reports where it got stuck. Assumption: a browser-driving child is available.
  Done when: `fm meant` runs the attempt and outputs a stuck-point list. A planted missing button is found, and a task with no runnable surface reports unproven.

- **Wild: attach a short replay clip of the passing flow to each finish receipt** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. A 10-second filmstrip of the flow the user cares about is easier to believe than a log line. It also gives a stale-proof check something to compare against next time.
  Done when: `fm task finish` on a UI task writes a filmstrip SVG next to the receipt and links it from the card.

- **Wild: let the user see proof coverage as a map of the repo** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: wild. A heat map in the web UI colours each area by its newest proof strength and age. It shows at a glance where "done" rests on nothing.
  Done when: the web UI page shows per-directory proof badges, and an area changed after its last proof turns grey.

Next question: Which verification claims has the user actually re-checked by hand after a "done", and which prover would have caught each one?
Next question: Which surfaces can Foreman never observe itself (real devices, production, third-party services), and what is the cheapest human witness for each?
