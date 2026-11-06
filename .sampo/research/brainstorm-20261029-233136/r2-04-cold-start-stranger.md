# Brainstorm — lens: cold-start stranger

- **Land one proven win before building the tower** — FEATURE — value 5 — effort M — risk low — category: first-run
  Why: assumption: a stranger judges Genesis by the first ten minutes, and a full tower takes far longer. The cheapest verified gap (a failing test, a broken command, a dead link) is closed first, with `fm task prove` evidence, then the tower is offered.
  Done when: on a fixture stranger repo with one planted trivial defect, `fm genesis` closes it with recorded proof before any gen-0 text is written, and prints the time elapsed.

- **Discover the gates by running them** — FEATURE — value 5 — effort M — risk med — category: recon
  Why: assumption: a stranger has no `fm doctor` or `plugin/tests/run.py` equivalent. A gen-0 that guesses test and build commands is invalid. Try candidates from manifests (Makefile, package.json, pyproject, Cargo.toml) in a read-only worktree, record exit codes and timing, and keep only the commands that ran.
  Done when: on 6 fixture repos (one per supported language), the discovered gate list matches the hand-written key, and a repo with no runnable gate is reported as "no gate" rather than invented.

- **Preflight the machine's toolchain before planning an exam** — FIX — value 4 — effort S — risk low — category: environment
  Why: assumption: `fm exam gen` covers 6 languages, but the stranger's machine may lack cargo or a JDK. Today that would show up as every scenario failing, which reads as a project with huge gaps.
  Done when: with the toolchain removed from PATH on a Rust fixture, Genesis reports "cannot grade: cargo missing", writes no gap map, and plants no scenarios.

- **Redact the context pack before any child sees it** — SECURITY — value 5 — effort M — risk med — category: privacy
  Why: the brainstormers are fed a pack built from a repo Foreman has never seen. A stranger's `.env`, keys and private URLs would flow into a model call and into the published tower page (the auto-publish exists).
  Done when: a fixture repo with planted fake secrets in `.env`, README and git history yields a pack and a published `site/genesis` containing none of them, checked by a scanner test.

- **Scale recon to repo size with a map-first reading budget** — PERFORMANCE — value 4 — effort M — risk low — category: recon
  Why: this repo alone is 2006 files, and the pack gets only a trimmed map. A cold start on a 50k-file monorepo needs a rule for what to read: entrypoints, manifests, the largest churn and the most-imported files, with a token cap.
  Done when: on a generated 20k-file repo, recon finishes under a fixed token cap, and the written gen-0 names the same top-level modules a full read finds (≥90% overlap).

- **Split a multi-project repo into scoped towers** — FEATURE — value 4 — effort M — risk med — category: scope
  Why: assumption: strangers' repos are often monorepos (a web app plus a CLI plus docs). One gen-0 for all of them would produce a vague spec and a muddy exam.
  Done when: on a fixture with 3 packages, `fm genesis` proposes 3 scopes (or asks once), each with its own gen-0 and exam, and none of them touches another's files.

- **Fall back to a black-box exam for stacks the exam generator doesn't know** — FEATURE — value 4 — effort L — risk med — category: exam
  Why: the exam supports 6 languages. A stranger's project in Elixir or Zig would get no held-out exam, and "closes the planted gaps" would be unmeasurable. Scenarios would run the built binary or HTTP surface with hidden expected outputs.
  Done when: on an Elixir fixture, `fm exam gen` produces ≥9 black-box scenarios with ≥3 held out, and the oracle passes while the empty arm fails.

- **Mark unknowable grid cells "blind", not empty** — CLEAN — value 3 — effort S — risk low — category: coverage grid
  Why: the request demands a grid with no empty cells. A stranger with no CI, no deploy config or no users has cells Genesis can't see into. Forcing them full invents content. A "blind" state carries the cost to learn it.
  Done when: the grid renders blind cells with "to learn: <cheapest probe>", and lint fails on an empty cell that isn't marked blind.

- **Score each cold-start gen-0 by the corrections the user makes in week one** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: assumption: the cold start is Genesis's weakest moment, and today nothing measures it. Count edits, vetoes and "no, not that" steers against the inferred MUSTs and NEVERs, per project kind, and feed that back as the prior for the next stranger.
  Done when: after a simulated week of 5 corrections on a fixture, `fm genesis status` shows an inferred-item correction rate, and the next cold start on the same kind weights those items down.

- **Use two independent gen-0 writers and ask only where they disagree** — FEATURE — value 4 — effort M — risk low — category: question selection
  Why: the pack already settles on at most one skippable question, but doesn't say which question. The disagreements between two tool-less drafts are the real unknowns, which beats asking a generic one.
  Done when: on a fixture where the README contradicts the code, the single question card names that contradiction, and on a consistent fixture no question is asked.

- **Wild: Build a ghost-maintainer persona from past review comments** — FEATURE — value 3 — effort L — risk med — category: taste
  Why: wild. A stranger's git log, PR text and CONTRIBUTING encode what the maintainer rejects. A tool-less child plays that maintainer, and gen-0 NEVERs and rewrites are pre-reviewed by it before the user sees them.
  Done when: replaying 20 historical merged and rejected commits on a fixture, the persona's merge verdicts match the real ones on ≥70%.

- **Wild: Seal a day-zero prediction and grade it at 30 days** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild. At first run, Genesis commits (hashed, in the tower) to what it expects the project to need: top 5 gaps and likely first user asks. `fm outcomes` 30-day survival and the user's real asks later score the prediction. This is the only honest measure of cold-start quality.
  Done when: `fm genesis status` after a seeded 30-day replay prints hits and misses against the sealed list, and the seal's hash verifies.

- **Wild: Run Genesis on a folder that isn't code** — FEATURE — value 3 — effort M — risk med — category: kind detection
  Why: wild. "Nothing typed" could happen in a thesis folder, a dotfiles repo or a notes vault. A kind classifier with an abstain option picks a capability spec for prose, config or data instead of forcing a software spec onto them.
  Done when: on a markdown-only fixture, gen-0 contains no "tests pass" MUST, and its exam checks links, structure and consistency instead.

- **Time-box recon with a "stranger passport" the user can read in 20 seconds** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: assumption: the user will want to see what Genesis learned about their repo before trusting it. This is one screen listing kind, languages, discovered gates, scopes, blind cells and what was not read.
  Done when: `fm genesis passport` prints ≤25 lines on a fixture repo, and each line carries a source file path.

Next question: What does Genesis do when the stranger repo's own tests are flaky or red at baseline, so that "closes the gap" cannot be told apart from noise?
Next question: When the user later gives the same stranger a second project of the same kind, which cold-start inferences should transfer, and what proves they weren't just luck?
