---
name: ssh
title: OpenSSH
area: tools
tags: [ssh, keys, tunnels, config, scp, security]
detect: [file:ssh_config, file:sshd_config, file:authorized_keys, file:known_hosts]
related: [tmux, shell-scripting, git]
---
OpenSSH client and server: key auth, `~/.ssh/config`, tunnels and a hardened `sshd_config`.

## Verify
- `ssh -G HOST | grep -E '^(hostname|user|port|identityfile) '`: the effective settings after config matching.
- `ssh -o BatchMode=yes HOST true`: key login works without any prompt.
- `ssh -v HOST 2>&1 | grep -i 'offering\|authenticated'`: which keys are tried and how auth succeeded.
- `sshd -t`: the server config parses (on the server, as root).
- `ssh-keygen -lf ~/.ssh/id_ed25519.pub`: fingerprint of the key you think you are using.

## Test first
Practice check: a key-only login fails closed when the key is wrong.
```sh
ssh -o BatchMode=yes -o PasswordAuthentication=no -o IdentitiesOnly=yes -i /nonexistent HOST true
echo $?     # expect 255 (denied), and no password prompt
```
After changing `sshd_config`, keep your current session open and test a second login before closing it.

## Do
- Use ed25519 keys: `ssh-keygen -t ed25519 -C "label"`, with a passphrase and `ssh-agent`.
- Put hosts in `~/.ssh/config` with `HostName`, `User`, `IdentityFile`, `IdentitiesOnly yes`.
- Use `ProxyJump bastion` (or `-J`) rather than agent forwarding to hop through hosts.
- Tunnel with `-L local:remote_host:port` and `-R`; add `-N` for tunnel-only sessions.
- Keep `~/.ssh` at mode 700 and private keys at 600.
- Server side: `PasswordAuthentication no`, `PermitRootLogin no` (or `prohibit-password`), `AllowUsers`.
- Reuse connections with `ControlMaster auto`, `ControlPath`, `ControlPersist 10m`.
- Use `ssh-keyscan` and verify fingerprints out of band when seeding `known_hosts`.

## Avoid
- `StrictHostKeyChecking no` or `UserKnownHostsFile /dev/null` in scripts: it removes man-in-the-middle protection. Pre-seed `known_hosts`.
- Agent forwarding (`-A`, `ForwardAgent yes`) to untrusted hosts: they can use your keys. Use `ProxyJump`.
- Passing secrets on the remote command line: they appear in `ps`. Send them on stdin.
- Committing private keys or using one key everywhere: use per-purpose keys and revoke by removing from `authorized_keys`.
- Editing `sshd_config` over the only session then restarting: a typo locks you out. Run `sshd -t` and keep a session open.
- Wrong permissions on `authorized_keys` or the home directory: key auth silently fails. Check `ssh -v` and server logs.
- Old key types (DSA, RSA under 3072 bits).

## Review
- [ ] Keys are ed25519 with passphrases; no private keys in repos.
- [ ] Host key checking is on, with known hosts seeded.
- [ ] Server disables password and root login, and `sshd -t` passes.
- [ ] Tunnels bind to localhost unless exposure is intended.
