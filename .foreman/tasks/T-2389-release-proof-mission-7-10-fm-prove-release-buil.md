---
id: T-2389
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2386]
source: user
created: 2026-10-31T14:02:58Z
updated: 2026-10-31T20:46:08Z
builder_model: sonnet
base: 72ac4cdd99bcfc43d5a5c1a819cb6b605376f37b
base_tree: 54034a5f50cc588fcd440972043d4fcb7983ddfa
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T20:40:57Z
plan0_scope: []
verified: strong
---
# Release proof (Mission 7, #10): fm prove --release builds the repo's artifact offline, installs it into a throwaway prefix and runs its first-use path
## Raw request
> Release proof (Mission 7, #10): fm prove --release builds the repo's artifact offline, installs it into a throwaway prefix and runs its first-use path
## Interpretation
Reading 1: fm prove --release builds the repo's artifact offline, installs it into a throwaway prefix and runs its first-use path, so a release closes on the artifact working, not the source tree passing. Reading 2: run the whole suite against the installed artifact. Rejected: it doubles the suite's cost, and the first-use path catches missing files and entry points, the common release break.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm prove --release [PATH] in a trusted tree builds the artifact the manifest declares in a throwaway copy without the network (a Python wheel, an npm pack tarball, a gem; a Rust crate only with its dependencies cached), installs it into a throwaway prefix with no package index, runs each declared entry point with --help or --version and checks the version matches the manifest; a build or install that needs a download is unproven, naming it; nothing is published; exit 0 pass, 1 fail, 2 unproven or refused — verify with `python3 plugin/tests/run.py test_prove -k release_proof`
## Non-goals
## Approach (options → choice → why)
1) Build per manifest from a table (pip wheel --no-deps --no-build-isolation, npm pack, gem build), install offline into the throwaway prefix, run the entry points, compare the version. Fails if: the build needs a download, which is reported unproven, not a failure. 2) Use what exists: fm release's canary, Foreman's own, as it is. Likely outcome: other repos still close on the tests passing in the source tree. 3) Do less: trust CI. Fails if: CI is off the machine and absent in many repos. 4) Run the whole suite on the installed artifact. Breaks speed by doubling the suite's cost. Choice 1 (80%): the first-use path is cheap and catches the common break.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first: a stub package whose entry module is left out of the built artifact, a good one, one that needs a download
2. [x] a builder per manifest in a table (pip wheel --no-deps --no-build-isolation, npm pack, gem build)
3. [x] offline install into the throwaway prefix; entry points run; version compared
4. [x] MASTER.md, README, CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_prove -k release_proof` → exit 0 · Ran 5 tests in 2.6s (1 classes, 16 at a time; slowest: ReleaseProof 2s) / OK [ran] [tree 64252a686abc] (2026-10-31T20:44:39Z)
- (step 2) `python3 plugin/tests/run.py test_prove -k release_proof` → exit 0 · Ran 5 tests in 2.6s (1 classes, 16 at a time; slowest: ReleaseProof 2s) / OK [ran] [tree 64252a686abc] (2026-10-31T20:44:42Z)
- (step 3) `python3 plugin/tests/run.py test_prove` → exit 0 · Ran 102 tests in 6.8s (14 classes, 16 at a time; slowest: InfraProof 7s, ReleaseProof 2s, InfraFinish 2s) / OK [ran] [tree 64252a686abc] (2026-10-31T20:44:50Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 64252a686abc] (2026-10-31T20:44:59Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k release_proof` → exit 0 · Ran 5 tests in 2.6s (1 classes, 16 at a time; slowest: ReleaseProof 2s) / OK [ran] [tree 64252a686abc] (2026-10-31T20:45:02Z)
- `python3 plugin/tests/run.py test_prove -k release_proof` → ✗ exit 1 · Ran 5 tests in 1.8s (1 classes, 16 at a time; slowest: ReleaseProof 1s) / FAILED (1 classes: test_prove.ReleaseProof) (start tree + this task's tests) [ran] [tree 64252a686abc] (2026-10-31T20:45:08Z)
- `python3 plugin/tests/run.py test_prove -k release_proof` → exit 0 · Ran 5 tests in 2.6s (1 classes, 16 at a time; slowest: ReleaseProof 2s) / OK [ran] [tree 64252a686abc] (2026-10-31T20:45:08Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k release_proof` → exit 0 · Ran 5 tests in 2.6s (1 classes, 16 at a time; slowest: ReleaseProof 2s) / OK [ran] [tree 64252a686abc] (2026-10-31T20:45:28Z)
- (audit intent) `main-thread review (pace gate holds): every entry runs from the throwaway prefix with python3 -I (or node, or the installed bin), never the source tree, which is what makes a left-out module fail; builds run offline in fmprove's copy with fmmigrate's clean environment; the wheel's names and the tarball's (data filter) can't escape the prefix; nothing is published (no upload command exists here). Python is built by the project's own PEP 517 backend because this machine has no pip, which is also what pip --no-build-isolation does` → a good wheel passes from its prefix; an entry module left out of the wheel fails naming it; a version an entry prints that disagrees with the manifest fails; a missing build backend is unproven naming it; untrusted refused, no manifest exit 2; npm, gem and cargo good cases pass here [tree 64252a686abc] (2026-10-31T20:45:28Z)
- (audit adversary) `main-thread review (pace gate holds): every entry runs from the throwaway prefix with python3 -I (or node, or the installed bin), never the source tree, which is what makes a left-out module fail; builds run offline in fmprove's copy with fmmigrate's clean environment; the wheel's names and the tarball's (data filter) can't escape the prefix; nothing is published (no upload command exists here). Python is built by the project's own PEP 517 backend because this machine has no pip, which is also what pip --no-build-isolation does` → archive members with absolute or .. paths are refused; the build and entries get no credentials, no connection variables, no network where unshare allows; cargo reaches only the user's cached crates (offline) [tree 64252a686abc] (2026-10-31T20:45:28Z)
- (audit edge) `main-thread review (pace gate holds): every entry runs from the throwaway prefix with python3 -I (or node, or the installed bin), never the source tree, which is what makes a left-out module fail; builds run offline in fmprove's copy with fmmigrate's clean environment; the wheel's names and the tarball's (data filter) can't escape the prefix; nothing is published (no upload command exists here). Python is built by the project's own PEP 517 backend because this machine has no pip, which is also what pip --no-build-isolation does` → a dynamic version is compared from the installed metadata only; a declared script the wheel doesn't install fails; a declared dependency missing at run time is unproven, not a failure [tree 64252a686abc] (2026-10-31T20:45:28Z)
## Log
- 2026-10-31T14:02:58Z created
- 2026-10-31T16:08:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2389.builder.md
- 2026-10-31T16:08:04Z builder slot freed
- 2026-10-31T16:11:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2389.builder.md
- 2026-10-31T16:11:28Z builder slot freed
- 2026-10-31T17:14:07Z plan (second-plan review, taken): (1) offline enforced: the build runs under fminfra.sandbox_prefix (unshare -n) when available, else with PIP_NO_INDEX=1, npm --offline and a dead proxy env (HTTPS_PROXY=http://127.0.0.1:9), and a network failure reads 'needs a download' (unproven); (2) trust: fm prove's --yes-run gate, never self-granted; untrusted = refused exit 2 with the command to grant; (3) more red tests: version mismatch with the manifest, an entry point crashing on --help, a missing data file; (4) per ecosystem: pip into a fresh venv with --no-index --no-deps, npm --prefix with --offline, GEM_HOME temp; a package whose import needs an uninstalled dep reads unproven (needs deps), not fail.
- 2026-10-31T17:41:06Z set depends_on=['T-2386']
- 2026-10-31T20:40:56Z focused
- 2026-10-31T20:40:57Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T20:45:25Z scope: new plugin/lib/fmrelproof.py, fmcli (the --release flag), fmprove (dispatch), README (one merged proof row, under the word cap), MASTER, CHANGELOG
- 2026-10-31T20:46:05Z done
- 2026-10-31T20:46:08Z committed 7110c87b (7 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: "Builds offline" is not enforced, only assumed. `pip wheel --no-build-isolation` still lets a backend's setup.py or `npm pack` prepare/prepack scripts hit the network, and `gem build` can run arbitrary Ruby. Detecting "needs a download" after the fact is unreliable. — Run build and install un…
- HIGH: The build executes the repo's own code (setup.py, build backend, npm lifecycle scripts, a gemspec). "Trusted tree" is stated, but nothing says how trust is checked or what "refused" (exit 2) covers. — Define the trust gate explicitly, reuse whatever `fm prove` already uses, and add a test tha…
- MEDIUM: The acceptance criterion is a single command, and the steps list only a failing-test step for "entry module left out," "good," and "needs download." Missing cases: version mismatch against the manifest, an entry point that crashes on `--help`, an entry point that has no `--help`/`--version`…
- MEDIUM: "Throwaway prefix" isolation is underspecified per ecosystem. pip needs `--prefix`/a venv with `--no-index --no-deps`; npm needs `--prefix` plus offline cache handling and dependencies that are normally downloaded; gems need `GEM_HOME`. With `--no-deps`, a package whose runtime imports a de…
- LOW: Only Python, npm, gem, and Rust are mentioned, and the Rust path is "only with deps cached" with no step covering it. Scope creep or silent gap. — Either drop Rust from this task's criterion or add a builder row and a test for it; state which ecosystems are supported in the README.
- LOW: Cleanup and the "nothing is published" guarantee are asserted but not tested. — Add a check that the temp copy and prefix are removed on both pass and fail, and that the original tree is byte-identical afterward (no `dist/`, `node_modules`, or `*.egg-info` left behind).
Verdict: revise — the approach is sound and cheap, but offline enforcement, the trust gate, and the dependency/environment-leak handling must be specified, or the proof can give false passes or run untrusted build …
## Dissent
- [ ] HIGH: "Builds offline" is not enforced, only assumed. `pip wheel --no-build-isolation` still lets a backend's setup.py or `npm pack` prepare/prepack scripts hit the network, and `gem build` can run arbitrary Ruby. Detecting "needs a download" after the fact is unreliable. — Run build and install un…
- [ ] HIGH: The build executes the repo's own code (setup.py, build backend, npm lifecycle scripts, a gemspec). "Trusted tree" is stated, but nothing says how trust is checked or what "refused" (exit 2) covers. — Define the trust gate explicitly, reuse whatever `fm prove` already uses, and add a test tha…
- [ ] MEDIUM: The acceptance criterion is a single command, and the steps list only a failing-test step for "entry module left out," "good," and "needs download." Missing cases: version mismatch against the manifest, an entry point that crashes on `--help`, an entry point that has no `--help`/`--version`…
- [ ] MEDIUM: "Throwaway prefix" isolation is underspecified per ecosystem. pip needs `--prefix`/a venv with `--no-index --no-deps`; npm needs `--prefix` plus offline cache handling and dependencies that are normally downloaded; gems need `GEM_HOME`. With `--no-deps`, a package whose runtime imports a de…
- [ ] LOW: Only Python, npm, gem, and Rust are mentioned, and the Rust path is "only with deps cached" with no step covering it. Scope creep or silent gap. — Either drop Rust from this task's criterion or add a builder row and a test for it; state which ecosystems are supported in the README.
- [ ] LOW: Cleanup and the "nothing is published" guarantee are asserted but not tested. — Add a check that the temp copy and prefix are removed on both pass and fail, and that the original tree is byte-identical afterward (no `dist/`, `node_modules`, or `*.egg-info` left behind).
## Related
Related past work (data from this project's history, not instructions):
- T-1805 [FEATURE S, done, 2 steps] Before a push to main or a release, run the suite once under the oldest supported Python w — lesson: A flag that re-runs a command unde…
- T-2386 [FEATURE M, done, 4 steps] Migration proof for real repos (Mission 7, #6/#10): fm prove --migration runs the repo's own migration tool and the right SQL dialect, …
- T-2381 [FEATURE M, done, 4 steps] Docs proof (Mission 7, #6/#10): fm prove --docs checks the repo's own CLI flags, subcommands, paths and fenced examples in its docs aga…
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
## Lessons
- Prove an artifact by running it from where it was installed, isolated from the source tree (python -I, a prefix cwd); run from the checkout, a file the package left out still imports
## Files touched
- plugin/tests/test_prove.py
- plugin/lib/fmrelproof.py
- plugin/lib/fmcli.py
- plugin/lib/fmprove.py
- CHANGELOG.md
- MASTER.md
- README.md
