---
name: mkcert
title: mkcert
area: tools
tags: [tls, https, certificates, localhost, development]
detect: []
related: [ngrok, curl-httpie, direnv]
---
mkcert: creates a local certificate authority trusted by your machine and issues locally trusted certificates for dev hostnames.

## Verify
- `mkcert -CAROOT`: where the local CA lives (never share or commit it).
- `mkcert -install`: the CA is added to the system and browser trust stores.
- `openssl x509 -in localhost.pem -noout -text | grep -A1 "Subject Alternative Name"`: the cert covers every hostname and IP you use.
- `openssl x509 -in localhost.pem -noout -dates`: the validity window has not passed.
- `curl --cacert "$(mkcert -CAROOT)/rootCA.pem" https://localhost:8443/`: the server presents the cert and a client trusting the CA accepts it.

## Test first
Prove the name you will use is in the cert before wiring it into the server.
```
mkcert -install
mkcert -key-file key.pem -cert-file cert.pem localhost 127.0.0.1 ::1 app.test
openssl x509 -in cert.pem -noout -ext subjectAltName   # lists all four
# start the server with the pair, then:
curl -sS --cacert "$(mkcert -CAROOT)/rootCA.pem" https://app.test:8443/ --resolve app.test:8443:127.0.0.1
```

## Do
- List every hostname and IP in one command, including `localhost`, `127.0.0.1` and `::1`.
- Name output files explicitly with `-key-file` and `-cert-file`.
- Keep generated keys and certs out of git (`*.pem` in the ignore file), and document the command in the README instead.
- For Node, set `NODE_EXTRA_CA_CERTS="$(mkcert -CAROOT)/rootCA.pem"`, since Node ignores the system store.
- For other machines or containers, copy only `rootCA.pem` (never `rootCA-key.pem`) and install it in that trust store.
- Use `*.app.test` wildcard certs for subdomains.

## Avoid
- Using these certs in production or sharing the CA key: anyone holding it can mint certs your machine trusts. Keep it local, and use a real CA for public hosts.
- Forgetting `mkcert -install` after a new browser profile or OS: the browser still warns. Rerun it, and restart the browser.
- Certificates missing the hostname used in code (`127.0.0.1` vs `localhost`): name mismatch. Add both.
- Firefox or Java trust stores not picked up: install needs the NSS tools or `JAVA_HOME` set when you run `mkcert -install`.
- Committing `key.pem`: rotate by regenerating and ignoring the file.
- Docker containers calling the host over HTTPS without the CA: mount `rootCA.pem` and update the container trust.

## Review
- [ ] SAN list covers each hostname and IP the app uses.
- [ ] No keys or CA files are in git.
- [ ] Node and container clients are told about the CA explicitly.
- [ ] Nothing outside dev uses the local CA.
