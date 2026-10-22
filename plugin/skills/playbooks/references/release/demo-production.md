<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Demo production: scripted, seeded, short

Use when making a product demo: a release video, a GIF for a README or pull request, a terminal recording, or a live
walkthrough. A demo is a claim about the product, so it is held to the same evidence rule as the code: it shows only
what the shipped build really does.

## The procedure

1. **Write the script.** One sentence the viewer should believe afterwards, then three to five beats, each with the
   action, what the viewer sees, and the line said or captioned. Budgets: a README or PR clip 30 s or less, a
   release video 2 minutes or less, a live demo 10 minutes or less. Pass: the script is a file in the repo and its
   beat timings add up within the budget.
2. **Seed the state.** A seed script builds the demo's data from empty: realistic but fake (names from a fixed list,
   `example.com` addresses, no customer data, no real keys). Pass: running it twice gives the same screen.
3. **Isolate the stage.** A demo account and a clean browser profile or terminal: notifications off, bookmarks bar
   hidden, plain prompt, history cleared, a fixed window (1280×720 or 1920×1080), text 16 px or larger as recorded.
   Any token the demo needs is scoped to it and revoked afterwards.
4. **Record from a script, not by hand.** Browser flows are a Playwright script (video recording on, a steady
   `slowMo`); terminal flows are a scripted recorder (a VHS tape or an asciinema run of a script). A UI change then
   means a rerun, not a reshoot. Pass: the recording's source script is committed next to the demo script.
5. **Cut the waiting, never the truth.** Pre-build and warm caches; trim dead air longer than a second. If a step
   was sped up or a slow external call stubbed, the demo says so on screen. Never show a result the build can't
   produce.
6. **Make it watchable without sound.** Captions for every spoken line, the cursor or key presses visible, nothing
   flashing more than three times a second. Ship MP4 or WebM; a GIF only if it stays under 5 MB.
7. **Have a fallback for live demos**: the recorded version of the same script, and the seed's reset command ready
   in a second window.
8. **Scrub before publishing.** Step through the frames for secrets, tokens, real names, internal URLs and
   notifications; check the version on screen matches the release. Pass: the check is a line in the release task's
   log.

## Checks

- [ ] The demo script is in the repo, with beats and timings within budget.
- [ ] The seed script rebuilds the same state from empty, with no real people or keys.
- [ ] The recording comes from a committed script (Playwright, VHS or asciinema).
- [ ] Every spoken line is captioned; nothing flashes more than three times a second.
- [ ] Any sped-up or stubbed step is labelled on screen.
- [ ] A frame-by-frame scrub found no secrets or personal data, and the version shown matches the release.

## Library cards

`fm lib show playwright` (scripted flows and video), `fm lib show test-data-factories` (the seed),
`fm lib show feature-flags` (hide unfinished paths), `fm lib show smoke-tests` (the build you show works),
`fm lib show video-transcoding` (MP4 and WebM output), `fm lib show accessibility` (captions, flashes).
