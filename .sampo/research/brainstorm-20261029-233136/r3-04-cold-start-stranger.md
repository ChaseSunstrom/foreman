# Brainstorm — lens: cold-start stranger

- **Backtest the cold start on the stranger's own history** — FEATURE — value 5 — effort L — risk med — category: calibration
  Why: wild. The pack scores gen-0 only by later user corrections, which arrive slowly. Check out the commit from about 200 commits back, run the cold start there, and compare its gap map with what maintainers actually built next. The git log supplies free ground truth.
  Done when: `fm genesis backtest <repo> --back 200` prints the share of the later-landed capability areas that the old-snapshot gap map named, and the number is stored with the gen-0.

- **Classify the user's history as portable or project-bound** — FEATURE — value 5 — effort M — risk low — category: transfer
  Why: assumption: "draws on the user's history and corrections" will leak project-specific steers (e.g. "update the site page") into a repo that has no site. Tag each steer as universal (e.g. "never skip tests"), stack-bound or project-bound before it can seed a MUST in a stranger.
  Done when: on a fixture stranger with no web surface, no gen-0 MUST derived from a project-bound steer appears, and each carried steer lists its tag.

- **Treat CI config as the declared gate list** — FEATURE — value 4 — effort S — risk low — category: recon
  Why: assumption: running gates to discover them (already proposed) is slow and unsafe, while `.github/workflows`, Makefile targets, `tox.ini` and `package.json` scripts already state the project's own bar. Parse them first, then verify each with a bounded run.
  Done when: on three fixtures with CI files, the gen-0 gate section matches the CI commands exactly, and any command it could not run is marked unverified.

- **Import the stranger's existing agent rules with precedence** — FEATURE — value 4 — effort M — risk med — category: rules
  Why: assumption: a repo may already carry CLAUDE.md, AGENTS.md or .cursorrules. Treating them only as data (injection defense) discards legitimate local rules. Import them as sourced MUSTs, flag conflicts with Foreman's core rules, and never let them override the guard.
  Done when: a fixture whose AGENTS.md says "always commit directly to main" produces a flagged conflict line and no weakening of guard behavior, while its test-command rule is kept as a MUST.

- **Fence generated and vendored code out of the exam** — FIX — value 4 — effort S — risk low — category: exam safety
  Why: assumption: a stranger repo has `vendor/`, `node_modules/`, lockfiles, protobuf output and minified bundles. Planted gaps or coverage cells there are unfixable noise that wastes generations.
  Done when: on a fixture with vendored and generated dirs, `fm exam gen` plants no scenario in them, and the skipped paths are listed with the reason (from .gitignore, a header such as "DO NOT EDIT", or a path rule).

- **Size the exam by measured gate latency** — PERFORMANCE — value 4 — effort S — risk low — category: planning
  Why: assumption: a stranger's suite may take 40 minutes or 4 seconds, and a fixed 9-scenario minimum behaves very differently in each case. Time one gate run first, then choose scenario count, repeats and parallelism from it.
  Done when: the gen-0 plan prints the measured gate seconds and the scenario count it chose; a slow-suite fixture gets a documented reduced plan and not a timeout.

- **Gate outward actions on detected ownership** — SECURITY — value 5 — effort S — risk low — category: authority
  Why: a standing publish grant exists for Foreman's own repo (T-2090). On a stranger, remotes, commit authors and org names may show it is someone else's repository. Compare the remote owner and the commit authors with the user's identities, and when unsure disable push, publish and PR actions for that tower.
  Done when: on a fixture cloned from a third-party remote, `fm genesis live on` refuses and explains why, and on a repo with the user's own remote it proceeds.

- **Mine the repo's self-reported debt as gap evidence** — FEATURE — value 4 — effort M — risk low — category: gap map
  Why: assumption: a cold-start gap map with no tasks and no history has nothing to count. TODO and FIXME comments, skipped or xfail tests, CHANGELOG "known issues" and docs/roadmap files are free local evidence. Cluster them into coverage-grid cells, each citing file:line.
  Done when: on a fixture with 12 planted TODOs and 2 skipped tests, the gap map cites at least 10 of those 14 by path, and cells with no such evidence are marked "no evidence", not guessed.

- **Adopt the project's own vocabulary** — FEATURE — value 3 — effort S — risk low — category: gen-0 quality
  Why: assumption: a gen-0 written in generic words ("module", "service") misreads a repo that says "lane", "crate" or "cartridge". Extract a glossary of the top terms from README, headings and identifiers, and require MUSTs and exam scenarios to use them.
  Done when: on a fixture with a distinctive vocabulary, at least 80% of the glossary's top 10 terms appear in the gen-0, and a tool-less reader can name the project's main nouns from the gen-0 alone.

- **Handle docs in another language** — FIX — value 3 — effort S — risk low — category: robustness
  Why: assumption: a stranger's README and comments may be in Japanese, German or Portuguese. Detect that, keep quotes in the source language, write the gen-0 in the user's language, and mark translated MUSTs as such.
  Done when: a fixture with a Japanese README yields a gen-0 whose MUSTs cite the original lines and carry a "translated" tag, with no empty sections.

- **Smoke-tour the running product in a sandbox** — FEATURE — value 4 — effort L — risk high — category: recon
  Why: assumption: README, tests and CI say what the project claims, but only running it shows what it does. Start the entry point in a network-off sandbox with a time limit, capture its output and exit codes, and use the observed behavior as spec evidence.
  Done when: on a fixture CLI, the spec includes at least 3 observed command behaviors with captured output; the run is killed at the limit, and nothing outside the sandbox directory changes.

- **Record the first ten minutes as a replayable stranger tape** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: wild. The first ten minutes are where cold-start errors begin, and the user can't see them. Keep a timestamped tape of every file read, command run and guess made, scrubbable on the tower page, so "why did it think this was a Django app?" has an answer.
  Done when: `fm genesis tape` lists the reads and commands in order, and clicking any gen-0 line on the page jumps to the tape step that produced it.

- **Borrow exam seeds from the stranger's dependencies** — FEATURE — value 3 — effort M — risk med — category: exam
  Why: wild. A fresh repo has no failure history, but its dependencies' own test suites and changelogs hold known edge cases, especially for parsers, HTTP and dates. Mine locally installed packages only (nothing fetched) for 3 edge-case seeds to be turned into held-out scenarios.
  Done when: on a fixture using a date library, at least one generated scenario traces to an edge case in the installed library's tests, with its source path recorded, and no network call is made.

- **Abstain when the project kind is unclear** — FEATURE — value 4 — effort S — risk low — category: classification
  Why: assumption: the cold start picks exam kinds and capability expectations from a guessed project kind, and a wrong guess (a game engine treated as a web app) poisons everything after it. Output a ranked kind guess with a confidence, and below a threshold use only the kind-neutral scenarios and ask the single skippable card.
  Done when: on an ambiguous fixture (a monorepo mixing a game client and a server), the gen-0 shows two ranked kinds, uses only the neutral exam kinds, and does not claim a single kind.

Next question: What does the cold start do when the "stranger" is a fork or clone of a project the user already has a mature tower for, and should it inherit from that tower or deliberately start blind?
Next question: How long should a cold-start tower stay in "probation" before its self-written MUSTs get the same weight as hand-written ones, and what observable counts as passing probation?
