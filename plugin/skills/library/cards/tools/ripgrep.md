---
name: ripgrep
title: ripgrep
area: tools
tags: [ripgrep, rg, search, grep, refactoring, code]
detect: [file:.ripgreprc, file:.rgignore]
related: [regex, sed-awk, refactoring, shell-scripting]
verified: 2026-10-22
---
ripgrep (`rg`): fast recursive search that respects ignore files; used for impact analysis before and after changes.

## Verify
- `rg -n 'symbol' --type-add 'src:*.{py,ts}' -t src`: every use of a symbol in the source types.
- `rg -l 'pattern' | wc -l`: how many files are affected.
- `rg --files -g '*.tf'`: list files by glob, honoring ignores.
- `rg -n --no-ignore -uu 'pattern'`: also searches ignored and hidden files, to confirm nothing hides there.

## Test first
Practice check: prove old usages are gone after a rename.
```sh
rg -n '\bold_name\b' src tests && echo "STILL REFERENCED" && exit 1
rg -c '\bnew_name\b' src | head      # expect the renamed sites
```
Grep before a refactor to count call sites; grep after to confirm zero.

## Do
- Use `-F` for fixed strings, `-w` for whole words, `-i` or `-S` (smart case) for case rules.
- Narrow with `-t py`, `-T md`, `-g 'src/**'` and `-g '!vendor/**'`.
- Use `-C 3` for context, `-o` for only the match, `-n` for line numbers, `--json` for tooling.
- Use `-l` and `-L` to list files with or without matches; `-c` for counts.
- Use `-U --multiline` for patterns that span lines; `-P` enables PCRE2 lookaround when compiled in.
- Pipe file names safely: `rg -l0 'x' | xargs -0 sed -i.bak 's/x/y/'`.
- Store defaults in a file named by `RIPGREP_CONFIG_PATH`.
- Search ignored paths deliberately with `--no-ignore` or `-u`.

## Avoid
- Treating zero results as proof: `.gitignore`, hidden files and binary skipping hide matches. Re-run with `-uu` when it matters.
- Unescaped regex metacharacters when you meant a literal: `rg 'foo(bar)'` is a group. Use `-F`.
- Piping `rg -l` into `xargs` without `-0` and `-l0`: file names with spaces break.
- Searching only code for a renamed identifier: it also lives in docs, configs, strings, tests and generated files. Search the repo, then judge.
- Substring matches (`id` matching `valid`): use `-w` or `\b`.
- Expecting `rg` output order to be stable across runs: it is parallel. Add `--sort path` when diffing.
- Relying on lookahead without `-P`: the default engine rejects it.

## Review
- [ ] Impact search covered source, tests, config and docs.
- [ ] Post-change search shows zero stale references.
- [ ] Ignored paths were checked on purpose.
- [ ] Literal searches use `-F` or are escaped.
