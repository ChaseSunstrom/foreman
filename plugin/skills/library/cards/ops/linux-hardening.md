---
name: linux-hardening
title: Linux hardening
area: ops
tags: [linux, security, ssh, sysctl, systemd, audit]
detect: [file:sshd_config, file:sysctl.conf]
related: [nftables, secrets-rotation, certificate-rotation, wireguard]
---
Harden a Linux host by measuring effective config, shrinking exposed surface, and re-checking after every change.

## Verify
- `sshd -T | grep -Ei 'permitrootlogin|passwordauthentication|pubkeyauthentication'`: the effective SSH policy, not the file text.
- `ss -tlnpH`: every listening socket and its owning process; each must be expected.
- `systemd-analyze security --no-pager`: exposure score per service unit.
- `sysctl kernel.kptr_restrict kernel.dmesg_restrict net.ipv4.conf.all.rp_filter net.ipv4.tcp_syncookies`: live kernel values match the intended baseline.
- `find / -xdev -perm -4000 -type f 2>/dev/null`: the SUID inventory, diffed against the last approved list.

## Test first
Write the baseline as a script that exits nonzero on drift, and watch it fail on the unhardened host.
```sh
#!/bin/sh
fail=0
sshd -T | grep -qi '^permitrootlogin no' || { echo "root ssh allowed"; fail=1; }
sshd -T | grep -qi '^passwordauthentication no' || { echo "ssh passwords on"; fail=1; }
[ "$(sysctl -n kernel.kptr_restrict)" -ge 1 ] || { echo "kptr exposed"; fail=1; }
[ "$(ss -tlnH | wc -l)" -le "${MAX_LISTENERS:-4}" ] || { echo "too many listeners"; fail=1; }
exit $fail
```
Run it in CI against a fresh image and on a schedule against live hosts.

## Do
- Keep config in drop-ins (`/etc/ssh/sshd_config.d/`, `/etc/sysctl.d/`, `systemctl edit`) so package upgrades never overwrite it.
- SSH: key-only, `PermitRootLogin no`, an `AllowUsers` or `AllowGroups` list. Validate with `sshd -t` before reload, and keep a second session open.
- Sandbox services with `NoNewPrivileges=`, `ProtectSystem=strict`, `ProtectHome=`, `PrivateTmp=`, `CapabilityBoundingSet=`; iterate on the `systemd-analyze security` output.
- Default-deny the firewall inbound; open only listed ports (see nftables).
- Disable and mask unused units; remove packages you do not run.
- Enable unattended security updates and know the reboot policy for kernel updates.
- Mount `/tmp` and `/var/tmp` with `nosuid,nodev,noexec` where workloads allow.
- Ship auth and sudo logs off-host so an intruder cannot erase them.

## Avoid
- Editing `/etc/ssh/sshd_config` blind and reloading: a typo locks you out. Run `sshd -t`, then test a new login before closing the old one.
- Trusting the config file over `sshd -T`: a `Match` block or an included file overrides it. Assert on `-T` output.
- Setting sysctls only with `sysctl -w`: they vanish at reboot. Put them in `/etc/sysctl.d/*.conf` and run `sysctl --system`.
- Hardening once and never rechecking: drift returns. Run the baseline script on a timer and alert on failure.
- `chmod 777` or `NOPASSWD: ALL` as a quick fix: scope the permission to the command or path.
- Disabling SELinux or AppArmor to silence a denial: read the denial log and add a narrow policy.

## Review
- [ ] Baseline script exists, fails on a stock image, and passes after hardening.
- [ ] No unexpected listener in `ss -tlnp`; firewall default policy is drop.
- [ ] Root and password SSH are off in the effective (`-T`) config.
- [ ] Settings persist across reboot (drop-in files, not runtime commands).
- [ ] Auth logs leave the host.
