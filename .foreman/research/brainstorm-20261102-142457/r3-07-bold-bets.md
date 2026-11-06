# Brainstorm — lens: bold bets

- **Run learned fixers and rules in a WASM sandbox** — SECURITY — value 4 — effort L — risk med — category: sandbox
  Why: assumption: the backlog proposes auto-evolved guard regexes, one-signature fixers and learned rules, all of which would be code or patterns written by a model and run on the user's machine. T-0791 is the open injection-defense work.
  Done when: a learned fixer that tries to open a file or socket fails inside the runtime, and a test records the denial.

- **Store lessons as typed facts, not prose** — SECURITY — value 4 — effort M — risk low — category: injection
  Why: assumption: lessons are re-injected into later sessions as text, so one poisoned line written once persists and is replayed. Rendering from a closed schema (symbol, claim, evidence id, expiry) removes free-form instructions at storage time.
  Done when: a lesson containing "ignore previous instructions" is rejected at write, and the recall output contains only schema fields.

- **Make a revoke-only watchdog agent** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: assumption: the drive and lanes can burn money or loop unattended, and the existing stop ideas are rules inside the same process. A separate sub-agent that reads only the ledger and can only pause, freeze or revoke a grant is easy to trust because it can never build.
  Done when: in a fixture where a lane repeats a no-progress loop, the watchdog pauses the drive, and a test shows its toolset contains no write verb.

- **Watch the host's release notes for features it now does natively** — CLEAN — value 4 — effort M — risk low — category: lean
  Why: the pack's backlog repeatedly names host features (native deny rules, prompt/agent hooks, a native todo list, scheduled tasks) that overlap Foreman verbs. Foreman only probes for upstream breakage, not for upstream replacing it. The watch reads each release note and files a retire-or-wrap task naming the Foreman verb or hook it overlaps.
  Done when: given three recorded release notes, it outputs a list that names at least one overlapping verb or hook for each overlap and files CLEAN tasks.

- **Declare an effect class in each skill's frontmatter** — SECURITY — value 4 — effort L — risk med — category: skills
  Why: `plugin/skills` holds 1,388 of about 2,125 files. A class (read, repo-write, outward) lets a lint fail any skill whose text names a command above its class, and lets the runtime refuse an out-of-class call.
  Done when: a seeded skill declared read that says "run git push" fails `fm check`.

- **Make the UI propose and the CLI dispose** — SECURITY — value 4 — effort M — risk low — category: ui
  Why: assumption: the web UI and Desktop can act, and the backlog has DNS-rebinding hardening on it. If the UI has no write endpoint at all and every button renders the exact `fm` command to run or confirm, there is no write route left to attack, and a UI-driven action goes through the same gates as a typed one.
  Done when: a scan of the web server shows only GET routes, and clicking Approve shows a copyable command and changes no state.

- **Put a blast-radius thermometer on the pane and status line** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: the pane is thin on safety signal. A cool-to-hot bar from what the session has touched (read-only, repo writes, outside-repo writes, outward effects) makes bypass mode felt, not stated.
  Done when: a fixture session that writes outside the repo turns the bar to its top state and the screenshot differs from the read-only one.

- **Map agent-written lines nobody has read** — SECURITY — value 3 — effort M — risk low — category: review
  Why: assumption: cold reads and the ship gate check the diff in front of them, not the long tail. Per-file authorship plus blast radius gives a review budget; ship warns when a high-blast file has only agent-written, never cold-read lines.
  Done when: `fm doctor` lists the top five such files and the list changes after one cold read of the first.

- **Hold an intent-class jury for irreversible commands** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: the guard decides on command shape. For the irreversible class only, three tool-less small models from different vendors each judge a rendered effect summary and all must agree. This is rarer and cheaper than a full review.
  Done when: a planted benign-looking `find -delete` variant is held with a stated effect, and a plain `ls` never spawns a juror.

- **Wild: Run a reputation auction among sub-agents** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: wild. Each specialist bids estimated tokens for a queue item, the cheapest credible bid wins, and overruns lower its next ceiling. Outcome survival feeds the reputation, so routing is learned from results and not set by hand.
  Done when: over a replay of 30 closed tasks, the auction picks an assignment, and a lane that overruns twice has a lower cap in the next run.

- **Wild: Give Foreman a dead-man's twin on another machine** — SECURITY — value 3 — effort M — risk low — category: liveness
  Why: wild. A 50-line script on a phone or second box expects a signed heartbeat from the drive and the guard and alerts when either is silent for a set time, so a dead tower is noticed from outside the machine it died on.
  Done when: stopping the heartbeat for the set interval raises an alert, and resuming clears it.

- **Wild: Hold a nightly "delete it and see" race on the costliest code** — PERFORMANCE — value 3 — effort M — risk low — category: lean
  Why: wild. A scratch copy has the top 20% of modules by size or hook time stubbed one at a time. Any stub that leaves the gate and exam green is a deletion candidate with its evidence attached.
  Done when: the race lists a planted dead module as safe and a live one as breaking.

Next question: which of Foreman's own outputs do the user's other harnesses (Codex, Gemini CLI, opencode) read as instructions rather than data, and what does that let a poisoned ledger line do there?
Next question: when the user types a command after a Foreman verdict to check it, which Foreman component could have predicted that command and handed over its result?
