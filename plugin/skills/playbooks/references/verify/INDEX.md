<!-- Foreman's own index (written for Foreman, not ported). -->
# Verify playbooks per stack

Proof that a change works, by stack. Paths are relative to the playbooks skill; the general loops are in SKILL.md.

- `references/verify/plugin-checks.md` — A Claude Code plugin changed: structure, fixture, session and eval layers, each named.
- `references/verify/data-quality.md` — A transform or table changed: contracts, old-versus-new diff, idempotence, schema drift.
- `references/verify/game-logic.md` — Game rules or physics changed: headless simulation, fixed step and seed, engine test runners.
- `references/verify/go-checks.md` — A Go package changed: table test first, race detector, fuzz target, tidy modules.
- `references/verify/mobile-tests.md` — A mobile app changed: analyzer, logic tests, device release run, platforms not exercised.
