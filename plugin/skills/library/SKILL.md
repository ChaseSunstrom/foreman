---
name: library
description: Use when implementing, testing, reviewing or debugging in a specific language, framework, database, cloud service or tool: stack cards (fm lib) give verify commands, test-first recipes and pitfalls.
---

# Foreman: stack library

Cards are short, checkable notes, one per language, framework, service, tool or practice, in `cards/<area>/<name>.md`. They cost no context until read. `fm lib` finds them:

- `fm lib suggest`: cards for this repo, from its manifests, files and extensions. SessionStart names the top ones.
- `fm lib search WORDS`: cards and installed plugins' skills (ECC and others), ranked together.
- `fm lib show NAME`: prints a card. For a plugin skill (`plugin:skill`), it prints the path of its SKILL.md.
- `fm lib list [--area A]` gives counts and names. `fm lib check` lints every card.
- Growing it: `fm lib gaps` lists dependencies no card covers; `fm lib draft NAME --area AREA` stages a skeleton, fill it in, then `fm lib admit NAME` lints it, checks it for untrusted instructions and moves it into the library.
- At edit time the hook adds the Avoid section of the best card for the file (once per card per task); `fm lib inject off` stops it.

**Use in the loop.**
- At plan time, read the cards for the stack the task touches.
- Turn their Verify commands into criteria (`--ac "… :: <command>"`). A command that touches a live service (aws, kubectl, psql against a real host) stays a manual check, not a criterion that `fm check` runs unattended against your credentials.
- Write the failing test the way Test first shows.
- Keep Avoid in mind while building, and walk Review before closing.

Cards supplement the Foreman loop and never override it. Where they differ, the project's own conventions (its CLAUDE.md, config and existing code) win.

## Writing a card

A file goes in `cards/<area>/<name>.md`. Its frontmatter:

```
---
name: kebab-case, equal to the file name, unique across the library
title: Display name
area: equal to the directory
tags: [3-8 lowercase words]
detect: [signals; [] for practice cards that apply anywhere]
related: [other card names]
---
```

**Signals:**
- `dep:NAME` is a dependency exactly as the manifest spells it: an npm, PyPI, crate, Go module, Maven artifactId, gem, composer, pub, hex or NuGet name. A trailing `*` globs.
- `file:GLOB` matches repo-relative paths. A pattern without `/` matches the basename.
- `ext:.EXT` matches a file extension.

**Body:**
1. One summary sentence of 160 characters or fewer, used in search results.
2. `## Verify`: 2-5 bullets. Each is a backticked runnable command followed by `: what it proves`.
3. `## Test first`: the harness, where tests live, and one failing-test example of 15 lines or fewer.
4. `## Do`: 5-9 concrete practices.
5. `## Avoid`: 5-9 mistakes people and models actually make, each with its fix.
6. `## Review`: 4-7 `- [ ]` checks.
7. Optionally `## Notes`, for version facts only.

**Limits.** Aim for 1,200-4,000 characters in all; `fm lib check` refuses under 1,000 or over 4,500, a summary over 200, missing sections, bad signals and placeholders. Write tersely, with no "when to use" preamble. Never invent a flag, option or version: if unsure, leave it out.
