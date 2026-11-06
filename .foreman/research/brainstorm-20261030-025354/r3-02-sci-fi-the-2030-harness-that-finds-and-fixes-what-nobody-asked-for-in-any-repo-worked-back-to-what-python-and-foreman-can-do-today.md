# Brainstorm — lens: sci-fi: the 2030 harness that finds and fixes what nobody asked for in any repo, worked back to what Python and Foreman can do today

- **Mine docstrings and asserts into executable claims** — FEATURE — value 5 — effort M — risk med — category: finders
  Why: the exam's `bug` kind needs an oracle, and the repo already states one in docstrings, type hints, `assert` and `raise` messages and README sentences. Today's Python can pull these out with `ast` and turn each into a one-function check. Assumption: most planted exam bugs contradict some stated claim.
  Done when: on a fixture whose docstring says "returns sorted" but whose code doesn't, `fm find` writes a test that is red on the untouched tree and names the docstring line.

- **Fuzz toward the repo's own `raise` and `assert` lines** — FEATURE — value 4 — effort M — risk med — category: finders
  Why: a stdlib-only, coverage-guided input sweep (`sys.settrace` plus type-hint-driven generators) can reach guards the author thought were unreachable. A reached assert is a proof without a model call. Assumption: Python-first, other stacks later.
  Done when: a fixture with an unreachable-looking `assert x > 0` is hit, and the finding carries a minimal failing input.

- **Treat linter and type-checker output as hypotheses, not findings** — FEATURE — value 4 — effort S — risk low — category: finders
  Why: the pack says the deterministic finders found 0 of 108. ruff, pyright, shellcheck and clippy already emit thousands of candidates. The funnel is: tool hit → one-file repro attempt → keep only red ones. Assumption: the tools are installed, otherwise "cannot prove here".
  Done when: a fixture with one real type bug and ten style nits files exactly one finding, with a red test.

- **Probe copy-paste divergence with AST clone pairs** — FEATURE — value 4 — effort M — risk low — category: bug finder
  Why: clone pairs where one operand or bound differs are a classic injected-bug shape. Normalized AST hashing is stdlib work. The model is asked only about the differing token. Assumption: the exam's planted bugs include such shapes.
  Done when: two near-identical functions with one flipped `<` / `<=` produce a ranked pair and a failing test.

- **Run the suite against the newest allowed dependencies in a throwaway worktree** — FEATURE — value 3 — effort M — risk low — category: dependency drift
  Why: `fm deps` only looks up versions. A pre-upgrade run finds latent breaks before the registry forces them. This is the "pending change" universe from a 2030 harness, doable today with a venv.
  Done when: a fixture pinned to an old API gets a finding naming the dependency and the first failing test.

- **Boot the repo cold as a newcomer and file every friction** — FEATURE — value 4 — effort M — risk low — category: onboarding bugs
  Why: scout today probes Foreman's own setup (the noted `probe_doctor` problem). A fresh clone in a clean directory, with only README commands, finds broken build and test instructions in any project.
  Done when: a fixture README with a stale install command yields a finding with the exact failing line.

- **Spend model calls with a bandit over files** — PERFORMANCE — value 4 — effort M — risk med — category: hunt budget
  Why: cost is the complaint (plain Claude does 3/3 at about 0.17 USD). Features such as churn, complexity, missing tests, recent fixes and the exam's past hits can set a prior. Each hunt's outcome then updates it. Assumption: `fm map` exposes these features.
  Done when: on 20 replayed exam repos, the bandit finds at least as many planted bugs as uniform order at a lower cost.

- **Log egress bytes per hunt and send function slices, never whole files** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: nothing in the pack shows what a scan sends out. A receipt line like "sent 41 KB in 12 slices, 0 secrets" makes the first-scan "no" path an informed one. Assumption: hunts call a remote model.
  Done when: `fm find` prints bytes sent, a test shows a planted secret never leaves, and a local-only flag sends 0.

- **Fix twice, accept only where independent patches agree** — FEATURE — value 3 — effort M — risk med — category: fix lane
  Why: a hardcode-the-test fix is the known failure. Two blind patches that must pass the proof and agree on a held-out input set make a literal-fit visible. The disagreement goes on the receipt.
  Done when: for a fixture where one patch hardcodes the literal, the pair is flagged and the fix is downgraded to a report.

- **Explain any finding by replaying its hunt trail** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the user rejects things they can't audit, and several earlier ideas assume trust in findings. `fm find why F-12` prints probe, slice sent, prover command and refuter verdict in plain lines.
  Done when: the output reproduces the finding's proof command and a test checks that it exits red.

- **Wild: watch the editor live and run one cheap probe on each saved function** — FEATURE — value 3 — effort L — risk med — category: ambient
  Why: the 2030 harness never waits for a night shift. It speaks only when a probe is red and silent otherwise. Assumption: a file watcher plus the claims miner is cheap enough to run per save.
  Done when: saving a function that breaks its docstring claim shows one pane line within 5 s, and a clean save shows nothing.

- **Wild: let finder arms bid and pay them by survival** — FEATURE — value 3 — effort L — risk med — category: orchestration
  Why: the evidence is that plain Claude beats the finders. A budget split among arms (claims miner, linter funnel, plain Claude) is repaid by proven and surviving findings, so the harness learns the cheapest arm per ecosystem without anyone choosing.
  Done when: after 30 simulated hunts the split shifts toward the arm with higher precision per dollar, and the ledger shows each arm's balance.

- **Wild: draft the upstream maintainer note and never send it** — FEATURE — value 2 — effort S — risk low — category: outward
  Why: for a dependency bug found while hunting, a ready minimal repro plus issue text saves the user an afternoon. Sending needs explicit approval, since outbound posts publish and may be indexed.
  Done when: a dependency-caused finding writes `upstream-note.md` with a stdlib-only repro, and no network call occurs.

Next question: What fraction of the exam's planted `bug` defects contradict a statement already in the repo (docstring, assert, test name, README), as against needing outside knowledge?
Next question: Which repo does the user most want hunted tonight, and what would they accept as "clean" for it?
