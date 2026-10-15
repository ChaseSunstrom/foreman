---
name: plugin-architecture
title: Plugin architecture
area: design
tags: [plugins, extensibility, interfaces, registry, isolation, versioning]
detect: []
related: [hexagonal-architecture, dependency-injection, semver, modular-monolith, configuration]
---
A small stable core defines extension points; plugins register against a versioned interface and cannot break the host.

## Verify
- `pytest -q -k plugin`: discovery, contract and failure-isolation tests.
- `python -c "from importlib.metadata import entry_points; print(list(entry_points(group='myapp.plugins')))"`: plugins are discovered through entry points (Python; use your own group name).
- `git grep -nE "import .*plugins\." -- src/core`: the core never imports a concrete plugin.

## Test first
A broken plugin must not take the host down, and every plugin must satisfy the contract.
```python
def test_broken_plugin_is_isolated(host):
    host.register(GoodPlugin()); host.register(RaisesOnLoad())
    result = host.load_all()
    assert "good" in result.loaded and "broken" in result.failed
    assert host.run_hook("on_save", doc=1) == ["good-ok"]      # others still run

@pytest.mark.parametrize("plugin", discover_all())
def test_plugin_meets_contract(plugin):
    assert plugin.api_version in SUPPORTED_API_VERSIONS
    assert callable(plugin.on_save) and plugin.name
```

## Do
- Define extension points as narrow interfaces (Protocol, trait, abstract class) with an explicit `api_version`.
- Discover through a registry: entry points, a plugins directory with a manifest, or explicit registration. Do not scan arbitrary code at import.
- Load lazily and wrap each call in error handling, timeouts and logging that names the plugin.
- Pass plugins a limited context object (capabilities, config, logger), not the whole application.
- Declare permissions in the manifest and enforce them; run untrusted plugins out of process or in a sandbox.
- Keep core-to-plugin dependencies one-way; ship a contract test suite plugin authors can run.
- Follow semver on the interface, support N-1, and deprecate with warnings first.

## Avoid
- Plugins importing core internals: any refactor breaks them. Expose a stable API module.
- One failing plugin raising into the host loop: outage. Catch, log and disable it.
- Implicit ordering between plugins: surprising behaviour. Declare priority or dependencies.
- Loading untrusted code in process: full privileges. Isolate or review and sign.
- No version handshake: silent incompatibility. Check `api_version` at load.

## Review
- [ ] Core has no import of concrete plugins.
- [ ] Interface versioned and documented.
- [ ] Plugin failure is isolated and observable.
- [ ] Trust model and permissions defined.
