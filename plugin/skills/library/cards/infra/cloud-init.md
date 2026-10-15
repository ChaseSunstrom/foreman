---
name: cloud-init
title: cloud-init
area: infra
tags: [cloud-init, provisioning, userdata, vm, bootstrap, cloud-config]
detect: [file:user-data, file:cloud-init.yaml, file:cloud-config.yaml, file:meta-data]
related: [ansible, packer, terraform, systemd]
---
cloud-init: first-boot provisioning through #cloud-config user-data, validated against the schema and checked from logs.

## Verify
- `cloud-init schema --config-file user-data.yaml --annotate`: validates the cloud-config against the schema with inline annotations.
- `cloud-init status --wait --long`: boot finished and whether it succeeded, with errors.
- `cloud-init analyze show`: per-module timing and ordering.
- `sudo cat /var/log/cloud-init-output.log`: output of commands run at boot.
- `cloud-init clean --logs && sudo reboot`: re-run first-boot on a test VM from scratch.

## Test first
Validate the config, then prove the effect on a throwaway VM.
```bash
cloud-init schema --config-file user-data.yaml          # fails on bad keys or types
# boot a test instance with the file, then:
ssh test 'cloud-init status --wait && test -f /etc/app/ready && systemctl is-active app'
```

## Do
- Start the file with `#cloud-config` on line one; without it the content is treated as a script or ignored.
- Use declarative modules: `users`, `ssh_authorized_keys`, `packages`, `package_update`, `write_files`, `runcmd`.
- Create users with `users: [{name, sudo, shell, ssh_authorized_keys, lock_passwd: true}]` and disable password SSH login with `ssh_pwauth: false`.
- Set `write_files` `permissions`, `owner` and `encoding: b64` for binary or tricky content; use `defer: true` to write after packages and users exist.
- Keep `runcmd` for what modules cannot do; make commands idempotent (they run once per instance, but a re-clean runs them again).
- Use `#cloud-config` merges and multipart MIME (`cloud-init devel make-mime`) to combine config and scripts.
- Pull bigger setup into an image (Packer) or a config tool, and let cloud-init do identity and hand-off.
- Reference secrets from the platform (instance metadata, secrets manager at runtime), not literals.

## Avoid
- Missing the `#cloud-config` header: the file is silently not parsed as config. Add it and run `cloud-init schema`.
- Tabs or wrong indentation in YAML: the whole file is dropped with a log warning. Validate before boot.
- Secrets in user-data: it is readable from the metadata service and stored on disk. Fetch secrets at runtime with instance identity.
- `runcmd` as a list of strings with shell operators relied on as arguments: each string runs through `sh`, lists of lists do not. Pick the right form.
- Long package installs in `runcmd` with network flakiness and no retries: use `packages` and check status. Bake it into the image if it is large.
- Assuming it re-runs on reboot: modules run once per instance unless you set `frequency`. Use `cloud-init clean` for tests.

## Review
- [ ] Header present and schema validation passes.
- [ ] No secrets in user-data.
- [ ] SSH password login disabled; users keyed.
- [ ] Commands are idempotent and checked with `cloud-init status`.
- [ ] Heavy setup lives in the image, not boot-time scripts.
