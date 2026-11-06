# Brainstorm — lens: simplicity

- **Use `prompt.suggest` to ghost-text the one required next action** — FEATURE — value 4 — effort S — risk low
  Why: Foreman injects "Next: <action>" into every prompt, which costs tokens and can be ignored. `prompt.suggest` is unused. A ghost-text Tab-accept of the next step (e.g. "approve plan", "start T-0082") replaces some of the nagging with zero model tokens. Assumption: `fm ui --json` already carries the next action.
  Done when: with an approvable plan pending, the prompt box shows ghost text "approve plan" and Tab submits it; with no active task the suggestion is empty.

- **Show the Foreman step in `PromptHint tail` and `SessionMode`, then remove the matching `state.line` and `badge.txt` writes** — CLEAN — value 3 — effort S — risk low
  Why: the footer slots are unused, and the cached state.line, progress.line and badge.txt files exist only to feed the statusline. Assumption: the statusline wrapper must remain as the fallback when mods are unavailable, so only the mod-active path stops writing them.
  Done when: with the mod on, the footer shows the step and no cache file is touched during a turn; with the mod off, the statusline is unchanged.

- **Add `fm help` with three tiers (core 8 commands, advanced, internal)** — CLEAN — value 3 — effort S — risk low
  Why: ~45 subcommands, and planning friction comes from exact section names and several calls. Assumption: this isn't covered by the earlier "gate subcommand sprawl" idea beyond its title, so make it concrete: the default `fm help` lists only the commands the model needs in a normal flow.
  Done when: `fm help` prints ≤10 lines, `fm help --all` lists everything, and a test fails if a new subcommand lacks a tier.

- **Make `fm task new` accept a free-form paragraph and auto-fill sections by fuzzy header matching** — FIX — value 4 — effort M — risk med
  Why: T-0075 and T-0080 come from strict section names ('Approach (options → choice → why)' vs 'Approach'). Fuzzy matching (prefix, case-insensitive, alias table) removes that class of failure without a new command. This is different from "one `fm task plan` call" because it fixes the existing `--section` path everyone already uses.
  Done when: `--section approach`, `--section Approach` and the full header all fill the same section, and an ambiguous name errors with the candidate list.

- **Fold a "token receipt" into the TurnDuration line from `$.session.usage()`** — FEATURE — value 3 — effort S — risk low
  Why: the user is usage-sensitive, and the per-turn summary exists but shows no tokens. Showing Foreman's own injected tokens (hints, rules) vs the turn total makes the always-on cost visible and measurable, which also supports the T-0085 rules diet. Assumption: usage() exposes per-turn input/output counts.
  Done when: each turn line shows "+N tok (F from Foreman)" and a test pins F against a known injected hint.

- **Cut the stage machine to a derived view: store only steps and criteria, compute stage** — CLEAN — value 4 — effort L — risk high
  Why: seven stored stages (captured→…→closing) cause drift on resume, extra transitions, and extra UI rows. Deriving the stage from step and criteria state removes a whole class of stage/step mismatches. Assumption: no external consumer writes the stage directly. Not the same as "cap at five visible stages", which only hides stages.
  Done when: no stage field is persisted, `fm task show` still prints the stage, and all 28 test files pass with the stored-stage code deleted.

- **Add a "quiet by default" Foreman profile: mod on means no hint injection unless a gate is about to fire** — PERFORMANCE — value 4 — effort M — risk med
  Why: hints go into every prompt and Stop, and the model can ignore them anyway. Injecting only when the next action differs from the last one stops repeating the same hint each turn. Assumption: the hook can compare against the last injected value.
  Done when: two consecutive prompts with an unchanged next action inject the hint once, and a changed action re-injects it.
