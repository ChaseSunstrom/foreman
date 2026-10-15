---
name: godot-gdscript
title: GDScript
area: games
tags: [godot, gdscript, signals, scenes, typing, gdunit]
detect: [ext:.gd, file:project.godot]
related: [godot, game-loop, game-physics]
---
GDScript in Godot 4: statically typed scripts, signals up and calls down, scenes as reusable nodes.

## Verify
- `godot --headless --path . --check-only --script res://path/script.gd`: that script parses with no errors.
- `godot --headless --path . --quit`: the project loads and autoloads initialise without errors.
- `godot --headless --path . -s addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://tests`: GdUnit4 suite runs (only when that addon is installed).
- `gdlint . && gdformat --check .`: style and format (only when gdtoolkit is installed).

## Test first
Keep logic in `RefCounted` classes so tests need no scene tree.
```gdscript
# tests/test_health.gd (GdUnit4)
extends GdUnitTestSuite

func test_damage_clamps_at_zero() -> void:
    var h := Health.new(10)
    h.damage(99)
    assert_int(h.current).is_equal(0)
```

## Do
- Type everything: `var speed: float = 200.0`, `func hit(dmg: int) -> void`. Typed code is faster and the editor catches mistakes.
- Signals up, calls down: a child emits, the parent connects. Never reach upward with `get_parent().get_parent()`.
- Use `@export` for tunables and `@onready var x: Node = $Path` for child refs. Use `%UniqueName` for stable lookups.
- Put movement and physics in `_physics_process(delta)`, input in `_unhandled_input`, visuals in `_process`.
- Use `Resource` subclasses (`class_name`) for data such as items and stats, saved as `.tres`.
- Use autoloads sparingly, for truly global services such as an event bus or save system.
- Free nodes with `queue_free()`, and await with `await get_tree().create_timer(t).timeout`.

## Avoid
- `get_node("../../Thing")` chains: they break when the scene is reorganised. Export a `NodePath` or emit a signal.
- Moving bodies by setting `position` every frame: it ignores collisions. Use `velocity` with `move_and_slide()`.
- Untyped `var` with Variant inference everywhere: errors surface at runtime. Add type hints.
- Calling `free()` on a node during its own signal or physics callback: use `queue_free()`.
- Connecting a signal in `_ready` and again on re-entry: duplicate calls. Check `is_connected` or use `CONNECT_ONE_SHOT`.
- Storing node references in autoloads across scene changes: they dangle. Check `is_instance_valid`.

## Review
- [ ] Public functions and exports are typed, with no new untyped Variant.
- [ ] No upward `get_parent()` coupling; communication uses signals.
- [ ] Physics code lives in `_physics_process` and uses `delta`.
- [ ] Data is in Resources, not hard-coded dictionaries scattered through scripts.
- [ ] Headless load of the project exits clean.
