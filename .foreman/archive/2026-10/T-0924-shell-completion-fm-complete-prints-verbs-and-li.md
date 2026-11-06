---
id: T-0924
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:25:20Z
updated: 2026-10-15T19:34:05Z
base: 5e8acd572ce1221dcf751b797086e8967f11b1ad
base_tree: 48906f1a9121d74a3b31497626ae32a5d10124ea
verified: strong
---
# Shell completion: fm complete prints verbs and live task ids; a bash/zsh hook installs it
## Raw request
> Shell completion: fm complete prints verbs and live task ids; a bash/zsh hook installs it
## Interpretation
Tab completion for fm in bash and zsh: verbs, a verb's subcommands, and live task ids where an id goes
## Assumptions (confidence)
## Acceptance criteria
- [x] fm complete lists verbs, a verb's subcommands and open task ids; fm completion bash prints a working hook — verify with `python3 plugin/tests/run.py -k Completion`
## Non-goals
## Approach (options → choice → why)
one verb, fm complete: with words it prints candidates read from the argparse tree and the live briefs; with --shell bash|zsh it prints the hook to source (chosen: one verb, nothing to install, always matches the real parser) · argcomplete (a new dependency, Foreman is stdlib-only) · static completion files generated at release (go stale between releases, no live task ids)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then fm complete and fm completion
## Resume here
## Docs impact
README quick start: bare fm and the completion hook; fm help lists complete
## Verification evidence
- `python3 plugin/tests/run.py -k Completion` → ✗ exit 1 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Completion 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 161e63b16f5f] (2026-10-15T19:33:46Z)
- `python3 plugin/tests/run.py -k Completion` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Completion 1s) / OK [ran] [tree 161e63b16f5f] (2026-10-15T19:33:46Z)
- (audit intent) `self` → met: verbs, a verb's subcommands, options (any '-' prefix) and open task ids where a positional goes, all read from the real argparse tree and the briefs; the hook passes bash -n; zsh loads bashcompinit first [tree 161e63b16f5f] (2026-10-15T19:33:46Z)
- (audit edge) `self` → outside a project ids complete to nothing (no find_project create); a word that isn't a subcommand leaves the walk where it is; the hook's 2>/dev/null keeps a broken fm from spraying the prompt [tree 161e63b16f5f] (2026-10-15T19:33:46Z)
- (ac 1) `python3 plugin/tests/run.py -k Completion` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Completion 1s) / OK [ran] [tree 9c45eed2f584] (2026-10-15T19:33:58Z)
- (step 1) `python3 plugin/tests/run.py -k Help` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: Help 1s) / OK [ran] [tree 9c45eed2f584] (2026-10-15T19:33:58Z)
- (audit edge) `self` → re-audit after the MASTER.md line (docs only): outside a project ids complete to nothing; a non-subcommand word leaves the walk in place; the hook silences fm's stderr [tree 9c45eed2f584] (2026-10-15T19:34:03Z)
- (audit intent) `self` → re-audit after the docs line: met as before [tree 9c45eed2f584] (2026-10-15T19:34:03Z)
- `python3 plugin/tests/run.py -k Help` → exit 0 · Ran 3 tests in 0.7s (1 classes, 16 at a time; slowest: Help 1s) / OK [ran] [tree 9c45eed2f584] (2026-10-15T19:34:04Z)
## Log
- 2026-10-15T19:25:20Z created
- 2026-10-15T19:32:57Z set approved=True
- 2026-10-15T19:32:57Z focused
- 2026-10-15T19:34:05Z done
- 2026-10-15T19:34:05Z committed 6333f3d (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round7-20261015: Probe: `fm ideas` with reliability + delight, 2 rounds, past every earlier ideas.md (brainstorm-20261015-132957): 49 new titles, eac…
- T-0854 [FIX M, done, 5 steps] A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what… — lesson: The firs…
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
## Lessons
- Completion read from the live argparse tree can't go stale; one verb with a --shell flag beats a verb per shell
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- README.md
- MASTER.md
