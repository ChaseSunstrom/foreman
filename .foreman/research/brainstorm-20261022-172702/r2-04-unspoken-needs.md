# Brainstorm — lens: unspoken needs

- **Replay real history against new descriptions** — FEATURE — value 5 — effort M — risk low — category: skills eval
  Why: the pack's trigger eval ideas use synthetic prompts; `fm usage` already holds 30 days of real turns where a skill should have fired (assumption: transcripts keep the prompts and tool calls).
  Done when: `fm skills replay` re-runs the last N real turns against the current descriptions and prints, per skill, how many turns would have loaded it versus how many did.

- **Check that skills reach builder lanes** — FIX — value 5 — effort M — risk med — category: lanes
  Why: assumption: most Foreman work happens in headless builder lanes whose briefs come from WORKER_SUBREADS, so those lanes may never see the skill listing and the usage counts would stay near zero however good the descriptions are.
  Done when: a lane transcript fixture shows the skill listing present, or a lane brief that names the needed skill by task type, and `fm usage` splits skill use by main session versus lane.

- **Gate FEATURE tasks on a first real use** — FEATURE — value 4 — effort M — risk med — category: adoption
  Why: the user keeps asking for features (fm design roll, fm critique, settings serve) while the skills they asked for earlier sit at zero use. Shipped does not mean used.
  Done when: closing a FEATURE task records a "first real use" entry (command or skill fired outside tests), and tasks without one show as "shipped, unused" in `fm status`.

- **Extend the usage census to every fm subcommand** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the pack measures only skills and playbooks, but the same disuse likely hits many of the 20+ commands the user requested. Assumption: the usage log already records fm invocations.
  Done when: `fm usage --commands` lists each subcommand with a 30-day count and flags those at zero next to the task that introduced them.

- **Show a "what's new and how to try it" digest in the final report** — FEATURE — value 4 — effort S — risk low — category: reporting
  Why: autonomous runs ship dozens of capabilities (the open-work and "asked" lists are long), and the user can't tell which ones exist now. They had to ask why skills go unused, which suggests they find out about capabilities late.
  Done when: the final report ends with a section listing each capability shipped this run with a one-line command that demos it, and each command runs clean.

- **Turn the user's steers and drops into a personal review skill** — FEATURE — value 4 — effort M — risk low — category: personalization
  Why: the "steered" and "dropped" lines repeat patterns (CHANGELOG entry missing, overlay location, reviewer nits about schema conventions). Assumption: these are mined from intake and can be clustered.
  Done when: a generated `foreman:your-rubric` skill lists the 5–10 recurring corrections with the task each came from, and a pre-close step cites it in the review.

- **Triage the deferred "Later from" backlog against usage evidence** — CLEAN — value 3 — effort M — risk low — category: backlog
  Why: about 30 tasks are deferred, many with "later: needs evidence of …" (T-0862, T-0863, T-0866). Foreman now has the evidence they were waiting for, but nothing re-reads them.
  Done when: `fm queue triage` re-ranks deferred tasks by their stated evidence condition and closes or promotes each with a one-line reason.

- **Show a skill-loaded chip in the foreman-ui tree** — FEATURE — value 3 — effort S — risk low — category: visibility
  Why: the user can't see skills working, so "hardly used" is a guess until they run the census. A visible chip makes use something they can watch live.
  Done when: loading a skill adds a labeled node under the prompt in the tree, and a screenshot test shows it.

- **Give skills a review date that expires them** — CLEAN — value 3 — effort S — risk low — category: skill hygiene
  Why: 13 skills ship and 12 are at zero, and nothing forces a decision. Assumption: SKILL.md frontmatter can carry an extra field without breaking Claude Code.
  Done when: each skill has `review_by`, and `fm doctor` warns on any skill past that date with zero uses.

- **Wild: Ghost-user test corpus built from the user's own past requests** — FEATURE — value 4 — effort L — risk med — category: eval corpus
  Why: wild. The "asked" list is a corpus of this user's real phrasing, and it could drive both skill-trigger evals and the bench cases that T-0866 is waiting for.
  Done when: a command turns the intake log into at least 40 redacted prompt fixtures, each labeled with the skill or playbook it should fire, and the replay eval uses them.

- **Wild: A skill that argues the user's side before close-out** — FEATURE — value 3 — effort M — risk med — category: review
  Why: wild. A pre-close skill role-plays the user from their steers ("why is this not moved?", "where is the changelog line?") and the close fails if the answers aren't in the diff.
  Done when: on a fixture task missing a changelog line, the skill's question list includes it before the reviewer catches it.

- **Wild: Skills that arrive as hook-time whispers when the file path matches** — FEATURE — value 4 — effort M — risk med — category: triggering
  Why: wild. Instead of waiting for the model to ask, the PreToolUse hook sees an edit to `*.html` or `scene.json` and attaches the matching skill's first 20 lines as context. The playbook-by-path idea in the pack is about playbooks; this applies it to skills and keeps it under the ~10 KB hook cap.
  Done when: editing a `scene.json` in a fixture adds the scene skill's summary to the hook context, within the size cap, and the `fm usage` count for that skill rises.

- **Wild: Export skills as an AGENTS.md block for Codex, Gemini and opencode** — FEATURE — value 2 — effort M — risk low — category: portability
  Why: wild. The blocked tasks T-0335, T-0336 and T-0337 show the other CLIs matter to the user, and skills are plain markdown that could reach them. Assumption: those CLIs read AGENTS.md or an equivalent.
  Done when: `fm skills export --agents` writes a block that fits each CLI's size limit and passes the guard lint, with Claude Code behavior unchanged.
