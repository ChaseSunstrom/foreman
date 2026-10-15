---
name: chi
title: chi
area: go
tags: [go, web, router, chi, http, middleware]
detect: [dep:github.com/go-chi/chi/v5, dep:github.com/go-chi/chi]
related: [go-testing, go-modules, go-concurrency, sqlc, gorm]
---
chi router: a thin layer over net/http with composable middleware, sub-routers and URL params.

## Verify
- `go vet ./... && go build ./...`: static checks and build.
- `go test ./... -race -count=1`: handler tests with the race detector.
- `go list -m github.com/go-chi/chi/v5`: the module is on the v5 path.
- `go test -run TestRoutes ./...`: a route-table test (see below) still passes.

## Test first
chi routers are `http.Handler`s, so use plain httptest. Build the router in a function.
```go
func TestGetItemBadID(t *testing.T) {
	r := NewRouter(fakeStore{})
	req := httptest.NewRequest(http.MethodGet, "/items/abc", nil)
	rec := httptest.NewRecorder()
	r.ServeHTTP(rec, req)
	if rec.Code != http.StatusBadRequest {
		t.Fatalf("got %d", rec.Code)
	}
}
```
To unit-test a handler alone, add the URL param to the request's `chi.RouteContext` before calling it.

## Do
- Import `github.com/go-chi/chi/v5` and `chi/v5/middleware`.
- Order middleware deliberately: `middleware.RequestID`, `RealIP` (only behind a trusted proxy), logger, `Recoverer`, `Timeout`.
- Compose with `r.Route("/items", func(r chi.Router){...})`, `r.Group(...)` and `r.With(mw)`.
- Read params with `chi.URLParam(r, "id")` and parse them once in a middleware or helper.
- Pass values via `context.WithValue` using an unexported key type, and read through typed accessors.
- Use `r.Mount` for sub-routers, and `r.NotFound` and `r.MethodNotAllowed` for consistent errors.
- Serve with an `http.Server` with timeouts and `Shutdown`.
- Use `chi.Walk` in a test to assert the route table.

## Avoid
- `chi.URLParam` outside a routed request (for example in a bare handler test): it returns "". Route through the router or set the route context.
- `middleware.RealIP` on a public listener: clients can spoof their address. Use it only behind a trusted proxy.
- Mounting at a path and registering the same prefix as a route: it panics or shadows. Use one.
- Registering middleware after routes with `r.Use`: chi panics. `Use` first, or use `With`.
- Using string keys in `context.WithValue`: collisions. Use a private type.
- `middleware.Timeout` assuming it kills handlers: it only cancels the context. Handlers must check `ctx.Done()`.
- Old `github.com/go-chi/chi` (v4 and earlier path) in new code.

## Review
- [ ] Middleware order is intentional and `Use` calls precede routes.
- [ ] URL params are parsed and validated with 400 on failure.
- [ ] Handlers honour context cancellation.
- [ ] Context keys use private types.
- [ ] Server timeouts and shutdown are set.
