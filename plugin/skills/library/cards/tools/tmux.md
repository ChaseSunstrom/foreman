---
name: tmux
title: tmux
area: tools
tags: [tmux, terminal, sessions, panes, scripting, remote]
detect: [file:.tmux.conf, file:tmux.conf, file:.tmuxinator.yml]
related: [ssh, shell-scripting]
---
tmux: persistent terminal sessions, scripted panes, and capturing output from long-running jobs.

## Verify
- `tmux ls`: the sessions that exist.
- `tmux capture-pane -p -t SESSION:0.0 -S -50`: the last 50 lines of a pane, to check what a job printed.
- `tmux show-options -g | head`: effective global options.
- `tmux source-file ~/.tmux.conf`: the config reloads without errors.

## Test first
Practice check: drive a detached session from a script and assert on its pane.
```sh
tmux new-session -d -s t1 'sleep 1; echo READY; sleep 30'
sleep 2
tmux capture-pane -p -t t1 | grep -q READY
tmux kill-session -t t1
```

## Do
- Start detached: `tmux new-session -d -s NAME -c DIR 'cmd'`; attach later with `tmux attach -t NAME`.
- Send input with `tmux send-keys -t NAME 'cmd' Enter`; use `-l` to send literal text.
- Use `tmux new-session -A -s NAME` to attach if present, create if not.
- Read output with `capture-pane -p`; add `-S -` for full scrollback and `-J` to join wrapped lines.
- Wait for completion with `tmux wait-for -S done` in the job and `tmux wait-for done` in the controller.
- Name windows with `rename-window`; target panes as `session:window.pane`.
- Set `set -g mouse on`, `set -g history-limit 50000`, and `set -s escape-time 10` in the config.
- Use `tmux run-shell` and `display-message -p '#{pane_current_path}'` for formats.

## Avoid
- Sending very long text through `send-keys`: it can be pasted, truncated or slow. Write a script to a file and send one short command to run it.
- `send-keys` without `Enter` or with the wrong target: it types into the wrong pane. Use explicit `-t session:window.pane`.
- Parsing `capture-pane` mid-render: it races with output. Wait on a marker line or `wait-for`.
- Relying on `tmux kill-server` in scripts: it kills every session. Kill by name.
- Putting `TERM` wrong: colors break. Set `default-terminal "tmux-256color"` and an RGB override for your terminal.
- Prefix conflicts with nested tmux over ssh: the inner one gets nothing. Send the prefix twice or rebind the inner.
- Using tmux as a process supervisor for services: use systemd.

## Review
- [ ] Sessions and windows have names that say what they run.
- [ ] Scripts target sessions explicitly and clean up after themselves.
- [ ] Waiting uses markers or `wait-for`, not fixed sleeps.
- [ ] Config reloads cleanly with `source-file`.
