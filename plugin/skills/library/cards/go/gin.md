---
name: gin
title: Gin
area: go
tags: [go, web, api, gin, http, middleware]
detect: [dep:github.com/gin-gonic/gin]
related: [go-testing, go-modules, go-concurrency, gorm, sqlc]
---
Gin HTTP services: routers, binding and validation, middleware, tested with httptest.

## Verify
- `go vet ./... && go build ./...`: static checks and build.
- `go test ./... -race -count=1`: handler tests through the engine.
- `GIN_MODE=release go test ./...`: tests pass without debug logging noise or debug-only behaviour.
- `go list -m github.com/gin-gonic/gin`: the pinned Gin version.

## Test first
Call the engine's `ServeHTTP` with a recorder. Build the router in a function.
```go
func TestCreateRejectsBlankName(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := NewRouter(fakeStore{})
	w := httptest.NewRecorder()
	req := httptest.NewRequest("POST", "/items", strings.NewReader(`{"name":""}`))
	req.Header.Set("Content-Type", "application/json")
	r.ServeHTTP(w, req)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("got %d", w.Code)
	}
}
```

## Do
- Use `gin.New()` and add `gin.Recovery()` plus your logger explicitly, rather than `gin.Default()`, when you control logging.
- Bind with `ShouldBindJSON`, `ShouldBindQuery` and `ShouldBindUri` and struct tags (`binding:"required,email"`), then return 400 on error.
- Group routes with `r.Group("/v1", authMiddleware)`.
- Handle errors in one middleware: `c.Error(err)` in handlers, then a middleware that maps `c.Errors` to responses.
- Pass `c.Request.Context()` to DB and HTTP calls so client cancellation propagates.
- Run the server via `http.Server{Handler: r, ReadHeaderTimeout: ...}` with `Shutdown(ctx)` on signal.
- Set `r.SetTrustedProxies(...)` to the real proxies, or nil.
- Call `c.Abort()` (or `AbortWithStatusJSON`) in middleware that stops the chain.

## Avoid
- `c.Bind*` (the `Must` variants): they write a 400 and abort on failure, hiding your error format. Use `ShouldBind*`.
- Using `*gin.Context` in a goroutine after the handler returns: it is reused. Pass `c.Copy()` or the needed values.
- Forgetting `return` after `c.JSON(...)` on an error branch: the handler continues and writes twice.
- `router.Run()` with no timeouts for production: slow-client exposure. Build an `http.Server`.
- Trusting `c.ClientIP()` with default trusted proxies: spoofable via `X-Forwarded-For`. Configure trusted proxies.
- `binding:"required"` on a bool or int where zero is valid: it rejects `false` and `0`. Use a pointer field.
- Debug mode in production: set `GIN_MODE=release`.

## Review
- [ ] Every handler returns after writing an error response.
- [ ] Input is bound and validated with `ShouldBind*`, with zero values handled via pointers.
- [ ] Auth and error mapping live in middleware.
- [ ] No `*gin.Context` escapes into goroutines.
- [ ] Server timeouts, trusted proxies and graceful shutdown are configured.
