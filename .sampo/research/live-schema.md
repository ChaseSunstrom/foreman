# sampo live: the shared contract (T-2997)

**Server: `sampo live [--port N]`**
- Python stdlib http.server only. Bound to 127.0.0.1 only.
- Auth reuses settingsserve's model: a one-time token URL, swapped for an HttpOnly SameSite=Strict cookie; a Host check against DNS rebinding; a strict CSP with nonces.
- It runs until stopped. No idle timeout: it is meant to stay up.
- It writes its URL to the project's state (live.url) so `sampo live --url` reprints it.
- Read-only: it never changes state.

**Endpoints**
- `GET /` serves the page (HTML, plus /static/live.css and /static/live.js from plugin/web/live/).
- `GET /api/state` returns one snapshot (JSON below).
- `GET /api/stream` is Server-Sent Events: a `state` event every 2 s, with the full snapshot (small).

**Snapshot JSON**

```
{
 "at": "2026-11-04T18:30:00Z",
 "project": {"slug": "foreman-4a056f", "drive": true, "autonomy": "standard"},
 "focus": {"id": "T-2995", "title": "...", "step": "3/3", "stage": "executing"} | null,
 "queue": [{"id", "title", "type", "tier", "status"}],              // up to 12
 "closed_today": [{"id", "title", "at"}],                             // newest first, up to 30
 "lanes": [{"task", "title", "model", "since"}],                      // builder lanes out now
 "jobs": [{"name", "kind": "funnel|grow|exam|train|bench|check|other", "pid", "since",
           "model": "profile or model name or null", "progress": {"done", "total"} | null, "line": "short status"}],
 "models": [{"name", "family": "claude|ollama|jeff|jarvis|embed", "where": "cloud|gpu|cpu|remote",
             "loaded": true, "vram_mb": 9728, "calls_5m": 12, "last_call": "iso" | null}],
 "gpu": {"name", "used_mb", "total_mb", "util_pct"} | null,
 "flows": [{"from": "card grow", "to": "haiku", "kind": "write|judge|embed|train|plan|act|review", "at": "iso"}],   // last 60 s
 "events": [{"at", "kind", "text"}],                                   // newest first, up to 60
 "stats": {"cards": {"general": 1894, "ui": 125, "ui_cells": 28, "grid_ui": 3840},
           "moons": {"candidates": 10007, "stages": {"kill": {"kept", "rejected", "waiting"}, ...}},
           "bench": [{"use", "contestant", "accuracy", "coverage"}],    // latest per use, top 5
           "closed_today": 23}
}
```

**Where the data comes from**
- **Focus, queue and closed_today:** briefs, via core.
- **Lanes:** lane metadata in briefs (builder, builder_model, lane).
- **Jobs:**
  - live processes matched by command line (sampo moons funnel, playbooks small grow, exam run, exam models, check, jeff-train);
  - `progress` from the funnel status, card coverage and the exam run meta when cheap.
- **Models:**
  - models.json profiles;
  - Ollama `GET http://127.0.0.1:11434/api/ps` for loaded models and VRAM;
  - the Jeff server's /v1/models for its adapters;
  - claude models seen in the ledger or usage records.
- **Flows:** the last 60 s of model calls from whatever the code already logs: the ledger's model, usage or cost events, and moons and cards events. Each call is a from-to pair: the caller (job or session) and the model.
- **GPU:** `nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits` (absent becomes null).
- **Events:** state/events.jsonl and the project ledger, newest first, plain text, with secrets redacted (core.redact).

Every collector is cheap (no model calls, no network beyond 127.0.0.1) and fails soft: an empty field, never a 500.
