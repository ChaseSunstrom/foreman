---
name: vscode-extension
title: VS Code extensions
area: node
tags: [vscode, extension, typescript, electron, packaging, editor]
detect: [dep:@vscode/*, file:.vscodeignore]
related: [typescript, esbuild, eslint, node]
---
VS Code extensions: a package.json manifest of contributions, an activate() that registers disposables, tests in a real VS Code host.

## Verify
- `npx tsc -p ./ --noEmit`: the extension type-checks against the `@types/vscode` it targets.
- `npm test`: the suite runs inside an Extension Development Host (`@vscode/test-electron` or `@vscode/test-cli`).
- `npx vsce ls`: the files that would ship; nothing from `src/`, tests or stray `node_modules`.
- `npx vsce package`: a .vsix builds and the manifest passes vsce's checks.

## Test first
Integration tests run with the real `vscode` API; assert on what the user sees.
```ts
import * as assert from "assert";
import * as vscode from "vscode";

suite("commands", () => {
  test("the hello command is registered", async () => {
    const all = await vscode.commands.getCommands(true);
    assert.ok(all.includes("myext.hello"));
  });
});
```

## Do
- Push every registration into `context.subscriptions` so it is disposed on deactivate.
- Keep `activate` fast: register commands and providers, start heavy work lazily.
- Declare narrow activation events (a command, a language, a workspace file) rather than activating on startup.
- Keep `engines.vscode` and the `@types/vscode` version in step; the types must not be newer than the engine.
- Bundle the extension (esbuild or webpack) and exclude sources and tests in `.vscodeignore`.
- Read settings through `vscode.workspace.getConfiguration` and react to `onDidChangeConfiguration`.
- Put pure logic in modules without `vscode` imports so plain unit tests cover it.

## Avoid
- Activating on `*`: every window pays the startup cost. Use specific activation events.
- Long synchronous work in `activate`: the extension host stalls. Defer it.
- Leaking listeners and watchers: memory grows across reloads. Dispose them through the context.
- `@types/vscode` newer than `engines.vscode`: APIs that don't exist at runtime. Align them.
- Shipping `node_modules` unbundled: large, slow packages. Bundle and check `vsce ls`.
- Hard-coding paths with `/`: breaks on Windows. Use `vscode.Uri.joinPath` and `path`.

## Review
- [ ] Activation events are specific.
- [ ] All disposables go through `context.subscriptions`.
- [ ] `engines.vscode` matches the types package.
- [ ] `vsce ls` shows only what should ship.
- [ ] Integration tests cover each contributed command.
