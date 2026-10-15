---
name: cdn-caching
title: CDN and HTTP caching
area: ops
tags: [cdn, cache, http, headers, purge, edge]
detect: []
related: [load-balancing, dns, certificate-rotation, uptime-monitoring]
---
Cache at the edge by sending explicit headers per route, then confirm hit, miss, and purge behavior with curl.

## Verify
- `curl -sI https://example.com/app.js`: `Cache-Control`, `ETag`, `Vary`, and the CDN's hit or miss header.
- `curl -sI https://example.com/app.js | grep -i '^age'`: a nonzero `Age` proves a cached copy served.
- `curl -s -o /dev/null -w '%{http_code}\n' -H 'If-None-Match: "<etag>"' https://example.com/app.js`: 304 means revalidation works.
- `curl -sI -H 'Accept-Encoding: br, gzip' https://example.com/ | grep -i content-encoding`: compression negotiated.
- `curl -sI 'https://example.com/?utm_source=x'`: whether junk query strings fragment the cache key.

## Test first
Write the cache contract as a script that fails on a miss-forever route.
```sh
u=https://example.com/static/app.3f9c1.js
curl -s -o /dev/null "$u"
h=$(curl -sI "$u")
echo "$h" | grep -qi 'cache-control:.*immutable' || { echo "no immutable"; exit 1; }
age=$(echo "$h" | awk -F': ' 'tolower($1)=="age"{print $2+0}')
[ "${age:-0}" -gt 0 ] || { echo "second request not cached"; exit 1; }
```
Also assert that `/account` returns `private` or `no-store`.

## Do
- Fingerprint static assets (`app.<hash>.js`) and send `Cache-Control: public, max-age=31536000, immutable`.
- Send `no-cache` (revalidate) on HTML shells, and `private, no-store` on authenticated or per-user responses.
- Emit `ETag` or `Last-Modified` and honor conditional requests.
- Set `Vary` only on headers that truly change the body (`Accept-Encoding`); every extra Vary shrinks the hit ratio.
- Use `s-maxage` for edge and `max-age` for browsers when they should differ; `stale-while-revalidate` and `stale-if-error` smooth origin trouble.
- Normalize the cache key: drop tracking params, sort the query, ignore cookies on static paths.
- Purge by URL or surrogate tag on deploy, and test the purge.
- Track hit ratio and origin offload, and alert on a drop.

## Avoid
- Caching responses that set cookies or carry auth: one user's page is served to another. Mark them `private` and strip `Set-Cookie` from cacheable routes.
- Long max-age on non-fingerprinted files: users run stale code for a year. Fingerprint or shorten.
- `Vary: Cookie` or `Vary: *` on public pages: every visitor is a unique key. Remove it.
- Purging everything on each deploy: origin stampede. Purge changed paths, and enable request collapsing or origin shielding.
- Caching 5xx or 404 for a long time: a blip becomes an outage. Use short negative TTLs.
- Testing only through the browser: devtools hides CDN headers. Use `curl -I`.

## Review
- [ ] Each route class has a stated Cache-Control policy, tested by a script.
- [ ] Authenticated responses are never public-cached.
- [ ] Cache key excludes noise params and unneeded Vary.
- [ ] Deploy includes a targeted purge and a post-purge check.
- [ ] Hit ratio and origin load are monitored.
