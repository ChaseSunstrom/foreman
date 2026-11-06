# Brainstorm — lens: unspoken needs

- **Ship releases with one command** — FEATURE — value 5 — effort M — risk med — category: release
  Why: Seven of the last twenty requests are "Release 1.2.x" or "Foreman 1.2.x … to GitHub main and JARVIS". The user is hand-driving the same pipeline each time.
  Done when: `fm release` bumps the version, writes the changelog from merged tasks, runs the gates, tags, pushes, updates every registered consumer project, runs `fm doctor` in each, and prints a per-project pass/fail table.

- **Canary-gate releases with consumer replay** — FEATURE — value 5 — effort M — risk med — category: release safety
  Why: Most recent fixes came from JARVIS hitting guard and drive problems after a release: symlink rm, `fm focus; sed`, lane merge, tool caches. `fm replay` exists but isn't tied to the release.
  Done when: before a release is tagged, every registered project's last N sessions are replayed through the candidate guard and drive. Any newly refused command that was allowed before blocks the release, with the command listed.

- **Capture consumer-project friction as Foreman tasks automatically** — FEATURE — value 5 — effort M — risk low — category: feedback loop
  Why: Tasks are phrased "(JARVIS: …)" and written by hand after the user notices. T-0317 "There's new bug feedback" shows a half-built inbox. Assumption: consumer projects log guard refusals and retries in the ledger.
  Done when: a repeated refusal or a refusal followed by a retry in a consumer project creates a Foreman-side FIX brief with the command, the verdict and a failing test stub. The user sees it in the inbox without having typed anything.

- **Enforce cleanup as a done-gate obligation** — FEATURE — value 5 — effort M — risk med — category: discipline
  Why: The user steered "cleanup requests (repo, docs, briefs, dead code, replaced functionality) never got done — trace why and fix". Tasks that replace something don't record what became dead.
  Done when: a task flagged as replacing or superseding something can't pass `fm task done` until a sweep finds no remaining references to the old symbol, doc or brief. Otherwise it spawns a linked CLEAN task that stays on the queue.

- **Groom the queue and expire deferrals** — FEATURE — value 4 — effort M — risk low — category: queue health
  Why: Open work has many "deferred" items (T-0034, T-0035, T-0166, T-0214, T-0217…) with no revisit date. The drive was already caught idling with 20+ queued.
  Done when: each deferral carries a reason and a review date. Once the date passes, `fm next` asks to do, drop or re-defer it. Duplicates and tasks the code has made obsolete are proposed for closing with evidence.

- **Predict the user's approvals to ask less** — FEATURE — value 4 — effort L — risk med — category: autonomy
  Why: The user dislikes friction, and budget limits "shouldn't block anything until 75%". `fm taste` records kept, dropped and steered choices but only feeds brainstorms. Assumption: enough approval history exists to learn from.
  Done when: for L plans and `?` items, Foreman scores the likelihood of approval from past decisions. Above a threshold it proceeds and logs a revisable decision. Below it, it asks. A backtest on past approvals reports accuracy.

- **Red-team the guard unattended** — SECURITY — value 4 — effort L — risk low — category: guard
  Why: The guard has keep appearing gaps (`bash -lc`, `python -c` with fmcli, symlink rm, T-0275 script files) found only by use. Real-bash differential tests and a 5000-command replay already exist to build on.
  Done when: a night job has an adversarial subagent generate bypass attempts and benign-lookalike commands. It runs them against both the guard and real bash in a sandbox, and files minimized failing cases as tasks.

- **Generate product journeys from acceptance criteria** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: The user asked "Foreman checks the product the way its user uses it", and `fm smoke` only checks a headless browser at two viewports. Criteria are already written in each brief.
  Done when: `fm task done` for a UI task generates a scripted user journey from its criteria and runs it headless with screenshots attached as evidence. The journey is saved as a regression that `fm sentinel` re-runs.

- **Let projects request changes from each other** — FEATURE — value 4 — effort M — risk med — category: multi-project
  Why: JARVIS sessions hit Foreman limits and the user relays them by hand. Foreman Desktop already lists every project on the device.
  Done when: a session in project A runs `fm request <project> "…"`, which lands in B's inbox with a back-link. When B's task finishes and releases, A's session is notified and offered the upgrade.

- **Run the queue across machines** — FEATURE — value 3 — effort L — risk high — category: fleet
  Why: `fm serve`, `fm run` and `fm session` are all local. Assumption: the user owns more than one box and wants idle capacity used overnight.
  Done when: `fm run --on <host>` pushes a task's lane to a remote machine over SSH. Ledger events and evidence stream back, and the lane merges locally only after the gates pass.

- **Dogfood arena: seeded-bug projects scored by the discipline** — FEATURE — value 4 — effort L — risk low — category: self-eval — wild
  Why: `fm bench` replays real finished tasks. Real tasks can't cover failure modes that haven't happened yet, such as drive idling, stuck steps and cleanup skipped.
  Done when: a generated synthetic repo with a planted bug and a planted dead-code trap is run through Foreman end to end. A scorecard reports whether the fix, the cleanup and the evidence all happened, and compares against the previous release.

- **Replay a task under a different plan or model** — FEATURE — value 3 — effort L — risk med — category: counterfactuals — wild
  Why: `fm evolve` ablates instruction files, but no one can see whether a different step order or model would have finished the same task cheaper or better. Checkpoints already exist.
  Done when: `fm fork T-xxxx --model/--plan` re-runs from a chosen checkpoint in a lane. It outputs a diff of cost, gate results and diff size against the original.

- **Auto-write standing vetoes from the user's repeated steers** — FEATURE — value 3 — effort M — risk low — category: learning — wild
  Why: Steers such as "no blocking until 75%" and "subagents never capped by token count" are restated across sessions, and `fm vetoes` only records explicit ones.
  Done when: a repeated correction pattern across tasks is proposed as a veto or standing rule with its source quotes. One typed confirmation activates it, and it shows up in `fm vetoes`.

- **Keep a self-writing project handbook that tracks reality** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: T-0365 (a generated section from `fm map`) is deferred, and `fm docs` only reports drift. MASTER.md is the single source of truth for a 262-file project.
  Done when: the gates, layout and command list in MASTER.md are regenerated from code on release. Any hand-edited drift fails `fm docs`, and the release diff shows what changed.
