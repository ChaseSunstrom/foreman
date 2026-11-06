# Brainstorm — lens: unspoken needs

- **Flash-safety lint for every animation** — FEATURE — value 4 — effort S — risk low — category: accessibility
  Why: The idea list proposes screen shakes, red ripples, flashes on verdicts, confetti and bursts, and none of them has a photosensitivity limit. assumption: the user wants motion that is safe to watch for hours. wild: no.
  Done when: a lint run on a fixture with 5 full-screen flashes in one second fails and names the frames. The same fixture at under 3 per second passes, in both the TUI clock and a generated CSS animation.

- **Turn a pasted ASCII mockup into a real layout** — FEATURE — value 4 — effort M — risk med — category: tui config
  Why: The user wants config from inside the TUI and "non generic" looks. Drawing boxes in text is the fastest way to say "panels here, this wide". wild.
  Done when: pasting a 3-box ASCII sketch into the settings screen shows a live preview of the matching `tui.toml` panel layout. Accepting writes the file, and a sketch that doesn't fit is refused with the reason.

- **Map taste words to token deltas** — FEATURE — value 4 — effort M — risk low — category: design vocabulary
  Why: The request is "non generic, good animations, styles". Words like calm, brutalist, snappy and heavy are how the user will actually ask. assumption: a small table of words to palette, easing, density and type-scale deltas can be written originally and tested. wild.
  Done when: `fm design nudge "calmer, less shouty"` changes only the named tokens in the DESIGN file and shows a before/after frame pair. Running it twice moves the tokens further, and `--undo` restores them.

- **Ship an offline font shelf with vetted pairings** — FEATURE — value 4 — effort M — risk med — category: typography
  Why: T-S24 requires fonts to be self-hosted with nothing loaded from third parties. The `typography` cards teach taste but give no fonts to use. assumption: OFL-licensed fonts can be bundled without breaking the stdlib-only rule, because they are data and not code.
  Done when: `fm design fonts` lists at least 12 pairings, each with licence text and a size cost. A scaffold using one passes the build's no-outside-host check.

- **Calibrate taste once with a 12-pair picker** — FEATURE — value 3 — effort M — risk low — category: personalization
  Why: The user hands down sweeping taste requests and can't review every frame. One sitting of choosing between pairs gives the critic and slop detector a stored preference. assumption: pairwise choice is less work than writing a style brief.
  Done when: `fm design taste` shows 12 pairs, saves a local profile, and a later design critique cites a pair as its reason ("you preferred sharp corners in pair 4"). The profile can be deleted with one command.

- **Reject duplicate proposals at capture time** — CLEAN — value 4 — effort M — risk low — category: queue hygiene
  Why: The "Ideas so far" list repeats the same ideas dozens of times (factory floor, replay scrubber, theme gallery, confetti). The deferred "Later from" tasks already number about 30. A recursive brainstorm without a novelty gate just inflates the queue.
  Done when: capturing a task whose text overlaps an open, closed or deferred task by n-gram score prints the nearest task id and asks to link or force. A round where more than 60% of proposals link to existing tasks suggests stopping.

- **Show the expansion of a vague sweeping request as a veto list** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: "etc. etc." and "super recursive" show the user is tired of enumerating scope. Foreman should list the clauses it inferred and let the user strike lines, not ask open questions. assumption: this builds on the existing clauses and mandate work and doesn't replace it.
  Done when: a request containing "etc." produces a numbered list of inferred clauses. Striking items by number removes them, and the remaining clauses are what the mandate records.

- **Probe headless rendering in `fm doctor`** — FEATURE — value 3 — effort S — risk low — category: visual proof
  Why: Screenshot proof of 3D and animation needs a browser and WebGL. The user runs a hardened Linux kernel, where GPU and sandbox access may be restricted. assumption: the screenshot tooling hasn't been checked on this machine.
  Done when: doctor reports headless browser, WebGL support, or software fallback as three separate lines. A UI task's proof step says "skipped: no WebGL" with the cause and never silently passes.

- **Require a "because" line on every design token** — FEATURE — value 4 — effort S — risk low — category: anti-generic
  Why: Generic UI comes from unexamined defaults. A token with no reason tied to the brief is a default in disguise, and the slop detector can flag exactly that.
  Done when: `fm check design` fails a DESIGN file where a color, font or easing token has no reason text. Adding a reason makes it pass.

- **Inspect why any element looks the way it does** — FEATURE — value 3 — effort L — risk med — category: observability
  Why: Hover or press `?` on a TUI cell or web element and see its token, its reason line and the task that last changed it. wild; assumption: the token to element mapping can be recorded at render time.
  Done when: in `fm code app`, pressing `?` on the focal line shows token name, value, reason and task id. An element with no token says "untokenized".

- **Take screenshots from a seeded fixture, never live data** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: Visual evidence for UI tasks would capture whatever the app shows, such as paths, emails and keys. The user is privacy-minded (passmail address, a stdlib-only, no-third-party stance).
  Done when: the shot loop refuses a page unless it is served from fixture data. A planted fake secret in a live-data run never appears in stored frames.

- **Pick one poster frame for every animated artifact** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: Animated SVGs and clips need a still for README previews, no-JS pages, social cards and reduced-motion users. wild; assumption: the most informative frame can be chosen by edge and color variance plus event markers.
  Done when: exporting a run writes `poster.png` alongside the animation. A recording with a failing-to-passing moment picks a frame that contains the verdict.
