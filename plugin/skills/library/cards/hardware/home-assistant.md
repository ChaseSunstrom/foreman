---
name: home-assistant
title: Home Assistant
area: hardware
tags: [home-assistant, python, yaml, integration, iot, automation]
detect: [dep:homeassistant, dep:pytest-homeassistant-custom-component, file:configuration.yaml, file:custom_components/*/manifest.json]
related: [mqtt, python, pytest, ruff]
---
Home Assistant configuration and custom integrations: YAML automations, config entries, async Python components.

## Verify
- `hass --script check_config -c config`: the configuration directory validates (YAML, schemas, references).
- `pytest -q tests/`: integration tests pass using `pytest-homeassistant-custom-component`.
- `ruff check custom_components tests && ruff format --check custom_components tests`: lint and format.
- `python -m json.tool custom_components/my_domain/manifest.json`: the manifest is valid JSON.

## Test first
Tests live in `tests/`, use the `hass` fixture and `MockConfigEntry`. Enable custom integrations in `conftest.py` via an autouse fixture using `enable_custom_integrations`.
```python
from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.my_domain.const import DOMAIN

async def test_setup_creates_sensor(hass, enable_custom_integrations):
    entry = MockConfigEntry(domain=DOMAIN, data={"host": "1.2.3.4"})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.my_domain_temperature") is not None
```
Mock the device client (patch the library your integration wraps), never real network calls.

## Do
- Give each integration a `manifest.json` with `domain`, `name`, `version`, `documentation`, `requirements`, `codeowners`, `iot_class`, and `config_flow` when used.
- Use config flows (`config_flow.py`) and config entries rather than YAML setup for new integrations.
- Use `DataUpdateCoordinator` for polling: one fetch shared by all entities, with `UpdateFailed` on errors.
- Make all I/O async (`aiohttp` via `async_get_clientsession(hass)`); run blocking libraries with `hass.async_add_executor_job`.
- Give entities a stable `unique_id`, `device_info`, and `_attr_has_entity_name = True`.
- Clean up in `async_unload_entry` with `async_unload_platforms` and remove listeners.
- In YAML automations, use `trigger`/`condition`/`action` with entity IDs from `developer tools`; quote templates and secrets via `!secret`.
- Keep secrets in `secrets.yaml`, not in committed config.

## Avoid
- Blocking calls (`requests`, `time.sleep`) in the event loop: freezes Home Assistant. Use async or the executor.
- Entities without a `unique_id`: can't be renamed or managed in the UI. Provide one.
- Each entity polling the device itself: hammers it. Use a coordinator.
- Old singular keys (`platform:` lists under legacy syntax, `service:` vs `action:`): current syntax uses plural `triggers`/`conditions`/`actions` and `action:` for calls. Check the current docs for the version in use.
- Hardcoded hosts or tokens in `configuration.yaml`: use `!secret`.
- Restarting to test every YAML edit: run `check_config` first, then reload the specific domain.
- Importing from `homeassistant.components.x` internals in unrelated integrations: those are not stable APIs.

## Review
- [ ] `check_config` passes and `manifest.json` has every required key.
- [ ] No blocking I/O on the event loop; coordinator used for polling.
- [ ] Entities have `unique_id` and `device_info`; unload fully cleans up.
- [ ] Tests mock the external client and cover setup, update failure and unload.
- [ ] No secrets in committed YAML.
