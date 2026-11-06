**Verdict: changes needed.** There are no injection holes. The real problems are remote process leaks and silent failures in the session view.

**Adversary (checked, no finding)**
- `valid_host` rejects a leading `-` and any character outside `[A-Za-z0-9._@-]`. The host is followed by `--`, and `sh_quote` is correct.
- There is no `{@html}`, `innerHTML` or `href` anywhere in `src`. All remote strings render as Svelte text.
- The CSP is `default-src 'self'`, so remote content cannot load scripts.
- Letting the webview pass arbitrary `fm` args is acceptable given that CSP and no remote content.
- Stream ids are sequential u32 values from 1, and a stale id is a no-op.

**Findings**

1. **MEDIUM-HIGH** — `src-tauri/src/lib.rs:95,155`, `fmsession.py:512-530`.
   - Remote `fm session tail --follow` leaks. `kill()` only kills the local ssh client. The remote command has no pty and stdin is `/dev/null`, so nothing tells it to stop.
   - `tail` detects a gone reader only on a write, and writes only when a new event arrives. An idle session therefore leaves a remote python process polling every 0.3 s indefinitely.
   - Opening and leaving an idle session, removing a device, an app quit, or a reload each leave one.
   - Fix: keep stdin piped for remote streams. Run the remote line as `fm … & p=$!; cat >/dev/null; kill $p`, so the closed ssh channel ends it. Alternatively, have `tail` poll for ppid/stdout death.
   - Confidence: high on the mechanism.

2. **MEDIUM** — `src/lib/ui/Sessions.svelte:46`, `lib.rs:157`.
   - The tail's `onState` callback only sets `first`, so it never shows an error. Offline device, fm missing, or "session X was removed" all give a blank pane with no message.
   - `live` also retries every 30 s indefinitely, including for a removed session, which spawns ssh each time.
   - Fix: surface `s.error` as `ProjectView` does. Stop retrying on exit codes that mean usage error.

3. **MEDIUM** — `src/lib/app.svelte.ts:76-85`.
   - Both streams share one `set`. A device whose Foreman predates `fm session` has a healthy `projects` stream but a failing `session list` stream.
   - `projects` calls `set({ok:true})` on each line and `session list` calls `set({ok:false})` on each end. The device dot and error flap between online and offline on every backoff cycle.
   - Fix: track status per stream. A device is offline only if all streams are down, or show a per-stream error.

4. **MEDIUM (likely, not verified against the Tauri source)** — `src/lib/ui/Sessions.svelte:50`, `src/lib/app.svelte.ts:52`.
   - Streams are stopped only through JS calls. A webview reload constructs a new `App` and reconnects while the old Rust streams keep running. `on_line.send` to a dead JS callback probably still returns `Ok`.
   - Fix: kill all registered streams on webview reload or destroy, in a Rust window event handler.

5. **LOW** — `src/lib/app.svelte.ts:105`.
   - `notify()` puts remote `r.title` and `last.text` into a Linux notification body. Servers such as dunst render markup, including `<a href>`, so a prompt-injected agent or a bad device can show a clickable link.
   - Fix: escape `<`, `&` and `>` in the title and body.

6. **LOW** — `lib.rs:152`.
   - `lines()` is unbounded, so a misbehaving remote can send a huge line with no newline and grow memory without limit.
   - Fix: cap line length.

7. **LOW** — `lib.rs:44`.
   - The remote line uses `${VAR:-…}` and `exec`, which is POSIX-shell syntax. It breaks on fish or csh login shells with a cryptic error.
   - Fix: wrap it as `sh -c '…'`.

8. **LOW** — `src/lib/ui/Sessions.svelte:29-38`.
   - The effect tracks `app.devices` through `app.device()`. Adding or removing any device tears down and replays the open tail, which clears the events and the scroll position.
   - Replay also calls `await tick()` plus a smooth scroll per event, which is O(n²) on large sessions.
   - `open[i]` is keyed by index, so expanded rows persist across a reset.
   - Fix: use `untrack` and batch the replay.

9. **LOW** — `src/lib/app.svelte.ts:114`, `lib.rs:29`.
   - `addDevice` does not validate the host. `box:2222` or an IPv6 address is saved, then retries forever with the error "not an ssh host", and no port is supported.
   - Fix: validate in the add form, and say to use `~/.ssh/config` for ports.

10. **LOW (dead code)** — `capabilities/default.json:10`, `lib.rs:242`.
    - `tauri_plugin_opener` and `opener:default` are never used by the frontend. Remove them to shrink the surface.
    - `fmText` in `fm.ts` appears unused (the grep hit only its definition, and I did not search further).
    - `StrictHostKeyChecking=accept-new` trusts the first key silently. This is documented in a comment but not shown in the UI.

**Not checked:** a runtime run against Tauri, the Channel `send` behaviour after reload, `Overview.svelte`, `Agents.svelte`, `Sidebar.svelte` and `types.ts` in full, whether local `fm` re-execs, and Windows and macOS behaviour.
