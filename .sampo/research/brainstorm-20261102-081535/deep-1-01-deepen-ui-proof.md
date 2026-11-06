# Brainstorm — lens: deepen: ui proof

- **Prove the shot is of the changed build** — FEATURE — value 5 — effort M — risk low — category: ui proof
  Why: the list has "prove the running thing is the changed thing" but stops at an idea. Grow it into a stamp: `fm shot` and `fm flow` read the served page's build hash (or the process's start time against the last file mtime) and refuse a pass when the screen came from a stale server, a cached bundle or a different port. The stamp is printed on every receipt.
  Done when: a test serves an old build, edits a source file, runs `fm shot`, and gets a "stale: served build predates change" refusal rather than a pass.

- **Make one proof record that unifies shot, flow, trace and masks** — FEATURE — value 5 — effort M — risk low — category: ui proof
  Why: baseline diffs, trace bundles, deterministic capture, learned masks and contact sheets are separate ideas that each need a store. Merge them into one `proof/<task>/` bundle (before, after, diff, mask, trace, a11y tree, build stamp, verdict) that every later idea writes into. The finish receipt links the bundle and nothing else.
  Done when: `fm task finish` on a UI task prints one bundle path whose manifest lists each artifact with its hash, and `fm proof show` opens it.

- **Judge "meant" by the user's own words, with each region tied to a criterion** — FEATURE — value 5 — effort L — risk med — category: ui proof
  Why: the request is "does it do what the user meant". Combine circle-the-change with tap-meant/not-meant: each changed region is mapped to the task criterion it should satisfy, and regions that map to no criterion are listed as "unrequested change". Taps are stored as labels; assumption: the user will tap only a few regions per task.
  Done when: a shot of a change that touched an unrelated header shows that region under "unrequested", and a tap on it is saved in the bundle.

- **Learn from the user's taps what to mask and what to flag** — FEATURE — value 4 — effort M — risk med — category: ui proof
  Why: learned volatile masks and "not meant" taps are the same signal. A region marked noise twice gets auto-masked; one marked "not meant" twice becomes a standing check on that screen. Reuses the bet ledger so mask confidence has a Brier score like other judgments.
  Done when: after two noise taps on a clock region, the next `fm shot` masks it and says so in the receipt with the count.

- **Score flakiness before trusting a pass** — FEATURE — value 4 — effort M — risk low — category: ui proof
  Why: deterministic capture, degenerate-capture refusal and demote-noisy-flow all ask whether a result is trustworthy. Run every flow N times at the start, record the pixel and assertion variance, and label a pass "stable 5/5" or "unproven: flaky 3/5". Matches the standing rule that what can't be proven gets labelled.
  Done when: a flow with a planted random animation is reported "unproven: flaky" and a clean flow "stable".

- **Run the same flow against a mutated app to prove it can fail** — FEATURE — value 5 — effort L — risk med — category: ui proof
  Why: a UI flow that passes on the broken UI proves nothing. Mirror `fm task prove` (test fails without the change): revert the change, rerun the flow and require it to fail, or inject mutations (hide a button, change a label) and require a catch. Reports flow "kill rate".
  Done when: a flow that checks nothing is reported "survived 3/3 mutations: proves nothing", and a good flow "killed 3/3".

- **Check the shot against the docs' screenshots and claims** — FEATURE — value 4 — effort M — risk low — category: ui proof
  Why: the sweep already compares site/README claims to exam lines. The site and README embed demo SVGs and screenshots; diff them against a fresh `fm shot` of the same screen and go red when the public image no longer matches the product.
  Done when: changing a label in foreman-ui makes the sweep name the stale README image path.

- **Cover surfaces beyond the browser: terminal and TUI frames** — FEATURE — value 4 — effort L — risk med — category: ui proof
  Why: foreman-ui lives in Claude Code's terminal and the pane's background bug (T-1217) came from a colour that only a cell-level capture shows. Capture the terminal as a cell grid with colours (via a pty and a vt emulator), diff and assert on it like a shot, and pin it per host release.
  Done when: a test asserts the pane's background cell colour and fails when it changes to #262626.

- **Wild: Replay the user's past sessions as visual regression tests** — FEATURE — value 4 — effort L — risk med — category: ui proof
  Why: wild. Journals already record what the user did and saw. Turn a finished session's clicks into a flow and its final screen into a baseline, so every real day of use becomes a regression test with no one writing it.
  Done when: `fm flow --from-session <id>` produces a runnable flow that passes on the unchanged build.

- **Wild: Let a second cold model describe the screen blind and compare to the goal** — FEATURE — value 4 — effort M — risk med — category: ui proof
  Why: wild. Matches the standing rule on signals Foreman didn't author. A different model sees only the screenshot and writes what it thinks the screen does; a diff against the stated goal catches "looks fine, does the wrong thing". Labelled as an opinion, never a pass.
  Done when: a shot of a screen missing the requested control gets a blind description that omits it, and the receipt flags the mismatch.

- **Wild: Time-lapse the build as a film for the user** — FEATURE — value 3 — effort M — risk low — category: ui proof
  Why: wild. Stitch each task's before/after shots and flow frames into a short looping clip on the site's Genesis page, so a week of work is watchable in 30 seconds, and a regression shows up as a visible jump.
  Done when: `fm proof film --week` writes a clip whose frames each trace to a task's bundle.

- **Report coverage of screens, not lines** — FEATURE — value 4 — effort M — risk low — category: ui proof
  Why: the UI state matrix and the shot per screen have no measure of what's untested. Walk the routes and components, list screens no flow has visited, and put "UI proof covers 9 of 14 screens" in `fm doctor`, naming the rest as unproven.
  Done when: removing a flow drops the doctor's count and names the screen it no longer covers.

- **Fail the proof when the page shouts in the console** — FIX — value 3 — effort S — risk low — category: ui proof
  Why: demote-noisy-flow needs a source of noise. Capture console errors, failed requests and uncaught exceptions during every shot and flow, attach them to the bundle, and downgrade a pass that made any.
  Done when: a flow on a page that logs one uncaught error is reported "passed with 1 error" and not plain pass.

Next question: Which proof artifacts has the user actually opened after a finish receipt, and does that record support a bundle this big?
Next question: When a UI check can't run (no display, no browser, headless CI), how does the receipt say "unproven" so it can't be read as a pass?
