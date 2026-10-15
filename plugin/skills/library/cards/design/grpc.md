---
name: grpc
title: gRPC and Protobuf
area: design
tags: [grpc, protobuf, rpc, streaming, deadlines, contracts]
detect: [file:*.proto, file:buf.yaml, file:buf.gen.yaml, dep:grpcio, dep:google.golang.org/grpc, dep:@grpc/grpc-js, dep:tonic]
related: [api-versioning, error-handling, retries-backoff, microservices]
---
gRPC services with evolvable protobuf schemas, explicit deadlines, status codes and tested streaming.

## Verify
- `buf lint`: style and package-layout rules on the `.proto` files.
- `buf breaking --against '.git#branch=main'`: no wire-incompatible change against main.
- `buf generate`: stubs regenerate cleanly from `buf.gen.yaml`.
- `grpcurl -plaintext localhost:50051 list`: the server is up and exposes reflection.

## Test first
Start the service on an in-memory or ephemeral port and call it through a real client stub.
```go
func TestGetOrder_NotFound(t *testing.T) {
	c := newTestClient(t) // bufconn server + client
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	_, err := c.GetOrder(ctx, &pb.GetOrderRequest{Id: "missing"})
	if status.Code(err) != codes.NotFound {
		t.Fatalf("got %v, want NotFound", err)
	}
}
```

## Do
- Never reuse or renumber a field tag. Remove with `reserved 4; reserved "old_name";`.
- Add fields, never change a type. Make new fields optional by meaning, since the zero value is indistinguishable from unset.
- Use `optional` (proto3 presence) or wrapper types when "unset" and the zero value differ.
- Put the version in the package (`acme.orders.v1`), and keep request and response messages unique per RPC (`GetOrderRequest`, not a shared type).
- Set a deadline on every client call, and propagate the incoming context to downstream calls.
- Return the right `codes.*` (`InvalidArgument`, `NotFound`, `FailedPrecondition`, `Unavailable`) and details through `google.rpc.Status`.
- Retry only idempotent calls on `Unavailable`, with backoff, through service config.
- Add health checking (`grpc.health.v1`) and keepalive settings that match the load balancer's idle timeout.

## Avoid
- Calls without a deadline: one hung server holds goroutines and connections forever. Always use a context timeout.
- Returning `Unknown` or `Internal` for client mistakes: callers can't branch on it. Pick the specific code.
- Enums without a `_UNSPECIFIED = 0` value: the default silently becomes a real value.
- Changing a field from `int32` to `string`, or reordering tags: it corrupts data on the wire. Add a new field.
- Reusing one connection per request: create the `ClientConn` once and share it.
- Large messages (over the 4 MB default limit): stream or chunk them instead of raising limits everywhere.

## Review
- [ ] `buf breaking` passes, and removed fields are `reserved`.
- [ ] Enums start with `_UNSPECIFIED = 0`.
- [ ] Every client call carries a deadline, and the server honors context cancellation.
- [ ] Errors use specific status codes, and tests assert them.
- [ ] Streaming handlers stop on `ctx.Done()` and bound their buffering.
