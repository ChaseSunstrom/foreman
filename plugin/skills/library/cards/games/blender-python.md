---
name: blender-python
title: Blender Python (bpy)
area: games
tags: [blender, python, bpy, addon, 3d, scripting]
detect: [dep:bpy, file:blender_manifest.toml, file:*.blend, ext:.blend]
related: [python, pytest]
---
Blender scripting and add-ons: the bpy API, operators and properties, headless runs with `blender --background`.

## Verify
- `blender --background --factory-startup --python-exit-code 1 --python tests/run.py`: the test script runs headless; a Python error gives exit code 1.
- `blender --background --factory-startup --python-expr "import addon_name"`: the add-on imports in a clean Blender.
- `blender --command extension build`: the extension package builds from `blender_manifest.toml`.
- `ruff check .`: lint, since Blender's Python is plain CPython.

## Test first
Use `unittest` inside Blender's Python; a runner script discovers tests and sets the exit code.
```python
# tests/run.py
import sys, unittest
import bpy

class TestOps(unittest.TestCase):
    def test_add_cube_sets_name(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.mesh.primitive_cube_add()
        self.assertEqual(bpy.context.active_object.name, "Cube")

suite = unittest.defaultTestLoader.discover("tests", pattern="test_*.py")
sys.exit(0 if unittest.TextTestRunner().run(suite).wasSuccessful() else 1)
```
Keep geometry and math in functions that take plain data so most tests run in ordinary pytest without bpy.

## Do
- Reset state per test with `bpy.ops.wm.read_factory_settings(use_empty=True)`.
- Prefer the data API (`bpy.data.objects`, `bpy.data.meshes.new`, `bmesh`) over `bpy.ops` for scripted geometry; ops depend on context.
- Register classes in `register()` and unregister in reverse in `unregister()`; use `bpy.utils.register_class`.
- Declare operators with `bl_idname` (`category.name`, lowercase), `bl_label`, and return `{'FINISHED'}` or `{'CANCELLED'}`.
- Put properties on classes with annotations: `my_prop: bpy.props.FloatProperty(...)`.
- Use `blender_manifest.toml` for extensions: `id`, `version`, `blender_version_min`, `permissions`.
- When ops need context, use `with bpy.context.temp_override(...)`.
- Free bmesh with `bm.free()` and update meshes with `bm.to_mesh(me)`; call `me.update()`.

## Avoid
- Property assignment with `=` instead of annotation `:` in classes: ignored in 2.8+. Use annotations.
- Overriding `context` via a dict argument to `bpy.ops` calls: removed in 4.0. Use `temp_override`.
- `import bpy` outside Blender in tests: fails unless the `bpy` wheel is installed. Isolate pure logic.
- Reading `bpy.context` during register or from threads: restricted. Defer with `bpy.app.timers.register`.
- Holding references to `bpy.data` objects across undo or file load: they become invalid. Re-look up by name.
- Heavy loops calling `bpy.ops` per element: slow and context-fragile. Use `bmesh`, `foreach_set` or numpy.
- Leaving handlers (`bpy.app.handlers`) registered after unregister: leaks and duplicates. Remove them.

## Review
- [ ] Register and unregister are symmetric, including handlers, keymaps and menus.
- [ ] Tests run headless with `--factory-startup` and exit non-zero on failure.
- [ ] No `bpy.ops` calls that depend on an interactive context outside `temp_override`.
- [ ] `blender_manifest.toml` version bounds and permissions match what the code uses.
- [ ] Pure logic is separated from bpy so it is unit-testable.
