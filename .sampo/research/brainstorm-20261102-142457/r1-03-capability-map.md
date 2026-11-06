# Brainstorm — lens: capability map

- **Add a static security lint pass over Foreman's own Python** — SECURITY — value 4 — effort S — risk low — category: security
  Why: assumption: no bandit/semgrep-style pass is wired into the gates. `plugin/lib` (133 files) runs subprocess, writes temp files and parses untrusted ledger text. Existing ideas cover subprocess deadlines, not injection or unsafe-API patterns.
  Done when: `fm check` runs a stdlib-AST rule set (shell=True, mktemp, pickle/yaml.load, os.system with f-strings) over `plugin/lib`, and a planted violation makes it fail.

- **Lint workflows and shell: pinned actions, least-privilege tokens, shellcheck** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: the pack shows `test.yml` and `install.sh`. No idea covers CI-supply-chain hygiene (SHA-pinned actions, `permissions: read-all`, script injection in `run:`) or shellcheck on `install.sh` and `plugin/bin/fm`. Assumption: these are unpinned today.
  Done when: a gate fails on an unpinned `uses:`, a missing `permissions:` block or a shellcheck error, and passes on the current tree.

- **Inventory the node and Desktop dependency tree with an offline advisory check** — SECURITY — value 3 — effort M — risk low — category: dependencies
  Why: `mods/foreman-ui` (tsx) and Foreman Desktop (T-0325, T-0352) sit outside the "stdlib only" story the Python side keeps. Listed ideas cover reachability and licences for goals, not the mod tree. Assumption: the mod has a lockfile.
  Done when: `fm doctor` shows count, direct versus transitive, and any known-vulnerable pinned version, and the number is ratcheted down-only.

- **Tag every module with its blast radius and budget the high-blast lines** — CLEAN — value 4 — effort M — risk low — category: simplicity/safety
  Why: lean and safe meet where code can touch the outside (network, `git push`, files outside the repo, spawned children, the user's home). No listed idea maps Foreman's own code that way. Assumption: a grep/AST classifier is enough.
  Done when: `fm tidy --blast` prints LOC per class (net, push, home-write, spawn) per module, a ceiling is stored, and adding a push call outside the allowed modules fails the gate.

- **Flag import cycles and layer violations with a layering file** — CLEAN — value 3 — effort S — risk low — category: architecture
  Why: 133 lib modules plus Genesis. The Genesis-out-of-core idea only works if hooks can't import it. No idea enforces direction.
  Done when: a `layers.txt` (hooks → core → genesis forbidden) is checked in `fm check`, and a planted upward import fails with the offending line.

- **Detect dead Python statically and file removal tasks** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: "find modules no session path reaches" is a runtime idea. A vulture-style static pass is free, needs no sessions and catches dead functions inside live modules. Assumption: a whitelist file handles dynamic verb dispatch.
  Done when: running it lists unreferenced top-level defs with a whitelist, and the first run's top 10 become CLEAN captures.

- **Check the web UI for XSS and CSP against hostile ledger strings** — SECURITY — value 4 — effort M — risk low — category: web security
  Why: `templates/web/index.html` renders task titles, lessons and briefs the agent wrote, and the pack lists prompt-injection concerns. Listed work covers DNS rebinding, not stored-content injection into the page.
  Done when: a fixture ledger with `<img onerror>`, `javascript:` links and 10k-char titles renders inert in a headless `fm shot`, and the server sends a strict CSP header.

- **Audit state-dir permissions and symlink safety** — SECURITY — value 3 — effort S — risk low — category: local security
  Why: ledgers hold prompts and pasted steers (some may hold secrets). The pack mentions tmpfs/`/run/user` paths and multi-writer ledgers. File modes were only listed as a post-prover check.
  Done when: `fm doctor` reports any state file group/world-readable or any write path following a symlink, and a planted symlink at a state path is refused.

- **Budget the repo's weight: bytes, files and largest blobs** — PERFORMANCE — value 3 — effort S — risk low — category: footprint
  Why: the map shows 2129 files (1388 under `plugin/skills`) plus SVG demos. Skill packing is listed, but nothing budgets install bytes, git object size or committed binaries.
  Done when: one `budget.json` holds ceilings for installed bytes, tracked files and largest tracked blob, and `fm ship` fails when one is exceeded and names the biggest contributor.

- **Detect near-duplicate source functions across `plugin/lib`** — CLEAN — value 3 — effort M — risk low — category: simplicity
  Why: only near-duplicate tests are listed. Several readers (`fmwatch`, `fmloop`, `fmmandate`) read the same ledgers. Assumption: copy-pasted ledger-parsing helpers exist.
  Done when: a token-shingle detector lists clone pairs ≥ 15 lines with a ratchet, and the top pair is merged.

- **Learn a sandbox profile from observed runs and enforce it** — SECURITY — value 4 — effort L — risk med — category: sandboxing — wild
  Why: bwrap/Landlock is listed, but profiles are hand-written. Recording file and network access during a month of lanes and compiling an allowlist (new access flagged for review) yields a least-privilege profile with no manual work.
  Done when: `fm sandbox learn` emits a profile from a recorded drive run, and a lane re-run under it passes while an off-profile write is denied and logged.

- **Draft a 3-line stdlib replacement for each dependency** — CLEAN — value 2 — effort M — risk low — category: dependencies — wild
  Why: assumption: the dependency tree has small-use packages. For each, a tool-less child proposes a replacement, and the test suite decides whether it is equivalent.
  Done when: the report lists each dependency with its call-site count and a replacement that passes the suite, or "keep: reason".

- **Publish a SECURITY.md and a private-report path, scored against OpenSSF Scorecard** — SECURITY — value 3 — effort S — risk low — category: publishing hygiene
  Why: the repo is public with a Pages site and a "Publish Desktop on GitHub" task (T-0352). No listed idea covers disclosure policy, branch protection checks or a scorecard run. Assumption: no SECURITY.md exists.
  Done when: `SECURITY.md` exists, the scorecard (or an offline subset) runs in CI and its score is shown on the site with its date.

- **Show the repo as a weight treemap by bytes, blast radius and last-used date** — FEATURE — value 2 — effort M — risk low — category: observability — wild
  Why: combines the footprint budget and blast-radius tags with `fm usage` data into one picture of what to cut, which a subtraction-minded user would show others. Assumption: the web UI can host it.
  Done when: the web UI page renders a treemap where clicking a cell opens the module's callers and last session use, and it works on a 2000-file repo in under 2 s.

Next question: which of Foreman's own deletions has the user actually regretted, and could that regret rate set the pace of subtraction?
Next question: what does Foreman write to disk or send out that the user would be surprised to find, and where would they look first to find out?
