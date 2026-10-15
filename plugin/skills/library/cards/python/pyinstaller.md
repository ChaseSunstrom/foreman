---
name: pyinstaller
title: PyInstaller
area: python
tags: [python, packaging, executable, bundle, distribution, build]
detect: [dep:pyinstaller, file:*.spec]
related: [python-packaging, uv, cython, pytest]
---
PyInstaller: freeze a Python app into a one-folder or one-file executable, with explicit data files and hidden imports.

## Verify
- `pyinstaller --clean --noconfirm app.spec`: builds from the committed spec (or `pyinstaller --name app src/app/__main__.py` first time).
- `./dist/app/app --version`: the frozen binary starts on the build OS (smoke test the artifact, not the source).
- `pyinstaller --log-level WARN app.spec`: lists missing hidden imports and modules.
- `pyi-archive_viewer dist/app/app`: confirms data files and modules are inside the bundle (one-file builds).

## Test first
The check that fails first is the frozen binary, on a clean machine or container.
```python
import subprocess, sys, pathlib

def test_frozen_binary_starts():
    exe = pathlib.Path("dist/app/app")
    r = subprocess.run([str(exe), "--version"], capture_output=True, text=True, timeout=30)
    assert r.returncode == 0 and r.stdout.strip()
```
Run it as a post-build CI step. Test source behaviour with pytest as usual.

## Do
- Commit the `.spec` file and build from it, so hooks, data files and options are reviewable.
- Prefer one-folder (`onedir`, the default) for startup speed and debugging. Use `--onefile` only when a single file is required.
- Add data with `datas=[("src/app/templates", "app/templates")]` and locate it at runtime through `sys._MEIPASS` when `getattr(sys, "frozen", False)`.
- Declare dynamic imports with `hiddenimports=[...]` or `collect_submodules`, `collect_data_files` from `PyInstaller.utils.hooks`.
- Build in a clean virtualenv with only runtime dependencies, so the bundle stays small.
- Build on each target OS and architecture: no cross compilation.
- Use `multiprocessing.freeze_support()` in `if __name__ == "__main__":` for apps using multiprocessing.
- Pin PyInstaller and `pyinstaller-hooks-contrib` in the build requirements.

## Avoid
- Relying on `__file__` for resource paths: points into a temp dir or the wrong place. Resolve via `sys._MEIPASS` when frozen.
- Using `--onefile` with large dependencies and fast-start needs: each run unpacks to a temp dir. Use `onedir`.
- Ignoring "hidden import not found" warnings: the app crashes at runtime on the first dynamic import. Add it in the spec.
- Bundling secrets or `.env` files: they are extractable. Load config at runtime.
- Skipping `--noconsole` (`console=False`) for GUI apps, or using it before debugging: console errors vanish. Debug with a console build first.
- UPX compression by default: triggers antivirus false positives and breaks some DLLs. Set `upx=False` unless measured.
- Shipping unsigned binaries on macOS and Windows: users get blocked. Sign and notarize.

## Review
- [ ] The spec is committed and the CI builds and runs the binary.
- [ ] Data files and dynamic imports are listed, and the smoke test touches them.
- [ ] Resource lookup works frozen and unfrozen.
- [ ] Build is reproducible from pinned requirements in a clean env.
