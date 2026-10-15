---
name: lua
title: Lua
area: lang
tags: [lua, luarocks, busted, luacheck, stylua, scripting]
detect: [ext:.lua, file:*.rockspec, file:.luacheckrc, file:stylua.toml, file:.busted]
related: [bash]
---
Lua code (5.1 to 5.4, LuaJIT, embedded hosts): luacheck, StyLua, busted, LuaRocks.

## Verify
- `luacheck .`: finds globals leaks, unused variables and shadowing (config in `.luacheckrc`).
- `stylua --check .`: formatting matches `stylua.toml`.
- `busted`: runs `spec/*_spec.lua` (config in `.busted`).
- `luac -p file.lua`: syntax check only, with no run (name varies for LuaJIT: `luajit -bl file.lua > /dev/null`).

## Test first
Specs live in `spec/` and end `_spec.lua`.
```lua
local parse = require("mylib.parse")

describe("parse.int", function()
  it("returns nil and a message for blank input", function()
    local n, err = parse.int("")
    assert.is_nil(n)
    assert.equals("empty", err)
  end)
end)
```
Run `busted`; add `-p _spec` or `--lpath` only if modules do not resolve.

## Do
- Declare every variable `local`; return a module table from each file and `require` it.
- Signal expected failure as `nil, err` returns; use `error()` for programmer mistakes and `pcall`/`xpcall` with a traceback handler at boundaries.
- Set the target in `.luacheckrc` (`std = "lua51"`, `"luajit"`, `"lua54"`, or a `max` std) and list host globals under `read_globals`.
- Cache hot globals in locals (`local insert = table.insert`) in tight loops.
- Use `ipairs` for arrays and `pairs` for maps; track length yourself if holes are possible.
- Write a rockspec with `dependencies` and a `build.modules` table for libraries.

## Avoid
- Accidental globals from a missing `local`: they leak across modules and break under strict mode. Fix with `local`, and let luacheck fail CI.
- `#t` on tables with holes or `nil` entries: undefined border. Store an explicit `n` or use `table.pack`/`select("#", ...)`.
- 1-based vs 0-based slips: `string.sub`, `table.insert(t, pos, v)` and loops start at 1.
- `==` on floats and integers across 5.3+: `1 == 1.0` is true but they print differently. Use `math.type` when it matters.
- `..` string concat inside loops: quadratic. Collect parts in a table and `table.concat`.
- `load`/`loadstring`/`dofile` on untrusted input without a sandbox environment.
- Using `unpack` on 5.2+: it moved to `table.unpack` (guard with `table.unpack or unpack` for 5.1 compat).

## Review
- [ ] `luacheck` reports 0 warnings, and no new `-- luacheck: ignore` without a reason.
- [ ] Target Lua version is stated, and no API from a newer or older one is used unguarded.
- [ ] Every module returns a table and creates no globals.
- [ ] Errors carry context, and `pcall` results are checked.
- [ ] Specs cover the nil/error branch.
