---
name: go-generics
title: Go generics
area: go
tags: [go, generics, type-parameters, constraints, slices, maps]
detect: []
related: [go-testing, go-errors, go-modules]
---
Go type parameters: use them to remove duplicated algorithms and containers, with tight constraints and stdlib helpers first.

## Verify
- `go build ./...`: instantiation and constraint errors surface at compile time.
- `go vet ./...`: catches misuse that compiles.
- `go test -race ./...`: generic containers shared across goroutines are safe.
- `go test -run XXX -bench . -benchmem ./...`: generic code isn't slower or allocating more than the concrete version.

## Test first
Table-test each instantiation you rely on, including a zero-size and a non-comparable-looking case.
```go
func TestMap(t *testing.T) {
	got := Map([]int{1, 2, 3}, strconv.Itoa)
	want := []string{"1", "2", "3"}
	if !slices.Equal(got, want) {
		t.Fatalf("got %v want %v", got, want)
	}
	if len(Map[int, string](nil, strconv.Itoa)) != 0 {
		t.Fatal("nil input should yield empty")
	}
}
```

## Do
- Reach for `slices`, `maps` and `cmp` (stdlib) before writing your own `Contains`, `Sort`, `Keys`, `Max`.
- Use the narrowest constraint: `comparable` for `==` and map keys, `cmp.Ordered` for `<`, a small method interface when you call methods.
- Define union constraints with `~`: `type Number interface{ ~int | ~int64 | ~float64 }` so named types qualify.
- Let inference work: `Map(xs, f)`; pass explicit type args only when it can't infer (`Zero[T]()` style).
- Write the concrete version first; generalize when a second real caller appears.
- Return the zero value with `var zero T; return zero, err`.
- Keep type parameter lists short and names meaningful beyond `T` when there are several (`K`, `V`, `E`).

## Avoid
- Generics where an interface already fits: methods on an interface are simpler and don't instantiate per type.
- `any` constraint plus a type switch inside: it is an interface in disguise. Use an interface or concrete overloads.
- `[T int | string]` without `~`: rejects `type ID string`. Add `~`.
- Generic methods: methods can't have their own type parameters. Use a generic function taking the receiver.
- Comparing `T` with `==` under `any`: compile error. Constrain with `comparable`.
- Ignoring that pointer-receiver methods need a second param (`PT interface{ *T; M() }`): leads to nil-pointer or compile errors; test with real types.
- Exporting heavily generic APIs early: hard to evolve. Keep them internal until stable.

## Review
- [ ] Constraints are as narrow as needed and use `~` for underlying types.
- [ ] Stdlib `slices`/`maps`/`cmp` weren't reimplemented.
- [ ] A concrete duplicate was actually removed, not a speculative abstraction added.
- [ ] Tests instantiate at least two distinct types, including a named type.
- [ ] Zero values and nil inputs are handled.
