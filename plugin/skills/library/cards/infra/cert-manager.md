---
name: cert-manager
title: cert-manager
area: infra
tags: [cert-manager, tls, kubernetes, acme, certificates, issuer]
detect: [file:cert-manager.yaml, file:clusterissuer.yaml, file:issuer.yaml, file:certificate.yaml, file:cluster-issuer.yaml]
related: [kubernetes, helm, nginx, traefik, vault]
---
cert-manager: Kubernetes-native certificate issuance and renewal through Issuers, ClusterIssuers and Certificate resources.

## Verify
- `kubectl get clusterissuer,issuer,certificate -A`: all show `READY True`.
- `kubectl describe certificate <name> -n <ns>`: events and conditions explain issuance state.
- `kubectl get certificaterequest,order,challenge -A`: ACME progress, and the failing step when stuck.
- `cmctl status certificate <name> -n <ns>`: a consolidated view (needs the `cmctl` CLI).
- `kubectl get secret <name> -n <ns> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -dates -subject`: the issued cert and its validity.

## Test first
Use the staging ACME or a self-signed issuer first and assert Ready, before production.
```sh
kubectl apply -f certificate.yaml
kubectl wait --for=condition=Ready certificate/app-tls -n app --timeout=120s   # red until issuer and DNS or HTTP route work
kubectl get secret app-tls -n app -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -ext subjectAltName | grep -q app.example.com
```

## Do
- Create a `ClusterIssuer` for ACME with `server`, `email`, `privateKeySecretRef` and a `solvers` list (`http01.ingress.ingressClassName` or `dns01`).
- Start against the Let's Encrypt staging server, then switch the `server` URL for production.
- Request certs with `Certificate` (`secretName`, `dnsNames`, `issuerRef`, `duration`, `renewBefore`) or by annotating an Ingress with `cert-manager.io/cluster-issuer`.
- Use `dns01` for wildcards and for private clusters, with credentials in a Secret or workload identity.
- Install with Helm and `crds.enabled=true` (or install CRDs separately), pin the chart version, and monitor controller metrics.
- Set `privateKey.rotationPolicy: Always` to rotate keys on renewal.
- Alert on `certmanager_certificate_expiration_timestamp_seconds` and `certmanager_certificate_ready_status`.
- Use the `selfSigned` or `CA` issuer for internal mTLS, or the Vault issuer for an internal PKI.

## Avoid
- Testing against production Let's Encrypt: rate limits (failed validations and duplicate certs) lock you out. Use staging first.
- `certmanager.k8s.io` API groups and `v1alpha2` or `v1beta1` versions: removed. Use `cert-manager.io/v1`.
- The `kubernetes.io/tls-acme` annotation alone with no issuer annotation: legacy and does nothing without ingress-shim config. Use `cert-manager.io/cluster-issuer`.
- Wildcards with `http01`: unsupported. Use `dns01`.
- Challenge pending because the ingress class or a redirect blocks `/.well-known/acme-challenge`: check `kubectl describe challenge` and allow the path over HTTP.
- Deleting the secret to force renewal in production: causes downtime. Use `cmctl renew`.
- Issuer and Secret in different namespaces: an `Issuer` is namespaced. Use a `ClusterIssuer` for shared use, and note its secrets live in the cert-manager namespace.
- Not pinning CRDs with Helm upgrades: CRDs lag and the controller fails. Upgrade CRDs with the chart.

## Review
- [ ] Issuers and Certificates are Ready, using `cert-manager.io/v1`.
- [ ] Staging was used before production and rate limits are respected.
- [ ] The solver matches the need (dns01 for wildcards and private networks).
- [ ] Expiry and readiness metrics feed alerts.
