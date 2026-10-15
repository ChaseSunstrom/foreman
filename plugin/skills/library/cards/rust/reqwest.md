---
name: reqwest
title: reqwest
area: rust
tags: [rust, http, client, async, tls, reqwest]
detect: [dep:reqwest]
related: [tokio, serde, thiserror-anyhow, tracing]
---
reqwest HTTP client: one shared Client, explicit timeouts, status checks, bounded bodies, tested against a mock server.

## Verify
- `cargo clippy --all-targets -- -D warnings`: lints, including unawaited futures.
- `cargo test`: client code runs against a local mock server.
- `cargo tree -i openssl-sys`: shows whether native TLS is pulled in when you meant rustls.
- `cargo tree -e features -i reqwest`: the enabled features are what you intended (`json`, `rustls-tls`, `stream`).

## Test first
Point the client at a mock (wiremock or httpmock if present) and assert the failure path first.
```rust
#[tokio::test]
async fn maps_500_to_error() {
    let srv = wiremock::MockServer::start().await;
    wiremock::Mock::given(wiremock::matchers::any())
        .respond_with(wiremock::ResponseTemplate::new(500))
        .mount(&srv).await;
    let api = Api::new(srv.uri());
    assert!(matches!(api.fetch().await, Err(ApiError::Status(500))));
}
```

## Do
- Build one `Client` with `Client::builder().timeout(..).connect_timeout(..).build()?` and clone it; it holds the connection pool and is cheap to clone.
- Call `.error_for_status()?` (or check `status()`) before decoding.
- Decode with `.json::<T>().await?` (needs the `json` feature) and send with `.json(&body)`.
- Put query params through `.query(&[("k", v)])`, never string concatenation.
- Set `User-Agent` and default headers on the builder; mark secrets with `HeaderValue::set_sensitive(true)`.
- Retry only idempotent requests, with backoff and a cap; consider `reqwest-middleware` if already in use.
- Stream big bodies with `.bytes_stream()` (`stream` feature) and limit size.
- Pick TLS deliberately: `default-features = false, features = ["rustls-tls", "json"]` for static builds.

## Avoid
- `reqwest::get(url)` in hot paths or `Client::new()` per request: no pool reuse, handshake each time. Share one client.
- No timeout: the default is none, so a stalled server hangs the task forever. Set `timeout`.
- `.text().await.unwrap()` on unknown responses: unbounded memory and panics. Check status and cap length.
- `danger_accept_invalid_certs(true)` to "fix" TLS errors: disables verification. Add the CA with `add_root_certificate`.
- Using the `blocking` client inside an async runtime: panics or stalls. Use the async client.
- Putting tokens in URLs: they end up in logs. Use `bearer_auth`.

## Review
- [ ] One shared Client with connect and total timeouts.
- [ ] Status is checked before body decode; errors keep the status and a bounded body snippet.
- [ ] No TLS verification bypass; TLS backend chosen via features.
- [ ] Retries are limited to idempotent calls with backoff.
- [ ] Tests use a mock server, not the real network.
