# Brainstorm — lens: planted-defect exam: for each exam kind (bug, vuln, untested, dep, docs, flake, perf, none) the cheapest finder that would catch it in a never-seen repo in any of six languages

- **Rerun the repo's own suite in each language's strictest mode** — FEATURE — value 5 — effort S — risk low — category: bug/vuln finder
  Why: assumption: the exam's 0/108 means no finder ever executes anything. Existing tests under `python -X dev -W error`, `node --throw-deprecation`, `ruby -w`, `cargo test` with `RUSTFLAGS=-D warnings` or miri, `tsc --strict`, and `cc -fsanitize=address,undefined` surface crashes, UB and swallowed warnings with no model call. A new red is already a reproduction.
  Done when: on a fixture repo per language with one planted memory or type bug, the strict rerun goes red where the normal run is green, and a clean twin stays green in all six.

- **Match each dangerous sink to a canary payload** — FEATURE — value 5 — effort M — risk med — category: vuln
  Why: assumption: planted vulns are classic sinks. A table of six-language sinks (`eval`, `pickle.loads`, `YAML.load`, `Marshal.load`, `innerHTML`, `child_process.exec`, `system`, `strcpy`, `format!` into SQL) costs nothing to grep. One cheap model question asks only whether argv, HTTP or file input reaches the sink. The proof is a payload that creates a canary file.
  Done when: for each planted vuln in a fixture set, the payload creates the canary file, and a sink that is unreachable from input produces no finding.

- **Diff the manifest against what the code imports** — FEATURE — value 4 — effort S — risk low — category: dep finder
  Why: assumption: planted dep defects are declared-but-unused, imported-but-undeclared, or lock and manifest drift. Parsing `requirements`/`pyproject`, `package.json` and lock, `Gemfile.lock`, `Cargo.toml` and lock, and `#include` against the build file works offline for all six languages.
  Done when: three planted dep defects (unused, undeclared, drifted lock) are each reported with the line that proves it, and a clean repo reports none.

- **Stub out each function to prove it is untested** — FEATURE — value 4 — effort M — risk low — category: untested finder
  Why: assumption: the `untested` kind is a function nothing asserts on. In a scratch copy, replace the body with a raise or `abort`, run the suite, and if it stays green the function is untested. The generated test then fails on the stub and passes on the real body. This is a per-function probe, so it is cheaper and more exact than name matching or whole-suite mutation.
  Done when: the stub of a planted untested function leaves the suite green, the stub of a tested one turns it red, and the new test is red on the stub and green on the original.

- **Check backticked identifiers in the docs against the source** — FEATURE — value 4 — effort S — risk low — category: docs finder
  Why: assumption: planted docs defects name a flag, parameter or function that doesn't exist or was renamed. Extract every backticked token and `--flag` from README and docs, then grep the source for each one. A dangling name is a finding. Add a diff of `--help` output against the documented flags.
  Done when: a README mentioning a renamed function and a removed flag yields exactly those two findings, and a clean docs tree yields zero.

- **Find flakes by shrinking the CPU and isolating each test** — FEATURE — value 4 — effort M — risk med — category: flake finder
  Why: assumption: planted flakes are sleeps, unseeded random, set or hash ordering, shared temp paths and thread races. Grep the test files for those smells, then rerun only the matching tests 20 times: once alone, once in the suite, once pinned to one CPU with `taskset` under load, and once with a shuffled seed. A pass/fail split between those runs is the proof.
  Done when: a planted order-dependent test passes alone and fails in suite order, and a deterministic test never flips across 20 runs.

- **Prove perf with instruction counts, not wall time** — FEATURE — value 4 — effort M — risk med — category: perf finder
  Why: assumption: planted perf defects are quadratic loops, `in list` inside a loop, or concatenation in a loop. Wall-clock proofs are themselves flaky. Doubling the input and comparing `perf stat -e instructions:u`, `valgrind --tool=callgrind` or Python call counts gives a deterministic ratio, and a ratio near 4 for a doubled input is quadratic.
  Done when: a planted quadratic function gives a count ratio above 3.5 on three repeated runs, and its linear fixed version gives about 2.

- **Check encode/decode pairs for round-trips** — FEATURE — value 3 — effort S — risk low — category: bug finder
  Why: assumption: many planted bugs are lossy serialization, parsing or escaping. Pair functions by name (`dump`/`load`, `encode`/`decode`, `parse`/`format`, `escape`/`unescape`), then run random inputs through both in the repo's own language and compare. A mismatch is a ready-made failing test.
  Done when: a planted off-by-one in an `encode`/`decode` pair is caught with a minimal failing input, and a correct pair passes 1000 random inputs.

- **Skip model tiers when the free pre-screen is clean** — PERFORMANCE — value 3 — effort S — risk med — category: none verdict
  Why: Plain Claude spends about 0.17 USD per repo, and most never-seen repos in the `none` kind have nothing to find. If the strict rerun is green, the smell tables are empty and the manifest and docs diffs are clean, print a "none" receipt that lists those checks and stop. The risk is silent bugs, so bug-kind scoring decides whether this stays.
  Done when: on a clean fixture repo the model is called zero times, the receipt names each check run, and exam recall on `bug` does not drop versus the model arm.

- **Rank lines by idiom surprise before any model reads them** — FEATURE — value 4 — effort M — risk med — category: bug finder (wild)
  Why: wild; assumption: planted defects are mostly one-token edits (`<=` for `<`, `+1`, a swapped argument) that look odd against the repo's own style. Build token n-gram statistics over the repo with no tools beyond a script, rank lines by surprise, and show the model only the top 20. This works in all six languages and cuts tokens per repo.
  Done when: on a fixture set with planted one-token edits, a majority of planted lines rank in the top 20 surprise lines, and the model call receives at most 20 lines.

- **Run tests under a time-warped clock** — FEATURE — value 3 — effort M — risk med — category: flake finder (wild)
  Why: wild; assumption: `libfaketime` or an equivalent works under the repo's runtimes. Run the suite with the clock jumped forward, a fixed timezone, `sleep` shortened and a frozen `now`. Date, expiry and timeout flakes then show up in seconds across any language.
  Done when: a planted test that fails only after midnight UTC fails under the warped clock and passes under the real one.

- **Translate each missed defect pattern into the other five languages** — FEATURE — value 3 — effort M — risk med — category: probe growth (wild)
  Why: wild; assumption: the exam plants the same class of defect in python, js, ts, ruby, rust and c. A pattern that a probe misses in one language can be written once as a language-neutral rule (for example unchecked index, `==` on floats, unclosed handle) and expanded to the other five. Rerun the held-out exam afterwards to see whether recall rose.
  Done when: one missed pattern becomes five per-language probes and the held-out exam recall on that pattern's kind rises in at least three languages.

- **Gate the cheapest tier per kind by its measured recall** — CLEAN — value 3 — effort S — risk low — category: exam routing
  Why: the exam reports recall by kind and language, and the finders scored 0 of 108. A table (kind × language → tier, cost, recall) lets a tier that finds nothing be skipped. The unproven kinds fall through to the model arm.
  Done when: a run on a fixture repo logs which tier answered each kind, and a tier with zero recall over the last exam is not called.

Next question: Which exam kinds does plain Claude miss on its own, and is a deterministic tier worth running only for those?
Next question: How many of the 108 planted defects are one-token edits, and how many need cross-file reasoning, since that split decides which finder tier can ever work?
