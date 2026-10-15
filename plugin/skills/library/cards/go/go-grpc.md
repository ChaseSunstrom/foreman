---
name: go-grpc
title: gRPC in Go
area: go
tags: [go, grpc, protobuf, interceptors, streaming, buf]
detect: [dep:google.golang.org/grpc, dep:google.golang.org/protobuf, file:buf.yaml, file:buf.gen.yaml]
related: [go-context, go-errors, go-slog, go-http-server]
---
Go gRPC services: generated stubs, status codes, deadlines, interceptors, streaming and bufconn tests.

## Verify
- `buf lint && buf breaking --against '.git#branch=main'`: proto style and wire compatibility (with buf configured).
- `buf generate`: stubs regenerate with no diff.
- `go build ./... && go vet ./...`: compiles against generated code.
- `go test -race ./...`: servers run in process over bufconn.

## Test first
In-memory server through `google.golang.org/grpc/test/bufconn`.
```go
func TestGetMissing(t *testing.T) {
	c := newTestClient(t) // starts server on bufconn, dials with insecure creds
	_, err := c.Get(context.Background(), &pb.GetReq{Id: "nope"})
	if status.Code(err) != codes.NotFound {
		t.Fatalf("code = %v", status.Code(err))
	}
}
```

## Do
- Return `status.Error(codes.X, "msg")` or `status.Errorf`; map domain errors to precise codes (`InvalidArgument`, `NotFound`, `FailedPrecondition`, `Unavailable`).
- Embed `pb.UnimplementedFooServer` (or the `Must` variant deliberately) in server structs.
- Always set a deadline on client calls: `ctx, cancel := context.WithTimeout(ctx, d)`.
- Connect with `grpc.NewClient(target, grpc.WithTransportCredentials(...))` on current grpc-go; `grpc.Dial` is the older entry point.
- Add cross-cutting behavior with `grpc.ChainUnaryInterceptor` and `ChainStreamInterceptor`: logging, auth, recovery, metrics.
- Register `grpc_health_v1` and optionally reflection; call `GracefulStop()` on shutdown with a timeout fallback to `Stop()`.
- In streams, honor `stream.Context().Done()` and return on `io.EOF` from `Recv`.
- Evolve protos additively; reserve removed field numbers.

## Avoid
- `grpc.WithInsecure()` outside tests: deprecated and unencrypted. Use TLS credentials, `insecure.NewCredentials()` only locally.
- No deadlines: calls hang forever. Set per-call timeouts.
- Returning plain `errors.New`: clients see `Unknown`. Return a `status` error.
- Reusing or renumbering proto fields: silent data corruption. Add new numbers, `reserved` old ones.
- Creating a connection per request: expensive. Share one `*grpc.ClientConn`.
- Sending huge messages: default limit is 4 MiB; stream or chunk instead of raising it blindly.
- Sharing a stream across goroutines for `Send`: not safe. Serialize sends.

## Review
- [ ] Every client call has a deadline and every handler maps errors to status codes.
- [ ] TLS configured for non-local use.
- [ ] Interceptors cover recovery, logging and auth.
- [ ] `buf breaking` (or equivalent) passes on proto changes.
- [ ] Graceful shutdown and health service exist.
