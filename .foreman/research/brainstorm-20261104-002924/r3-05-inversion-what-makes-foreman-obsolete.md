# Brainstorm — lens: inversion: what makes Foreman obsolete

Inversion lens: if Foreman should be obsolete, the lean work is making each capability prove it still earns its place, with a defined exit. The pack's evidence: 2,733 characters injected twice at session start, a 75,758-token MASTER.md the Read tool refuses, 2.4 GB of state, and 48–76 characters per turn. I haven't repeated anything from the ideas-so-far list.

- **Move discipline from injection to a post-hoc transcript audit** — FEATURE — value 4 — effort M — risk med — category: lean
  Why: assumption: most per-turn and session-start text exists to steer the model *before* it acts, but a Stop-time audit of the transcript could check the same rules afterwards for zero context cost. The 48–76 characters per turn is the burden it would remove.
  Done when: with injection off and audit-only on, `sampo exam` shows the same Ward-block and plan-before-edit catch rates on the held-out scenarios, and the per-turn character count is 0.

- **Make MASTER.md a build artifact, not a committed file** — CLEAN — value 4 — effort M — risk low — category: docs
  Why: the 75,758-token file can't be Read and has to be hand-sharded. Generating it at install from verb docstrings and the skills' `SKILL.md` files means the repo never holds an unreadable doc, and the doc cannot drift from the code.
  Done when: the repo has no `MASTER.md`, `sampo doc` is generated from code, and a test fails if any generated section exceeds the Read ceiling.

- **Fade nudges per user once the habit is unprompted** — FEATURE — value 3 — effort S — risk low — category: scaffolding
  Why: assumption: some users already plan before editing. If the user wrote a plan unprompted in N consecutive sessions, that nudge class stops injecting and an instrumented counter watches for regression.
  Done when: a fixture ledger with 10 unprompted-plan sessions yields no plan nudge on session 11, and a regression session brings the nudge back.

- **Skip ceremony the user's own CI already enforces** — PERFORMANCE — value 3 — effort M — risk med — category: overlap
  Why: the gates (`fm doctor`, `roundtrip.py`, `bench_hooks.py`) overlap what a workflow file usually runs. Reading `.github/workflows` lets `prove` skip a command CI proves identically, while still running it for what CI misses.
  Done when: on a repo whose CI runs the same test command, `sampo task prove` prints "covered by CI: <job>" and spends no tokens on it. The skip is withdrawn if the CI job is absent.

- **Require every injected line to carry an expiry** — CLEAN — value 4 — effort S — risk low — category: lean
  Why: the double SessionStart injection shows text gets added and never re-justified. Each injected line gets an owner, an outcome it changed and a 30-day expiry. Unrenewed lines drop out of the build.
  Done when: the ship gate fails if any hook-emitted line lacks a petition record, and a line with a lapsed expiry is absent from the next session-start text.

- **Run a "ten-line Sampo" duel** — FEATURE — value 4 — effort M — risk low — category: necessity
  Why: assumption: a minimal competitor of a CLAUDE.md block, a few host deny rules and a pre-commit hook might capture most of the value. Generate it from the repo and run both arms on the held-out scenarios. Any capability the competitor matches gets a deletion task.
  Done when: `sampo exam duel-minimal` prints per-capability win, tie and loss against the generated kit, and each tie files a retire task.

- **Downgrade the Ward to audit-only when the host enforces it natively** — SECURITY — value 3 — effort M — risk high — category: guard
  Why: assumption: once the host's own permission rules pass the Ward exam, running the Ward as a hook adds latency and a second attack surface. Audit-only mode keeps the exam and a logging tripwire but drops the blocking path. The downgrade is tighten-only reversible.
  Done when: with native deny rules installed and exam-passing, the Ward hook goes to log-only and the exam still fails on a planted bypass.

- **Keep a "needed share" in doctor, with a Lite recommendation** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: a single number such as "gates changed an outcome in 3 of 140 closes this month" tells the user whether they still need the full install.
  Done when: `sampo doctor` prints the share, and below a threshold it names the one command that switches to the Lite profile.

- **Wild: make the product a 4 KB seed prompt** — FEATURE — value 3 — effort L — risk med — category: moonshot
  Why: wild. The reverse of obsolescence is Sampo as a prompt a future model uses to rebuild the discipline in any repo at first run, with no program installed. The seed is scored by whether the rebuilt discipline passes the exam.
  Done when: a cold child given only the seed and an empty repo produces a working plan, prove and Ward loop that scores within 10% of the installed arm.

- **Wild: have a rival harness write the obsolescence report** — RESEARCH-style FEATURE — value 3 — effort M — risk low — category: necessity
  Why: wild. Run Codex or Gemini CLI through the exam with no Sampo, then have it list which capabilities it considers unnecessary and why. The cross-vendor view is a signal Sampo didn't author.
  Done when: a dated file lists each capability with the rival's verdict and quoted reason, linked from `sampo louhi`.

- **Wild: stage a "host catch-up day" each quarter** — FEATURE — value 2 — effort S — risk low — category: roadmap
  Why: wild. On a fixed date, disable every capability that has a host-native equivalent the previous quarter's release notes mention, and run the user's real work for one day. Report what was missed.
  Done when: the run produces a one-page "missed / didn't miss" list per capability and files a retire task for each "didn't miss".

- **Measure the cost of having the fallback ready** — PERFORMANCE — value 2 — effort S — risk low — category: lean
  Why: assumption: keeping compatibility shims (the thin `foreman` and `foreman-ui` plugins, renamed env vars) costs hook time and injected text, even though renames are meant to be permanent. Time them.
  Done when: `bench_hooks.py` prints the overhead of the shim path separately, and a ratchet blocks it from growing.

Next question: which of the capabilities listed in `sampo exam` has a measured advantage over the bare model that has *grown* rather than shrunk across the last three model releases?

Next question: what does a user lose on the day they run `sampo off` for a week that no existing gauge would show them?
