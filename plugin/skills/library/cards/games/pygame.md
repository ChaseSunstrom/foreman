---
name: pygame
title: pygame
area: games
tags: [pygame, python, game, sprites, clock, surface]
detect: [dep:pygame, dep:pygame-ce]
related: [game-loop, game-physics, pathfinding, pytest]
---
pygame games: one event loop, `Clock` for pacing, Surfaces and sprite groups, logic separated so pytest can run it headless.

## Verify
- `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy pytest -q`: tests run with no display or audio device.
- `ruff check . && ruff format --check .`: lint and format.
- `python -c "import pygame; print(pygame.version.ver)"`: pygame imports in this environment.
- `SDL_VIDEODRIVER=dummy python -m mygame --frames 120`: only if the game offers a frame limit flag for headless smoke runs.

## Test first
Put rules in plain classes with an explicit `dt`. Use the dummy video driver only for rendering tests.
```python
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame
from game.player import Player

def test_player_moves_by_speed_times_dt():
    p = Player(x=0, speed=100)
    p.update(0.5)
    assert p.x == 50

def test_player_rect_stays_in_bounds():
    p = Player(x=790, speed=100)
    p.update(1.0)
    assert p.rect.right <= 800
```

## Do
- Call `pygame.init()` once, create the display with `pygame.display.set_mode`, and `pygame.quit()` in a `finally`.
- Pace the loop with `dt = clock.tick(60) / 1000`, and use dt in all movement.
- Drain input with `for event in pygame.event.get()` every frame. Use `get_pressed()` for held keys.
- Call `convert()` or `convert_alpha()` on loaded images once after `set_mode`, and load assets before the loop.
- Use `pygame.sprite.Group` and `groupcollide` or `spritecollide` for collisions, and `pygame.Rect` methods for geometry.
- Keep positions as floats (a `Vector2`) and derive the integer `rect` for drawing, since Rect truncates.
- Use `pygame.display.flip()` or `update()` once per frame, after drawing everything.

## Avoid
- Not calling `pygame.event.get()` (or `pump`): the window freezes as not responding. Drain events every frame.
- `time.sleep` for pacing: jittery. Use `Clock.tick`.
- Loading images or fonts inside the loop: slow. Load once and keep references.
- Storing fractional motion in `Rect`: slow movement rounds to zero. Keep float state and assign to the rect.
- Running tests with a real display: CI fails without a display. Set the SDL dummy drivers.
- Mixing `pygame` and `pygame-ce` in one environment: import conflicts. Install only one.

## Review
- [ ] All motion and timers use dt from the clock.
- [ ] The event queue is drained every frame, and quit is handled.
- [ ] Assets load once before the loop, with `convert` applied.
- [ ] Game rules sit in classes tested headless.
- [ ] Only one of pygame or pygame-ce is a dependency.
