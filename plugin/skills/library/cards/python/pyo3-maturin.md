---
name: pyo3-maturin
title: PyO3 and maturin
area: python
tags: [python, rust, pyo3, maturin, extension, ffi]
detect: [dep:pyo3, dep:maturin, file:Cargo.toml]
related: [python-packaging, pytest, uv, nox-tox]
---
Rust extension modules for Python with PyO3, built and published with maturin.

## Verify
- `maturin develop`: builds the extension and installs it into the active virtualenv (add `--release` to time it).
- `pytest -q`: the Python tests against the freshly built module.
- `cargo test`: Rust unit tests (may need `--no-default-features` if `extension-module` blocks linking).
- `cargo clippy -- -D warnings`: Rust lints.
- `maturin build --release`: a wheel builds into `target/wheels`.

## Test first
Test the Python-visible behavior from pytest after `maturin develop`.
```python
import pytest
import mylib

def test_parse_rejects_empty():
    with pytest.raises(ValueError):
        mylib.parse("")

def test_sum_releases_gil_result_matches():
    assert mylib.sum_squares(list(range(5))) == 30
```
Rust-only logic gets plain `#[test]` functions in the crate, kept free of `Python` where possible.

## Do
- Declare `[lib] crate-type = ["cdylib"]` and `name` matching the `#[pymodule]` function name.
- Configure `[build-system] requires = ["maturin>=1,<2"]`, `build-backend = "maturin"` and `[tool.maturin]` in `pyproject.toml`.
- Return `PyResult<T>` and map Rust errors with `PyErr::new::<PyValueError, _>(msg)` or `impl From<MyErr> for PyErr`.
- Use `py.allow_threads(|| ...)` (named `detach` in newer PyO3) around long pure-Rust work so other Python threads run.
- Accept borrowed inputs (`&str`, `&[u8]`, `PyReadonlyArray` via the numpy crate) to avoid copies.
- Ship type information: a `.pyi` stub next to the module and a `py.typed` marker.
- Build wheels for each target in CI (`maturin-action` or `cibuildwheel`); set `abi3` features if one wheel per OS is enough.
- Use `maturin develop` for the loop and `maturin build --release` for what ships.

## Avoid
- Benchmarking or shipping a debug build: `maturin develop` is unoptimized by default. Use `--release`.
- `unwrap()` and `panic!` in exported functions: surfaces as `PanicException`. Return errors.
- Holding the GIL through long computation or I/O: freezes Python threads. Release it.
- PyO3 API names from old tutorials (`&PyModule` with `Python<'_>` pools, `#[pymodule] fn m(_py, m: &PyModule)`): newer releases use `Bound<'_, PyModule>`. Check the pinned PyO3 version's guide.
- Mismatched module names between `[lib] name`, `#[pymodule]` and `module-name`: `ImportError: dynamic module does not define module export function`.
- `pip install .` with the Rust toolchain missing in CI: fails late. Install Rust or use prebuilt wheels.
- Importing from the source directory instead of the installed build: tests pass against stale code. Run from the installed environment.

## Review
- [ ] Rust errors map to specific Python exceptions with messages.
- [ ] Long work releases the GIL; no `unwrap` on user input.
- [ ] Module names agree across Cargo, `pyproject.toml` and `#[pymodule]`.
- [ ] CI builds release wheels for every supported platform and Python.
- [ ] Python tests run against the built wheel, not the source tree.
