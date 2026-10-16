---
name: tauri
title: Tauri
area: web
tags: [tauri, desktop, rust, webview, ipc, security]
detect: [dep:@tauri-apps/api, dep:@tauri-apps/cli, dep:tauri, dep:tauri-build, dep:tauri-plugin-*, dep:@tauri-apps/plugin-*, file:src-tauri/tauri.conf.json]
related: [rust, playwright, react, vue, svelte]
---
Tauri desktop apps: a Rust core, a system webview frontend, typed commands over IPC, and a capability-based permission model.

## Verify
- `cargo check --manifest-path src-tauri/Cargo.toml`: the Rust side compiles.
- `cargo test --manifest-path src-tauri/Cargo.toml`: command logic and unit tests.
- `cargo clippy --manifest-path src-tauri/Cargo.toml -- -D warnings`: lint.
- `npx tauri build`: bundles the app (runs the frontend build first).

## Test first
Keep command bodies thin and put logic in plain Rust functions; test those. Test the command wiring with Tauri's mock runtime.
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_path_outside_data_dir() {
        let base = std::path::Path::new("/data");
        assert!(resolve_in(base, "../etc/passwd").is_err());
    }
}
```
Frontend: Vitest with `@tauri-apps/api/mocks` (`mockIPC`) to fake `invoke` calls.

## Do
- Define commands with `#[tauri::command]`, register them in `tauri::generate_handler![...]`, and call with `invoke("name", { args })` from `@tauri-apps/api/core`.
- Return `Result<T, E>` where `E` implements `serde::Serialize`, so errors reach the frontend as values.
- Grant each window only what it needs in capability files (`src-tauri/capabilities/*.json`) and scope fs, shell and http permissions to specific paths or URLs.
- Share state with `.manage(...)` and `tauri::State<T>`, using `Mutex` or `RwLock` for mutation.
- Make long-running commands `async` so they do not block the main thread; use events (`emit`/`listen`) for progress.
- Set a strict `app.security.csp` in `tauri.conf.json`.
- Validate and canonicalize every path and argument in Rust; the frontend is untrusted.
- Use the official plugins (`tauri-plugin-fs`, `-shell`, `-dialog`, `-updater`) and sign updater artifacts.
- Check the installed major version: the config and permission model changed between Tauri 1 and 2.

## Avoid
- Broad permissions (`fs:default` with `**` scope, `shell:allow-execute` without a scope): any XSS reads files or runs commands. Scope them narrowly.
- Tauri 1 config keys (`allowlist`, `tauri > allowlist`) in a v2 project: ignored. Use capabilities and permissions.
- Blocking work in a sync `#[tauri::command]`: freezes the UI thread. Make it `async` or spawn.
- `unwrap()` and `panic!` in commands: crashes the app. Return errors.
- `csp: null` or `unsafe-inline` scripts: removes XSS defense. Set a CSP and use nonces or hashes if needed.
- Passing a user-provided path to `std::fs` untouched: path traversal. Resolve against a base and verify it stays inside.
- Importing v1 module paths (`@tauri-apps/api/tauri`) in v2 code: use `@tauri-apps/api/core`.

## Review
- [ ] Capabilities grant the minimum permissions with scoped paths and URLs.
- [ ] Commands return `Result` with serializable errors and validate input.
- [ ] Logic is in testable plain functions with unit tests.
- [ ] A CSP is set and no remote content is trusted.
- [ ] Clippy and `cargo test` pass, and the frontend mocks IPC in tests.
