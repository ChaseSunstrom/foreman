# Brainstorm — lens: capability map

- **Bootstrap any clone to first green** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: assumption: the pack shows fresh-distro installs of Foreman, but nothing that takes a user's repo from clone to a passing test run. Aider, Devin and devcontainer tools all do some form of this.
  Done when: in a fresh clone of a fixture repo, `fm bootstrap` installs the toolchain and dependencies, runs the gate, and writes the recipe to a repo file. A second run from a clean checkout reaches green with no prompts.

- **Adopt existing agent-rule files on first contact** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: the pack has outbound compilation (steers to AGENTS.md, GEMINI.md and .cursor/rules) but no inbound path. Users arriving from Cursor, Cline or Copilot already have `.cursorrules`, `AGENTS.md`, `CONTRIBUTING.md` and `CODEOWNERS`. Assumption: this is a common first-hour state.
  Done when: a repo with a `.cursorrules` and a `CONTRIBUTING.md` yields proposed steers and gate commands, each citing its source line, and nothing is stored until the user accepts.

- **Print upgrade notes filtered to the verbs you use** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: Genesis ships many changes per week, and `fm usage` already knows which verbs the user runs. Assumption: nobody reads the full changelog.
  Done when: after an install bump, the next `fm` shows at most 5 lines naming changed or retired verbs from the user's last 30 days of usage, and nothing when none apply.

- **Route CODEOWNERS-sensitive changes to a sign-off row** — FEATURE — value 3 — effort S — risk low — category: team workflow
  Why: assumption: Copilot Workspace and Danger both respect ownership. Foreman has co-change hints and a team ledger but no ownership-aware gate.
  Done when: a diff touching a CODEOWNERS path adds an "owner sign-off needed: @x" line to the finish receipt, and the task cannot land as "fully proven" without it recorded.

- **Run downstream consumers' proofs on a library change** — FEATURE — value 3 — effort L — risk med — category: multi-repo
  Why: the pack has "apply one change across repos" and "port a fix", but not the reverse direction. A change in repo A should trigger repo B's gate against it.
  Done when: with two registered repos where B imports A, a breaking change to A's public function makes `fm prove --downstream` report B's red test by name.

- **Mine the forge's past review comments into repo-scoped lessons** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: the pack mines the user's post-landing edits and new review comments, but not the years of existing PR review history that encode a repo's taste.
  Done when: given a fixture PR history, it proposes lessons that each quote a reviewer comment and cite the PR number. Lessons stay inactive until accepted.

- **Write an ADR for each costly decision into docs/adr** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: `fm decide --kind costly` already stores the context, the options and the reason, and the pack proposes a notes-vault export. A repo-native ADR file is the form teams already review.
  Done when: a costly decision produces `docs/adr/NNNN-title.md` in the standard format, with a link back to the task id. Re-running the export doesn't duplicate it.

- **Plan a git-history secret purge, rotation first** — SECURITY — value 3 — effort M — risk high — category: security
  Why: the pack scrubs secrets from Foreman's own stores and scans diffs for them. It doesn't help once a secret is already in the user's pushed history. The plan covers rotation, filter-repo commands and forge cache notes. It is plan-only, and any history rewrite goes through a grant.
  Done when: on a fixture repo with a planted key, `fm purge --plan` lists every commit and ref containing it, puts "rotate first" at the top, and changes nothing.

- **Sign unattended commits with a dedicated, revocable key** — SECURITY — value 3 — effort S — risk low — category: provenance
  Why: the pack gives unattended commits their own author, but not a signature. A forge "Verified" badge on drive commits separates them from the user's hand edits, and revoking one key kills the lane's credibility.
  Done when: commits from `fm run` verify under the dedicated key, and `git log --show-signature` marks a user-authored commit as unsigned or signed by a different key.

- **Ship `fm top`, a standalone live view for non-Claude harnesses** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the pane lives inside Claude Code through foreman-ui, while the README says Foreman works with Codex, Gemini CLI and opencode. A terminal view that reads only the ledgers closes the gap for those users.
  Done when: `fm top` in a separate terminal shows the task, stage, spend and last 5 events, and updates within 2 s of a ledger append, with no claude on PATH.

- **Package Foreman for Nix, Homebrew and pipx** — FEATURE — value 2 — effort M — risk low — category: distribution
  Why: the pack mentions an AUR package idea and `install.sh`, but a discipline layer for several agents needs the other common install paths. Assumption: install friction is the main barrier for non-Arch users.
  Done when: a clean container installs each channel and `fm doctor` passes with no manual steps.

- **(wild) Map receipts to SOC 2 and ISO change-management controls** — FEATURE — value 3 — effort L — risk med — category: compliance
  Why: wild. The pack offers signed audit packs, but a mapping from "task, plan, proof, review, approver" to control IDs is what turns them into audit evidence. Vanta and Drata sell this.
  Done when: `fm audit --controls soc2` emits a table of control IDs against receipt ids for a date range, and marks each control with no matching evidence as a gap.

- **(wild) Bridge `fm ask` and status to Matrix, Slack or Discord** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild. The pack has phone push and webhook replies, but a chat bridge gives teams and always-on chat clients a surface. It needs a signed-reply scheme so an injected chat message can't approve a grant.
  Done when: a pending `fm ask` appears in a test room, a reply from an allowlisted user answers it, and a reply from anyone else is ignored and logged.

- **(wild) Teach the user one thing a week from the agent's own diffs** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. The apprentice-mode idea runs from the user to the agent. This runs the other way: Foreman picks one technique or library idiom the agent used that the user has never written in their own commits, and explains it in five lines with the file and line.
  Done when: the weekly card cites a real commit and file:line from the past 7 days, and `fm teach --skip` records a dislike for that topic.

- **(wild) Open a third-party extension registry with a lean budget** — FEATURE — value 3 — effort L — risk high — category: ecosystem
  Why: wild. The pack has prover plugin contracts, shareable guard packs and stack cards, but no single signed registry. Each installed extension would have to declare its token and latency cost and be dropped when it doesn't earn them, so the registry can't bloat the install.
  Done when: `fm ext install` fetches a signed pack to a pinned version, shows its declared cost, and `fm ext prune` removes any extension unused for 60 days.

Next question: which of these capabilities does the user's own 60-day usage history show they would actually reach, versus ones that only look complete against Cursor, Aider and Devin?
Next question: which first-hour steps (bootstrap, adopting rule files, upgrade notes) could be tested by a cold child that has only the README, so install friction is measured instead of assumed?
