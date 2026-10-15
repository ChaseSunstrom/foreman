---
name: cc-plugin-release
title: Releasing a plugin
area: claude-code
tags: [claude-code, plugin, release, versioning, marketplace, changelog]
detect: [file:.claude-plugin/marketplace.json]
related: [cc-marketplaces, cc-plugin-manifest, cc-plugin-testing, cc-plugin-evals]
---
A release is a version bump that agrees everywhere, a green validate and test run, and a catalog entry users can install.

## Verify
- `claude plugin validate --strict .`: manifest and catalog pass with warnings as failures.
- `grep -rn '"version"' .claude-plugin/ plugin/.claude-plugin/`: every version string you ship, to compare by eye or in a test.
- `python3 -m unittest discover -s tests -t tests`: the suite is green on the tree you tag.
- `claude --plugin-dir ./plugin -p "ping" --output-format stream-json --verbose`: a fresh session loads it (check `plugin_errors` in `system/init`).

## Test first
A version-agreement test that fails before the bump is done.
```python
import json, pathlib
def test_versions_agree():
    m = json.loads(pathlib.Path("plugin/.claude-plugin/plugin.json").read_text())["version"]
    cat = json.loads(pathlib.Path(".claude-plugin/marketplace.json").read_text())
    entry = next(p for p in cat["plugins"] if p["name"] == "myplugin")
    assert entry["version"] == m == cat["metadata"]["version"]
```

## Do
- Bump `version` in `plugin.json` and the catalog entry in the same commit; the manifest wins when they differ.
- Remember that an explicit `version` pins installs: users update only when it changes.
- Keep a changelog entry per release and a note for any breaking change (renamed skills, hook behavior).
- Run validate with `--strict`, the test suite, and an eval smoke run before tagging.
- Tag the commit (`git tag vX.Y.Z`) so a release is reproducible.
- Keep state out of `${CLAUDE_PLUGIN_ROOT}`; it changes on update. Migrate state in `${CLAUDE_PLUGIN_DATA}` with versioned files.
- State the minimum Claude Code version when you use newer features, such as `userConfig` `options` (2.1.271) or `onFailure` on hooks (2.1.295).

## Avoid
- Editing code without bumping `version`: users with the old pinned version never see it. Bump.
- Letting the catalog and manifest drift: mismatched listings. Assert equality in a test.
- Breaking renames without a note: users' saved settings and permissions reference old names. Document or alias.
- Releasing on a red or unvalidated tree: fix, then tag.
- Relying on new manifest fields while claiming older support: older builds reject strict objects. Declare the minimum version.
- Shipping secrets or local paths in the manifest or fixtures.

## Review
- [ ] Versions agree in manifest, catalog and tag.
- [ ] `claude plugin validate --strict .` and tests pass.
- [ ] Changelog and breaking-change notes are written.
- [ ] Minimum Claude Code version is documented.
- [ ] A fresh `--plugin-dir` session loads without errors.
