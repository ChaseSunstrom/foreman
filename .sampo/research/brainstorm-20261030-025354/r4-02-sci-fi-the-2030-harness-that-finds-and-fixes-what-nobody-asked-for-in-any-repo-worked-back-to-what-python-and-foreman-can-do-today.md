# Brainstorm — lens: sci-fi: the 2030 harness that finds and fixes what nobody asked for in any repo, worked back to what Python and Foreman can do today

- **Infer invariants from the suite's own execution, then attack them** — FEATURE — value 4 — effort M — risk med — category: bug finding
  Why: assumption: the exam's bug kind rewards finding contract violations in never-seen repos, and the deterministic finders scored 0/108. Trace the repo's tests with `sys.settrace` or `sys.monitoring`, record argument and return ranges per function (Daikon-style), and propose invariants the tests only ever satisfy by accident (never negative, never empty, sorted). Then generate inputs just outside each one.
  Done when: on a fixture repo with a planted off-by-one on an empty input, the pipeline emits a red one-file test for it, and emits nothing on its clean twin.

- **Fault-inject every I/O call site in turn** — FEATURE — value 4 — effort M — risk med — category: bug finding
  Why: assumption: unhandled error paths are the bugs plain tests never reach. Run the repo's suite with a shim that makes the Nth `open`, `subprocess.run` or `socket` call raise, once per call site. A traceback that escapes where the code claims to handle errors becomes a finding, and the shim's N is the reproduction.
  Done when: a fixture with a bare `open()` and no try/except yields a finding that reproduces with one command naming the call index.

- **Order the hunt by churn × complexity × past-fix density** — PERFORMANCE — value 4 — effort S — risk low — category: ranking
  Why: assumption: a hunter reading every file spends its budget on the wrong ones, and 0/108 suggests blind sweeping doesn't work. `git log --numstat` plus a cheap AST complexity count gives a free deterministic hotspot list, and the hunter reads from the top. Without git history it falls back to size order and says so.
  Done when: on a repo with 3 seeded bugs, all 3 files rank in the top 20% of the list, and the order is identical on two runs.

- **Read the machine's exhaust as free bug reports** — FEATURE — value 3 — effort S — risk low — category: signal sources
  Why: assumption: users already leave failures lying around. `.pytest_cache/v/cache/lastfailed`, tracebacks in project logs, journald entries for the project's services and coredumps all name real failures nobody filed. Each one is turned into a repro attempt, and only paths inside the project are read.
  Done when: a fixture with a populated `lastfailed` and a log traceback produces two candidate findings, each carrying its source path and none read from outside the repo.

- **Run the suite on the oldest and newest interpreter the metadata claims** — FEATURE — value 3 — effort M — risk low — category: compatibility
  Why: assumption: `python_requires` and `engines` fields are claims nobody tests. `uv` can run the suite on the lowest and highest supported version in a throwaway env. A failure on a claimed version is a proven bug with a trivial reproduction.
  Done when: a fixture declaring `>=3.8` but using `match` gets a finding naming the version and the failing test, and a repo that passes on both gets a "supported range holds" line.

- **Mutate the README's examples with boundary inputs** — FEATURE — value 3 — effort S — risk low — category: docs and bugs
  Why: Foreman already has `fm docs` for paths and commands, but it only checks that they exist. Take each documented example and vary its input (empty, one element, unicode, negative, very large). A crash or a result that contradicts the prose is a finding. This reaches bugs and stale docs in one pass.
  Done when: a fixture README example that crashes on empty input yields a finding with the exact varied command.

- **Mine closed issues for repros that have no regression test** — FEATURE — value 3 — effort M — risk low — category: history
  Why: assumption: `gh` is available and issues exist. A closed bug whose repro was never encoded as a test is likely to come back. Foreman writes that test and runs it on HEAD. If it is red, the bug has regressed. If it is green, the test is offered as a free regression guard.
  Done when: for a fixture issue with an embedded snippet and a deliberately reintroduced bug, the generated test is red on HEAD and green on the fixed parent.

- **Transplant bug shapes from public advisories** — SECURITY — value 4 — effort M — risk med — category: security
  Why: assumption: the OSV/GHSA data can be cached offline. Take the patch diffs of recent advisories in the same language and ecosystem, abstract the vulnerable shape (unsanitized path join, `yaml.load`, `shell=True` on a formatted string), and search this repo for it. Each hit needs a reproduction before it is shown.
  Done when: a fixture with a `tarfile.extractall` path traversal gets a finding with an exploit test that writes outside the target directory.

- **Predict, then prove: score the hunter's confidence** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: assumption: ranking and abstention need a trustworthy confidence, and a model's stated confidence is not one. Before running a proof, the hunter must write the probability that it fails. The Brier score per repo and per kind is stored, and rank and the "none" threshold use the calibrated number.
  Done when: the ledger shows predicted against observed outcome for 20 proofs, and ranking uses the corrected number, which a unit test verifies.

- **Wild: Blind twin from the docstring** — FEATURE — value 3 — effort M — risk med — category: oracle
  Why: wild. A second model sees only a function's signature and docstring and writes it fresh. Fuzz original against twin on shared inputs, and treat any disagreement as a suspect for bug or doc drift. Only a cold reproduction promotes it to a finding, since either side may be wrong.
  Done when: on a fixture where the docstring says "inclusive" and the code is exclusive, the disagreement is found and reproduced by a red test.

- **Wild: Replay the user's shell history as a fuzz corpus** — FEATURE — value 3 — effort M — risk med — category: local signal
  Why: wild. The commands the user actually runs against a project's CLI describe real use. Recombine their flags and arguments into near-miss variants and run them in a sandbox copy. Raw history never leaves the machine, and the variants are written without secrets.
  Done when: a fixture history containing `app run --n 5` finds a crash at `--n 0`, and no history line appears in the output verbatim.

- **Wild: Prove impossible branches with an AST constant-folder** — FEATURE — value 2 — effort M — risk low — category: static proof
  Why: wild. Fold literal conditions and type-narrowed comparisons (`if x < 0 and x > 5`, a branch after an unconditional return). A dead branch that was clearly meant to run is a bug with a mathematical proof instead of a test. No model is needed, so it is cheap and quiet on clean repos.
  Done when: a fixture with a contradictory guard is flagged with the contradiction spelled out, and 5 clean fixture repos produce zero flags.

- **Wild: Cassandra receipt for every "none"** — FEATURE — value 3 — effort S — risk low — category: clean verdict
  Why: wild. The exam grades "none", so a clean verdict needs more than silence. It lists the hotspots read, the proofs tried and the predicted-vs-observed numbers. It ends with the one place the hunter would look next if given more budget.
  Done when: on a clean fixture the receipt names at least 3 inspected files and one next-look target, and an extra unrun hunt does not change the verdict.

Next question: Which of these signal sources (history, runtime traces, advisories, machine exhaust) appear in the exam's never-seen repos, and which only exist on the user's own machine?
Next question: When a proof tool such as `uv`, `gh` or a tracer is missing, does the pipeline report "cannot prove here" or does it quietly fall back to a weaker finder?
