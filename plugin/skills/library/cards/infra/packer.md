---
name: packer
title: Packer
area: infra
tags: [packer, image, ami, hcl2, provisioner, golden-image]
detect: [file:*.pkr.hcl, file:*.pkr.json, file:*.pkrvars.hcl, file:*.auto.pkrvars.hcl]
related: [ansible, terraform, docker, nix]
---
Packer: machine images built from HCL2 templates with pinned plugins, provisioners and post-processors.

## Verify
- `packer fmt -check -recursive .`: HCL2 formatting.
- `packer init .`: installs the plugins pinned in `required_plugins`.
- `packer validate -var-file=prod.pkrvars.hcl .`: template, variables and plugin config are valid.
- `packer build -only='*.base' .`: builds a single source for a smoke image.
- `packer inspect .`: lists sources, variables and build blocks as resolved.

## Test first
The failing check is a boot-and-assert step using the built image, run through the provisioner itself or a separate launch.
```hcl
build {
  sources = ["source.amazon-ebs.base"]
  provisioner "shell" {
    inline = ["test \"$(id -u app)\" != 0", "systemctl is-enabled app"]
  }
}
```
Red first: the build fails at this provisioner until the earlier steps create the user and enable the unit. A `shell-local` provisioner can run `goss` or `inspec` against the instance.

## Do
- Use HCL2 (`*.pkr.hcl`) with `packer { required_plugins { ... } }`, and `packer init` in CI.
- Pin plugin versions with `version = "~> x.y"` constraints.
- Declare `variable` blocks with `type`, `default` and `sensitive = true` for credentials, and feed them from the environment (`PKR_VAR_name`).
- Tag images with a build id, git SHA and timestamp via `locals` and `timestamp()` or `uuidv4()` in the image name.
- Make provisioning scripts idempotent and fail-fast (`set -euo pipefail`). Delegate configuration to Ansible or a script file, not long `inline` lists.
- Clean up before capture: remove SSH keys, cloud-init state, shell history and package caches.
- Use a `manifest` post-processor to emit the artifact id for downstream Terraform.
- Set `force_deregister` only for ephemeral dev builds.

## Avoid
- JSON templates and `variables` plus `builders` keys: legacy. Use HCL2 `source` and `build` blocks.
- Credentials in the template or `-var` flags on the command line: they appear in logs and shell history. Use environment or a secrets store.
- No `required_plugins`: builds depend on whatever plugin is installed locally. Pin and `init`.
- Leaving the build user's SSH key or a default password in the image: remove it in the last provisioner.
- `provisioner "shell"` with `apt-get upgrade` unpinned: non-reproducible images. Pin packages or start from a pinned base.
- `PACKER_LOG=1` output committed or posted: it may include secrets. Scrub before sharing.
- Skipping `packer validate` in CI: errors surface only after a slow cloud boot.

## Review
- [ ] `packer fmt`, `init` and `validate` all pass in CI.
- [ ] Plugins and base images are pinned and sensitive vars are marked.
- [ ] Image contains no keys, credentials or build artifacts.
- [ ] Output artifact id and tags are recorded for consumers.
