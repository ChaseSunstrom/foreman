---
name: direnv
title: direnv
area: tools
tags: [environment, shell, dotenv, per-directory, dev-setup]
detect: [file:.envrc]
related: [mise, shell-scripting, mkcert]
---
direnv: loads and unloads environment variables per directory from an .envrc file, after you explicitly allow it.

## Verify
- `direnv status`: the loaded .envrc, whether it is allowed, and the last load time.
- `direnv allow`: approve the current .envrc contents (required again after every edit).
- `direnv export json | head`: the variables direnv would set, without touching the shell.
- `env | grep MY_VAR`: the variable is in the shell after `cd` into the directory.
- `bash -n .envrc`: the file has no syntax errors (it is bash).

## Test first
Prove the variable appears inside the directory and disappears outside it.
```
cd project && echo 'export APP_ENV=dev' > .envrc
direnv allow
echo "$APP_ENV"           # dev
cd .. && echo "${APP_ENV-unset}"   # unset
```

## Do
- Hook direnv into the shell (`eval "$(direnv hook bash)"`, or the zsh or fish equivalent) once in the rc file.
- Use the stdlib helpers: `dotenv`, `dotenv_if_exists .env.local`, `PATH_add bin`, `layout python`, `use_nix` or `use mise` where available.
- Commit `.envrc` when it has no secrets, and put secrets in an ignored `.env.local` loaded by `dotenv_if_exists`.
- Keep `.envrc` fast: it runs on every `cd` into the tree. Cache slow lookups.
- Use `source_up` to inherit a parent directory's .envrc in monorepos.
- Run `direnv allow` after reviewing diffs from a pull, since changed .envrc files are blocked until you do.
- In CI, set variables normally instead of relying on direnv.

## Avoid
- `direnv allow` on a freshly cloned or pulled .envrc without reading it: it executes arbitrary shell. Read first.
- Secrets in a committed .envrc: they land in git history. Use ignored files or a secret manager, and rotate leaked ones.
- Slow commands (network calls, `docker ps`) in .envrc: the prompt lags. Cache or move to a task.
- Editing .envrc and wondering why nothing changed: it is blocked until the next `direnv allow`.
- Exporting PATH by string concatenation: use `PATH_add`, which avoids duplicates.
- Expecting direnv in non-interactive scripts: only the hook loads it. Use `direnv exec . cmd`.

## Review
- [ ] .envrc contains no secrets and runs quickly.
- [ ] A new contributor can run `direnv allow` and get the variables, with an example env file provided.
- [ ] Ignored local files hold the real secrets.
- [ ] CI and scripts set env explicitly or use `direnv exec`.
