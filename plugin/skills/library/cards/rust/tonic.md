---
name: tonic
title: tonic (gRPC)
area: rust
tags: [rust, grpc, protobuf, tonic, prost, streaming]
detect: [dep:tonic, dep:tonic-build, dep:prost, file:build.rs]
related: [tokio, tracing, serde, cargo]
---
tonic gRPC services with prost codegen: build.rs, status codes, deadlines, streaming, health and reflection.

## Verify
- `cargo build`: build.rs regenerates code from the `.proto` files.
- `cargo clippy --all-targets -- -D warnings`: lints on generated-adjacent code.
- `cargo test`: services run in process over a duplex or local port.
- `buf lint` (if `buf.yaml` exists): proto style and breaking checks.

## Test first
Serve on an ephemeral port and call with the generated client.
```rust
#[tokio::test]
async fn get_missing_returns_not_found() {
    let addr = spawn_server().await; // binds 127.0.0.1:0
    let mut c = ItemsClient::connect(format!("http://{addr}")).await.unwrap();
    let err = c.get(GetReq { id: 9 }).await.unwrap_err();
    assert_eq!(err.code(), tonic::Code::NotFound);
}
```

## Do
- Generate in `build.rs`: `tonic_build::compile_protos("proto/svc.proto")?` (prost-build config for options); include with `tonic::include_proto!("pkg")`.
- Return `Result<Response<T>, Status>`; map domain errors to precise codes (`InvalidArgument`, `NotFound`, `FailedPrecondition`, `Unavailable`).
- Add `tonic-health` and, if wanted, `tonic-reflection` with the encoded file descriptor set.
- Use interceptors or tower layers for auth, tracing and timeouts; keep metadata keys lowercase.
- Set client deadlines with `Request::set_timeout` and server `Server::builder().timeout(..)`.
- Stream with `tokio_stream::wrappers::ReceiverStream` and a bounded channel for backpressure.
- Set `max_decoding_message_size` deliberately; the default is 4 MiB.
- Evolve protos additively: never reuse or renumber fields; reserve removed ones.

## Avoid
- `Status::internal(e.to_string())` for everything: leaks internals and hides the code. Map errors and log the detail.
- Unbounded `mpsc::unbounded_channel` for streams: memory grows with a slow client. Bound it.
- No deadlines: a hung call holds resources forever. Set timeouts on both ends.
- Committing generated code that drifts from the proto: build in `build.rs` or check regeneration in CI.
- Forgetting `protoc`: build fails on CI. Install it or use a vendored option.
- Plaintext channels in production: configure `ServerTlsConfig`/`ClientTlsConfig`.
- Blocking work inside handlers: use `spawn_blocking`.

## Review
- [ ] Every handler maps errors to specific status codes without leaking internals.
- [ ] Deadlines, message-size limits and TLS are configured.
- [ ] Proto changes are backward compatible (no renumbering, reserved removed fields).
- [ ] Streaming uses bounded channels and handles client cancel.
- [ ] Health service is registered and tests cover a failure code.
