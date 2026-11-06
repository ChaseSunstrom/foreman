# Brainstorm — lens: docs against code

- **Compile spec examples into runnable criteria at plan time** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: the request names meaning as the largest unproven class (599) and wants spec example assertions turned into runnable criteria. Assumption: MASTER.md and the skills hold fenced examples with an expected output next to them.
  Done when: planning a task whose doc cites `fm X` with an expected output yields a criteria block, and running it against a planted-wrong implementation fails.

- **Keep a claims table with cited-file hashes** — FEATURE — value 5 — effort M — risk low — category: docs ledger
  Why: 421 docs flag claims no run has checked. A table of claim id, cited paths, their hash and the last checking run turns "unchecked" into a number. Assumption: claims can be pulled out by sentence plus a backtick path.
  Done when: editing a cited file makes `sampo doctor` list the claims whose stamp is now stale.

- **Lint public surfaces for role words, not vendor or machine names** — SECURITY — value 5 — effort S — risk low — category: public text
  Why: the request says public surfaces must name models by role and the orchestrator as any agent. The user pushed back on "jarvis" and on naming Claude in the scene. Assumption: README, site/, design/ SVG text and genesis data are the surfaces.
  Done when: the ship gate fails on a planted "jarvis" or "Claude as orchestrator" in site/index.html, README.md or an SVG `<text>` node, and passes on the clean tree.

- **Render model roles from one role table** — CLEAN — value 4 — effort M — risk low — category: public text
  Why: hand-typed names caused the pushback; the lint only detects them. A table of role to display name that the site, README and scenes read prevents them. Assumption: the animated-scene task (T-2888) hand-types its labels.
  Done when: grepping site/ and README for model names finds none outside the role table's generator input.

- **Template doc numbers from the commands that produce them** — FIX — value 4 — effort M — risk low — category: docs drift
  Why: the README states counts ("2358 files", skill totals, stats) that drift. Assumption: some are typed by hand.
  Done when: a number in README or site changes only via a generated block, and a test fails when a typed copy disagrees with its probe.

- **Hatch every unproven doc claim with a typed reason** — FEATURE — value 4 — effort M — risk low — category: labelling
  Why: "whatever can't be proven is labelled unproven". Reasons would be: needs host, needs a network, needs a model, subjective, stale. Assumption: the web UI can show reasons as grouped shelves.
  Done when: the unproven count prints per reason, and no unchecked claim lacks a reason.

- **Run the quickstart in a scratch home under a docs-only child** — FEATURE — value 4 — effort M — risk med — category: onboarding proof
  Why: install.sh and fm doctor claims are checked only by their own tests. A tool-less newcomer child following the README, scored on what it had to guess, tests the prose rather than the code. Assumption: a scratch-home mode exists, per the drill verbs.
  Done when: a run emits a list of README steps whose command failed or needed a guess, and a planted wrong flag in the README is found.

- **Mutate doc claims to find ones nothing guards** — FEATURE — value 4 — effort M — risk low — category: docs against code
  Why: a claim whose change leaves every test green is unguarded. Assumption: each claim maps to a file or verb that can be mutated in a scratch copy.
  Done when: flipping a documented default in a scratch copy turns at least one check red, or the claim is labelled unguarded.

- **Flag code surface no doc mentions** — FEATURE — value 3 — effort S — risk low — category: docs coverage
  Why: the reverse direction of the 421 flagged claims. Verbs without a MASTER.md anchor are invisible to a newcomer. Assumption: the verb table is machine-readable.
  Done when: a command lists verbs, flags and env vars with no doc mention, and the list is empty or each entry is waived.

- **Verify CHANGELOG lines against commits and proof links** — FIX — value 3 — effort S — risk low — category: release truth
  Why: each push is gated and the CHANGELOG ships with it. Assumption: entries cite task ids.
  Done when: a CHANGELOG line whose task id has no closing commit or proof prints as unproven.

- **Wild: Open any claim to a replayable "show me" panel** — FEATURE — value 4 — effort L — risk med — category: trust (wild)
  Why: every claim in the docs gets a button that re-runs its probe in a sandbox and shows the output. Assumption: the claims table above exists.
  Done when: clicking a claim on the site's docs page shows output from a run less than a day old, or "unproven" with a reason.

- **Wild: Have a cold child guess who the orchestrator is from the rendered site** — FEATURE — value 3 — effort S — risk low — category: leak test (wild)
  Why: a lint catches known strings; a reader catches the implied ones the user kept spotting. Assumption: a tool-less child can read a text-extracted page.
  Done when: the child, given the site's text and SVG labels, answers "can't tell" about vendor, host and machine, and a planted hint makes it answer otherwise.

- **Wild: Age proof stamps by the commits that touch their cited files** — FEATURE — value 3 — effort M — risk low — category: trust decay (wild)
  Why: a stamp from last week on a file rewritten daily means less. Assumption: the claims table records cited paths.
  Done when: the proven badge dims in proportion to the churn since its run, and a quiet file keeps its full badge.

Next question: which of the 421 flagged claims are about behaviour a run can check in under a second, and which can only be checked by a user?
Next question: do the 599 meaning-class gaps cluster on a few verbs, so that one criteria compiler would clear most of them?
