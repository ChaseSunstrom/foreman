---
name: actix-web
title: Actix Web
area: rust
tags: [rust, web, api, actix, http, async]
detect: [dep:actix-web]
related: [tokio, serde, sqlx, clippy, cargo]
---
Actix Web services: App factories, extractors, web::Data state, ResponseError, in-process tests.

## Verify
- `cargo clippy --all-targets -- -D warnings`: lint.
- `cargo test`: handler tests via `actix_web::test`.
- `cargo check --all-targets`: handler and extractor signatures.
- `cargo tree -d | grep -i actix`: duplicate actix crates from mixed versions.

## Test first
Build the service with `test::init_service` and send a `TestRequest`.
```rust
use actix_web::{test, web, App};

#[actix_web::test]
async fn health_returns_ok() {
    let app = test::init_service(
        App::new().route("/health", web::get().to(crate::health)),
    ).await;
    let req = test::TestRequest::get().uri("/health").to_request();
    let res = test::call_service(&app, req).await;
    assert!(res.status().is_success());
}
```
Keep an `fn configure(cfg: &mut web::ServiceConfig)` that both `main` and tests use.

## Do
- Share state through `web::Data<T>` registered with `app_data`. Create the pool once outside the `HttpServer::new` closure and clone it in.
- Configure routes with `ServiceConfig` and `web::scope` per module.
- Implement `ResponseError` on one error enum, then return `Result<HttpResponse, AppError>` from handlers.
- Use typed extractors: `web::Json<T>`, `web::Path<T>`, `web::Query<T>`. Tune them with `JsonConfig` (size limit, error handler).
- Run blocking work through `web::block`.
- Add middleware with `wrap` (Logger, Compress, `actix-cors` Cors, auth via `from_fn` or a Transform).
- Set `.workers(n)` and `.shutdown_timeout(s)` deliberately.

## Avoid
- Building the pool or a `Mutex<Vec>` inside the `HttpServer::new` closure: each worker gets its own copy. Create once outside, wrap in `web::Data`.
- Wrapping state as `Data<Arc<T>>`: `Data` already holds an `Arc`. Double wrapping breaks extractor type lookup.
- `web::Data<T>` type mismatch between `app_data` and the handler: it returns a 500 at request time. Use the identical type.
- Blocking calls in handlers: they stall the worker thread. Use `web::block` or async clients.
- `Cors::permissive()` in production: list allowed origins.
- Mixing actix-web 4 with old 3.x-era crates or `actix_rt::main` examples: check the version first.
- `unwrap()` in handlers: use an error type that renders a response.

## Review
- [ ] Shared state is created once and is `Data<T>` with matching types.
- [ ] Errors flow through `ResponseError`, with no panics on bad input.
- [ ] Payload and JSON limits are set.
- [ ] No blocking calls in async handlers.
- [ ] Tests use `init_service` with the production `configure` function.
