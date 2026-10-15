---
name: go-slog
title: Go log/slog
area: go
tags: [go, logging, slog, structured, observability]
detect: []
related: [go-http-server, go-context, go-errors, go-pprof]
---
Structured logging with the stdlib log/slog: one configured logger, typed attributes, context-aware handlers and test capture.

## Verify
- `go vet ./...`: the `slog` analyzer flags mismatched key/value pairs.
- `go test ./...`: tests assert on captured log output where logs matter.
- `grep -rn "log.Printf\|log.Println\|fmt.Println" --include=*.go .`: no legacy logging left in service code.
- `go run . 2>&1 | head`: JSON or text output has the expected keys.

## Test first
Capture with a handler writing to a buffer.
```go
func TestLogsUserID(t *testing.T) {
	var buf bytes.Buffer
	l := slog.New(slog.NewJSONHandler(&buf, nil))
	handle(l, User{ID: 7})
	var m map[string]any
	_ = json.Unmarshal(buf.Bytes(), &m)
	if m["user_id"] != float64(7) {
		t.Fatalf("log = %s", buf.String())
	}
}
```

## Do
- Build the logger once in `main`: `slog.New(slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{Level: lvl}))` and `slog.SetDefault(l)`.
- Use a `slog.LevelVar` so the level can change at runtime.
- Log pairs or typed attrs: `l.Info("created", "user_id", id)` or `slog.Int("user_id", id)`; typed attrs avoid mismatches.
- Use the `Context` variants (`InfoContext(ctx, ...)`) so a custom handler can add trace or request IDs from ctx.
- Derive request loggers with `l.With("req_id", id)` and `WithGroup` for namespaces.
- Redact secrets via `ReplaceAttr` in `HandlerOptions` or implement `LogValuer` on sensitive types.
- Pass `*slog.Logger` as a dependency; don't hide it in globals for library code.
- Log an error once at the boundary with `"err", err`.

## Avoid
- Odd-length key/value lists (`l.Info("x", "k")`): output `!BADKEY`. Run `go vet`, prefer typed attrs.
- Formatting into the message (`Sprintf`): defeats structure. Put variables in attrs.
- Logging at hot loops with `Debug` building expensive attrs: guard with `l.Enabled(ctx, slog.LevelDebug)`.
- Logging secrets, tokens or full request bodies: redact.
- Creating a new handler per call: allocation churn and interleaved output. Reuse one.
- Logging and returning the same error at every layer: duplicates. Log at the edge.
- Using the `log` package output plus slog with different formats: parsers choke. Route `log` through `slog.NewLogLogger` if legacy code remains.

## Review
- [ ] One logger configured in `main`, level adjustable.
- [ ] Attributes are keyed consistently (snake_case) and `go vet` is clean.
- [ ] Context-aware calls used in request paths.
- [ ] Sensitive values are redacted.
- [ ] No leftover `fmt.Println` or `log.Printf` in service code.
