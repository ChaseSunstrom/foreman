# Brainstorm — lens: user value

- **Ship an Arch AUR package for Foreman** — FEATURE — value 4 — effort M — risk low — category: distribution
  Why: assumption: the owner runs Arch (T-0325 already needs `sudo pacman -S libappindicator-gtk3`), and `install.sh` is the only install path in the pack.
  Done when: `makepkg -si` in a clean Arch container installs `fm`, `fm doctor` passes, and `pacman -R` leaves nothing in `/usr` or `~/.claude`.

- **Tag every Genesis generation and offer a one-command rollback** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: the tower rewrites itself every generation, and the standing rules say nothing is killed without a recorded reason. The pack shows no way to return to a known-good generation if a later one regresses.
  Done when: `fm genesis rewind 2` restores the code and tower files of gen 2 on a scratch branch, and the exam arms that run for free pass on it.

- **Gate the site on accessibility, links and weight** — CLEAN — value 3 — effort S — risk low — category: site
  Why: the standing rule publishes `site/genesis` to main automatically, with nothing in the pack checking what ships. The Genesis page is the public face of the project.
  Done when: the ship gate fails on a planted broken link, an image without alt text, or a page over a byte budget.

- **Export deferred tasks as contributor-ready issues** — FEATURE — value 3 — effort S — risk med — category: community
  Why: about 40 deferred or blocked tasks (T-0788 to T-0869) carry a brief and a "later: needs…" reason. The repo has a public GitHub and CI badge. This is outward-facing, so it needs a publish grant.
  Done when: `fm issues --dry-run` prints N issues, each with context, a done-when command and a blocker note, and nothing is posted without the grant.

- **Run a hardened-kernel verb matrix** — SECURITY — value 3 — effort S — risk low — category: portability
  Why: the host is `7.2.10-hardened1`, where user namespaces and similar primitives are often restricted. Sandbox, lane and `fm code` verbs may degrade silently.
  Done when: `fm doctor --host` lists each verb as full, degraded (with the cause), or unavailable on this kernel, and a test fakes a disabled userns.

- **Seal the final-report forecast at generation 0 and score it at the end** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the user steered to never block and to wait out limits, so the end-of-run report is where they judge the whole run. A prediction made up front, of what will and won't be built, gives the report a baseline.
  Done when: the report has a "predicted vs actual" table that reads from a hash-stamped forecast file written at gen 0.

- **Mine `fm ask` timeouts to learn which questions were not worth asking** — FEATURE — value 3 — effort M — risk low — category: attention
  Why: the standing rule says to pick the option closest to gen-0 and record it rather than ask. Questions the user answered with "whatever you think" are evidence of over-asking.
  Done when: a report lists question classes where the user's answer matched Foreman's default more than 90% of the time, with a proposed auto-decide rule for each.

- **Wild: Foreman Wrapped** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. A local-only, shareable year-in-review image or page built from the ledgers: held-rate, guard saves, closes, dollars per close, and the largest thing deleted.
  Done when: `fm wrapped` writes one self-contained HTML file with no network requests and no secrets, and a test scans it for both.

- **Wild: Dry-run the user's day on yesterday's ledger with a candidate steer applied** — FEATURE — value 4 — effort L — risk med — category: steering
  Why: wild. The user adds a steer almost every day and each one persists. A replay showing which of yesterday's decisions would have changed lets them judge a steer by its effect.
  Done when: `fm decide --preview "<steer>"` prints how many past events would have been affected, with three example diffs, without storing the steer.

- **Wild: A "stop-the-line" word the user can type in any pane** — FEATURE — value 4 — effort M — risk med — category: control
  Why: wild. Long unattended runs and parallel lanes make the main fear a runaway the user cannot interrupt quickly. One typed word would freeze lanes and unattended pushes and summarise state.
  Done when: typing `halt` in the Foreman pane stops the drive and lanes within 5 seconds, and `fm resume` restores them from the recorded state.

- **Wild: Test whether every standing rule would survive its author's absence** — CLEAN — value 3 — effort M — risk low — category: steering hygiene
  Why: wild. Fifty or so steers refer to "user steer 2026-10-31 #2" and similar. A cold child that sees only a rule's text should be able to tell when it applies, and a rule it can't read the same way twice is ambiguous.
  Done when: two cold readers classify 10 sample situations for each rule, and a rule with under 90% agreement is listed for rewording.

- **Show each task's cost against the user's review time on the finish card** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: the user cares about the human minutes a closed task costs them as well as the dollars. The ledger has timestamps for finish and next user message.
  Done when: the finish card prints dollars, agent minutes and an estimate of user review minutes, and a test checks the estimate against fixture timestamps.

Next question: which of Foreman's outward-facing artifacts (site, README, GitHub issues, packages) does a stranger actually see first, and is any of it checked before it publishes?
Next question: which steers does the user restate in different words across weeks, suggesting the stored rule isn't the one they meant?
