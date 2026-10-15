---
name: grafana
title: Grafana
area: infra
tags: [grafana, dashboards, provisioning, observability, panels, alerting]
detect: [file:grafana.ini, file:provisioning/dashboards/*.yaml, file:provisioning/datasources/*.yaml, file:dashboards/*.json, file:*.dashboard.json]
related: [prometheus, loki, opentelemetry, kubernetes]
---
Grafana: dashboards and alerting managed as code via provisioning files, with variables and datasource UIDs.

## Verify
- `jq empty dashboards/*.json`: every dashboard file is valid JSON.
- `jq -e '.uid and .title and (.schemaVersion|type=="number")' dashboards/app.json`: required top-level keys exist.
- `curl -s -u admin:$GF_PASS localhost:3000/api/health`: the server is up.
- `curl -s -u admin:$GF_PASS localhost:3000/api/search?query=app`: the provisioned dashboard loaded.
- `grep -rn '"datasource": *"' dashboards/`: no dashboard references a datasource by name (use uid).

## Test first
Check that the provisioned dashboard appears and queries resolve, in a throwaway Grafana container.
```sh
docker run -d --name g -p 3000:3000 \
  -v $PWD/provisioning:/etc/grafana/provisioning \
  -v $PWD/dashboards:/var/lib/grafana/dashboards grafana/grafana
curl -fsS -u admin:admin localhost:3000/api/dashboards/uid/app-overview   # red until it exists
```
Red first: it returns 404 until the JSON has `uid: app-overview` and the provider path matches.

## Do
- Provision datasources (`apiVersion: 1`, `datasources:` with a fixed `uid`) and dashboard providers (`providers:` with `options.path`).
- Keep each dashboard JSON with a stable `uid`, `id: null`, and `version` managed by git. Export with "Export for sharing externally" or use the HTTP API.
- Reference datasources by `{ "type": "prometheus", "uid": "..." }`, or by a `${DS_PROMETHEUS}` variable.
- Use template variables (`label_values(metric, label)`) with `$__rate_interval` for rate windows.
- Set units, thresholds and descriptions per panel, and put `$__interval` in query steps.
- Manage alert rules as code with file provisioning or the Terraform provider, and route through contact points.
- Pass secrets with `$__env{VAR}` or `$__file{path}` in provisioning files.
- Set `allowUiUpdates: false` so provisioned dashboards stay the source of truth.

## Avoid
- Editing a provisioned dashboard in the UI and expecting it to persist: the file wins on restart. Edit the JSON.
- `id` set in exported JSON: conflicts on import. Set `id: null` and keep `uid`.
- Datasource by display name: renaming breaks panels. Use uid.
- Hardcoded `[5m]` in rate queries: wrong at other zooms. Use `$__rate_interval`.
- Default `admin:admin` credentials or anonymous admin in production: change them, and use OAuth or SSO.
- Secrets in provisioning YAML committed in clear: use env or file interpolation.
- Queries returning high-cardinality series per panel: slow dashboards. Aggregate with `sum by`.
- Legacy "classic" alerting (panel alerts): removed. Use Grafana-managed alert rules.

## Review
- [ ] Datasources and dashboards are provisioned with stable uids.
- [ ] No dashboard depends on a datasource name or fixed rate windows.
- [ ] Secrets use interpolation, and default credentials are changed.
- [ ] Alert rules have contact points and are version-controlled.
