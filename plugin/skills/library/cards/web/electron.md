---
name: electron
title: Electron
area: web
tags: [electron, desktop, ipc, security, node, chromium]
detect: [dep:electron, dep:electron-builder, dep:@electron-forge/cli]
related: [playwright, typescript, react, vue]
---
Electron desktop apps: a privileged main process, sandboxed renderers, and a preload script exposing a narrow IPC API.

## Verify
- `npx tsc --noEmit`: main, preload and renderer types.
- `npx electron .`: the app launches (a manual smoke; end-to-end tests below automate it).
- `npx playwright test`: drives the app through `_electron.launch` (Playwright's Electron support is experimental).
- `npx electronegativity -i .`: scans for common Electron security misconfigurations, if installed.

## Test first
Unit-test main-process logic and IPC handlers as plain functions; test the window with Playwright.
```ts
import { _electron as electron, test, expect } from "@playwright/test";

test("window opens with the title", async () => {
  const app = await electron.launch({ args: ["."] });
  const win = await app.firstWindow();
  await expect(win).toHaveTitle("My App");
  await app.close();
});
```

## Do
- Create windows with `contextIsolation: true`, `nodeIntegration: false` and `sandbox: true` (the defaults in current versions; never turn them off).
- Expose a minimal API from the preload script with `contextBridge.exposeInMainWorld("api", { ... })`, one function per capability.
- Use `ipcMain.handle` with `ipcRenderer.invoke` for request and response; do not expose `ipcRenderer` itself.
- Validate every IPC argument in the main process, and check `event.senderFrame` origin for sensitive handlers.
- Set a strict Content-Security-Policy and load local content, not remote.
- Restrict navigation: handle `setWindowOpenHandler` and `will-navigate`, open external links with `shell.openExternal` only for allowlisted `https:` URLs.
- Store secrets with `safeStorage`, not plain files or localStorage.
- Sign builds and enable auto-update through your packaging tool (Forge or electron-builder), over HTTPS.
- Pin `electron` and update promptly: Chromium security fixes ship through it.

## Avoid
- `nodeIntegration: true` or `contextIsolation: false` "to make require work": any XSS becomes remote code execution. Use preload plus IPC.
- Exposing `ipcRenderer.send` or `require` through `contextBridge`: the renderer can call anything. Expose named functions.
- `shell.openExternal(userUrl)` unchecked: can launch local files or protocol handlers. Parse and allowlist `https:`.
- `remote` module and `enableRemoteModule`: removed. Use IPC.
- Loading remote URLs in a privileged window: a compromised site gets your APIs. Load local files, or isolate with a separate sandboxed `WebContentsView`.
- `webSecurity: false` or `allowRunningInsecureContent`: disables same-origin protection. Fix CORS properly.
- Heavy sync work in the main process: freezes every window. Use workers or utility processes.

## Review
- [ ] Every `BrowserWindow` keeps isolation and sandbox on, with no Node in renderers.
- [ ] The preload exposes named, narrow functions, and main validates all IPC input.
- [ ] A CSP is set and navigation and new windows are restricted.
- [ ] Secrets use `safeStorage`; builds are signed.
- [ ] An end-to-end test launches the packaged or dev app.
