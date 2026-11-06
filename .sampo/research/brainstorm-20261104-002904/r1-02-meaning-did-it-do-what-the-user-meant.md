# Brainstorm — lens: meaning: did it do what the user meant

- **Compile spec examples into criteria at plan time** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: the mission names meaning as the largest unproven class (599). Examples in an ask ("`sampo louhi models` prints…", "the scene shows 'the orchestrator'") are the user's own acceptance tests, and today they are prose.
  Done when: filing a task whose text holds 3 quoted examples yields 3 criterion rows, each marked `runnable`, `needs-eyes` or `unprovable` with a reason, and `fm task finish` lists any row with no result.

- **Turn each pushback into a regression probe on the spot** — FEATURE — value 5 — effort M — risk med — category: steers
  Why: "dont showcase it as jarvis", "don't say it's you", "stop asking me for stuff". Each was a negation the user had to say after the fact. Steers already have `--check`, but the check is hand-authored.
  Done when: a message containing a negation about output ("don't show X") creates a stored check (a forbidden-string scan over the named surface) within the same session, and a planted "jarvis" in `site/` fails it.

- **Lint public surfaces for role words, not vendor or host names** — SECURITY — value 5 — effort S — risk low — category: public surfaces
  Why: the mission requires "models by role, orchestrator as any agent". The user corrected this twice (jarvis, Claude as orchestrator). Surfaces include README, `site/`, `demo/*.svg`, `design/` and the generated genesis data.
  Done when: `fm doctor` scans those paths against a role vocabulary (planner, router, embedder, generator, orchestrator) and a denylist (endpoint profile names, home paths, vendor model ids outside an allowlisted compatibility table). The check fails on 3 planted terms and passes on main.

- **Make numbers in docs computed, not typed** — FIX — value 4 — effort M — risk low — category: docs
  Why: 421 docs flag claims no run has checked. README carries counts such as files, tests and stats that rot.
  Done when: a doc number can be written as `{{fm: cmd}}`, the renderer fills it from a real run, and a stale or failing command turns it into a hatched "unproven" mark instead of a number.

- **Stamp doc claims with the run that checked them and the files they cite** — FEATURE — value 4 — effort L — risk med — category: docs
  Why: "claims no run has checked" is a count, but the claims aren't individually addressable. Without a stamp, "unproven" can't shrink.
  Done when: each claim in MASTER.md has `verified: <run id> @ <sha>` plus a cited-path hash, and editing a cited file flips the claim to unproven in `fm doctor`'s count.

- **Resolve every proper noun in an ask before building** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: "jeff", then "jev", then "JEPA-style" took three rounds. T-2887 had to research what Jev is. Unresolved names get silently guessed.
  Done when: intake extracts capitalised or odd tokens, greps the repo and catalogue, and for each miss files a "what is X" research step and records the guess. The finish card prints `read 'jev' as: <guess> (source: …)` for every guessed name.

- **Show an unproven shelf grouped by reason** — FEATURE — value 4 — effort S — risk low — category: reporting
  Why: the mission wants whatever can't be proven labelled unproven. A single count hides which kind (taste, needs a live host, needs a second model, needs the user's machine).
  Done when: `fm next` and the finish card print `unproven: 3 taste, 1 live-host` with the one command or key that settles each group.

- **Sweep universal words as repo-wide checks** — FEATURE — value 4 — effort M — risk med — category: scope
  Why: "everywhere", "any", "never show" were each satisfied in one file while others stayed wrong, such as the scene versus the README versus the site data. Genesis data is generated and easy to miss.
  Done when: an ask containing a universal quantifier files a sweep criterion over all tracked and generated files, and a planted violation in a generated JSON file is caught.

- **Wild: have a user-proxy child answer yes or no to each example from the artifact alone** — FEATURE — value 3 — effort M — risk med — category: acceptance
  Why: assumption: a tool-less child given only the user's words and the rendered output judges meaning more independently than the builder. It must quote the line that decides each example.
  Done when: for 5 closed tasks with known later user corrections, the proxy fails at least 3 of the example rows that the user later corrected.

- **Wild: read a rendered screenshot cold and say what the product is** — FEATURE — value 3 — effort M — risk med — category: public surfaces
  Why: scenes are SVG and animation, and text lint can't see what a viewer infers (does it look like one vendor's product?). A vision child gets only the screenshot.
  Done when: the landing page and README header are rendered headless, a cold child lists the agents and models it believes are shown, and the check fails if a vendor or host name appears that isn't in the role vocabulary.

- **Wild: run a "wrong-but-green" game on each plan** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: assumption: if a cold child can write a trivial change that passes every criterion yet breaks the example's intent, the criteria are weak. This is separate from the existing lazy-satisfy idea because it targets example-derived criteria.
  Done when: a criterion set where the child's decoy passes is marked weak at plan time, and the builder gets one added criterion before starting.

- **Print "what I took you to mean" as a diff against the user's next message** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: assumption: the next user message is the cheapest meaning signal Foreman doesn't author. A correction starting with "no," or "I meant" is a miss.
  Done when: a message beginning "no," or "I meant" after a close is stored against that task as a meaning miss, with its sentence quoted, and `fm outcomes` reports meaning misses per week.

Next question: Which of the 599 unproven meaning items could a runnable example have settled, versus the ones that only the user's eye can settle?
Next question: When a role-name lint blocks a public line, who owns the allowlist: the user, or the cold reviewer, and what keeps the allowlist from growing?
