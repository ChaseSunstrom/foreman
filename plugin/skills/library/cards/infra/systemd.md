---
name: systemd
title: systemd
area: infra
tags: [systemd, units, services, timers, linux, sandboxing]
detect: [file:*.service, file:*.timer, file:*.socket, file:*.mount, file:*.target]
related: [podman, nginx, ansible, nix]
---
systemd units: services, timers and sockets with correct ordering, restart policy, hardening and journal logging.

## Verify
- `systemd-analyze verify ./app.service`: unit syntax, unknown keys and missing executables.
- `systemd-analyze security app.service`: exposure score and which sandbox options are missing.
- `systemd-analyze calendar 'Mon..Fri *-*-* 03:00'`: the next elapse time of a timer expression.
- `systemctl daemon-reload && systemctl status app.service`: the unit loaded and its state.
- `journalctl -u app.service -b --no-pager`: this boot's logs for the service.

## Test first
Verify before installing, then start and assert. For a user unit, add `--user`.
```sh
systemd-analyze verify ./app.service        # red until ExecStart points at a real binary
systemctl --user start app.service
systemctl --user is-active --quiet app.service
```
Use a `systemd-run --user --pty ./cmd` run to test a command under the same limits without writing a unit.

## Do
- Use `Type=simple` for foreground daemons, `notify` when the app calls `sd_notify`, and `oneshot` for tasks.
- Set `ExecStart` to an absolute path, with no shell features. Use `/bin/sh -c` only when needed.
- Declare ordering and need: `After=network-online.target`, `Wants=network-online.target`, `Requires=` for hard dependencies.
- Set `Restart=on-failure`, `RestartSec=`, and `StartLimitIntervalSec`/`StartLimitBurst` in `[Unit]` and `[Service]`.
- Run as an unprivileged `User=` or `DynamicUser=yes`, with `StateDirectory=`, `RuntimeDirectory=` and `LogsDirectory=`.
- Harden: `NoNewPrivileges=yes`, `ProtectSystem=strict`, `ProtectHome=yes`, `PrivateTmp=yes`, `CapabilityBoundingSet=`, `RestrictAddressFamilies=`.
- Put overrides in drop-ins (`systemctl edit app.service`) rather than editing vendor units.
- Schedule with `.timer` units and `Persistent=true`, with `OnCalendar=` and `RandomizedDelaySec=`.
- Enable with `systemctl enable --now`, and keep secrets in `EnvironmentFile=` (mode 600) or `LoadCredential=`.

## Avoid
- `Type=forking` with a foreground process, or the reverse: systemd marks it failed or loses it. Match the type to the daemon.
- Environment variables expanded in `ExecStart` as shell (`$HOME`, pipes, `&&`): not a shell. Use `%h` specifiers or `sh -c`.
- `After=network.target` for services needing connectivity: it only means the stack is up. Use `network-online.target` with `Wants=`.
- Editing `/usr/lib/systemd/system/*.service`: package updates overwrite it. Use `systemctl edit`.
- Forgetting `daemon-reload` after a change: the old unit keeps running.
- `Restart=always` with no `RestartSec` on a crashing service: a tight loop hits the start limit. Set a delay and limits.
- Running as root with all capabilities because "it works": drop with sandbox options and check `systemd-analyze security`.
- Cron-style `@reboot` hacks: use a unit or timer.

## Review
- [ ] `systemd-analyze verify` is clean and ordering and dependency are right.
- [ ] Runs as non-root with sandboxing, and its score is acceptable.
- [ ] Restart policy has a delay and rate limit.
- [ ] Secrets are in credentials or a restricted file, with overrides in drop-ins.
