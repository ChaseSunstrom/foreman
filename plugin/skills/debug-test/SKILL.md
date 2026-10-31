---
name: debug-test
description: Use whenever you debug, a test fails, a run crashes or a bug comes back: reproduce, root cause, fix.
---

# Foreman: debug a failure

Root cause before any fix: the iron law of `../intake/references/debugging.md`. No brief yet? This is a FIX: `/foreman:intake` first (the hooks refuse edits without one).

1. **Read the failure, not the whole log.** Pipe the run into `fm fail` (the test, the error, the repo frames, the failing source), a stack trace into `fm trace`, a long log into `fm logs` (`--since-good` shows what's new against a good run).
2. **Reproduce** with one command that fails the same way every time. It passes and fails with no code change → `../playbooks/references/fix/flaky-tests.md` first. Hard to pin down → one `foreman:fm-reproducer` (brief from `fm lane brief ID`) commits the smallest failing test.
3. **Narrow it down**, cheapest first:
   - where: `fm suspects` ranks files from the failing run's output;
   - when: it passed at an older commit → `fm bisect --run "<cmd>" --good REF` names the first bad commit and its files;
   - which part of this task's change: `fm whyred "<cmd>"` finds the smallest hunks that turn it red;
   - which values: `fm record "<python cmd>"` shows the locals where the exception unwound;
   - where the bad value starts: trace it upstream with `../intake/references/debugging-root-cause-tracing.md`.
4. **One hypothesis at a time**, written down: `fm task hypo ID add "<claim>"`, change one thing, rerun, then mark it ruled-out or confirmed. Keeps coming back → one `foreman:fm-debugger` with the failure, what was ruled out and the suspects.
5. **Fix test-first** (`../intake/references/regression-test.md`): red on the old code, green on the fix; `fm task prove ID --run "<cmd>"` shows both. A sleep or timeout in the test → `../intake/references/debugging-condition-based-waiting.md`; guard every layer the bad value crossed → `../intake/references/debugging-defense-in-depth.md`.
6. **Prove it:** `fm task evidence ID --step N --run "<cmd>"`, `fm check --affected` while iterating, then `fm check`. Something that got you past the obstacle goes in `fm fix add` for the next session.

Three failed fixes on one step → stop: it's the design, not the line. Write the diagnosis and `fm task block ID "<why>"`.
