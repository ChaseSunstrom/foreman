---
name: go-interfaces
title: Go interfaces
area: idioms
tags: [go, interfaces, design, testing, errors, composition]
detect: []
related: [go, golangci-lint]
---
Go interfaces: small, defined by the consumer, accepted as parameters and not returned from constructors.

## Verify
- `go vet ./...`: suspicious constructs, including bad interface use.
- `go build ./...`: every type still satisfies the interfaces it is used as.
- `go test -race ./...`: tests pass with the race detector on.
- `golangci-lint run`: when the repo configures it.

## Test first
Define the narrow interface where it is consumed, and fake it in the test.
```go
type store interface{ Get(id string) (string, error) }

type fake map[string]string

func (f fake) Get(id string) (string, error) {
	v, ok := f[id]
	if !ok { return "", errNotFound }
	return v, nil
}

func TestGreetUnknownUser(t *testing.T) {
	_, err := Greet(fake{}, "u1")
	if !errors.Is(err, errNotFound) { t.Fatalf("got %v", err) }
}
```

## Do
- Keep interfaces to one to three methods and name them for behavior (`Reader`, `Store`).
- Declare the interface in the package that uses it, not next to the implementation.
- Accept interfaces and return concrete types.
- Compose with embedding (`io.ReadWriter`) instead of widening one interface.
- Add a compile-time check where a type must implement an interface: `var _ Store = (*pg)(nil)`.
- Reuse standard interfaces first: `io.Reader`, `io.Writer`, `fmt.Stringer`, `error`, `sort.Interface`.
- Use `errors.Is` and `errors.As` with sentinel and typed errors, and wrap with `%w`.

## Avoid
- Defining an interface before there are two users or a test need: the result is indirection with no benefit. Start concrete.
- Large "mirror" interfaces copying every method of a struct: they cannot be faked cheaply. Split by caller need.
- Returning an interface from a constructor: it hides the type and blocks access to extra methods. Return `*T`.
- A nil pointer stored in an interface: `iface != nil` is then true. Return an untyped `nil` explicitly.
- `interface{}` or `any` parameters when generics (type parameters) fit: use `func Map[T, U any]`.
- Type assertions without the comma-ok form: `v := x.(T)` panics. Use `v, ok := x.(T)`.

## Review
- [ ] Each interface has few methods and lives with its consumer.
- [ ] Constructors return concrete types.
- [ ] No typed-nil returned through an interface.
- [ ] Fakes in tests are small hand-written types.
- [ ] Errors are wrapped with `%w` and checked with `errors.Is` or `errors.As`.
