---
name: ansible
title: Ansible
area: infra
tags: [ansible, playbook, roles, idempotent, inventory, config-management]
detect: [file:ansible.cfg, file:playbook.yml, file:site.yml, file:requirements.yml, file:roles/*/tasks/main.yml, file:inventory/*]
related: [terraform, systemd, vault, packer]
---
Ansible: idempotent playbooks and roles using fully qualified modules, vaulted secrets and check-mode runs.

## Verify
- `ansible-lint`: style and risky patterns (shell without need, missing names, deprecated modules).
- `ansible-playbook site.yml --syntax-check`: the playbook parses.
- `ansible-playbook site.yml --check --diff`: a dry run showing what would change.
- `ansible-playbook site.yml` run twice: the second run reports `changed=0` (idempotence).
- `molecule test`: role scenario test, when Molecule is configured.

## Test first
Molecule runs the role in a container and verifies. Put assertions in `molecule/default/verify.yml`.
```yaml
- name: Verify
  hosts: all
  tasks:
    - name: nginx is listening
      ansible.builtin.wait_for:
        port: 80
        timeout: 5
    - name: config exists
      ansible.builtin.stat: { path: /etc/nginx/nginx.conf }
      register: conf
      failed_when: not conf.stat.exists
```
Red first: fails until the role installs and starts the service.

## Do
- Use fully qualified names (`ansible.builtin.copy`, `ansible.posix.sysctl`) and name every task.
- Prefer modules over `command` and `shell`. When forced, set `creates`, `removes` or `changed_when` and `failed_when`.
- Keep a role layout: `tasks/`, `handlers/`, `defaults/` (overridable), `vars/` (fixed), `templates/`, `meta/`.
- Use handlers with `notify` for restarts, and `meta: flush_handlers` when order matters.
- Encrypt secrets with `ansible-vault` and set `no_log: true` on tasks handling them.
- Pin collections and roles in `requirements.yml`, and install with `ansible-galaxy install -r`.
- Use `become` per task or play, not globally by habit.
- Limit and test with `--limit host` and `--check` before production runs.

## Avoid
- `shell: apt-get install ...` or `command: systemctl ...`: not idempotent and always changed. Use `ansible.builtin.package` or `ansible.builtin.systemd_service`.
- Short module names (`copy:`, `yum:`): ambiguous across collections, flagged by lint. Use FQCN.
- Bare Jinja in `when:` (`when: "{{ x }}"`): templating warning. Write `when: x`.
- `ignore_errors: true` to quiet failures: it hides real faults. Use `failed_when` or `block/rescue`.
- Plaintext passwords in `group_vars`: commit only vaulted files and avoid echoing in logs.
- `latest` for packages in production: drift on each run. Use `present` and a pinned version.
- `with_items` loops: legacy form. Use `loop:`.
- `include:`: removed. Use `include_tasks` (dynamic) or `import_tasks` (static).

## Review
- [ ] `ansible-lint` is clean and a second run reports no changes.
- [ ] Secrets are vaulted and `no_log` covers them.
- [ ] Handlers and `changed_when` express real change, not always-changed.
- [ ] Collections and roles are version-pinned.
