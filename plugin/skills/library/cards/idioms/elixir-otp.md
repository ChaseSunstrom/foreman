---
name: elixir-otp
title: Elixir and OTP
area: idioms
tags: [elixir, otp, genserver, supervisor, processes, fault-tolerance]
detect: [file:mix.exs]
related: [elixir, exunit, phoenix]
---
OTP in Elixir: processes only for state and concurrency, supervised, with a pure functional core behind them.

## Verify
- `mix compile --warnings-as-errors`: compiles clean.
- `mix test`: runs the ExUnit suite.
- `mix format --check-formatted`: formatting is clean.
- `mix credo --strict`: style and design checks, when Credo is a dependency.

## Test first
Test the pure logic directly and the GenServer through its public API.
```elixir
defmodule CounterTest do
  use ExUnit.Case, async: true

  test "increments and reports" do
    pid = start_supervised!(Counter)
    assert Counter.incr(pid) == 1
    assert Counter.incr(pid) == 2
  end
end
```
Use `start_supervised!` so the test process owns cleanup.

## Do
- Put logic in plain modules and functions, and wrap them in a GenServer only for state, serialization or timing.
- Give each GenServer a client API of public functions that call `GenServer.call` or `cast`, with `handle_*` callbacks kept thin.
- Start long-lived processes under a `Supervisor` with a clear restart strategy and child specs.
- Use `Task.Supervisor.async_nolink` for work that may crash, and `Task.async_stream` with `max_concurrency` for bounded fan-out.
- Use `Registry` for named process lookup instead of atoms made at runtime.
- Let it crash: pattern match the expected shape and let supervisors recover, handling only errors you can act on.
- Use `handle_continue` for post-init work so `init` returns quickly.
- Use `:telemetry` events for metrics, and `Logger` metadata for tracing.

## Avoid
- A process per object by habit: processes are for concurrency or isolation, not code organization. Use modules and structs.
- Slow work inside `handle_call`: it blocks the whole server and times out callers. Reply, then work in a Task, or use `handle_continue`.
- `GenServer.call` with the default 5 second timeout around slow calls and no thought for the caller crash: set a timeout deliberately.
- `String.to_atom` on external input: atoms are never garbage collected. Use `String.to_existing_atom` or keep strings.
- Unsupervised `spawn` or `Task.start`: crashes vanish. Use supervised tasks.
- Rescuing everything with `try/rescue`: it defeats supervision. Return `{:ok, _}` and `{:error, _}` for expected failures.
- Calling a GenServer from within its own callback: deadlock. Pass the work through a message.

## Review
- [ ] Every long-lived process sits under a supervisor with a deliberate strategy.
- [ ] Callbacks are thin and do not block on slow work.
- [ ] No runtime atom creation from external data.
- [ ] Expected errors use tagged tuples, and unexpected ones crash.
- [ ] Tests use `start_supervised!` and avoid `Process.sleep`.
