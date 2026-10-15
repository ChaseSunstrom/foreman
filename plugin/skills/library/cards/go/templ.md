---
name: templ
title: templ (Go HTML components)
area: go
tags: [go, templ, html, components, htmx, ssr]
detect: [dep:github.com/a-h/templ, ext:.templ]
related: [go-http-server, chi, echo, go-testing]
---
templ typed HTML components: .templ files generate Go, with contextual escaping, composition and htmx-friendly fragments.

## Verify
- `templ generate`: `_templ.go` files regenerate from `.templ` sources.
- `templ fmt .`: formatting of templates.
- `git diff --exit-code -- '*_templ.go'`: committed generated code is current (after `templ generate`).
- `go build ./... && go vet ./...`: generated code compiles.
- `go test ./...`: component render tests pass.

## Test first
Render to a buffer and assert on the output.
```go
func TestGreetingEscapes(t *testing.T) {
	var buf bytes.Buffer
	err := Greeting(`<script>x</script>`).Render(context.Background(), &buf)
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(buf.String(), "<script>") {
		t.Fatalf("not escaped: %s", buf.String())
	}
}
```

## Do
- Write components as `templ Name(args) { ... }`; call them `@Name(args)` and pass children with `{ children... }`.
- Serve with `templ.Handler(Page())` or call `Page().Render(r.Context(), w)` in a handler, setting `Content-Type: text/html; charset=utf-8` first.
- Return partial components from endpoints for htmx swaps; keep full-page layout in one `Layout` component.
- Use `templ.KV("class", cond)` and `templ.Attributes{...}` for conditional attributes.
- Pass data as typed structs; move logic into plain Go funcs called from templates.
- Run `templ generate --watch` in dev; commit or generate generated files in CI consistently, not both ways.
- Pin the `templ` CLI to the same version as the `github.com/a-h/templ` module in go.mod.

## Avoid
- `templ.Raw(userInput)` or unescaped URLs: XSS. Only `Raw` for trusted static HTML; use `templ.SafeURL` after validating the scheme.
- Building HTML with `fmt.Sprintf` in Go helpers and injecting: bypasses escaping. Write a component.
- CLI and library version mismatch: generation errors or runtime panics. Align versions.
- Editing `_templ.go` files: overwritten. Edit `.templ`.
- Ignoring the `Render` error: a failed write after partial output. Log it, and handle before writing headers where possible.
- Putting heavy queries in components: render does I/O unpredictably. Load data in the handler.
- Inline `<script>` with interpolated data: use `templ.JSONScript` or data attributes.

## Review
- [ ] `templ generate` leaves no diff.
- [ ] No `Raw` or unchecked `SafeURL` on user input.
- [ ] Handlers set content type and handle `Render` errors.
- [ ] CLI and module versions match.
- [ ] Components take typed args and contain no data fetching.
