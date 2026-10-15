---
name: homebrew
title: Homebrew
area: tools
tags: [macos, linux, packages, brewfile, formulae, tap]
detect: [file:Brewfile]
related: [mise, shell-scripting]
---
Homebrew: package manager for macOS and Linux, with a Brewfile to make a machine's dependencies reproducible and a formula format for your own tools.

## Verify
- `brew bundle check`: every entry in the Brewfile is installed (exit nonzero if not).
- `brew bundle install`: installs what is missing from the Brewfile.
- `brew doctor`: warnings about a broken setup (unlinked kegs, conflicting paths).
- `brew deps --tree <formula>`: what a package pulls in.
- `brew audit --strict --new <formula>` and `brew install --build-from-source <formula>` then `brew test <formula>`: for a formula you maintain.

## Test first
Prove a fresh machine can use the Brewfile.
```
cat Brewfile             # brew "jq"  /  cask "docker"
brew bundle check || brew bundle install
brew bundle check        # exits 0 now
jq --version
```
For a formula, a failing `test do` block comes first, then the fix.

## Do
- Keep a `Brewfile` with `tap`, `brew`, `cask` and `vscode` lines, committed with the repo.
- Use `brew bundle cleanup` to list (and with `--force`, remove) packages not in the Brewfile; read the list first.
- Use `brew bundle dump --file=Brewfile --force` to capture a new machine's state, then prune by hand.
- Update in steps: `brew update`, `brew outdated`, then `brew upgrade <name>` for chosen packages.
- Pin a formula that must not move with `brew pin <name>`.
- For your own formula, set `url`, `sha256`, `license`, `depends_on`, `install` and a real `test do` block.
- Check the shell environment with `brew shellenv` in your profile, since the prefix differs between Intel, Apple silicon and Linux.

## Avoid
- `sudo brew`: it breaks ownership of the prefix. Run as your user, and fix permissions with `chown` on the prefix.
- `brew upgrade` on everything before a release or demo: tools jump versions. Pin or upgrade selectively.
- Mixing system Python or Node with brew's and fighting PATH order: use a version manager (mise) for languages.
- Formula without `sha256` or with a mutable URL: installs change silently. Use a tagged release archive and its checksum.
- Treating a Brewfile as a lockfile: versions float. Pin critical ones with versioned formulae, or use mise.
- Piping an install script to a shell without reading it: fetch it, read it, and then run it.

## Review
- [ ] `brew bundle check` exits 0 on a clean setup.
- [ ] The Brewfile has only what the project needs, with taps declared.
- [ ] Critical tool versions are pinned elsewhere or via versioned formulae.
- [ ] Any formula passes audit and has a real test.
