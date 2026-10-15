---
name: erlang
title: Erlang
area: lang
tags: [erlang, otp, rebar3, eunit, dialyzer, gen-server]
detect: [ext:.erl, ext:.hrl, file:rebar.config, file:rebar.lock, file:*.app.src]
related: [elixir]
---
Erlang/OTP baseline: rebar3 builds, EUnit and Common Test, supervised OTP behaviours, Dialyzer specs, let-it-crash.

## Verify
- `rebar3 compile`: compiles, honoring `erl_opts` such as `warnings_as_errors`.
- `rebar3 eunit`: EUnit tests.
- `rebar3 ct`: Common Test suites under `test/*_SUITE.erl`.
- `rebar3 dialyzer`: success typing and spec mismatches.
- `rebar3 xref`: calls to undefined or unused functions.

## Test first
EUnit: functions ending `_test()` in the module, or a `test/` module. Fail on the bad input.
```erlang
-module(port_parser_tests).
-include_lib("eunit/include/eunit.hrl").

rejects_empty_test() ->
    ?assertEqual({error, invalid}, port_parser:parse(<<>>)).
```

## Do
- Add `{erl_opts, [debug_info, warnings_as_errors]}` in rebar.config; list deps with exact versions and commit `rebar.lock`.
- Return `{ok, V}` or `{error, Reason}`; match on them in function heads and `case`.
- Build processes with OTP behaviours (`gen_server`, `gen_statem`, `supervisor`) and set restart intensity and strategy deliberately.
- Add `-spec` to exported functions and run Dialyzer in CI.
- Use binaries (`<<"text">>`) for text and `iolist`s for output building, not lists of integers by default.
- Name processes with `{local, Name}` or a registry rather than passing raw pids through config.
- Use `logger` macros (`?LOG_INFO`), not `io:format`, for runtime logging.

## Avoid
- `catch Expr`: conflates exits, throws and errors, and returns ambiguous values. Use `try ... catch Class:Reason:Stack`.
- `list_to_atom` on external data: the atom table is finite and never collected. Use `list_to_existing_atom` or keep binaries.
- Blocking work in `handle_call`: serializes callers and times out at 5000 ms by default. Reply later with `{noreply, ...}` and `gen_server:reply/2`, or offload.
- Unlinked `spawn` for work that matters: failures vanish. Use `spawn_link`, `proc_lib` or a supervisor.
- Unbounded mailboxes via `cast` floods: memory growth. Apply backpressure or use calls.
- `length(L) == 0` or `++` in loops: O(n) per check. Match `[]` and prepend.
- Selective receive in busy loops over huge mailboxes: quadratic scan. Handle messages in order.
- Defensive programming that swallows errors: let the supervisor restart.

## Review
- [ ] Every long-lived process is under a supervisor with a justified strategy.
- [ ] No dynamic atom creation from untrusted input.
- [ ] Exported functions have specs and Dialyzer is clean.
- [ ] `handle_call` and `init` return quickly; timeouts are explicit where needed.
- [ ] rebar.lock committed; compile has no warnings.
