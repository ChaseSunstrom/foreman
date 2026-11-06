Live probe of `claude remote-control` (Claude Code 2.1.280), 2026-09-26:
- Untrusted workspace → exits 1 immediately: "Error: Workspace not trusted. Please run `claude` in <dir> first to review and accept the workspace trust dialog."
- Trust lives in ~/.claude.json projects[<path>].hasTrustDialogAccepted; a subdirectory of a trusted path is trusted (probe in foreman/local/rc-probe connected).
- Running in tmux (TTY) it prints "Connected · <repo> · <branch>", "Capacity: 1/32 · New sessions will be created in the current directory", the session URL (treat as sensitive; never log it), "space to show QR code · w to toggle spawn mode".
- Ctrl-C exits 0. Without the git remote HEAD it warns that remote sessions will work on a generated branch.
- systemd --user works here, Linger=yes, tmux 3.7c.
