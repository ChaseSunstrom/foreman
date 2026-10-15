---
name: heroku
title: Heroku
area: cloud
tags: [heroku, paas, dynos, procfile, buildpacks, add-ons]
detect: [file:Procfile, file:app.json, file:heroku.yml, file:.slugignore, file:runtime.txt]
related: [railway, fly-io]
---
Heroku apps: a `Procfile` of process types, buildpacks or container stack, config vars, release phase, ephemeral dynos.

## Verify
- `heroku releases -a APP`: recent releases and whether the release phase succeeded.
- `heroku ps -a APP`: dynos are up, by process type.
- `heroku logs --tail -a APP`: live router and app logs (look for H10, H12, R14).
- `heroku config -a APP`: config var names set (never paste values into chat or commits).
- `heroku run -a APP -- <cmd>`: runs a one-off dyno.

## Test first
Fail on the Procfile and the boot contract.
```python
def test_procfile_declares_web_with_port():
    lines = dict(l.split(":", 1) for l in open("Procfile") if ":" in l)
    web = lines["web"]
    assert "$PORT" in web
```
Then `curl -fsS https://APP.herokuapp.com/healthz` after release.

## Do
- Declare process types in `Procfile` (`web`, `worker`, `release`); bind `web` to `0.0.0.0:$PORT`.
- Put migrations in the `release` process so a failed one blocks the release.
- Store settings in config vars (`heroku config:set`); read them from the environment.
- Pin the runtime (`.python-version`, `engines` in `package.json`, `.ruby-version`) and lock dependencies.
- Use `app.json` for review apps, add-ons and `scripts.postdeploy`.
- Use a connection pool sized to the dyno count and the database plan limit.
- Write logs to stdout and stderr; Heroku routes them with Logplex.
- Use Standard or Performance dynos for production, with at least two web dynos.
- Handle SIGTERM: dynos get 30 seconds to exit.

## Avoid
- Writing files to the dyno disk expecting persistence: it is ephemeral and reset on restart (at least daily). Use S3 or a database.
- Not binding to `$PORT`: boot times out with R10, and the app crashes with H10.
- Free or Eco dynos for production: they sleep or have limits.
- Running `db:migrate` in the web start command: several dynos race.
- Committing `.env` or config values; read `DATABASE_URL` from the environment because it can change.
- Long requests: the router times out at 30 seconds (H12). Return 202 and queue the work.
- Heavy slug size from vendored assets: use `.slugignore`.

## Review
- [ ] `web` binds to `$PORT`, `release` handles migrations.
- [ ] Config only in config vars; runtime pinned.
- [ ] No reliance on local disk.
- [ ] Pool sizes fit the database plan.
- [ ] SIGTERM handled and at least two production web dynos.
