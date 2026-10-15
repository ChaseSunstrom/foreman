---
name: elixir
title: Elixir
area: lang
tags: [elixir, mix, exunit, otp, genserver, credo]
detect: [ext:.ex, ext:.exs, file:mix.exs, file:mix.lock]
related: [erlang, phoenix, ecto]
---
Elixir baseline: mix tasks as the gate (compile with warnings as errors, format, ExUnit), pattern matching, supervised OTP processes.

## Verify
- `mix compile --warnings-as-errors`: compiles clean.
- `mix format --check-formatted`: formatting.
- `mix test`: the suite (`mix test path/to/file_test.exs:12` for one test).
- `mix credo --strict`: style checks, when Credo is a dependency.
- `mix deps.unlock --check-unused`: no stale entries in mix.lock.

## Test first
ExUnit, tests in `test/`, files `*_test.exs`, `async: true` when the test has no shared state.
```elixir
defmodule PortParserTest do
  use ExUnit.Case, async: true

  test "rejects empty input" do
    assert {:error, :invalid} = PortParser.parse("")
  end
end
```

## Do
- Return tagged tuples (`{:ok, v}` and `{:error, reason}`) and chain with `with`.
- Pattern match in function heads and use guards; keep functions small and multi-clause.
- Put state in supervised processes (`GenServer`, `Agent`, `Task.Supervisor`) and give every child a supervisor.
- Keep pure logic in plain modules; make the GenServer a thin wrapper.
- Use `@spec` on public functions and run Dialyzer (via dialyxir) when configured.
- Use `Logger` with metadata, and `@impl true` on callbacks.
- Use `Stream` for large or lazy data and `Enum` otherwise; use `Task.async_stream` with `max_concurrency` for bounded parallelism.

## Avoid
- Spawning with `spawn` or unsupervised `Task.start`: silent crashes and leaks. Use supervisors.
- Raising for expected failures: callers cannot pattern match. Return `{:error, _}`, and use bang functions (`fetch!`) only when failure is a bug.
- `String.to_atom` on user input: atoms are never collected and exhaust the VM. Use `String.to_existing_atom` or keep strings.
- Doing slow or blocking work inside a GenServer callback: serializes every caller and times out. Offload to a Task.
- Using the process dictionary or a GenServer as a global variable for state that belongs in the database or ETS.
- `Enum` chains over huge lists: multiple full passes. Use `Stream` or a single `Enum.reduce`.
- Deprecated `Enum.at` loops for indexing: O(n) per call. Use maps or pattern matching.
- Rescuing everything (`rescue _ ->`): hides crashes the supervisor should see. Let it crash.

## Review
- [ ] Processes are started under a supervisor with a sensible restart strategy.
- [ ] No `String.to_atom` or unbounded atom creation from external input.
- [ ] GenServer callbacks are fast; call timeouts are considered.
- [ ] Expected failures use tagged tuples with specs on public functions.
- [ ] Compile has no warnings; format and tests pass.
