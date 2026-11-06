# Brainstorm — lens: delight

- **Watch the proof go green** — FEATURE — value 4 — effort M — risk low — category: dev loop
  Why: assumption: `fm shot`, `fm flow` and docs checks run only on demand, so the loop between an edit and its proof is slow. Unit-test watchers feel alive; non-unit proofs don't.
  Done when: `fm prove --watch` re-runs the affected shot, flow or docs proof within 3 s of a file save, and the status line goes amber then green (or red) with the changed claim named.

- **Write a lab-notebook entry per proof** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: assumption: proof output today is verdict-shaped. A fixed Claim / Method / Observed / Conclusion / Not shown entry reads like a human wrote it and sets "unproven" apart as an honest conclusion.
  Done when: each finished proof appends a 5-line entry to a notebook file, and `fm notebook` prints the last N, each citing the real command and its exit code.

- **Show the shot inline in the terminal** — FEATURE — value 4 — effort M — risk med — category: terminal UI
  Why: the surface is a terminal, and users currently leave it to open a PNG. Kitty/sixel images outline the changed regions, with an ANSI half-block fallback.
  Done when: `fm shot --show` renders before/after with changed boxes outlined in kitty, and a fallback mode produces readable output over plain SSH. A test asserts the fallback.

- **Print the proof delta in release notes** — FEATURE — value 3 — effort S — risk low — category: changelog
  Why: the CHANGELOG commit trail shows numbers need counts and baselines (T-2591). A line like "+14 claims proven, 2 newly unproven, 1 expired" makes progress visible and is easy to share.
  Done when: `fm ship` prints and writes the delta against the previous tag. Each count is backed by listed claim ids.

- **Post the proof to the PR as a collapsible comment** — FEATURE — value 3 — effort M — risk med — category: sharing
  Why: assumption: reviewers can't see what was verified unless the author pastes it. Before/after shots, flow results and an "Unproven" section go in `<details>` blocks.
  Done when: `fm ship --pr-comment` produces one markdown comment with those sections, scrubbed of secrets, and posts it only after an explicit yes. Dry-run output is checkable.

- **Hold a catch-of-the-week card** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user sees only green. The one time a proof caught a real false done or off-screen button never gets celebrated, though it is why they trust the tool.
  Done when: the weekly digest names the single best catch, with the claim, the planted or real defect and the proof that caught it, from ledger data. It prints "nothing caught" rather than inventing one.

- **Step through data changes as row polaroids** — FEATURE — value 3 — effort M — risk low — category: data proof
  Why: assumption: row-count and invariant checks are correct but dull. Three sampled before/after rows, with changed fields highlighted, let the user judge "is that what I meant?" in seconds.
  Done when: `fm prove data --cards` shows N sampled rows as before/after cards, navigable with arrow keys, and records which the user confirmed or flagged.

- **Run doc snippets from a button in the web UI** — FEATURE — value 3 — effort M — risk med — category: docs proof
  Why: docs-against-code is in the request. A Run button beside each doc command, executed in a scratch copy with output shown, proves the docs and lets a newcomer try it safely.
  Done when: clicking Run on a README snippet executes it in a temp clone, shows stdout and exit code, and marks the snippet verified-at-HEAD or failing. The real tree is untouched.

- **Draw the tick** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: assumption: a claim flipping unproven → proven is the product's core moment, yet it likely just changes text colour. A short stroke-draw tick and a calm settle explain the state change.
  Done when: the web UI animates a claim row on flip, with `prefers-reduced-motion` showing a static tick. A screenshot flow checks both states.

- **Guess the verdict first (wild)** — FEATURE — value 2 — effort S — risk low — category: game
  Why: wild. Before a long proof returns, the user can press p or f for pass or fail. Over weeks it shows how often their gut matches reality and which claim kinds surprise them most, which is useful for deciding what to verify.
  Done when: an opt-in prompt records guess and result, and `fm prove --gut` prints a hit rate by proof kind.

- **Flip through the app across commits (wild)** — FEATURE — value 4 — effort L — risk med — category: visual bisect
  Why: wild. Run `fm shot` at each of the last N commits and build a flipbook. Regressions appear as a jump, and `fm shot bisect` stops at the first commit where a named region changed. This answers "when did it start looking wrong?" without the user guessing a commit.
  Done when: on a fixture repo with a planted CSS break, bisect names the breaking commit and writes a self-contained HTML flipbook.

- **Say performance in human scale (wild)** — FEATURE — value 2 — effort S — risk low — category: perf legibility
  Why: wild. "p95 212→168 ms, noise ±9" is accurate but numb. Add "about a third of a blink faster, beyond noise", and when the change is inside the noise, say "can't tell yet".
  Done when: perf verdicts print the technical line and a one-line plain gloss. A run inside the noise floor never gets a "faster" phrase.

- **Tour the provers with a planted bug** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: `fm demo` exists, but nothing shows what proof beyond unit tests feels like. A 60-second tour on a bundled toy app plants a bug, has shot, flow and docs proofs catch it, then fixes it and goes green.
  Done when: `fm demo prove` runs offline, with each prover catching its planted fault, and exits 0 only if all three were caught.

Next question: which proof moment would the user actually screenshot or forward to someone, and does any current output survive being read without Foreman installed?
Next question: of the claims marked unproven in the last 30 days, which did the user later prove by hand, and how did they do it?
