---
name: crystal
title: Crystal
area: lang
tags: [crystal, shards, spec, ameba, fibers, nil-safety]
detect: [ext:.cr, file:shard.yml, file:shard.lock, file:.ameba.yml]
related: [bash]
---
Crystal projects: Shards dependencies, compile-time type and nil checking, built-in `spec`, Ameba linting.

## Verify
- `shards install`: dependencies resolve and `shard.lock` is current.
- `crystal tool format --check`: formatting is canonical (`crystal tool format` writes).
- `crystal spec`: runs every `spec/**/*_spec.cr`.
- `crystal build --no-codegen src/app.cr`: type-checks the whole program fast, with no binary.
- `bin/ameba`: lint, when `ameba` is a development dependency (build it with `shards build ameba`).

## Test first
Specs live in `spec/`, with `require "./spec_helper"` at the top.
```crystal
require "./spec_helper"

describe Parser do
  it "rejects blank input" do
    expect_raises(ArgumentError, /empty/) do
      Parser.parse_int("")
    end
  end

  it "returns nil for junk in the lenient variant" do
    Parser.parse_int?("x").should be_nil
  end
end
```
`spec_helper.cr` holds `require "spec"` and `require "../src/<project>"`.

## Do
- Declare dependencies in `shard.yml` and commit `shard.lock` for applications; set `crystal:` to the minimum compiler version.
- Annotate public method arguments and return types so errors point at the call site and compile times stay low.
- Handle nilable values with `if x = foo`, `.try`, `||` defaults or `not_nil!` only after an explicit check; keep `?` method variants (`parse_int?`) returning nil, and the bang or plain variant raising.
- Define custom exception classes under your module and `raise` them with context.
- Use `Channel`, `spawn` and `WaitGroup`/`Mutex` for concurrency; Crystal fibers are cooperative on one thread by default.
- Build release binaries with `crystal build --release --no-debug src/app.cr`, and develop without `--release`.
- Use `ensure` for cleanup, or block forms (`File.open(path) { |f| ... }`) that close resources.

## Avoid
- `not_nil!` on external input: raises `NilAssertionError` at runtime. Check the value and handle the nil case.
- Capturing a loop variable in `spawn` blocks: all fibers see its final value. Copy it into a local first (`i = i; spawn { ... }`) or pass it through a channel.
- Blocking C calls or tight CPU loops with no yield: starve other fibers. Offload or add `Fiber.yield`.
- Unions grown by reassigning a variable to different types (`x = 1; x = "a"`): `Int32 | String` spreads through the code. Use separate names.
- Metaprogramming macros for what a method does: error messages degrade. Use macros only for real compile-time need.
- Relying on `String#[]` byte versus char indexing: strings are UTF-8, and indexing is O(n) for non-ASCII. Use `each_char` or `byte_slice` deliberately.
- Passing `--release` for tests: slow build and hides compile-time diagnostics you want while iterating.

## Review
- [ ] `crystal tool format --check` and `crystal spec` pass, and Ameba shows no new offenses.
- [ ] No unchecked `not_nil!` and no unexplained `as(Type)` casts.
- [ ] Public methods have type restrictions and doc comments.
- [ ] Fibers are joined or tracked, and shared mutable state is guarded.
- [ ] `shard.yml` and `shard.lock` agree with the code's `require`s.
