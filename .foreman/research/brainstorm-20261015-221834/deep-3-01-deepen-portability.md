# Brainstorm — lens: deepen: portability

- **Ship a git-native brain with a custom merge driver** — FEATURE — value 5 — effort L — risk med — category: portability
  Why: the user steered that "fixes must travel with git so other sessions/clones/teammates use them"; T-1032 stores hints but concurrent edits from two clones will conflict as plain text. Prior ideas: merge driver and `.foreman/known/` bundle (combined here).
  Done when: two branches each add a different known-fix hint to the same file, `git merge` completes with no conflict markers, and `fm doctor` shows both hints loaded.

- **Split learned state into repo-scope and machine-scope with explicit promotion** — FEATURE — value 5 — effort M — risk low — category: scope
  Why: the user asked for "project fixes in the repo, machine-wide ones in Foreman state". Assumption: today there is no promotion path between the two.
  Done when: `fm known promote <id> --to repo|machine` moves a hint, and a fresh clone sees repo-scope hints while another project on the same machine sees only machine-scope ones.

- **Add a hint provenance and trust ledger** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: hints pulled from git steer an agent running in bypass mode; T-0791 (injection and supply-chain defenses) is already deferred. A teammate's or attacker's hint is a prompt injection route.
  Done when: a hint added by a commit not signed or approved locally is shown as "unreviewed" and is not auto-applied until `fm known trust` is run; a test covers an unreviewed hint being skipped.

- **Make resume state a committed handoff file per worktree** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: the user asked for easy resume of stopped worktree builders (T-1028). A `.foreman/handoff/T-xxxx.json` (task, brief, branch, last step, open questions, next command) pushed with the branch lets any clone resume.
  Done when: after `git clone` and checkout of a builder's branch on a fresh machine, `fm resume T-xxxx` restores the brief and step position without the original machine's state.

- **Wild: Hand off a running agent between machines via a git ref** — FEATURE — value 4 — effort L — risk high — category: handoff
  Why: wild. Pushes `refs/foreman/handoff/T-xxxx` holding the worktree diff, handoff file and a transcript digest, so a laptop session continues on a desktop or a cloud lane (relates to T-0793).
  Done when: `fm handoff push` on machine A and `fm handoff pull` on machine B yield an identical working tree and a resumed builder that passes its next step.

- **Export a hint pack as a shareable, versioned bundle** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: the card library (1,084 cards, 6 ever fired) and the fix hints are valuable across projects. A signed `.fmpack` file or git URL could be imported to seed a new project.
  Done when: `fm pack export` then `fm pack import` into an empty repo reproduces the same hints, and import refuses a bundle with a mismatched checksum.

- **Wild: Let a clone inherit the learned brain with one `git pull`, with a "what I learned since you were gone" digest** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: wild, from the previous list. A SessionStart line summarises new hints, lessons and vetoes pulled from git (supports T-0862 newcomer tour).
  Done when: after a pull that brings in 3 new hints, the next session's start shows exactly those 3, and not again on the following session.

- **Run gates under an environment matrix, including "no claude on PATH" and the native install path** — FIX — value 4 — effort M — risk low — category: portability
  Why: several recent asks were environment breakage: claude only at `~/.local/bin`, tests reaching the paid binary after the T-0990 fallback, PATH-faked lockouts.
  Done when: `fm doctor --matrix` runs the roundtrip gate with PATH variants (none, native-only, stripped) and every cell passes without invoking the real binary, which a canary test asserts.

- **Detect hint staleness against code drift** — FEATURE — value 4 — effort M — risk low — category: hygiene
  Why: a hint fixed against one version of a repo can be wrong after a dependency or file move; shared hints will outlive their context. Assumption: hints record a trigger signature but not a file or dependency fingerprint.
  Done when: a hint stores the lockfile and path fingerprint it was learned under, and `fm known check` flags one whose fingerprint no longer matches.

- **Wild: Make the hint corpus a cross-project commons with opt-in anonymised upstream sharing** — FEATURE — value 3 — effort L — risk high — category: community
  Why: wild. Many users hit the same obstacle (e.g. Claude Code's folder-trust prompt stalling recordings); a curated public registry would let them start fixed. Needs a privacy review and nothing sent without an explicit setting.
  Done when: with sharing off nothing leaves the machine, verified by a network-denied test; with it on, `fm known publish` produces a redacted preview the user must approve.

- **Auto-translate hints to other harnesses (AGENTS.md, Codex, Gemini, Cursor rules)** — FEATURE — value 4 — effort M — risk med — category: interop
  Why: the research notes call for AGENTS.md and other harness support from one setup; T-0335/T-0337 are blocked on harness parity. Repo-scope hints rendered into `AGENTS.md` would travel to teammates who do not run Foreman.
  Done when: `fm known render --target agents-md` writes a managed block that a non-Foreman Codex session reads, and re-running is idempotent.

- **Provide an eject and portability check that proves the repo works without Foreman** — CLEAN — value 3 — effort S — risk low — category: portability
  Why: T-0794 lists eject; teammates without the plugin should not hit broken references or hooks. 
  Done when: `fm eject --dry-run` lists everything Foreman added to the repo, and after a real eject the repo's own tests still pass.

- **Wild: Replay a task from its recorded trail on a clone as a regression "flight recording"** — FEATURE — value 3 — effort L — risk med — category: replay
  Why: wild; builds on T-0798 replay and T-0035 eval capture. A committed trail of a task's commands and verdicts lets a teammate replay it to verify a fix or a hint still holds.
  Done when: `fm replay T-xxxx` on a clean clone re-runs the recorded verify commands and reports pass or fail per step.

- **Add a hint-merge conflict preview in `fm doctor`** — FEATURE — value 2 — effort S — risk low — category: diagnostics
  Why: before a pull, show which local hints would collide with incoming ones (assumption: collisions happen when two sessions learn different fixes for the same obstacle).
  Done when: `fm doctor` lists colliding hint ids between HEAD and `origin` with a suggested resolution.
