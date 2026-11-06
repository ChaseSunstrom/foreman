# Brainstorm — lens: approaches

- **Cut the slate to one tracer bullet, `fm look`** — FEATURE — value 4 — effort M — risk low — category: process
  Why: about 2,000 ideas are logged and the user asked for "super recursive … etc." The proven path is one thin slice that touches all four asks. Assumption: no end-to-end slice exists yet.
  Done when: `fm look roll` writes DESIGN.md and tokens, the TUI theme changes live from the settings screen, one design playbook loads, and one eval with/without that playbook passes.

- **Make the model confess its defaults, then ban them for that task** — FEATURE — value 4 — effort S — risk low — category: design process
  Why: static slop detectors are listed, but none adapts to the model's own habits for this brief. The brief gets a "defaults I'd reach for" section of at least 3 items, and verify greps the diff for them.
  Done when: a UI task cannot close without that section, and a diff that contains a confessed default fails verify.

- **Run visual QA in a forked skill context** — FEATURE — value 4 — effort S — risk low — category: visual QA
  Why: screenshots are token-heavy, and `fm shot` plus the critic panel would bloat the main context. A skill with `context: fork` returns only a bounded verdict (at most 10 lines plus file paths). Assumption: the Claude Code skills `context: fork` frontmatter is available in the installed version.
  Done when: a UI task's main transcript contains no image blocks, and the verdict file lists the issues and the shot paths.

- **Critique design from a computed-style census, not pixels** — FEATURE — value 4 — effort M — risk low — category: design lint
  Why: the pack covers vision critique and token linting, but not a census of the live DOM. Dump `getComputedStyle` for every element, then count the distinct font sizes, colours and radii and measure how far spacing strays from the scale. That is cheap, deterministic and needs no vision model.
  Done when: `fm check design --census` reports counts against the DESIGN.md scale and fails on an off-scale spacing value in a fixture page.

- **Declare each screen as a state chart and shoot every state** — FEATURE — value 4 — effort M — risk med — category: UI proof
  Why: empty, loading and error states are the usual crafted-UI gap, and only "hostile condition matrix" gestures at them. The chart is the one source for the proof shots, the motion transitions and the test traversal.
  Done when: a screen with an undesigned reachable state fails `fm check ui`, and one screenshot per state lands in the receipt.

- **Test the settings screen with a model as a first-time user** — FEATURE — value 4 — effort M — risk low — category: TUI config
  Why: the pack plans a settings screen, search palette and scope picker, but nothing measures whether a person can find things. A cheap model gets frames as text plus a goal ("make motion calmer") and reports the keys it pressed.
  Done when: `fm code tui --usability` lists per-goal key counts and fails any goal that takes more than 6 keys or is not found.

- **Write only the keys the user changed to tui.toml** — FEATURE — value 3 — effort S — risk low — category: TUI config
  Why: a sparse override file lets new release defaults flow through. That makes the "default changed" notices unnecessary for settings the user never touched. Assumption: tui.toml is currently written in full.
  Done when: after changing one setting the file holds one key, and bumping a default changes the unset keys' behaviour.

- **Project one design source into Claude-native channels** — CLEAN — value 3 — effort M — risk low — category: skills
  Why: the pack plans per-CLI rules projection but not the Claude-native shapes. One playbook source would generate a skill, an output style, a path-scoped rule that loads only on touched `*.css` or `*.tsx`, and a designer subagent definition.
  Done when: editing the source and running the generator updates all four artifacts, and a test fails if any of them has drifted.

- **Inject live project facts into playbooks at load** — FEATURE — value 3 — effort S — risk med — category: playbooks
  Why: playbook text is static. Load-time injection from read-only `fm` verbs (tokens, browser availability, `fm map` gates) lets the guidance name this project's real values. Risk: injected commands run, so they need an allowlist.
  Done when: loading the playbook prints the project's tokens, and a non-allowlisted injection line is refused.

- **Ship 3D scenes as an `<fm-scene>` web component** — FEATURE — value 3 — effort M — risk low — category: 3D
  Why: scaffolds and templates exist as ideas, but a drop-in tag with a poster fallback and reduced-motion handling is a different packaging. It is easy to use and easy to test.
  Done when: one tag renders a scene, shows the baked poster with WebGL disabled, and a test asserts both.

- **Assert reduced-motion equals the animation's final frame** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: "calm mode is the test mode" is logged, but the exact invariant isn't: the calm frame hash must equal the last frame of every animation, which proves motion is only presentational.
  Done when: the frame-hash test fails when an animation's end state differs from its static state.

- **Import tokens through a Figma MCP adapter behind the guard** — FEATURE — value 3 — effort M — risk med — category: design import
  Why: the pack covers token export (Tailwind, DTCG JSON) but no import, and the user asked for much stronger design capability. Assumption: users hold Figma files. Third-party output stays data.
  Done when: a recorded Figma MCP response becomes a valid DESIGN.md tokens block, and no network call occurs without a setting.

- **Route UI tasks by a blind multi-runner taste panel** — FEATURE — value 3 — effort L — risk med — category: routing (wild)
  Why: wild. Each configured runner designs the same brief, the user picks between unlabelled results, and the win rate per runner feeds the router for UI kinds. This is the first taste-based routing signal; the pack only routes on cost and pass rate.
  Done when: `fm code taste-panel` records blind picks and the next UI task shows its runner choice citing that win rate.

- **Write the launch note first and check the hero exists** — FEATURE — value 3 — effort S — risk low — category: design process (wild)
  Why: wild. A UI task starts with a three-sentence launch note naming the one element a stranger would screenshot. A DOM selector for that element must exist and be visible above the fold in the proof shot.
  Done when: removing the named element from a fixture fails the check.

- **Render the same layout in five historical idioms** — FEATURE — value 2 — effort M — risk low — category: design exploration (wild)
  Why: wild. A 1984 terminal, a Swiss poster, a 1998 web page, a skeuomorphic one and a brutalist one. The structure decisions that survive all five (hierarchy, grouping) are kept, and the rest becomes the style choice.
  Done when: `fm look eras` outputs five contact-sheet shots from one brief and lists the surviving structure decisions.
