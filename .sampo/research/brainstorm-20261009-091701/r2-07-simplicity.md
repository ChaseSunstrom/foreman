# Brainstorm — lens: simplicity

Round 2, simplicity lens. Most of the obvious subtraction ideas (command tree collapse, nightly subtraction, one-page contract, folded log) are already listed. These aim at removing the need for the user to know or configure anything, and at shrinking Foreman's own core.

- **Add a single rigor dial** — FEATURE — value 5 — effort M — risk med — category: config
  Why: assumption: gates, tiers, autonomy, reviewers, asks and budget are separate knobs across 70+ commands. The user steered "budget/pace limits shouldn't block until 75%", which is one preference hand-wired into one subsystem.
  Done when: `fm rigor 1|2|3` sets every one of those from a single table, and `fm rigor` prints which concrete settings each level changed.

- **Infer the whole init from the repo and history** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: `fm map` already finds gates, layout and tests. `init`, `autonomy`, `sensitive` and `notify` still need manual choices (assumption).
  Done when: `fm init` on a fresh repo asks at most one confirmation, shows the inferred gates, rigor and sensitivity, and the first task runs without further setup.

- **Add `fm pause` as a visible kill switch** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user's repeated complaints are Foreman refusing things (guard refusals on JARVIS, "refused twice in a row"). There is no cheap way to answer "is this Foreman's fault?" without uninstalling.
  Done when: `fm pause` makes every hook a no-op with a band indicator, logs the pause to the ledger, and `fm resume-all` restores hooks. A test proves the guard passes a blocked command while paused.

- **Derive task tier from the diff, not the declaration** — FEATURE — value 4 — effort M — risk med — category: classification
  Why: gates depend on declared type and tier (`fm gates` is by type and tier). A declared S that touches the guard is under-gated. Assumption: classification errors have occurred.
  Done when: `fm task done` computes the effective tier from the changed paths, uses the stricter of declared and derived, and says why when it overrides.

- **Make the guard a declarative policy table** — CLEAN — value 4 — effort L — risk high — category: guard
  Why: recent commits patch the guard one case at a time (T-0414, T-0421, T-0422, the `bash -lc` cluster fixed inline in `_shell_c`). Each fix grows code. Assumption: most fixes are expressible as rows of command pattern, verdict and example.
  Done when: rules live as data rows, each with an allowed or blocked example. The 5000-command replay and the real-bash differential tests pass unchanged, and a new rule is added without editing parser code.

- **Ship Foreman as one self-contained binary** — FEATURE — value 4 — effort L — risk med — category: distribution
  Why: install needs Python 3.12.7+ and may need Homebrew or `uv`. Native Windows is unsupported. Desktop distribution is also blocked (T-0352).
  Done when: a single downloaded file runs `fm doctor` green on a machine with no Python, and `install.sh` skips the Python step when the file is used.

- **Extract a tiny portable kernel for the adapters** — CLEAN — value 4 — effort L — risk med — category: architecture
  Why: Codex, Gemini and opencode need separate adapters and each is separately blocked (T-0335, T-0336, T-0337). Assumption: the discipline (decide on event and state, return allow, deny or inject) is the same underneath.
  Done when: one pure `decide(event, state) → action` core is covered by table tests. Each adapter is a shim of under N lines that only translates events, and the Gemini deny-discards-answer case is a table row.

- **Add `fm less` to remove the thing that bothers you most** — FEATURE — value 4 — effort M — risk low — category: adaptive
  Why: the user's drops and steers (a loosened budget gate, brief-gate friction, repeated refusals) show tolerance is learned, not configured. Wild.
  Done when: `fm less` names the single rule, nag or refusal that fired most while being overridden or retried in the last N days, proposes demoting it, and applies it only on a typed yes.

- **Wild: Add a "was it Foreman?" differential rerun** — FEATURE — value 3 — effort L — risk med — category: diagnosis
  Why: assumption: when a downstream project like JARVIS reports trouble, finding out whether Foreman caused it is manual. Wild.
  Done when: given a recorded session step, `fm blame-self` replays it with hooks off and on in a lane and reports which difference, if any, changed the outcome.

- **Wild: Run a "silent unless needed" mode with a measured output budget** — FEATURE — value 3 — effort S — risk low — category: noise
  Why: assumption: band, pane, statusline, drive offers and hook text all compete for attention. Wild because the aim is invisibility.
  Done when: in silent mode, a normal task emits zero Foreman text except blocks and the final receipt, and a test counts injected tokens per turn against a stated ceiling.

- **Wild: Make Foreman a ~200-line spec a fresh model can rebuild** — FEATURE — value 3 — effort L — risk med — category: self-hosting
  Why: `BUILD_PROMPT.md` and `--build` already exist. Wild: compress the discipline to the minimum that still passes `fm bench`.
  Done when: a rebuild from the short spec passes the e2e roundtrip, and the gap in bench score against the full build is reported.

- **Generate MASTER.md sections from code** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: `fm docs` only reports drift. The command list, hook list and file map are derivable from `fm help`, hook registration and `fm map`.
  Done when: running `fm docs --write` regenerates those sections, and the doctor gate fails if committed sections differ from generated ones.

- **Report settings that nobody changes** — CLEAN — value 2 — effort S — risk low — category: config
  Why: `fm usage` covers commands, not settings (assumption). Unchanged knobs are candidates to hardcode.
  Done when: `fm usage --settings` lists each setting with its change count across registered projects and flags those never changed.
