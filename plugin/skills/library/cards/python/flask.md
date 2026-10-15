---
name: flask
title: Flask
area: python
tags: [python, web, wsgi, flask, blueprints, jinja]
detect: [dep:flask, dep:Flask]
related: [sqlalchemy, alembic, pytest, httpx, ruff]
---
Flask apps: application factory, blueprints, request/app contexts, Jinja templates, config from env.

## Verify
- `flask --app app routes`: the app imports through its factory and routes register.
- `pytest -q`: the suite using `app.test_client()`.
- `ruff check . && ruff format --check .`: lint and format.
- `flask --app app db upgrade --sql` (Flask-Migrate only): migrations render to SQL.

## Test first
Build the app from a factory with test config. Fixtures live in `tests/conftest.py`.
```python
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SECRET_KEY": "t"})
    return app.test_client()

def test_missing_title_is_400(client):
    r = client.post("/posts", json={})
    assert r.status_code == 400
```

## Do
- Use `create_app(config)` and register blueprints inside it; avoid a global `app` that imports everything.
- Create extensions unbound (`db = SQLAlchemy()`) and call `init_app(app)` in the factory.
- Load config with `app.config.from_prefixed_env()` or `from_object`; keep secrets out of the repo.
- Use `current_app` and `g` inside requests; push `app.app_context()` in scripts and tests that need them.
- Register `@app.errorhandler` for 404/500 and domain errors; return JSON for API blueprints.
- Validate input with a schema layer (pydantic or marshmallow) rather than reading `request.json` keys ad hoc.
- Run production under gunicorn or waitress, never `app.run`.

## Avoid
- `app.run(debug=True)` or `FLASK_DEBUG=1` on a reachable host: the debugger allows remote code execution. Keep it local only.
- `render_template_string` with user input, or `|safe` on user data: template injection and XSS. Let Jinja autoescape.
- `request.json["x"]` with no check: a missing key is a 400 or 500. Use `request.get_json(silent=True)` and validate.
- Importing `app` into blueprints (circular imports): use `current_app` or the factory pattern.
- Touching `db.session` or `current_app` outside an app context: `RuntimeError: Working outside of application context`. Push the context.
- A hardcoded `SECRET_KEY`: sessions can be forged. Read it from env.
- Pre-2.3 idioms such as `@app.before_first_request`: removed. Do the setup in the factory.

## Review
- [ ] Config and secrets come from the environment; debug is off outside local runs.
- [ ] Blueprints do not import the app object; extensions use `init_app`.
- [ ] Every input is validated and every failure path returns a deliberate status.
- [ ] Tests use the factory with `TESTING=True` and an isolated database.
- [ ] User-controlled data never reaches `Markup`, `|safe` or `render_template_string`.
