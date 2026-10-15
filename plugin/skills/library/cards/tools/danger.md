---
name: danger
title: Danger
area: tools
tags: [pull-requests, review, automation, ci, danger-js]
detect: [file:dangerfile.*, dep:danger]
related: [code-review, github-cli, commitlint]
---
Danger: runs a dangerfile in CI to comment on pull requests (missing tests, changelog, large diffs, forbidden changes).

## Verify
- `npx danger local`: run the dangerfile against the local git diff, no PR needed.
- `npx danger pr https://host/org/repo/pull/123`: dry run against a real PR (needs a token env var for private repos).
- `npx danger ci`: what the CI step runs; it needs the platform token in the environment.
- `npx tsc --noEmit dangerfile.ts`: a TypeScript dangerfile type checks.
- `git diff --name-only origin/main...HEAD`: the file list `danger.git` will see.

## Test first
Prove the rule fires on the diff shape you care about.
```
// dangerfile.ts
import { danger, fail } from "danger"
const src = danger.git.modified_files.some(f => f.startsWith("src/"))
const tests = danger.git.modified_files.some(f => f.includes("test"))
if (src && !tests) fail("Source changed without tests.")
```
Edit a file under `src/` only, run `npx danger local`, and expect the failure.

## Do
- Use `fail` for blockers, `warn` for advice, `message` for info, `markdown` for longer notes.
- Keep rules few and about things reviewers repeat (tests, changelog, lockfile in sync, large PR).
- Read `danger.git.created_files`, `modified_files`, and `danger.github.pr` for title and body checks.
- Give CI a token with comment rights, and run Danger on pull request events only.
- Make rules idempotent: Danger updates its own comment, so avoid output that changes every run.
- Check out full history, so diffs against base resolve.

## Avoid
- Fork pull requests with no secrets: Danger cannot comment. Use the platform's safe pattern or accept no comment.
- Rules that fail on style: a linter does that better. Keep Danger for process.
- Heavy network calls in the dangerfile: they slow and flake CI. Cache or skip.
- Failing on warnings in the same step: the meaning of `warn` is lost. Reserve `fail` for blockers.
- Running `danger ci` locally without env vars and getting a generic error: use `danger local`.
- Reading file contents without awaiting: `danger.git.diffForFile` is async, so `await` it.

## Review
- [ ] `danger local` shows the expected message for a positive and a negative diff.
- [ ] Each `fail` matches a rule the team agreed on.
- [ ] CI token and checkout depth are set correctly.
- [ ] Output is stable between runs, so the comment updates cleanly.
