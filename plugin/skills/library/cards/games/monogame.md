---
name: monogame
title: MonoGame
area: games
tags: [monogame, csharp, dotnet, xna, content-pipeline, spritebatch]
detect: [dep:MonoGame.Framework.DesktopGL, dep:MonoGame.Framework.WindowsDX, dep:MonoGame.Content.Builder.Task, file:Content.mgcb]
related: [game-loop, game-physics, pathfinding]
---
MonoGame games in C#: Game subclass with Update and Draw, content built by the MGCB pipeline, SpriteBatch rendering.

## Verify
- `dotnet build -warnaserror`: the game and its content build with no warnings.
- `dotnet test`: logic tests pass (keep them in a separate project with no GraphicsDevice).
- `dotnet format --verify-no-changes`: formatting matches the repo style.
- `dotnet run -- --smoke`: only if the project defines a smoke flag that runs a few frames and exits.

## Test first
Keep game rules in plain classes taking `GameTime` values or `float dt`. Test them without a window.
```csharp
public class MoverTests {
    [Fact] public void Moves_By_Speed_Times_Dt() {
        var m = new Mover(x: 0, speed: 100);
        m.Update(0.5f);
        Assert.Equal(50f, m.X, 3);
    }
    [Fact] public void Clamps_To_Bounds() {
        var m = new Mover(x: 790, speed: 100, maxX: 800);
        m.Update(1f);
        Assert.Equal(800f, m.X);
    }
}
```

## Do
- Add every asset to `Content.mgcb` and load it in `LoadContent` through `Content.Load<T>("name")` without the extension.
- Use `gameTime.ElapsedGameTime.TotalSeconds` for movement, and keep `IsFixedTimeStep` on (default 60 Hz) for deterministic updates.
- Batch drawing: one `SpriteBatch.Begin`/`End` per pass, sprites sorted by texture, and sprite sheets rather than many textures.
- Read input as a state snapshot each Update (`Keyboard.GetState`) and compare with the previous one to detect presses.
- Dispose graphics resources you create (`RenderTarget2D`, `Texture2D.FromStream`) and let `ContentManager` own the ones it loaded.
- Use `SamplerState.PointClamp` for pixel art, and set the back buffer size once at startup.
- Keep Update free of allocation (no `new` in the loop, no LINQ) to avoid GC hitches.

## Avoid
- Content files copied to the output without the pipeline: load fails at runtime. Register them in the mgcb file.
- `Content.Load` inside `Update` or `Draw`: disk reads every frame. Load once in `LoadContent`.
- Using frame count for motion: speed varies with machine. Scale by dt.
- Nested `SpriteBatch.Begin` without `End`: throws. Finish one batch before beginning another.
- Accessing graphics objects from a background thread: undefined behaviour. Do the GPU work on the game thread.
- Game logic coupled to `Game1`: untestable. Extract classes with no MonoGame types where possible.

## Review
- [ ] Every asset is in the content project and loaded once.
- [ ] Movement and timers use elapsed time.
- [ ] No per-frame allocations in Update and Draw.
- [ ] Logic classes are tested without a GraphicsDevice.
- [ ] Disposable resources have a clear owner.
