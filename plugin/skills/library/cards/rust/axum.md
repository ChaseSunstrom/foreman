---
name: axum
title: Axum
area: rust
tags: [rust, web, api, axum, tower, async, http]
detect: [dep:axum]
related: [tokio, serde, sqlx, clippy, cargo]
---
Axum services: Router, extractors, shared state, tower middleware, tested in process.

## Verify
- `cargo clippy --all-targets -- -D warnings`: lint, including async footguns.
- `cargo test`: handlers driven through the Router with no socket.
- `cargo check --all-targets`: handler signatures satisfy `Handler` (errors there are long, read the first line).
- `cargo tree -i axum`: one axum version, matching the tower-http and axum-extra versions.

## Test first
Call the router as a `tower::Service` using `oneshot` (needs `tower` with the `util` feature).
```rust
use axum::{body::Body, http::{Request, StatusCode}};
use tower::ServiceExt;

#[tokio::test]
async fn unknown_item_is_404() {
    let app = crate::app(test_state());
    let res = app
        .oneshot(Request::get("/items/999").body(Body::empty()).unwrap())
        .await
        .unwrap();
    assert_eq!(res.status(), StatusCode::NOT_FOUND);
}
```
Build the router in a function so tests and `main` share it.

## Do
- Share state with `Router::with_state(AppState)` and `State<AppState>`. Make the state `Clone`, with `Arc` or pools inside.
- Put the body extractor (`Json`, `Form`, `Bytes`) last in the handler arguments.
- Return `Result<T, AppError>` and implement `IntoResponse` for `AppError`, mapping to status codes in one place.
- Layer middleware with `ServiceBuilder` or `.layer(...)`: tracing, timeout, body limit, CORS from tower-http.
- Compose with `Router::nest` and `merge`. Use the `{id}` path syntax in the current series, `:id` in older ones; check the pinned version.
- Shut down with `axum::serve(listener, app).with_graceful_shutdown(signal)`.
- Use custom extractors (`FromRequestParts`) for auth.

## Avoid
- Extractor order mistakes (body not last): a compile error pointing at the handler. Move the body extractor to the end.
- `axum::Server` and `hyper::Server` from old tutorials: use `axum::serve` with a `tokio::net::TcpListener`.
- `unwrap()` on extraction or DB results in handlers: that panics the task. Return an error type.
- Mutex-wrapped global state for everything: use a pool or channel, and don't hold a std guard across `.await`.
- Mixing axum and tower-http major versions: trait mismatches that read as missing impls. Align them.
- Leaving the default body limit unexamined: set `DefaultBodyLimit` deliberately.
- Permissive `CorsLayer::very_permissive()` in production: list origins.

## Review
- [ ] Each handler maps every failure to a deliberate status and body.
- [ ] Auth runs as middleware or an extractor, not per-handler copy-paste.
- [ ] Body size and request timeout limits are set.
- [ ] State is cheaply cloneable and holds no long-lived std lock guards.
- [ ] Tests exercise the real router, including one error path per route.
