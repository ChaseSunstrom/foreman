---
name: go-http-server
title: Go net/http server
area: go
tags: [go, http, server, timeouts, shutdown, middleware, servemux]
detect: []
related: [chi, gin, go-context, go-slog, go-errors]
---
Production net/http servers: timeouts, graceful shutdown, ServeMux patterns, body limits and httptest.

## Verify
- `go vet ./...`: lints.
- `go test -race ./...`: handlers and middleware under concurrency.
- `go test -run TestShutdown -count=20 ./...`: graceful shutdown isn't flaky.
- `curl -si localhost:8080/healthz`: the live server answers with expected status and headers.

## Test first
Use httptest; no network port.
```go
func TestCreateRejectsBigBody(t *testing.T) {
	h := NewRouter()
	req := httptest.NewRequest("POST", "/items", strings.NewReader(strings.Repeat("x", 2<<20)))
	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, req)
	if rec.Code != http.StatusRequestEntityTooLarge {
		t.Fatalf("code = %d", rec.Code)
	}
}
```

## Do
- Build `&http.Server{Addr, Handler, ReadHeaderTimeout, ReadTimeout, WriteTimeout, IdleTimeout}`; never `http.ListenAndServe` bare in production.
- Shut down: on `signal.NotifyContext(ctx, os.Interrupt, syscall.SIGTERM)`, call `srv.Shutdown(ctxWithTimeout)`; treat `http.ErrServerClosed` as success.
- Route with the stdlib `http.ServeMux` patterns (`"GET /items/{id}"`, `r.PathValue("id")`) on Go 1.22 and later.
- Limit bodies: `r.Body = http.MaxBytesReader(w, r.Body, 1<<20)`; decode JSON with `json.NewDecoder` and `DisallowUnknownFields` when strict.
- Set headers before `WriteHeader`/first write; write the status once.
- Wrap middleware as `func(http.Handler) http.Handler`: recover, request ID, logging, auth.
- Use `r.Context()` for downstream calls so client disconnects cancel work.
- Expose `/healthz` and `/readyz` that check real dependencies for readiness.

## Avoid
- No timeouts: slowloris holds connections forever. Set `ReadHeaderTimeout` at minimum.
- `http.DefaultServeMux` and `DefaultClient`: global state anyone can register on. Make your own mux and client.
- `WriteHeader` after writing the body or twice: "superfluous WriteHeader" log and wrong status. Write once.
- Ignoring `Encode` errors or double-writing after `http.Error`: forgetting `return` after an error response.
- `os.Exit` or `log.Fatal` in handlers or after `ListenAndServe`: skips deferred cleanup. Return errors to `main`.
- Reading unbounded request bodies: memory DoS. Use `MaxBytesReader`.
- Starting goroutines in handlers that outlive the request using `r.Context()`: it is cancelled. Use a detached context.

## Review
- [ ] Server has read-header, read, write and idle timeouts.
- [ ] Graceful shutdown on SIGTERM with a deadline.
- [ ] Bodies are size-limited; every error branch returns after responding.
- [ ] No use of default mux or default client in production code.
- [ ] Tests use `httptest` for success and failure.
