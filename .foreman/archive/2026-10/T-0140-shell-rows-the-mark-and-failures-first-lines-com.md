---
id: T-0140
type: FIX
tier: S
status: done
priority: normal
scope: [mods/foreman-ui/**, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-03T05:47:17Z
updated: 2026-10-03T05:51:25Z
base: 08ee9cd1c4d5665e7561d2ee3a9f123a5182d3cb
base_tree: 87a59a1e9a97ad5cc0a7b786fa8dd09b5acd9e0c
verified: strong
---
# Shell rows: status and failures-first come from the exit status, not text tone
## Raw request
> Shell rows: the ✗ mark and failures-first lines come from text tone, so a grep listing 'except Exception:' reads as failed; use the exit status
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a zero-exit grep listing 'except Exception:' shows ✓ and its tail; a failed command still shows ✗ and its failure lines first — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then mark and selection from isErrored; sync dev-mods; screenshot
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 41 tests across 1 file. [1.87s] (start tree + this task's tests) [ran] [tree fa0531414613] (2026-10-03T05:50:31Z)
- `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 41 tests across 1 file. [1.92s] [ran] [tree fa0531414613] (2026-10-03T05:50:31Z)
- `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 41 tests across 1 file. [2.02s] (start tree + this task's tests) [ran] [tree 54ae4e09fabf] (2026-10-03T05:50:48Z)
- `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 41 tests across 1 file. [2.00s] [ran] [tree 54ae4e09fabf] (2026-10-03T05:50:48Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 41 tests across 1 file. [2.17s] [ran] [tree e5860578c052] (2026-10-03T05:51:15Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 41 tests across 1 file. [2.05s] [ran] [tree e5860578c052] (2026-10-03T05:51:25Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 41 tests across 1 file. [2.05s] [ran] [tree e5860578c052] (2026-10-03T05:51:25Z)
- (audit self) `self: diff is 6 lines in kit.ts/register.tsx; the failed-command path (isErrored) keeps failures first, covered by the existing cargo test case; the new zero-exit case is red on the start tree, green now; dev-mods copy synced, validate passes` → no findings [tree e5860578c052] (2026-10-03T05:51:25Z)
## Log
- 2026-10-03T05:47:17Z created
- 2026-10-03T05:50:21Z planned from capture
- 2026-10-03T05:50:21Z focused
- 2026-10-03T05:51:25Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
- playbook Terminal and mod UI (skills/playbooks/references/ui/terminal-ui.md)
- likely tests for the scope: plugin/tests/test_shot.py
## Lessons
- Status marks must come from the exit status; text tone is only a colour hint
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
