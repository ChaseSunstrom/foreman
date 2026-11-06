# Brainstorm — lens: public surfaces honest

- **Lint every public surface for forbidden names** — SECURITY — value 5 — effort S — risk low — category: honesty
  Why: the user had to say "don't showcase it as jarvis" and "don't name Claude as the orchestrator". `demo/live.svg` and the README still name "Claude Code 2.1.301".
  Done when: a check over README, site/, demo/*.svg and the genesis data fails on a planted profile name, hostname, `/home/<user>` path or vendor model name used as the orchestrator, and passes on main.

- **Keep one role vocabulary and render public text through it** — CLEAN — value 4 — effort M — risk low — category: naming
  Why: the roles (orchestrator, planner, judge, decision model, embedder, reranker, generator) are described ad hoc, and the profile names (jarvis, qwen3.x) leak from config into scenes.
  Done when: a single `roles` table maps every local profile to a role, and the site and README scene builders can only emit role strings. A test shows an unmapped profile makes the build fail.

- **Extract spec example assertions into runnable criteria at plan time** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: the request says meaning is the largest unproven class (599) and spec examples should become criteria. Assumption: examples are fenced blocks shaped like "`cmd` → output".
  Done when: `sampo plan` on a spec with 3 examples writes 3 criteria into the task's Done-when, and a failing example turns the task red.

- **Stamp every doc claim with its last checking run, or hatch it as unproven** — FEATURE — value 5 — effort M — risk med — category: docs
  Why: 421 docs make claims no run has checked. The ideas so far have the hatched glyph but no per-claim stamp.
  Done when: MASTER.md and the site show `checked <run-id> @ <commit>` or a hatched "unproven" per claim, and the count matches `sampo doctor`.

- **Scrub the genesis and site data at publish, with a planted canary** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: `fm genesis live` publishes to main automatically (standing rule), and the data can carry endpoint URLs, home paths and steer text.
  Done when: a canary hostname and path in a fixture ledger never appear in the published JSON, and the publish aborts naming the field if one does.

- **Extract text from SVGs and rendered scenes and lint it like prose** — FIX — value 4 — effort S — risk low — category: honesty
  Why: the demo and animated scenes are images, so a text grep over source files misses names baked into them.
  Done when: the lint reads `<text>` nodes from every SVG in demo/ and site/ and flags the same forbidden names as the prose lint.

- **Bind each number on the site to a data path and a run** — FEATURE — value 4 — effort M — risk low — category: honesty
  Why: the site shows real stats and model bench numbers, and nothing shows that they stay tied to a measurement.
  Done when: a literal number in site HTML fails the build unless it is rendered from `site/data` carrying `n`, the arm and the measurement date.

- **Label bench results by role, size class and arm, never by endpoint** — FEATURE — value 3 — effort S — risk low — category: models
  Why: the Models section is about to publish numbers, and the user said any orchestrator must work.
  Done when: every row reads "decision model, small, with-Sampo vs without, n=…", and no profile or vendor name appears.

- **Require a proof link on every CHANGELOG line, or print it as unproven** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: a lot of commits ship under the push grant, and changelog claims such as "fixed" are self-reported.
  Done when: each entry links a test or run id, and lines without one render with an "unproven" tag in the release notes.

- **Wild: Run a blind leak reader over the public site** — SECURITY — value 4 — effort M — risk low — category: red-team — wild
  Why: assumption: a tool-less child that sees only the rendered site can say what the author's machine, vendor and orchestrator are, which is a stronger test than grep.
  Done when: the child's guesses are scored against the real values, and the build fails when it names any of them correctly.

- **Wild: Open any claim to a replayable "show me" panel** — FEATURE — value 4 — effort L — risk med — category: trust — wild
  Why: assumption: a reader who can rerun a claim's check in a scratch home trusts the site more than one reading a badge.
  Done when: clicking a claim shows the exact command, the stored output and a copyable one-line replay, and a changed output turns the badge hatched.

- **Wild: Make the orchestrator in every scene a rotating parameter** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: the user wants "any orchestrator", and a scene that cycles through generic agent glyphs shows this without naming a vendor.
  Done when: the README and site scene render at least 3 anonymous agent silhouettes and the lint finds no vendor name.

- **Wild: Age proof stamps by the commits that touch their cited files** — FEATURE — value 3 — effort M — risk med — category: verification — wild
  Why: a stale "checked" stamp is the same dishonesty as no stamp.
  Done when: editing a file a claim cites flips that claim's stamp to hatched in the next build, with no manual step.

- **Publish a retraction log of claims that were corrected** — FEATURE — value 2 — effort S — risk low — category: trust
  Why: assumption: showing past corrections makes the remaining "checked" labels more credible.
  Done when: the site lists each retracted claim with its date and the fix, generated from the stamp history.

Next question: Which public claims were true when written but have since drifted, and can the drift be found from git history alone?
Next question: Do the user's own asks to fix names ("jarvis", "Claude") show a general class of leaks, such as paths, hostnames, versions and model sizes, that no check covers yet?
