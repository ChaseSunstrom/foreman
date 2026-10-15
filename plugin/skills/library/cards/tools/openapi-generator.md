---
name: openapi-generator
title: OpenAPI Generator
area: tools
tags: [openapi, codegen, sdk, api, client, spec]
detect: [file:openapitools.json, dep:@openapitools/openapi-generator-cli]
related: [buf, fastapi, curl-httpie]
---
OpenAPI Generator: builds client SDKs, server stubs and docs from an OpenAPI spec, so the spec is the source of truth.

## Verify
- `openapi-generator-cli validate -i openapi.yaml`: the spec is valid before anything is generated.
- `openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o /tmp/out`: generation succeeds for the target (swap the generator name).
- `openapi-generator-cli list`: the generator name you pass to `-g` exists.
- `git diff --stat -- generated/`: regenerating produces no diff when the spec did not change (output is deterministic and committed, or fully ignored).
- Build and test the generated package with its own tool (`tsc --noEmit`, `go build ./...`, `pytest`).

## Test first
Break the contract in the spec and see what fails, or reproduce the bad output.
```
openapi-generator-cli validate -i openapi.yaml   # fails on a $ref typo or missing operationId
openapi-generator-cli generate -i openapi.yaml -g python -o /tmp/out
grep -n "def create_item" -r /tmp/out            # the operationId became the method name
```

## Do
- Pin the generator version in `openapitools.json` (or the image tag) so output does not drift between machines.
- Give every operation a stable `operationId`: it becomes the method name.
- Keep options in a config file passed with `-c`, and templates overrides in a `-t` directory under version control.
- Use `.openapi-generator-ignore` to protect hand-written files from overwrite.
- Decide once: commit generated code and check for drift in CI, or generate at build time and ignore it.
- Keep the spec lint (for example validate) as a CI step before generation.

## Avoid
- Editing generated files by hand: the next run erases it. Change the spec, config or templates.
- Unpinned generator versions: naming and formatting change on upgrade. Pin and upgrade in one reviewed commit.
- Missing `operationId`: names get derived from the path and break clients when paths change. Add them.
- Using `oneOf` or `allOf` heavy specs without checking the output: several generators handle them poorly. Inspect the models.
- Committing output from a different generator version than CI uses: CI diff check fails. Regenerate with the pinned one.
- Forgetting `additionalProperties` and nullable semantics: clients reject valid payloads. Test with a real response.

## Review
- [ ] The spec validates and the diff in generated code matches the spec change.
- [ ] The generator version and options are pinned in the repo.
- [ ] Hand-written code sits outside generated paths or in the ignore file.
- [ ] CI regenerates and fails on drift, or the output is not committed.
