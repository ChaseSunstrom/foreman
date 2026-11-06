# Brainstorm — lens: unspoken needs

- **Give every blocked task an unblock probe** — FEATURE — value 4 — effort S — risk low — category: queue
  Why: T-0316, T-0325, T-0335, T-0336, T-0337, T-0352 and T-0418 are blocked on things only the user can do (`sudo pacman`, a Claude Code update, a publish step, an account). Nothing notices when they are done, so the work sits.
  Done when: `fm task block` accepts a probe command, and the next `fm next` or drive tick flips a task to queued once the probe passes, logging the event, with a test using a fake probe.

- **Run projects on release channels** — FEATURE — value 4 — effort M — risk med — category: release
  Why: 1.2.8 to 1.2.16 shipped within days to "GitHub main and JARVIS". The session that edits Foreman also runs on it, so a bad edit can lock out its own fix. A `stable` channel (the last release that passed consumer replay) and an `edge` channel (HEAD), with the Foreman dev session pinned to stable, would give a one-command rollback. Assumption: install.sh can keep two checkouts side by side.
  Done when: `fm channel stable|edge` switches a project's wiring, and a deliberately broken edge hook leaves a stable-pinned session fully working.

- **Make intake read pasted transcripts and reproduce first** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: the user relays consumer symptoms with the evidence in parentheses ("JARVIS: 'fm focus T-0278 …; sed -i …' refused twice"). Today those become briefs by hand.
  Done when: pasting a session excerpt into `fm capture` extracts the failing command, replays it through the guard in a scratch dir, and attaches a red repro result to the brief, or says why it could not reproduce.

- **Sweep a fix across its sibling sites** — FEATURE — value 4 — effort M — risk low — category: fix quality
  Why: the fixes arrive one case at a time. T-0408 added tool caches to `lane rm` after JARVIS hit them, T-0409 fixed one refusal message, and the symlink `rm` fix came from one builder. Each is a class of defect found by a consumer.
  Done when: closing a FIX task runs a sibling check that lists structurally similar sites (other refusal strings, other cache names, other path-removal branches) and requires each to be fixed, tested or waived, shown in `fm tour`.

- **Test refusal messages with a cold reader** — FEATURE — value 4 — effort M — risk low — category: guard UX
  Why: a refusal that told the agent to run `fm task new` instead of resuming T-0278, and a builder refused twice in a row for chaining `fm focus` with `sed`. The wording misled a reader.
  Done when: a fixture-driven eval gives a cheap model each refusal plus context and checks it picks the right next command; failing messages are listed by `fm doctor`.

- **Detect the XY problem at intake** — FEATURE — value 4 — effort M — risk med — category: intake (wild)
  Why: assumption: the stated request is often a symptom (an idle JARVIS session led to "offer queued work", then to "long-lived jobs never idle", then to a "drive" redesign). Foreman could compare a request with recent ledger and friction evidence and say "this looks like the same cause as T-0401/T-0412; fix that instead?"
  Done when: on a fixture with two prior symptom tasks sharing a root cause, a new request gets a one-line "likely root cause" note with links, and it never blocks capture.

- **Cut releases from a clean throwaway worktree** — FEATURE — value 3 — effort M — risk low — category: release
  Why: the user asks "Release 1.2.N" while the main checkout is mid-task. Lane merge already had to learn to cope with a dirty main (T-0403).
  Done when: `fm release` builds, tests and tags from a fresh worktree of `main` with a dirty main checkout, leaving the dirty files untouched.

- **Close a release only when consumers have run it** — FEATURE — value 3 — effort S — risk low — category: release
  Why: "to GitHub main and JARVIS" means two targets, but nothing proves JARVIS's next session loaded the new version.
  Done when: hook events carry the Foreman version, the release task lists consumers as pending, and each flips to confirmed on its first session event at that version.

- **Distil consumer repo shapes into synthetic fixtures** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: the real-world failures were shape problems: a `node_modules` symlink to the main checkout, tool caches in lane worktrees, many queued tasks, and a dirty main. Assumption: a shape fingerprint (symlinks, cache dirs, queue size, worktree count) can be extracted without any content.
  Done when: `fm map --shape` outputs a content-free fingerprint, a generator builds a repo from it, and the lane and guard tests run against at least one generated shape.

- **Audit lane writes that pass through symlinks** — SECURITY — value 3 — effort S — risk low — category: lanes
  Why: a JARVIS builder's `node_modules` was a link into the main checkout. A write through such a link lands in main, bypassing the lane's isolation.
  Done when: a test writing through a lane symlink to main is flagged at the PostToolUse hook or merge, while writes to ordinary lane files pass.

- **Keep an effort ledger by origin** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: tasks from self-improvement passes (friction, evolve, brainstorm) compete with user-requested ones, and the user has already pushed back on the budget crowding out work. They never see the split.
  Done when: each task is tagged user, self or consumer, and `fm digest` shows the share of tasks and tokens per origin, with a warning past a configurable ratio.

- **Wild: Give each consumer project an ambassador** — FEATURE — value 3 — effort L — risk med — category: multi-project (wild)
  Why: assumption: a persistent per-project profile (its quirks, past refusals, symlinks, preferred gates) lets a small agent review each Foreman release as that project and file objections before the user finds them.
  Done when: before a release closes, each registered consumer's ambassador runs its project's replay and either approves or files a brief citing a concrete failing case.

- **Wild: Collect a candid state of the union from each consumer** — FEATURE — value 3 — effort S — risk low — category: feedback loop (wild)
  Why: assumption: sessions in JARVIS hold the best view of where Foreman gets in the way, but it only reaches Foreman when the user relays it. Once a week, a headless agent re-reads recent transcripts and writes a one-page "what slowed me down" with quotes.
  Done when: `fm night` writes a dated report per project into the central inbox, and each distinct complaint is captured as a draft brief.
