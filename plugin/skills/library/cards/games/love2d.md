---
name: love2d
title: LOVE (Love2D)
area: games
tags: [love2d, lua, game, callbacks, canvas, quads]
detect: [file:conf.lua]
related: [game-loop, game-physics, pathfinding]
---
LOVE games in Lua: `love.load`, `love.update(dt)` and `love.draw` callbacks, `conf.lua` for window setup, logic kept testable apart from the love module.

## Verify
- `luacheck . --globals love`: no undefined globals or unused variables, with `love` allowed.
- `busted`: unit tests for logic modules pass under plain Lua (only when busted is installed).
- `love . --console`: the game starts with a console on Windows. On other platforms `love .` is enough, and stderr shows errors.
- `stylua --check .`: formatting (only when StyLua is installed).

## Test first
Write logic modules that never call `love.*`, and test them with busted.
```lua
-- spec/mover_spec.lua
local Mover = require("src.mover")

describe("Mover", function()
  it("advances by speed times dt", function()
    local m = Mover.new(0, 100)
    m:update(0.5)
    assert.are.equal(50, m.x)
  end)
  it("clamps at the right edge", function()
    local m = Mover.new(790, 100, 800)
    m:update(1)
    assert.are.equal(800, m.x)
  end)
end)
```

## Do
- Use `love.update(dt)` with `dt` for all motion. For physics-critical code, accumulate and step a fixed `1/60`.
- Set window and modules in `conf.lua` (`love.conf(t)`), and disable modules you do not use (`t.modules.joystick = false`).
- Load images, fonts and sounds once in `love.load`. Use `love.graphics.newQuad` on sprite sheets and `love.graphics.newSpriteBatch` for many sprites.
- Set `love.graphics.setDefaultFilter("nearest", "nearest")` for pixel art before loading images.
- Use `love.audio.newSource(path, "static")` for short effects and `"stream"` for music.
- Keep state in modules or tables, use `local` everywhere, and `require` by dotted path.
- Use `love.filesystem` for saves (write directory only) and serialise with a small table-to-string function or JSON library.

## Avoid
- Global variables by accident: they leak across files and hide typos. Use `local` and luacheck.
- Creating images, fonts or tables inside `love.draw`: GC pressure and slowdowns. Create once in `love.load`.
- Motion without `dt`: speed depends on frame rate. Multiply by dt.
- Writing outside the save directory with `io.open`: sandbox and portability issues. Use `love.filesystem.write`.
- Resetting colour state: `love.graphics.setColor` persists, so call `setColor(1, 1, 1, 1)` before drawing images. Colours are 0 to 1 in LOVE 11 and later.
- Large `love.keypressed` chains: unmaintainable. Dispatch to the current state.

## Review
- [ ] luacheck is clean and no accidental globals remain.
- [ ] Logic modules have busted specs and do not touch `love.*`.
- [ ] All motion and timers use `dt`.
- [ ] Assets load once in `love.load`.
- [ ] Saves use `love.filesystem`.
