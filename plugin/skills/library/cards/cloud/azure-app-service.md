---
name: azure-app-service
title: Azure App Service
area: cloud
tags: [azure, app-service, webapp, deploy, slots, az]
detect: [file:azure.yaml, file:.deployment, file:web.config, file:.azure/*.yml, file:.github/workflows/azure*.yml]
related: [azure-bicep, azure-functions, cloud-cost]
---
Azure App Service web apps: app settings, deployment slots, managed identity, health checks, container or code deploys.

## Verify
- `az webapp show -g RG -n APP --query '[state,httpsOnly,siteConfig.minTlsVersion]' -o tsv`: running, HTTPS only, TLS floor set.
- `az webapp log tail -g RG -n APP`: live application and platform logs.
- `az webapp config appsettings list -g RG -n APP -o table`: settings as deployed (secrets should be Key Vault references).
- `curl -fsS https://APP.azurewebsites.net/healthz`: the deployed app answers.

## Test first
The check that fails first is a post-deploy smoke test on the slot, before swap.
```python
import os, urllib.request

def test_staging_slot_healthy():
    url = os.environ["SLOT_URL"] + "/healthz"
    with urllib.request.urlopen(url, timeout=10) as r:
        assert r.status == 200
```
App unit tests stay in the framework's harness.

## Do
- Deploy to a staging slot, warm it, then `az webapp deployment slot swap`; mark connection strings and settings that must stay put as slot-sticky.
- Bind to the port the platform provides (`PORT` or `WEBSITES_PORT` for containers).
- Turn on `httpsOnly`, minimum TLS 1.2, and FTPS-only or FTP disabled.
- Use system-assigned managed identity and Key Vault references (`@Microsoft.KeyVault(SecretUri=...)`) for settings.
- Configure the health check path so unhealthy instances leave rotation.
- Enable Always On for plans that support it for non-trivial apps.
- Send logs to Application Insights or a Log Analytics workspace.
- Define the plan, app and settings in IaC (Bicep), not by clicking.
- Use autoscale rules or a fixed instance count sized to load.

## Avoid
- Editing settings on the production app by hand: it drifts from IaC and restarts the app.
- Storing state on local disk: only `/home` persists, it is shared across instances, and it is not for hot data.
- Basic auth publishing credentials in CI: use OIDC login and `azure/webapps-deploy`.
- Free or Shared tiers for production: no Always On, no slots, CPU quotas.
- Missing `WEBSITES_PORT` on a container that does not listen on 80.
- Swapping without warm-up: users hit a cold app. Use slot auto-swap with warm-up or preswap checks.

## Review
- [ ] HTTPS only, TLS 1.2 or higher, FTP off.
- [ ] Secrets are Key Vault references; identity is managed.
- [ ] Health check path and slot swap flow in place.
- [ ] Settings flagged sticky correctly.
- [ ] Infrastructure matches the Bicep source.
