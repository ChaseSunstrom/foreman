---
name: helm
title: Helm
area: infra
tags: [helm, chart, kubernetes, templates, values, release]
detect: [file:Chart.yaml, file:values.yaml, file:helmfile.yaml, file:templates/*.tpl]
related: [kubernetes, kustomize, argo-cd, flux]
---
Helm charts: templated manifests with typed values, a schema, helper templates and testable releases.

## Verify
- `helm lint ./chart --strict`: chart structure and template errors, warnings fail.
- `helm template rel ./chart -f values.yaml | kubectl apply --dry-run=server -f -`: rendered output is valid to the API server.
- `helm template rel ./chart --debug`: shows the rendered YAML with line context when a template errors.
- `helm unittest ./chart`: unit tests, when the helm-unittest plugin is installed.
- `helm upgrade --install rel ./chart --dry-run --debug`: the upgrade path computes against the live release.

## Test first
Chart tests render without a cluster. With helm-unittest, tests live in `chart/tests/*_test.yaml`.
```yaml
suite: deployment
templates: [deployment.yaml]
tests:
  - it: sets non-root by default
    asserts:
      - equal:
          path: spec.template.spec.securityContext.runAsNonRoot
          value: true
```
Red first: it fails until the template reads from `.Values` with a safe default.

## Do
- Keep `Chart.yaml` `version` (chart) and `appVersion` (app) separate, and bump `version` on any template change.
- Ship `values.schema.json` so bad values fail at `helm install` and `helm lint`.
- Put labels and names in `_helpers.tpl` (`define "app.fullname"`) and reuse them via `include`.
- Use `{{ include "x" . | nindent 4 }}` for blocks, `toYaml` for maps, and `quote` for strings that may look numeric.
- Use `required "msg" .Values.x` for values with no safe default.
- Add a pod-template checksum annotation of the ConfigMap or Secret so changes roll pods.
- Add `templates/tests/*.yaml` with `helm.sh/hook: test` for `helm test`.
- Lock subcharts with `helm dependency update` and commit `Chart.lock`.

## Avoid
- `apiVersion: v1` charts with `requirements.yaml`: Helm 2 style. Use `apiVersion: v2` and `dependencies` in `Chart.yaml`.
- `template` used for a block: it cannot be piped, so indentation breaks. Use `include` with `nindent`.
- Secrets in default `values.yaml`: they leak via `helm get values`. Reference an existing Secret by name.
- Unquoted values like `"yes"`, `1e3` or version-like strings that YAML coerces: wrap in `quote` or `toString`.
- Checking nil deep paths (`.Values.a.b.c` when `a` is missing): panics. Use `dig` or `default (dict) .Values.a`.
- `helm install` in automation: not idempotent. Use `helm upgrade --install --atomic --wait`.
- CRDs placed in `templates/`: they are not upgraded sanely. Use the `crds/` directory or a separate chart.

## Review
- [ ] `helm lint --strict` and a schema pass, and the rendered output validates server-side.
- [ ] Every configurable value has a default and a documented key in `values.yaml`.
- [ ] Selectors and labels are stable across upgrades.
- [ ] Config changes trigger pod rollouts, and `Chart.lock` is committed.
