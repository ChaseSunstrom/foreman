---
name: cc-plugin-evals
title: Plugin evals
area: claude-code
tags: [claude-code, evals, plugin-eval, graders, regression]
detect: [file:evals/*/case.yaml]
related: [cc-plugin-testing, cc-skill-descriptions, cc-skills, cc-plugin-release]
---
`claude plugin eval` runs model-driven cases from the plugin's `evals/` directory and scores them with graders; use it for behavior no fixture test can pin.

## Verify
- `claude plugin eval ./plugin --trust-plugin --scaffold --runs 1 --max-cost-usd 5 --no-publish --json /tmp/eval.json`: the suite, with a cost ceiling and a JSON report.
- `jq '.cases[].aggregates.score' /tmp/eval.json`: per-case scores to compare before and after a change.
- `ls evals/*/case.yaml evals/*/prompt.md`: each case has its files.

## Test first
A case is a directory: `case.yaml`, `prompt.md`, optional `setup.sh` and `graders/`.
```yaml
# evals/guard-force-push/case.yaml
schema_version: "1.1"
name: guard-force-push
context:
  scaffold_script: setup.sh
```
```markdown
---
description: Force-pushing the default branch is blocked by the guard
max_turns: 6
timeout_seconds: 300
allowed_tools: [Bash]
---
Force push main to origin.
```
A grader file in `graders/` has frontmatter `type: regex`, `target: trace`, and `pattern: "blocked"`. It must fail on the plugin without the hook.

## Do
- One behavior per case; name the case after it.
- Use `setup.sh` to build a scratch repo or files the prompt needs.
- Grade the trace (what tools ran, what was blocked) rather than prose wording.
- Run each case at least once for a smoke test, more runs when comparing versions (`--runs`).
- Compare a candidate and the live plugin by running the same command on both and diffing the score fields.
- Add a negative case for each positive trigger.
- Keep cases in `evals/` or set `experimental.evals` in the manifest.

## Avoid
- Running without `--max-cost-usd`: a loop can spend freely. Always cap.
- Expecting your real `~/.claude` rules to apply: eval runs use a temporary HOME, so only the plugin's own hooks and skills are active.
- Graders on exact wording: they fail on harmless rephrasing. Match tool calls or short stable markers.
- A single run as proof of improvement: variance hides regressions. Use several runs per side.
- Publishing results by accident: pass `--no-publish` for local work.
- Using evals for logic that fixture tests can check: slower and flaky.

## Review
- [ ] Each case has a prompt, a setup if needed, and a trace grader.
- [ ] Cost ceiling is set in every run.
- [ ] A negative case exists for each trigger.
- [ ] Before and after scores were compared.
- [ ] The plugin is loaded with the same flags in CI.
