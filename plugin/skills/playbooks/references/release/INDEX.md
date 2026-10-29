<!-- Foreman's own index (written for Foreman, not ported). -->
# Release playbooks: showing what shipped

Paths are relative to the playbooks skill. The stage's other playbooks (release and changelog, dependency upgrades)
are listed in SKILL.md.

- `references/release/ship-to-main.md` — Push finished work to main: fetched main in a scratch worktree, oldest runtime, fast-forward only, every exit code read, CI-only failures.
- `references/release/demo-production.md` — Demos, release videos and GIFs: a script with beats, seeded fake data, recorded from code, captions, a scrub for secrets.
