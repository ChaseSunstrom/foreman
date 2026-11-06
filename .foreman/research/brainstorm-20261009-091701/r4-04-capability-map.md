# Brainstorm — lens: capability map

- **Gate briefs with a Definition-of-Ready lint** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: T-0317 ("There's new bug feedback") and T-0432 ("Super brainstorm") sit in the queue as briefs with no testable criterion. The drive keeps tripping over such items, and `fm task new` accepts them silently.
  Done when: `fm task new` or `fm focus` on a brief with no verifiable criterion, no bounded scope, or an unresolved "it/this" returns a scored lint and a proposed rewrite. A fixture brief shaped like T-0317 fails the lint, and a rewritten one passes.

- **Detect hallucinated APIs at edit time** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: assumption: the biggest silent failure of coding agents is calling functions, flags or options that don't exist in the installed version. Foreman checks tests and gates but not whether a referenced symbol resolves. Pin docs and signatures per dependency version. After each edit, resolve imports and attribute accesses against the real environment, and run `--help` for CLI flags the diff introduces.
  Done when: an edit calling a nonexistent method of an installed library produces a warning naming the symbol and the nearest real one, before any test runs. A test fixture proves it.

- **Stack a task's diff into independently green commits** — FEATURE — value 4 — effort M — risk med — category: review
  Why: assumption: L tasks produce one commit and one big review, while "split oversized briefs" only acts at intake. At done, partition the diff into an ordered series by hunk dependency. Each commit must pass the task's gates on its own, checked in a throwaway worktree, and `fm pr` emits the series.
  Done when: a task whose diff touches 3 independent areas yields 3 commits, each with a recorded gate pass. `git rebase --exec` over the series is green.

- **Resolve lane merge conflicts using both briefs' intent** — FEATURE — value 4 — effort L — risk high — category: orchestration
  Why: JARVIS hit lane-merge refusals (T-0280 couldn't land during T-0278), and lanes will conflict textually and semantically as the merge train grows. Hand a conflict agent both briefs, both diffs and both proofs. It proposes a resolution that must pass both tasks' recorded verifies plus a combined gate run, and otherwise returns to the user with the conflict explained in brief terms.
  Done when: two lanes editing the same function merge through `fm lane merge`. Both tasks' verify commands pass on the result, and a deliberately incompatible pair is refused with a two-brief explanation.

- **Price technical debt by how often agents tripped on it** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: Foreman already records `fm surprise` entries, hot files and blocked or deferred tasks, but nothing converts them into a priority. Attribute each surprise, retry and repeated refusal to a file or area, then rank "interest paid per week" and auto-propose the CLEAN task with the best payoff.
  Done when: `fm debt` lists areas ranked by surprises, retries and gate time attributable to them over the last 30 days. Each entry cites its ledger events, and the top one can be queued with one command.

- **Learn a playbook from one demonstration** (wild) — FEATURE — value 4 — effort L — risk med — category: skills
  Why: wild. Repeat detection needs three occurrences. The user often does a one-off manual workflow, like the "cleaned them by hand before each rm" the JARVIS builder did. `fm teach` records a shell session, with the user's narration optional. Foreman then compiles it into a parameterized playbook with guard-checked steps and a dry-run mode.
  Done when: after recording `fm teach start` … `fm teach stop` on a 5-step workflow, `fm playbook run NAME --dry-run` prints the same steps with parameters substituted. A real run reproduces the end state in a clean worktree.

- **Predict gate outcomes before running them** (wild) — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: wild. `fm surprise` relies on the model noticing it was wrong. Make the prediction explicit: before each `fm check` or verify command, record the expected result (pass/fail, which test), then log mismatches automatically. A repo-specific calibration score then drives rigor, so low calibration means more lenses and a smaller step size.
  Done when: the ledger holds a `predicted` field on check events and `fm digest` shows a calibration rate. Three consecutive mismatches in an area raise that area's review tier in a test.

- **Compose the final change from the best hunks of racing attempts** (wild) — FEATURE — value 3 — effort L — risk high — category: orchestration
  Why: wild. The existing race ideas pick one winner. Often attempt A has the better core logic while B has the better tests or error handling. Score attempts per hunk with gates and lenses, assemble a hybrid in a fresh lane, and accept it only if it beats every parent on the gate suite.
  Done when: given two attempts with complementary strengths in a fixture, `fm race compose` produces a hybrid whose gate pass and lens score exceed both parents', with each hunk attributed to its source attempt.

- **Add a host health governor for lanes and gates** — PERFORMANCE — value 3 — effort M — risk low — category: resources
  Why: assumption: lanes, headless browsers for `fm smoke`, node_modules trees and `fm run` children compete for CPU, RAM and disk on one box, and the user's tool-cache cleanup problems suggest disk pressure is real. The governor admits or defers new lanes by free memory, load, disk and battery, and reaps orphaned processes it started.
  Done when: with free disk below a configured floor, `fm lane new` refuses with the number and a suggestion. An orphaned smoke browser from a killed run is reaped within a minute, and a test proves both.

- **Broker scoped privileged steps for blocked tasks** (wild) — SECURITY — value 3 — effort M — risk high — category: autonomy
  Why: wild. T-0325 has been blocked on `sudo pacman -S libappindicator-gtk3`. A tiny allowlisted helper, installed once by the user with explicit consent, can run named verbs like `pacman -S <pkg>` from a user-approved package list, with every call logged and tied to a task. Anything outside the allowlist still goes to the user.
  Done when: an approved package installs without a password prompt via `fm priv install PKG`. An unlisted package or a flag injection attempt is refused, and both paths are logged.

- **Serve Foreman's knowledge to any editor as an LSP** — FEATURE — value 3 — effort M — risk low — category: editor surface
  Why: assumption: the user works in Claude Code and the desktop app, but vetoes, lessons, `fm why` history, surprises and "unverified lines" all attach naturally to file ranges. Expose them as diagnostics, hovers and code lenses over standard LSP, so Neovim, VS Code and JetBrains need no custom extension.
  Done when: opening a file with a recorded surprise in an LSP client shows a diagnostic at that range. Hovering shows the lesson and the task, and a headless LSP test asserts it.

- **Conform diffs to the repo's own style fingerprint** — FEATURE — value 3 — effort M — risk low — category: quality
  Why: the working rule is that new code must read like the surrounding code, but only configured linters enforce anything. Derive a fingerprint from the repo itself, covering comment density, naming, error-handling idiom, function length and test layout. Flag diff hunks that fall outside its distribution before done.
  Done when: a fixture diff with heavy docstrings in a terse-comment module is flagged with the measured densities. A diff in house style passes with no flags.

- **Adopt the user's manual commits into the ledger** — FEATURE — value 3 — effort M — risk low — category: continuity
  Why: assumption: when the user edits directly, the ledger, `fm why` and recall go blind to it, and drift between STATE and `git log` grows. Detect human commits since the last sync. Reconstruct a brief, the affected criteria and the nearest passing evidence, then file them as closed tasks marked "reconstructed" for the user to confirm or discard.
  Done when: after a manual commit, `fm adopt` creates a closed task whose brief names the changed files and the gates that passed on that tree. The task is flagged reconstructed and `fm why FILE` now lists it.
