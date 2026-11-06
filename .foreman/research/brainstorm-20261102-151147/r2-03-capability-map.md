# Brainstorm — lens: capability map

- **Add a local semantic code index** — FEATURE — value 3 — effort L — risk low — category: search
  Why: Cursor, Continue and Sourcegraph all ship meaning-based code search. The pack has `fm map` and `fm find` (structural) and a session-history grep idea, but no embedding index over the code itself. Privacy angle: use a local embedding model and store the index on disk, keyed by tree hash and built incrementally. (assumption: a small local embedder is installable.)
  Done when: `fm find --meaning "retry with backoff"` returns the right file on a fixture repo with no network, and a one-file edit re-embeds only that file.

- **Point at an element in the running app to file a task** — FEATURE — value 3 — effort M — risk low — category: surfaces
  Why: Stagewise and Cursor's browser mode let you click a UI element and hand the agent its selector, styles and a screenshot. The pack has `fm shot`, `fm flow` and "tap changed regions", but nothing that starts a task from the page.
  Done when: a click in a dev-server page, via a bookmarklet or small extension, creates a task whose brief contains the selector, computed styles, screenshot path and URL.

- **Cache dependency docs pinned to lockfile versions** — FEATURE — value 4 — effort M — risk low — category: context
  Why: Context7-style doc retrieval is a standard feature, and Foreman has the "catch hallucinated package names" idea but no version-correct API reference. Fetch the docs once per locked version, keep them offline, and inject only the symbols the diff touches. (assumption: wrong-version API use is a real failure mode here.)
  Done when: for a fixture repo pinned to lib vX, `fm docs SYMBOL` prints vX's signature offline, and a symbol absent in vX is reported as such.

- **Make gates and tasks workspace-aware for monorepos** — FEATURE — value 3 — effort M — risk low — category: scale
  Why: Nx, Turborepo and Bazel run "affected" by package graph. The pack's impacted-tests ideas work at test level, not package level. Derive the graph from manifests, then scope tasks, gates, `fm map` and owners per package.
  Done when: in a two-package fixture, a change to leaf package A runs only A's gate and its dependents' gates, and `fm map` lists packages.

- **Split a landed lane series into a stack of green, reviewable changes** — FEATURE — value 3 — effort M — risk med — category: review
  Why: Graphite and `git-branchless` make stacked PRs normal. The pack orders a diff for review and merges lanes, but never splits one big result into independently provable steps. Use `fm prove` per step.
  Done when: a 3-commit fixture splits into 3 branches that each pass the gate alone and re-merge to a tree identical to the original.

- **Add `fm release`: semver, tag, notes and artifact check in one gated verb** — FEATURE — value 3 — effort M — risk med — category: release
  Why: semantic-release and changesets are the reference tools. The pack lists the pieces separately (API-surface diff, release notes from receipts, "artifacts match the tag") but no verb that composes them. The push still needs a grant.
  Done when: on a fixture repo it proposes a version from the API diff, writes notes from closed tasks, and refuses to tag if the built artifact doesn't match the tree.

- **Give the unattended tick a launchd and Task Scheduler backend** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: the open items are Arch-specific (T-0325 needs `pacman`), and the tick and timer work assumes systemd. The standing rule says Foreman isn't tied to Claude Code, but nothing says it isn't tied to Linux.
  Done when: `fm doctor` on a macOS/launchd fixture renders and lints a valid plist for the tick, with the same job table as the systemd unit.

- **Probe local engines and pick a ceremony for `fm code`** — FEATURE — value 3 — effort M — risk low — category: local-first
  Why: T-1207 and T-1331 need `fm code` to run on any model. Discover Ollama, llama.cpp and LM Studio endpoints, then measure tokens per second, context limit and tool-call validity, and choose plan and prove depth from the result. This extends "start unseen model IDs on probation".
  Done when: `fm code --probe` against a fake OpenAI-compatible server prints a score card, and a model with 40% malformed tool calls gets the stricter ceremony.

- **Add a system-wide quick-capture with context** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: Raycast and Alfred-style capture is table stakes for task tools. The pack has a tray icon (blocked) and voice dictation, but no one-keystroke text capture that grabs the active repo, selection and clipboard.
  Done when: a bound shortcut running `fm capture --from-clipboard` files a task carrying the cwd repo and the clipboard text, and prints its id.

- **Make proofs notebook-aware** — FEATURE — value 2 — effort M — risk low — category: ecosystems
  Why: Jupyter and nbdev users expect cells to run top to bottom, outputs to be stripped from diffs, and `nbdime`-style review. The pack has the data kit and ML metric gating but nothing for `.ipynb` structure. (assumption: some of the user's repos contain notebooks.)
  Done when: `fm prove` on a fixture notebook fails when a cell errors on a clean kernel, and the diff view ignores output-only changes.

- **(wild) Map a macro pad or foot pedal to Foreman verbs** — FEATURE — value 2 — effort S — risk low — category: devices
  Why: assumption: a Stream Deck or any HID device could carry approve, freeze, next and a posture light, using the same verbs as the "phone kill switch" and "andon light" ideas. The `fm` verb table is the whole API, so only a config file is needed.
  Done when: a config line binds a key to `fm ask --approve-last`, and a simulated key event runs the verb and logs it.

- **(wild) Maintain a patch queue over an upstream fork or PKGBUILD** — FEATURE — value 3 — effort L — risk med — category: ecosystems
  Why: assumption: the user runs Arch with a hardened kernel and may carry local patches. Quilt and Gentoo patch sets are the model: track upstream releases, re-apply the local patch series on each, auto-fix rejects, and prove the build with `namcap`/tests.
  Done when: on a fixture upstream that bumps one version, the queue rebases three patches, fixes one rejected hunk, and reports the build and tests green.

- **(wild) Run a local-model league on the user's own closed tasks** — FEATURE — value 3 — effort M — risk low — category: local-first
  Why: closed tasks already store the ask and the proof. Replay a sample of them offline through each local model and tell the user which task kinds a free model can handle. This feeds the cheapest-passing-model routing idea without any cloud spend.
  Done when: `fm league --local` runs 10 closed FIX tasks against two fake models and prints a pass-rate table per task kind.

Next question: Which of these ecosystem gaps (monorepo, notebooks, macOS, forks) match repos the user actually works in, according to the languages and manifests in their registered repos?
Next question: Which of Foreman's existing verbs would a user from Aider, Cursor or Cline look for first and fail to find, judging by the wording in the first-run guide?
