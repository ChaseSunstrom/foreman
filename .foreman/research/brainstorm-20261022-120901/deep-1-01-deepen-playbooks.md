# Brainstorm — lens: deepen: playbooks

- **Compile playbooks into a chain router with stage contracts** — FEATURE — value 5 — effort M — risk low — category: playbooks
  Why: 48 files in 15 stages, and the existing idea "route request to chain" is only a lookup. Yes-and: each playbook declares `needs:` (artifacts it consumes, e.g. a direction brief) and `yields:` (artifacts it must leave, e.g. a screenshot set), so `fm playbooks route` builds a chain such as direction → build → motion → visual QA → a11y, and `fm task prove` can check each stage's yield exists.
  Done when: `fm playbooks route "landing page with a 3D hero"` prints an ordered chain whose every link names its needs and yields, and a chain with an unmet `needs:` is refused with the missing artifact named.

- **Make the UI family a design-brief-first pipeline with a gate** — FEATURE — value 5 — effort M — risk med — category: playbooks, UI
  Why: the pack has one 13-line ui playbook, and the user asks for "non generic" UI. Combine "force a point of view" with "bank of exemplars": a `ui/direction` step writes `design-brief.md` (references, three rejected cliches, type pair, palette with roles, one signature motion), and later UI playbooks refuse to start without it.
  Done when: a UI task's first edit is blocked by the done-gate until `design-brief.md` has all required fields, and a fixture brief missing "rejected cliches" fails `fm check`.

- **Ship a generic-detector that lints built UI against the brief** — FEATURE — value 4 — effort M — risk med — category: design QA
  Why: assumption: taste can be partly checked mechanically. Stdlib scan of CSS/TSX for default tells (system-ui only, #6366f1-style indigo gradients, uniform 8px radii, three equal feature cards, no easing curves beyond `ease`) and drift from the brief's palette and fonts.
  Done when: running it on a fixture of a template-looking page reports at least 5 named tells, and on the Foreman site reports none above a threshold.

- **Give every playbook a before/after eval pair that runs in `fm eval`** — FEATURE — value 5 — effort L — risk low — category: playbooks, evals
  Why: combines "before/after pairs", "ablate every line", and "contradiction check". The plugin already has plugin/evals/ (21). Each playbook ships a task, a grader, and a with/without run, so a playbook that does not move its pass rate gets flagged for pruning and each line's ablation is recorded.
  Done when: `fm playbooks score ui/motion` prints a with/without pass rate over N runs, and a playbook with no measurable lift appears in a prune list.

- **Add playbook inheritance and project overlays** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: "inject live project facts" plus a gap in the pack: Foreman's own site wants a house style, others want theirs. A repo-level `.foreman/playbooks/` can `extends: ui/direction` and override fields (fonts, forbidden patterns, verify commands), merged at load, with the override shown in diff form.
  Done when: an overlay that overrides one section loads merged, `fm playbooks show --resolved` marks the overridden lines, and an overlay that removes a guard-related directive is refused.

- **Write a "visual proof" playbook with screenshot receipts** — FEATURE — value 4 — effort M — risk med — category: verify, UI
  Why: Foreman's thesis is proving work with commands that ran; UI work currently has no equivalent. Playbook plus helper: render at 3 widths and reduced-motion on/off, store the images as task evidence, and require the author to name what each image shows.
  Done when: a UI task cannot close until `fm task prove` finds screenshots from at least two viewports and a reduced-motion capture recorded by a command that ran.

- **Build a playbook-writing playbook that lints new playbooks** — FEATURE — value 3 — effort S — risk low — category: playbooks, meta
  Why: the user wants many more playbooks, and the constraint is original writing. A meta playbook with `fm check playbook` verifies the required frontmatter, a length ceiling, a before/after pair, a verify command, and a similarity check against indexed third-party skill text to enforce "original writing".
  Done when: a playbook copying a paragraph from a quarantined index source fails the check with the matching source named.

- **Let playbooks read the session's failures and rewrite their own priorities** — FEATURE — value 4 — effort M — risk med — category: playbooks, learning
  Why: ties to T-0217 (lesson confidence). Playbook sections that preceded first-time passes rise in the loaded order; sections never recalled before a failure get demoted from the injected excerpt, keeping token cost down.
  Done when: after replaying a fixture history, `fm playbooks show X` orders sections by measured lift, and the change is reversible with one command.

- **Offer playbooks in `fm code` as a one-line, token-costed intake** — FEATURE — value 3 — effort S — risk low — category: playbooks, fm code
  Why: pack shows the open intake-offer ask; extend it to Foreman's own playbooks with their token cost and the stage they serve.
  Done when: an `fm code` request mentioning "animation" prints one line naming `ui/motion` with its token cost and installs nothing.

- **Wild: Make playbooks executable "dojo" katas** — FEATURE — value 3 — effort L — risk med — category: wild, training
  Why: wild. Each playbook ships a tiny broken scenario (a janky easing, a flaky test, an unsafe migration) and `fm dojo` has a cheap model attempt it under the playbook; the result is the eval fixture, a demo for the site, and a way to check that weaker runner models can follow the playbook.
  Done when: `fm dojo ui/motion` runs the kata and reports pass/fail with the diff produced.

- **Wild: Add a "taste ledger" that learns the owner's design preferences** — FEATURE — value 4 — effort M — risk med — category: wild, UI
  Why: wild. When the user accepts, edits or reverts a generated UI, Foreman records the diff as a signal (they keep rejecting rounded cards; they prefer dense tables), then writes it into their project overlay so later direction briefs start from their taste and not the median.
  Done when: after three recorded reverts of a pattern, a new `design-brief.md` lists that pattern under rejected cliches with the evidence count.

- **Wild: Generate a playbook from any finished task's transcript** — FEATURE — value 4 — effort L — risk high — category: wild, playbooks
  Why: wild. Foreman has the task and tool history; distilling a successful hard task (a migration, an incident fix) into a draft playbook with before/after and a verify step, quarantined as draft until a human promotes it, makes the library grow from real work.
  Done when: `fm playbooks distill T-NNNN` writes a draft that passes `fm check playbook` and is not loadable until `fm playbooks promote`.

- **Wild: Render playbooks as a browsable "field guide" on the site with live exemplars** — FEATURE — value 3 — effort M — risk low — category: wild, site
  Why: wild. Site build already exists; each UI playbook page embeds its runnable exemplar (a small motion demo, a 3D scene) with the brief that produced it, doubling as proof of the taste claim.
  Done when: `site/build.py` outputs a page per UI playbook with a working exemplar and fails the build on any outside host.

- **Add a contradiction and budget check across loaded playbook sets** — CLEAN — value 3 — effort S — risk low — category: playbooks, hygiene
  Why: with chains of 5+ playbooks, directives will collide (e.g. "no animation over 200ms" versus a cinematic intro) and tokens add up. Check the resolved chain for opposing rules and total size before it loads.
  Done when: a fixture chain with a known conflict prints the two lines and the chain's token total, and exits non-zero.
