# Brainstorm — lens: unspoken needs

- **Add `fm triage` as the one backlog entry point** — FEATURE — value 4 — effort S — risk low — category: backlog
  Why: Round 5 review: there are four ways to triage (first, swipe TTY, swipe --serve, app view `I`) and no entry that picks one. Assumption: terminal vs browser vs app can be inferred from `$SSH_TTY`, `$DISPLAY`, and whether the app is running.
  Done when: `fm triage` in a TTY, over ssh, and with the app open each lands on a different surface, with the choice printed and `--via` overriding it, covered by a test.

- **Re-sync a fetched ticket into its existing brief** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: T-1859 only reads Jira and Linear, and an upstream edit currently makes a second brief. The review also lists no GitHub issues, no comments, and no post-back. Assumption: `gh` is on PATH for the GitHub case.
  Done when: `fm inbox ticket` on an already-fetched key updates the brief and shows a diff of what changed, `gh` issue URLs are accepted, and close offers a "comment commit link" step that does nothing until the user confirms it.

- **Report known-fix hit rates and demote bad signatures** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: Review of T-1865: matching is safer now, but nothing reports how often a known fix was offered, accepted, or wrong. Assumption: accept and reject are already observable from later task state.
  Done when: `fm fixes stats` shows offered/accepted/wrong per signature, and a signature wrong 2 of its last 3 offers stops being offered, shown by a fixture test.

- **Count self-collisions apart from real risk, and show the rewrite** — FIX — value 4 — effort M — risk med — category: guard
  Why: The review says the risk budget tripped (6 destructive blocks) mostly from the agent's own `$VAR` paths and `rm` on `/tmp` globs. The guard's refusal text doesn't name the literal-path rewrite. Guard strictness stays unchanged.
  Done when: a block caused by an unexpanded `$VAR` or glob names the literal-path form in its message and is tagged "self-collision" in the budget ledger, and a retry using that form passes in a test.

- **Serve every page from one `fm serve` hub** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: Review: settings serve and swipe serve use one-shot tokens, need Ctrl-C to stop, each duplicate their own style block, and swipe --serve has no undo or cards-left count.
  Done when: `fm serve` lists every servable page under one shared stylesheet, a page survives a browser refresh within the session, and swipe shows "n left" and an Undo that restores the last verdict.

- **Audit DESIGN.md tokens against the CSS** — FEATURE — value 3 — effort S — risk low — category: design
  Why: Review of T-1652/1672: Figma import is one-way, and nothing checks that DESIGN.md tokens are actually used.
  Done when: `fm design audit` lists unused and undeclared-but-used tokens for a fixture project, exits non-zero in `--strict`, and the Figma export direction round-trips the imported tokens.

- **Add a scene gallery with captions and a render budget** — FEATURE — value 3 — effort M — risk low — category: scenes
  Why: Review of T-1846..1855: many showpiece scenes, no gallery index, no "what is this telling me" caption, and no test that each renders in under 1 s.
  Done when: `fm scene gallery` renders every scene with a one-line caption, and a test fails if any scene takes over 1 s on the fixture machine.

- **Offer a standing push authorization after the third "push X to main"** — FEATURE — value 4 — effort S — risk med — category: autonomy
  Why: The user's words include "Push foreman/build to main so the site publishes" and "Push T-1785, T-1830..T-1834, T-1839, T-1803 to main". Assumption: the offer is a decision card, and the grant is scoped to one branch and one remote and expires.
  Done when: the third such request produces a card, accepting it writes a scoped, expiring grant that the next push uses without asking, and a different remote or branch still asks.

- **Make closing a FEATURE open its docs step** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: The user asked for MASTER.md to document T-1403's probe, and fixed a help-position collision that broke test_help. Both are feature-adjacent chores someone had to remember.
  Done when: closing a FEATURE with no new line in MASTER.md or help creates a linked docs step, and the close is refused until the step is done or waived with a reason.

- **Wild: Run a persona walkthrough that writes the next round's review** — FEATURE — value 4 — effort L — risk med — category: self-review
  Why: This round's "read as its user" review was written by hand and was the best source of gaps (triage, ticket refresh, serve hub). Automating it at round start would make that review a standing input. Assumption: a child reading only the release diff, `fm help` and the docs can play a first-time user.
  Done when: `fm round review` produces a gap list of 5+ filed candidates from a release range, and at least half are judged valid by the user on the checklist page.

- **Wild: Turn each "I shouldn't have had to tell you" into a detector** — FEATURE — value 5 — effort M — risk med — category: self-noticing
  Why: The user said Foreman should have noticed its usage burn itself. The same shape (a steer that names something Foreman should have caught) will recur. Assumption: the steer ledger can flag "should have" phrasings.
  Done when: a steer matching that pattern creates a task whose output is a session-start sweep check with a test, and the check shows a visible "added because you said" note once.

- **Wild: Reproduce CI-only failures locally with a quirk profile** — FEATURE — value 4 — effort M — risk low — category: CI
  Why: The recent asks are all CI-only breakage: the runner's chromium crashing under load, Ubuntu 26's copied `sleep` dying, and the 20-minute job cap hiding a hang.
  Done when: `FOREMAN_CI_QUIRKS=1 fm check` applies a profile (no chromium, a dying copied `sleep`, a 20-minute cap, parallel load) and reproduces at least two of the known past CI-only failures from fixtures.

- **Wild: Surface hidden settings verbs when the user repeats a change by hand** — FEATURE — value 2 — effort S — risk low — category: discoverability
  Why: Review: settings log, macro, duel and replay are discoverable only through help, and `fm settings newcomer` never offers macros.
  Done when: making the same settings edit twice prints one line naming the macro verb that would replay it, and `newcomer` ends by listing the four hidden verbs.
