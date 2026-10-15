---
name: keycloak
title: Keycloak
area: infra
tags: [keycloak, oidc, saml, sso, identity, oauth, realm]
detect: [file:*-realm.json, file:realm-export.json, dep:keycloak-js, dep:python-keycloak, dep:keycloak-connect]
related: [vault, cert-manager, kubernetes-rbac, nginx]
---
Keycloak: realms, clients and roles as code, OIDC flows done correctly, and production settings that are not dev defaults.

## Verify
- `curl -s https://HOST/realms/REALM/.well-known/openid-configuration | jq .issuer`: the realm discovery document answers with the expected issuer.
- `kc.sh show-config`: effective server configuration (from the distribution's bin directory).
- `kc.sh build && kc.sh start --optimized --hostname HOST`: production-mode start with a built configuration.
- `curl -s -o /dev/null -w '%{http_code}' https://HOST/health/ready`: readiness, when `--health-enabled=true` is set.

## Test first
Prove the token contract against a throwaway realm.
```bash
tok=$(curl -s -d grant_type=password -d client_id=app -d username=alice -d password=pw \
  http://localhost:8080/realms/test/protocol/openid-connect/token | jq -r .access_token)
test "$tok" != null
echo "$tok" | cut -d. -f2 | base64 -d 2>/dev/null | jq -e '.realm_access.roles | index("user")'
```
Use Testcontainers or `docker compose` with `--import-realm` to start the realm from a committed export.

## Do
- Use the Quarkus distribution; configure with `KC_*` environment variables or `kc.sh` flags, not the legacy WildFly settings.
- Run production with `start`, `--hostname`, a TLS terminating proxy setting (`--proxy-headers xforwarded` or `forwarded`) and an external database.
- Authorization Code flow with PKCE for browser and mobile clients; make SPAs public clients and backends confidential.
- Set exact `Valid redirect URIs` and `Web origins`; keep the `iss` and `aud` checks in resource servers by validating tokens via JWKS.
- Keep realm config as code: `kc.sh export` for review, `--import-realm` with files in the `data/import` directory for repeatable setups.
- Map roles into tokens with client scopes and protocol mappers; use groups for assignment.
- Set token lifespans, brute-force detection and required actions per realm policy.
- Back up the database and test upgrades on a copy first.

## Avoid
- Password grant (direct access grants) in production apps: it exposes credentials to clients. Use the code flow with PKCE.
- `start-dev` in production: HTTP, no caching, weak defaults. Use `start`.
- Redirect URI wildcards such as `*`: open redirect and token theft. List exact URLs.
- Default `admin` bootstrap credentials left in place: set `KC_BOOTSTRAP_ADMIN_USERNAME` and password only for first start, then rotate.
- Trusting token claims without verifying signature, issuer and audience: validate with the JWKS endpoint.
- Exporting realms with secrets into git: strip client secrets or encrypt the file.

## Review
- [ ] Production run uses `start` with hostname and TLS configured.
- [ ] Clients use PKCE or confidential flows with exact redirect URIs.
- [ ] Resource servers verify signature, issuer and audience.
- [ ] Realm config is reproducible and contains no secrets.
- [ ] Admin access and backups are controlled.
