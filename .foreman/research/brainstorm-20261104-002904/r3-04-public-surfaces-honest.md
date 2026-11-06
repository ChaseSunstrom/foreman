# Brainstorm — lens: public surfaces honest

- **Gate public surfaces on a leak-term allowlist at publish** — SECURITY — value 5 — effort M — risk low — category: public text
  Why: the user pushed back on "jarvis" and on naming Claude as orchestrator; the pack's own ideas list proposes a lint but no step stops it at the moment of publish (`fm genesis live`, site data, README). Assumption: the denylist (machine names, endpoint names, vendor models, the user's email) can come from one file.
  Done when: planting "jarvis", a vendor model ID and a home path in site/genesis data makes `fm genesis live` and `fm ship` exit non-zero naming the file and line, and removing them passes.

- **Render every model and orchestrator name from one role table** — CLEAN — value 4 — effort M — risk low — category: roles
  Why: the user said "any orchestrator should work"; scenes, bench results and hook notes are hand-typed today. Assumption: a role table (orchestrator, planner, decider, embedder, reranker, generator) does not exist yet.
  Done when: grep of site/, README and the animation sources finds no vendor or endpoint name outside the role table file, and changing a table entry changes every rendered caption.

- **Turn each doc number into a probe-backed value** — FEATURE — value 4 — effort M — risk med — category: doc claims
  Why: 421 docs flag claims no run has checked, and counts like "2358 files" or "599" drift. Assumption: most numbers come from a verb's `--json`.
  Done when: a doc number is written as a tagged placeholder resolved by a command, and the ship gate fails when the typed text and the command output differ.

- **Stamp each doc claim with its last checking run and cited-file hash** — FEATURE — value 5 — effort L — risk med — category: proof status
  Why: the request says what can't be proven is labelled unproven; today there is no per-sentence label. A cited-file change should flip the label.
  Done when: `sampo docs claims` lists claims as proven (with run id and hash), stale (hash changed) or unproven (with a typed reason), and editing a cited file moves its claims to stale.

- **Expire "works with any agent" into a per-agent proven matrix** — FEATURE — value 4 — effort M — risk low — category: honesty
  Why: T-0335, T-0336 and T-0337 are blocked (codex, gemini and opencode never live-verified), yet the README says it works with all of them. Assumption: the README claim is not yet qualified.
  Done when: the README table shows each agent × capability as proven, unproven or blocked with the task id, generated from the ledger, and no cell reads "supported" without a run.

- **Lint rendered text, not just source: SVGs, alt text, scene captions** — SECURITY — value 4 — effort M — risk low — category: leak lint
  Why: demo/live.svg and the animated model-kind scene carry text that grep over prose misses; the "jarvis in the animation" complaint was exactly this.
  Done when: the lint extracts `<text>`, `alt` and `title` from every SVG and HTML file, and a planted vendor name inside an SVG fails it.

- **Make CHANGELOG lines carry a proof link or print as unproven** — FEATURE — value 3 — effort S — risk low — category: changelog
  Why: the CHANGELOG ships under the push grant with no check against its commits. Assumption: each entry maps to a T-id.
  Done when: each CHANGELOG line resolves to a task with a close proof, and lines without one render with an "unproven" mark.

- **Run the quickstart in a scratch home under a docs-only child** — FEATURE — value 4 — effort M — risk med — category: onboarding proof
  Why: README Quick start and the "works with no claude on PATH" steer are asserted, not replayed on a clean host.
  Done when: a nightly run executes the README's install block in an empty HOME with no `claude`, records the output, and fails on the first step that needs something undocumented.

- **Show an Unproven shelf in the web UI, grouped by reason** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: "meaning" is the largest unproven class (599) and nothing shows the user the shape of it. Assumption: reasons can be typed (needs host, needs human, too slow, no example).
  Done when: a web page lists unproven counts per reason with a link to each item, and a count falls when its item gets a proof.

- **Wild: Mystery orchestrator: scenes rotate the orchestrator name per load** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user wants any orchestrator to work, and a fixed label bakes in one. A rotating placeholder from a list of CLIs shows it plainly. Assumption: the scenes are scripted SVG/JS that can take a parameter.
  Done when: reloading the site scene shows different agent CLI names across loads and the underlying markup contains no fixed one.

- **Wild: Blind leak reader: a tool-less child reads only the rendered site and names the host, vendor and user** — SECURITY — value 4 — effort M — risk low — category: leak test
  Why: lints only catch the terms we thought of; the pushback came from a human spotting what ours missed.
  Done when: a child given the rendered pages answers "who runs this?" and the run passes only when it names none of the machine, vendor or person, and its guesses are logged.

- **Wild: Quine check: Sampo's spec regenerates a claims file that matches the real one** — FEATURE — value 2 — effort L — risk med — category: self-proof
  Why: the standing intent is a discipline layer that proves itself; the docs about it should be held to the same bar. Assumption: claims are structured enough to diff.
  Done when: a regenerated claims file from the docs alone equals the stored one, or the diff names the unstated claims.

- **Date-stamp host-behaviour claims and recheck on a host upgrade** — FEATURE — value 3 — effort S — risk low — category: host claims
  Why: statements about Claude Code hooks and pane colours (T-1217) rot when the host changes.
  Done when: each such claim carries a host version, and a version change flags every dependent claim as stale in `fm doctor`.

Next question: Which public surfaces (site data, README, SVGs, CHANGELOG, `--help`, hook-injected notes) does the vocabulary lint not yet read, and who has actually seen each rendered?

Next question: When a claim is labelled unproven, does the user read that as honest or as noise, and what do they do next?
