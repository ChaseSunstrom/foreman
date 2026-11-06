# Brainstorm — lens: unspoken needs

- **Pre-mark the checklist page with predicted build/skip** — FEATURE — value 4 — effort M — risk med — category: triage
  Why: wild. Pillar 3 has the user mark every idea build/skip, and they have clear habits: they drop findings that are "already built" and steer toward fewer asks. The ledger holds ~2,000 ideas, so marking them all is a chore. Predict each mark from their past verdicts and drops, then ask only about the uncertain third.
  Done when: on a fixture of past verdicts, the page arrives with ≥70% of cards pre-marked and shows a held-out accuracy line, with the uncertain cards listed first.

- **Accept ranges and lists wherever a task id goes** — FEATURE — value 4 — effort S — risk low — category: CLI
  Why: the user writes "Push T-1785, T-1830..T-1834, T-1839, T-1803" and "T-1830/T-1831/T-1832". Assumption: the verbs currently take one id each.
  Done when: `fm task show T-1830..T-1832,T-1839` expands to four tasks, and an unknown id inside a range is named rather than silently skipped.

- **Reserve registry slots per lane at launch** — FIX — value 4 — effort S — risk low — category: lanes
  Why: "fm dojo shares help position 306 with another command, so test_help fails", and the steer about filling PLUGIN_ROUTES and APP_ONLY in test_plugin_parity. Parallel lanes all add rows to the same registries and collide at merge.
  Done when: two lanes started together each get a disjoint help-position and route block, and two parallel fixture lanes adding commands merge with test_help green.

- **Give the idea ledger a theme map with a saturation count** — PERFORMANCE — value 4 — effort M — risk low — category: brainstorm
  Why: the ledger sent to every child is ~2,000 titles, and "thin so far" shows skills and playbooks swamping it. The user's usage-burn complaint covers brainstorms too. Send a ~40-line map (theme, count, three exemplars, saturated yes/no) in place of the raw list.
  Done when: the pack's ideas section drops below 3k tokens, and a test confirms a known-duplicate idea is still caught by its theme.

- **Keep a ledger of tests skipped in CI, each with an expiry** — FEATURE — value 4 — effort S — risk low — category: CI
  Why: "CI turns browser tests off: the runner's chromium crashes under parallel load". That is a quiet loss of coverage. Show "N tests off in CI since DATE" in `fm doctor` and the session-start sweep.
  Done when: disabling a test class in CI without a ledger entry fails the gate, and an expired entry shows as a doctor failure.

- **Pin each review finding to a line hash and drop it on filing if the line changed** — FIX — value 3 — effort M — risk low — category: review
  Why: five recent findings were dropped as "already built" or "already fixed" (set_panic atomic write, fmscene lights, the cmd_scene FILE check). Each wasted a reviewer cycle and a user glance.
  Done when: a finding citing `file:line` plus a snippet is auto-closed as stale if the snippet is gone, and the close note names the commit that removed it.

- **Build commands through a guard-safe wrapper** — FIX — value 4 — effort M — risk low — category: guard
  Why: the review says the risk budget tripped on 6 blocks, mostly Foreman's own `$VAR` paths and `rm` on /tmp globs. Explaining the refusal after the fact is not enough; agents should construct only shapes the guard accepts. This is a typed `fm sh rm-tmp NAME` that resolves to literal paths.
  Done when: replaying the day's refused commands through the wrapper yields zero refusals, and a test shows the wrapper refuses the same cases the guard does.

- **Preview the rendered site diff before a push to main** — FEATURE — value 3 — effort M — risk med — category: site
  Why: "Push foreman/build to main so the site publishes" is a recurring ask, and a push to main is outward-facing and hard to undo. Build both versions locally and show changed pages as before/after screenshots.
  Done when: `fm site diff` lists pages changed between main and the build branch with paired screenshots, and prints "no visible change" when there is none.

- **Run a weekly canary on the next CI runner image** — FEATURE — value 3 — effort S — risk low — category: CI
  Why: the Ubuntu 26 failures (copied sleep dying, a zombie with no cwd) arrived as surprises. Assumption: GitHub exposes a beta or latest label to target.
  Done when: a scheduled workflow runs the suite on the newest image label and files one deduped task when it differs from the pinned image's result.

- **Fill gate and build waits with S-sized chores** — FEATURE — value 3 — effort M — risk med — category: lanes
  Why: pillar 1 says "never idle while a gate, build, pipeline or review runs". Assumption: waits are currently idle. Chores are limited to read-only work (stale-finding checks, doc-link checks, LOW-finding triage).
  Done when: a lane waiting on a gate longer than 60 s starts a read-only chore, and the chore never touches a leased file.

- **Record a reason code on every swipe skip** — FEATURE — value 3 — effort S — risk low — category: triage
  Why: the review notes that `prefer` never explains why one item outranks another, and a skip is a bare "no". One tap for too big, not now, wrong, or already done would let `prefer --why` speak.
  Done when: the served page and the TTY swipe both store a reason, and `fm inbox prefer --why T-xxxx` quotes it.

- **Use hesitation on swipe cards as a signal** — FEATURE — value 2 — effort S — risk low — category: triage
  Why: wild. Dwell time is free signal, kept on the user's machine. A long pause before a verdict suggests an unsure card, which resurfaces for a discussion line instead of being filed.
  Done when: cards decided after a threshold dwell are tagged "unsure", appear in a "revisit" tray, and no dwell data leaves the machine.

- **Slow bulk approvals when the verdicts come too fast** — SECURITY — value 3 — effort S — risk low — category: triage
  Why: wild. Pillar 3 builds "almost all" ideas in rounds, so a fast run of 40 "build" taps commits a lot of spend and a lot of guard-adjacent work without a real read. After N verdicts under about 1 s each, show the summed cost estimate and ask once.
  Done when: a scripted burst of 10 builds in 3 s triggers a single confirm card showing the total effort, and normal-paced use never sees it.
