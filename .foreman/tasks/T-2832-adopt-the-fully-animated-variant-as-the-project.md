---
id: T-2832
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-03T19:25:49Z
updated: 2026-11-03T21:07:54Z
steer_method_rate: 0.218
done_in: T-2742
---
# Adopt the fully animated variant as the project's single canonical theme: choose it as…
## Raw request
> Honestly I like the fully animated one, can you super improve it entirely, and make that the new theme and such? on all aspects of it? readme, the tower, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Adopt the fully animated variant as the project's single canonical theme: choose it as the default and retire or remove the alternative theme variants (or clearly mark them as legacy) so there is one source of truth.
- Substantially upgrade that animated theme itself: improve its motion design, visual polish, smoothness, timing and easing, color and typography consistency, and overall quality, going beyond a copy of the current version.
- Apply the theme across every surface it touches, not just one: the tower (UI and visuals), README, docs, screenshots or demo media, landing or marketing pages, configuration and theme settings, assets, and any other place the old look appears.
- Keep the surfaces consistent with each other: shared colors, fonts, animation tokens, naming and wording derive from one place, so the README, docs and the tower all describe and show the same theme.
- Make the animation robust: respect reduced-motion preferences, keep performance smooth (no jank or heavy CPU or GPU use), and ensure it works across supported browsers, terminals or platforms, with a graceful static fallback.
- Preserve accessibility and function: sufficient contrast, readable text, no broken behavior, and no regressions in existing features.
- Verify the result by running the build, tests and linters, and viewing the actual output (the tower rendered, the README previewed), then report honestly what was checked and what could not be.
- Act directly on all of this without asking for step-by-step approval, but keep anything outward-facing or irreversible (publishing, deploying, pushing, deleting user data) behind explicit user approval, and keep removals of old variants recoverable (for example in version control, or a backup if th…
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-03T19:25:49Z created
- 2026-11-03T21:07:54Z done in T-2742: this steer is T-2788's brief (12 as the single canonical theme, carried through every surface), run under T-2742 step 7
## Follow-ups captured
