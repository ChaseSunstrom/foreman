# Brainstorm — lens: unspoken needs

- **Catch secrets pasted into the prompt** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: bracketed paste into the prompt just shipped (T-1316), so logs, `.env` snippets and curl commands now land in the transcript in one keystroke. Earlier ideas fence secret paths and exports, not what the user pastes in. Assumption: a prompt-submit hook can see the text before the model does.
  Done when: submitting a prompt containing a fake `AKIA…` key or a `Bearer` token pauses with a masked preview, and the saved transcript holds the placeholder, not the secret.

- **Mutation-test the guard** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard has an evasion corpus for 24 commands (T-1263), but nothing shows that each rule is the one making its tests pass. Weakening a rule and finding the corpus still green would expose a rule that is never actually exercised.
  Done when: `fm guard mutate` weakens each rule in turn, reruns the corpus, and lists every surviving mutant; the release gate fails if any survive without an explicit waiver.

- **Alert when a repo's Claude config changes between sessions** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: T-1472 names a repo's hooks, MCP servers and allow rules once, at the first session. A later `git pull` can add a hook that is never named again. The review steers (apiKeyHelper, `enableAllProjectMcpServers`) show how much the user cares about this surface.
  Done when: after a pull that edits `.claude/settings.json`, the next session prints a diff of only the added or changed commands, warnings first, and stays silent when nothing changed.

- **Replay past review nits as a pre-review checklist** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the steers repeat patterns (the T-1405 nits 1–6, "skip it in headless runs", "show it to the user too", "commands in other settings keys are also commands"). Assumption: these recur across tasks and the user would rather not catch them by hand each time.
  Done when: before close, a reviewer lens checks the diff against a list distilled from the last N review steers and cites which past nit each finding matches; on a seeded diff that repeats an old nit, the finding appears.

- **Break approval fatigue** — SECURITY — value 3 — effort M — risk med — category: human factors — wild
  Why: assumption: with bypass mode and long unattended queues, the real hole is the human clicking "yes" in under a second. If several permission dialogs are answered faster than anyone could read them, the next one shows a plain-language summary and needs a typed word.
  Done when: in a scripted run, 5 approvals under 1.5 s each cause the sixth prompt to demand typed confirmation, and a slow, deliberate approval never triggers it.

- **Run a cold-reader test on the README and site** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: the pack's README text is dense with internal names (stations, lanes, slots), and the newcomer tour (T-0862) is deferred for lack of evidence. A context-free child can produce that evidence cheaply.
  Done when: `fm docs coldread` gives a no-context child only the README and site, asks "what is this for and what is the first command?", and scores the answer against a stated one-sentence purpose; a fail lists the confusing terms.

- **Add `fm doctor --wrong <check>` to appeal a false alarm** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the user keeps hitting false positives and transients (supply check vs in-use markers, canary flakes, the reverted auto-accept). Today each costs a manual round trip to explain.
  Done when: the command snapshots the check's inputs and output into a task that cites the evidence, and the same check, unchanged, then shows "appealed, T-nnnn" instead of repeating the alarm.

- **Require a renewal for unattended runs** — SECURITY — value 3 — effort M — risk med — category: autonomy — wild
  Why: assumption: `fm night` and long `fm code` runs are the widest-open window. An unattended lease (touch a file, tap a phone link, or answer a notification every N hours) downgrades the run to read-only when it lapses, so a forgotten run can't keep writing for days.
  Done when: letting the lease lapse in a test moves the run to read-only, with a journal line saying so and a one-command renew.

- **Keep a prediction ledger with a calibration curve** — FEATURE — value 3 — effort M — risk low — category: estimates
  Why: the pack's ideas include forecasts (cost, finish time, ghost of past runs) but nothing records whether they were right. A ledger of each guess against the outcome tells the user when to trust an estimate.
  Done when: `fm calibrate` prints predicted vs actual for the last 30 tasks, and a task with no prediction is marked "no estimate" rather than defaulted.

- **Generate a good-first-task list from the backlog** — FEATURE — value 3 — effort S — risk low — category: contributors
  Why: the repo has a CI badge and a public GitHub home, and about 30 deferred "Later from…" tasks. Few of them carry a ready verify command, so an outsider can't tell which are safe to pick up. Assumption: outside contributors are a goal (T-0352 is about publishing).
  Done when: `fm good-first` lists only tasks with a written failing verify command, a scope of 3 files or fewer, and no blocked dependency, and each links to its test.

- **Read the morning digest aloud** — FEATURE — value 2 — effort S — risk low — category: voice — wild
  Why: assumption: the digest and "needs you" lists already exist as text. Speaking the one-sentence version through a local text-to-speech engine (espeak or piper, only if installed) suits a kitchen or a drive. Dictation is covered by earlier ideas, but speech output is not.
  Done when: `fm digest --say` pipes a generated summary of 40 words or fewer to the installed engine, makes no network call, and prints "no speech engine found" instead of failing.

- **Render a desk card for a spare e-paper or old phone** — FEATURE — value 2 — effort S — risk low — category: ambient display — wild
  Why: phone LAN status pages are already proposed, but a 400×300 black-and-white SVG written to a file works on anything that can show an image. It would show queue depth, one "needs you" line and the last proved task.
  Done when: `fm card --out card.svg` writes a deterministic SVG under 20 KB that stays legible in grayscale at 400×300, and a golden-file test covers it.
