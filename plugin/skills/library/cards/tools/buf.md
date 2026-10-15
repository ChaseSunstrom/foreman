---
name: buf
title: Buf
area: tools
tags: [protobuf, grpc, lint, breaking-changes, codegen]
detect: [file:buf.yaml, file:buf.gen.yaml, file:buf.work.yaml]
related: [openapi-generator, pre-commit]
---
Buf: lints Protobuf, detects wire and source breaking changes against a baseline, and runs code generation from buf.gen.yaml.

## Verify
- `buf lint`: style and structure rules from buf.yaml pass.
- `buf build`: every proto compiles and imports resolve.
- `buf breaking --against '.git#branch=main'`: no breaking change relative to main.
- `buf format -d --exit-code`: formatting is canonical (diff printed, nonzero if not).
- `buf generate`: generated code builds from the current protos, then check the diff.

## Test first
Prove the rule catches the change before you rely on it.
```
sed -i 's/string name = 2;/string title = 2;/' proto/acme/v1/item.proto
buf breaking --against '.git#branch=main'   # expect a FIELD_SAME_NAME finding (FILE category)
git checkout proto/acme/v1/item.proto
```
For a lint rule, add a violation (for example a lowerCamel message name), and `buf lint` must fail.

## Do
- Keep protos in versioned packages (`acme.item.v1`) in a matching directory layout.
- Choose the breaking category deliberately: `WIRE_JSON` or `WIRE` for services where only the wire matters, `FILE` for generated source stability.
- Run `buf breaking` in CI against the default branch, and `buf lint` and `buf format` on every PR.
- Pin plugins and managed-mode options in `buf.gen.yaml`, so generated code does not drift.
- Reserve removed field numbers and names: `reserved 4; reserved "old_name";`.
- Add new fields instead of changing types, and bump the package version for real breaks.

## Avoid
- Reusing or renumbering a field: old clients decode garbage. Reserve the number and add a new field.
- Renaming a field in a JSON-exposed API under only the WIRE category: JSON breaks. Use `WIRE_JSON` or keep the name.
- Disabling a lint rule globally to silence one file: use `ignore_only` for that path.
- Shallow clones in CI with `.git#branch=main`: the baseline is missing. Fetch the base branch.
- Changing `enum` zero values or removing an enum value without reserving it: reserve the value and name.
- Committing generated code from an unpinned plugin: pin its version or ref in `buf.gen.yaml`.

## Review
- [ ] `buf lint`, `buf format -d --exit-code` and `buf breaking` pass.
- [ ] Removed fields and enum values are reserved.
- [ ] The breaking category matches how clients consume the API.
- [ ] Generated output is current and plugin versions are pinned.
