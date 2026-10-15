---
name: ngrok
title: ngrok
area: tools
tags: [tunnel, webhooks, localhost, http, debugging]
detect: []
related: [curl-httpie, mkcert, tcpdump]
---
ngrok: exposes a local port at a public URL, to test webhooks and share a dev server, with a local inspector for requests.

## Verify
- `ngrok http 3000`: starts a tunnel to local port 3000 and prints the public URL.
- `curl -s http://127.0.0.1:4040/api/tunnels`: the local agent API lists active tunnels and their public URLs.
- `curl -i https://<your-subdomain-from-output>/health`: the public URL reaches your app.
- `ngrok config check`: the agent config file is valid.
- `curl -s http://127.0.0.1:3000/health`: the app answers locally first, so a tunnel failure is not an app failure.

## Test first
Prove the local service before blaming the tunnel.
```
curl -i http://127.0.0.1:3000/webhook -d '{"ping":1}' -H 'content-type: application/json'
# 2xx locally, then through the tunnel:
curl -i "$(curl -s http://127.0.0.1:4040/api/tunnels | python3 -c 'import sys,json;print(json.load(sys.stdin)["tunnels"][0]["public_url"])')/webhook" -d '{"ping":1}' -H 'content-type: application/json'
```
Open the inspector at port 4040 to see the request and replay it.

## Do
- Authenticate once with `ngrok config add-authtoken <token>` (the token lives in the agent config, not in the repo).
- Use the inspector (`http://127.0.0.1:4040`) to view headers and bodies, and to replay a webhook while you fix the handler.
- Verify the webhook signature in the app, since the URL is public.
- Use a reserved domain when the provider needs a fixed callback URL.
- Bind the app to localhost, and tunnel only the port you need.
- Stop the tunnel when done.

## Avoid
- Leaving a tunnel to an admin or debug server running: it is open to the internet. Add auth, or stop it.
- Hard-coding the random URL in provider settings: it changes on restart on free plans. Use a reserved domain.
- Host header checks failing (allowed hosts, CORS): add the tunnel hostname to the dev allow list, or forward the host with the agent's host header option.
- Testing a webhook with no signature check, then shipping the same: add verification before deploy.
- Committing the authtoken or a config with it: rotate the token and keep it out of git.
- Tunneling HTTPS-only local servers without the right scheme: point at `https://localhost:PORT` with the matching flags, or tunnel plain HTTP.

## Review
- [ ] The app answers locally before the tunnel is blamed.
- [ ] Webhook handlers verify signatures and are idempotent for replays.
- [ ] No authtoken or tunnel URL is committed.
- [ ] Tunnels are closed, and tunneled dev servers have auth.
