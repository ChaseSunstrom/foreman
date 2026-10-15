---
name: godot
title: Godot
area: games
tags: [godot, gdscript, game, engine, scenes, gut]
detect: [file:project.godot, ext:.gd, ext:.tscn]
related: [csharp]
---
Godot 4 projects: GDScript, scene trees, signals, resources, headless runs and GUT or gdUnit4 tests.

## Verify
- `godot --headless --path . --quit`: the project loads headless with no script parse errors in the log.
- `godot --headless --path . -s addons/gut/gut_cmdln.gd -gdir=res://tests -gexit`: GUT tests pass and the process exits with a failing code on failure.
- `godot --headless --path . --check-only -s res://scripts/player.gd`: one script parses.
- `git diff --stat -- '*.tscn' '*.tres'`: scene and resource diffs stay small and intentional.

## Test first
Tests live in `res://tests`, files named `test_*.gd`, extending `GutTest` (or the gdUnit4 equivalent).
```gdscript
extends GutTest

func test_damage_clamps_at_zero():
    var h := Health.new(10)
    h.damage(50)
    assert_eq(h.current, 0)

func test_died_signal_emitted():
    var h := Health.new(1)
    watch_signals(h)
    h.damage(1)
    assert_signal_emitted(h, "died")
```
Keep logic in scripts that do not need the scene tree; use `add_child_autofree()` for nodes that do.

## Do
- Use static typing (`var x: int`, `func f(a: float) -> void`) and `@export` for inspector values.
- Communicate upward with signals, downward with method calls: "call down, signal up".
- Use `@onready var n := $Path` or unique names (`%Name`) rather than `get_node` in `_process`.
- Put tunable data in custom `Resource` classes (`class_name`), saved as `.tres`.
- Do physics in `_physics_process(delta)` and use `delta` for all motion.
- Use `await` with signals or timers (`get_tree().create_timer(1.0).timeout`).
- Use `preload` for constant paths, `load` for dynamic ones; use autoloads sparingly.

## Avoid
- Godot 3 syntax in 4 projects: `onready`, `export`, `yield`, `connect("sig", obj, "method")`. Use `@onready`, `@export`, `await`, `sig.connect(callable)`.
- `KinematicBody2D` and old node names: renamed to `CharacterBody2D` and so on. Check the 4.x class reference.
- `get_node` or `find_child` every frame: cache in `@onready`.
- Calling `queue_free()` then using the node in the same frame: check `is_instance_valid(node)`.
- Hardcoded `res://` strings scattered everywhere: moving a file breaks them silently. Use `preload`, exported `PackedScene` or constants.
- Editing `.godot/` or committing it: it is generated cache, so ignore it.
- Big logic in autoload singletons that cannot be tested: pass dependencies in.

## Review
- [ ] Scripts are typed and no Godot 3 API remains.
- [ ] Signals are connected once and disconnected or auto-freed with the node.
- [ ] `_process` and `_physics_process` do no node lookups or allocation.
- [ ] `.godot/` and export credentials are ignored; `.import` churn is not committed.
- [ ] New behavior has a GUT or gdUnit4 test that fails without the change.
