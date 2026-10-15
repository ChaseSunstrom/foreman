---
name: nix
title: Nix
area: infra
tags: [nix, flakes, nixos, reproducible, derivation, devshell]
detect: [ext:.nix, file:flake.nix, file:flake.lock, file:shell.nix, file:default.nix]
related: [docker, packer, systemd]
---
Nix: reproducible builds and dev shells via flakes, pinned inputs and pure derivations, plus NixOS modules.

## Verify
- `nix flake check`: evaluates all outputs and runs declared `checks`.
- `nix build .#pkg --print-build-logs`: the package builds in the sandbox.
- `nix develop -c <cmd>`: the dev shell provides the tools the command needs.
- `nix fmt`: runs the flake's formatter, when `formatter` is set.
- `nixos-rebuild build --flake .#host`: the system configuration builds without switching.

## Test first
Add a failing entry to `checks.<system>` so `nix flake check` fails first. For NixOS, use `pkgs.nixosTest`.
```nix
checks.x86_64-linux.cli-version = pkgs.runCommand "cli-version" { } ''
  ${self.packages.x86_64-linux.default}/bin/app --version | grep -q "1.2"
  touch $out
'';
```
Red first: it fails until the build installs `bin/app` and the version matches.

## Do
- Commit `flake.lock` and update inputs deliberately with `nix flake update` or `nix flake lock --update-input nixpkgs`.
- Pin `nixpkgs` through a flake input, not `<nixpkgs>` from the channel.
- Declare a dev shell with `devShells.default = pkgs.mkShell { packages = [ ... ]; }`.
- Use `buildInputs` for runtime libs and `nativeBuildInputs` for build tools, to get cross-compilation right.
- Fix hashes with a fake hash (`lib.fakeHash`) and copy the real hash from the error, never skip verification.
- Use `lib.mkIf`, `mkDefault` and `mkOption` with `types` in NixOS modules, so options compose.
- Keep secrets out of the store: pass paths via `agenix` or `sops-nix` rather than string values.
- Set `meta` (description, license, mainProgram) on packages.

## Avoid
- Impure access (`builtins.currentTime`, `<nixpkgs>`, `fetchurl` with no hash, `getEnv`): flakes forbid or break it. Use pinned inputs and hashes.
- Untracked files in a flake repo: Nix only sees files known to git, so `git add` new files before building.
- Secrets in `.nix` literals or `environment.etc.text`: world-readable in `/nix/store`. Use agenix or sops-nix.
- `with pkgs;` at the top of large expressions: hides where names come from and shadows. Use explicit `pkgs.x` or scoped `inherit`.
- `rec { }` for self reference: infinite recursion risk. Use `let ... in` or `finalAttrs`.
- `nix-env -i` for tooling: imperative state not in the config. Declare it in a flake or `home-manager`.
- Running `nix-collect-garbage -d` on a host and then expecting rollbacks: it deletes old generations.

## Review
- [ ] `nix flake check` passes and `flake.lock` is committed.
- [ ] All fetches have hashes, and no impure builtins are used.
- [ ] Build inputs are split correctly between native and runtime.
- [ ] No secrets in the store.
