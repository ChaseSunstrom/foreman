---
name: echo
title: Echo
area: go
tags: [go, web, api, echo, http, middleware]
detect: [dep:github.com/labstack/echo/v4, dep:github.com/labstack/echo/v5]
related: [go-testing, go-modules, gorm, sqlc, go-concurrency]
---
Echo HTTP services: handlers returning errors, binding and validation, middleware, httptest-driven tests.

## Verify
- `go vet ./... && go build ./...`: static checks and build.
- `go test ./... -race -count=1`: handler tests.
- `go list -m all | grep labstack`: the Echo major version (v4 and v5 differ), plus middleware module versions.
- `go mod tidy -diff`: dependencies are tidy.

## Test first
Create a context from a recorder and call the handler directly, or use `e.ServeHTTP`.
```go
func TestGetUserNotFound(t *testing.T) {
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/users/9", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.SetPath("/users/:id")
	c.SetParamNames("id")
	c.SetParamValues("9")

	err := h.GetUser(c)
	var he *echo.HTTPError
	if !errors.As(err, &he) || he.Code != http.StatusNotFound {
		t.Fatalf("got %v", err)
	}
}
```
Test the whole router with `e.ServeHTTP(rec, req)` when middleware matters.

## Do
- Return errors from handlers (`return echo.NewHTTPError(http.StatusBadRequest, "msg")`). Customise `e.HTTPErrorHandler` for the JSON error shape.
- Set `e.Validator` to a validator (go-playground/validator) and call `c.Validate(&req)` after `c.Bind(&req)`.
- Use `middleware.Recover()`, `middleware.RequestID()`, `middleware.Logger()` or a structured request logger, and `middleware.CORSWithConfig` with explicit origins.
- Group routes with `e.Group("/api", authMW)`.
- Pass `c.Request().Context()` to downstream calls.
- Run with `http.Server` timeouts and `e.Shutdown(ctx)`, not bare `e.Start` in production.
- Bind path, query and header sources explicitly (`echo.PathParamsBinder`, `QueryParamsBinder`) when types matter.

## Avoid
- Importing `github.com/labstack/echo` without `/v4`: the unmaintained v3 path. Use the versioned module path.
- Calling `c.JSON` then returning `nil` on an error path and carrying on: return right after the response.
- `c.Bind` binding from query, path and body together unexpectedly: for GET it reads query, and field source tags matter. Define separate request structs.
- Skipping validation because `Bind` succeeded: bind only parses. Call `Validate`.
- `middleware.CORS()` defaults (any origin) on authenticated APIs: set `AllowOrigins`.
- Using the `Context` after the handler returns: it is pooled and reused.
- Hard-coding `e.Debug = true` in production: it leaks error details.

## Review
- [ ] Handlers return errors and one error handler shapes the response.
- [ ] Every bound request is validated.
- [ ] CORS origins, timeouts and recover middleware are configured.
- [ ] The Context is not retained past the handler.
- [ ] Tests cover one failure path per route.
