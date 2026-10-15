---
name: cc-marketplaces
title: Plugin marketplaces
area: claude-code
tags: [claude-code, marketplace, plugin, distribution, versioning]
detect: [file:.claude-plugin/marketplace.json]
related: [cc-plugins, cc-plugin-manifest, cc-plugin-release]
---
A marketplace is a repo with `.claude-plugin/marketplace.json` listing plugins by `source`; users add it and install from it.

## Verify
- `claude plugin validate .`: run at the marketplace root to check the catalog and the manifests it points at.
- `python3 -m json.tool .claude-plugin/marketplace.json`: catalog parses.
- `claude --plugin-dir ./plugin`: the plugin itself loads before you publish the entry.
- `jq -r '.plugins[] | .source' .claude-plugin/marketplace.json`: each listed source path exists on disk.

## Test first
A script that fails when the catalog and manifests disagree.
```python
import json, pathlib
def test_catalog_matches_manifests():
    cat = json.loads(pathlib.Path(".claude-plugin/marketplace.json").read_text())
    for e in cat["plugins"]:
        m = json.loads((pathlib.Path(e["source"]) / ".claude-plugin/plugin.json").read_text())
        assert m["name"] == e["name"] and m["version"] == e["version"]
```

## Do
- Shape: `name`, `owner: {name}`, optional `metadata: {description, version}`, and `plugins: [{name, source, description, version}]`.
- Use a relative `source` (`./plugin`) for plugins in the same repo; a local-path marketplace loads in place, so edits apply on reload.
- Keep one version string per plugin and bump the manifest and the entry together; the manifest's `version` wins when they differ.
- Remember that `strict` defaults to true: an entry may add components to a plugin that has its own manifest. With `strict: false` the entry must not declare components the manifest also declares.
- Entries accept the manifest fields except the directory-listing ones (`icon`, support and policy URLs); set those in `plugin.json`.
- Use `displayName` and `defaultEnabled` on the entry to control listing and starting state.

## Avoid
- Catalog and manifest versions drifting: users see stale or pinned installs. Bump both in one commit, and assert it in a test.
- Listing a plugin whose `source` has no content at that path: it fails to install. Check the path exists.
- Entry `hooks` as a file path or array when there is no `plugin.json`: only the inline object form loads. Inline it.
- Directory-listing fields in an entry: reported unknown. Move them to `plugin.json`.
- Changing `defaultEnabled` and expecting existing users to change: their saved `enabledPlugins` entry persists.

## Review
- [ ] Every entry has `name`, `source`, `description`, `version`, and the source exists.
- [ ] Entry versions equal manifest versions.
- [ ] No two entries share a name.
- [ ] `claude plugin validate .` passes at the catalog root.
