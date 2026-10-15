---
name: ansible-molecule
title: Ansible Molecule
area: infra
tags: [ansible, molecule, testing, roles, idempotence, containers]
detect: [file:molecule.yml, file:molecule/*/molecule.yml, file:.ansible-lint]
related: [ansible, docker, podman, cloud-init]
---
Molecule testing for Ansible roles: converge in a disposable instance, prove idempotence, then verify real state.

## Verify
- `ansible-lint`: playbook and role lint rules.
- `molecule test`: full cycle (create, converge, idempotence, verify, destroy).
- `molecule converge && molecule idempotence`: second run must report zero changes.
- `molecule verify`: run verification against the converged instance.
- `yamllint .`: YAML style, if configured.

## Test first
Write the verifier assertion first, then the role that satisfies it.
```yaml
# molecule/default/verify.yml
- name: Verify
  hosts: all
  gather_facts: false
  tasks:
    - name: nginx listens on 80
      ansible.builtin.wait_for: { port: 80, timeout: 5 }
    - name: config is not world-writable
      ansible.builtin.stat: { path: /etc/nginx/nginx.conf }
      register: st
    - ansible.builtin.assert: { that: st.stat.mode == '0644' }
```
`molecule converge && molecule verify` fails until the role does the work.

## Do
- Keep a scenario in `molecule/default/` with `molecule.yml`, `converge.yml` and `verify.yml`.
- Pick a driver and platform images that match production: containers with systemd for service roles, or VMs for kernel-level work.
- Use `ansible.builtin.assert`, `stat`, `command` with `changed_when: false`, and `service_facts` in verify for observable state.
- Write tasks with state-based modules (`package`, `template`, `service`) so the idempotence step passes.
- Use fully qualified collection names (`ansible.builtin.copy`).
- Add `handlers` with `notify` rather than unconditional restarts.
- Test multiple platforms with the `platforms` list and matrix in CI.
- Run `ansible-lint` in CI before Molecule.

## Avoid
- `command` or `shell` tasks without `creates`, `removes` or `changed_when`: idempotence fails. Add the guard.
- Treating a green converge as proof: it only means no errors. The verify playbook checks state.
- Unqualified module names and `ignore_errors: true` to quiet failures: hides real bugs. Use FQCNs and `failed_when`.
- Testing only on one distro while shipping to several: add platforms.
- Secrets in `molecule.yml` or converge vars: use test values and vault only where needed.
- Leaving instances behind: run `molecule destroy` in CI teardown with `always`.

## Review
- [ ] Idempotence step passes with zero changed tasks.
- [ ] Verify asserts state, not just success.
- [ ] Platforms cover supported distros.
- [ ] `ansible-lint` is clean with no broad skips.
- [ ] No secrets in scenarios.
