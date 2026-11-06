# Brainstorm — lens: delight

- **Draw a design constraint card** — FEATURE — value 4 — effort S — risk low — category: design skills
  Why: the pack's only UI playbook is 13 lines, and generic output is the user's complaint. A seeded deck of constraints (e.g. "one typeface weight", "no shadows, depth by overlap only", "motion on one axis") breaks defaults more cheaply than a full style roll. This is different from the existing "style dice", which picks a whole aesthetic. Assumption: constraints are easier to check than taste.
  Done when: `fm design draw --seed 7` prints the same card twice, and `fm check design` fails a fixture page that violates that card's rule.

- **Add an audacity dial to UI tasks** — FEATURE — value 4 — effort M — risk low — category: design skills
  Why: assumption: the user wants "non-generic" but not always maximal weirdness. One `--boldness 0..5` setting scales how far design-direction, motion and 3D playbooks may stray. It also sets slop-detector strictness, so a calm admin tool and a launch page don't get the same advice.
  Done when: the same brief at boldness 1 and 5 yields different token files, and each passes the slop detector at its own level.

- **Render receipts as blueprint sheets** — FEATURE — value 3 — effort M — risk low — category: artifacts
  Why: `fm page` artifacts and the closing receipt are plain. A blueprint style (cyan paper, dimension lines for file sizes, a title block with task id, gates and proof) makes receipts something people screenshot and share. It is one distinctive look in the existing site/page pipeline. Assumption: the page generator can take a style module.
  Done when: `fm page --style blueprint T-1213` writes a self-contained SVG/HTML with a title block listing the task's verify commands, and it makes no third-party requests.

- **Wipe between before and after on UI receipts** — FEATURE — value 4 — effort M — risk low — category: visual proof
  Why: the pack proposes film strips and before/after frame pairs but not the interaction. A draggable, keyboard-operable wipe with an onion-skin 50% mode lets the user judge a UI change in seconds. It reuses the screenshots the visual proof loop already captures.
  Done when: the receipt HTML for a UI task has a slider operable by arrow keys, and the before and after images are the exact files named in the task proof.

- **Add a photo booth for TUI frames** — FEATURE — value 3 — effort S — risk low — category: sharing
  Why: SVG replay export exists, but a single beautiful still does not. `fm code snap` would take the current frame and add window chrome, soft shadow, gradient backdrop and the theme's accent, with secrets scrubbed first. It is what people post, and it doubles as README and site imagery.
  Done when: `fm code snap --out x.svg` produces a framed image from a golden frame, and a fixture containing a fake API key shows it redacted.

- **Collect looks as trading cards** — FEATURE — value 3 — effort S — risk low — category: gallery
  Why: the planned lookbook and style shelf are lists. A generated card per look (swatches, type specimen, motion sample, and stats from `fm check design` such as contrast floor and animation budget) makes the shelf browsable and comparable. Assumption: the 10–40 looks will exist as token files.
  Done when: `fm design cards` writes one SVG per look, and each card's contrast figure equals what the checker reports for that look.

- **Overlay motion X-ray on a dev page** — FEATURE — value 4 — effort M — risk low — category: motion tooling
  Why: the motion playbook is planned, but nobody sees the motion it prescribes. A debug script draws each animated element's easing curve, duration and delay as fading ghost trails, and flags anything outside the page's motion tokens. This lets Claude and the user inspect motion in practice, not only in the spec.
  Done when: loading a fixture page with `?motion=xray` shows a trail per animated element, and a deliberately off-token animation is marked red.

- **Fold a run into a printable zine** — FEATURE — value 2 — effort M — risk low — category: keepsake — wild
  Why: assumption: a keepsake is more fun when it is physical. An 8-panel one-sheet SVG/PDF with fold and cut lines would carry the request, the plan, the red-to-green moment, the guard saves and the receipt. It is built from the same run report the other exports read, offline.
  Done when: `fm zine T-1213` writes a single-page file whose eight panels each cite a field of the run report, with the fold lines drawn.

- **Add a risograph overprint theme** — FEATURE — value 3 — effort M — risk med — category: TUI look — wild
  Why: two-spot-colour overprint with slight misregistration suits the claims-versus-proof ledger. Claimed work prints in ink A, proved work in ink B, and where they overlap, a third colour shows it is proved. State then reads from texture and overlap, and the frame is unlike any generic dark theme. It also needs a mono-safe fallback.
  Done when: the theme renders a ledger frame in which an unproved claim shows one ink and a proved claim shows the overlap colour, and the frame stays legible under NO_COLOR via glyph fill.

- **Turn a finished run into a lathe-turned vase** — FEATURE — value 2 — effort L — risk med — category: 3D keepsake — wild
  Why: the planned stdlib rasteriser could render a solid of revolution whose profile is the run's per-file change-size histogram. It spins in the terminal, can be exported as an STL, and is a 3D piece that exists for delight. It also gives the 3D rasteriser a modest first job.
  Done when: `fm code vase T-1213` shows a rotating shaded solid in a pty test, and `--stl` writes a valid ASCII STL with a closed mesh.

- **Let a hand-drawn margin sketch annotate any playbook** — FEATURE — value 2 — effort S — risk low — category: playbooks — wild
  Why: assumption: dense playbooks are skimmed. Each design playbook could carry one tiny original ASCII or SVG diagram, such as an easing curve, a camera angle or a type scale ladder. `fm playbooks show` would draw it beside the rule it explains, in the project's current theme.
  Done when: the `ui/` playbooks each embed a diagram block that renders in `fm playbooks show`, and a lint rejects a design playbook rule that has no diagram or example.
