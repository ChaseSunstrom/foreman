<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Dependency admission: before adding one

Use when you are about to add any new package, library, plugin, action, container base image or vendored file to a project,
including a dev-only or transitive one you pull in on purpose. Upgrading one already admitted is
`dependency-upgrade.md`.

Built on library cards: `fm lib show dependency-audit` (known vulnerabilities), `fm lib show supply-chain-pinning`
(lockfiles, hashes, pinned actions), `fm lib show sbom` (recording what ships), `fm lib show dependency-upgrades`
(keeping it current afterwards).

## The procedure

1. **Try not to.** Standard library, a dependency already in the lockfile, or under ~50 lines of your own code
   covers it? Then stop here. Pass: the brief names what you checked and why it falls short.
2. **Confirm the name.** Copy it from the project's own docs or repository, not from memory or a search result;
   look for near-miss names (typosquats) and a registry entry that links back to that repository. Pass: the
   brief links the source repository.
3. **Licence.** It must be compatible with this project's licence and use (shipped, served, internal). Unknown,
   custom or missing licence is a fail until someone with authority says yes. Pass: the licence is named.
4. **Health.** Last release and last commit within about a year, more than one maintainer or a backing
   organisation, issues answered. A finished, tiny, stable library can pass on age alone: say so.
5. **Security.** Run the ecosystem's audit (`pip-audit`, `npm audit`, `cargo audit`, `govulncheck`, or OSV) on a
   branch with it added. No known unfixed high or critical advisory. No install scripts that fetch or run code
   you haven't read.
6. **Weight.** Count what it pulls in: the lockfile diff's new packages, install size, bundle size for a
   frontend. Pass: the brief states the number of new transitive packages.
7. **Pin it.** Exact version in the lockfile, with hashes where the tool supports them; CI actions pinned to a
   commit, base images to a digest.
8. **Contain it.** Call it through one module of your own so it can be swapped later; a dependency imported in
   forty files is a migration, not a swap.
9. **Record the admission** with `fm decide "add <name>" --why "…" --rejected "…"` (the alternatives from step 1).

A no on any of steps 2, 3 or 5 is a stop, not a trade-off.
